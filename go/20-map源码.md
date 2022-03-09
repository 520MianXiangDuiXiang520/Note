# Go map 源码分析

map 是 Go 中使用非常频繁的一种数据结构，其本质是 HashMap 几乎所有的现代编程语言中都提供了类似的结构，他们能以 $O(1)$ 的时间复杂度提供对键值对的读写操作，常常被用在数据存储，去重等常见下，同时，比起其他的类型，它们的结构又往往比较复杂，如果不加节制的使用，可能会造成内存或 GC 上的问题。本文将简单介绍 Go map 读写的原理，希望能在未来使用它时提供一定的参考。

<!-- more -->

> 本文基于 Windows 平台下的 1.17.5 版本，其他版本和平台可能有不同的细节，但核心思想应该不会差很多。
>
> ```txt
> E:\桌面文件\笔记\Go\map>go version
> go version go1.17.5 windows/amd64
> ```

## 梦开始的地方

不同于其他第三方库，map 是一个相当底层的数据结构，看它的源码似乎有点无从下手，别急，我们或许可以从编译后的代码看出一些端倪：

```go
package main

func main() {
	src := make(map[int64]int16, 10)
	_ = src
}
```

```txt
E:\桌面文件\笔记\Go\map>go build -gcflags="-l -S" base.go
# command-line-arguments
"".main STEXT size=86 args=0x0 locals=0x50 funcid=0x0
        0x0000 00000 (E:\桌面文件\笔记\Go\map\base.go:3)        TEXT    "".main(SB), ABIInternal, $80-0
        0x0000 00000 (E:\桌面文件\笔记\Go\map\base.go:3)        CMPQ    SP, 16(R14)
        0x0004 00004 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-2
        0x0004 00004 (E:\桌面文件\笔记\Go\map\base.go:3)        JLS     79
        0x0006 00006 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-1
        0x0006 00006 (E:\桌面文件\笔记\Go\map\base.go:3)        SUBQ    $80, SP
        0x000a 00010 (E:\桌面文件\笔记\Go\map\base.go:3)        MOVQ    BP, 72(SP)
        0x000f 00015 (E:\桌面文件\笔记\Go\map\base.go:3)        LEAQ    72(SP), BP
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $0, gclocals·33cdeccccebe80329f1fdbee7f5874cb(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $1, gclocals·26c19b003b4032a46d3e8db29831f3fe(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $2, "".main.stkobj(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+24(SP), CX
        0x0019 00025 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (CX)
        0x001d 00029 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+40(SP), DX
        0x0022 00034 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (DX)
        0x0026 00038 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+56(SP), DX
        0x002b 00043 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (DX)
        0x002f 00047 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    type.map[int64]int16(SB), AX
        0x0036 00054 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVL    $10, BX
        0x003b 00059 (E:\桌面文件\笔记\Go\map\base.go:4)        PCDATA  $1, $0
        0x003b 00059 (E:\桌面文件\笔记\Go\map\base.go:4)        NOP
        0x0040 00064 (E:\桌面文件\笔记\Go\map\base.go:4)        CALL    runtime.makemap(SB)
        0x0045 00069 (E:\桌面文件\笔记\Go\map\base.go:10)       MOVQ    72(SP), BP
        0x004a 00074 (E:\桌面文件\笔记\Go\map\base.go:10)       ADDQ    $80, SP
        0x004e 00078 (E:\桌面文件\笔记\Go\map\base.go:10)       RET
        0x004f 00079 (E:\桌面文件\笔记\Go\map\base.go:10)       NOP
        0x004f 00079 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $1, $-1
        0x004f 00079 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-2
        0x004f 00079 (E:\桌面文件\笔记\Go\map\base.go:3)        CALL    runtime.morestack_noctxt(SB)
        0x0054 00084 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-1
        0x0054 00084 (E:\桌面文件\笔记\Go\map\base.go:3)        JMP     0
        0x0000 49 3b 66 10 76 49 48 83 ec 50 48 89 6c 24 48 48  I;f.vIH..PH.l$HH
        0x0010 8d 6c 24 48 48 8d 4c 24 18 44 0f 11 39 48 8d 54  .l$HH.L$.D..9H.T
        0x0020 24 28 44 0f 11 3a 48 8d 54 24 38 44 0f 11 3a 48  $(D..:H.T$8D..:H
        0x0030 8d 05 00 00 00 00 bb 0a 00 00 00 0f 1f 44 00 00  .............D..
        0x0040 e8 00 00 00 00 48 8b 6c 24 48 48 83 c4 50 c3 e8  .....H.l$HH..P..
        0x0050 00 00 00 00 eb aa                                ......
        rel 50+4 t=15 type.map[int64]int16+0
        rel 65+4 t=7 runtime.makemap+0
        rel 80+4 t=7 runtime.morestack_noctxt+0
// ...
```

可以看到 `make(map)` 最终在运行时调用了 `runtime.makemap()` ，事实上使用字面量初始化 map 同样会调用该函数。

> 你可能注意到了我们在初始化 map 时 len 参数写了 10，因为初始化长度小于 8 的 map 时 go 有一些单独的优化，不会走到 `makemap` 中，但其细节对我们了解 map 的原理并无太大帮助，就不过多追究了。

我们可以在 `runtime/map.go` 中找到这个函数：

