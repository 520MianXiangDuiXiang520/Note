# Golang Channel

> 1. channel 底层数据结构是什么？
>
> 2. 向 channel 写数据是否会对管道加锁？

`chan` 是 Golang 中内置的数据类型，不像 `Mutex` 等需要引入，他是 first-class 类型，他在 Go 的并发控制中起着相当重要的作用。chan 的思想来自 Tony Hoare 在 1978 年发表的论文 [Communicating Sequential Processes](https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf), 它提出了一种并发的编程语言，用来描述并发系统中的互动模式，在后来的演化过程中，才逐渐形成了 CSP 并发模式。CSP 模式中存在 **Process/Channel** 每个 Process 独立运行，多个 Process 之间通过 Channel 通信。

Go 并发控制的核心思想：Don’t communicate by sharing memory, share memory by communicating. 即不要通过共享内存来通信，而是要通过通信来共享内存，前一句话对应传统利用 锁 等方式控制并发，后者就对应 CSP方式，go 中的 goroutine/chan 分别与 CSP 中的 Process/Channel 对应。

## 基本用法

Go 中，chan 属于基本数据类型，可以像普通数据类型注入 `int64` 那样定义，唯一不同的是每个 `chan` 只能存储特定类型的数据（包括chan 类型），所以在定义或创建 chan 时，需要指定其允许的数据类型.

```go
var cInt chan int
var cChan chan chan
```

chan 的零值为 `nil`, 操作 nil 的 chan 会陷入阻塞，所以在使用中一定要初始化 chan, chan 使用 `make()` 函数初始化，初始化时可以指定 长度（缓冲区长度），如下：

```go
cIntWithBuff := make(chan int, 10)
```

指定了长度（有缓冲区）的 chan 叫做 buffered chan, 初始化时也可以不指定长度，叫做 unBuffered chan, 如下：

```go
cIntWithoutBuff := make(chan int)
```

除了定义缓冲区，我们还可以使用 `<-` 定义 chan readOnly 或 writeOnly, 默认定义的 chan 都是双向的（可读可写）:

```go
readOnlyChan := make(<-chan int, 0)
writeOnlyChan := make(chan<- int, 0)
```

chan 的读写使用 `<-` 操作符，如下：

```go
// 把 1 写入 cInt 这个 chan 中
cInt <- 1

// 从 cInt 这个 chan 中取出一个元素
r, ok := <- cInt
```

从 chan 中取数据时，会返回两个值，第一个就是拿到的值，第二个是 `bool` 类型，表示是否真正拿到了数据，如果返回 `false`, 表示 chan 已经被关闭并且缓冲区中没有足够的数据。

我们可以使用 `close()` 关闭一个 chan, 向已经关闭的 chan 中 send 数据会导致 panic, 但对于 buffered channer 即便他已经被关闭，我们任然可以从其中获取已有的数据（如果有的话），如：

```go
func main() {
    cInt := make(chan int, 1)
    go func() {
        cInt <- 1
    }()
    time.Sleep(1000)
    close(cInt)
    r, ok := <- cInt
    fmt.Println(r, ok)  // 1 true
    r, ok = <- cInt
    fmt.Println(r, ok)  // 0 false
}
```

在这种情况下，第一个返回值在缓冲区空时会返回零值，需要根据第二个返回值判断 chan 中是否还有未消费的数据。

> ### 关于阻塞
>
> 对于一个 buffered channer, 如果一个 goroutine 向**已满的 buffered channer 中发送数据**，该 goroutine 会被阻塞，同理，从一个空的 buffered channer 中获取数据也会造成 goroutine 阻塞。
>
> > 通过 `len()` 函数，可以获得 channel 中存在的未被取走的元素数量
> >
> > 通过 `cap()` 函数，可以获得 channel 的容量。
>
> 而对于一个 Unbuffered Channer, 只有**等读写都准备好之后才不会发生阻塞**， 如：
>
> ```go
> package main
> 
> import (
>  `fmt`
>  `time`
> )
> 
> type data struct {}
> 
> func send(ch chan<- data) {
>  fmt.Println("send begin")
>  ch <- data{}              // 阻塞
>  fmt.Println("send exit")  // 不会被执行
> }
> 
> func main() {
>  ch := make(chan data)
>  go send(ch)
>  time.Sleep(time.Second * 5)
> }
> 
> // send begin
> // 
> // Process finished with exit code 0
> 
> ```
>
> 如上代码，由于定义的 ch 是一个 Unbuffered Channel, 并且我们只给这个 chan 发送了数据而没有做消费的操作，这会导致 18 行开启的这个 goroutine 会被一直阻塞，在开发中，这会导致严重的 **goroutine泄露**， 而这里的解决办法就是把这个 Unbuffered Channel 改为长度为 1 的 Buffered Channel.

