/**
 * 要为每一个a标签添加一个单击响应函数
 * 利用事件的绑定，为a的父标签添加
 * 通过方法调用，this指向调用该方法的对象，div
 * 要获取触发事件的对象，使用事件的target属性
 * 会为整个div添加事件，需要判断
 */

 var div1 = document.getElementById("div1");
 div1.onclick = function(event){
     event = event || window.event;
    //  alert(event.target.tagName);
     if (event.target.tagName == "A"){
        alert(event.target.innerHTML);
     }
 }