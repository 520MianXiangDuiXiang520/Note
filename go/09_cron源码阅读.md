# Cron 源码阅读

`robfig/cron/v3` 是一个 Golang 的定时任务库，支持 cron 表达式。Cron 的源码真实教科书级别的存在（可能是我菜 ...）,真的把低耦合高内聚体现地淋漓尽致，另外其中涉及的装饰器模式，并发处理等都很值得学习。

<!-- more -->

使用 cron 可以很方便的实现一个定时任务，如下：

```go
go get github.com/robfig/cron/v3@v3.0.0
```

 ```go
package main

import "github.com/robfig/cron/v3"

c := cron.New()
// 添加一个任务，每 30s 执行一次
c.AddFunc("30 * * * *", func() { fmt.Println("Every hour on the half hour") })
// 开始执行（每个任务会在自己的 goroutine 中执行）
c.Start()

// 允许往正在执行的 cron 中添加任务
c.AddFunc("@daily", func() { fmt.Println("Every day") })

// 检查上一个和下一个任务执行的时间
inspect(c.Entries())
..
c.Stop()  // 停止调度，但正在运行的作业不会被停止
 ```

通过上面的示例，可以发现， cron 最常用的几个函数：

* `New()`: 实例化一个 cron 对象
* `Cron.AddFunc()`: 向 Cron 对象中添加一个作业，接受两个参数，第一个是 `cron` 表达式，第二个是一个无参无返回值的函数（作业）
* `Cron.Stop()`: 停止调度，Stop 之后不会再有未执行的作业被唤醒，但已经开始执行的作业不会受影响。

