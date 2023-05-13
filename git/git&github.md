# git & github

## 配置 git 账号

与 github 等远程仓库交互前，你需要配置 git 的用户名和邮箱，一般保持与远程仓库一致：

```git
git config --global user.email "123@google.com"
git config --global user.username "startoo"
```

## 配置 SSH 密钥

推送代码到远程仓库时，远程仓库需要对你进行认证，当然可以每次都输账号和密码，但更好的办法是使用 SSL 认证，它更加安全和方便：

### Windows

打开 git bash 输入：

```git
ssh-keygen -t rsa -C "123@google.com"
```

一路回车，会在 `C:\User\你的用户名\.ssh` 文件夹下生成 `id_rsa` 和 `id_rsa.pub` 文件，用记事本或随便什么软件打开 `id_rsa.pub` 文件，复制其中的全部内容。

打开 github 点击头像  → Settings → SSH and GPG keys → New SSH key

Title 随便输，建议是电脑的名字，将复制的内容粘贴到 Key 中，点 “Add SSH Key” 

回来在 git bash 上输入 `ssh -T git@github.com` 看到 success 就成功了。

## 远程仓库

如果 github 上已经有仓库了，可以直接执行 ``
