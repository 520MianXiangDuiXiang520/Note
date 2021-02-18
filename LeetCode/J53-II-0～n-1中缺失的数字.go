package main

import (
	"fmt"
)

func missingNumber(nums []int) int {
	right := len(nums) - 1
	left := 0
	for left <= right {
		mid := left + (right-left)/2
		if nums[mid] > mid {
			right = mid - 1
		} else if nums[mid] == mid {
			left = mid + 1
		}

	}
	return left
}

func main() {
	fmt.Println(missingNumber([]int{0, 1, 2, 3, 4, 5, 6, 8}))
}
