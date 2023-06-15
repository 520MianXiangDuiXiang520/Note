package main

import "fmt"

func numTimesAllBlue(flips []int) int {
	res := 0
	max := flips[0]
	for i, flip := range flips {
		if flip > max {
			max = flip
		}
		if max == i+1 {
			res += 1
		}
	}
	return res
}

func main() {
	cases := [][]int{
		{1, 15, 24, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 2, 57, 27, 18, 19, 79, 21, 22, 23, 3, 25, 46, 17, 59, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 26, 47, 65, 49, 50, 51, 52, 53, 54, 55, 56, 16, 58, 28, 60, 61, 69, 62, 64, 48, 66, 67, 68, 63, 70, 71, 72, 73, 74, 75, 76, 77, 78, 20, 80, 81},
		{3, 2, 4, 1, 5},
	}
	ans := []int{4, 2}
	for i, ca := range cases {
		res := numTimesAllBlue(ca)
		if res != ans[i] {
			fmt.Printf("Error: %d want: %d got: %d", i, ans[i], res)
		}
	}
}
