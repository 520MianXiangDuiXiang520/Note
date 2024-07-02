#!/bin/bash

# 循环 ping 192.168.110 网段的所有主机
for ((i = 0; i <= 255; i++)); do
    ipAddr="192.168.110.$i"
    if ping -i 0.2 -c 2 -W 0.5 "$ipAddr" >/dev/null; then
        echo "$ipAddr ping success"
    else
        echo "$ipAddr ping fail"
    fi
done
