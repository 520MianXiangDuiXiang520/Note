---
title: "Hexo + GitHub搭建个人博客"
data: 2020-1-11 18:26
tags: 
  - hexo
---
# HEXO + GitHub搭建个人博客

## 1. 安装Node.js

hexo 基于 node.js 所以需要下载，[下载地址](https://nodejs.org/en/download/) 下载结束后在命令行输入`node -v`

```cmd
C:\Users\lenovo>node -v
v12.13.0
```

说明安装成功

## 2. 检查npm是否安装

命令行输入`npm -v`

```cmd
E:\>npm -v
6.12.0
```

正确打印版本号就可以了

## 3. 下载hexo

新建一个文件夹，在这个文件夹里用命令行运行`npm install -g hexo-cli`

```cmd
E:\Blog>npm install -g hexo-cli
C:\Users\lenovo\AppData\Roaming\npm\hexo -> C:\Users\lenovo\AppData\Roaming\npm\node_modules\hexo-cli\bin\hexo
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@2.1.2 (node_modules\hexo-cli\node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.1.2: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

+ hexo-cli@3.1.0
added 26 packages from 13 contributors, removed 169 packages and updated 34 packages in 467.784s
```

看到有一个warning错误，但[这篇博客](https://blog.csdn.net/u013291076/article/details/84967778)告诉我windows环境可以忽略。

## 4. 初始化

依旧在刚才那个文件夹中用命令行输入`hexo init blog`

还是会有上面的错误，可以不用管，最后输出`INFO  Start blogging with Hexo!`就可以了。

## 5. 检查

```cmd
hexo new testSite
hexo g
hexo s
```

上面那条命令运行完之后，不出意外新建的文件夹中因该或有一个blog文件夹，进去这个文件夹，使用`hexo n title`创建一篇新文章，`hexo g`生成，`hexo s`启动服务预览，然后浏览器输入`localhost:4000`应该就能访问到一个站点，这就可以了，下一步就是推送到外网。

## 6. 创建GitHub仓库

创建一个名为`yourName.github.io`的仓库， `yourName`就是自己的GitHub名

## 7. 修改 _config.yml文件

为了把本地博客与GitHub仓库链家起来，修改`_config.yml`文件的`deploy`字段

```yml
deploy:
  type: git
  repo: https://github.com/520MianXiangDuiXiang520/520MianXiangDuiXiang520.github.io.git
  branch: master
```

## 8. 安装git部署插件

```cmd
npm install hexo-deployer-git --save
```

## 9. 部署网站

```cmd
hexo clean   # 清理缓存
hexo g   # 生成
hexo d   # 部署
```

这时候访问`https://yourname.github.io/`应该就可以看到和刚才一样的页面了，如果404的话，再执行一次`hexo d`试一试。

## 10. 绑定域名

1. 在自己的域名提供商后台添加两条记录

```txt
 1. 主机记录： @
     记录类型：A
     记录值：192.30.252.154 或者 192.30.252.153

 2. 主机记录： www
      记录类型： CNAME
      记录值： xxx.github.io  (这里就是你的github仓库名称)
```

2. 在自己GitHub博客仓库的setting 中的Custom domain写上自己的域名。

3. 在你的博客的 sources 目录下新建一个 CNAME 文件，里面写自己的域名就行。然后用`git d` push到github

4. 访问自己的域名，就可以看见之前的页面了。

## 11. 修改主题

从[这里](https://hexo.io/themes/)找个好看的主题，下载到博客根目录下的themes文件夹下，然后把**项目**配置文件`_config.yml`中的 `theme`改成刚下载的主题文件夹名，主题具体配置按照每个主题的README文件来



