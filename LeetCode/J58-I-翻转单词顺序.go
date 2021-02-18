package main

import (
	"fmt"
	"strings"
)

func reverseWords(s string) string {
	sSlice := strings.Split(s, " ")
	res := make([]string, 0)
	for i := len(sSlice) - 1; i >= 0; i -- {
		if sSlice[i] == "" {
			continue
		}
		res = append(res, sSlice[i])
	}
	return strings.Join(res, " ")
}

func main() {
	fmt.Println(reverseWords("  hello world!  "))
}

