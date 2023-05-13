
dlv 查看寄存器： regs
函数调用： rbp(栈底) 和 rsp(栈顶)

```
B 1 byte
W 2 byte
D 4 byte
Q 8 byte
```

常数用 `$` 开头

```
.data   数据段：有初始值的全局变量，自定义常量
.bss    数据段： 没有初始值的全局变量
.text   代码段
.rodata 只读数据段
```