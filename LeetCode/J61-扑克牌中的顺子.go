package main

import (
	"fmt"
	"sort"
)

func isStraight(nums []int) bool {
	sort.Slice(nums, func(i, j int)bool{return nums[i] < nums[j]})
	// fmt.Println(nums)
    less, zero := 0, 0
    for i, v := range nums {
        if v == 0 {
            zero ++
        }else if i < 4 {
			l := nums[i + 1] - nums[i]
			if l == 0 {
				return false
			}
            if l > 1 {
                less += l - 1
            }
            
        }
	}
	// fmt.Println(less, zero)
    return less <= zero 
}

func main() {
	fmt.Println(isStraight([]int{4,7,5,9,2}))
}