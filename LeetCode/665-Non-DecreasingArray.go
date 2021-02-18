// 非递减数列

package main

import "fmt"

func checkPossibility(nums []int) bool {
    flag := false
    for i := 1; i < len(nums); i++ {
        if nums[i] < nums[i - 1] {
            if !flag {
                flag = true
                if i >= 2 && nums[i] < nums[i - 2] {
                    nums[i] = nums[i - 1];
                }  
            } else {
                return false
            }
        }

    }
    return true
}

func main() {
	fmt.Println(checkPossibility([]int{4, 2, 3}))
	fmt.Println(checkPossibility([]int{3, 4, 2, 3}))
}