```go
func makemap(t *maptype, hint int, h *hmap) *hmap {}
```

这个函数接收三个参数，并返回一个 `hmap` 的指针，`hmap` 其实就是 map 底层最核心的数据结构，它的结构如下：

```go
type hmap struct {
    count     int // map 中键值对的数量，len(map) 返回的就是该值
    flags     uint8
    B         uint8  // 用来表示桶的数量，它是真实桶数量的开方，也就是 map 拥有 2^B 个桶
    noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
    hash0     uint32 // 哈希种子

    buckets    unsafe.Pointer // 一个长度为 2^B 的 bucket 的数组
    oldbuckets unsafe.Pointer // 长度是 buckets 的一半，用在扩容时，其余时间时 nil
    nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)

    extra *mapextra // optional fields
}
```

然后再看三个参数：

* `t *maptype`: 从名字就可以看出来包含创建 map 的一些基本的类型信息
* `hint int`: 所需要桶的个数
* `h *hmap`: 不为空处理和返回的就是它，为空会 `new()` 一个

最后看代码：

```go
func makemap(t *maptype, hint int, h *hmap) *hmap {
	mem, overflow := math.MulUintptr(uintptr(hint), t.bucket.size)
	if overflow || mem > maxAlloc {
		hint = 0
	}

	// initialize Hmap
	if h == nil {
		h = new(hmap)
	}
	h.hash0 = fastrand()

	// Find the size parameter B which will hold the requested # of elements.
	// For hint < 0 overLoadFactor returns false since hint < bucketCnt.
	B := uint8(0)
	for overLoadFactor(hint, B) {
		B++
	}
	h.B = B

	// allocate initial hash table
	// if B == 0, the buckets field is allocated lazily later (in mapassign)
	// If hint is large zeroing this memory could take a while.
	if h.B != 0 {
		var nextOverflow *bmap
		h.buckets, nextOverflow = makeBucketArray(t, h.B, nil)
		if nextOverflow != nil {
			h.extra = new(mapextra)
			h.extra.nextOverflow = nextOverflow
		}
	}

	return h
}
```

代码结构非常清晰：

1. 溢出判断：计算请求分配的桶是否会溢出或超过最大的内存限制（由此看来 map 能存储的数量是有上限的）
2. `new(hmap)`: 对应上面说调用参数时的第三点
3. 哈希种子选取
4. 计算 `B` 就是找到一个最小的 B 使得 $2^B > hint$
5. 构建 bucket 列表，如果存在溢出桶，还需要初始化溢出指针和拓展字段，这里的核心就是 `makeBucketArray()` 通过它，我们就可以基本推断出 map 完整的结构了。

### 渐入佳境——桶

```go
func makeBucketArray(t *maptype, b uint8, dirtyalloc unsafe.Pointer) (buckets unsafe.Pointer, nextOverflow *bmap) {
	base := bucketShift(b)  // 2^B
	nbuckets := base
	// For small b, overflow buckets are unlikely.
	// Avoid the overhead of the calculation.
	if b >= 4 {
		// Add on the estimated number of overflow buckets
		// required to insert the median number of elements
		// used with this value of b.
		nbuckets += bucketShift(b - 4)
		sz := t.bucket.size * nbuckets
		up := roundupsize(sz)
		if up != sz {
			nbuckets = up / t.bucket.size
		}
	}

	if dirtyalloc == nil {
		buckets = newarray(t.bucket, int(nbuckets))
	} else {
		// dirtyalloc was previously generated by
		// the above newarray(t.bucket, int(nbuckets))
		// but may not be empty.
		buckets = dirtyalloc
		size := t.bucket.size * nbuckets
		if t.bucket.ptrdata != 0 {
			memclrHasPointers(buckets, size)
		} else {
			memclrNoHeapPointers(buckets, size)
		}
	}

	if base != nbuckets {
		// We preallocated some overflow buckets.
		// To keep the overhead of tracking these overflow buckets to a minimum,
		// we use the convention that if a preallocated overflow bucket's overflow
		// pointer is nil, then there are more available by bumping the pointer.
		// We need a safe non-nil pointer for the last overflow bucket; just use buckets.
		nextOverflow = (*bmap)(add(buckets, base*uintptr(t.bucketsize)))
		last := (*bmap)(add(buckets, (nbuckets-1)*uintptr(t.bucketsize)))
		last.setoverflow(t, (*bmap)(buckets))
	}
	return buckets, nextOverflow
}
```

这个的结构也很清晰，可以分成三部分：

1. 额外分配溢出桶：`base` 算出来是真实桶的个数 $2^B$ ,  `nbuckets` 是最终真正会被分配的桶的个数；如果要分配的桶数大于 $2^4$ 时，就会额外多分配 $2^{b - 4}$ 个桶，这些多分配出来的桶其实就是溢出桶，它是为处理哈希冲突而存在的。可以看出 go 认为当桶数大于 $2^4$ 时溢出就是普遍存在的了，因此会提前分配一些空间来保存可能冲突的键值对。
2. `dirtyalloc` 暂且不讨论，因为新建 map 时这个字段一定是 nil, 这时就会调用 `newarray()` 分配桶的内存空间，注意请求内存的长度是 `nbuckets` 也就是正常桶加上溢出桶的长度，由此可以看出 go 中正常桶和溢出桶是 **内存连续** 的，这能保证即使冲突发生了，读效率也不会因为内存随机读下降很厉害。
3. 如果分配了溢出桶，就需要设置 `Overflow` 的指针，就三行代码，第一行找到第一个溢出桶的位置，第二行找到最后一个溢出桶的位置，第三行设置最后一个溢出桶的 `overflow` 指针，也就是说如果预分配的 `overflow` 指针是空的，说明可以通过该指针拿到更多可用的溢出桶。

