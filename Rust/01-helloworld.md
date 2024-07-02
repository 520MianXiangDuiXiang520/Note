# Rust 基础

## Hello Rust

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
echo "export $PATH=$PATH:~/.cargo/bin" >> ~/.bashrc
source ~/.bashrc
```

### Vscode 插件推荐

### cargo

cargo 是 Rust 的包管理工具，下载 Rust 时会自动下载

常用命令：

```sh
# 创建 cargo 项目，有两种模式 bin 和 lib 前者是可运行项目，后者是依赖库项目，默认 bin
cargo new $projectName

# 执行 cargo 项目，默认 debug 模式，release 模式使用 `cargo run --release`
cargo run

# 只编译
cargo build

# 编译期检查
cargo check
```

#### 目录结构

* src 源码目录
* Cargo.toml: 项目数据描述文件，包含项目的所有元配置信息（版本，依赖项……）
* Cargo.lock: 依据 Cargo.toml 生成的详细依赖清单，由 Cargo 管理，不需要修改

#### 依赖管理

cargo 允许的依赖来源于三个地方：

* Rust 官方仓库 crates.io
* git 仓库
* 本地

```toml
[dependencies]
rand = "0.3"
hammer = { version = "0.5.0" }
color = { git = "https://github.com/bjz/color-rs" }
geometry = { path = "crates/geometry" }
```

#### 替换默认源

1. **永久替换**

编辑 `$HOME/.cargo/config.toml`

```toml
[source.crates-io]
replace-with = 'ustc'

[sourice.ustc]
registry = "git://mirrors.ustc.edu.cn/crates.io-index"
```

2. **临时替换**

修改项目 Cargo.toml 依赖项的 `registry` 字段，如：

```toml
hammer = { version = "0.5.0", registry = "ustc"}
```

3. **常用源地址**

```toml
# 中科大
[sourice.ustc]
registry = "git://mirrors.ustc.edu.cn/crates.io-index"

# ByteDance
[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"
```

### Hello World

程序入口在 `main.rs` 的 main 函数：

```rust
fn main(){
    println!("Hello Rust")
}
```

## 基础知识

### 变量的绑定与解构

* Rust 使用 `let` 关键字给一个变量绑定值（对象），执行绑定后，这个值就拥有了这个对象的**所有权**.

* 同一个变量名可以重复绑定不同的对象,称为变量屏蔽（shadowing）。

* Rust 所有的变量都是**不可变**的，即绑定对象后不允许再修改，除非重新使用 `let` 绑定.
* 可以使用 `let mut` 声明变量是**可变的**
* 使用 `const` 声明常量，常量可以声明在任意作用域内，常量必须标注类型

```rust
const PLANCK_CONSTANT: f64 = 6.626E-34;

fn main() {
    println!("{}", PLANCK_CONSTANT);
    let x = 1i32;
    let x = 1f64;
    println!("{}", x);
    let mut x = true;
    x = false;
    assert_eq!(x, false);
}
```

* `let` 支持变量解构，Rust 1.59 后，支持在左式中使用元组，切片和结构体模式：

```rust
    id: i64,
}

fn main() {
    let (mut x, y): (i32, f64) = (1, 1f64);
    x += 1;
    println!("x:{}, y:{}", x, y); // x:2, y:1

    let (a, b, c, d, e);
    (a, b) = (1, 2);
    [c, .., d, _] = [1, 2, 3, 4, 5, 6, 7];
    Square { id: e } = Square { id: 99 };
    assert_eq!([a, b, c, d, e], [1, 2, 1, 6, 99]);
}
```

### 基本数据类型和流程控制

基本数据类型：

* 整数类型： i8, u8, i16, u12, i32, u32, i64, u64, i128, u128, isize, usize
* 浮点类型：f32, f64
* 字符：`'字'`
* 布尔：true, false
* 单元类型：`()`：是一个占位符，类似于 Go 的 `struct{}` 没有显式返回值的函数返回的就是一个单元。

需要注意的是：
* 整数的默认类型是 `i32`，浮点默认类型是 `f64`
* 在 debug 模式下，整数溢出会 panic，release 模式下会按补码循环溢出，想要显式地溢出可以使用以下方法：
  * `wrapping_xx`: 显式溢出
  * `checked_xx`: 溢出时返回 None
  * `overflowing_xx`: 会额外带一个返回值表示有没有溢出
  * `saturating_xx`: 如果溢出，则取最大值或最小值

  ```rust
    fn main() {
        let x = i8::wrapping_add(127, 3);
        println!("{}", x); // -126

        let result = i8::checked_add(127, 3);
        match result {
            None => println!("overflowing!!"),
            Some(x) => println!("{}", x)
        }

        let (x,y) = i8::overflowing_add(127, 3);
        println!("{}, {}", x, y); // -126, true

        let x = i8::saturating_add(127, 3);
        println!("{}", x); // 127
    }
  ```
* Rust 中浮点数没有实现 `std::cmp::Eq` 特征，因此不能被用作 HashMap 的 key（在 go 中是可以的）
* `NaN` 表示数学上未定义的结果，如负数开根，可以使用 `is_nan()` 判断
* 整数不可以除 0， 正数除 0 返回 inf(正无穷大)，负数除 0 返回 -inf(负无穷大), 0 除 0 返回 nan

```rust
fn main() {
    println!("{}", (1.0/0.0f32).is_infinite());
    println!("{}", (-1.0/0.0f32).is_infinite());
    println!("{}", (0.0/0.0f32).is_nan());
}
```

* 所有 Unicode 值都可以作为一个 char，占 4 字节

#### 流程控制

##### 函数

```rust
fn add(a: i32, b:i32) -> i32 {
    a + b // 表达式
}
```

* 所有参数都要标注参数
* 无返回值的函数，如 `main()` 返回值其实是 单元 `()`
* 可以用 `!` 表示某个函数永远不会返回（发散函数），如 `fn dead_func() -> ! { panic!("game over") }`

##### 语句和表达式

Rust 中语句和表达式是严格区分的（许多语言是混淆的）
* 语句（statement）：执行一个操作，但不返回任何东西， 语句以分号结尾，如 `let x = 1_i32;`
* 表达式（expression）：会在求值后返回一个结果，表达式不以分号结束，函数以及语句块都是表达式, 可以被绑定给某个变量或作为函数返回值返回，如 

```rust
fn main() {
    let sum = add(1, 3); // 表达式
    println!("{}", sum);

    let y = {
        let mut x = 1;
        x + 1
    };
    println!("{}", y);
}

