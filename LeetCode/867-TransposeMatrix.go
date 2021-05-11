package main

import "fmt"

func transpose(matrix [][]int) [][]int {
	line, row := len(matrix), len(matrix[0])
	if line == row {
		for i := 0; i < line; i++ {
			for j := i; j < row; j++ {
				if j < line && i < row {
					matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
				}
			}
		}
		return matrix
	} else {

		res := make([][]int, row)
		for i := 0; i < row; i++ {
			res[i] = make([]int, line)
		}
		max := line
		if row > line {
			max = row
		}
		for i := 0; i < max; i++ {
			for j := i; j < max; j++ {
				if i < line && j < row {
					res[j][i] = matrix[i][j]
				}
				if i < row && j < line {
					res[i][j] = matrix[j][i]
				}
			}
		}
		return res
	}

}

func main() {
	fmt.Println(transpose([][]int{
		{1, 2},
		// {2},
		// {4, 5, 6},
	}))
	// 1 4 7
	// 2 5 6
	// 3 6 9
}
