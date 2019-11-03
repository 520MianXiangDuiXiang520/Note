# REST 用户认证源码

在Django中，从URL调度器中过来的HTTPRequest会传递给disatch(),使用REST后也一样

```py
# REST的dispatch
def dispatch(self, request, *args, **kwargs):
    """
    `.dispatch()` is pretty much the same as Django's regular dispatch,
    but with extra hooks for startup, finalize, and exception handling.
    """
    self.args = args
    self.kwargs = kwargs
    request = self.initialize_request(request, *args, **kwargs)
    self.request = request
    self.headers = self.default_response_headers  # deprecate?

    try:
        self.initial(request, *args, **kwargs)

        # Get the appropriate handler method
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                                self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        response = handler(request, *args, **kwargs)

    except Exception as exc:
        response = self.handle_exception(exc)

    self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response
```

代码第三行通过一个方法`initialize_request()`重新分装了原来从URL调度器传来的request对象，并且返回的也是一个request对象，具体分装的内容：

```py
    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        parser_context = self.get_parser_context(request)
        return Request(
            request,
            parsers=self.get_parsers(), # 解析器
            authenticators=self.get_authenticators(), # 用于身份验证
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )
```

`initialize_request()`返回的是一个Request对象

```py
class Request(object):

    def __init__(self, request, parsers=None, authenticators=None,
                 negotiator=None, parser_context=None):
        pass
        self._request = request
        self.parsers = parsers or ()
        # ...
```

Request这个类使用"组合"将普通的httprequest分装在它的内部，除此之外还提供了用于身份验证的authenticators，用于解析请求内容的解析器（parsers）只关心authenticators  

authenticators由`self.get_authenticators()`函数返回，是个列表

```py
def get_authenticators(self):
    """
    Instantiates and returns the list of authenticators that this view can use.
    """
    return [auth() for auth in self.authentication_classes]
```

get_authenticators遍历authentication_classes，并实例化authentication_classes中的对象加入到列表中返回

```py
authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
```

实际上authentication_classes只是一个包含认证类的列表

----

已经乱了，整理一下

首先，用户会生成一个`httprequest`,这个请求到URL调度器后会执行`as_view()`

```py
path('shop/', views.ShopView.as_view())
```

而在as_view()中就会把这个原生的`httprequest`传递给`dispatch()`在`dispatch()`中会对这个`httprequest`进一步封装，在这里具体就是增加了一个`authenticators`,他是一个列表，列表中是一系列从authentication_classes列表中实例化出来的对象。

----

然后进入`try`块，执行`self.initial(request, *args, **kwargs)`,这条语句用来 “运行在调用方法处理程序之前需要发生的任何事情” 可以说是一个功能集合，聚合了认证管理，权限管理，版本控制等几个功能模块

```py
def initial(self, request, *args, **kwargs):

    self.format_kwarg = self.get_format_suffix(**kwargs)
    # 执行内容协商并存储关于请求的接受信息
    neg = self.perform_content_negotiation(request)
    request.accepted_renderer, request.accepted_media_type = neg

    # 版本控制
    version, scheme = self.determine_version(request, *args, **kwargs)
    request.version, request.versioning_scheme = version, scheme
    # 用户认证
    self.perform_authentication(request)
    # 权限控制
    self.check_permissions(request)
    # 访问频率控制
    self.check_throttles(request)
```

现在只关心用户认证的工作，进入`perform_authentication(request)`（现在的request已经是重新包装过的的request了）,也只有一句话。

```py
def perform_authentication(self, request):
    request.user
```

它调用了这个request对象的user属性，进入user,是一个属性方法,主体是调用了`self._authenticate()`

```py
@property
def user(self):
    if not hasattr(self, '_user'):
        # 只是一个上下文管理器，方便清理之类的工作
        with wrap_attributeerrors():
            self._authenticate()
    return self._user
```

现在是那个封装过的request对象调用了自己的user属性方法，所以`self`已经是request了，之前是在视图（view.py）中自己定义的ShopView

进入`self._authenticate()`

```py
    def _authenticate(self):
       
        for authenticator in self.authenticators:
            try:
                user_auth_tuple = authenticator.authenticate(self)
            except exceptions.APIException:
                self._not_authenticated()
                raise

            if user_auth_tuple is not None:
                self._authenticator = authenticator
                self.user, self.auth = user_auth_tuple
                return

        self._not_authenticated()
```

他会遍历`self.authenticators`，现在的self是那个分装过的request,所以`self.authenticators`其实就是上面列表生成式生成的那个认证类对象列表，它遍历并调用每一个认证类对象的`authenticate`方法，这个方法必须覆盖，
