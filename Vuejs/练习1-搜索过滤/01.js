let vm = new Vue({
    el : '#app',
    data : {
        something : "",
        isnone : true,
        students : [
            {name:'zhangsan',age:18,sex:'boy'},
            {name:'zhangsi',age:20,sex:'boy'},
            {name:'baigujin',age:18,sex:'girl'},
            {name:'yutujin',age:19,sex:'girl'}
        ],
    },
    computed: {
        showinfo(){
            // showword是筛选之后的数组
            let showword
            this.isnone = true
            // console.log(this.students)
            let {something,isnone,students} = this
            showword = students.filter(function(item){
                isin = item.name.indexOf(something)
                return isin >= 0
            })
            if(showword.length == 0){
                vm.$data.isnone = false
                showword = ['can not find']
            }
            return showword
        }
    },
})