关于 cron 表达式可以先看看 [cron表达式的介绍与使用](https://blog.csdn.net/qq_39135287/article/details/95664533?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.control) 这篇文章，一个 cron 表达式是一个由 5 个空格分隔的字符串，每一部分从左到右分别表示 秒，分， 时， 天，月， 星期，每个部分由数字和一些特殊字符表示一个约定的时间项，在  `robfig/cron` 中，每一部分允许的特殊字符如下：


|Field name   | 是否强制 ? | 允许的值         | 允许的特殊字符|
|----------   | ---------- | --------------  | --------------------------|
|Seconds      | Yes        | 0-59            | * / , -|
|Minutes      | Yes        | 0-59            | * / , -|
|Hours        | Yes        | 0-23            | * / , -|
|Day of month | Yes        | 1-31            | * / , - ?|
|Month        | Yes        | 1-12 or JAN-DEC | * / , -|
|Day of week  | Yes        | 0-6 or SUN-SAT  | * / , - ?|


这些特殊字符的含义如下：

* `*`: 匹配该字段所有值，如 `0 0 * 1 1 *`, 第三个字段为 `*` 表示（1 月 1 日）每小时。
* `/`: 表示范围增量，如 `*/12 * * * * *` 表示每 12 秒执行一次
* `,`: 用来分隔同一组中的项目，如 `* * 5,10,15 3,4 * *` 表示每个三月或四月的 5， 10， 15 号（3.05， 3.10， 3.15， 4.05， 4.10，4.15）
* `-`: 表示范围，如 `*/5 * 10-12 * * *` 表示每天十点到十二点每五秒执行一次
* `?`: 同 `*`

cron 表达式虽然简单，但他却能满足定时任务复杂的使用场景，比如每周一到周五早上十点就可以表示为 `0 0 10 * * 1-5`,除此之外，cron 还有几个预定义的时间表：

|Entry                  | Description                                | Equivalent To|
|-----                  | -----------                                | -------------|
|@yearly (or @annually) | Run once a year, midnight, Jan. 1st        | 0 0 1 1 *|
|@monthly               | Run once a month, midnight, first of month | 0 0 1 * *|
|@weekly                | Run once a week, midnight between Sat/Sun  | 0 0 * * 0|
|@daily (or @midnight)  | Run once a day, midnight                   | 0 0 * * *|
|@hourly                | Run once an hour, beginning of hour        | 0 * * * *|


表示每隔多长时间时，你还可以使用预定义的 `@every <duration>` 如每隔十分钟就可以表示为 `@every 10m`

......

## 源码概览

cron 并不是一个很大的库，核心文件与作用如下：

* `chain.go`: 装饰器模式，使用 Chain 可以给一个作业添加多个装饰器，以实现日志记录等功能
* `constantdelay.go`：顾名思义，提供了一个简单的常量延迟，如 每5分钟，最小粒度支持到秒
* `cron.go`：提供核心功能
* `logger.go`： 定义了一个 Logger 接口，使之能插入到结构化日志系统中
* `option.go`：对默认行为的修改相关
* `parser.go`：解析 cron 表达式
* `spec.go`：

### 核心数据结构和接口

#### type Entry truct

`Entry` 是对添加到 Cron 中的作业的封装，每个 Entry 有一个 ID，除此之外，Entry 里保存了这个作业上次运行的时间和下次运行的时间。

```go
type EntryID int

type Entry struct {
	ID EntryID
	Schedule Schedule
	Next time.Time
	Prev time.Time
	WrappedJob Job
	Job Job
}
```

#### type Cron struct

```go
type Cron struct {
    entries   []*Entry          // 保存了所有加入到 Cron 的作业
    chain     Chain
    stop      chan struct{}     // 接收 Stop() 信号的 chan
    add       chan *Entry       // Cron 运行过程中接收 AddJob() 信号的 chan 
    remove    chan EntryID      // 接收移除 Job 信号的 chan
    snapshot  chan chan []Entry // 快照信号
    running   bool              // 标志 Cron 是否在运行中
    logger    Logger
    runningMu sync.Mutex        // Cron 运行前需要抢占该锁，保证并发安全
    location  *time.Location
    parser    ScheduleParser    // cron 表达式的解析器
    nextID    EntryID           // 即将加入的 Job 对应的 Entry 的 ID
    jobWaiter sync.WaitGroup
}
```

#### interface

```go
// Cron 表达式解析器接口，Parse 方法接收一个 Cron 表达式 spec,
// 返回一个解析出的 Schedule 类型对象
type ScheduleParser interface {
	Parse(spec string) (Schedule, error)
}

// Schedule 类型的对象用来表输 Job 的工作周期，它包含一个 Next() 方法，
// 用来返回 Job 下一次执行的时间
type Schedule interface {
	Next(time.Time) time.Time
}

// Job is an interface for submitted cron jobs.
type Job interface {
	Run()
}
```

### 对接口的实现

#### ScheduleParser 的实现

在 `parser.go` 中，我们可以找到对 ScheduleParser 接口的实现 `Parser`：

```go
type Parser struct {
	options ParseOption
}

func (p Parser) Parse(spec string) (Schedule, error) {...}
```

Parser 通过 `NewParser()` 方法创建：

```go
func NewParser(options ParseOption) Parser {
	optionals := 0
	if options&DowOptional > 0 {
		optionals++
	}
	if options&SecondOptional > 0 {
		optionals++
	}
	if optionals > 1 {
		panic("multiple optionals may not be configured")
	}
	return Parser{options}
}
```

除此之外，`parser.go` 中，创建了一个私有的全局变量 `standardParser`：

```go
var standardParser = NewParser(
	Minute | Hour | Dom | Month | Dow | Descriptor,
)
```

后续 Cron 所使用的就是这个解析器。

#### Schedule 的实现

Schedule 的实现位于 `spec.go` 中，定义了一个 `SpecSchedule` 结构体，实现了 `Schedule` 接口：

```go
type SpecSchedule struct {
	Second, Minute, Hour, Dom, Month, Dow uint64
	Location *time.Location
}

func (s *SpecSchedule) Next(t time.Time) time.Time {...}
```

#### Job 的实现

Job 其实就是用户传入的一个函数，对其的实现位于 `cron.go` 中：

```go
type FuncJob func()

func (f FuncJob) Run() { f() }
```

### 总结

Cron 中核心数据结构的类图如下：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1613570298647-1613570298614.png)