### 其他用法

chan 还一般会配合 `for - range` 关键字使用, 如：

```go
for v := range ch { 
    fmt.Println(v)
}

// 清空 channel
for range ch {
}
```

另外一个专门配合 chan 使用的关键字是 `select`, 它的语法和 `switch` 类似，但它的 `case` 必须跟 chan 的收发操作，如：

```go
func main() {
    ch := make(chan data, 1)
    for {
        select {
        case ch <- data{}:
            fmt.Println("send")
        case v := <-ch:
            fmt.Println(v)
        }
    }
}
```

select 的有趣之处在于他会非阻塞地进行 chan 地收发操作，如上面地代码如果修改为下面这样：

```go
func main() {
    ch := make(chan data, 1)
    for {
        select {
        // case ch <- data{}:
        //     fmt.Println("send")
        case v := <-ch:
            fmt.Println(v)
        default:
            fmt.Println("default")
        }
    }
}
```

因为没有人像 ch 中写数据，那么如果以阻塞地方式进行收发，那当前 goroutine 将会被阻塞到第七行，但事实上 select 会直接执行 default 中的内容，所以 select 实现地是一种类似多路复用的方案，它会去同时监听多个 case 是否可以执行， **如果有多个 case 同时可以执行，他会随机挑选一个执行。**

由于 select 主要被用来监听 chan 的状态，如果需要监听的 chan 很多时，显然无法使用硬编码的方式实现，所以 Go 允许我们使用`reflect.Select` 动态监听多个 chan:

Select 函数接受一组 `selectCase`, 他同普通的 select 语句一样，他会阻塞到有 case 可以执行，如果有多个 case 同时满足，他也会随机执行一个，该函数会返回三个值：

```go
func Select(cases []SelectCase) (chosen int, recv Value, recvOK bool) {
    //...
}
```

* 第一个 chosen 是所选的 case 在 SelectCase 列表中的索引
* 如果执行的 case 是接受操作，那么第二个和第三个返回值就表示接收到的值和是否接受到，与普通取值操作一样。

`SelectCase` 是一个结构体，包含下面三个字段：

```go
type SelectCase struct {
	Dir  SelectDir // direction of case
	Chan Value     // channel to use (for send or receive)
	Send Value     // value to send (for send)
}
```

* Dir 表示该 case 的类型，可选以下三个值：

  ```go
  const (
  	_             SelectDir = iota
  	SelectSend              // case Chan <- Send
  	SelectRecv              // case <-Chan:
  	SelectDefault           // default
  )
  ```

  * SelectSend 表示该 case 执行发送操作，类似 `case ch <- data{}:`
  * SelectRecv 表示该 case 执行接受操作， 类似 `case v := <-ch:`
  * SelectDefault 表示一种默认行为，该类型下， Chan  和 Send 字段必须是零值。

* Chan  表示 要操作的那个 channel 的 Value， 如果 Chan 为零值（nil）时，该 case 会被忽略。

* Send 用于 Dir 为 SelectSend 时， 是发送给 chan 的数据，在 SelectRecv 模式下， Send 必须是零值。

一个小栗子：

```go
func main() {
    ch := make(chan data, 1)
    chosen, recv, ok := reflect.Select([]reflect.SelectCase{
        {Dir: reflect.SelectRecv, Chan: reflect.ValueOf(ch)},
        {Dir: reflect.SelectSend, Chan: reflect.ValueOf(ch), Send: reflect.ValueOf(data{})},
    })
    fmt.Println(chosen, recv, ok)
}
```



## 实现方法

### 数据结构

chan 的底层实现可以在 `runtime/chan.go` 中看到，从这我们可以看到 chan 的底层数据结构 `hchan`:

