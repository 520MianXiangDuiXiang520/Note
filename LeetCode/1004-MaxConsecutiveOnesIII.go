// 最大连续 1 的个数 III
// 滑动窗口

package main

import "fmt"

func longestOnes(A []int, K int) int {
	left, right := 0, 0
	oneNumInWin := 0

	for right = 0; right < len(A); right ++ {
		if A[right] == 1 {
			oneNumInWin ++
		}
		if oneNumInWin + K < right - left + 1 {
			if A[left] == 1 {
				oneNumInWin --
			}
			left ++
		}
	}
	return right - left
}

func main() {
	fmt.Println(longestOnes([]int{1,1,1,0,0,0,1,1,1,1,0}, 2))
}