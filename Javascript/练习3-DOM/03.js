// var box1 = document.getElementById("box1");
// var body = document.getElementsByTagName("body")[0];
// document.onmousemove = function(event){
//     event = event || window.event;
//     /**
//      * 获取鼠标位置有两种办法，clientX，clientY和pageX,pageY
//      *  - clientX,clientY获取的位置是相对于可见窗口的，如果有滚动条的话会出现偏差
//      *  - pageX,pageY是相对于页面的，不支持IE8及以下浏览器
//      *  - 关于滚动条
//      *      - chorme 认为滚动条是相对于body的，document.body.sorollTop/sorollLeft
//      *      - 其他浏览器认为滚动条是相对于HTML的,document.documentElement.sorollTop/sorollLeft
//      */
//     var x = event.pageX;
//     var y = event.pageY;
//     box1.style.left = x + "px";
//     box1.style.top = y + "px";
// }

/**
 * 鼠标拖拽的实现
 * 鼠标按下事件
 * 鼠标移动事件
 * 鼠标松开事件
 */

var box2 = document.getElementById("box2");
// 为box2添加一个
box2.onmousedown = function(event){
    event = event || window.event;
    var m = event.clientX - box2.offsetLeft;
    var n = event.clientY - box2.offsetTop;
    
    document.onmousemove = function(event){
        event = event || window.event;
        var x = event.pageX - m;
        var y = event.pageY - n;
        box2.style.left = x + "px";
        box2.style.top = y + "px";
    };
    document.onmouseup = function(){
        document.onmousemove = null;
    }
    return false;
}