```go
type hchan struct {
	qcount   uint           // total data in the queue
	dataqsiz uint           // size of the circular queue
	buf      unsafe.Pointer // points to an array of dataqsiz elements
	elemsize uint16
	closed   uint32
	elemtype *_type // element type
	sendx    uint   // send index
	recvx    uint   // receive index
	recvq    waitq  // list of recv waiters
	sendq    waitq  // list of send waiters
	lock mutex
}
```

* qcount: chan 中现有多少数据
* dataqsiz：chan 的容量
* buf: 缓冲区, 是一个循环队列，buf 就是该循环队列的指针
* elemsize： chan 中一个元素的大小
* closed：标识 chan 是否被 close
* elemtype: chan 中元素的类型
* sendx: chan 中最后一个接受到的元素的索引，没插入一个元素，该值会加一，加到 dataqsiz 会重新从 0 开始加
* recvx: 同 sendx, 表示下一个可以被接收的元素在环形队列中的索引。
* recvq: 被阻塞的接收者队列
* sendq: 被阻塞的发送者队列
* lock: 互斥锁，用来保护所有的字段

```go
type waitq struct {
	first *sudog
	last  *sudog
}
```

sendq 和 recvq 的类型都是 waitq, 这是一个 sudog 类型的队列，first 和 last 指针分别指向队首和队尾，`sudog` 是队列中的一个节点，它代表了一个 g, 在 GMP 模型中， Golang 使用结构体 `g` 表示一个 goroutine, 但在这里，由于每个 g 和 chan 是多对多的关系，这就意味着每个 goroutine 可能处于多个不同的waitq 中，而一个 chan 也可能在等待多个 g, 所以用 sudog 来表示这个正在等待的 g

### 创建

通过 `make` 函数创建 chan 的行为会最终被转换为使用 `runtime.makechan()` 或 `runtime.makechan64()`, 后者用来处理缓冲区大小大于$2^{32}$的情况，实际是也是调用了 `makechan()`:

```go
func makechan64(t *chantype, size int64) *hchan {
	if int64(int(size)) != size {
		panic(plainError("makechan: size out of range"))
	}
	return makechan(t, int(size))
}
```

```go
const (
	maxAlign  = 8
    // chan对象8字节对齐后的大小
	hchanSize = unsafe.Sizeof(hchan{}) + uintptr(-int(unsafe.Sizeof(hchan{}))&(maxAlign-1))
	debugChan = false
)

func makechan(t *chantype, size int) *hchan {
	elem := t.elem

	// 安全检查，保证 chan 中存的数据类型小于 2^16
	if elem.size >= 1<<16 {
		throw("makechan: invalid channel element type")
	}
    // 判断hchanSize是否关于maxAlign对齐
	if hchanSize%maxAlign != 0 || elem.align > maxAlign {
		throw("makechan: bad alignment")
	}

    // 通过 math.MulUintptr 计算 elem.size * size 即需要的缓冲区大小
    // 如果 overflow == true，说明乘法溢出。
    // 这里判断了申请缓冲区过大的情况
	mem, overflow := math.MulUintptr(elem.size, uintptr(size))
	if overflow || mem > maxAlloc-hchanSize || size < 0 {
		panic(plainError("makechan: size out of range"))
	}

	var c *hchan
	switch {
	case mem == 0:
		// mem == 0，可能是因为 elem.size == 0 或 size == 0, 只分配 hchan 无需分配缓冲区空间 
		c = (*hchan)(mallocgc(hchanSize, nil, true))
		// Race detector uses this location for synchronization.
		c.buf = c.raceaddr()
	case elem.ptrdata == 0:
		// 如果元素不是指针，就会给 hchan 和 buf 分配一块连续的内存空间
		c = (*hchan)(mallocgc(hchanSize+mem, nil, true))
		c.buf = add(unsafe.Pointer(c), hchanSize)
	default:
		// 如果元素中包含指针，会单独给 buf 分配内存
		c = new(hchan)
		c.buf = mallocgc(mem, elem, true)
	}

	c.elemsize = uint16(elem.size)
	c.elemtype = elem
	c.dataqsiz = uint(size)

	return c
}
```

makechan 会分下面三种情况创建 chan:

1. 无需缓冲区：创建 Unbuffered Channel 或 Channel 中的元素大小为 0 时，只会创建 hchan
2. Channel 中的元素不包含指针时，会为 hchan 和 buf 一起申请一块连续的内存。
3. Channel 中的元素包含指针时，会单独为 buf 申请内存，这样是为了减轻 GC 的压力。

