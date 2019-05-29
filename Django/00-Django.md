# Django


## 安装Django

```shell
sudo pip install Django
# 在这之后创建Django项目会报错，根据错误提示安装需要的东西就行

# 第一个报错
Command 'django-admin' not found, but can be installed with:

sudo apt install python-django-common
# 之后依旧不能创建项目，报下面的错误，网上教程说下载python（不是python3），亲测无用，提示找不到python-django or python3-django.就下载python3-django呗，果然好用。。。
Cannot find installed version of python-django or python3-django.

sudo apt install python3-django
```

查看Django版本号

```cmd
python -m django --version
```

创建Django项目

```cmd
django-admin startproject mysite
```

Django目录结构

```shell
.                      # 项目容器，可以重命名为任何你喜欢的名字
├── manage.py          # 管理Django项目的命令行工具
└── mysite             # 项目包
    ├── __init__.py    # 说明是一个python的包
    ├── settings.py    # Django配置文件
    ├── urls.py        # url申明
    └── wsgi.py        # 项目的运行在 WSGI 兼容的Web服务器上的入口

```

启动服务器：django内置了一个轻量级服务器运行

```shell
python manage.py runserver [指定端口号]
```
>用于开发的服务器在需要的情况下会对每一次的访问请求重新载入一遍 Python 代码。所以你不需要为了让修改的代码生效而频繁的重新启动服务器。然而，一些动作，比如添加新文件，将不会触发自动重新加载，这时你得自己手动重启服务器。

创建应用：

```shell
python manage.py startapp polls

# 目录结构
└── polls
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py

```