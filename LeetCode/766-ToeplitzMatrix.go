// 托普利茨矩阵

package main

import "fmt"

func equal(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func isToeplitzMatrix(matrix [][]int) bool {
	lineSize := len(matrix[0])
	for i := 0; i < len(matrix) - 1; i++ {
		if !equal(matrix[i][:lineSize - 1], matrix[i + 1][1:]) {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(isToeplitzMatrix([][]int{
		{1, 2, 3, 4},
		{5, 1, 2, 3},
		{7, 5, 1, 2},
		{8, 7, 5, 1},
		{9, 8, 7, 51},
	}))
}