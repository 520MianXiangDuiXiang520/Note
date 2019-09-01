/**
 * 代码如诗
 */
let vm = new Vue({
    el : '#app',
    data : {
        something : "",
        isnone : true,
        typesort : 0,
        students : [
            {name:'zhangsan',age:18,sex:'boy'},
            {name:'zhangsi',age:20,sex:'boy'},
            {name:'baigujin',age:18,sex:'girl'},
            {name:'yutujin',age:19,sex:'girl'}
        ],
    },
    methods: {
        ageup : function(type){
            this.typesort = type
        },
    },
    computed: {
        showinfo(){
            // showword是筛选之后的数组
            let showword
            this.isnone = true
            // console.log(this.students)
            let {something,students,typesort} = this
            showword = students.filter(function(item){
                isin = item.name.indexOf(something)
                return isin >= 0
            })
            if(showword.length == 0){
                vm.$data.isnone = false
                showword = ['can not find']
            }
            if(typesort !== 0){
                showword.sort(function(a,b){
                    if(typesort == 1){
                        // 升序排序
                        return a.age - b.age
                    }else{
                        return b.age - a.age
                    }
                })
            }
            return showword
        },
       
    },
})