在最后，我们看到了强制类型转换：`(*bmap)(add(buckets, base*uintptr(t.bucketsize)))` 桶的指针被断言成了 `bmap` 加上上面分配桶时并没有区分正常桶和溢出桶，所以我们就可以确定这两种桶的实际类型就是 `bmap`, 它的结构如下：

```go
const (
	// Maximum number of key/elem pairs a bucket can hold.
	bucketCntBits = 3
	bucketCnt     = 1 << bucketCntBits  // 8
)

// A bucket for a Go map.
type bmap struct {
	// tophash generally contains the top byte of the hash value
	// for each key in this bucket. If tophash[0] < minTopHash,
	// tophash[0] is a bucket evacuation state instead.
	tophash [bucketCnt]uint8
	// Followed by bucketCnt keys and then bucketCnt elems.
	// NOTE: packing all the keys together and then all the elems together makes the
	// code a bit more complicated than alternating key/elem/key/elem/... but it allows
	// us to eliminate padding which would be needed for, e.g., map[int64]int8.
	// Followed by an overflow pointer.
}
```

这里只定义了 `tophash` 字段，但根据注释和后面读写的源码，我们可以还原真实的 `bmap` 如下：

```go
type bmap struct {
    tophash  [bucketCnt]uint8
    keys     [bucketCnt]keyType
    elems    [bucketCnt]elemType
    overflow uint16
}
```

下面三个字段其实都是不存在，源码通过直接操作内存实现了类似上面结构体的效果，可以看到三个需要注意的点：

1. go 中键值对是分开存储的，这样的好处就是可以避免一些内存对齐可能浪费的空间
2. 每个桶中都有一个 8 字节的 `tophash` 字段，它用来存储每个键的哈希值的高 8 位，这样的好处可以在读的时候看到。
3. 每个桶最多保存 `bucketCnt` 也就是 8 个键值对。

> 这里其实有一个有意思的点：每个桶需要 8 字节额外数据去存储 `tophash` ，假设我们有 $n$ 个键值对需要存储，我们就可以算出至少需要 $n / 8 * 8 = n$ 字节的额外空间存储 `tophash` 这些就是使用 map 可能需要考虑的一个问题，如果你的键值对本身很小，如 `map[uint32]uint8` 且数量很多，那要考虑是否可以合并键值对值类的，尽量让这些额外空间的占比小一点。

到此，我们已经能窥见 map 的真实面目了，一个典型的 map 结构如下：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/16452974553921645297454633.png)

好了，剩下的就是 map 如何读写了 

## 写数据

我们还是通过汇编来找到写键值对的入口：

```go
package main

func main() {
	src := make(map[int64]int16, 10)
	src[1] = 2
}
```

```txt
E:\桌面文件\笔记\Go\map>go build -gcflags="-l -S" base.go
# command-line-arguments
"".main STEXT size=111 args=0x0 locals=0x50 funcid=0x0
        0x0000 00000 (E:\桌面文件\笔记\Go\map\base.go:3)        TEXT    "".main(SB), ABIInternal, $80-0
        0x0000 00000 (E:\桌面文件\笔记\Go\map\base.go:3)        CMPQ    SP, 16(R14)
        0x0004 00004 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-2
        0x0004 00004 (E:\桌面文件\笔记\Go\map\base.go:3)        JLS     104
        0x0006 00006 (E:\桌面文件\笔记\Go\map\base.go:3)        PCDATA  $0, $-1
        0x0006 00006 (E:\桌面文件\笔记\Go\map\base.go:3)        SUBQ    $80, SP
        0x000a 00010 (E:\桌面文件\笔记\Go\map\base.go:3)        MOVQ    BP, 72(SP)
        0x000f 00015 (E:\桌面文件\笔记\Go\map\base.go:3)        LEAQ    72(SP), BP
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $0, gclocals·33cdeccccebe80329f1fdbee7f5874cb(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $1, gclocals·26c19b003b4032a46d3e8db29831f3fe(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:3)        FUNCDATA        $2, "".main.stkobj(SB)
        0x0014 00020 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+24(SP), CX
        0x0019 00025 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (CX)
        0x001d 00029 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+40(SP), DX
        0x0022 00034 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (DX)
        0x0026 00038 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    ""..autotmp_1+56(SP), DX
        0x002b 00043 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVUPS  X15, (DX)
        0x002f 00047 (E:\桌面文件\笔记\Go\map\base.go:4)        LEAQ    type.map[int64]int16(SB), AX
        0x0036 00054 (E:\桌面文件\笔记\Go\map\base.go:4)        MOVL    $10, BX
        0x003b 00059 (E:\桌面文件\笔记\Go\map\base.go:4)        PCDATA  $1, $0
        0x003b 00059 (E:\桌面文件\笔记\Go\map\base.go:4)        NOP
        0x0040 00064 (E:\桌面文件\笔记\Go\map\base.go:4)        CALL    runtime.makemap(SB)
        0x0045 00069 (E:\桌面文件\笔记\Go\map\base.go:5)        MOVQ    AX, BX
        0x0048 00072 (E:\桌面文件\笔记\Go\map\base.go:5)        MOVL    $1, CX
        0x004d 00077 (E:\桌面文件\笔记\Go\map\base.go:5)        LEAQ    type.map[int64]int16(SB), AX
        0x0054 00084 (E:\桌面文件\笔记\Go\map\base.go:5)        CALL    runtime.mapassign_fast64(SB)
        0x0059 00089 (E:\桌面文件\笔记\Go\map\base.go:5)        MOVW    $2, (AX)
        0x005e 00094 (E:\桌面文件\笔记\Go\map\base.go:9)        MOVQ    72(SP), BP
        0x0063 00099 (E:\桌面文件\笔记\Go\map\base.go:9)        ADDQ    $80, SP

        
......
```

