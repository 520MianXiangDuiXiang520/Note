package main

import (
	"time"
)

func main() {
	ch := make(chan int, 10)

	go func() {
		var i = 1
		for {
			i++
			ch <- i
		}
	}()

	tick := time.NewTicker(30 * time.Second)
	for {
		select {
		case x := <-ch:
			println(x)
			// case <- time.After(30 * time.Second):
			//     println(time.Now().Unix())
		case <-tick.C:
			println(time.Now().Unix())

		}
	}
}
