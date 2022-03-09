package main

import "fmt"
import "strings"

func findOcurrences(text string, first string, second string) []string {
	var res []string
	list := strings.Split(text, " ")
	size := len(list)
	if size < 3 {
		return res
	}
	for i := 0; i < size-2; i++ {
		if list[i] == first && list[i+1] == second {
			res = append(res, list[i+2])
		}
	}
	return res
}

func main() {
	fmt.Println(findOcurrences("alice is a good girl she is a good student",
		"a",
		"good"))
}
