/**
 * 每一个函数都有一个属性：prototype,默认指向object空对象，就是原型对象,原型对象有一个constructor属性，指向函数对象
 * 每一个实例化对象都有一个属性 __proto__ ,默认指向构造函数的原型对象（是构造函数原型对象的一个引用）
 * 每个函数都是Function的实例化对象，也就是每个函数都有一个__proto__属性，他的值与Function的显性原型相同
 */

 var Fun = function(){
    // console.log("构造函数")
 }

console.log(Fun.prototype.constructor === Fun)

var fu = new Fun()

console.log(fu.__proto__ === Fun.prototype)

Fun.prototype.newfun = function(){
    console.log("新方法")
}

fu.newfun()

console.log(Function.prototype)
console.log(Fun instanceof Function) //true
console.log(Object instanceof Function) //true
console.log(Function instanceof Object) // true
console.log(Function instanceof Function) //true

console.log(Object.prototype === Fun.prototype.__proto__) // true
console.log(Object.prototype.__proto__) // null

console.log(Function.prototype === Object.__proto__) // true
console.log(Function.__proto__ === Function.prototype) // true
console.log(Function.prototype.__proto__ === Object.prototype) // true

console.log("--------------------------------------------------------")

function F(){}
Object.prototype.a = function(){
    console.log("a()")
}
Function.prototype.b = function(){
    console.log("b()")
}

var f = new F()

f.a()
// f.b() // error 
F.a()
F.b()

console.log(f)
console.log(Object.prototype)