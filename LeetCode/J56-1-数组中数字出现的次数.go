package main

import "fmt"


// 只有两个数字出现了一次，找出这两个数字
// 两个相同的数字异或结果为 0， 所以所有数字异或结果为两个只出现了一次的数字异或的结果
// 所有数字异或的结果必然存在一位为 1， 两个只出现了一次的数字的这一位必定不相同
// 根据这一位将数组分为两半，每一半分别做异或得到的就是所求的值
func singleNumbers(nums []int) []int {
	//  整体做异或
	k := 0
	for _, v := range nums {
		k ^= v
	}

	// 找到 k 中的值为 1 的某一位（最低位）
	mask := 1
	for k & mask == 0 {
		mask <<= 1
	}

	// 分组异或
	a, b := 0, 0
	for _, v := range nums {
		if v & mask == 0 {
			a ^= v
		} else {
			b ^= v
		}
	}

	return []int{a, b}

}

func main() {
	fmt.Println(singleNumbers([]int{1, 2, 5, 2}))
}