### send

用 `ch <- i` 发送数据的操作会最终被转换成 `runtime.chansend1()` 函数，该函数有会调用 `runtime.chansend()`:

```go
func chansend1(c *hchan, elem unsafe.Pointer) {
	chansend(c, elem, true, getcallerpc())
}
```

该函数接收四个参数：

```go
func chansend(c *hchan, ep unsafe.Pointer, block bool, callerpc uintptr) bool {}
```

* c: 要发送到的 chan
* ep: 发送的元素
* block：为 true 时表示阻塞

chansend 总共100 多行，但可以分以下几部分阅读：

第一部分：关于 nil chan 的判断：

```go
if c == nil {
    if !block {
        return false
    }
    gopark(nil, nil, waitReasonChanSendNilChan, traceEvGoStop, 2)
    throw("unreachable")
}
```

对于 chan 为空的情况，会根据 `block` 判断，当 `block == false` 即不需要阻塞时，会直接返回 false, 但通过 chansend1 调用时，block == false, 所以一般情况下，c 为空时会直接抛出错误。

> block == false 的情况出现在 `select` 中：
>
> ```go
> func selectnbsend(c *hchan, elem unsafe.Pointer) (selected bool) {
>     return chansend(c, elem, false, getcallerpc())
> }
> ```

第二部分：

```go
if !block && c.closed == 0 && ((c.dataqsiz == 0 && c.recvq.first == nil) ||
		(c.dataqsiz > 0 && c.qcount == c.dataqsiz)) {
    return false
}
```

这里有三个判断条件，在普通发送数据时，由于 chansend1 传递地 block 始终为 true, 所以事实上通过 `ch<- a` 大方式发送数据时，第一个判断就不满足，当 block == false 时（使用 select 时会出现）才会继续后面的判断：

1. `c.closed == 0`: chan 没有关闭

2. `c.dataqsiz == 0 && c.recvq.first == nil` : buf 容量为0 且没有接收者

3. `c.dataqsiz > 0 && c.qcount == c.dataqsiz`: buf 满时

满足 `1 && (2 || 3)` 时， 就会直接返回 false, 发送失败

第三部分：加锁

```go
lock(&c.lock)
```

第四部分：

```go
// 发送过程中如果 chan 被关闭，会导致 panic
if c.closed != 0 {
    unlock(&c.lock)
    panic(plainError("send on closed channel"))
}

// dequeue() 用来从接收者队列队首返回一个接收者 sudog, 并从队列中删除该 sudog
// 如果接收者队列为空，返回 nil。
// 这是很巧妙的一点，在发送时，如果发现有 goroutine 正在等待着接收，就直接把数据交给
// 这个等待着的接收者，而不用先放到缓冲区再让接收者去取，可以提示一部分性能。
if sg := c.recvq.dequeue(); sg != nil {
    // 绕过写缓冲区，直接给接收者
    send(c, sg, ep, func() { unlock(&c.lock) }, 3)
    return true
}

// 缓冲区中有可用空间，将元素放入缓冲区
if c.qcount < c.dataqsiz {
    // 计算这个元素应该存放在缓冲区的哪
    qp := chanbuf(c, c.sendx)
    // 拷贝元素到缓冲区
    typedmemmove(c.elemtype, qp, ep)
    // 修改 sendx
    c.sendx++
    // 环形队列，由于缓冲区大小是 elemsize 的整数被，所以
    // 如果 sendx 等于队列大小，就置 sendx = 0
    if c.sendx == c.dataqsiz {
        c.sendx = 0
    }
    // chan 中的元素数量加一
    c.qcount++
    unlock(&c.lock)
    return true
}
```

```go
func chanbuf(c *hchan, i uint) unsafe.Pointer {
	return add(c.buf, uintptr(i)*uintptr(c.elemsize))
}
```

第四部分是整个发送的核心，他又以下几个要点：

1. 不管是直接交付给接收者还是放到缓冲区，都是需要加锁的

2. 发送时如果 chan 被关闭会直接引起 panic，所以一般情况下，关闭 chan 都由发送者进行，或者在接收者关闭 chan 时，一定要通知发送者。

3. 发送时，如果有接收者在 recvq 中，就可以直接把数据交给接收者，避免了写入缓冲区再读造成的性能浪费。

