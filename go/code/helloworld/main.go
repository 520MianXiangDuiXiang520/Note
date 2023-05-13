package main

import "fmt"

func setOne(slice []int) {
	slice[0] = 1
}

func appendOne(slice []int) {
	slice = append(slice, 1)
}

func main() {
	s := []int{0}
	setOne(s)
	fmt.Println(s)

	s2 := []int{0}
	appendOne(s)
	fmt.Println(s2)
}
