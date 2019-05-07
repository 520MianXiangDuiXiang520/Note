# DOM 操作 HTML

DOM Document Object Model，文档对象模型，用js操作文档对象

![dt](image/domtree.gif)

* 节点：构成网页最基本的部分，网页的每一部分都是一个节点
  * 文档节点：
  * 元素节点：
  * 属性节点：
  * 文本节点：
* 事件：用户与浏览器的交互行为
  * 操作事件的两种办法：
  * 在属性中添加js代码，高耦合，不推荐
  * 绑定事件响应函数
* 文档的加载: 自顶向下，读一行，加载一行，所以dom应该写在body最后面，或者用onload声明整个页面加载完后再执行

```js
<script>
    window.onload = function(){
        // jsCode
    }
</script>
```

## 获取元素节点

* getElementById()
* getElementsByName()：返回类数组对象
* getElementsByTagName()：返回类数组对象
* innerHTML；文本节点
* innerText：文本节点，没标签

----

通过具体元素调用：

* childNodes:所有子节点
* firstChild：第一个子节点
* lastChild：最后一个子节点
* children：所有子**元素**
* parentNode:获取当前节点的父节点
* previousSibling:前一个兄弟节点
* nextSibling:后一个兄弟节点

**注意:**标签间的空白也会被当成节点,可以使用一下几个获取子元素，但不兼容IE8及以下浏览器

* firstElementChild:
* lastElementChild:
* previousElementSibling:前一个兄弟元素
* nextElementSibling:后一个兄弟元素

### 操作元素节点

* createElement(): 创建元素节点对象，传入标签名的字符串
* createTextNode():创建文本节点对象，传入文本
* appendChild():向父节点添加一个子节点
* insertBefore():在父节点的指定子节点前插一个新节点

```js
fatherNode.insertBefore(childNode,newNode);
```

* replaceChild():用新节点替换子节点

```js
fatherNode.replaceChild(newNode,oldNode);
```

* removeChild()：删除当前节点的指定子节点