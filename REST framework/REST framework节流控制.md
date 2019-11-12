# REST framework 节流控制源码

## 节流

节流就是控制用户对接口的访问频率，可以通过用户IP或用户对象进行节流

## 源码流程

从dispatch进入initial

```py
def initial(self, request, *args, **kwargs):
    # ...
    self.check_throttles(request)
```

```py
def check_throttles(self, request):
    for throttle in self.get_throttles():
        if not throttle.allow_request(request, self):
            # 访问频繁，把认证类对象的wait()方法的返回值传递给throttled
            self.throttled(request, throttle.wait())
```

```py
def get_throttles(self):
    # 产生节流类对象列表
    return [throttle() for throttle in self.throttle_classes]
```

```py
throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
```

所有过程与认证，权限一样，`get_throttles()`先从当前的视图类里寻找`throttle_classes`字段，找不到就到父类`APIView`中找，父类中的这个字段由配置文件中的`DEFAULT_THROTTLE_CLASSES`定义。找到后，产生`throttle_classes`列表（节流类列表）的对象列表（节流类对象列表）。  
然后在`check_throttles()`中遍历节流类对象列表，如果节流类对象的`allow_request()`方法返回`False`进入`throttled()`，阻止访问，反之通过验证。

```py
def throttled(self, request, wait):
    # 错误 429 Too Many Requests
    raise exceptions.Throttled(wait)
```

一旦`allow_request()`方法返回`False`进入`throttled()`就会抛出`Throttled(wait)`异常，这是一个429错误。

```py
class Throttled(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('Request was throttled.')
    extra_detail_singular = 'Expected available in {wait} second.'
    extra_detail_plural = 'Expected available in {wait} seconds.'
    default_code = 'throttled'

    def __init__(self, wait=None, detail=None, code=None):
        if detail is None:
            # 错误详情
            detail = force_text(self.default_detail)
        if wait is not None:
            # 需要等待多长时间才能继续访问
            wait = math.ceil(wait)
            detail = ' '.join((
                detail,
                force_text(ungettext(self.extra_detail_singular.format(wait=wait),
                                     self.extra_detail_plural.format(wait=wait),
                                     wait))))
        self.wait = wait
        super(Throttled, self).__init__(detail, code)
```

在错误信息里，认证类对象中wait()的返回值将会作为需要等待的时间展示在错误信息里。

## 自定义节流控制类

## 内置节流控制类

### SimpleRateThrottle

```py
def __init__(self):
    if not getattr(self, 'rate', None):
        self.rate = self.get_rate()
    self.num_requests, self.duration = self.parse_rate(self.rate)
```

在初始化时，先找rate这个属性，如果找不到，使用`self.get_rate()`获取rate的值

```py
def get_rate(self):
    if not getattr(self, 'scope', None):
        msg = ("You must set either `.scope` or `.rate` for '%s' throttle" %
                self.__class__.__name__)
        raise ImproperlyConfigured(msg)

    try:
        return self.THROTTLE_RATES[self.scope]
    except KeyError:
        msg = "No default throttle rate set for '%s' scope" % self.scope
        raise ImproperlyConfigured(msg)
```

而在`get_rate()`中，先判断有没有scope属性，没有抛出异常，有的话以这个属性的值作为键在配置文件中对应的值，找到的值作为频率返回，否则也抛出异常。