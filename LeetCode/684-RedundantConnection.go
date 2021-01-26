// 冗余连接
package main

import "fmt"

type FindUnion struct {
	Parents map[int]int
	Rank    map[int]int
}

func findRoot(n int, fu *FindUnion) int {
	if fu.Parents[n] == 0 {
		return n
	}
	return findRoot(fu.Parents[n], fu)
}

func union(x, y int, fu *FindUnion) {
	if fu.Rank[x] > fu.Rank[y] {
		fu.Parents[y] = x
	} else if fu.Rank[x] < fu.Rank[y] {
		fu.Parents[x] = y
	} else {
		fu.Parents[x] = y
		fu.Rank[y]++
	}
}

func findRedundantConnection(edges [][]int) []int {
	fu := FindUnion{
		Parents: make(map[int]int),
		Rank:    make(map[int]int),
	}
	for _, edge := range edges {
		rootX := findRoot(edge[0], &fu)
		rootY := findRoot(edge[1], &fu)
		if rootX != rootY {
			union(rootX, rootY, &fu)
		} else {
			return edge
		}
	}
	return []int{}
}

func main() {
	fmt.Println(findRedundantConnection([][]int{
		{1, 2}, {2, 3}, {3, 4}, {1, 4}, {1, 5},
	}))
}