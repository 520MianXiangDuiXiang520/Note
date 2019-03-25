# vi和vim

vi 和 vim 是Linux中最经典的文本编辑软件，核心思想是让程序员双手不离开键盘中心，
特点：

* 没有界面
* 不用鼠标
* 没有菜单
* 不能排版
* 只有命令
* vim提供了程序员常用的代码补全等功能

## vi常用命令

### 打开或新建

```linux
vi 文件名
```

* 如果文件存在，就打开，否则就新建
* 新建必须保存，`:w`
* 定位到行：`vi 文件名 + 行数`
* 不加行数打开会直接定位到文件末尾

### 删除交换文件

如果vi异常退出，在磁盘上会保存交换文件，下次再使用时，会报E325的错误，可以使用`d`删除交换文件

### vi的工作模式

#### 命令模式

打开文件会直接进入命令模式，是程序入口，在其他模式下使用Esc键进入命令模式，在命令模式下使用`:`进入末行模式，使用`i`进入编辑模式

##### 命令模式常用命令

1. 重复

```vi
    数字 命令
```

2. 移动和选择

|方向|字母|备注|
|-|-|-|
|上|k| |
|下|j| |
|左|h| |
|右|l| |
|向后移动一个单词|w| |
|向前移动一个单词|b| |
|回到行首|0| |
|回到行首第一个不是空白字符的位置|^| |
|回到行尾|$| |
|回到文件顶部|gg| |
|回到文件尾部|G| |
|移动到对应行数|数字gg| |
||数字G| |
||:数字|末行模式|
|向上翻页|CTRL+b| |
|向下翻页|ctrl+f| |
|屏幕顶部|H| |
|屏幕中间|M| |
|屏幕底部|L| |
|向上寻找段落|{|
|向下寻找段落|}|
|在括号间切换|%|
|添加标记|m 标记（a-z|A-Z）|
|回到标记|`'标记`|
|可视模式|v|
|可视行|V|
|可视列|CTRL+v|

3. 编辑

|命令|功能|
|----|----|
|u|撤回|
|CTRL+r|恢复撤销|
|x|删除光标所在字符或选中的文本|
|d（移动命令）|删除移动命令所对应的文本|
|dd|删除光标所在行|
|D|删除至行尾|
4. 撤销，重复
5. 查找替换

#### 编辑模式

编辑

#### 末行模式

执行保存和退出，`w`保存`q`退出，可组合使用 `x`或`wq`，如果不想保存直接退出，使用 `q!`

### 退出

```vi
:q
```