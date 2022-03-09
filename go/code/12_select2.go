package main

import "fmt"

func send(ch chan int) {
	for i := 0; i < 5; i++ {
		ch <- i
	}
}

func recvAndSend(ch1, ch2 chan int) {
	for {
		select {
		case ch1 <- <-ch2:
			fmt.Println("send to ch1")
		default:
			fmt.Println("default")
		}
	}
}

func recv(ch chan int) {
	for {
		select {
		case v := <- ch:
			fmt.Printf("got v: %d \n", v)
		}
	}
}

func main() {
	ch1 := make(chan int, 5)
	ch2 := make(chan int, 5)
	// go send(ch2)
	go recvAndSend(ch1, ch2)
	go recv(ch1)
	for{}
}