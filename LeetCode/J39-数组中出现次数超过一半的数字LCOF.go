package main

import "fmt"

func majorityElement(nums []int) int {
	// hash := make(map[int]int)
	// for _, v := range nums {
	// 	hash[v] ++
	// 	if hash[v] > len(nums) / 2 {
	// 		return v
	// 	}
	// }
	// return 0

	// 摩尔排序
	magor, count := nums[0], 1
	for i := 1; i < len(nums); i++ {
		if nums[i] == magor {
			count ++
			if count > len(nums) / 2 {
				return magor
			}
		} else {
			if count > 0 {
				count --
			} else {
				magor = nums[i]
				count = 1
			}
		}
	}
	return magor
}

func main() {
	fmt.Println(majorityElement([]int{1, 2, 3, 2, 2, 2, 5, 4, 2}))
}