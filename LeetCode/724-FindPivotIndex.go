// 寻找数组的中心索引

package main

import "fmt"

func pivotIndex(nums []int) int {
	sum := 0
	for i := 0; i < len(nums); i++ {
		sum += nums[i]
	}
	left := 0
	for i := 0; i < len(nums); i++ {
		if left == sum - nums[i] - left {
			return i
		}
		left += nums[i]
	}
	return -1
}

func main() {
	fmt.Println(pivotIndex([]int{
		1, 2, 3,
	}))
}