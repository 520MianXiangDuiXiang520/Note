// 最长连续递增序列
package main

import "fmt"

func findLengthOfLCIS(nums []int) int {
	if len(nums) <= 1 {
		return len(nums)
	}
	exec := nums[0]
	maxLen := 0
	thisLen := 1
	for i := 1; i < len(nums); i++ {
		if nums[i] > exec {
			thisLen ++
		} else {
			if thisLen > maxLen {
				maxLen = thisLen
			}
			thisLen = 1
		}
		exec = nums[i]
	}
	if thisLen > maxLen {
		return thisLen
	}
	return maxLen
}

func main() {
	res := findLengthOfLCIS([]int{2, 3, 4, 3, 4, 5, 6})
	fmt.Println(res)
}