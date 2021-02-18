package main

import "fmt"

func maxProfit(prices []int) int {
	min := prices[0]
	max := -1
	for i := 0; i < len(prices); i++ {
		if min > prices[i] {
			min = prices[i]
		}
		m := prices[i] - min
		if max < m {
			max = m
		}
	}
	return max
}

func main() {
	fmt.Println(maxProfit([]int{7, 1, 5, 3, 6, 4}))
}