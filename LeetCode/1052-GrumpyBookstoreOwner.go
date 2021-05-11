package main

import "fmt"

func maxSatisfied(customers []int, grumpy []int, X int) int {

	min := 0

	if X >= len(grumpy) {
		for _, v := range customers {
		    min += v
	    }
		return min
	}

	for i, v := range customers {
		if grumpy[i] != 1 {
			min += v
		}
	}

	if X == 0 {
		return min
	}
	left, right := 0, X - 1
	t := min
	for i := 0; i < X; i++ {
		if grumpy[i] == 1 {
			t += customers[i]
		}
	}
	max := min
	if t > max {
		max = t
	}
	left ++
	right ++
	t = max
	for right < len(grumpy) {
		
		if grumpy[right] == 1 {
			t += customers[right]
		}
		if grumpy[left - 1] == 1 {
			t -= customers[left - 1]
		}
		if t > max {
		    max = t
	    }
		fmt.Println(t)
		left ++
	    right ++
	}
	return max
	
}

func main() {
	fmt.Println(maxSatisfied([]int{1,0,1,2,1,1,7,5}, []int{0,1,0,1,0,1,0,1}, 3))
	// fmt.Println(maxSatisfied([]int{3, 2, 5}, []int{0,1,1}, 2))
}