## New()

`cron.go` 中的 `New()` 方法用来创建并返回一个 `Corn` 对象指针，其实现如下：

```go
func New(opts ...Option) *Cron {
	c := &Cron{
		entries:   nil,
		chain:     NewChain(),
		add:       make(chan *Entry),
		stop:      make(chan struct{}),
		snapshot:  make(chan chan []Entry),
		remove:    make(chan EntryID),
		running:   false,
		runningMu: sync.Mutex{},
		logger:    DefaultLogger,
		location:  time.Local,
		parser:    standardParser,
	}
	for _, opt := range opts {
		opt(c)
	}
	return c
}
```

这个函数接收一组可变的 Option 类型的参数，该类型实际上是一类函数：

```go
type Option func(*Cron)
```

Corn 内置了一些 Option 类型的函数，都在 `option.go` 中，以 `With` 开头，用来改变 `Cron` 的默认行为，在 `New()` 中创建完 `Cron` 之后，会依次执行这些函数。

另外，注意 `c.parser` 的值是 `standardParser`, 这个变量在上一节介绍过，位于 ``parser.go`` 中，是一个 `Parse` 类型的变量， `Parse` 是对 `SchedleParse` 的一个默认实现。

## AddFunc()

`AddFunc()` 用于向 Corn 中添加一个作业：

```go
func (c *Cron) AddFunc(spec string, cmd func()) (EntryID, error) {
    // 包装
	return c.AddJob(spec, FuncJob(cmd))
}

func (c *Cron) AddJob(spec string, cmd Job) (EntryID, error) {
	schedule, err := c.parser.Parse(spec)
	if err != nil {
		return 0, err
	}
	return c.Schedule(schedule, cmd), nil
}
```

`AddFunc()` 相较于 `AddJob()`  帮用户省去了包装成 `Job` 类型的一步，在 `AddJob()`  中，调用了 `standardParser.Parse()` 将 cron 表达式解释成了 schedule 类型，最终，他们调用了 `Schedule()` 方法：

```go
func (c *Cron) Schedule(schedule Schedule, cmd Job) EntryID {
	c.runningMu.Lock()
	defer c.runningMu.Unlock()
	c.nextID++
	entry := &Entry{
		ID:         c.nextID,
		Schedule:   schedule,
		WrappedJob: c.chain.Then(cmd),
		Job:        cmd,
	}
	if !c.running {
		c.entries = append(c.entries, entry)
	} else {
		c.add <- entry
	}
	return entry.ID
}
```

这个方法负责创建 Entry 结构体，并把它追加到 Cron 的 entries 列表中，如果 Cron 已经处于运行状态，会将这个创建好的 `entry` 发送到 Cron 的 `add` chan 中，在 `run()` 中会处理这种情况。

## Entries() 和 Entry()

这两个方法被用来返回 Cron entries 的一组快照，`Entries()` 返回所有作业的快照，`Entry(id EntryID)` 根据 ID 返回特定作业的快照，其实就是遍历了一遍 `Entries()` 的返回值：

```go
func (c *Cron) Entry(id EntryID) Entry {
	for _, entry := range c.Entries() {
		if id == entry.ID {
			return entry
		}
	}
	return Entry{}
}
```

关键在于 `Entries()` 的实现上：

```go
func (c *Cron) Entries() []Entry {
	c.runningMu.Lock()
	defer c.runningMu.Unlock()
	if c.running {
		replyChan := make(chan []Entry, 1)
		c.snapshot <- replyChan
		return <-replyChan
	}
	return c.entrySnapshot()
}
```

获取快照时，根据 Cron 是否在运行有不同的处理逻辑，为了避免获取快照过程中 Cron 开始运行，需要竞争 `runningMutex`;

如果 Cron 没在运行，直接调用 `entrySnapshot()` 返回快照：

```go
func (c *Cron) entrySnapshot() []Entry {
	var entries = make([]Entry, len(c.entries))
	for i, e := range c.entries {
		entries[i] = *e
	}
	return entries
}
```

