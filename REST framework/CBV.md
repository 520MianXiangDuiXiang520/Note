# Django CBV

Django 视图有两种表示方法，常见FBV（function base view）和CBV（class base view），就是使用函数创建视图和用类创建的区别

创建CBV视图必须继承自django的View

```py
from django.shortcuts import render, HttpResponse
from django.views import View


# Create your views here.
class ShopView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("get")

    def post(self, request, *args, **kwargs):
        return HttpResponse("post")

    def put(self, request, *args, **kwargs):
        return HttpResponse("put")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("delete")
```

```py
urlpatterns = [
    path('shop/', views.ShopView.as_view()),
]
```

CBV会根据请求的方式（methor）的不同选择不同的方法

## 原理-反射

请求会先给url调度器，调度器会把请求直接传递给dispath,dispath根据不同的method决定使用哪个方法。

```py
def dispatch(self, request, *args, **kwargs):
    # Try to dispatch to the right method; if a method doesn't exist,
    # defer to the error handler. Also defer to the error handler if the
    # request method isn't on the approved list.

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    # 如果请求方式是self.http_method_names中的一种
    if request.method.lower() in self.http_method_names:
        # 反射,从当前对象寻找名为 method.lower() 的方法或属性，如果存在，handler就为这个方法或属性
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    else:
        # 否则返回HttpResponseNotAllowed对象
        handler = self.http_method_not_allowed
    # 最后返回的其实是我们定义的get等方法
    return handler(request, *args, **kwargs)
```

## CBV 处理CSRF

在FBV模式下，取消CSRF验证可以使用`@csrf_exempt`但是在CBV模式下，`@csrf_exempt`的被装饰函数应该是`dispatch()`

```py
class ShopView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        print("自定义的dispatch 开始")
        ret = super().dispatch(request, *args, ** kwargs)
        print("自定义的dispatch 结束")
        return ret
```

也可以

```py
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ShopView(View):
    pass
```
