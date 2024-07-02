# 100 道 shell 练习题

1. 循环 ping 192.168.110 网段的所有主机, 找到所有在线的地址

```sh
#!/bin/bash

for i in {0..255}; do
    ipAddr="192.168.110.$i"
    if ping -i 0.2 -c 2 -W 0.5 "$ipAddr" >/dev/null; then
        echo "$ipAddr ping success"
    else
        echo "$ipAddr ping fail"
    fi
done
```

* 可以使用 `for i in {0..255}` 代替 `for ((i = 0; i <= 255; i++))` 前者是 shell 的一种拓展语法：https://opengers.github.io/linux/linux-shell-brace-parameter-command-pathname-expansion/
* 判断语句是否执行成功时使用 `if commond; then` 代替 `command \n if [ $? -eq 0 ];then` 参见：[SC2181](https://www.shellcheck.net/wiki/SC2181)

## 参考

https://cloud.tencent.com/developer/article/1691052