通过汇编我们可以看到第五行的写操作最终调用了 `runtime.mapassign_fast64` 函数：如果你去看源码，就不难发现，源码中有很多类似命名的函数，如： `mapassign_faststr`, `mapassign_fast32`, `mapassign_fast64ptr`, `mapassign_fast32ptr` 它们实际上是在 go 针对不同的键类型做的单独的优化，如当键类型是 `int64` 时，就会调用 `mapassign_fast64` 类型是 `string` 时，调用的就是 `mapassign_faststr` ，指针也类似会调用对应的 `xxptr` 方法。除此之外，如类型是 `int16` 或 `byte` 等时，会调用 `map.go` 中的 `mapassign` 方法，这里我们着重分析该方法，具体优化最后再看。

我们一段一段来看这个函数：

```go
if h == nil {
    panic(plainError("assignment to entry in nil map"))
}
```

众所周之对 nil 的 map 读写会导致，就是这儿判断

```go
if raceenabled {
    callerpc := getcallerpc()
    pc := funcPC(mapassign)
    racewritepc(unsafe.Pointer(h), callerpc, pc)
    raceReadObjectPC(t.key, key, callerpc, pc)
}
if msanenabled {
    msanread(key, t.key.size)
}
if h.flags&hashWriting != 0 {
    throw("concurrent map writes")
}
hash := t.hasher(key, uintptr(h.hash0))

// Set hashWriting after calling t.hasher, since t.hasher may panic,
// in which case we have not actually done a write.
h.flags ^= hashWriting
```

这一段主要与 data race 有关，并发对 map 进行读写或写写都会导致 panic 进而避免 data race. 这一段就与写保证相关，用 `flags` 字段标记当前 map 有没有正在被写，这里先计算了 key 的哈希值，再去标记 map 在 “写中” 原因是 `hasher` 也产生的 panic 。

```go
if h.buckets == nil {
    h.buckets = newobject(t.bucket) // newarray(t.bucket, 1)
}
```

这是针对例如 `make(map[int]int, 0)` 这样初始化的 map,前面说这样的 map 有单独的优化没有在 `makemap` 中对相关字段复制和初始化，所以在写时，需要保证 buckets 是被分配了内存的。

```go
again:
	bucket := hash & bucketMask(h.B)
	if h.growing() {
		growWork(t, h, bucket)
	}
	b := (*bmap)(add(h.buckets, bucket*uintptr(t.bucketsize)))
	top := tophash(hash)

	var inserti *uint8
	var insertk unsafe.Pointer
	var elem unsafe.Pointer
```

这一段是根据 key 的哈希值定位到具体的 bmap 桶。定位到桶后， go 会先去遍历桶的 8 个 tophase, 这有三种情况：

1. 找到一个 tophase 是空的，说明当前桶有空位子，并且 key 在 map 中并不存在，直接在此存储键即可：

   ```go
   bucketloop:
       for {
           // 1. 遍历 8 个 tophash 找到一个空的位子
           for i := uintptr(0); i < bucketCnt; i++ {
               if b.tophash[i] != top {
                   if isEmpty(b.tophash[i]) && inserti == nil {
                       inserti = &b.tophash[i]
                       // 将用来存储 key 的地方
                       insertk = add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
                       // 将用来存储 value 的地方
                       elem = add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.elemsize))
                   }
                   if b.tophash[i] == emptyRest {
                       break bucketloop
                   }
                   continue
               }
               // ...
           } 
       }
   // ...
   ```

   这里 `isEmpty()` 的实现是：

   ```go
   const (
       emptyRest = 0 
       emptyOne  = 1 
   )
   func isEmpty(x uint8) bool {
   	return x <= emptyOne
   }
   ```

   `emptyRest` 和 `emptyOne` 同样表示该 tophase 对于位置是空的，但前者表示后面或溢出桶中全是空的，`emptyOne` 则有可能是删除等操作导致该位为空，这种情况你还需要遍历后面的位子和溢出桶，保证这个 key 不被存储两次。

   还有 `dataOffset` 这其实就是 tophase 字段的大小(因为源码中 `hmap` 只定义了 `tophase` 字段)，但 go 保证了即使在 32 位机器上该字段的值也是 `hmap` 按 64 位对齐后的大小：

   ```go
   dataOffset = unsafe.Offsetof(struct {
       b bmap
       v int64
   }{}.v)
   ```

   通过 `inserti` 和 `insertk` 的计算方法，我们佐证第一节说到的 `bmap` 的真实结构，`tophase`, `keys`, `values` 紧密排列，至于 `overflow` 会在后面出现。

