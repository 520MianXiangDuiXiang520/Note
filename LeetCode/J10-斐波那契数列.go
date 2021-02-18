package main

import "fmt"

func fib(n int) int {
    a, b := 0, 1
    for i := 2; i <= n; i ++ {
        a, b = b, (a + b) % 1000000007
    }
    return b 
}

func main() {
	fmt.Println(fib(90), fib(91))
}