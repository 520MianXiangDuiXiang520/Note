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
    for (var i = 0; i < quanxuanlist.length; i++) {
        if (quanxuanlist[i].checked == false) {
            isCheckbox.checked = false;
            break;
        } else if (i == quanxuanlist.length - 1) {
            isCheckbox.checked = true;
        }
    };
});

//全选复选框
Check("is",function(){
    var s = true;
    for(var i = 0;i<quanxuanlist.length;i++){
        quanxuanlist[i].checked = this.checked;
    }
})

for(var i = 0; i < quanxuanlist.length; i++){
    quanxuanlist[i].onclick = function(){
        for (var i = 0; i < quanxuanlist.length; i++){   
            if (quanxuanlist[i].checked == false){
                isCheckbox.checked = false;
                break;
            }else if(i == quanxuanlist.length-1){
                isCheckbox.checked = true;
            }
        };
    }
}