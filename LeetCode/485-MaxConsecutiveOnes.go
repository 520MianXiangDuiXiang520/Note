// 最大连续 1 的个数
// 滑动窗口

package main


import "fmt"

func findMaxConsecutiveOnes(nums []int) int {
	left, right := 0, 0
	oneNumInWin := 0

	for right = 0; right < len(nums); right ++ {
		if nums[right] == 1 {
			oneNumInWin ++
		}
		if oneNumInWin < right - left + 1 {
			if nums[left] == 1 {
				oneNumInWin --
			}
			left ++
		}
	}
	return right - left
}

func main() {
	fmt.Println(findMaxConsecutiveOnes([]int{1, 1, 0, 1, 1, 1}))
}