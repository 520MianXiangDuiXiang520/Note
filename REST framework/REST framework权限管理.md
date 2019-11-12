# REST framework 权限管理源码分析

同认证一样，dispatch()作为入口，从`self.initial(request, *args, **kwargs)`进入`initial()`

```py
    def initial(self, request, *args, **kwargs):
        # .......
        # 用户认证
        self.perform_authentication(request)
        # 权限控制
        self.check_permissions(request)
        # ...
```

`check_permissions()`便是权限管理源码的入口

```py
    # 权限管理
    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
```

和用户认证一样，同样遍历一个权限类对象列表，并且调用该列表中元素的`has_permission()`方法，该方法返回布尔值，`True`代表有权限，`False`代表没有权限.

```py
    def get_permissions(self):
        return [permission() for permission in self.permission_classes]
```

如果没有权限，就调用`permission_denied()`

```py
    def permission_denied(self, request, message=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message)
```

如果使用了REST的认证框架（authentication_classes数组不为空）并且身份认证失败，就抛出**NotAuthenticated**异常，否则会抛出**PermissionDenied**异常

```py
class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated'
```

NotAuthenticated会导致一个401错误（缺少用户凭证）  

```py
class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'permission_denied'
```

而PermissionDenied会返回**错误403**（拒绝授权访问）

在向`permission_denied()`类传递参数时，使用了反射

```py
self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
```

会在这个权限类对象中寻找`message`属性，没找到就使用`None`,而这个参数在后来只会被用在PermissionDenied异常上，这些异常都继承自APIException,而在APIException的构造器中，可以发现detail参数就是异常描述，而在自己的权限类中定义message属性可以改变认证失败后的描述

```py
class APIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
    # ...
```

## 示例

```py
# api/utils/Permission.py
from rest_framework.permissions import BasePermission


class CommonPermission(BasePermission):
    """
    普通用户权限，作用于全局
    """
    def has_permission(self, request, view):
        print(request.user)
        if request.user.user_type == 1:
            return True

    def has_object_permission(self, request, view, obj):
        """
        一旦获得View权限，将获得所有object权限
        :return: True
        """
        return True


class VipPermission(BasePermission):
    """
    VIP 用户权限
    """
    message = '您首先要称为VIP才能访问'
    
    def has_permission(self, request, view):
        print(request.user)
        if request.user.user_type == 2:
            return True

    def has_object_permission(self, request, view, obj):
        return True

```

```py
# api/view.py
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from api.utils.Permission import VipPermission


class LoginView(APIView):
    authentication_classes = []
    # 登录无需权限认证
    permission_classes = []

    def post(self, request, *args, **kwargs):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class ShopView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(request.user.username)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')



class VipIndexView(APIView):
    """
    只授权给VIP用户查看
    """
    permission_classes = [VipPermission]

    def get(self, *args, **kwargs):
        return JsonResponse("welcome VIP ", safe=False)

```

```py
# RESTdemo.setting.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['api.utils.MyAuthentication.MyAuthentication'],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'DEFAULT_PERMISSION_CLASSES': ['api.utils.Permission.CommonPermission']
}
```