这种情况很简单，如果 Cron 已经在运行中了，会向 `c.snapshot` 发送一个信号，在 `cron.run()` 中会处理这个信号：

```go
case replyChan := <-c.snapshot:
    replyChan <- c.entrySnapshot()
    continue
```

这有点向一个钩子，`Entries()` 中创建了一个新的 chan `replyChan`, 并将其发送给了 `c.snapshot`, `run()` 中通过多路复用监听到这个信号后，调用了 `c.entrySnapshot()` ,并将结果发送到了 `replyChan` 中，`Entries()` 阻塞等待结果并返回。

既然最终调用的都是 `c.entrySnapshot()` 为什么要分两种情况呢？后面再说。

## Remove()

`Remove()` 用于删除一个作业，实现逻辑和 `Entries()` 类似：

```go
func (c *Cron) Remove(id EntryID) {
	c.runningMu.Lock()
	defer c.runningMu.Unlock()
	if c.running {
		c.remove <- id
	} else {
		c.removeEntry(id)
	}
}

func (c *Cron) removeEntry(id EntryID) {
	var entries []*Entry
	for _, e := range c.entries {
		if e.ID != id {
			entries = append(entries, e)
		}
	}
	c.entries = entries
}
```

`run()` 中处理 `c.remove` 信号：

```go
case id := <-c.remove:
    timer.Stop()
    now = c.now()
    c.removeEntry(id)
    c.logger.Info("removed", "entry", id)
```

## Stop()

`Stop()` 用来停止 Cron 的运行，但已经在执行中的作业是不会被打断的，也就是从执行 `Stop()` 之后，不会再有新的作业被调度：

```go
func (c *Cron) Stop() context.Context {
	c.runningMu.Lock()
	defer c.runningMu.Unlock()
	if c.running {
		c.stop <- struct{}{}
		c.running = false
	}
	ctx, cancel := context.WithCancel(context.Background())
	go func() {
         // 等待所有已经在执行的作业执行完毕
		c.jobWaiter.Wait()
         // 会发出一个 cancelCtx.Done() 信号
		cancel()
	}()
	return ctx
}
```

大体逻辑和上面的一样，比较巧妙地是 `Stop()` 返回了一个 `Context`, 具体来说是一个 `cancelCtx`, 用户可以监听 `cancelCtx.Done()` 得知什么时候 Cron 真的停止了.



## Start()

`Start()` 用于开始执行 Cron:

```go
func (c *Cron) Start() {
	c.runningMu.Lock()
	defer c.runningMu.Unlock()
	if c.running {
		return
	}
	c.running = true
	go c.run()
}
```

这个函数干了三件事：

1. 获取锁
2. 将 `c.running` 置为 `true` 表示 cron 已经在运行中了
3. 开启一个 goroutine 执行 `c.run()`, `run` 中会一直轮循 `c.entries` 中的 entry, 如果一个 entry 允许执行了，就会开启单独的 goroutine 去执行这个作业

`run`是整个 cron 的一个核心，它负责处理 cron 开始执行后的大部分事情，包括添加作业，删除作业，执行作业等，这是一个近一百行的大函数，其结构如下：

```go
func (c *Cron) run() {
	c.logger.Info("start")

    // 第一部分
	now := c.now()
	for _, entry := range c.entries {
		entry.Next = entry.Schedule.Next(now)
		c.logger.Info("schedule", "now", now, "entry", entry.ID, "next", entry.Next)
	}

    // 第二部分
	for {
        // 2.1
		sort.Sort(byTime(c.entries))

        // 2.2
		var timer *time.Timer
		if len(c.entries) == 0 || c.entries[0].Next.IsZero() {
			timer = time.NewTimer(100000 * time.Hour)
		} else {
			timer = time.NewTimer(c.entries[0].Next.Sub(now))
		}

        // 2.3
		for {
			select {}
			break
		}
	}
}
```

大概包含下面这几部分：

* 第一部分：遍历了 `c.entries` 列表，通过 `schedule.Next()` 计算出这个作业下一次执行的时间，并赋值给了 `entry.Next` 字段。