4. 关于数据写入缓冲区的流程见下图：

   ![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1608121927230-1608121927224.png)

第五部分：阻塞发送者：

到这说明缓冲区已满或 Unbuffered Channel 接收者未准备好，要把发送者放入 sendq 中：

```go
// 获取当前 g
gp := getg()
// 创建一个新的 sudog (即一个新节点)
mysg := acquireSudog()

// 填充 sudog
mysg.releasetime = 0
if t0 != 0 {
    mysg.releasetime = -1
}
mysg.elem = ep
mysg.waitlink = nil
mysg.g = gp
mysg.isSelect = false
mysg.c = c
gp.waiting = mysg
gp.param = nil
// 插入一个新节点
c.sendq.enqueue(mysg)
// 阻塞当前 goroutine, 直到 chanparkcommit 返回 true
gopark(chanparkcommit, unsafe.Pointer(&c.lock), waitReasonChanSend, traceEvGoBlockSend, 2)
KeepAlive(ep)
```

第六部分：被唤醒

```go
// someone woke us up.
if mysg != gp.waiting {
    throw("G waiting list is corrupted")
}
gp.waiting = nil
gp.activeStackChans = false
if gp.param == nil {
    if c.closed == 0 {
        throw("chansend: spurious wakeup")
    }
    panic(plainError("send on closed channel"))
}
gp.param = nil
if mysg.releasetime > 0 {
    blockevent(mysg.releasetime-t0, 2)
}
mysg.c = nil
// 销毁 sudog
releaseSudog(mysg)
return true
```

### recv

```go
i <- ch
i, ok <- ch
```

这两种从 chan 中接收数据的方式最终会被转换成 `runtime.chanrecv1()` 和 `runtime.chanrecv2()`, 而这两个函数最终调用的则是 `runtime.chanrecv()`：

```go
//go:nosplit
func chanrecv1(c *hchan, elem unsafe.Pointer) {
	chanrecv(c, elem, true)
}

//go:nosplit
func chanrecv2(c *hchan, elem unsafe.Pointer) (received bool) {
	_, received = chanrecv(c, elem, true)
	return
}
```

 chanrecv 的结构和 chansend 大体一样，接收三个参数，作用分别是：

1. c: 要从哪个 chan 接收
2. ep: 将接受到的数据写入 ep, 如果 ep == nil 则丢弃数据。
3. block: 标识是否阻塞，在这里，chanrecv1 和 chanrecv2 传递的都是 true

```go
func chanrecv(c *hchan, ep unsafe.Pointer, block bool) (selected, received bool) {
    ...
}
```

chanrecv 的返回值是两个布尔值：

1. block == false 并且 chan 中没有可用的元素时，返回 `false, flase`
2. 如果 chan 被关闭，则返回 `true, false`, 并且 ep 为 零值。
3. 一切正常时获取值填充 ep 并返回 `true, true`

依然分几个部分来看接收的过程：

第一部分：对 nil chan 的处理：

```go
if c == nil {
    if !block {
        return
    }
    gopark(nil, nil, waitReasonChanReceiveNilChan, traceEvGoStop, 2)
    throw("unreachable")
}
```

 和发送一样，从一个未初始化的 chan 接收数据会使当前 goroutine 陷入阻塞。

第二部分：非阻塞状态下的快速失败

```go
// 接收
if !block && (c.dataqsiz == 0 && c.sendq.first == nil ||
              c.dataqsiz > 0 && atomic.Loaduint(&c.qcount) == 0) &&
atomic.Load(&c.closed) == 0 {
    return
}

// 发送
if !block && c.closed == 0 && ((c.dataqsiz == 0 && c.recvq.first == nil) ||
		(c.dataqsiz > 0 && c.qcount == c.dataqsiz)) {
    return false
}
```

TODO：同样与发送时类似，只有在使用 `select` 时才会满足第一个判断，但后面的判断顺序变了，并且使用了原子操作，不知道为什么

第三部分：加锁

```go
lock(&c.lock)
```

第四部分：

```go
// 如果 chan 已经被关闭并且没有可用的数据时，
// 就会清除 ep 指针中的数据病理科返回
if c.closed != 0 && c.qcount == 0 {
    unlock(&c.lock)
    if ep != nil {
        typedmemclr(c.elemtype, ep)
    }
    return true, false
}
```

