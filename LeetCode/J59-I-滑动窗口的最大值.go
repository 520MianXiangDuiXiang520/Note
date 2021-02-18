package main

import "fmt"

func getMax(nums []int) (index, value int) {
	value = nums[0]
	for i, v := range nums {
		if v > value {
			index, value = i, v
		}
	}
	return
}

func maxSlidingWindow(nums []int, k int) (res []int) {
	if k <= 1 {
		return nums
	}
	if k > len(nums) {
		k = len(nums)
	}
	left, right := 0, k-1
	maxIndex, maxValue := getMax(nums[left : right+1])
	if k == len(nums) {
		return []int{maxValue}
	}
	res = append(res, maxValue)

	for right < len(nums) {
		left++
		right++
		if right < len(nums) {
			if maxIndex < left {
				maxIndex, maxValue = getMax(nums[left : right+1])
				maxIndex += left
			} else {
				if nums[right] > maxValue {
					maxValue = nums[right]
					maxIndex = right
				}
			}
			res = append(res, maxValue)
		}

	}
	return
}

func main() {
	fmt.Println(maxSlidingWindow([]int{7, 2, 4}, 2))
}
