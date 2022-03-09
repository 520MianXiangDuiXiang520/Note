package main

import "fmt"

func construct2DArray(original []int, m int, n int) [][]int {
    size := len(original)
    if m * n != size {
        return [][]int{}
    }
    res := make([][]int, m)
    for i := 0; i < m; i++ {
        res[i] = original[i * n: i * n + n]
    }
    return res
}

func main() {
	fmt.Println(construct2DArray([]int{1, 2, 3, 4, 5, 6}, 3, 2))
}