这部分代码对应下面的情况：chan 中没有数据并且 chan 已经被关闭：

```go
func main(){
    ch := make(chan int, 1)
    close(ch)
    r, ok := <- ch
    fmt.Println(r, ok)
}

// 0 false
```

第五部分：快速接收

```go
if sg := c.sendq.dequeue(); sg != nil {
    recv(c, sg, ep, func() { unlock(&c.lock) }, 3)
    return true, true
}
```

同发送时的 “直接发送” 机制，在接收时，如果发现 sendq 队列中有阻塞的等待发送的发送者，就会直接取出发送者，并从他那接收数据，避免写入缓冲区。

第六部分：写缓冲区，阻塞 当前 goroutine, 等待被唤醒，销毁 sudog

这些和发送时一样，不再赘述。

### close

关闭 chan 的行为最终会被转换为对 `runtime.closechan()` 的函数调用, 该函数可以分以下四部分去理解：

1. 异常处理
2. 释放所有接收者
3. 释放所有发送者
4. 重新调度被阻塞的 goroutine

第一部分：异常情况处理

```go
// 关闭未初始化的 chan 会导致 panic
if c == nil {
    panic(plainError("close of nil channel"))
}

lock(&c.lock)

// 关闭已关闭的 chan 会导致 panic
if c.closed != 0 {
    unlock(&c.lock)
    panic(plainError("close of closed channel"))
}

// 修改标志位
c.closed = 1
```

第二部分：释放所有接收者

```go
var glist gList

// release all readers
for {
    // 从 recvq 头部获取一个 sudoq
    sg := c.recvq.dequeue()
    if sg == nil {
        break
    }
    if sg.elem != nil {
        typedmemclr(c.elemtype, sg.elem)
        sg.elem = nil
    }
    if sg.releasetime != 0 {
        sg.releasetime = cputicks()
    }
    gp := sg.g
    gp.param = nil
    // 其实是把所有 recvq 中阻塞着的接收者 goroutine 放到 glist 中
    glist.push(gp)
}
```

第三部分：释放所有发送者：

```go
for {
    sg := c.sendq.dequeue()
    if sg == nil {
        break
    }
    sg.elem = nil
    if sg.releasetime != 0 {
        sg.releasetime = cputicks()
    }
    gp := sg.g
    gp.param = nil
    glist.push(gp)
}
```

和上面的逻辑相似，把所有阻塞着的发送者放到 glist 中。

第四部分：解锁后调度所有被阻塞的 goroutine

```go
unlock(&c.lock)

// Ready all Gs now that we've dropped the channel lock.
for !glist.empty() {
    gp := glist.pop()
    gp.schedlink = 0
    goready(gp, 3)
}
```

关于重新调度，可以看下面的例子：

```go
func recv(ch <-chan data) {
    r, ok := <-ch
    fmt.Println(r, ok)
    fmt.Println("recv exit")
}

func main(){
    ch := make(chan data)
    go recv(ch)
    time.Sleep(time.Second)
    close(ch)
    time.Sleep(time.Second)
    fmt.Println("main exit")
}

// {} false
// recv exit
// main exit
```

由于创建了一个 Unbuffered Channel, 且只有接收者，所以 main 中新开的 goroutine 会被阻塞到第二行，直到 ch 被关闭，返回 `{}, false`

## 使用 chan 应注意

chan 并不是并发操作的银弹，使用不当可能导致 **goroutine 泄露** 或 程序崩溃 的严重后果，一般来说导致 goroutine 泄露的主要原因是阻塞，下面总结了可能导致阻塞和 panic 的几个原因：

### 发送阻塞的情况

发送时只有两种情况不会阻塞：

1. 有等待中的接收者：这时会直接把数据交付给接收者
2. 对于 Buffereed Channel, 缓冲区未满时，会将数据放入缓冲区

除此之位，下面三种情况都会造成发送阻塞“

1. **向未初始化的 chan 发送数据**：

   ```go
   if c == nil {
       gopark(nil, nil, waitReasonChanSendNilChan, traceEvGoStop, 2)
       throw("unreachable")
   }
   ```

2. **Unbuffered Channel 接收者未准备好**：对于 Unbuffered Channel, 要想不阻塞，只能走上面第一条路，否则就会阻塞。

3. **Buffered Channel 缓冲区已满。**

### 接收阻塞的情况

