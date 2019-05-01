# git

以列表形式列出git配置

```shell
git config --list
```

克隆仓库

```shell
git clone [url] [本地仓库名]
```

在现有目录中初始化仓库

```shell
git init
```

查看当前文件状态

```shell
git status
```

追踪新文件

```shell
git add [文件名]
```

查看修改

```shell
git diff
```

提交更新

```shell
git commit -m "更新信息"

# 跳过暂存提交更新
git commit -m "更新信息" -a
```

移除文件

```shell
# rm命令会把文件从本地和暂存区都删除，如果只在本地删除了文件，已暂存的文件会出现在Changes not staged for commit:中
git rm

# 删除修改过，并且已经放在暂存区的文件，必须加强制删除 -f
git rm [文件名] -f

# 只从暂存区删除，但仍保留在本地
git rm [文件名] --cached
```

移动文件(重命名暂存区文件)

```shell
git mv [file_from][file_to]
```

查看提交历史

```shell
git log

# 参数 -p 显示每次提交的内容差异 -2 指定近几次

git log -p -2

# --stst 每次修改的简略统计
git log --stat

# --pretty 指定用不同格式展示提交历史
git log --pretty=format:"%h - %an , %ar : %s"
```

撤销操作

```shell
# 尝试重新提交
git commit --amend

# 取消暂存的文件
git reset HEAD [文件名]

# 撤销对文件的修改
git checkout -- [filename]
```

查看远程仓库

```shell
# -v 显示url
git remote -v

# 更详细的
git remote show origin
```

添加远程仓库

```shell
# shortname可以看作url的简写，以后可以使用shortname代替url
git remote add <shortname> <url>
```

从远程仓库抓取或拉取数据

```shell
git fetch [remote-name]
```

推送到远程仓库

```shell
git push

# 将master分支推送到origin服务器
git push origin master
```

同步远程仓库

```shell
git pull
```

远程仓库的移除和重命名

```shell
git remote rm [name]
```

git隐藏,用于不得不切换分支，但又不能提交当前代码的情况

```shell
# 将一个新的存根推到堆栈上
git stash

# 查看已存在的更改列表
git stash list

# 从堆栈中删除更改并将其放置在当前工作目录
git stash pop
```

git标签

```shell
# 创建标签
git tag -a [标签名] -m [标签消息]

# 查看所有可用标签
git tag -l

# 查看详情
git show [标签名]

# 删除标签
git tag -d [标签名]
```

git分支管理

```shell
# 创建分支
git branch <branch name>

# 列出可用分支
git branch

# 切换分支
git checkout <branch name>

# 删除分支
git branch -D <branch name>

# 重命名分支
git branch -m <old branch name> <new branch name>

# 合并分支(选择一个分支合并到当前分支)
git merge [branch]
```