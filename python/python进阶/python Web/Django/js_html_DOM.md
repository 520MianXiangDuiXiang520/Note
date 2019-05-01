# DOM

> 是HTML和XML文档的编程接口。它提供了对文档的结构化的表述，并定义了一种方式可以使从程序中对该结构进行访问，从而改变文档的结构，样式和内容。DOM 将文档解析为一个由节点和对象（包含属性和方法的对象）组成的结构集合。简言之，它会将web页面和脚本或程序语言连接起来。

>一个web页面是一个文档。这个文档可以在浏览器窗口或作为HTML源码显示出来。但上述两个情况中都是同一份文档。文档对象模型（DOM）提供了对同一份文档的另一种表现，存储和操作的方式。 DOM是web页面的完全的面向对象表述，它能够使用如 JavaScript等脚本语言进行修改。

## DOM基本功能：
① 查询某个元素
② 查询某个元素的祖先、兄弟以及后代元素
③ 获取、修改元素的属性
④ 获取、修改元素的内容
⑤ 创建、插入和删除元素

### 查询

* 通过id查找  `var x=document.getElementById("intro");`
* 通过标签 `var x=document.getElementById("main");`
* 通过类名 `var x=document.getElementByClassName("main");`

### 修改

* 改变HTML输出流 `document.write() `
* 改变HTML内容 `document.getElementById(id).innerHTML=新的 HTML`
* 改变HTML属性

```html
<img id="image" src="smiley.gif" width="160" height="120">
<script>
document.getElementById("image").src="landscape.jpg";
</script>
```

* 改变CSS
`document.getElementById(id).style.property=新样式`
或使用事件
```html
<button type="button"
onclick="document.getElementById('id1').style.color='red'">
点我!</button>
```

## 事件
