var info = document.getElementById('number')
var button = document.getElementById('post')

button.onclick = function(){
    var number = info.value
    console.log("send info")
     // 创建worker对象
    var worker = new Worker("07.thr.js")
    // 发送消息
    worker.postMessage(number)

    // 接受消息
    worker.onmessage = function(event){
        alert(event.data)
    }

}