fn add(a: i32, b:i32) -> i32 {
    a + b // 表达式
}
```
* 有一点需要注意 `x+=3` 是语句，因为它本质上等价于 `let x = x + 3;`

### 所有权和借用

Rust 引入所有权和生命周期概念的原因是为了解决垃圾回收的问题，它会在编译期分析变量的生命的周期，并在合适的位置插入代码释放内存，因此 Rust 中的每个对象都必须有非常明确的引用关系和生命周期。

考虑下面有问题的代码

```rust
fn main() {
    let x = String::from("hello world");
    {
        let _x1 = x;
    }
    println!("{}", x);
}
```

第二行在堆上初始化了一个 String 对象，把它绑定给了 x 变量，第四行又把这个对象绑定到了 _x1 变量上，_x1 的生命周期到第四行就结束了，因此到这原来的对象就会被释放掉，然而第六行我们又在使用这个对象，这就会导致非预期的结果，即便不使用，第六行之后也要释放这个对象，会导致二次释放的问题。

为了避免这些问题， Rust 规定：

1. 每一个值都被一个变量所拥有，该变量被称为值的所有者
2. 一个值同时只能被一个变量所拥有，
3. 当所有者(变量)离开作用域范围时，这个值将被丢弃(drop)

变量绑定的本质就是所有权的转移，一旦变量失去对象的所有权，该变量便不再可用，对象被 drop 的时机是确定的，即拥有所有权的变量离开作用域时。

函数传参和返回值同样涉及所有权的转移。

上面的代码一开始对象的所有权被 x 拥有，第四行移交给 _x1，这时 x 变量便不再可用，同时 _x1 的作用域在第五行结束，对象被销毁。

对于简单的数据类型，变量绑定时会拷贝一份值，所以并不存在所有权转移的问题，因为每个变量都拥有一份全新的，完全独占的值（对象），如下面的代码是完全正确的：

```rust
fn main() {
    let x: i32 = 9;
    let _x1 = x;
    println!("{}", x);
}
```

其实，除了基本数据类型外，所有分配在栈上的或者拥有 `Copy` 特征的对象在变量绑定时都是拷贝的，如不可变引用，内部元素都是可 Copy 的元组等（`(i32, i32)`）。

对于分配在堆上的对象，如 String 可以使用其 `clone()` 方法深拷贝一份新的对象绑定到新变量上，如：

```rust
fn main(){
    let s = String::from("hello");
    let _s = s.clone();
    println!("{}", s)
}
```

#### 借用

借用其实是对拥有对象所有权的变量的引用，它不会改变对象的所有权，因为变量本质是一个指向对象的指针，指针的绑定是拷贝的。

借用分为可变和不可变两种，不可变借用只能读原对象，不能修改，因此它是无害的，对一个变量，可以声明多个不可变借用。

只有可变变量才能声明可变借用，一个变量只能声明一个可变借用，同时，不允许同时声明可变借用和不可变借用。（类比并发控制很好理解，只能允许并发读，不能允许并发读写，或者并发写）

```rust
fn main() {
    let mut s = String::from("hello");
    append_world(&mut s); // 可变借用
    assert_eq!(str_len(&s), 12); // 不可变借用
    println!("{}", s); // 所有权没改变
}

fn str_len(s: &String) -> usize {
    s.len()
}

fn append_world(s: &mut String) {
    s.push_str(", world")
}
```

> 实际上 Rust 的编译器足够聪明，以下代码虽然同时有可变和不可变借用，但它是可以编译通过的：
> ```rust
> fn tt() {
>    let mut s = String::from("hello");
>    let _s1 = &mut s;
>    let _s2 = &s;
> }
> ```
> 原因是 _s1 的生命周期其实只到第三行，这种在作用域结束前就结束变量生命周期的行为称为 NLL(Non-Lexical Lifetimes)
>

### 复合数据类型

### 模式匹配

### 泛型和特征

### 生命周期

### 包和模块

