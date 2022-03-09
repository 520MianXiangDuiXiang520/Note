package main

import "fmt"

func Sum[K comparable, V int64 | float64](m map[K]V) V {
	var sum V
	for k, v := range m {
		sum += v
		fmt.Println(k)
	}
	return sum
}

func Sum2[V int | int64 | float64 | int32 | float32](a, b V) V {
	return a + b
}

func PI[V int | float64]() V {
   var v V
   v = 10.0
   return v
}

func main() {
	fmt.Println(Sum(map[int64]float64{1: 2.3, 2: 3.3}))
	fmt.Println(Sum2[int](1, 2))
	fmt.Println(Sum2(2.7, 3.9))
	fmt.Println(PI())
}
