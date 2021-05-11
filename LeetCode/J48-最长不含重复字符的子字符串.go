package main

import "fmt"

func lengthOfLongestSubstring(s string) int {
	size := len(s)
	if size <= 1 {
		return size
	}
	maxLen := 0
	m := make(map[byte]struct{}, 0)
	for left, right := 0, 0; right < len(s); {
		if _, ok := m[s[right]]; ok {
			delete(m, s[left])
			left++
		} else {
			m[s[right]] = struct{}{}
			right++
		}
		if right-left > maxLen {
			maxLen = right - left
		}
	}
	return maxLen
}

func main() {
	fmt.Println(lengthOfLongestSubstring("pwwkeww"))
}
