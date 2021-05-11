package main

import (
	`fmt`
)

func numRabbits(answers []int) int {
	cache := make(map[int]int)
	for _, v := range answers {
		cache[v] ++
	}
	res := 0
	for k, v := range cache {
		if v <= k + 1 {
			res += (k + 1)
		} else {
			y := v % (k + 1)
			if y == 0 {
				res += v / (k + 1) * (k + 1)
			} else {
				res +=  (v / (k + 1) + 1) * (k + 1)
			}
		}
	}
	return res
}

func main() {
	fmt.Println(numRabbits([]int{1, 1, 5}))
}