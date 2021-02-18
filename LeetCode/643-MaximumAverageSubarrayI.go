// 子数组最大平均数
// 滑动窗口

package main

import "fmt"

func findMaxAverage(nums []int, k int) float64 {
	sum := nums[0]
	for i := 1; i < k; i++ {
		sum += nums[i]
	}
	res := float64(sum) / float64(k)
	if len(nums) == k {
		return res
	}
	left, right := 1, k
	for right < len(nums) {
		sum -= nums[left-1]
		sum += nums[right]
		p := float64(sum) / float64(k)
		if res < p {
			res = p
		}
		left++
		right++
	}
	return res
}

func main() {
	res := findMaxAverage([]int{1, 12, -5, -6, 50, 3}, 4)
	fmt.Println(res)
}
