# Django REST framework 框架

django中间件（最多五个方法）权限，登录认证，csrf（view 检查视图是否被免除csrf认证）

@csrf_protect
@csrf_exempt

CBV装饰器：

```py
from ddjango.utils.decorators import method_decorator

@method_decorator(csrf_exempt)
def dispatch():


@method_decorator(csrf_exempt, name="dispatch")
class Demo()
```

为什么用： 前后端分离，分工明细

FBV CBV 基于函数的视图和基于类的视图

CBV 自动分发
FBV 

反射，getattr(),根据请求方式不同执行不同方法
    路由对应view方法，方法对应dispatch， dispatch反射不同

```py
from django.views import View
class DemoView(view):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')

    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('DELETE')
```

dispatch()

```py
url("",views.DemoView.as_view())
```

> Postman工具

```py
class Foo:
    pass

class Bar:
    pass

# 对象列表
v = [item() for item in [Foo, Bar]]
```

CBV

本质：反射
流程：路由，View，dispatch反射
装饰器，dispatch

restful规范：
1. 一条数据使用一个url，根据methor区分
2. 建议使用https
3. 建议使用专用域名（子域名【跨域问题】或专用url）
4. 版本
5. 面向资源编程（url名词）
6. method： get post put patch delete
7. 过滤，url加条件
8. 状态码code
9. 错误处理
10. 返回值

REST 


