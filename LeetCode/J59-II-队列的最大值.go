package main

import "fmt"

type MaxQueue struct {
	vals []int
	maxs []int
}


func Constructor() MaxQueue {
	return MaxQueue{
		vals: make([]int, 0),
		maxs: make([]int, 0),
	}
}


func (this *MaxQueue) Max_value() int {
	if len(this.maxs) > 0 {
		return this.maxs[0]
	}
	return -1
}


func (this *MaxQueue) Push_back(value int)  {
	this.vals = append(this.vals, value)
	i := 0
	for ; i < len(this.maxs); i ++ {
		if this.maxs[i] < value {
			this.maxs = this.maxs[:i]
			break
		}
	}
	// if i > 0 {
	// 	this.maxs = this.maxs[i: ]
	// }
	this.maxs = append(this.maxs, value)
}


func (this *MaxQueue) Pop_front() (res int) {
	if len(this.vals) <= 0 {
		return -1
	}
	res = this.vals[0]
	this.vals = this.vals[1:]
	if res == this.maxs[0] {
		this.maxs = this.maxs[1:]
	}
	return
}

func main() {
	obj := Constructor()
	obj.Push_back(1)
	obj.Push_back(72)
	param_1 := obj.Max_value() // 72
	obj.Push_back(90)
	obj.Push_back(7)
	obj.Push_back(70)
	param_2 := obj.Max_value() // 90
	param_3 := obj.Pop_front() // 1
	param_4 := obj.Max_value() // 90
	_ = obj.Pop_front() // 72
	_ = obj.Pop_front() // 90
	param_5 := obj.Max_value() // 70
	obj.Push_back(100)
	param_6 := obj.Max_value() // 100
	param_7 := obj.Pop_front() // 7
	param_8 := obj.Max_value() // 100
	fmt.Printf("%v, %v, %v, %v, %v, %v, %v, %v\n", param_1, param_2, param_3, param_4, param_5, param_6, param_7, param_8)
}
