mvvm

model:
view
viewModel(数据绑定，DOM监听)

语法：

1. {{}}
2. 强制数据绑定 `v-bind: src=""` 或 `:src=""`
3. 绑定数据监听
4. v-text
5. v-html
6. methods() 回调函数(你定义的，你没有调用，它执行了)
7. v-model
8. 计算属性：computed: {} 初始化和相关数据发生改变时执行（缓存）
9. 监视：watch

```vue
firstname: function (value) {
    // 需要读取当前属性值时回调，
    get() {
         this.fullname = value + " " + lastname
    }
    // 属性值发生改变时回调(监视当前值的变化)
    set (newvalue, oldwalue) {

    }
   
}
```

遍历时的变异方法