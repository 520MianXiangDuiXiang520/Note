package main

import (
	"fmt"
)

// 快速幂
func myPow(x float64, n int) float64 {
	if n == 1 {
		return x
	}
	if n == 0 {
		return 1.0
	}
	if n < 0 {
		x = 1 / x
		n = 0 - n
	}
	t := myPow(x, n / 2)
	if n % 2 == 0 {
		return t * t
	}
	return t * t * x
}

func main() {
	fmt.Println(myPow(2.10000, 3))
	fmt.Println(myPow(2.00000, -2))
}