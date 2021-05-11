package main

import "fmt"

type value struct {
	v [3]int
}

func findShortestSubArray(nums []int) int {
	if len(nums) <= 1 {
		return len(nums)
	}
	// [0] 第一次出现的位置
	// [1] 最后一次出现的位置
	// [2] 出现的次数
	cache := make(map[int]value)
	max := 0
	maxs := make([]int, 0)
	for i, v := range nums {
		
		if cache[v].v[2] == 0 {
			cache[v] = value{
				v: [3]int{i, 0, 0},
			}
		}
		get := cache[v].v
		n := get[2]
		cache[v] = value {
			v: [3]int{get[0], i, n + 1},
		}
		
		if n + 1 == max {
			maxs = append(maxs, v)
		} else if n + 1 > max {
			maxs = []int{v}
			max = n + 1
		}
	}
	// fmt.Println(cache)
	res := 1000000000
	for _, v := range maxs {
		if cache[v].v[2] == 1 {
			return 1
		}
		r := cache[v].v[1] - cache[v].v[0] + 1
		if r < res {
			res = r
		}
	}
	return res
}

func main() {
	fmt.Println(findShortestSubArray([]int{1, 2, 2, 3, 1}))
}