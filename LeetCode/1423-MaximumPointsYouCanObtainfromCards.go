// 可获得的最大点数
// 滑动窗口

package main

import "fmt"

func sumSlice(nums []int) (res int) {
	for _, v := range nums {
		res += v
	}
	return
}

// 思路：维持两个滑动窗口，两个滑动窗口长度和为 k, 看那种情况 sum 最大
func maxScore(cardPoints []int, k int) int {
	size := len(cardPoints)
	if size <= k {
		return sumSlice(cardPoints)
	}
	left, right := 0, k - 1
	sumLeft := sumSlice(cardPoints[left: right + 1])
	sumRight := 0
	res := sumLeft
	right --
	for ;right >= -1; right -- {
		sumLeft -= cardPoints[right + 1]
		lenRight := k - right + left - 1
		sumRight += cardPoints[size - lenRight]
		sum := sumLeft + sumRight
		if res < sum {
			res = sum
		}
	}
	return res
}

func main() {
	fmt.Println(maxScore([]int{13, 2, 1, 7, 6, 200, 1, 0}, 3))
}