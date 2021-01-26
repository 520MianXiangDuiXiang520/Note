// 等价多米诺骨牌对的数量
package main

import "fmt"

func numEquivDominoPairs(dominoes [][]int) int {
	dict := [100]int{}
	res := 0
	for _, dom := range dominoes {
		add := dom[0] * 10 + dom[1]
		if dom[0] > dom[1] {
			add = dom[1] * 10 + dom[0]
		}
		res += dict[add]
		dict[add] += 1
	}
	return res
}

func main() {
	res := numEquivDominoPairs([][]int{
		{1, 2}, {2, 1}, {3, 4}, {5, 6},{1, 2},
	})
	fmt.Println(res)
}