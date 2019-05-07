
var delelist = document.getElementsByTagName("a");
console.log(delelist)

/**
 * 删除
 * 对列表中的每一个对象添加一个点击响应方法
 * 要删除的是整个tr标签，delelist中是a标签对象，他的夫标签是td，td的父标签才是tr，
 * 要删除tr，要用table.removeChild()
 * this 作为方法被调用，指向调用它的那个对象，也就是delelist[i]
 * 为什么delelist[i]在绑定方法之后会变成underfind？？？
 * 获取name
 */

function fun() {
    console.log(this);
    var tr = this.parentNode.parentNode;
    var name = tr.children[0].innerText;
    var isdele = confirm("确定要删除" + name + "吗？");
    if (isdele) {
        tr.parentNode.removeChild(tr);
    }
}

 for(var i = 0; i < delelist.length; i++){
     delelist[i].onclick = fun;
 }

 /**
  * 插入
  * createElement()
  * 1. 先为按钮添加一个方法
  * 2. 得到输入框中输入的数据
  *     - value
  * 3. 创建元素节点 `createElement()`
  *     - tr 标签，父标签是table
  *     - 两个td标签，父标签是tr
  */

  var button = document.getElementById("button");
  button.onclick = function(){
    //   confirm("aaa");
      var inputName = document.getElementById("inputName").value;
      var inputPnum = document.getElementById("inputPnum").value;
      var tableTab = document.getElementById("table");
      var newtr = document.createElement("tr");
      // name
      var newName = document.createElement("td");
      newName.innerHTML = inputName;
      newtr.appendChild(newName);
      // phoneNumber
      var newPnum = document.createElement("td");
      newPnum.innerHTML = inputPnum;
      newtr.appendChild(newPnum);
      // 操作
      var newCaozuo = document.createElement("td");
      var newA = document.createElement("a");
      newA.href = "javascript: ;";
      newA.innerHTML = "删除";
      newA.onclick = fun;
      newCaozuo.appendChild(newA);
      newtr.appendChild(newCaozuo);
      var tbody = tableTab.getElementsByTagName("tbody")[0];
      tbody.appendChild(newtr);
  }