# shell 练习

每天一道 shell 练习题

## 01.循环 ping 192.168.110 网段的所有主机, 打印所有在线的地址

```sh
function find_online_addr () {
    for((i=0;i<255;i++)); do
        ip_addr="192.168.110.$i"
        if ping -c 2 -W 0.5 -i 0.2 $ip_addr > /dev/null;then
            echo "$ip_addr online"
        else
            echo "$ip_addr outline"
        fi
    done
}
```

可以使用 拓展（Expansions）来替换上面的循环：

```sh
function finc_online_addr_with_expansions() {
    for i in {0..255}; do
        ip_addr="192.168.110.$i"
        if ping -c 2 -W 0.5 -i 0.2 "$ip_addr" >/dev/null; then
            echo "$ip_addr online"
        else
            echo "$ip_addr outline"
        fi
    done
}
```