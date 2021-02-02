// 公平的糖果棒交换

package main

import "fmt"

func fairCandySwap(A []int, B []int) []int {
    setB := make(map[int]struct{})
    sumB := 0
    for _, b := range B {
        sumB += b
        setB[b] = struct{}{}
    }
    sumA := 0
    for _, a := range A {
        sumA += a
    }
    fair := int((sumA + sumB) / 2)
    for _, a := range A {
        if _, ok := setB[fair - sumA + a]; ok {
            return []int{a, fair - sumA + a}
        } 
    }
    return []int{0, 0}
}

func main() {
	fmt.Println(fairCandySwap([]int{1, 1}, []int{2, 2}))
}