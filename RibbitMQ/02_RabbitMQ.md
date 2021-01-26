# RabbitMQ 的七种工作模式

简单模式，任务队列，发布订阅，路由， Topic,  RPC,  Publisher Confirms

<!-- more -->

官网给出了 RabbitMQ 的七种工作模式，分别是：

1. 简单模式（Hello World）：一个生产者，一个消费者
2. 任务队列（[Work queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)）：多个消费者，每个消费者拿到的消息是唯一的
3. 发布订阅（[Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-python.html)）：多个消费者，同一个消息可以被多个消费者同时拿到
4. 路由（[Routing](https://www.rabbitmq.com/tutorials/tutorial-four-python.html)）
5. [Topics](https://www.rabbitmq.com/tutorials/tutorial-five-python.html)
6. [RPC](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)
7. [Publisher Confirms](https://www.rabbitmq.com/tutorials/tutorial-seven-java.html)

## simplest 

特征：只有一个生产者，一个消费者，生产者产生的消息会经过 `AMQP default` 交换机的转发到指定 queue。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1602590715992-1602590715774.png)

生产者：

```go
q, err := ch.QueueDeclare(
    "hello", false, false, false, false, nil,     
)
failOnError(err, "Failed to declare a queue")

// 向队列中发送数据
err = ch.Publish(
    "",     // exchange, 使用默认的 AMQP default
    q.Name, // routing key, 指定转发到特定队列
    false,  // mandatory
    false,  // immediate
    amqp.Publishing {
        ContentType: "text/plain",
        Body:        []byte(Hello World!),
    })
```

## Work Queues

特征：一个生产者，多个消费者，每个消费者拿到的数据是唯一的。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1602590860586-1602590860571.png)

### 数据分配策略

由于存在多个消费者，但一条消息只能分配给某个唯一的消费者，所以需要制定分配哪个数据应该分配给哪个消费者的策略，有两种：**轮循**和**公平分配**

#### 轮循

轮循即按照数据被写入队列的先后顺序依次分配给每个消费者，这是默认的策略。在这种策略下，队列接受到消息后会立刻把它分配给对应的消费者，所以如果某个消费者在消费过程中突然挂掉，那分配给他的这些消息就会丢失，为了保证消息不被丢失，Rabbit MQ 有消息确认机制。

##### 消息确认

消费者在接受到消息后，需要向 MQ Server 发送一个确认 `ACK`, 只有在接受到 `ACK` 消息后，消息才会被从 Server 中删除，在声明消费者时， 可以传递 `autoAck`, 当 `autoAck = true` 时，消费者在接受到消息后会立刻回复`ACK`(这时可能还没真的消费该消息)，这就会出现上面的消息丢失的情况，为此，对于重要的消息，一般采取手动 ACK 的方式：

```go
msgs, err := ch.Consume(
    q.Name, // queue
    "",     // consumer
    false,   // 禁止自动响应 ack
    false,  false, false, nil,
)

for d := range msgs {
    // do sonething...
    err = d.Ack(false) // 手动 ACK
}

```

`Delivery.Ack()` 接受一个 `bool` 类型的参数 `multiple `, 当 `multiple = true` 时，当前和之前发送给该消费者的消息都会被确认，这可以在某些情况下避免发送大量的 ACK 信息而造成通信效率低下，节约网络带宽。

**Delivery Tags**

同一个 Channel 中存在多条消息和确认，为了将消息和确认一一匹配，在调用 `Basic.Deliver`向消费者推送消息时会在 AMQP 头部添加 8 位的 `Delivery-Type` 字段，其类型为 `int`, 在同一个 Channel 里，它是一个唯一的递增标识，消费者接受到消息后，从头部读取 `Delivery-Type` 字段的值，并在适当的时机携带 `Delivery-Type`调用 `basic.ACK` 向服务端发送确认.

Publish 时的包：

```txt
Advanced Message Queueing Protocol
    Type: Method (1)
    Channel: 1
    Length: 123
    Class: Basic (60)
    Method: Deliver (60)
    Arguments
        Consumer-Tag: ctag-C:\Users\lenovo\AppData\Local\Temp\go-build142183146\b001\exe\seceriver.exe-1
        Delivery-Tag: 1
        .... ...0 = Redelivered: False
        Exchange: test_topic
        Routing-Key: api.article.tag
```

确认包：

```txt
Advanced Message Queueing Protocol
    Type: Method (1)
    Channel: 1
    Length: 13
    Class: Basic (60)
    Method: Ack (80)
    Arguments
        Delivery-Tag: 1
        .... ...0 = Multiple: False
```

如果消费者没有发送确认但已死亡（其通道已关闭，连接已关闭或TCP连接丢失），这些未确认的消息就会重新排队，如果还有其他可用的消费者，这些消息会很快分配给其他可用的消费者。

可能存在这种情况，消息已经被消费，但在回传 Ack 的过程中出现了错误，对于 Server 来说，这个消息没有收到确认，就会被排队重传，这会引发幂等性问题，客户端需要考虑到这种情况，并做好处理重复交付消息的工作。

还需要注意的是使用消息确认机制并不能完全保证消息不被丢失，因为可能存在 Server 宕机的情况，因为消息被存储在 Server 的内存中，一旦 Server 挂掉，这些数据还是会丢失，要持久化 Server 的数据到磁盘需要在声明队列时声明 `durable = true`

```go
    q, err := ch.QueueDeclare(
        "hello", // name
        true,   // 持久化数据
        false, false, false, nil, 
    )
```

> 队列配置在声明队列时已经固定了，所以对已存在的队列修改此配置是不起作用的，如果要使用持久化功能，需要在第一次注册队列时就声明。

哪怕使用了 Ack 和 持久化，还是不能 100% 保证消息不被丢失， 尽管它告诉RabbitMQ将消息保存到磁盘，但是RabbitMQ接受消息但尚未将其保存时，仍有很短的时间。 而且，RabbitMQ不会对每条消息都执行持久化，它可能只是保存到缓存中，而没有真正写入磁盘。 持久性保证并不强，但是对于我们的简单任务队列而言，这已经绰绰有余了。 如果您需要更强有力的保证，则可以使用 [发布者确认](https://www.rabbitmq.com/confirms.html)。

#### 公平分配

这是能者多劳的模式，例如生产者产生下面的这样的消息，数字大小对应处理消息需要的时间，且只有两个消费者时：

```txt
1, 10, 1, 10, 1, 10 ...
```

第一个消费者拿到的永远只是任务量小的消息，第二个消费者拿到的永远是任务量大的任务，这样第一个消费者总是空闲，而第二个消费者的任务会越积压越多，我们可以通过 Qos 避免这种情况。

Qos，全称 Quality of Service（服务质量），用来保证客户端和服务器的缓冲区被尽可能使用（保证缓冲区满），Golang 中， `Channel.Qos` 接受三个参数：

```go
func (ch *Channel) Qos(prefetchCount, prefetchSize int, global bool) error 
```

`prefetchCount` 用来指定在接受到消费者 Ack 之前，Server 能给消费者发送多少**条**消息，`prefetchSize` 用来指定在接受到 Ack 之前， Server 最多能给消费者发送多少 bytes 的数据，`global = true` 时，Qos 设置将适用于该连接（connection）下的所有消费者（现在和未来），反之只适用于该 Channel 下的消费者（现在和未来）。

为了实现公平分配，我们可以指定 Qos `prefetchCount = 1`, 且禁用 `autoAck`,等处理完消息后再手动 Ack，

```go
ch.Qos(1, 0, false)
   
for d := range msgs {
    // do something
    err = d.Ack(false)
    utils.FailOnError(err, "Fail to ack")
}
```

 这样一来在接受到 Ack 之前，Server 一次只能发送一个消息给消费者，如上面的例子，一开始第一个和第二个消费者都处于空闲状态，Server 可以按 `prefetchCount` 为他们分配消息，一秒后，消费者 1 消费完向 Server 发送 Ack, 但消费者 2 由于没有消费完未发生确认，所以按照 Qos 的规定，Server 只能将下一个消息分配给消费者1，这样，消息的分配不再是按序进行，而是看哪个消费者空闲，实现能者多劳。

## Publish/Subscribe

特征： 多个消费者，每条消息会被所有订阅了该队列的消费者消费

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1602591411281-1602591411263.png)

发布订阅模式使用 Fanout Exchange(扇形交换机)，这种交换机会把接受到的消息**广播**给所有与他绑定的队列。

生产者：

```go
// 注册交换机，名称为 logs, 类型为扇形交换机
err = ch.ExchangeDeclare("logs", "fanout", false,
                         false, false, false, nil)
utils.FailOnError(err, "Fail to declare exchange")

// name 指定 "" 以使用匿名队列，每次获得一个随机的 queue
// 匿名队列会自动与 publish 时的 exchange 和 key 绑定，所以在生产者中，
// 如果使用了匿名队列，可以不用绑定
// 指定 exclusive 为 true, 使得 queue 与 消费者断开时可以被自动删除
q, err := ch.QueueDeclare("", false, false, true, false, nil)
utils.FailOnError(err, "Fail to declare queue")

msg := "panic: Cannot execute call on objects of non-function type!"
// publish 时指定注册好的 logs exchange
err = ch.Publish("logs", "", false, false, amqp.Publishing{
    ContentType: "text/plain",
    Body:        []byte(msg),
})
```

消费者

```go
// 注册交换机， 类型为扇形
err = ch.ExchangeDeclare(
        "logs", "fanout", false, false, false,false, nil, 
    )
failOnError(err, "Failed to declare an exchange")

// 注册匿名队列
q, err := ch.QueueDeclare(
    "", false, false, true, false, nil,  
)
failOnError(err, "Failed to declare a queue")

// 绑定队列与交换机（订阅 logs 频道）
err = ch.QueueBind(
    q.Name, "", "logs", false, nil,
)
failOnError(err, "Failed to bind a queue")

// 注册消费者
msgs, err := ch.Consume(
    q.Name, "", true, false, false, false, nil, 
)
failOnError(err, "Failed to register a consumer")

go func() {
    for d := range msgs {
        log.Printf(" [x] %s", d.Body)
    }
}()
```

## Routing

特征： 生产者产生的消息经过 `direct` 交换机转发到特定队列。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1602591549463-1602591549460.png)

