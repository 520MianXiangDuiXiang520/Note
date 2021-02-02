// 相似字符串组
// 并查集

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

// 返回两个字符串是否相似
func isSimilar(a, b string) bool {
	if len(a) != len(b) {
		return false
	}
	if a == b {
		return true
	}
	diff := 0
	diffs := [2][2]byte{}
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			if diff < 2 {
				diffs[diff][0] = a[i]
				diffs[diff][1] = b[i]
			}
			diff++
		}
		if diff > 2 {
			return false
		}
	}
	if diff != 2 {
		return false
	}
	if diffs[0][0] != diffs[1][1] || diffs[0][1] != diffs[1][0] {
		return false
	}
	return true

}

func numSimilarGroups(strs []string) (res int) {
	uf := UnionFind{
		Parents: make([]int, len(strs)),
		Rank:    make([]int, len(strs)),
	}
	for i := 0; i < len(strs); i++ {
		uf.Parents[i] = -1
	}
	for i := 0; i < len(strs); i++ {
		for j := i + 1; j < len(strs); j++ {
			if isSimilar(strs[i], strs[j]) {
				rootX, rootY := uf.findRoot(i), uf.findRoot(j)
				if rootX != rootY {
					uf.union(rootX, rootY)
				}
			}
		}
	}
	for i := 0; i < len(uf.Parents); i++ {
		if uf.Parents[i] == -1 {
			res ++
		}
	}
	// fmt.Println(uf.Parents)
	return res
}

func main() {
	fmt.Println(numSimilarGroups([]string{
		"omv","ovm",
	}))
}