通过源码阅读，可以了解到接收不阻塞也只有两种情况，与发送类似：

1. 有阻塞着的发送者，会直接从发送者那拿到数据返回。
2. 对于 Buffered Channel， 如果缓冲区中有数据，就会直接从缓冲区中取出而不用阻塞。

除此之外，如果 chan 被关闭且缓冲区中无数据，也会直接返回。

而接收者阻塞的情况业余发送时类似：

1. **试图从一个为 nil 的 chan 接收数据**
2. **Unbuffered Channel 发送者未准备好**
3. **Buffered Channel 缓冲区空。**

### 引起 panic 的情况

1. chan 中的对象过大导致申请失败：

   ```go
   mem, overflow := math.MulUintptr(elem.size, uintptr(size))
   if overflow || mem > maxAlloc-hchanSize || size < 0 {
       panic(plainError("makechan: size out of range"))
   }
   ```
   
   **避免办法**：对象过大时考虑使用指针
   
2. 试图向一个已经关闭了的 chan 发送数据：

   ```go
   if c.closed != 0 {
       unlock(&c.lock)
       panic(plainError("send on closed channel"))
   }
   ```

   **避免办法**：关闭操作尽量由发送者去做，因为接收者从已关闭的 chan 中接收数据不会导致 Panic, 或者接收者关闭 chan 后一定要通知发送者

3. 试图关闭一个已经关闭的 chan 时：

   ```go
   lock(&c.lock)
   if c.closed != 0 {
       unlock(&c.lock)
       panic(plainError("close of closed channel"))
   }
   ```

4. 试图关闭一个 nil 的 chan

   ```go
   if c == nil {
       panic(plainError("close of nil channel"))
   }
   ```

   **避免办法**：避免创建 nil 的 chan

## 锁

在阅读源码的过程中，我们发现 chan 对 buf 的操作都会加锁，但这个锁和 `sync.Mutex` 的实现并不一样，下面在研究以下这个锁：

chan 中的这个锁的类型是 `mutex` 定义在 `runtime2.go` 中，通过 Find Usages， 发现它被大量用在底层源码中，根据注释，他在无竞争的条件下和自旋锁一样快（只有几条机器指令），但如果发生竞争，他会在内核中休眠。它的结构很简单：

```go
type mutex struct {
	key uintptr
}
```

在不同的实现中，这个 key 是不同的，在基于  `futex` 的实现中， key 是一个 `uint32` 的值， 在基于 `sema` 的实现中，他是 `M* waitm`:

具体实现可以看：[Go运行时中的 Mutex](https://colobu.com/2020/12/06/mutex-in-go-runtime/)

## 总结

对开发者来说， chan 是一种不同于传统共享内存的同步方案，生产者将要同步的数据发送给 chan, 消费者从 chan 中获取到数据，生产者消费者各自独立运行，通过 chan 通信，但就 Buffered Channel 的实现来说，应该还是通过加锁和共享内存的方式（共享了 buf）。

源码中比较重要的点如下：

1. chan 底层数据结构为 hchan。
2. 创建 chan 时， 如果存储的类型不包含指针，buf 的地址空间和 hchan 是连续的，因为不包含指针的话每个元素的大小是固定的。
3. chan 中存储的数据类型有大小限制，如果对象太大或不确定时，建议使用指针
4. 在读写 chan 中的数据时，依然会使用锁。
5. 发送或接收数据有一个快速通道：如果有等待者，就直接将数据与等待者交易。
6. 创建的 Buffered Channel 中的 buf 是一个环形队列，那些来不及接收的数据会被放在这。
7. 发送或接收发生阻塞时，被阻塞的 goroutine 会被加入 sendq 或 recvq 中，这是一个 sudoq 组成的双向链表。
8. 关闭 chan 并不会销毁 buf, 只会调度所有阻塞着的 g, 所以可以从已关闭的 chan 中读数据。

## 参考

1. 鸟窝的【Go 并发编程实战课】
2. [draveness 的 【Go 语言设计与实现】](https://draveness.me/golang/docs/part3-runtime/ch06-concurrency/golang-channel)
3. [【深入浅出golang的chan】](https://blog.csdn.net/weixin_42663840/article/details/81285886)
4. [Journey-C 的 【channel 源码阅读】](https://journey-c.github.io/2020/10/29/channel-read/)

