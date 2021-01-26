# sync.Map

## 不安全的 map

go 中原生的 map 不是并发安全的，多个 goroutine 并发地去操作一个 map 会抛出一个 panic

```go
package main
import "fmt"
func main() {
    m := map[string]int {
        "1": 1, "2": 2,
    }
    // 并发写
    for i := 0; i < 100; i ++ {
        go func(i int) {
            m[fmt.Sprintf("%d", i)] = i
        }(i)
    }
    // 读
    for i := 0; i < 100; i ++ {
        fmt.Println(i, m[fmt.Sprintf("%d", i)])
    }
}

PS E:\test\gol\main> go run .\01.go
fatal error: concurrent map writes
fatal error: concurrent map writes
```

解决的办法是互斥地去读写，如：

```go
type SafeMap struct {
	data map[interface{}]interface{}
	sync.RWMutex
}

func (sm *SafeMap) Set(key interface{}, val interface{}) {
	sm.Lock()
	defer sm.Unlock()
	sm.data[key] = val
}

func (sm *SafeMap) Get(key interface{}) (val interface{}){
	sm.Lock()
	defer sm.Unlock()
	val, ok := sm.data[key]
	if !ok {
		val = ""
	}
	return 
}
```

而另一个常用的办法就是使用 `sync` 包提供的 `Map`.

## sync.Map 概览

`sync.Map` 包的核心是 `Map` 结构体，其向外暴露了四个方法：

```go
// 从 Map 中取出一个 value
func (m *Map) Load(key interface{}) (value interface{}, ok bool)

// 向 Map 中 存入一个 KV 对
func (m *Map) Store(key, value interface{})

// 如果 Map 中存在 key,覆盖并返回 (旧值, true), 否则返回 (新值, false)
func (m *Map) LoadOrStore(key, value interface{}) (actual interface{}, loaded bool)

// 从 Map 中删除一个 KV 对
func (m *Map) Delete(key interface{})

// 对 Map 中的所有 KV 执行 f, 直到 f 返回 false
func (m *Map) Range(f func(key, value interface{}) bool)
```



## 源码分析

### 数据结构和设计思想

