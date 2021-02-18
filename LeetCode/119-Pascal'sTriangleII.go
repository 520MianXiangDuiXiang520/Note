//  杨辉三角

package main

import (
	"fmt"
)

func getRow(rowIndex int) []int {
	if rowIndex == 0 {
		return []int{1}
	}
	if rowIndex == 1 {
		return []int{1, 1}
	}
	pre := []int{1, 1}
	var res []int
	for row := 2; row <= rowIndex; row++ {
		res = make([]int, row + 1)
		res[0] = 1
		for i := 1; i < row; i++ {
			res[i] = pre[i] + pre[i - 1]
		}
		res[row] = 1
		pre = res
	}
	return res
}

func main() {
	fmt.Println(getRow(3))
}