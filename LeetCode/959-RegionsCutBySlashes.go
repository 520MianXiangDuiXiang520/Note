// 有斜杠划分区域
package main

import "fmt"

type UnionFind struct {
	Parents []int
	Rank    []int
}

func (uf *UnionFind) findRoot(x int) int {
	if uf.Parents[x] == -1 {
		return x
	}
	return uf.findRoot(uf.Parents[x])
}

func (uf *UnionFind) union(x, y int) {
	rootX, rootY := uf.findRoot(x), uf.findRoot(y)
	if rootX == rootY {
		return
	}
	if uf.Rank[rootX] > uf.Rank[rootY] {
		uf.Parents[rootY] = rootX
	} else if uf.Rank[rootX] < uf.Rank[rootY] {
		uf.Parents[rootX] = rootY
	} else {
		uf.Parents[rootX] = rootY
		uf.Rank[rootY] ++
	}
}

func regionsBySlashes(grid []string) int {
	N := len(grid)
	size := 4 * N * N
	uf := UnionFind {
		Parents: make([]int, size),
		Rank:    make([]int, size),
	}
	for i := 0; i < size; i++ {
		uf.Parents[i] = -1
	}

	squareIndex := 0
	for line := 0; line < N; line++ {
		for row := 0; row < len(grid[line]); {
			// 说明上面有东西，需要与上面的网格合并
			if line > 0 {
				upSquareIndex := squareIndex - N
				uf.union(squareIndex * 4, upSquareIndex * 4 + 2)
			}
			// 说明左面有东西，需要和左面的网格合并
			if row > 0 {
				leftSquareIndex := squareIndex - 1
				uf.union(squareIndex * 4 + 3, leftSquareIndex * 4 + 1)
			}
			if grid[line][row] == '/' {
				uf.union(squareIndex * 4, squareIndex * 4 + 3)
				uf.union(squareIndex * 4 + 1, squareIndex * 4 + 2)
				row ++
			} else if grid[line][row] == '\\' {
				uf.union(squareIndex * 4, squareIndex * 4 + 1)
				uf.union(squareIndex * 4 + 2, squareIndex * 4 + 3)
				row ++
			} else {
				uf.union(squareIndex * 4, squareIndex * 4 + 1)
				uf.union(squareIndex * 4 + 1, squareIndex * 4 + 2)
				uf.union(squareIndex * 4 + 2, squareIndex * 4 + 3)
				row ++
			}
			squareIndex ++
		}
	}
	res := 0
	for i := 0; i < size; i ++ {
		if uf.Parents[i] == -1 {
			res ++
		}
	}
	return res
}

func main() {
	res := regionsBySlashes([]string{
		"/\\", "\\/",
	})
	fmt.Println(res)
}