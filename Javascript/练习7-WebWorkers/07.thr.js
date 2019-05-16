var feibo = function(begin){
    return begin < 2? 1:feibo(begin - 1) + feibo(begin - 2)
}

var onmessage = function(event){
    console.log("接收到数据："+event)
    var res = feibo(event.data)
    postMessage(res)
}