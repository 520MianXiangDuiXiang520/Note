# django开发流程

新建项目

```shell
django-admin startproject projectname
```

注册app

```shell
python manage.py startapp appname
```

修改配置

* 在INSTALLED_APPS中注册app
* 修改TEMPLATES中DIRS字段   
```python
'DIRS': [os.path.join(BASE_DIR,'templates').replace('\\','/')],
```
* 修改语言和时区
```python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```
* 配置静态文件地址
```python
STATIC_URL = '/static/'
MEDIA_URL= '/upload/'
```
* 配置主路由
```python
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from JBlog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='首页'),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)\
    +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```
