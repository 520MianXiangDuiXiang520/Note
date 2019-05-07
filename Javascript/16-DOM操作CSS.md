# DOM操作CSS

```js
元素.style.样式名 = 样式值
```

* 如果样式名中含有`-`要使用驼峰命名法，把`-`删除，后面字母大写
* 通过DOM修改是添加内联样式，内联样式有较高优先级，会覆盖外部样式，但如果使用`!important`会是最高优先级，js会失效

## 读取样式

* 元素.style.样式名
  * 只能读取内联样式
* 元素.currentStyle.样式名
  * 读取正在显示的样式
  * 只有IE支持....
* getCopputedStyle(要获取样式的元素，伪元素（一般为Null）)
  * 返回一个对象，可以使用对象名.样式名 的方法获取
  * IE8及以下浏览器不支持
* 方法四：

```js
function GetStyle(obj,name){
    if(window.getCopputedStyle(obj,Null)){
        return getCopputedStyle(obj,Null)[name];
    }else{
        return obj.currentStyle.name;
    }
}
```

## 其他方法

[W3School](http://www.w3school.com.cn/jsref/dom_obj_style.asp)