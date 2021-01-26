# Vue-Cli 项目首屏加载慢的问题

这几天发现自己的博客第一次打开特别慢，但后面的请求速度还可以，第一反应是 SSL 握手或者是 TCP 握手的原因，因为我用了 HTTP/2 后面的请求可以复用之前的 TCP 连接，但仔细以看并不是这样：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1610631906632-1610631906619.png)

发现大部分的耗时其实花在了请求 `chunk-vendors.xxx.js` 上，这是 Vue-Cli Build 之后生成的，大小高达 1.5M，怪不得加载慢，那解决办法就很简单了——减少这个文件的大小和采用 CDN 加速

## 压缩

减少文件大小一个最简单有效的办法就是压缩，我们可以先使用 `ompression-webpack-plugin` 插件压缩



