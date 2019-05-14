function fun(n,o){
    console.log(o)
    return {
        name : "jjj",
        obj : function(m){
            return fun(m,n)
        }
    }
}

var a = fun(0)  //underfind
var s = a.obj(1)  // 0
a.obj(2)  // 0
a.obj(3)  // 0

var b = fun(0).obj(1).obj(2).obj(3)  // underfind 0 1 2

var c = fun(0).obj(1)  // underfind 0
c.obj(2)  // 1
c.obj(3)  // 1