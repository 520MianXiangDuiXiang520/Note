/**
 * 1. 先执行变量提前，再执行函数提前，a被覆盖
 */

 function a(){}
 var a
 console.log(typeof a)  // function

/**
 * 2. 用var定义的变量会被提前并赋值为underfind，并添加为window的属性
 *   * 不要把if代码块中的语句与函数混淆，
 */

 if(!(b in window)){
     var b = 5
 }
 console.log(b)  // underfind

 /**
  * 1. 第一行c使用var定义，会先被赋值为underfind
  * 2. 程序向下运行到第一行，把c从underfind赋值为1
  * 3. 下面是一个函数，函数只有在被调用时才会被提前，2-5行暂时会跳过
  * 4. 第六行c以函数运行，会报错
  */

  var c = 1
  function c(c){
    c = 2
    console.log(c)
  }
c(5)  // 05.js:31 Uncaught TypeError: c is not a function at 05.js: 31

/**
 * 作用域与作用域链
 */

 var fu = function(){
     console.log(fu)
 }

 fu()

 var obj = {
     fu2 : function(){
         console.log(fu2)
     }
 }
obj.fu2()  //05.js:44 Uncaught ReferenceError: fu2 is not defined

/**
 * 函数作用域在函数创建时就确定了，并且不会改变，
 * 在show中调用fn，fn与show的作用域也是相互隔绝的
 */

var x = 10
function fn(x){
    console.log(x) 
}
function show(f){
    var x = 20
    f()
}
show(fn) // 10