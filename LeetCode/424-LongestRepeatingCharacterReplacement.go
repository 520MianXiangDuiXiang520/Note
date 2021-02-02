// 替换后的最长重复字符
// 滑动窗口

package main

import "fmt"

func getMax(ints []int) int {
	max := ints[0]
	for i := 1; i < len(ints); i++ {
		if max < ints[i] {
			max = ints[i]
		}
	}
	return max
}

func characterReplacement(s string, k int) int {
	size := len(s)
	if k >= size || size <= 1 {
		return size
	}
	cache := make([]int, 26)
	left, right := 0, 0
	for right = 0; right < size; right++ {
		cache[int(s[right]-'A')]++
		// fmt.Println(cache)
		if getMax(cache)+k < right-left+1 {
			cache[int(s[left]-'A')]--
			left++
		}
	}
	return right - left
}

func main() {
	fmt.Println(characterReplacement("ABAA", 1))
}
