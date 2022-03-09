package main

func f1(s []int) {
	_ = s[0] // line 5: 需要边界检查
	_ = s[1] // line 6: 需要边界检查
	_ = s[2] // line 7: 需要边界检查
}

func f2(s []int) {
	_ = s[2] // line 11: 需要边界检查
	_ = s[1] // line 12: 边界检查被消除
	_ = s[0] // line 13: 边界检查被消除
}

func f3(s []int, index int) {
	_ = s[index] // line 17: 需要边界检查
	_ = s[index] // line 18: 边界检查被消除
}

func f4(a [5]int) {
	_ = a[4] // line 22: 边界检查被消除
}

func main() {}