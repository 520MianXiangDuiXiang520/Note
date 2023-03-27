package main

import (
	"fmt"
	"sort"
)

func specialArray(nums []int) int {
	size := len(nums)
	if size == 0 {
		return -1
	}
	sort.Slice(nums, func(i, j int) bool {
		return nums[i] > nums[j]
	})
	if nums[size - 1] >= size {
		return size
	}
	for i := 1; i <= size; i++ {
        if nums[i-1] >= i && (i == size || nums[i] < i) {
            return i
        }
    }
	return -1
}

func main() {
	fmt.Println(specialArray([]int{5, 4, 0,1,0,4,3}))
	fmt.Println(specialArray([]int{5,3}))
}