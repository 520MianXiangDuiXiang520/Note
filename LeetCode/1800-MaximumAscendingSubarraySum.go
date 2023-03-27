package main

import "fmt"

func maxAscendingSum(nums []int) int {
	size := len(nums)
	if size == 0 {
		return 0
	}
	res := nums[0]
	this := res
	for i := 1; i < size; i++ {
		if nums[i] > nums[i - 1] {
			this += nums[i]
			if this > res {
				res = this
			}
		} else {
			this = nums[i]
		}
	}
	return res
}

func main() {
	fmt.Println(maxAscendingSum([]int{1, 2, 3, 2, 10, 200, 230, 340, 20}))
}