2. 找到了一个 tophase 与要存储的 key 高 8 位相同，需要取出完整的 key 与要存储的 key 作比较，如果不相等，继续遍历后面的 tophase, 如果相等，说明当前 key 已经存在，只需要更新对应的 value 即可。

   ```go
   bucketloop:
       for {
           // 1. 遍历 8 个 tophash 找到一个空的位子
           for i := uintptr(0); i < bucketCnt; i++ {
               if b.tophash[i] != top {
                   // ...
               }
               // 2. key 的高 8 位相同，算出 key 的值进一步比较
               k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
               if t.indirectkey() {
                   k = *((*unsafe.Pointer)(k))
               }
               if !t.key.equal(key, k) {
                   continue
               }
               // 3. key 已经存在，更新键值对
               if t.needkeyupdate() {
                   typedmemmove(t.key, k, key)
               }
               elem = add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.elemsize))
               goto done
           }
   done:
       // ...
   ```

3. 遍历完了 8 个 tophase 也没找到空位子，说明当前桶已经满了，需要去溢出桶继续重复上面的遍历：

   ```go
   bucketloop:
       for {
           // ...
           // 4. 遍历完正常桶没有找到空位子，沿着 bmap 的 overflow 指针一直遍历溢出桶找空位子
           ovf := b.overflow(t)
           if ovf == nil {
               break
           }
           b = ovf
       }
   ```

   `overflow()` 方法如下，通过 `uintptr(t.bucketsize)-sys.PtrSize` 就可以看出每个 bucket 的最后 64 位或 32 位（取决于机器位数）是一个指针，存储了下一个溢出桶的地址。

   ```
   func (b *bmap) overflow(t *maptype) *bmap {
      return *(**bmap)(add(unsafe.Pointer(b), uintptr(t.bucketsize)-sys.PtrSize))
   }
   ```

   当然，有可能溢出桶也全满了，这时就需要新建一个溢出桶在存储：

   ```go
   bucketloop:
      for{}
      // ...
   	if inserti == nil {
   		// 5. 当前正常桶和溢出桶都满了，要新分配一个溢出桶给 h
   		newb := h.newoverflow(t, b)
   		inserti = &newb.tophash[0]
   		insertk = add(unsafe.Pointer(newb), dataOffset)
   		elem = add(insertk, bucketCnt*uintptr(t.keysize))
   	}
   ```

   还记得创建 map 时会预分配一些溢出桶吗，在 `newoverflow` 时会优先尝试使用这些预分配的溢出桶，`nextOverflow` 指向第一个可用的预分配溢出桶，当预分配的溢出桶全用完后，会将 `nextOverflow` 置为 nil

   ```go
   func (h *hmap) newoverflow(t *maptype, b *bmap) *bmap {
   	var ovf *bmap
   	if h.extra != nil && h.extra.nextOverflow != nil {
   		ovf = h.extra.nextOverflow 
   		if ovf.overflow(t) == nil {
                // 后面还有预分配的，移动 nextoverflow 指针
   			h.extra.nextOverflow = (*bmap)(add(unsafe.Pointer(ovf), uintptr(t.bucketsize)))
   		} else {
                // 前面说过之后最后一个预分配的溢出桶才会设置 overflow 指针
   			ovf.setoverflow(t, nil)
   			h.extra.nextOverflow = nil
   		}
   	} else {
            // 没有预分配的桶，新建一个做溢出桶
   		ovf = (*bmap)(newobject(t.bucket))
   	}
        // 计算溢出桶的数量
   	h.incrnoverflow()
   	if t.bucket.ptrdata == 0 {
   		h.createOverflow()
   		*h.extra.overflow = append(*h.extra.overflow, ovf)
   	}
       // 设置溢出桶
   	b.setoverflow(t, ovf)
   	return ovf
   }
   ```

   ```go
   func (b *bmap) setoverflow(t *maptype, ovf *bmap) {
   	*(**bmap)(add(unsafe.Pointer(b), uintptr(t.bucketsize)-sys.PtrSize)) = ovf
   }
   ```


当找到存储位置后，只需要调用 `typedmemmove` 将 key 放在对应位置，更改 tophase 即可：

```go
typedmemmove(t.key, insertk, key)
*inserti = top
h.count++
```

最后更改 `flag` 标记写完成，返回存储值位置的指针，真正写入值是在编译时做的

```go
done:
	if h.flags&hashWriting == 0 {
		throw("concurrent map writes")
	}
	h.flags &^= hashWriting
	if t.indirectelem() {
		elem = *((*unsafe.Pointer)(elem))
	}
	return elem
```

```plan9
0x004d 00077 (E:\桌面文件\笔记\Go\map\base.go:5)        LEAQ    type.map[int64]int16(SB), AX
0x0054 00084 (E:\桌面文件\笔记\Go\map\base.go:5)        CALL    runtime.mapassign_fast64(SB)
0x0059 00089 (E:\桌面文件\笔记\Go\map\base.go:5)        MOVW    $2, (AX)
```

### 读

还是通过汇编看入口：

```go
package main

func main() {
    m := make(map[int64]struct{}, 10)
    p, ok := m[1]
    _ = p
    _ = ok
    p2 := m[2]
    _ = p2
}
```

