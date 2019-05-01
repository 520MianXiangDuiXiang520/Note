var Demo01=new Vue({
    el : '#vue-det',
    data : {
        name : "test-01",
        html : "<a href='www://google.com'>谷歌</a>",
        href : "https://www.baidu.com",
        message : 'message',
        date : Date(),
    },
    methods : {
        fun1 : function(){
           return this.name="test-001";
        },
    },
})