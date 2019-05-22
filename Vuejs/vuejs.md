# Vue.js

## 起步

1. 引入vuejs,建议直接把[vue.min.js](https://vuejs.org/js/vue.min.js)下载到本地
2. 实例化一个vue对象，每个vue对象至少包含`el`,`data`两部分，还起码要有`methods`
   * el:指定vue.js作用的区域
   * data：数据
   * methods：定义函数的地方
3. 在html中调用数据`{{}}`
4. 模板语法：
   * v-html:输出html文本
   * v-bind:更新html属性，缩写为 `:`
   * v-if:判断
   * v-on：监听DOM事件,缩写为 `@`
   * v-model：绑定数据
   * v-watch:监视
5. 过滤器：`|`:将函数的执行结果赋值给第一个参数（`{{messade|function}}`）,
   * 可串联 `{{messade|function|fun2}}`
   * 可传参
6. 计算属性：computed
7. 事件处理
   * 停止冒泡：`@click.stop`
   * 阻止事件默认行为：`@click.prevent`
   * 按键修饰符：`@keyup.13(keycode)/enter(keyname)`
