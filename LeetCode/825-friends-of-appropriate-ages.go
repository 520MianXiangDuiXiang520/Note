package main

import (
    "sort"
)

func numFriendRequests(ages []int) (ans int) {
    sort.Ints(ages)
    left, right := 0, 0
    for _, age := range ages {
        if age < 15 {
            continue
        }
        t := age + 14
        for ages[left]*2 <= t {
            left++
        }
        for right+1 < len(ages) && ages[right+1] <= age {
            right++
        }
        ans += right - left
    }
    return
}

func main() {
	numFriendRequests([]int{2, 6, 1})
}