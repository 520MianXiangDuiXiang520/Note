package main

import "fmt"

func Snail(long, short string) int {
	if len(short) > len(long) {
		return -1
	}

	for i := 0; i <= len(long) - len(short); i++ {
		j := 0
		for j < len(short) {
			if long[i + j] != short[j] {
				break
			}
			j ++
		}
		if j == len(short){
			return i
		}
	}

	return -1
}

func KMP(long, short string, next []int) int {
	if len(short) > len(long) {
		return -1
	}

	for i := 0; i <= len(long) - len(short);  {
		fmt.Println(i)
		j := 0
		for j < len(short) {
			if long[i + j] != short[j] {
				break
			}
			j ++
		}
		if j == len(short){
			return i
		}
		if j == 0 {
			i ++
		} else {
			i += j - next[j - 1]
		}
		
	}

	return -1
}


func main() {
	fmt.Println("____")
	fmt.Println(Snail("abcde", "abcde"))
	fmt.Println(KMP("abcabcabmabcabx", "abcabx", []int{0, 0, 0, 1, 2, 0}))
}