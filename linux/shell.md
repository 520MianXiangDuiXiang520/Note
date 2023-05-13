# Shell

## 执行 shell

```sh
# 路径上的目录有 rx 权限，文件有 rx 权限
./scripts.sh
/home/root/scripts.sh
```

```sh
# 只需要路径上的目录有 rx 权限，文件有 r 权限
bash ./scripts.sh
```

这两者都是在子进程中执行的，无法共享父进程的变量

```sh
. scripts.sh
source scripts.sh
```

当前 shell 进程中执行

### 调试

```sh
# 输出打印该内容的命令
bash -x scripts.sh

# 输出打印该内容的命令 + 注释
bash -vx scripts.sh

# 只检查语法问题
bash -n scripts.sh
```

```sh
set -xv
# jjj
echo "111"
set +xv
```

set -x 和 set +x 可以控制只输出某些命令的调试信息

## 技巧

命令展开：

```sh
echo file{1..10}
echo file{1..10..2}
```

## 变量

```sh
# 获取所有传进来的变量
$*
$@
```

获取所有传进来的变量,注意加上引号后他们的区别：

```sh
for var in $*
do
    echo $var
done

echo "---------"

for var in "$*"
do
    echo $var
done

echo "---------"

for var in $@
do
    echo $var
done

echo "---------"

for var in "$@"
do
    echo $var
done
```

```txt
{0:22}/Users/junebao/Project/Note/linux:master ✗ ➭ bash code/var.sh v1 v2 "v3 p"
v1
v2
v3
p
---------
v1 v2 v3 p
---------
v1
v2
v3
p
---------
v1
v2
v3 p
```

对于传入 `"name zhangsan"` 样式的参数， 使用 `"$@"` 是更合适的选择

`$#` 用于获取传入变量的个数

`$?` 用于获取上一个语句的执行情况 0 表示成功

`$$` 获取当前进程 pid

`${11}` 索引大于 9 的要加 `{}`

`readonly` 标识只读的常量

### 运算

`$` 或 `${}` 在算数运算表达式中时不必要的, 参考 [SC2004](https://www.shellcheck.net/wiki/SC2004)

```sh
echo $(($n + ${arr[i]}))
# 等价于
echo $((n + arr[i]))
```

## 文本处理

### 正则表达式

### grep

### sed

### awk