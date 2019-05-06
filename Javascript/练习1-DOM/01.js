function Check(InputId,fun){
    var items = document.getElementById(InputId);
    items.onclick = fun;
}
var quanxuanlist = document.getElementsByName("checkbox");
var isCheckbox = document.getElementById("is");
// 提交
Check("tijiao", function () {
    var quanxuanlist = document.getElementsByName("checkbox");
    for (var i = 0; i < quanxuanlist.length; i++) {
        if (quanxuanlist[i].checked) {
            alert(quanxuanlist[i].value)
        }
    }
});
//全选
Check("quanxuan", function () {  
    for (var i = 0; i < quanxuanlist.length; i++) {
        quanxuanlist[i].checked = true;
    }
    isCheckbox.checked = true;
});
//全不选
Check("quanbuxuan", function () {
    for (var i = 0; i < quanxuanlist.length; i++) {
        quanxuanlist[i].checked = false;
    }
    isCheckbox.checked = false;
});

//反选
Check("fanxuan", function () {
    for (var i = 0; i < quanxuanlist.length; i++) {
        if (quanxuanlist[i].checked == false) {
            quanxuanlist[i].checked = true;
        } else {
            quanxuanlist[i].checked = false;
        }
    }
});

//全选复选框
Check("is",function(){
    var s = true;
    for(var i = 0;i<quanxuanlist.length;i++){
        quanxuanlist[i].checked = isCheckbox.checked;
    }
})
