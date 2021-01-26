// 省份的数量
package main

import "fmt"

type UnionFind struct {
	Parents []int
	Rank    []int
}

func findRoot(x int, uf *UnionFind) int {
	if uf.Parents[x] == -1 {
		return x
	}
	return findRoot(uf.Parents[x], uf)
}

func union(x, y int, uf *UnionFind) {
	if uf.Rank[x] > uf.Rank[y] {
		uf.Parents[y] = x
	} else if uf.Rank[y] > uf.Rank[x] {
		uf.Parents[x] = y
	} else {
		uf.Parents[x] = y
		uf.Rank[y] ++
	}
}

func findCircleNum(isConnected [][]int) (res int) {
	uf := UnionFind {
		Parents: make([]int, len(isConnected[0])),
		Rank:    make([]int, len(isConnected[0])),
	}
	for i := 0; i < len(isConnected[0]); i++ {
		uf.Parents[i] = -1
	}
	for i, connect := range isConnected {
		for j, conn := range connect {
			if i != j && conn == 1 {
				rootX := findRoot(i, &uf)
				rootY := findRoot(j, &uf)
				if rootX != rootY {
					union(rootX, rootY, &uf)
				}
			}
		}
	}
	for i := 0; i < len(uf.Parents); i++ {
		if uf.Parents[i] == -1 {
			res ++
		}
	}
	return
}

func main() {
	fmt.Println(findCircleNum([][]int{
		{1, 0, 0}, {0, 1, 0}, {0, 0, 1},
	}))
}