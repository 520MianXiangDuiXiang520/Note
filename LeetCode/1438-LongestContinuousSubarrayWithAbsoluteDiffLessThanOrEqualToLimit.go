package main

import "fmt"

func longestSubarray(nums []int, limit int) (ans int) {
    var minQ, maxQ []int
    left := 0
    for right, v := range nums {
        for len(minQ) > 0 && minQ[len(minQ)-1] > v {
            minQ = minQ[:len(minQ)-1]
        }
        minQ = append(minQ, v)
        for len(maxQ) > 0 && maxQ[len(maxQ)-1] < v {
            maxQ = maxQ[:len(maxQ)-1]
        }
        maxQ = append(maxQ, v)
        for len(minQ) > 0 && len(maxQ) > 0 && maxQ[0]-minQ[0] > limit {
            if nums[left] == minQ[0] {
                minQ = minQ[1:]
            }
            if nums[left] == maxQ[0] {
                maxQ = maxQ[1:]
            }
            left++
        }
        ans = max(ans, right-left+1)
    }
    return
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}


func main() {
	fmt.Println(longestSubarray([]int{2,2,2,4,4,2,5,5,5,5,5,2}, 2))
}
