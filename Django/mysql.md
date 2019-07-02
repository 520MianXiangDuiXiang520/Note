# Django 连接mysql

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxxxxx',
        'USER':'xxxx',
        'PASSWORD':'*****',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}
```

init.py

```python
import pymysql
pymysql.install_as_MySQLdb()
```