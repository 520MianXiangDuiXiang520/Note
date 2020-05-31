## 信号和槽

参数：

1. 信号发送者
2. 信号（事件）
3. 信号接收者
4. 槽函数（响应）

```cpp
connect(btn, &QPushButton::clicked,this, &QPushButton::close);
```

