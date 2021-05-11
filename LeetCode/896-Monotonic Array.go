package main

import "fmt"

func isMonotonic(A []int) bool {
	if len(A) <= 2 {
		return true
	}
	// 递增
	increasing := false
	i := 0
	for ; i < len(A) - 1; i++ {
		if A[i] < A[i + 1] {
			increasing = true
			break
		}
		if A[i] > A[i + 1] {
			break
		}
	} 
	for j := i; j < len(A) - 1; j ++ {
		if increasing && A[j] > A[j + 1] {
			return false
		}
		if !increasing && A[j] < A[j + 1] {
			return false
		}
	}
	return true
}

func main(){
	fmt.Println(isMonotonic([]int{5}))              // true
	fmt.Println(isMonotonic([]int{1, 1, 3, 4, 5}))  // true
	fmt.Println(isMonotonic([]int{1, 2, 2, 4, 5}))  // true
	fmt.Println(isMonotonic([]int{5, 4, 3, 2, 1}))  // true
	fmt.Println(isMonotonic([]int{5, 5, 3, 2, 1}))  // true
	fmt.Println(isMonotonic([]int{5, 5, 5, 5, 5}))  // true
	fmt.Println(isMonotonic([]int{5, 5, 6, 2, 1}))  // false
	fmt.Println(isMonotonic([]int{5, 5, 5, 1, 4}))  // false
}