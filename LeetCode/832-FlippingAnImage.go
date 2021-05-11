package main

import "fmt"

func not(a int) int {
	if a == 0 {
		return 1
	}
	return 0
}

func flipAndInvertImage(A [][]int) [][]int {
	size := len(A[0])
	for i, a := range A {
		left, right := 0, size - 1
		for left <= right {
			A[i][left], A[i][right] = not(a[right]), not(a[left])
			left ++
			right --
		}
	}
	return A
}

func main() {
	fmt.Println(flipAndInvertImage([][]int{
		{0, 1, 1},{1, 0, 1},
	}))
}