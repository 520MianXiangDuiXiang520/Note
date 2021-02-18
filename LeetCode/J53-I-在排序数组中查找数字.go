package main

import (
	"fmt"
)

func find(nums []int, target int) (index int) {
	left, right := 0, len(nums) - 1
	for left <= right {
		mid := left + (right - left) / 2
		if nums[mid] == target {
			return mid
		} else if nums[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	return -1
}

func search(nums []int, target int) int {
	index := find(nums, target)
	fmt.Println(index)
	if index == -1 {
		return 0
	}
	res := 1
	for i := index - 1; i >= 0 && nums[i] == target; i -- {
		res ++
	}
	for i := index + 1; i < len(nums) && nums[i] == target; i ++ {
		res ++
	}
	return res
}

func main() {
	fmt.Println(search([]int{6}, 6))
	fmt.Println(search([]int{6, 7, 8, 8, 9, 9, 9, 10}, 9))
}