* 第二部分是一个死循环，这一部分又可以分为三个部分：

  * 2.1：调用了 sort 的快排，其实是对 entries 中的元素按 `Next` 字段的时间线后顺序排序。

  * 2.2：这一部分是对定时器的一个初始化操作：如果没有可以执行的作业，定时器被设置为十万小时后触发（其实就是休眠），否则定时器会在第一个作业允许被执行时触发，定时器触发后， 2.3 部分会去做剩下的事。

  * 2.3：这又是整个 `run` 的核心，其主体是一个死循环（其实它会退出，不算是死循环），这个循环里面的核心又是一个 `select` 多路复用，这个多路复用里监听了五种信号，这五种信号是怎样发出的我们在上面其实已经说过了，他们分别是定时器触发信号 `timer.C`, 运行过程中添加作业的信号 `c.add`,  快照信号 `c.snapshot`, cron 停止的信号 `c.stop`, 移除作业的信号 `c.remove`。

    ```go
    for {
        select {
            case now = <-timer.C:
                // ...
            
            case newEntry := <-c.add:
                // ...
            
            case replyChan := <-c.snapshot:
                // ...
                continue
            
            case <-c.stop:
                // ...
                return
            
            case id := <-c.remove:
               // ...
        }
    
        break
    }
    ```

    下面我们分开看对每一种信号的处理：

### 对 timer.C 的处理

```go
case now = <-timer.C:
    now = now.In(c.location)
    c.logger.Info("wake", "now", now)

    // Run every entry whose next time was less than now
    for _, e := range c.entries {
        if e.Next.After(now) || e.Next.IsZero() {
            break
        }
        c.startJob(e.WrappedJob)
        e.Prev = e.Next
        e.Next = e.Schedule.Next(now)
        c.logger.Info("run", "now", now, "entry", e.ID, "next", e.Next)
    }
```

这个信号被触发有两种情况：

1. 排序后 entries 中第 0 位的作业可以被执行了。
2. 休眠了十万小时后，定时器被触发.....

在处理这类信号时，run 会遍历所有的 entries, 因为这些作业都是按下一次执行时间排过序的，所以如果因为第一种情况出发了信号，说明至少有一个作业是可以执行的，我们遍历整个 entries，直到遇到一个作业可执行时间大于当前时间，说明前面遍历到的都是可以执行的，后面的都是不可以执行的；如果因为第二种情况发出来这个信号，则在第一次判断时就会 break

执行作业调用了 `cron.startJob()` 方法，这个方法会为每个作业开启一个 goroutine 去执行用户函数：

```go
func (c *Cron) startJob(j Job) {
	c.jobWaiter.Add(1)
	go func() {
		defer c.jobWaiter.Done()
		j.Run()
	}()
}
```

这里的操作简单粗暴，直接开 goroutine 去执行，在使用时要注意定时任务一定要能结束，定时任务执行时间过长且执行速率很高时，可能造成 goroutine 泄露，进而可能导致内存溢出。

还有关于 `jobWaiter`，他是为了通知用户程序 Cron 什么时候真的结束了，结合 `Stop()` 可以理解。

### 对 c.add 的处理

```go
case newEntry := <-c.add:
    timer.Stop()
    now = c.now()
    newEntry.Next = newEntry.Schedule.Next(now)
    c.entries = append(c.entries, newEntry)
    c.logger.Info("added", "now", now, "entry", newEntry.ID, "next", newEntry.Next)
```

如果 cron 在运行的过程中有作业被加入，会停止定时器（新加入的作业需要重新进行排序），然后计算新作业的下一次执行时间（cron 未运行时添加作业没有这一步，是因为在 Start 的第一步会集中计算，集中计算结束后，进入第二步的死循环，就不会再次集中计算了），最后把新作业加入到 entries 列表中。

### 对 c.snapshot 的处理

```go
case replyChan := <-c.snapshot:
    replyChan <- c.entrySnapshot()
    continue
```

