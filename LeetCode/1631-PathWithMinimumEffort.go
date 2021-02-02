// 最小体力消耗路径
// 并查集 + 二分查找

package main

import (
	"fmt"
	"sort"
)

type UnionFind struct {
	Parents []int
	Rank    []int
}

func initUnionFind(n int) *UnionFind {
	uf := UnionFind {
		Parents: make([]int, n),
		Rank:    make([]int, n),
	}
	for i := 0; i < n; i++ {
		uf.Parents[i] = -1
	}
	return &uf
}

func abs(x int) int {
	if x < 0 {
		return 0 - x
	}
	return x
}

func (uf *UnionFind) FindRoot(x int) int {
	if uf.Parents[x] == -1 {
		return x
	}
	return uf.FindRoot(uf.Parents[x])
}

func (uf *UnionFind) Union(rootX, rootY int) {
	if uf.Rank[rootX] > uf.Rank[rootY] {
		uf.Parents[rootY] = rootX
	} else if uf.Rank[rootX] < uf.Rank[rootY] {
		uf.Parents[rootX] = rootY
	} else {
		uf.Parents[rootX] = rootY
		uf.Rank[rootY] ++
	}
}

func minimumEffortPath(heights [][]int) int {
	edges := make([][3]int, 0)
	name := 0
	line := len(heights)
	row := len(heights[0])
	// 生成所有边
	for i := 0; i < line; i++ {
		for j := 0; j < row; j++ {
			if i < line - 1 {
				edges = append(edges, [3]int{name, name + row, abs(heights[i][j] - heights[i + 1][j])})
			}
			if j < row - 1 {
				edges = append(edges, [3]int{name, name + 1, abs(heights[i][j] - heights[i][j + 1])})
			}
			name ++
		}
	}
	sort.Slice(edges, func(i, j int) bool { return edges[i][2] < edges[j][2]})
	// unionFind
	uf := initUnionFind(line * row)
	res := 0
	for _, edge := range edges {
		rootX, rootY := uf.FindRoot(edge[0]), uf.FindRoot(edge[1])
		if rootX != rootY {
			uf.Union(rootX, rootY)
		}
		if uf.FindRoot(0) == uf.FindRoot(row * line - 1) {
			res = edge[2]
			return res
		}
	}
	return 0
}

func main() {
	res := minimumEffortPath([][]int{
		{1, 2, 1, 1, 1},
		{1, 2, 1, 2, 1},
		{1, 2, 1, 2, 1},
		{1, 2, 1, 2, 1},
		{1, 1, 1, 2, 1},
	})
	fmt.Println(res)
}