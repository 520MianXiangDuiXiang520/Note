# Select 死锁

今天看到一个有趣的问题：

```go

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
```

关键在于 `recvAndSend` 函数的 `case ch1 <- <-ch2:` 我们希望在一条 case 中从 chan2 中取出数据并放到 chan1 中，但事实上这样会导致死锁，虽然平时谁也不会写出这种神仙代码，但下面这个就很容易被写出来了：

```go
package main
 
import (
    "time"
)
 
func main()  {
    ch := make(chan int, 10)
 
    go func() {
        var i = 1
        for {
            i++
            ch <- i
        }
    }()
 
    for {
        select {
        case x := <- ch:
            println(x)
        case <- time.After(30 * time.Second):
            println(time.Now().Unix())
        }
    }
}
```

我们希望每隔一定时间就打印出一些信息，或者是做一些心跳值类的事，但上面这个函数会导致内存泄漏，并且`After`时间越长泄漏越严重，原因和第一段代码死锁一样，都是 `select` 会对 case 后面的表达式求值，可以在[官方文档](https://golang.org/ref/spec#Select_statements)中找到说明：

> For all the cases in the statement, the channel operands of receive operations and the channel and right-hand-side expressions of send statements are evaluated exactly once, in source order, upon entering the "select" statement. The result is a set of channels to receive from or send to, and the corresponding values to send. Any side effects in that evaluation will occur irrespective of which (if any) communication operation is selected to proceed. Expressions on the left-hand side of a RecvStmt with a short variable declaration or assignment are not yet evaluated.

大意就是在进入 `select` 时，go 会按照源码顺序对接收操作的操作数和channel以及发送操作右侧的表达式进行一次求值。

对于第一个例子, case 后面是一个发送操作：`ch1 <- xxx` 那么就会对发送操作右侧的表达式 `<- ch1` 巧的是这个操作又是一个读 chan 操作，由此导致死锁。可以改写成下面的形式避免求值：

```go
select {
    case v := <- ch2:
        ch1 <- v
    default:
        print("")
}
```

第二段代码 case 执行的是一个接收操作，看 `After` 的源码，就知道这个函数返回了一个只读的 chan:

```go
func After(d Duration) <-chan Time {
	return NewTimer(d).C
}
```

每次执行 for 循环都会创建一个 `Time chan` 而这个 chan 只有等计时结束后才能被销毁，由此，时间越长，泄漏越严重，这种情况可以使用 `Ticker` 实现相同功能。

总之，如果你的 case 后面跟了一个函数或其他奇怪的东西，而不是单纯的变量 send 或 recv, 请留意她是否会被提前求值。
