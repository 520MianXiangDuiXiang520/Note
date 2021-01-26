// 连通网络的操作次数
package main

import "fmt"

type FindUnion struct {
	Parents []int
	Rank    []int
}

func getRoot(n int, fu *FindUnion) int {
	fmt.Println(fu.Parents)
	if fu.Parents[n] == -1 {
		return n
	}
	return getRoot(fu.Parents[n], fu)
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

func makeConnected(n int, connections [][]int) int {
	if len(connections) < n-1 {
		return -1
	}
	findUnion := FindUnion{
		Parents: make([]int, n),
		Rank:    make([]int, n),
	}
	for i := 0; i < n; i++ {
		findUnion.Parents[i] = -1
	}

	for _, connection := range connections {
		rootX := getRoot(connection[0], &findUnion)
		rootY := getRoot(connection[1], &findUnion)
		if rootX != rootY {
			union(rootX, rootY, &findUnion)
		}

	}
	res := 0
	for _, i := range findUnion.Parents {
		if i == -1 {
			res++
		}
	}
	return res - 1
}

func main() {
	n := 8
	connections := [][]int{
		{0, 1}, {2, 3}, {4, 5}, {4, 7},
		{5, 6}, {5, 7}, {6, 7},
	}
	fmt.Println(makeConnected(n, connections))
}
