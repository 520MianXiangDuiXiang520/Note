# BOM

JS有三类对象，自定义对象，内建对象，宿主对象

* 内建对象：
  * Array
  * Boolean
  * Date
  * Math
  * Number
  * String
  * RegExp
  * Functions
  * Events
* 宿主对象
  * DOM
    * Document
    * Element
    * Attribute
    * Event
  * BOM
    * Window
    * Navigator
    * Location
    * History
    * Screen

BOM，浏览器对象模型，用来通过JS操作浏览器

## Navigator

用来查看浏览器信息，

属性

|属性 |描述 |
|---|---|
|appCodeName |返回浏览器的代码名。 |
|appMinorVersion |返回浏览器的次级版本。 |
|appName |返回浏览器的名称。 |
|appVersion |返回浏览器的平台和版本信息。 |
|browserLanguage |返回当前浏览器的语言。 |
|cookieEnabled |返回指明浏览器中是否启用 cookie 的布尔值。 |
|cpuClass |返回浏览器系统的 CPU 等级。 |
|onLine |返回指明系统是否处于脱机模式的布尔值。 |
|platform |返回运行浏览器的操作系统平台。 |
|systemLanguage |返回 OS 使用的默认语言。 |
|userAgent |返回由客户机发送服务器的 user-agent 头部的值。 |
|userLanguage |返回 OS 的自然语言设置。 |

方法

|方法 |描述 |
|---|---|
|javaEnabled() |规定浏览器是否启用 Java。 |
|taintEnabled() |规定浏览器是否启用数据污点 (data tainting)。 |

着重批评**IE11**，为了不让人知道他是 IE 先是把自己的 appName 改成活活被他逼死的航海家，又删除掉自己UA头里所有有关IE的字段，还让自己特有的ActiveObject无论发生什么都返回false，这样用`if(activeObject())`判断时大家一样返回false了。。。更可恶的是你这UA头，like Gecko 什么鬼？？？？像？？奥，像！！！

```js
   User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134
```

不过可以使用 in 判断是不是IE

```js
if(activeObject in window){
    alert("IE!!");
}
```