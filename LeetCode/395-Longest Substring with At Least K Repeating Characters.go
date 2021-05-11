package main

import (
	"fmt"
	"strings"
)

func longestSubstring(s string, k int) int {
	dict := [26]int{}
	if len(s) < k {
		return 0
	}
	// 如果一个字符 c 在 s 中甚至没有出现 k 次，那包含 c 的字串
	// 必定不在答案中，所以以 c 分隔字符串后，答案一定在这些字串中
	for _, c := range s {
		if dict[c-'a'] > 0 {
			continue
		}
		dict[c-'a'] = 1
		if strings.Count(s, string(c)) < k {
			max := 0
			for _, child := range strings.Split(s, string(c)) {
				if child != "" {
					fmt.Println(child, s, string(c))
					r := longestSubstring(child, k)
					if r > max {
						max = r
					}
				}
			}
			return max
		}
	}
	return len(s)
}

func main() {
	fmt.Println(longestSubstring("bchhbbdefghiaaacb", 3))
}