```SAS
 0x004a 00074 (E:\桌面文件\项目\MapSize\test\main.go:5)  MOVQ    AX, BX
 0x004d 00077 (E:\桌面文件\项目\MapSize\test\main.go:5)  MOVL    $1, CX
 0x0052 00082 (E:\桌面文件\项目\MapSize\test\main.go:5)  LEAQ    type.map[int64]struct {}(SB), AX
 0x0059 00089 (E:\桌面文件\项目\MapSize\test\main.go:5)  PCDATA  $1, $1
 0x0059 00089 (E:\桌面文件\项目\MapSize\test\main.go:5)  CALL    runtime.mapaccess2_fast64(SB)
 0x005e 00094 (E:\桌面文件\项目\MapSize\test\main.go:8)  LEAQ    type.map[int64]struct {}(SB), AX
 0x0065 00101 (E:\桌面文件\项目\MapSize\test\main.go:8)  MOVQ    "".m+24(SP), BX
 0x006a 00106 (E:\桌面文件\项目\MapSize\test\main.go:8)  MOVL    $2, CX
 0x006f 00111 (E:\桌面文件\项目\MapSize\test\main.go:8)  PCDATA  $1, $0
 0x006f 00111 (E:\桌面文件\项目\MapSize\test\main.go:8)  CALL    runtime.mapaccess1_fast64(SB)
 0x0074 00116 (E:\桌面文件\项目\MapSize\test\main.go:10) MOVQ    80(SP), BP
 0x0079 00121 (E:\桌面文件\项目\MapSize\test\main.go:10) ADDQ    $88, SP
 0x007d 00125 (E:\桌面文件\项目\MapSize\test\main.go:10) RET

```

可以看到，如果是 `p, ok := m[1]` 形式的调用，会调用 `runtime.mapaccess2_fast64(SB)` 方法，如果不需要第二个 `ok bool` 返回值，则会调用 `runtime.mapaccess1_fast64(SB)` 方法，与写的 `mapassign_fast64` 类似，`mapaccess1_fast64` 和 `mapaccess2_fast64` 是专门对 int64 做优化的，更普遍的函数是 `mapaccess1` 和 `mapaccess2`.这两个的实现几乎一致，我们就只看 `mapaccess2`

```go
if h == nil || h.count == 0 {
    if t.hashMightPanic() {
        t.hasher(key, 0) // see issue 23734
    }
    return unsafe.Pointer(&zeroVal[0]), false
}
```

首先是快速失败，这里说明可以对一个未初始化的 map 进行读，它会返回 value 的零值，但写 nil 的 map 却是会 panic 的（见上一节）。

