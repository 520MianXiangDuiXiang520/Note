// 尽可能使字符串相等
// 滑动窗口

package main

import "fmt"

func equalSubstring(s string, t string, maxCost int) (maxLen int) {
    n := len(s)
    diff := make([]int, n)
    for i, ch := range s {
        diff[i] = abs(int(ch) - int(t[i]))
	}
	left, right := 0, 0
	sum := diff[0]
	if sum <= maxCost {
		maxLen = 1
	}
	for right < n {
		if sum > maxCost {
			// 窗口向右huadong
			sum -= diff[left]
			left ++	
		}
		right ++
		if right < n {
			sum += diff[right]
		}
		
		if sum <= maxCost && right < n && right - left + 1 > maxLen{
			maxLen = right - left + 1
		}
	}
    return
}

func abs(x int) int {
    if x < 0 {
        return -x
    }
    return x
}


func main(){
	fmt.Println(equalSubstring("abcd", "cdee", 5))
}