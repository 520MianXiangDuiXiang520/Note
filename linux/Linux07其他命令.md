# 查找文件
* find用来在指定目录下搜索符合条件的文件

```
find [路径] -name "正则表达式"
```
```
junbao111@ubuntu:~/Desktop$ find ~ -name "*.py"
/home/junbao111/Note/Linux/test/02.py
/home/junbao111/Desktop/Python/01.py
junbao111@ubuntu:~/Desktop$ 

```

# 文件软链接(快捷方式)

```
ln -s 被链接的源文件的完整路径(绝对路径) 链接文件名
```
* 如果没有 `-s`建立的是硬链接
  * 硬链接：与源文件占用相同大小的硬盘空间
* 在写源文件路径时应该使用绝对路径，否则软连接移动位置后就无法使用

```


junbao111@ubuntu:~/Desktop$ tree
.
└── Python
    ├── 01.py
    └── test
        └── demo

3 directories, 1 file
junbao111@ubuntu:~/Desktop$ touch Python/test/demo/test.py
junbao111@ubuntu:~/Desktop$ tree
.
└── Python
    ├── 01.py
    └── test
        └── demo
            └── test.py

3 directories, 2 files
junbao111@ubuntu:~/Desktop$ ln -s Python/test/demo/test.py xiangdui
junbao111@ubuntu:~/Desktop$ ln -s /home/junbao111/Desktop/Python/test/demo/test.py juedui
junbao111@ubuntu:~/Desktop$ cat xiangdui 
junbao111@ubuntu:~/Desktop$ cat xiangdui 
# this is a test file
junbao111@ubuntu:~/Desktop$ cat juedui 
# this is a test file
junbao111@ubuntu:~/Desktop$ ls -l
总用量 4
lrwxrwxrwx 1 junbao111 junbao111   48 3月  12 15:29 juedui -> /home/junbao111/Desktop/Python/test/demo/test.py
drwxr-xr-x 3 junbao111 python    4096 3月  12 15:27 Python
lrwxrwxrwx 1 junbao111 junbao111   24 3月  12 15:28 xiangdui -> Python/test/demo/test.py
junbao111@ubuntu:~/Desktop$ mv xiangdui Python/
junbao111@ubuntu:~/Desktop$ mv juedui Python/
junbao111@ubuntu:~/Desktop$ cd Python/
junbao111@ubuntu:~/Desktop/Python$ cat xiangdui 
cat: xiangdui: 没有那个文件或目录
junbao111@ubuntu:~/Desktop/Python$ cat juedui 
# this is a test file
junbao111@ubuntu:~/Desktop/Python$ 

```
# 打包压缩
* window：rar
* Mac：zip
* Linux：tar.gz

## 打包解包

```

# 打包
tar -cvf 打包文件名.tar 被打包文件...
# 多个文件用空格分割

# 解包
tar -xvf 压缩文件.tar


```
**tar选项**
* c：生成档案文件，创建打包文件
* x：解开档案文件
* v：列出归档解档的详细过程，显示进度
* f：指定档案文件名称，f后面必须是.tar文件，所以该选项必须放在最后

**tar只负责打包解包，不负责压缩**

## 压缩解压
**gzip**
在打包解包中增加`-z`选项，会调用gzip对文件压缩或解压缩，最终生成后缀为`.tar.gz`的压缩文件，在解压最后怎加 `-C`选项可以把文件解压缩到指定目录，指定目录必须存在。
**bzip2**
把原有`-z`改成`-j`注意文件拓展名是`.tar.bz2`

# 安装，卸载软件

```
# 安装
sudo apt install 软件名

# 卸载
sudo apt remove 软件名

# 打印可更新列表
sudo apt update

# 更新
sudo apt upgrade 
```