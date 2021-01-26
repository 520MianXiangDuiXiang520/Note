// 婴儿的名字
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type UnionFind struct {
	Parents map[string]string
	Rank    map[string]int
}

func findRoot(x string, uf *UnionFind) string {
	if uf.Parents[x] == "" {
		return x
	}
	return findRoot(uf.Parents[x], uf)
}

func union(x, y string, uf *UnionFind) {
	minL := len(x)
	if len(y) < minL {
		minL = len(y)
	}

	i := 0
	for ; i < minL; i++ {
		if x[i] < y[i] {
			uf.Parents[y] = x
			return
		} else if x[i] > y[i] {
			uf.Parents[x] = y
			return
		}
	}
	if len(x) > len(y) {
		uf.Parents[x] = y
	} else {
		uf.Parents[y] = x
	}
	
}

func trulyMostPopular(names []string, synonyms []string) []string {
	uf := UnionFind{
		Parents: make(map[string]string),
		Rank:    make(map[string]int),
	}
	for _, synonym := range synonyms {
		sp := strings.Split(string(synonym[1:len(synonym)-1]), ",")
		x, y := sp[0], sp[1]
		rootX := findRoot(x, &uf)
		rootY := findRoot(y, &uf)
		if rootX != rootY {
			union(rootX, rootY, &uf)
		}
	}
	res := make(map[string]int)
	for _, name := range names {
		n, age := strings.Split(name, "(")[0], strings.Split(name, "(")[1]
		ageInt, _ := strconv.Atoi(string(age[:len(age)-1]))
		rootName := findRoot(n, &uf)
		res[rootName] += ageInt
	}
	result := make([]string, len(res))
	index := 0
	for k, v := range res {
		result[index] = fmt.Sprintf("%s(%d)", k, v)
		index++
	}
	return result
}

func main() {
	names := []string{
		"John(15)", "Jon(12)", "Chris(13)", "Kris(4)", "Christopher(19)",
	}
	synonyms := []string{
		"(Jon,John)", "(John,Johnny)", "(Chris,Kris)", "(Chris,Christopher)",
	}
	fmt.Println(trulyMostPopular(names, synonyms))
}
