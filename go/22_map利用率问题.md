# Go 中 map 利用率

今天刷 B 站看见有 Up 主在讲布隆过滤器，提到了利用率的问题，假设有一组数据，范围分布非常广，使用布隆过滤器时如何尽量少的减少内存使用，感觉除了针对特定数据的定向优化外没什么特别好的办法，类似于 Google 那种加数据头以跳过大段间隙那样。然后想到类似的问题应该广泛存在于所有使用哈希表的数据结构中，那 go 中 map 的利用率如何呢？

## 数据收集

在 go 中 map 是一个内置的数据结构，没有一个简单的方法来拿到它占用的内存，以下两种方法供参考：

### pprof

通过 pprof 定向收集内存分配和使用，我们可以直观的得到某个函数占用了多少内存：

```go
package main
import (
	"net/http"
	_ "net/http/pprof"
)

func demo() {
	n := 90000
	m := make(map[int64]int64)
	for i := 0; i < n; i++ {
		m[int64(i)] = int64(i)
	}
	for {
	}
}

func TestSize(t *testing.T) {
	go func() {
		http.ListenAndServe(":3390", nil)
	}()
	demo()
}
```

然后通过 `go tool pprof -http :9090 http://127.0.0.1:3390/debug/pprof/heap` 观察 `demo` 的内存使用情况就可以了：

```txt
                                         2468.70kB   100% |   github.com/520MianXiangDuiXiang520/MapSize.TestSize /Users/junebao/Project/MapSize/mapsize_test.go:23 (inline)
 2468.70kB 40.77% 83.09%  2468.70kB 40.77%                | github.com/520MianXiangDuiXiang520/MapSize.demo /Users/junebao/Project/MapSize/mapsize_test.go:13
```

如上，我们就可以知道九万个 int64 的键值对占用了 2468.70KB

上面的办法简单粗暴，但要统计起来很麻烦

### unsafe

我们知道 map 的底层结构其实是 `runtime_hmap` 那通过 `unsafe` 理论上就可以强转得到原始结构，只要知道了数据桶和溢出桶的个数，我们也可以计算出 map 的真实内存：

```go
func Size[K comparable, V any](m map[K]V) int64 {
	var zeroK K
	var zeroValue V
	keySize := unsafe.Sizeof(zeroK)
	valueSize := unsafe.Sizeof(zeroValue)
	vo := reflect.ValueOf(m)
	hm := (*hmap)(unsafe.Pointer(vo.Pointer()))
	bn := 1<<hm.B + uintptr(hm.noverflow)
	bz := unsafe.Sizeof(bmap{}) + (keySize+valueSize)*bucketCnt
	return int64(unsafe.Sizeof(hmap{}) + bz*bn)
}
```

这个方法的缺点在于数值不精确，一来是 `noverflow` 是一个统计值，某些情况下可能会导致得到的溢出桶数量略小于真实数量，二来 `bmap`  中的 `overflow` 指针会根据键值对的类型有所变化，上面的程序中并没有计算该字段，因为键值对都不包含指针，理论上 map 会使用 `hmap` 的拓展字段存储溢出指针，总体来说该方法得到的值会小于真实值，但作为参考足够。如同样的九万个键值对使用上面方法得到的大小是 2457.976KB 比 pprof 版本少了 11KB

## 统计

```go
func main() {
	for i := 0; i < 1000; i++ {
		n := i * 100
		m := make(map[int64]int64)
		for i := 0; i < n; i++ {
			m[int64(i)] = int64(i)
		}
		res := Size(m)
		t := int64(16 * n)
		fmt.Printf("%d,%d,%d,%d,%f\n", n, res, t, res-t, float64(t)/float64(res))
	}
}
```

以 100 为 步幅测试一千组用例，导入 CSV 用 python 绘制出图表：

```python
import matplotlib.pyplot as plt
import csv


class MapSizeStatistic:
    """
    A statistic of map storage usage in go where key-value pairs are all int64
    """

    def __init__(self):
        self.utilization_list = []

        with open("./int64.csv") as fp:
            reader = csv.reader(fp)
            self.utilization_list = [float(i[-1]) for i in reader]
            print(self.utilization_list)

    def draw_utilization(self):
        x = [i*100 for i in range(len(self.utilization_list))]
        plt.plot(x, self.utilization_list)
        plt.show()


if __name__ == '__main__':
    mss = MapSizeStatistic()
    mss.draw_utilization()

```

结果如下：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1651660306137Figure_1.png)

将键全部使用随机数，得到结果如下：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1651674221416Figure_3.png)

几乎没有差别，周期性变化非常明显，可以确定引起利用率变化的主要原因在于元素数量，而利用率突然降低的节点就是发生了等量扩容。

从上面的测试可以看到最高利用率在 0.8 左右，最低利用率只有 0.4, 平均只有 0.5 左右

## 总结

总体利用率在 50% 左右，主要影响因素在于等量扩容，虽然 map 本就是空间换时间，但如果确实需要优化并且走投无路时，希望这些数据或许可以提供一些参考（分片，卡利用率的点……）

最后放上一张合影：

![](https://cdn.jsdelivr.net/gh/520MianXiangDuiXiang520/cdn@master/img/1651675491654Figure_4.png)

[代码](https://github.com/520MianXiangDuiXiang520/MapSize)