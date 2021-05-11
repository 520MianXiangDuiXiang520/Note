package main

import (
	"fmt"
)

type Node struct{
	Val int
	Next *Node
}

func getLink(vals []int) *Node {
	root := Node{
		Val: 0,
		Next: nil,
	}
	ptr := &root
	for _, v := range vals {
		ptr.Next = &Node{
			Val: v,
			Next: nil,
		}
		ptr = ptr.Next
	}
	return root.Next
}

func print(root *Node) {
	ptr := root
	for ptr != nil {
		fmt.Print(ptr.Val, " -> ")
		ptr = ptr.Next
	}
}

func re(root *Node) *Node {
	var pre *Node
	this := root
	// pre := root
	for this != nil {
		next := this.Next
		this.Next = pre
		pre = this
		this = next
	}
	return pre
}

func main() {
	root := getLink([]int{1, 2, 3, 4})
	print(re(root))
}