package main

import (
	"io"
	"slices"
)

func accountsMerge(accounts [][]string) (ans [][]string) {
	io.ReadWriter
	mailDict := make(map[string]struct{})
	mails := make([]string, 0)
	email2idx := make(map[string]int32)
	id2email := make(map[int32]string)
	id2name := make(map[int32]string)
	idx := int32(0)
	for _, accountList := range accounts {
		for i, account := range accountList {
			if i == 0 {
				continue
			}
			_, ok := mailDict[account]
			if !ok {
				mails = append(mails, account)
				email2idx[account] = idx
				id2email[idx] = account
				id2name[idx] = accountList[0]
				idx++
				mailDict[account] = struct{}{}
			}
		}
	}

	uf := make([]int32, idx)
	for i := int32(0); i < idx; i++ {
		uf[i] = i
	}

	var find func(x int32) int32
	find = func(x int32) int32 {
		if uf[x] == x {
			return x
		}
		return find(uf[x])
	}

	merge := func(x, y int32) {
		if x < y {
			uf[find(y)] = find(x)
		} else {
			uf[find(x)] = find(y)
		}
	}

	for _, accountList := range accounts {
		x1 := email2idx[accountList[1]]
		for _, account := range accountList[2:] {
			x2 := email2idx[account]
			merge(x1, x2)
			//fmt.Println(email2idx[accountList[1]], email2idx[account], x1, x2, uf)
		}
	}

	mm := make(map[int32][]string)

	for idx, p := range uf {
		root := find(p)
		list, ok := mm[root]
		if !ok {
			list = make([]string, 0)
			list = append(list, id2name[int32(idx)])
		}
		list = append(list, id2email[int32(idx)])
		mm[root] = list
	}
	//fmt.Println(mm)
	res := make([][]string, 0)
	for _, strings := range mm {
		slices.Sort(strings[1:])
		res = append(res, strings)
	}
	//fmt.Println(res)
	return res
}

func main() {
	//accountsMerge([][]string{
	//	{"Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"},
	//	{"Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"},
	//	{"Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"},
	//	{"Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"},
	//	{"Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"}})

	accountsMerge([][]string{
		{"David", "David0@m.co", "David1@m.co"},
		{"David", "David3@m.co", "David4@m.co"},
		{"David", "David4@m.co", "David5@m.co"},
		{"David", "David2@m.co", "David3@m.co"},
		{"David", "David1@m.co", "David2@m.co"}})
}

//[["David","David0@m.co","David1@m.co","David2@m.co","David3@m.co","David4@m.co","David5@m.co"]]}
