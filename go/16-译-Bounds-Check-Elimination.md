# [译] Bounds Check Elimination 边界检查消除

Go 是一种内存安全的语言，在针对数组 (array) 或 Slice 做索引和切片操作时，Go 的运行时（runtime）会检查所涉及的索引是否超出范围。如果索引超出范围，将产生一个 Panic，以防止无效索引造成的伤害。这就是边界检查（BCE）。边界检查使我们的代码能够安全地运行，但也会影响一定的性能。

<!-- more -->

> 原文链接：
>  [Bounds Check Elimination](https://go101.org/article/bounds-check-elimination.html)



自从 Go Toolchain 1.7 以后，标准的 Go 编译器采用了一个基于 SSA (静态单赋值形式)的新的编译器后端。SSA 帮助 Go 编译器有效地进行代码优化，比如 BCE (边界检查消除) 和 CSE (公共子表达式消除)。BCE 可以避免一些不必要的边界检查，CSE 可以避免一些重复的计算，如此使得标准的 Go 编译器可以生成更高效的程序。有时这些优化的改进效果是显而易见的。

本文将列出一些示例，说明 BCE 如何与标准的 Go 编译器1.7 + 协同工作。

对于 Go Toolchain 1.7 + ，我们可以使用 `-gcflags = “-d=ssa/check _ bce/debug=1” `编译器标志来显示哪些代码行仍然需要进行边界检查。

## 例 1

```go
// example1.go
package main

func f1(s []int) {
	_ = s[0] // line 5: 需要边界检查
	_ = s[1] // line 6: 需要边界检查
	_ = s[2] // line 7: 需要边界检查
}

func f2(s []int) {
	_ = s[2] // line 11: 需要边界检查
	_ = s[1] // line 12: 边界检查被消除
	_ = s[0] // line 13: 边界检查被消除
}

func f3(s []int, index int) {
	_ = s[index] // line 17: 需要边界检查
	_ = s[index] // line 18: 边界检查被消除
}

func f4(a [5]int) {
	_ = a[4] // line 22: 边界检查被消除
}

func main() {}
```

```cmd
$ go run -gcflags="-d=ssa/check_bce/debug=1" example1.go
./example1.go:5: Found IsInBounds
./example1.go:6: Found IsInBounds
./example1.go:7: Found IsInBounds
./example1.go:11: Found IsInBounds
./example1.go:17: Found IsInBounds
```

我们可以看到，没有必要为函数 `f2` 中的第 12 行和第 13 行进行边界检查，因为第 11 行的边界检查确保了第 12 行和第 13 行的索引不会超出范围。

但在函数 `f1` 中，必须对这三行都进行边界检查。因为第 5 行的边界检查不能保证第六行和第七行的安全，同样第六行的检查也不能保证第七行的安全。

而对于函数 `f3`，编译器知道如果第一个 `s [ index ]` 是安全的，那么第二个 ` s [ index ]` 就也是绝对安全的。

编译器还能正确地判断出 `f4` 中的唯一一行（22行）是安全的。

## 例 2

```go
// example2.go
package main

func f5(s []int) {
	for i := range s {
		_ = s[i]
		_ = s[i:len(s)]
		_ = s[:i+1]
	}
}

func f6(s []int) {
	for i := 0; i < len(s); i++ {
		_ = s[i]
		_ = s[i:len(s)]
		_ = s[:i+1]
	}
}

func f7(s []int) {
	for i := len(s) - 1; i >= 0; i-- {
		_ = s[i]
		_ = s[i:len(s)]
	}
}

func f8(s []int, index int) {
	if index >= 0 && index < len(s) {
		_ = s[index]
		_ = s[index:len(s)]
	}
}

func f9(s []int) {
	if len(s) > 2 {
	    _, _, _ = s[0], s[1], s[2]
	}
}

func main() {}
```

```cmd
$ go run -gcflags="-d=ssa/check_bce/debug=1" example2.go
```

酷! 标准编译器删除程序中的所有绑定检查。

注意: 在 Go Toolchain 1.11 版本之前，标准编译器不够智能，无法检测到第22行是安全的。

## 例3

```go
// example3.go
package main

import "math/rand"

func fa() {
	s := []int{0, 1, 2, 3, 4, 5, 6}
	index := rand.Intn(7)
	_ = s[:index] // line 9: bounds check
	_ = s[index:] // line 10: bounds check eliminated!
}

func fb(s []int, i int) {
	_ = s[:i] // line 14: bounds check
	_ = s[i:] // line 15: bounds check, not smart enough?
}

func fc() {
	s := []int{0, 1, 2, 3, 4, 5, 6}
	s = s[:4]
	i := rand.Intn(7)
	_ = s[:i] // line 22: bounds check
	_ = s[i:] // line 23: bounds check, not smart enough?
}

func main() {}
```

```cmd
$ go run -gcflags="-d=ssa/check_bce/debug=1" example3.go
./example3.go:9: Found IsSliceInBounds
./example3.go:14: Found IsSliceInBounds
./example3.go:15: Found IsSliceInBounds
./example3.go:22: Found IsSliceInBounds
./example3.go:23: Found IsSliceInBounds
```

哦，这么多地方还需要做边界检查！

但是，为什么标准的 Go 编译器认为第 10 行是安全的，而第 15 行和第 23 行却不是呢？编译器还不够聪明吗？

事实上，编译器设计如此！为什么？原因是子切片表达式中的起始索引可能大于原始切片的长度。让我们看一个简单的例子:

```go
package main

func main() {
	s0 := make([]int, 5, 10) // len(s0) == 5, cap(s0) == 10

	index := 8

    // 在 go 中，对于子切片语法 s[a:b] 必须保证 0 <= a <= b <= cap(s)
    // 否则会引起 panic

	_ = s0[:index]
	
    // 上面一行是安全的，但不能保证下面一行也是安全的
    // 事实上，下面一行将会导致 panic
	_ = s0[index:] // panic
}
```

因此，只有满足 `len(s) == cap(s)` 时，才能根据 `s[:index]` 是安全的得出 `s[index:]` 也是安全地的结论，这就是为什么函数 `fb` 和 `fc` 中的代码行仍然需要进行边界检查的原因。

标准 Go 编译器成功地检测到函数 `fa` 中的 `len (s)` 等于 `cap (s)` 干得好! Go团队加油！

## 例4

```go
// example4.go
package main

import "math/rand"

func fb2(s []int, index int) {
	_ = s[index:] // line 7: bounds check
	_ = s[:index] // line 8: bounds check eliminated!
}

func fc2() {
	s := []int{0, 1, 2, 3, 4, 5, 6}
	s = s[:4]
	index := rand.Intn(7)
	_ = s[index:] // line 15 bounds check
	_ = s[:index] // line 16: bounds check eliminated!
}

func main() {}
```

```cmd
$ go run -gcflags="-d=ssa/check_bce/debug=1" example4.go
./example4.go:7:7: Found IsSliceInBounds
./example4.go:15:7: Found IsSliceInBounds
```

在这个例子中，go 编译器成功推断出：

* 如果第 7 行是安全的，那么第 8 行也是安全地
* 如果第 15 行是安全的，那么第 16 行也是安全地

注意:在1.9版本之前的 Go Toolchain 中，标准的 Go 编译器无法检测到第 8 行不需要边界检查。

## 例 5

当前版本的标准 Go 编译器不够聪明，无法消除所有不必要的边界检查。有时，我们可以做一些提示来帮助编译器消除一些不必要的边界检查.

```go
// example5.go
package main

func fd(is []int, bs []byte) {
	if len(is) >= 256 {
		for _, n := range bs {
			_ = is[n] // line 7: bounds check
		}
	}
}

func fd2(is []int, bs []byte) {
	if len(is) >= 256 {
		is = is[:256] // line 14: a hint
		for _, n := range bs {
			_ = is[n] // line 16: BCEed!
		}
	}
}

func fe(isa []int, isb []int) {
	if len(isa) > 0xFFF {
		for _, n := range isb {
			_ = isa[n & 0xFFF] // line 24: bounds check
		}
	}
}

func fe2(isa []int, isb []int) {
	if len(isa) > 0xFFF {
		isa = isa[:0xFFF+1] // line 31: a hint
		for _, n := range isb {
			_ = isa[n & 0xFFF] // line 33: BCEed!
		}
	}
}

func main() {}
```

```cmd
$ go run -gcflags="-d=ssa/check_bce/debug=1" example5.go
./example5.go:7: Found IsInBounds
./example5.go:24: Found IsInBounds
```

> 核心的思想就是尽量消除在循环中的边界检查，这个例子有点奇怪，可以看下面这个：
>
> ```go
> // example4.go
> package main
> 
> func bad(a, b []int64, n int) {
> 	if len(a) >= n && len(b) >= n {
> 		for i, v := range b {
> 			a[i] = v
> 		}
> 	}
> }
> 
> func good(a, b []int64, n int) {
> 	if len(a) >= n && len(b) >= n {
> 		a = a[:n]
> 		b = b[:n]
> 		for i, v := range b {
> 			a[i] = v
> 		}
> 	}
> }
> 
> func main() {}
> 
> ```
>
> ```cmd
> $ go run -gcflags="-d=ssa/check_bce/debug=1" .\example2.go
> # command-line-arguments
> .\example2.go:7:5: Found IsInBounds
> .\example2.go:14:8: Found IsSliceInBounds
> ```
>
> 通过 14 15 行的子切片操作，我们可以把边界检查放到循环之外，简单跑一下 Benchmark 差距还是挺明显的
>
> ```txt
> cpu: Intel(R) Core(TM) i7-7500U CPU @ 2.70GHz
> BenchmarkBCE
> BenchmarkBCE/good
> BenchmarkBCE/good-4         	  296671	      4912 ns/op
> BenchmarkBCE/bad
> BenchmarkBCE/bad-4          	  182302	      6136 ns/op
> PASS
> ```

## 摘要

标准的 Go 编译器进行了更多的 BCE 优化。它们可能不像上面列出的那么明显，所以本文不会全部展示。

尽管标准 Go 编译器中的 BCE 特性仍然不够完美，但对于许多常见情况来说，它确实做得很好。毫无疑问，标准的 Go 编译器在以后的版本中会做得更好，这样上面第5个例子中的提示可能就没有必要了。谢谢团队增加了这个美妙的功能！

## 参考文献

1. [Bounds Check Elimination 边界检查消除](https://docs.google.com/document/d/1vdAEAjYdzjnPA9WDOQ1e4e05cYVMpqSxJYZT33Cqw2g)
2. [Utilizing the Go 1.7 SSA Compiler 使用 Go 1.7 SSA 编译器](https://talks.godoc.org/github.com/klauspost/talks/2016/go17-compiler.slide) (and (及[the second part 第二部分](https://talks.godoc.org/github.com/klauspost/talks/2016/go17-compiler-2.slide))