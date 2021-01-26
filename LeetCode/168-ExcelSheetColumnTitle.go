// Excel表列名称
package main

import "fmt"

func convertToTitle(n int) string {
	res := ""
	for n > 0 {
		n --
		res = fmt.Sprintf("%s%s",res, string('A' + n % 26))
		n /= 26
	}
	return res
}

func main() {
	fmt.Println(convertToTitle(702))
}