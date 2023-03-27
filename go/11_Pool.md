# sync.Pool

有时，我们需要频繁地创建或销毁一些对象（如网络连接等）这会带来大量地 GC 开销，为此，可以将这些对象在用完后保存到一个 “池” 中，下次需要时就可以从池中直接返回了；sync.Pool 就提供了这样一个功能。

## 使用方法

`sync.Pool` 是定义在 `sync/pool.go` 里的一个结构体，暴露了一个公共字段 `New` 和两个公共方法： `Get()` 和 `Put`;

Get 方法的签名如下：

```go
func (p *Pool) Get() interface{} {}
```

用来从池中获取一个对象，如果池中没有可用对象，会调用 New 创建一个新对象，如果未指定 New 字段，会返回 nil

`Put`方法的签名如下：

```go
func (p *Pool) Put(x interface{}) {}
```

用来将一个用完的对象放到池中。

## 实现原理
