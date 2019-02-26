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
models.py中加入自定义的内容如：

```python
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class 普通会员表(models.Model):
    用户=models.OneToOneField(User,on_delete=models.CASCADE)
    昵称=models.CharField(blank=True,max_length=50)
    生日=models.DateField(blank=True)
    
    class Meta:
        verbose_name_plural="普通会员表"
```
新建froms.py文件
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