这里还对 key 做了一次哈希，目的是为了保证如果一个 key 不能被哈希，那即使是空 map 也应该抛出 panic 而不是返回零值，见 [#23734](https://github.com/golang/go/issues/23734)

然后是 data race 检查：

```go
if h.flags&hashWriting != 0 {
    throw("concurrent map read and map write")
}
```

接下来就是遍历正常桶和溢出桶，先判断 tophase 是否相同，再看 key 是否相同，与写的逻辑其实差不多：

```go
hash := t.hasher(key, uintptr(h.hash0))
m := bucketMask(h.B) // 多少个正常桶
b := (*bmap)(add(h.buckets, (hash&m)*uintptr(t.bucketsize)))
// 扩容相关...
top := tophash(hash)
bucketloop:
	for ; b != nil; b = b.overflow(t) {
		for i := uintptr(0); i < bucketCnt; i++ {
			if b.tophash[i] != top {
                  // 后面和溢出桶都没啦
				if b.tophash[i] == emptyRest {
					break bucketloop
				}
				continue
			}
             // 取出完整的 key
			k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
			if t.indirectkey() {
				k = *((*unsafe.Pointer)(k))
			}
			if t.key.equal(key, k) {
				e := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.elemsize))
				if t.indirectelem() {
					e = *((*unsafe.Pointer)(e))
				}
				return e, true
			}
		}
	}
	return unsafe.Pointer(&zeroVal[0]), false
```



### 扩容

读写的流程中我们都跳过了扩容的步骤，当 map 中被写如越来越多数据导致正常桶不够用或使用了太多溢出桶导致读效率大幅下降后，go 会考虑通过扩容来改善这些问题，在写数据的 `mapassign` 函数中我们可以窥见扩容条件：

```go
if !h.growing() && (overLoadFactor(h.count+1, h.B) || tooManyOverflowBuckets(h.noverflow, h.B)) {
    hashGrow(t, h)
    goto again // Growing the table invalidates everything, so try again
}

if inserti == nil {
    // ...
```

具体条件是：

1. 当前没有正在扩容
2. 装载因子超过了某个值
3. 使用了过多的溢出桶

```go
const (
    loadFactorNum = 13
    loadFactorDen = 2
)
func overLoadFactor(count int, B uint8) bool {
	return count > bucketCnt && uintptr(count) > loadFactorNum*(bucketShift(B)/loadFactorDen)
}
```

写成数学公式就是：
$$
count > 13  \frac{2^B}{2} = 6.5 \cdot 2^B
$$
我们知道对于 B 最多存储 $8 \cdot 2^B$ 个键值对，上面的 `overLoadFactor` 就是判断如果 80% 的桶已经被装满了，那就需要扩容了。

```go
func tooManyOverflowBuckets(noverflow uint16, B uint8) bool {
	if B > 15 {
		B = 15
	}
	return noverflow >= uint16(1)<<(B&15)
}
```

这里认为溢出桶太多了的依据就是看溢出桶的数量是不是已经接近或超过常规桶数量了。

```go
func hashGrow(t *maptype, h *hmap) {
	bigger := uint8(1)
	if !overLoadFactor(h.count+1, h.B) {
		bigger = 0
		h.flags |= sameSizeGrow
	}
	oldbuckets := h.buckets
	newbuckets, nextOverflow := makeBucketArray(t, h.B+bigger, nil)

	flags := h.flags &^ (iterator | oldIterator)
	if h.flags&iterator != 0 {
		flags |= oldIterator
	}
	// commit the grow (atomic wrt gc)
	h.B += bigger
	h.flags = flags
	h.oldbuckets = oldbuckets
	h.buckets = newbuckets
	h.nevacuate = 0
	h.noverflow = 0

	if h.extra != nil && h.extra.overflow != nil {
		// Promote current overflow buckets to the old generation.
		if h.extra.oldoverflow != nil {
			throw("oldoverflow is not nil")
		}
		h.extra.oldoverflow = h.extra.overflow
		h.extra.overflow = nil
	}
	if nextOverflow != nil {
		if h.extra == nil {
			h.extra = new(mapextra)
		}
		h.extra.nextOverflow = nextOverflow
	}

	// the actual copying of the hash table data is done incrementally
	// by growWork() and evacuate().
}

```

`hashGrow` 是扩容的入口，通过上面的函数，我们可以了解到 go 中有两种类型的扩容方式：

* 等量扩容：如果是使用了太多溢出桶导致的扩容，这种情况一般是由于大量插入，又大量删除导致溢出桶越来越多，但其实绝大部分是空的，这时 go 会进行等量扩容，你可以看到这种情况 `bigger` 是 0 说明没有多分配桶。
* 倍数扩容：如果正常桶中绝大部分被占用，说明桶已经不太够用了，这种情况下冲突会大量存在，插入和读效率都会下降，这时 go 会倍数扩容（`bigger` 是 1）

通过 `hashGrow` 我们还可以看到，扩容并不是一个原子的过程，`makeBucketArray` 创建好新桶后，会将 `hmap` 的 `buckets` 指针指向新桶的位置，而旧桶和旧溢出桶会被挂载到 `oldbuckets` 或 `extra.oldoverflow` 上，后续旧桶中的数据会逐步迁移到新桶中，数据迁移是在 `growWork()` 和 `evacuate()` 中增量完成的。

`growWork()` 调用的也是 `evacuate()` 所以我们直接看这个函数：

```go
b := (*bmap)(add(h.oldbuckets, oldbucket*uintptr(t.bucketsize)))
newbit := h.noldbuckets()
if !evacuated(b) {
    // ...
}
```

`evacuated` 判断这个桶有没有被重新分配过：

```go
func evacuated(b *bmap) bool {
	h := b.tophash[0]
	return h > emptyOne && h < minTopHash
}
```

这里的 tophase 有三种可能的值：

```go
const (
    evacuatedX     = 2 // key/elem is valid.  Entry has been evacuated to first half of larger table.
	evacuatedY     = 3 // same as above, but evacuated to second half of larger table.
	evacuatedEmpty = 4 // cell is empty, bucket is evacuated.
)
```

* `evacuatedX` 该桶已经被重新分配到了倍数扩容的前一半
* `evacuatedY` 该桶已经被分配到了倍数扩容的后一半
* `evacuatedEmpty` 该桶是空的，并且已经被重新分配过了

关于 X 和 Y 我们后面会将它们是怎么确定的。

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/16459742070211645974206187.png)

上图描述了一个发生倍数扩容后的 hmap, 当前要对 b 处的桶做重新分配（等量扩容也一样）

```go
type evacDst struct {
	b *bmap          // current destination bucket
	i int            // key/elem index into b
	k unsafe.Pointer // pointer to current key storage
	e unsafe.Pointer // pointer to current elem storage
}
```

```go
var xy [2]evacDst
x := &xy[0]
x.b = (*bmap)(add(h.buckets, oldbucket*uintptr(t.bucketsize)))
x.k = add(unsafe.Pointer(x.b), dataOffset)
x.e = add(x.k, bucketCnt*uintptr(t.keysize))

if !h.sameSizeGrow() {
    // Only calculate y pointers if we're growing bigger.
    // Otherwise GC can see bad pointers.
    y := &xy[1]
    y.b = (*bmap)(add(h.buckets, (oldbucket+newbit)*uintptr(t.bucketsize)))
    y.k = add(unsafe.Pointer(y.b), dataOffset)
    y.e = add(y.k, bucketCnt*uintptr(t.keysize))
}
```

第一步就是找到 b 在新桶中前半部分和后半部分对应的位置，表现在图上就是：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/16459750892531645975089177.png)

接下来就是遍历当前要移动的桶和它所有的溢出桶，并将它们移动到对应位置：

