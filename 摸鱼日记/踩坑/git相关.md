## 1. 强制 pull 并覆盖本地文件

从远程下载最新的，而不尝试合并或rebase任何东西

```git
git fetch --all
```

将主分支重置为您刚刚获取的内容。 --hard选项更改工作树中的所有文件以匹配origin/master中的文件。

```
git reset --hard origin/<branch_name>
```

## 2. 彻底清除Github上某个文件的历史（针对误上传密码文件等情况）

```git
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch FILE_PATH' --prune-empty --tag-name-filter cat -- --all
git push origin master --force
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now
git gc --aggressive --prune=now
```

