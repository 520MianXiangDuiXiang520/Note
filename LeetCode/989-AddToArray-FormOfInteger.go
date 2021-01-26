// 数组形式的加法
package main

import "fmt"

func addToArrayForm(A []int, K int) []int {
	res := make([]int, 0)
	for i := len(A) - 1; i >= 0; i-- {
		if K <= 0 {
		    res = append(res, A[i])	
		} else {
			k := K % 10             // 
			K /= 10                 // 
			sum := A[i] + k         // 12 8  5
			if sum >= 10 {
				K ++                // 52
				sum %= 10           // 2
			}
			res = append(res, sum)  // 2, 8, 5
		}
	}
	for K > 0 {
		k := K % 10
		K /= 10
		res = append(res, k)
	}
	start, end := 0, len(res) - 1
	for start < end {
		res[start], res[end] = res[end], res[start]
		start ++
		end --
	}
	return res
}

func main() {
	fmt.Println(addToArrayForm([]int{1,2,6}, 919))
}