Direct Exchange(直连交换机)

* 如果注册了 `direct` 类型的交换机，在 `Publish` 时可以指定参数 `key string` 用来将消息转发到特定的队列，如上图，Exchange X 将 `key = orange` 的消息转发到 Q1， 将 `key = black || key = green` 的消息转发到 Q2, 应为 C1 绑定了 Q1， C2 绑定了 Q2, 那 C1 只能拿到 `key = orange`  的信息， C2 则可以拿到 black 和 green 的消息。

生产者：

```go
// 注册交换机，类型为直连交换机
err = ch.ExchangeDeclare("test_routing", "direct", false,
                         false, false, false, nil)
utils.FailOnError(err, "Fail to declare exchange")

q, err := ch.QueueDeclare("", false, false, true, false, nil)
utils.FailOnError(err, "Fail to declare queue")

args := os.Args
if len(args) < 3{
    panic("miss arg")
}
key := args[1]
msg := "panic: Cannot execute call on objects of non-function type! (" + args[2] + ")"
// 指定让 test_routing  Exchange 转发消息到 key 绑定的队列 
err = ch.Publish("test_routing", key, false, false, amqp.Publishing{
    ContentType: "text/plain",
    Body:        []byte(msg),
})
utils.FailOnError(err, "Fail to publish message")
```

