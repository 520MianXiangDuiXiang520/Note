auth 用户授权相关的登录登出等

### 1.登录

首先因该建表，应为Django提供了与表单验证相关的表，但还未建立，运行
```
python manage.py migrate
```
其次，通过以下调用登录，登出，验证相关的函数
```python
from django.contrib.auth import authenticate,login,logout
```

>authenticate  验证,如果用户存在，返回一个user对象，否则返回none
>
>login 登录,login(request,user)
>
>logout 登出,logout(request)

```python
def logins(request):
    if request.method=='POST':
        user=authenticate(request,username=request.POST['用户名'],password=request.POST['密码'])
        if user==None:
            return render(request, "myauth/login.html",{'错误':'用户名或密码错误'})
        else:
            login(request,user)
            return  redirect('myauth:主页')
    else:
        return render(request,"myauth/login.html")
```
登录逻辑：  
1. 如果用户发起POST请求，将POST传入的数据传入authenticate，判断用户是否存在，存在返回一个user对象，不存在返回none
2. 如果用户不存在，返回一个错误字典，在前端通过键值配对的方式获得错误信息
3. 如果用户存在，使用login函数登录，重定向到主页

### 2.登出
直接使用logout(request)登出
```python
def logouts(request):
    logout(request)
    return redirect('myauth:主页')
```
在前端使用user.is_authenticated判断是否处在登录状态

```python
{% if user.is_authenticated %}
    <a href="{% url 'myauth:登出' %}">退出登录</a>
{% else %}
    <a href="{% url 'myauth:登录' %}">登录</a>
    <a href="{% url 'myauth:注册' %}">注册</a>
{% endif %}
```

### 3.注册
注册时Django会提供现成的表单模板和表单验证机制，需要导入

```python
from django.contrib.auth.forms import UserCreationForm
```

```python
from django.contrib.auth.forms import UserCreationForm
def zhuce(request):
    if request.method == 'POST':
    # 如果用户发起POST请求，将该请求传给表单
        froms=UserCreationForm(request.POST)
        # 如果表单填写正确
        if froms.is_valid():
            # 将表单保存到数据库
            froms.save()
            # 创建一个user对象
            user=authenticate(username=froms.cleaned_data['username'],password=froms.cleaned_data['password1'])
            login(request, user)
            return redirect('myauth:主页')
    else:
        froms = UserCreationForm()
    # 如果表单填写错误，会直接运行到此，在返回的froms中会包含一个errors,可以在前端捕获
    表单={'表单':froms}
    return render(request, "myauth/zhuce.html",表单)
```
自定义表单内容
首先要怎加数据库中表的列数
models.py中加入自定义的内容如：

```python
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# 重新创建一张表，叫普通会员表
class 普通会员表(models.Model):
    # 表中的用户信息一对一继承User表，怎加昵称和生日两个信息
    用户=models.OneToOneField(User,on_delete=models.CASCADE)
    昵称=models.CharField(blank=True,max_length=50)
    生日=models.DateField(blank=True)
    
    class Meta:
        verbose_name_plural="普通会员表"
```
新建froms.py文件，设置注册时要求用户填写的表单
```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class 自定义表单(UserCreationForm):
    昵称=forms.CharField(required=False,max_length=50)
    生日=forms.DateField(required=False)

    class Meta:
        model=User
        # 表单中显示出来的内容
        fields=('username','password1','password2','email','昵称','生日')
```
然后把之前注册时的UserCreationForm改为自定义的表单
```python
def zhuce(request):
    if request.method == 'POST':
        froms=自定义表单(request.POST)
        # 如果表单填写正确
        if froms.is_valid():
            froms.save()
            user=authenticate(username=froms.cleaned_data['username'],password=froms.cleaned_data['password1'])
            user.email=froms.cleaned_data['username']
            普通会员表(用户=user,昵称=froms.cleaned_data['昵称'],生日=froms.cleaned_data['生日']).save()
            login(request, user)
            return redirect('myauth:主页')
    else:
        froms = 自定义表单()
    表单={'表单':froms}
    return render(request, "myauth/zhuce.html",表单)
```
**自定义错误信息**
传过来的“表单”包含一个errors 的字典，其中的键是表单名，如username,password1，等，可以通过判断某个键是否存在判断某个错误是否发生，以此实现自定义表单
```Django
 {% if 表单.errors.username %}
    <p style="color: red">用户名已存在</p>
 {% endif %}
```
第二=种方法：重新构造函数,在froms.py文件中重新构造init函数
```python
class 自定义表单(UserCreationForm):
    昵称=forms.CharField(required=False,max_length=50)
    生日=forms.DateField(required=False)

    class Meta:
        model=User
        fields=('username','password1','password2','email','昵称','生日')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages={'unique':'用户名已存在！！！','invalid':'用户名不合法'}
```
其中如 'unique','iunvalid'等是username表单的错误类型，可以查文档得到，也可以用.as_json打印查看
```Django
{{表单.errors.username.as_json}}
```

### 4.修改用户信息
修改用户信息涉及到两个库
```python
# 修改密码
from django.contrib.auth.forms import PasswordChangeForm
# 修改用户信息
from django.contrib.auth.forms import UserChangeForm
```
与UserCreationForm类似，不过PasswordChangeForm与UserChangeForm要求传入的参数名不同
```python

PasswordChangeForm(data=request.POST,user=request.user)
UserChangeForm(request.POST,instance=request.user)
```
### 5. 验证码
使用第三方包django-simple-captcha
[官方文档](https://django-simple-captcha.readthedocs.io/en/latest/usage.html#adding-to-a-form)
首先下载
```python
······Scripts>pip install django-simple-captcha
```
然后需要在setting.py中注册APP
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myauth',
    'captcha',
]
```
然后需要重新建表
```
python manage.py migrate
```
在总URL.py中加入
```python
path('captcha/',include('captcha.urla')),
```