```go
for ; b != nil; b = b.overflow(t) {
    k := add(unsafe.Pointer(b), dataOffset)
    e := add(k, bucketCnt*uintptr(t.keysize))
    // 遍历桶的 8 个键值对
    for i := 0; i < bucketCnt; i, k, e = i+1, add(k, uintptr(t.keysize)), add(e, uintptr(t.elemsize)) {
        top := b.tophash[i]
        if isEmpty(top) {
            b.tophash[i] = evacuatedEmpty
            continue
        }
        if top < minTopHash {
            throw("bad map state")
        }
        k2 := k
        if t.indirectkey() {
            k2 = *((*unsafe.Pointer)(k2))
        }
        // useY 表示要把这个桶移动到新桶（s）的前面还是后面
        var useY uint8
        if !h.sameSizeGrow() {
            // 这里决定了桶被分配到 x 还是 y
            hash := t.hasher(k2, uintptr(h.hash0))
            if h.flags&iterator != 0 && !t.reflexivekey() && !t.key.equal(k2, k2) {
                useY = top & 1
                top = tophash(hash)
            } else {
                if hash&newbit != 0 {
                    useY = 1
                }
            }
        }

        if evacuatedX+1 != evacuatedY || evacuatedX^1 != evacuatedY {
            throw("bad evacuatedN")
        }

        b.tophash[i] = evacuatedX + useY // 设置旧桶的 tophase
        dst := &xy[useY]                 // evacuation destination

        // 新 buckets 对应位置的桶已经满了，放到溢出桶里
        if dst.i == bucketCnt {
            dst.b = h.newoverflow(t, dst.b)
            dst.i = 0
            dst.k = add(unsafe.Pointer(dst.b), dataOffset)
            dst.e = add(dst.k, bucketCnt*uintptr(t.keysize))
        }
        // 设置对应的 tophase
        dst.b.tophash[dst.i&(bucketCnt-1)] = top // mask dst.i as an optimization, to avoid a bounds check
        // 移动键
        if t.indirectkey() {
            *(*unsafe.Pointer)(dst.k) = k2 // copy pointer
        } else {
            typedmemmove(t.key, dst.k, k) // copy elem
        }
        // 移动值
        if t.indirectelem() {
            *(*unsafe.Pointer)(dst.e) = *(*unsafe.Pointer)(e)
        } else {
            typedmemmove(t.elem, dst.e, e)
        }
        dst.i++

        // 遍历下一个键值对
        dst.k = add(dst.k, uintptr(t.keysize))
        dst.e = add(dst.e, uintptr(t.elemsize))
    }
}
```

这里很巧妙，因为不管是什么样的扩容，一个旧桶只能是对应一个新桶，这里直接先列出旧桶可能的存储位置 `var xy [2]evacDst` 然后在后面直接初始化一个 `dst := &xy[useY]` 就 ok 了，代码简洁，逻辑清晰。

最后，会调用 `advanceEvacuationMark` 去修改 `hmap.nevacuate` 的值, 它表示移动的进度, 当所有的旧桶都被转移时，会销毁 `oldbuckets`, 随后 GC 会回收这些内存

```go
if oldbucket == h.nevacuate {
    advanceEvacuationMark(h, t, newbit)
}
```

```go
func advanceEvacuationMark(h *hmap, t *maptype, newbit uintptr) {
	h.nevacuate++
	// Experiments suggest that 1024 is overkill by at least an order of magnitude.
	// Put it in there as a safeguard anyway, to ensure O(1) behavior.
	stop := h.nevacuate + 1024
	if stop > newbit {
		stop = newbit
	}
	for h.nevacuate != stop && bucketEvacuated(t, h, h.nevacuate) {
		h.nevacuate++
	}
    // 所有的旧桶都被转移了
	if h.nevacuate == newbit { // newbit == # of oldbuckets
		h.oldbuckets = nil
		if h.extra != nil {
			h.extra.oldoverflow = nil
		}
		h.flags &^= sameSizeGrow
	}
}
```

你或许会疑惑为什么要使用这样一种方式更新 `nevacuate` 的值，每次移动完一个桶后判断 `h.nevacuate == newbit` 应该更简单啊？答案藏在 `growWork` 中，上面说这是触发移动的入口，但问题在于只有在插入和删除时才会触发 `growWork`, 这意味着你需要把全部数据全部写一遍后扩容才能结束，这或许有点困难，所以 `growWork` 不光会移动当前桶，还会移动 `h.nevacuate` 这个桶。

```go
func growWork(t *maptype, h *hmap, bucket uintptr) {
	// make sure we evacuate the oldbucket corresponding
	// to the bucket we're about to use
	evacuate(t, h, bucket&h.oldbucketmask())

	// evacuate one more oldbucket to make progress on growing
	if h.growing() {
		evacuate(t, h, h.nevacuate)
	}
}
```

假设第一次我们移动了 6 号桶，这时 `h.nevacuate` 是 0 所以实际上移动了 0 号 和 6 号桶，移动 0 号桶时会触发 `advanceEvacuationMark` `h.nevacuate` 增加到 1 ，第二次假设我们移动了 2 号桶，实际移动的就是 1 和 2 号桶，`h.nevacuate` 最终会增加到 3 ，这样一来，你只需要写一半任意键值对扩容就可以正常结束了，虽然这是一个很巧妙的设计，但如果你是在构建一个只读数据，并且十个妥妥的非酋，在插入最后一个数据时发生了增量扩容，后面完全没写操作了，那你完了，你的内存将会额外多出一倍来！
