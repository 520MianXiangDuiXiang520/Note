// 情侣牵手
package main

import (
	"fmt"
)


func minSwapsCouples(row []int) int {
    n := len(row)
	position := make([]int, n)
	for k, v := range row {
		position[v] = k
	}
	res := 0
	for i := 0; i < n; i += 2 {
		lovers := row[i]^1
		if row[i+1] == lovers {
			continue
		}
		res++
		other := row[i+1]
		row[i+1], row[position[lovers]] = row[position[lovers]], row[i+1]
		position[lovers], position[other] = position[other], position[lovers]
	}
	return res
}

func main() {
	fmt.Println(minSwapsCouples([]int{0, 2, 1, 3}))
}