上面已经说过这个信号，如果 Cron 在运行过程中，用户请求获取作业快照会触发这个信号，之所以不在 `Entries()` 中直接返回，是因为一旦 Cron 被启动，entries 列表中的元素就会被不断排序，而这个操作是在另一个 goroutine 中进行的，这就可能导致直接返回的数据是脏数据。

另外，请注意这个 `continue`, 如果没有 `continue`, 这个 `case` 执行完后，`select` 会退出，接着执行 `break`, 这可能导致与 `c.snapshot` 同时满足的其他事件不被执行；可以说，`select` 外层的那个 `for` 就是未这种情况存在的。

那为什么只有 `c.snapshot` 需要 `continue` 呢？其实这个 `select`  最终的目的是让 `run` 重新阻塞等待下一个事件信号，其他几个不重新阻塞，原因在于他们执行完后需要对 entries 重新排序，而快照不需要，仔细对比 `c.add` 和 `c.snapshot`, 就会恍然大悟。

### 对 c.stop 的处理

```go
case <-c.stop:
    timer.Stop()
    c.logger.Info("stop")
    return
```

这就很简单了，停止定时器，结束 `run` goroutine, 因为作业的执行在自己单独的 goroutine 中，所以 `run()` goroutine 的返回不会影响他们。

### 对 c.remove 的处理

```go
case id := <-c.remove:
    timer.Stop()
    now = c.now()
    c.removeEntry(id)
    c.logger.Info("removed", "entry", id)
```

逻辑和 `c,add` 是一样的。

## Option

开头说过，`New()` 时可以接收一组 `option` 参数，用以改变 Cron 的默认行为，这些参数其实是一些函数，他们会在 Cron 初始化后被依次执行，Cron 内置了一些函数, 他们会返回 `Option` 类型的函数，下面简单了解一些这些函数的作用：

### WithLocation

用于改变时区，默认情况下通过 `time.Local` 获取

```go
func WithLocation(loc *time.Location) Option {
	return func(c *Cron) {
		c.location = loc
	}
}
```

可以这样使用:

```go
c := cron.New(cron.WithLocation(nyc))
```

### WithSeconds

用于覆盖默认的 Cron 解析格式，默认的格式是 `分钟 小时 日 月 星期`，也就是 `Minute | Hour | Dom | Month | Dow`

```go
func WithSeconds() Option {
	return WithParser(NewParser(
		Second | Minute | Hour | Dom | Month | Dow | Descriptor,
	))
}
```

允许的字段如下：

```go
const (
	Second         ParseOption = 1 << iota // Seconds field, default 0
	SecondOptional                         // Optional seconds field, default 0
	Minute                                 // Minutes field, default 0
	Hour                                   // Hours field, default 0
	Dom                                    // Day of month field, default *
	Month                                  // Month field, default *
	Dow                                    // Day of week field, default *
	DowOptional                            // Optional day of week field, default *
	Descriptor                             // Allow descriptors such as @monthly, @weekly, etc.
)
```

### WithParser

如果你觉得 Cron 表达式是在难以理解，也记不住，可以写一个自己的解析器，用这个函数替代原来的解析器。

```go
func WithParser(p ScheduleParser) Option {
	return func(c *Cron) {
		c.parser = p
	}
}
```

### WithChain

修改默认修饰器

```go
func WithChain(wrappers ...JobWrapper) Option {
	return func(c *Cron) {
		c.chain = NewChain(wrappers...)
	}
}
```

### WihLogger

使用自定义的 logger

```go
func WithLogger(logger Logger) Option {
	return func(c *Cron) {
		c.logger = logger
	}
}
```

## Chain

这是一个很值得学习的装饰器模式，我们先看一下默认情况下，装饰器是怎么工作的：

Cron 结构体只有一个 Chain 类型的 `chain` 字段，该字段在执行 `New()` 时会通过 `NewChain()` 初始化：

```go
c := &Cron{
    entries:   nil,
    chain:     NewChain(),
    // ...
}
```

这个 `NewChain()` 接收一组装饰器函数，并且会用这些函数初始化一个 Chain 对象返回:

