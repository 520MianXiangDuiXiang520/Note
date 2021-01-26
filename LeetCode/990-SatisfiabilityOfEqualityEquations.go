// 等式方程的可满足性
package main

import "fmt"

type UnionFind struct {
	Parents map[byte]byte
	Rank    map[byte]int
}

func findRoot(x byte, uf *UnionFind) byte {
	if uf.Parents[x] == 0 {
		return x
	}
	return findRoot(uf.Parents[x], uf)
}

func union(x, y byte, uf *UnionFind) {
	if uf.Rank[x] > uf.Rank[y] {
		uf.Parents[y] = x
	} else if uf.Rank[y] > uf.Rank[x] {
		uf.Parents[x] = y
	} else {
		uf.Parents[x] = y
		uf.Rank[y] ++
	}
}

func equationsPossible(equations []string) bool {
	uf := UnionFind{
		Parents: make(map[byte]byte),
		Rank:    make(map[byte]int),
	}
	for _, equation := range equations {
		if equation[0] == equation[3] && equation[1] == '=' {
			continue
		}
		if equation[0] == equation[3] && equation[1] == '!' {
			return false
		}
		if equation[1] == '!' {
			continue
		}
		rootX := findRoot(equation[0], &uf)
		rootY := findRoot(equation[3], &uf)
		if rootX != rootY {
			union(rootX, rootY, &uf)
		}
		
	}
	for _, eq := range equations {
		if eq[1] == '!' {
            rootX := findRoot(eq[0], &uf)
		    rootY := findRoot(eq[3], &uf)
		    if rootX == rootY {
			    return false
		    }
        }
	}
	return true
}

func main() {
	fmt.Println(equationsPossible([]string{
		"a==b","b!=c","c==a",
	}))
}