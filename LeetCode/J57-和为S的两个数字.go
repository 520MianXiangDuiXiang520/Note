package main

import (
	"fmt"
)

func twoSum(nums []int, target int) []int {
	left, right := 0, len(nums) - 1
	for ;right >= left && nums[right] > target; right -- {}
	for right > left {
		if nums[left] + nums[right] < target {
			left ++
		} else if nums[left] + nums[right] > target {
			right --
		} else {
			return []int{nums[left], nums[right]}
		}
	}
	return []int{0,0}

}

func main() {

}