package main

import "fmt"

func min(nums map[int]int) int {
	if len(nums) == 0 {
		return 0
	}
	res := 100000000000
	for _, v := range nums {
		if v < res {
			res = v
		}
	}
	return res
}

func leastBricks(wall [][]int) int {
	maxRes := len(wall)
	if maxRes == 0 {
		return 0
	}
	dict := make(map[int]int)
	for _, row := range wall {
		end := 0
		for j := 0; j < len(row) - 1; j++ {
			end += row[j]
			_, ok := dict[end]
			if ok {
				dict[end] --
			} else {
				dict[end] = maxRes - 1
			}
		}
		// fmt.Println()
	}
	if len(dict) == 0 {
		return maxRes
	}
	return min(dict)
}

func main() {
	fmt.Println(leastBricks([][]int{
		// {1, 2, 2, 1}, {3, 1, 2}, {1, 3, 2}, {2, 4}, {3, 1, 2}, {1, 3, 1, 1},
		// {1}, {1}, {1},
		{},
	}))
}