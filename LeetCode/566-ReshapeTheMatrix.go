// 重塑矩阵
package main

import "fmt"

func matrixReshape(nums [][]int, r int, c int) [][]int {
	line, row := len(nums), len(nums[0])

	if line == r && row == c {
		return nums
	}

	if line * row != r * c {
		return nums
	}

	res := make([][]int, r)
	for i := 0; i < r; i++ {
		res[i] = make([]int, c)
	}
	
	for i := 0; i < r * c; i++ {
		res[i / c][i % c] = nums[i / row][i % row] 
	}
	return res
}

func main() {
	fmt.Println(matrixReshape([][]int{
		{1, 2, 3, 4,  5,  6},
		{7, 8, 9, 10, 11, 12},
	}, 3, 4))
}