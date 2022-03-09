package main

import (
	"strings"
	"fmt"
)

func modifyString(s string) string {
    var a [] byte = []byte(s)
    var n int = len(s)
    for i := 0; i < n; i ++ {
        if s[i] == '?' {
            for c := byte('a'); c < 'd'; c ++ {
                if (0 <= i - 1 && a[i - 1] == c) || (i + 1 < n && a[i + 1] == c) {
                    continue
                } else {
                    a[i] = c
                    break
                }
            }
        }
    }
    return string(a)
}

func main() {
	fmt.Println(modifyString("j?qg??b"))
	fmt.Println(modifyString("?c"))
	fmt.Println(modifyString("a?"))
	fmt.Println(modifyString("a?c?c"))
	fmt.Println(modifyString("a?c?"))
	fmt.Println(modifyString("c?c"))
	fmt.Println(modifyString("c????c"))
}