```go
type Chain struct {
	wrappers []JobWrapper
}

func NewChain(c ...JobWrapper) Chain {
	return Chain{c}
}
```

每个 `Entry` 结构体持有一个 `WrappedJob Job` 属性，在 `Schedule()` 中初始化时，会调用 `chain` 的 `Than()` 方法初始化：

```go
entry := &Entry{
    ID:         c.nextID,
    Schedule:   schedule,
    WrappedJob: c.chain.Then(cmd),
    // ...
}
```

在 `Then()` 中，这些装饰器会被执行：

```go
func (c Chain) Then(j Job) Job {
	for i := range c.wrappers {
		j = c.wrappers[len(c.wrappers)-i-1](j)
	}
	return j
}
```

`Then()` 返回的是执行完装饰器之后的 Job(被装饰后的 Job), 这也解释了为什么在 `run()` 中，传递给 `startJob()` 的是 `e.WrappedJob` 而不是 `e.job`.

了解了装饰器是如何工作的，我们再来看 `chain.go` 中提供的三个内置装饰器

### Recover

类似于内置的 `recover()`，它会捕捉运行过程中的 panic，并使用提供的 logger 记录下来，其实做的事情就是往用户的 Job 里插入了一个 `defer func(){}()`

```go
func Recover(logger Logger) JobWrapper {
	return func(j Job) Job {
		return FuncJob(func() {
			defer func() {
				if r := recover(); r != nil {
					const size = 64 << 10
					buf := make([]byte, size)
					buf = buf[:runtime.Stack(buf, false)]
					err, ok := r.(error)
					if !ok {
						err = fmt.Errorf("%v", r)
					}
					logger.Error(err, "panic", "stack", "...\n"+string(buf))
				}
			}()
			j.Run()
		})
	}
}
```

### DelayIfStillRunning

这个装饰器的作用是保证一个 Job 的前一次执行完，后一次才执行，比如有一个 Job 需要执行 10s, 但执行频率是一秒一次，如果我们想要保证同时只有一个相同的 Job 被执行，就可以使用这个装饰器，在实现上，他是为每个 Job 添加了一个排它锁实现的，Job 执行前获取该锁，退出时释放锁，当一个 Job 等待该锁的时间大于一分钟，会记录在日志中，设计很巧妙。

```go
func DelayIfStillRunning(logger Logger) JobWrapper {
	return func(j Job) Job {
		var mu sync.Mutex
		return FuncJob(func() {
			start := time.Now()
			mu.Lock()
			defer mu.Unlock()
			if dur := time.Since(start); dur > time.Minute {
				logger.Info("delay", "duration", dur)
			}
			j.Run()
		})
	}
}
```

### SkipIfStillRunning

上面那个是等待执行完，这个是如果上一个还在执行，就直接跳过，在实现上，这个装饰器使用了一个容量为 1 的 chan, 在执行 Job 前，会消费 chan 里的数据，执行完后，再往 chan 里填一个数据，通过 select 监听 chan, 如果里面有数据，则执行，否则说明上一个还在执行，只打印一个日志就好了。

```go
func SkipIfStillRunning(logger Logger) JobWrapper {
	return func(j Job) Job {
		var ch = make(chan struct{}, 1)
		ch <- struct{}{}
		return FuncJob(func() {
			select {
			case v := <-ch:
				defer func() { ch <- v }()
				j.Run()
			default:
				logger.Info("skip")
			}
		})
	}
}
```

## 总结

Cron 的几个特点：

1. 允许在允许中添加或删除 Job：通过 chan 发送信号，select 监听，重新排序。
2. 装饰器机制：允许给 Job 添加装饰器，装饰器会在 Entry 初始化时执行。
3. 低耦合：`New()` 时可以传递 `Option`, 以此可以改变一些默认行为，如可以实现自己的 cron 解释器。
4. 每个 Job 使用单独的 goroutine 执行。
5. Stop Cron 不会停止已经开始执行但为执行完的 Job, 可以通过 `Context` 得知什么时候执行完了。