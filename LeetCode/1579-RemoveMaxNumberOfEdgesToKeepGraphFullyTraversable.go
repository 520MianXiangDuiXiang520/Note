// 保证图可完全遍历
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
	if uf.Rank[x] > uf.Rank[y] {
		uf.Parents[y] = x
	} else if uf.Rank[x] < uf.Rank[y] {
		uf.Parents[x] = y
	} else {
		uf.Parents[x] = y
		uf.Rank[y] ++
	}
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

func maxNumEdgesToRemove(n int, edges [][]int) int {
	if len(edges) < n - 1 {
		return -1
	}
	AliceUF := initUnionFind(n)
	BobUF := initUnionFind(n)
	res := 0
	// 贪心遍历公共边
	for _, edge := range edges {
		if edge[0] != 3 {
			continue
		}
		rootX, rootY := AliceUF.findRoot(edge[1] - 1), AliceUF.findRoot(edge[2] - 1)
		if rootX == rootY {
			res ++
			continue
		}
		AliceUF.union(rootX, rootY)
		BobUF.union(rootX, rootY)
	}
	// 遍历 Alice 独享边
	for _, edge := range edges {
		if edge[0] != 1 {
			continue
		}
		rootX, rootY := AliceUF.findRoot(edge[1] - 1), AliceUF.findRoot(edge[2] - 1)
		if rootX == rootY {
			res ++
			continue
		}
		AliceUF.union(rootX, rootY)
	}
	// 遍历 Bob 独享边
	for _, edge := range edges {
		if edge[0] != 2 {
			continue
		}
		rootX, rootY := BobUF.findRoot(edge[1] - 1), BobUF.findRoot(edge[2] - 1)
		if rootX == rootY {
			res ++
			continue
		}
		BobUF.union(rootX, rootY)
	}

	// 检查无法完全遍历的情况
	aliceNo, bobNo := 0, 0
	for i := 0; i < n; i++ {
		if AliceUF.Parents[i] == -1 {
			aliceNo ++
		}
		if BobUF.Parents[i] == -1  {
			bobNo ++
		}
	}
	if aliceNo > 1 || bobNo > 1 {
		return -1
	}

	return res
}

func main() {
	// 4 [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]  --  2
	// res := maxNumEdgesToRemove(4, [][]int{
	// 	{3, 1, 2}, {3, 2, 3}, {1, 1, 3}, {1, 2, 4},
	// 	{1, 1, 2}, {2, 3, 4},
	// })

	// 4 [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]  -  0
	// res := maxNumEdgesToRemove(4, [][]int{
	// 	{3, 1, 2}, {3, 2, 3}, {1, 1, 4}, {2, 1, 4},
	// })

	// 4 [[3,2,3],[1,1,2],[2,3,4]]
	res := maxNumEdgesToRemove(4, [][]int{
		{3, 2, 3}, {1, 1, 2}, {2, 3, 4},
	})
	fmt.Println(res)
}