通过上面直接对所有读写操作加锁的方式类似于Java中的 `HashTable`, 效率并不高，所以参考 `ConcurrentHashMap`,  orcaman 提出了 [concurrent_map](https://github.com/orcaman/concurrent-map/blob/master/README-zh.md) 

> 通过对内部`map`进行分片，降低锁粒度，从而达到最少的锁等待时间(锁冲突).

但这样只是降低了锁粒度，`sync.Map` 的思路是尽可能使用原子操作而不是锁，因为原子操作直接由硬件支持，在多核 CPU 环境下有更好的拓展性和性能。

如何对 `map` 使用原子操作呢?,之所以出现不安全的现象，是由于多个 goroutine 对同一个公有变量（map）操作引起的，如果我们将这个`map` 存储在 `atomic.Value` 中，读的时候使用 `Load`原子地获取到 `map`, 再返回 `map[key]`不就可以避免读时锁竞争了吗？

```go
type SafeMap struct {
    read atomic.Value
}

type readOnly struct {
    m map[interface{}]interface{}
}

func (m *SafeMap) Load(key interface{}) interface{}{
    read := m.read.Load().(readOnly)
    return read.m[key]
}
```

类似于上面地伪代码，将 `map` 包装成 `readOnly` 后，使用 `Value` 存储，在需要 `Load` 的时候，原子地取出 `readOnly`, 由于 `read` 变量不是公有的，所以在拿出 `readOnly` 后，再从其中查找 `key` 对应的 `value` 就不存在线程安全的问题了。

这样看起来很完美，但问题在于仅仅使用 `Value` 无法安全的存储键值对：

```go
func (m *SafeMap) Store(k, v interface{}) {
    read := m.read.Load().(readOnly)
    read.m[key] = v
    m.read.Store(rea)
}
```

上面三条语句操作的其实是同一个 `map` ，可能出现在 store 之前已经有别人 store 的情况，不对这三条语句加锁可能导致覆盖别人的数据，所以其并不是安全的，要想实现安全存储，必须加锁：

```go
type SafeMap struct {
    mu sync.Mutex
    read atomic.Value
}

func (m *SafeMap) Store(k, v interface{}) {
    m.mu.Lock()
    read := m.read.Load().(readOnly)
    read.m[key] = v
    m.read.Store(rea)
    m.mu.UnLock()
}
```

但这就退化到了最初的情况，每次 `Store` 都需要竞争锁，为了提高`Store` 的效率，`sync.Map` 使用了一个冗余的字段 `dirty`, 如果是往 `Map` 中插入新值，就加锁插入到 `dirty` 中， 如果是要修改已经存在的 key 对应的 value ，就可以直接修改 `read` ，当达到某种条件时，会把 `dirty` 转换为 `read`, 这样设计能够尽可能避免使用 `Mutex`而改用性能和拓展性更好的 原子操作来实现安全并发。

#### Map struct

```go
type Map struct {
    mu sync.Mutex
    read atomic.Value
    dirty map[interface{}]*entry
    misses int
}
```

* `mu`: 用于对 dirty 操作时保障并发安全的锁
* `read`: 与上面伪代码中的 `read` 相同，存储一个只读的量 `readOnly`, 对它的操作是原子的，所以对 `Map` 的操作会优先在 `read` 上尝试。
* `dirty`: 这里存储的是最新的 KV 对，一个新的键值对会被存储在这，等时机成熟，`dirty` 会被转换为 `read`, 然后该字段会被置为空，由于 `dirty` 中的数据总是比 `read` 中的更新，所以在查询修改等操作中，`read` 中如果找不到还需要回到 `dirty` 中找。
* `misses`: 控制什么时候 `dirty` 转换为 `read`, 每次从 `read` 中没找到回到 `dirty` 中查询都会导致 `misses` 自增一，等 `misses > len(dirty)` 时， 就会触发转换。

#### readOnly

```go
type readOnly struct {
    // m 和 dirty 中的 value 是同一块内存
    m       map[interface{}]*entry
    // 如果 dirty 和 read 中的数据不一致时，amended 为 true
    amended bool 
}
```

`readOnly` 同样类似于上面伪代码中的 `readOnly`, `Map.read`中存放的就是它，其中 `m` 便是车存储键值对的地方，由于 `read` 中的数据可能滞后于 `dirty`, 所以需要使用 `amended` 来标识， read 中没有读到且 `amended == true` 时，要回 `dirty` 中查询。

#### entry

```go
type entry struct {
    p unsafe.Pointer // *interface{}
}
```

从上面可以看到，`readOnly` 和 `dirty` 中存储的 Value 都是 `entry` 的指针，这样做的好处在于：

1. `dirty` 和 `readOnly.m` 中同一个 `key` 指向的其实是同一个 `value`, 这样冗余的就只有 key 和 一个指向值的指针了，可以减少空间浪费。
2. 修改值时可以直接修改指针指向，这样对 `read` 和 `dirty` 都能生效

### Load

```go
func (m *Map) Load(key interface{}) (value interface{}, ok bool) {
    read, _ := m.read.Load().(readOnly)
    // 尝试从 read 中获取
    e, ok := read.m[key]
    // 如果 read 中没找到并且 read 和 dirty 不一致，需要从 dirty 中找
    if !ok && read.amended {
        m.mu.Lock()
        // double-checking， 避免在加锁过程中 dirty 被提升为 read
        read, _ = m.read.Load().(readOnly)
        e, ok = read.m[key]
        // 双重检查没有得到，去 dirty 中找
        if !ok && read.amended {
            e, ok = m.dirty[key]
            // 修改 misses，尝试提升 dirty
            m.missLocked()
        }
        m.mu.Unlock()
    }
    if !ok {
        return nil, false
    }
    return e.load()
}
```

`Load` 的逻辑很简单，就是先从 `read` 中找，找不到就去 `dirty` 中找，并执行 `missLocked()` 修改 `misses` 判断是否需要提升 dirty 到 read. 唯一需要注意的是这里的 `double-checking`:

由于可能存在一个 goroutine 在执行完 ` if !ok && read.amended` 但还没有加锁完成时，另一个 goroutine 将 dirty 提升成了 read 的情况，所以在加锁之后还需要再从 read 中检查一遍，这与 Java 安全单例中的双重检查是一样的，双重检查会在 `Map` 中多次使用到。

从 read 或 dirty 中得到 key 对应的 value 后，并不是最终的结果，而是一个指向 entry 的指针，我们需要根据其指向的 entry 中的 `p` 拿到真实的 value：

```go
func (e *entry) load() (value interface{}, ok bool) {
    p := atomic.LoadPointer(&e.p)
    if p == nil || p == expunged {
        return nil, false
    }
    return *(*interface{})(p), true
}
```

`entry.p` 有三种可能的值：

1. nil
2. expunged
3. 其他具体的值

前两种的出现是由于 `Map` 的延时删除策略，到删除时再说，所以在这个，如果 `p` 等于前两种值，就说明 `key` 不存在或已经被删除，所以返回 `nil, false`

`missLocked` 的逻辑也很简单，每当调用，就将 `misses`自增 1 ，当 `m.misses >= len(m.dirty)` 时，会进行提升，提升的过程也很简单，提升结束后，会对 `dirty` 和 `misses` 初始化。

```go
func (m *Map) missLocked() {
    m.misses++
    if m.misses < len(m.dirty) {
        return
    }
    // 将 dirty 提升为 read
    m.read.Store(readOnly{m: m.dirty})
    // 重置相关字段
    m.dirty = nil
    m.misses = 0
}
```

### Delete

```go
func (m *Map) Delete(key interface{}) {
    read, _ := m.read.Load().(readOnly)
    e, ok := read.m[key]
    if !ok && read.amended {
        m.mu.Lock()
        read, _ = m.read.Load().(readOnly)
        e, ok = read.m[key]
        if !ok && read.amended {
            // read 中没有，从 dirty 中删除
            delete(m.dirty, key)
        }
        m.mu.Unlock()
    }
    if ok {
        e.delete()
    }
}
```

`Delete` 的逻辑类似于 `Load()` ，通过双重检查判断键值对是否在 `read` 中，不在的话直接从 `dirty` 中删除，否则调用 `entry` 的 `delete` 方法从`read` 中删除。

```go
func (e *entry) delete() (hadValue bool) {
    for {
        p := atomic.LoadPointer(&e.p)
        // 不存在或被删除
        if p == nil || p == expunged {
            return false
        }
        // CAS 将 enter.p 指向 nil
        if atomic.CompareAndSwapPointer(&e.p, p, nil) {
            return true
        }
    }
}
```

在 `enter.delete()` 中，并没有真的删除 value， 只是通过 CAS 把 `enter.p` 标记为了 nil，但这时这个键值对并没有被从 `read` 中删除，仅仅是吧它的值指向了 nil, 在之后的 `Store` 操作中，这个键可能还会被复用到，否则，直到下一次 `dirty` 升级这个键值才会被真正删除，这就是延时删除。

### Store

```go
func (m *Map) Store(key, value interface{}) {
    read, _ := m.read.Load().(readOnly)
    // kv 在 read 中能找到，更新 read key 对应的 entry
    if e, ok := read.m[key]; ok && e.tryStore(&value) {
        return
    }
    
    m.mu.Lock()
    read, _ = m.read.Load().(readOnly)
    if e, ok := read.m[key]; ok {
        if e.unexpungeLocked() {
            m.dirty[key] = e
        }
        e.storeLocked(&value)
    } else if e, ok := m.dirty[key]; ok {
        e.storeLocked(&value)
    } else {
        if !read.amended {
            m.dirtyLocked()
            m.read.Store(readOnly{m: read.m, amended: true})
        }
        m.dirty[key] = newEntry(value)
    }
    m.mu.Unlock()
}
```

#### 更新值

更新值对应有两种情况：

1. 键值对在 `read` 中能找到，这时直接通过 `tryStore` 修改 `enter.p` 。

   ```go
       read, _ := m.read.Load().(readOnly)
       // kv 在 read 中能找到，更新 read key 对应的 entry
       if e, ok := read.m[key]; ok && e.tryStore(&value) {
           return
       }
   ```

   ```go
   func (e *entry) tryStore(i *interface{}) bool {
       for {
           p := atomic.LoadPointer(&e.p)
           // 被删除
           if p == expunged {
               return false
           }
           // 比较 e.p 与 p, 相等赋新值，否则自旋比较
           if atomic.CompareAndSwapPointer(&e.p, p, unsafe.Pointer(i)) {
               return true
           }
       }
   }
   ```

   `tryStore` 中使用 CAS 实现轻量级锁实现了并发安全的更新操作。

2. 在 `read` 中找不到，在 `dirty` 中：在持锁状态下通过 `storeLocked` 修改 `dirty` 中 `entry.p`

   ```go
   //  m.mu.Lock()
   else if e, ok := m.dirty[key]; ok {
       e.storeLocked(&value)
   } 
   ```

   ```go
   func (e *entry) storeLocked(i *interface{}) {
       atomic.StorePointer(&e.p, unsafe.Pointer(i))
   }
   ```

#### 插入新值

新值会被直接加锁写入到 `dirty` 中.

```go
else {
    if !read.amended {
        m.dirtyLocked()
        m.read.Store(readOnly{m: read.m, amended: true})
    }
    m.dirty[key] = newEntry(value)
}
```

需要注意的是，如果 `read.amended == false` 时，即 `dirty` 中没有新数据时，会执行 if 块中的那两条语句，这在两种情况下会发生：

1. 第一次往 `Map` 中插入数据时，`amended == false`, `dirty` 是一个空 map , 这时 `dirtyLocked`  会直接返回什么也不做，然后第二条语句会给 `read` 分配一个空 `map`, 并标记 `dirty` 中有新数据。

2. dirty 刚被提升为了 read, 这时 `amended == false`, `dirty == nil`,  `dirtyLocked` 会将 `read` 中没有被删除的字段复制到 `dirty` 中， 当下一次提升 dirty 时，那些被标记的键值对才会被真正删除。

   ```go
   func (m *Map) dirtyLocked() {
       // 对应情况 1
       if m.dirty != nil {
           return
       }
       // 情况 2
       read, _ := m.read.Load().(readOnly)
       m.dirty = make(map[interface{}]*entry, len(read.m))
       for k, e := range read.m {
           // 没有被删除，复制到 dirty 中
           if !e.tryExpungeLocked() {
               m.dirty[k] = e
           }
       }
   }
   ```

   `tryExpungeLocked` 用来判断 `entry` 是否被删除，当 `entry.p == nil` 时，说明这个 value 被标记为删除，这时会把它重新标记为 `expunged` 返回 true， 否则返回 false

   这里的并发安全同样使用 CAS 轻量级锁实现

   ```go
   func (e *entry) tryExpungeLocked() (isExpunged bool) {
       p := atomic.LoadPointer(&e.p)
       for p == nil {
           if atomic.CompareAndSwapPointer(&e.p, nil, expunged) {
               return true
           }
           p = atomic.LoadPointer(&e.p)
       }
       return p == expunged
   }
   ```

####  修改已删除的值

   从上面知道，当对已经存在于 `read` 中的键值对执行删除操作时，而是会把其暂时标记为 `nil`, 等 dirty 升级为 read 后再插入新值时会把 read 中标记为 `nil` 的值标记为 `expunged`, 而其他的值会被重新复制到 dirty 中，当这时插入刚被删除的键后，就会直接把之前标记为 `expunged` 的键的值赋为新值，如：

   ```go
sMap := Map{}

sMap.Store(1, 2)
sMap.Store(2, 3)
sMap.Store(5, 5)
fmt.Println("[*] ", len(sMap.dirty))  // 3
sMap.Load(10)
sMap.Load(10)
sMap.Load(10)   // 到这会执行 dirty 的提升
sMap.Load(10)
fmt.Println("[*] ", len(sMap.dirty))  // 0， 提升后 dirty == nil
sMap.Delete(1)  // 此时 1 在 read 中，删除会将其标记为 nil
sMap.Store(4, 4)  // 触发复制，
sMap.Store(1, 5)  // 不会把 1 当作一个新值插入，而是直接存储在刚删除的 1 的位置
fmt.Println("[*] ", len(sMap.dirty))  // 4， 新值会先存储在 dirty 中，同时会修改 read 中对应的 value
   ```

   > 上面的代码是我将 Map 源码整体复制出来后测试的，Map 中的所有字段都是私有的，直接访问不到

   这种情况对应源码中加锁后的第一次判断：

   ```go
read, _ = m.read.Load().(readOnly)
if e, ok := read.m[key]; ok {
    if e.unexpungeLocked() {
        m.dirty[key] = e
    }
    e.storeLocked(&value)
}
   ```

```go
func (e *entry) unexpungeLocked() (wasExpunged bool) {
    return atomic.CompareAndSwapPointer(&e.p, expunged, nil)
}
```

加锁后就老朋友 double-checking ，然后如果 key 在 read 中时，会调用 `storeLocked()` 将 value 的指针存储在 `e.p` 中，并且当value 被标记为 `expunged`时（通过 `e.unexpungeLocked()`判断），意味着该键值对在之前已经被删除，但由于它还是新加入的，所以必须存放在 `dirty` 中，否则下一次提升 dirty 就会丢失这个值.

这与第一种更新值的不同点在于更新值只会从 read 中更新，不会去操作 dirty， 这是因为在更新值时，dirty 与 read 是一致的，或则 dirty 比 read 更新，这是允许的，但在从 read 中复制值到 dirty 中时，我们不能将已标记的键值对也复制过去，这会导致这些键值无法被删除，所以如果在插入已删除的键值时还和更新值时一样只改 read就会导致 read 比 dirty 新，这是不允许的。

### LoadOrStore

`LoadOrStore()` 的作用是如果 key 存在，就 `Load`, 否则就 `Store`, 其逻辑与 Load 和 Store 基本一致，

```go
func (m *Map) LoadOrStore(key, value interface{}) (actual interface{}, loaded bool) {
    // 命中 read
    read, _ := m.read.Load().(readOnly)
    if e, ok := read.m[key]; ok {
        actual, loaded, ok := e.tryLoadOrStore(value)
        if ok {
            return actual, loaded
        }
    }
  
    // 未命中read 或 `expunged`
    m.mu.Lock()
    // ...
    m.mu.Unlock()
    
    return actual, loaded
}
```

```go
func (e *entry) tryLoadOrStore(i interface{}) (actual interface{}, loaded, ok bool) {
    p := atomic.LoadPointer(&e.p)
    if p == expunged {
        return nil, false, false
    }
    if p != nil {
        return *(*interface{})(p), true, true
    }
    
    // p == nil
    ic := i
    for {
        // 赋新值
        if atomic.CompareAndSwapPointer(&e.p, nil, unsafe.Pointer(&ic)) {
            return i, false, true
        }
        // 已经被别的协程修改，重新判断
        p = atomic.LoadPointer(&e.p)
        if p == expunged {
            return nil, false, false
        }
        if p != nil {
            return *(*interface{})(p), true, true
        }
    }
}
```

如果 key 在 read  中， 会进入 `tryLoadOrStore`：

1. `e.p == expunged` 时， 说明 Key 已经被标记删除，这时为了同时更新 dirty， 会延时到加锁后执行。
2. `e.p != nil` 时， 说明 Key Value 存在， 直接返回 Value
3. `e.p == nil` 时，说明键值对已经被删除，但还没有进行 dirty 的提升，会通过 CAS 赋新值（没有提升，也就不需要像第一种情况一样考虑 dirty），如果 CAS 没有通过，说明已经有其他协程修改了这个键值，再次判断其是 `nil` 或 `expunged`

read 没有命中或 `entry.p == expunged` 时，需要加锁对 dirty 进行操作，流程与 `Store` 完全一样，不再赘述。

```go
func (m *Map) LoadOrStore(key, value interface{}) (actual interface{}, loaded bool) {
    // Avoid locking if it's a clean hit.
    read, _ := m.read.Load().(readOnly)
    if e, ok := read.m[key]; ok {
        actual, loaded, ok := e.tryLoadOrStore(value)
        if ok {
            return actual, loaded
        }
    }
    
    m.mu.Lock()
    read, _ = m.read.Load().(readOnly)
    if e, ok := read.m[key]; ok {
        if e.unexpungeLocked() {
            m.dirty[key] = e
        }
        actual, loaded, _ = e.tryLoadOrStore(value)
    } else if e, ok := m.dirty[key]; ok {
        actual, loaded, _ = e.tryLoadOrStore(value)
        m.missLocked()
    } else {
        if !read.amended {
            // We're adding the first new key to the dirty map.
            // Make sure it is allocated and mark the read-only map as incomplete.
            m.dirtyLocked()
            m.read.Store(readOnly{m: read.m, amended: true})
        }
        m.dirty[key] = newEntry(value)
        actual, loaded = value, false
    }
    m.mu.Unlock()
    
    return actual, loaded
}
```

   

### Range

我们可以使用安全的 `for-range` 对一个原生的 map 进行随机遍历，但 `Map` 使用不了这种简单的方法，好在其提供了 `Map.Range`,可以通过回调的方式随机遍历其中的键值。

`Range` 接受一个回调函数，在调用时，Range 会把当前遍历到的键值对传给这个给回调 `f`, 当 `f` 返回 false 时，遍历结束。

`Range` 的源码很简单，为了保证遍历完整进行，在真正遍历之前，他会通过 `double-checking` 提升 dirty.

```go
func (m *Map) Range(f func(key, value interface{}) bool) {
    read, _ := m.read.Load().(readOnly)
    if read.amended {
        m.mu.Lock()
        read, _ = m.read.Load().(readOnly)
        if read.amended {
            read = readOnly{m: m.dirty}
            m.read.Store(read)
            m.dirty = nil
            m.misses = 0
        }
        m.mu.Unlock()
    }
    
    for k, e := range read.m {
        v, ok := e.load()
        if !ok {
            continue
        }
        if !f(k, v) {
            break
        }
    }
}
```



## 总结

原生的 `map` 并不是并发安全的，在并发环境下使用原生 map 会直接导致一个 panic，为此，Go 官方从 1.7 之后添加了 `sync.Map`,用于支持并发环境下的键值对存取操作。

实现并发安全的两个思路分别是 **原子操作** 和 **加锁**， 原子操作由于是直接面向硬件的一组不可分割的指令，所以效率要比加锁高很多，因此 Map 的基本思路就是尽可能多的使用原子操作，直到迫不得已才去使用锁机制，Map 的做法是将数据冗余存储了两个数据结构中，read 是一个只读的 `sync.Value` 类型的结构，其上存储的数据可以通过 `Value.Load()`和 `Value.Store()` 安全存取，另外，新的数据会被存储在 `dirty` 中， 等实际成熟， dirty 会被升级为 read.所有的读和修改操作都会优先在 `read` 上进行，以此尽量避免使用锁。

Map 的优势主要集中于下面两个场景：

> (1) when the entry for a given key is only ever written once but read many times, as in caches that only grow,
> (2) when multiple goroutines read, write, and overwrite entries for disjoint sets of keys. 

即：

1. 一次写，多次读
2. 多个 goroutine 操作的键不相交时

## 关于源码

源码中的一些核心思想：

1. 空间换时间
2. 缓存思想
3. double-checking
4. 延迟删除

### 关于 dirty 的提升

Map 中维持了一个 int  类型的 `misses` 每当 Map 未命中 read 时，会将该值自增 1， 当该值大于 dirty 的长度后，dirty 就会被提升为 read，提升之后，dirty 和 misses 会被重置，等下一次插入新值时，会将 read 中未删除的数据复制到 dirty 中。

除此之外，执行 `Range` 时，也会先进行一次提升。

### 关于延迟删除

当执行 `Delete` 时，如果 read 没有击中， 就会直接从 dirty 中删除，否则如果键值在 read 中，会先将其 Value 的指针（enter.p）标记为 nil, 等下一次执行复制时，这些被标记为 nil 的键值会被重新标记为 expunged，即 enter.p 有三种可能的值：

1. nil: 表示 键值已经被删除，但这一版的 read 还没有被复制到 dirty 中，所以 dirty 此时为 nil, 遇到要重新插入这个key时，可以直接修改 read，之后进行复制时，这个最新的值会被同步回 dirty。
2. expunged: 表示该键值已经被删除并且经历了复制， dirty 不为 nil， 这时需要同时修改 read 和 dirty， 避免 read 的数据比 dirty 中的数据新，导致下一次提升时丢失新数据。
3. `!= nil`: 表示存储的是具体的 value 的指针。

**被删除的数据直到下一次提升时才会被真正删除**

