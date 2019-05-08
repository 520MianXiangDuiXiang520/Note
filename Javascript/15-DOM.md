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

完整版

| 属性 / 方法                                                   | 描述                                           |
|-----------------------------------------------------------|----------------------------------------------|
| element.accessKey                                         | 设置或返回元素的快捷键。                                 |
| element.appendChild()                                     | 向元素添加新的子节点，作为最后一个子节点。                        |
| element.attributes                                        | 返回元素属性的 NamedNodeMap。                        |
| element.childNodes                                        | 返回元素子节点的 NodeList。                           |
| element.className                                         | 设置或返回元素的 class 属性。                           |
| element.clientHeight                                      | 返回元素的可见高度。                                   |
| element.clientWidth                                       | 返回元素的可见宽度。                                   |
| element.cloneNode()                                       | 克隆元素。                                        |
|                         element.compareDocumentPosition() | 比较两个元素的文档位置。                                 |
|                         element.contentEditable           | 设置或返回元素的文本方向。                                |
| element.dir                                               | 设置或返回元素的内容是否可编辑。                             |
| element.firstChild                                        | 返回元素的首个子。                                    |
|                         element.getAttribute()            | 返回元素节点的指定属性值。                                |
|                         element.getAttributeNode()        | 返回指定的属性节点。                                   |
|                         element.getElementsByTagName()    | 返回拥有指定标签名的所有子元素的集合。                          |
| element.getFeature()                                      | 返回实现了指定特性的 API 的某个对象。                        |
| element.getUserData()                                     | 返回关联元素上键的对象。                                 |
|                         element.hasAttribute()            | 如果元素拥有指定属性，则返回true，否则返回 false。               |
|                         element.hasAttributes()           | 如果元素拥有属性，则返回 true，否则返回 false。                |
|                         element.hasChildNodes()           | 如果元素拥有子节点，则返回 true，否则 false。                 |
| element.id                                                | 设置或返回元素的 id。                                 |
| element.innerHTML                                         | 设置或返回元素的内容。                                  |
| element.insertBefore()                                    | 在指定的已有的子节点之前插入新节点。                           |
| element.isContentEditable                                 | 设置或返回元素的内容。                                  |
| element.isDefaultNamespace()                              | 如果指定的 namespaceURI 是默认的，则返回 true，否则返回 false。 |
| element.isEqualNode()                                     | 检查两个元素是否相等。                                  |
| element.isSameNode()                                      | 检查两个元素是否是相同的节点。                              |
| element.isSupported()                                     | 如果元素支持指定特性，则返回 true。                         |
| element.lang                                              | 设置或返回元素的语言代码。                                |
| element.lastChild                                         | 返回元素的最后一个子元素。                                |
| element.namespaceURI                                      | 返回元素的 namespace URI。                         |
| element.nextSibling                                       | 返回位于相同节点树层级的下一个节点。                           |
| element.nodeName                                          | 返回元素的名称。                                     |
| element.nodeType                                          | 返回元素的节点类型。                                   |
| element.nodeValue                                         | 设置或返回元素值。                                    |
| element.normalize()                                       | 合并元素中相邻的文本节点，并移除空的文本节点。                      |
| element.offsetHeight                                      | 返回元素的高度。                                     |
| element.offsetWidth                                       | 返回元素的宽度。                                     |
| element.offsetLeft                                        | 返回元素的水平偏移位置。                                 |
| element.offsetParent                                      | 返回元素的偏移容器。                                   |
| element.offsetTop                                         | 返回元素的垂直偏移位置。                                 |
| element.ownerDocument                                     | 返回元素的根元素（文档对象）。                              |
| element.parentNode                                        | 返回元素的父节点。                                    |
|                         element.previousSibling           | 返回位于相同节点树层级的前一个元素。                           |
|                         element.removeAttribute()         | 从元素中移除指定属性。                                  |
|                         element.removeAttributeNode()     | 移除指定的属性节点，并返回被移除的节点。                         |
| element.removeChild()                                     | 从元素中移除子节点。                                   |
| element.replaceChild()                                    | 替换元素中的子节点。                                   |
| element.scrollHeight                                      | 返回元素的整体高度。                                   |
| element.scrollLeft                                        | 返回元素左边缘与视图之间的距离。                             |
| element.scrollTop                                         | 返回元素上边缘与视图之间的距离。                             |
| element.scrollWidth                                       | 返回元素的整体宽度。                                   |
|                         element.setAttribute()            | 把指定属性设置或更改为指定值。                              |
|                         element.setAttributeNode()        | 设置或更改指定属性节点。                                 |
| element.setIdAttribute()                                  |                                              |
| element.setIdAttributeNode()                              |                                              |
| element.setUserData()                                     | 把对象关联到元素上的键。                                 |
| element.style                                             | 设置或返回元素的 style 属性。                           |
| element.tabIndex                                          | 设置或返回元素的 tab 键控制次序。                          |
| element.tagName                                           | 返回元素的标签名。                                    |
| element.textContent                                       | 设置或返回节点及其后代的文本内容。                            |
| element.title                                             | 设置或返回元素的 title 属性。                           |
| element.toString()                                        | 把元素转换为字符串。                                   |
| nodelist.item()                                           | 返回 NodeList 中位于指定下标的节点。                      |
| nodelist.length                                           | 返回 NodeList 中的节点数。                           |
