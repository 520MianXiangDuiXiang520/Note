// 加 1

package main

import "fmt"

func plusOne(digits []int) []int {
	for i := len(digits) - 1; i >= 0; i-- {
		this := digits[i] + 1
		if this >= 10 {
			digits[i] = 0
		} else {
			digits[i] ++
			return digits
		}
	}
	res := make([]int, len(digits) + 1)
	res[0] = 1
	for i := 1; i < len(digits); i++ {
		res[i] = 0
	}
	return res
}

func main() {
    fmt.Println(plusOne([]int{
		9, 9, 9, 9,
	}))
}