// 滑动窗口中的中位数
// 滑动窗口

package main

import (
	"fmt"
	"sort"
)

func getMid(nums []int) float64 {
	if len(nums)%2 == 0 {
		return (float64(nums[len(nums)/2]) + float64(nums[len(nums)/2-1])) / 2
	}
	return float64(nums[int(len(nums)/2)])
}


// 将 x 插入有序集合 nums 中
func add(nums []int, x int) []int {
	index := 0
	if x >= nums[len(nums) - 1] {
		index = len(nums)
	} else if x <= nums[0] {
		index = 0
	} else {
		index = sort.Search(len(nums) - 1, func(i int) bool {return nums[i] >= x})
	}
	
	// fmt.Println(index)
	end := make([]int, len(nums[index:]))
	for i := 0; i < len(nums[index:]); i++ {
		end[i] = nums[index+i]
	}
	pre := nums[:index]
	pre = append(pre, x)
	return append(pre, end...)
}

func medianSlidingWindow(nums []int, k int) []float64 {
	if len(nums) <= k {
		sort.Slice(nums, func(i, j int) bool { return nums[i] < nums[j] })
		return []float64{getMid(nums)}
	}
	if k == 1 {
		res := make([]float64, len(nums))
		for i := 0; i < len(nums); i++ {
			res[i] = float64(nums[i])
		}
		return res
	}
	save := make([]int, len(nums))
	for i := 0; i < len(nums); i++ {
		save[i] = nums[i]
	}
	left, right := 0, k-1
	window := nums[left : right+1]
	res := make([]float64, len(nums)-k+1)
	sort.Slice(window, func(i, j int) bool { return window[i] < window[j] })

	for right < len(nums) {
		res[right-k+1] = getMid(window)
		right++
		// fmt.Println("window: ", window, "remove: ", left, save[left])
		index := sort.SearchInts(window, save[left])
		end := append(window[:index], window[index+1:]...)
		
		if right < len(nums) {
			// fmt.Println("end: ", end, " ,add: ", save[right])
			window = add(end, save[right])
			left++
		}
		// fmt.Println("window: ", window)

	}
	return res
}

func main() {

	fmt.Println(medianSlidingWindow([]int{4,1,7,1,8,7,8,7,7,4}, 4))
	// fmt.Println(add([]int{5, 8, 8, 9}, 6))
	// fmt.Println(remove([]int{-5, -3, 2, 7, 10}, -3))
}
