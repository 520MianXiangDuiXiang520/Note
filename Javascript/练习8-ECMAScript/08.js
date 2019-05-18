'use strict'
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

console.log(test2)
console.log(test2.name)
test2.sex = "girl"
console.log(test2.sex)

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

console.log("------------------------------------")

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