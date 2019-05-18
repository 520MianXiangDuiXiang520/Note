# ES5

## 严格模式

1. 定义方法 `use strict`
2. 特性：
    1. 必须使用var定义变量
    2. 存在eval作用域
    3. 禁止自定义函数中的this指向window
    4. 对象不能有重名属性

## JSON对象

* json.stringify(obj/arr):js对象转换为json对象
* json.parse(str):json对象转换为js对象

## Object拓展

Object.create(prototype,[descriptors])

* 作用：以指定对象为原型创建新对象
* descriptors参数
    * value：指定值
    * writeable：是否可修改
    * configurable：是否可删除
    * enumerable：是否能用for in 遍历

```js
var test1 = {
    name : "test1",
}

var test2 = {}

test2 = Object.create(test1,{
    sex:{
        value : "boy",
        writable : true,
        configurable : true,
        enumerable : true,
    },
    age : {
        value : 18,
    }

})
```

## Arrey拓展

* indexOf():取得值在数组中的第一个下标
* lastIndexOf():取得值在数组中的最后一个下标
* forEach()：遍历数组
* map():返回加工后的数组
* filter():过滤数组

```js
var arr = [1,2,3,,2,3,4,5,3,4,5,67,7,8,0]
var index_of = arr.indexOf(3)
console.log(index_of) // 2
var lastindex_of = arr.lastIndexOf(3)
console.log(lastindex_of)
// 无法使用break跳出遍历
arr.forEach(function(v){
    console.log(v)
})
var arr2 = arr.map(function(v){
   return  v + 1
})

console.log(arr2)

var arr3 = arr.filter(function(v){
    return v>2
})
console.log(arr3)
```

## Call,apply,bind

* call()：直接传递参数
* apply()：以数组形式传递参数
* bind()：直接传递参数，不会立即调用，返回函数

```js
var fun = function(a,b){
    console.log(this)
    console.log(a+b)
}

var fun1 = function(){
    var fun1_name = "fun1"
}

fun.call(fun1,"aa","bb")
fun.apply(fun1,["aa","bb"])
// 不会立即调用
var fun3 = fun.bind(fun1,"aa","bb")
fun3()
```