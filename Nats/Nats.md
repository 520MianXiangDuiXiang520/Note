# Nats

## 安装

```
# client cli tool
brew install nats-io/nats-tools/nats

# server
brew install nats-server
```

NATS 本质上是一个消息队列，**订阅发布**是他最核心的功能，**主题 （Subject）**就是订阅发布的依据。

Subject 是一个字符串，发布者依据 Subject 发布消息，所有订阅了该 Subject 的消费者都可能消费到这条消息（注意是可能，因为大部分消息是不允许重复消费的，需要时 Nats 可以保证这一点）。

Subject 一般由 ASCII 字符组成，`$` 开头的一般被用于系统保留使用，`.` 保留用于分割 Subject 的层次结构，如 `time.us`, `.` 将 Subject 划分为了多个令牌（Token） `*` 和 `>` 被保留用作通配符, 前者匹配任意一个令牌，后者匹配一个活多个令牌，如发布者发布了以下 Subject 的消息：

```
china.sichaun.mianyang
china.sichuan.chengdu.longquan
```

`china.sichuan.*` 只会匹配到 `china.sichaun.mianyang` 而 `china.sichuan.>` 则会匹配到两个

## 三种基础模式

### Publish-Subscribe

所有订阅了该 Subject 的订阅者都可以收到发布者发布的消息

```sh
# shell 1 订阅
nats sub "china.sichuan.*"

# shell 2 订阅
nats sub "china.sichuan.>"

# shell 3 发布
nats pub "china.sichuan.chengdu.wuhou" "Hello Nats"
```

结果

```sh
# shell 1
[#1] Received on "china.sichuan.wuhou"
Hello Nats

# shell 2
[#1] Received on "china.sichuan.wuhou"
Hello Nats
```


### Request-Reply

类似于负载均衡，发布者在某个 Subject 上发布消息后，所有订阅该消息的消费者中的某一个将会消费该消息，并向发布者回复一条确认消息。

```sh
# shell 1 订阅
nats reply "china.sichuan.*" "OK1"

# shell 2 订阅
nats reply "china.sichuan.>" "OK2"

# shell 3 发布
nats request "china.sichuan.chengdu.wuhou" "Hello Nats"
```

结果

```sh
# shell 1
01:55:04 [#4] Received on subject "china.sichuan.wuhou":

Hello Nats

# shell 2
01:54:22 Listening on "china.sichuan.*" in group "NATS-RPLY-22"

# shell 3
01:55:04 Sending request on "china.sichuan.wuhou"
01:55:04 Received with rtt 425.416µs
OK1
```

多请求几次，会发现消息会被不同的消费者消费

如果发布的消息没有订阅者，将会立刻返回错误：

```
junbao 1:55:04 ~ $ nats request "china2.sichuan.wuhou" "Hello Nats"
02:02:15 Sending request on "china2.sichuan.wuhou"
02:02:15 No responders are available
```

### Queue Groups



## JetStream

## 编程使用

## 参考文档

[Nats Docs](https://docs.nats.io/)