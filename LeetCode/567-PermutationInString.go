// 字符串的排列
// 滑动窗口

package main

import (
	"fmt"
)

func checkInclusion(s1 string, s2 string) bool {
	s1Size, s2Size := len(s1), len(s2)
	if s1Size > s2Size {
		return false
	}
	s1Map := [26]int{}
	s2Map := [26]int{}
	for i := 0; i < s1Size; i++ {
		s1Map[s1[i] - 'a'] ++
	}

	left, right := 0, s1Size - 1
	for i := 0; i < s1Size; i++ {
		s2Map[s2[i] - 'a'] ++
	}
	if s1Map == s2Map {
		return true
	}

	
	right ++
	for ;right < s2Size; right++ {
		s2Map[s2[left] - 'a'] --
		s2Map[s2[right] - 'a'] ++
		left ++
		// fmt.Println(s1Map, s2Map)
		if s1Map == s2Map {
		    return true
	    }
	}
	return false

}

func main(){
	fmt.Println(checkInclusion("ab", "gccbcac"))
}