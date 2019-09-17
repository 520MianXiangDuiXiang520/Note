# Django中的用户身份认证

[原文档](https://docs.djangoproject.com/zh-hans/2.1/topics/auth/)

Django附带一个用户身份验证系统。它处理用户帐户、组、权限和基于cookie的用户会话。  

Django的身份认证包括认证和授权两部分。

* 认证是判断请求服务的用户是不是他们自称的“用户”
* 授权决定 **通过认证**的用户能做哪些事情

Django用户认证依赖于`django.contrib`中的两个包

* `django.contrib.auth`:这里包含身份认证的核心以及相关模型
* `django.contrib.contenttypes`：允许把用户权限与模型关联

与之相关的还有两个中间`SessionMiddleware` 和 `AuthenticationMiddleware` 用于管理请求

## User对象

User对象是整个Django用户认证的核心，框架中所有用户都来源于这一个类。主要有五个属性：username,password,email,first和last name

### 创建用户

创建用户最简单的方法是使用`create_user()`方法，【在这之前要迁移和创建数据表啊】

```python
user = User.objects.create_user('dapeng', 'dapeng@souhu.com', 'password')
user.save()
```

### 更改密码

Django不会在数据库明文储存密码（犯法的）保存的是哈希值，所以直接对数据库中的密码选项做修改是没意义的，所以Django提供了几种修改密码的函数：

* 在命令行中修改

```shell
python manage.py changepassword *username*
```

如果不提供username，会修改当前系统用户密码

* 使用`set_password()`方法

```python
u = User.objects.get(username='dapeng')
u.set_password('new password')
u.save()
```

### 验证用户

使用 `authenticate()` 来验证用户。它使用 `username` 和 `password` 作为参数来验证,如果验证通过，则会返回一个User对象，否则返回None

```python
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
```

## 权限和认证

Django 带有一个简单的权限系统。它提供了为指定的用户和用户组分配权限的方法。

## Web请求的认证

Django 使用 sessions 和中间件将身份验证系统挂接到请求对象中。

它们在每次请求中都会提供 request.user 属性。如果当前没有用户登录，这个属性将会被设置为 AnonymousUser ，否则将会被设置为 User 实例。

你可以使用 is_authenticated 区分两者

```py
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```

### 用户登录

要在views中让用户登录，使用 login() 。它需要 HttpRequest 对象和 User 对象。通过 Django 的 session 框架， login() 会在 session 中保存用户的ID。

```python
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```

### 用户登出

已经登录的用户可以使用logout登出，需要传入HttpRequest对象，没有返回值

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
```

如果用户未登录，logout() 不会报错
