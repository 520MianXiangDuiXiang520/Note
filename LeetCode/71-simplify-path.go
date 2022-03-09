package main

import (
	"fmt"
	"strings"
)

func simplifyPath(path string) string {
	list := strings.Split(path, "/")
	res := make([]string, 0)
	for _, p := range list {
		switch p {
		case ".":
		case "..":
			if len(res) != 0 {
				res = res[:len(res) - 1]
			}
		case "":
		default:
			res = append(res, p)
		}
	}
	return "/" + strings.Join(res, "/")
}

func main() {
	fmt.Println(simplifyPath("/a/./b/../../c/"))
	fmt.Println(simplifyPath("/a/./b/"))
	fmt.Println(simplifyPath("/home//foo/"))
	fmt.Println(simplifyPath("/../"))
}