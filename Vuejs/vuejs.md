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
5. 过滤器：`|`:将函数的执行结果赋值给第一个参数（`{{messade|function}}`）,
   * 可串联 `{{messade|function|fun2}}`
   * 可传参

## 条件循环语句

