### 1.环境搭建
#### 1.1 安装虚拟环境

```python
pip install virtualenv
```

#### 1.2 创建虚拟环境
* 新建一个文件夹，如 textvir
* win+R 输入CMD打开命令行
```txt
cd textvir
```
* 进入该文件夹运行
  `virtualenv .`
  该命令会把当前文件夹作为虚拟文件夹
#### 1.3 启用虚拟环境
```txt
cd Scripts
activate
```
成功启动会在命令行前面加一个括号，里面是虚拟环境名称
### 2. 其他命令
1. 安装包
```python
pip install 包名==版本号
```
2. 查看已安装的包
```python
pip freeze
```
3. 创建项目
```python
django-admin startproject 项目名
```
4. 创建APP
```python
# 先cd进入项目文件夹，运行
python manage.py startapp APP名
```
5. 启动服务器
```python
python manage.py runserver
```
6. 制作迁移文件
```python
python manage.py makemigrations
```
7. 建表
```python
python manage.py migrate
```
8. 清空数据库
```
python manage.py flush
```
9. 创建超级管理员
```
python manage.py createsuperuser
```