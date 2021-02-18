// 找到所有数组中消失的数字

package main

import (
	"fmt"
)


// 最直观的想法是使用一个 map 保存 nums 中每一个元素出现的次数
// 同时维持一个最大值，然后遍历 map 得到结果，这时空间复杂度为 O(n),
// 时间复杂度为 O(n);
// 由于 nums 中元素的范围是 1 ~ n, 所以也可以使用一个 n 位长的数组代替 map
// 时间空间复杂度不变；
// 由于 n 等于数组大小，所以可以使用给定的 nums 数组充当上面的数组，遍历 nums,
// 如果得到 x, 则将 nums[x - 1] 置为 -nums[x - 1] (为了不丢失原来的值)，
// 最后再遍历一遍 nums，如果 nums[x] > 0 则缺失了 x + 1
func findDisappearedNumbers(nums []int) (res []int) {
	for _, v := range nums {
		if v < 0 {
			v =  0 - v
		}
		if nums[v - 1] > 0 {
			nums[v - 1] = -nums[v - 1]
		}
	}
		for i, v := range nums {
		if v > 0 {
			res = append(res, i + 1)
		}
	}
	return
}


func main() {
	fmt.Println(findDisappearedNumbers([]int{4, 3, 2, 7, 8, 2, 3, 1}))
}