消费者

```go
// 声明一个直连交换机
err = ch.ExchangeDeclare(
    "test_routing", "direct", false, false, false, false, nil,
)
failOnError(err, "Failed to declare an exchange")

// 声明一个匿名队列
q, err := ch.QueueDeclare(
    "", false, false, true, false, nil, 
)
failOnError(err, "Failed to declare a queue")

if len(os.Args) < 2 {
    log.Printf("Usage: %s [info] [warning] [error]", os.Args[0])
    os.Exit(0)
}
for _, s := range os.Args[1:] {
    // 绑定交换机，匿名队列和 route
    err = ch.QueueBind(
        q.Name, s, "test_routing", false, nil
    )
    failOnError(err, "Failed to bind a queue")
}

// 声明消费者
msgs, err := ch.Consume(
    q.Name, "", true, false, false, false, nil,
)
failOnError(err, "Failed to register a consumer")

go func() {
    for d := range msgs {
        log.Printf(" [x] %s", d.Body)
    }
}()
```

## Topic

Topic 模式和 Routing 模式类似，只不过 Topic 模式下，生产者发布消息 `key` 的格式为 `a.b.c` a, b, c 均为单词， 消费者注册绑定 Queue，Key, 和 Exchange 时，Key 可以使用通配符：

1. `.` 匹配一个单词
2. `#` 匹配 0 个或多个单词

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn/img/1602645197011-1602645196987.png)

## RPC

