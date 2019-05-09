# 事件对象

事件句柄

|属性 |此事件发生在何时... |
|---|---|
|onabort |图像的加载被中断。 |
|onblur |元素失去焦点。 |
|onchange |域的内容被改变。 |
|onclick |当用户点击某个对象时调用的事件句柄。 |
|ondblclick |当用户双击某个对象时调用的事件句柄。 |
|onerror |在加载文档或图像时发生错误。 |
|onfocus |元素获得焦点。 |
|onkeydown |某个键盘按键被按下。 |
|onkeypress |某个键盘按键被按下并松开。 |
|onkeyup |某个键盘按键被松开。 |
|onload |一张页面或一幅图像完成加载。 |
|onmousedown |鼠标按钮被按下。 |
|onmousemove |鼠标被移动。 |
|onmouseout |鼠标从某元素移开。 |
|onmouseover |鼠标移到某元素之上。 |
|onmouseup |鼠标按键被松开。 |
|onreset |重置按钮被点击。 |
|onresize |窗口或框架被重新调整大小。 |
|onselect |文本被选中。 |
|onsubmit |确认按钮被点击。 |
|onunload |用户退出页面。 |

鼠标 / 键盘属性

|属性 |描述 |
|---|---|
|altKey |返回当事件被触发时，"ALT" 是否被按下。 |
|button |返回当事件被触发时，哪个鼠标按钮被点击。 |
|clientX |返回当事件被触发时，鼠标指针的水平坐标。 |
|clientY |返回当事件被触发时，鼠标指针的垂直坐标。 |
|ctrlKey |返回当事件被触发时，"CTRL" 键是否被按下。 |
|metaKey |返回当事件被触发时，"meta" 键是否被按下。 |
|relatedTarget |返回与事件的目标节点相关的节点。 |
|screenX |返回当某个事件被触发时，鼠标指针的水平坐标。 |
|screenY |返回当某个事件被触发时，鼠标指针的垂直坐标。 |
|shiftKey |返回当事件被触发时，"SHIFT" 键是否被按下。 |

IE 属性：

|属性 |描述 |
|---|---|
|cancelBubble |如果事件句柄想阻止事件传播到包容对象，必须把该属性设为 true。 |
|fromElement |对于 mouseover 和 mouseout 事件，fromElement 引用移出鼠标的元素。 |
|keyCode |对于 keypress 事件，该属性声明了被敲击的键生成的 Unicode 字符码。对于 keydown 和 keyup 事件，它指定了被敲击的键的虚拟键盘码。虚拟键盘码可能和使用的键盘的布局相关。 |
|offsetX,offsetY |发生事件的地点在事件源元素的坐标系统中的 x 坐标和 y 坐标。 |
|returnValue |如果设置了该属性，它的值比事件句柄的返回值优先级高。把这个属性设置为 fasle，可以取消发生事件的源元素的默认动作。 |
|srcElement |对于生成事件的 Window 对象、Document 对象或 Element 对象的引用。 |
|toElement |对于 mouseover 和 mouseout 事件，该属性引用移入鼠标的元素。 |
|x,y |事件发生的位置的 x 坐标和 y 坐标，它们相对于用CSS动态定位的最内层包容元素。 |

标准 Event 属性：

|属性 |描述 |
|---|---|
|bubbles |返回布尔值，指示事件是否是起泡事件类型。 |
|cancelable |返回布尔值，指示事件是否可拥可取消的默认动作。 |
|currentTarget |返回其事件监听器触发该事件的元素。 |
|eventPhase |返回事件传播的当前阶段。 |
|target |返回触发此事件的元素（事件的目标节点）。 |
|timeStamp |返回事件生成的日期和时间。 |
|type |返回当前 Event 对象表示的事件的名称。 |

标准 Event 方法：

|方法 |描述 |
|---|---|
|initEvent() |初始化新创建的 Event 对象的属性。 |
|preventDefault() |通知浏览器不要执行与事件关联的默认动作。 |
|stopPropagation() |不再派发事件。 |

## 事件的冒泡，委派，绑定，传播

* 事件的冒泡：Bubble，事件的向上传导，当后代的事件被触发时，其祖先的相同事件也会被触发
* 事件的委派：利用事件的冒泡，减少事件绑定的次数
  * target:获取触发事件的对象
* 事件的绑定：
  * addeventListener
    * 参数：
      * 事件的字符串，去掉on
      * 回调函数，先绑定的先执行
      * 是否在捕获阶段触发事件，一般为false
    * 不支持IE8及以下
    * this指向绑定事件的对象
  * attachEvent
    * 参数：
      * 事件的字符串，有on
      * 回调函数，先绑定的后执行
    * this指向window
* 事件的传播
  * 微软：由内向外
  * 网景：由外向内
  * W3C：分三阶段
    * 捕获阶段：从document/window向内捕获，不执行响应函数
    * 目标阶段：执行响应函数
    * 冒泡阶段：从目标向祖先传递