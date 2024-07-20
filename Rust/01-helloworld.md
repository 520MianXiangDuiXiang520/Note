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
struct Square {
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

#### 函数

```rust
fn add(a: i32, b:i32) -> i32 {
    a + b // 表达式
}
```

* 所有参数都要标注参数
* 无返回值的函数，如 `main()` 返回值其实是 单元 `()`
* 可以用 `!` 表示某个函数永远不会返回（发散函数），如 `fn dead_func() -> ! { panic!("game over") }`

#### 语句和表达式

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

#### 流程控制

**分支结构**：Rust 使用经典的 `if - else if - else` **表达式** 表示分支结构，因为是表达式，所以可以为其绑定变量，如

```rust
fn main() {
    let x = 12;
    let x = if x % 10 == 0 {
        1
    } else {
        2
    };
    assert_eq!(x, 1)
}
```

**循环结构**：Rust 支持 `for`, `while`, `loop` 三种循环模式，支持在多重循环中加标签直接跳出外层循环， 如：

```rust 
fn main() {
    let mut count = 0;
    'outer: loop {
        while count < 20 {
            count += 2;
        }

        count += 5;

        loop {
            if count >= 30 {
                break 'outer;
            }

            continue 'outer;
        }
    }
    println!("{}", count);
}
```

loop 是一个表达式，可以用 break 返回值：

```rust
fn main() {
    let count = loop {
        break 1;
    };
    println!("{}", count);
}
```

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

#### 数组和切片

数组是类型相同，长度固定的数据结构, 可以使用 `[初始值;数量]` 快速初始化数组，如：

```rust
fn main() {
    let list = [1, 1, 1, 1, 1];
    let list2 = [1; 5];
    assert_eq!(list, list2)
}
```

使用这种方式初始化数组时，数组的每个元素都是 copy 出来的，所以如果数组元素不是基本类型时，要注意是否实现了 Copy 特征，没实现的可以选择通过函数初始化，如：

```rust
fn main() {
    let mut _list:[String;5] = std::array::from_fn(|_i| String::from("value"));
}
```

**切片** 是对数组中部分连续片段的引用

```rust
fn main() {
    let  list:[String;5] = std::array::from_fn(|_i| String::from("value"));
    let  _list0:&[String] =  &list[0..3];
}
```

#### 字符串

Rust 核心只支持一种字符串类型 `str` 它是一个不可变的字节序列 `[u8;x]`，由于他的长度是不确定的，所以几乎无法直接使用 `str` 这种类型，一般都会使用他的引用 `&str`, 或者叫字符串切片。

> Go 中类似，`string` 本身是一个指针，指向底层的某个字节数组，这个数组在 Rust 中就是 `str` 类型。
> ```go
> type StringHeader struct {
>     Data uintptr
>     Len  int
> }
> 
> ```
> 因此，Rust 的 `&str` 可以类比 Go 的 `string`，是 `str` 的一个切片，当然，Go 中并不是切片，但与切片的结构体相比，字符串只少了一个表示容量的 Cap 字段，因此，你也可以说 Go 的字符串是一个只读切片。
> ```go
> type SliceHeader struct {
>     Data uintptr
>     Len  int
>     Cap int
> }
> ```
> 

经常使用的字符串字面量就是字符串切片 `&str`， 它指向的不可变字节数组就位于数据段的只读区：

```rust
fn main(){
    let _s: &str = "hello rust";
}
```

另一种常用的字符串类型是 `String` 它是标准库（不是 Rust Core）提供的一种可变的字符串类型，底层是一个动态的字节数组：

```rust
pub struct String {
    vec: Vec<u8>,
}
```

你可以使用 `as_str()` 方法将它方便地转换成 `&str` 类型，由于 deref 隐式强制转换，你也可以直接对其取引用得到 `&str` 类型

```rust
fn main() {
    let s = String::from("hello word");
    let _ps: &str= s.as_str();
    let _ps2: &str = &s;
}
```

值得注意的是 不管是字面量 `&str` 还是 `String` 其编码方式都是 UTF-8 这意味着单个字符是不定长的，直接对其执行切片操作是很危险的，<text style="color:red">如果索引的字节没有落到字符边界上，将会导致程序崩溃</text>。

```rust
let hello = "中国人";

let s = &hello[0..2]; // will panic
```

你可以使用 `chars()` 方法去遍历其中的 char, 更复杂的操作可以使用 [utf8-slice](https://crates.io/crates/utf8_slice) 库。


#### 元组

元组是一种由多种数据类型按固定顺序组织在一起的固定长度的复合数据结构，如

```rust
fn main() {
    let mut tup:(f64,i32,i16) =(1.0, 2, 3);
    tup.0 = 2.0;
    println!("{}", tup.0)
}
```

你可以使用 `.` 来操作其中的元素，也可以使用模式匹配结构元组：

```rust
fn main() {
    let mut tup:(f64,i32,i16) =(1.0, 2, 3);
    tup.0 = 2.0;
    println!("{}", tup.0);
    let (x,y,z) = tup;
    println!("{}, {}, {}", x, y, z);
}
```

空的元组不占用任何空间，被称为 `unit` 类似于 Go 中的 `struct{}`

```rust
fn main(){
    let _u: () = ();
}
```

#### 结构体和方法

你可以将元组看成一个匿名字段的结构体（这样看来 `()` 和  `struct{}` 确实是一样的），结构体是一种功能更强大和复杂的元组：

```rust
struct Blog {
    id: u64,
    abs: String,
    tags: Vec<String>
}

fn main() {
    let blog = Blog {
        id: 1,
        abs: "hello rust".to_string(),
        tags: vec!["rust".to_string()]
    };
    println!("{}", blog.abs);
}
```

需要注意的是初始化结构体时，<text style="color:red">每个字段都必须初始化</text>

Rust 不允许将结构体中某个单独的字段标识为可变的，如果想要修改某个字段，则要求整个结构体都是可变的。

某些情况下，我们不关心结构体中的字段名，这时，你可以声明一个类似元组的结构体，称为 `tuple struct`:

```rust
struct Vector(f64, f64, f64);

fn main() {
    let _p = Vector(1.0, 0.0, 1.0);
}
```

当然，类似于 unit 你也可以声明一个没有任何字段的结构体，这在需要实现某些特征时会很有用：

```rust
struct Empty;

fn main() {
    let _e = Empty;
}
```

##### 语法糖

1. 当使用函数初始化结构体时，如果函数参数和结构体字段名相同，初始化时可以省略字段名：

```rust
struct Pet {
    id: i32,
    pet_type: i32,
    level: u32,
}

fn new_pet(id: i32, tp: i32, level: u32) -> Pet {
    Pet {
        id,
        pet_type: tp,
        level,
    }
}

fn main() {
    let _pet = new_pet(1, 1, 1);
}
```

2. 当你用一个结构体实例更新另一个结构体实例时，如果只是要改其中的某几个字段，可以使用结构体更新语法：

```rust
fn main() {
    let pet1 = new_pet(1, 1, 1);
    let pet2 = Pet{
        id: 2,
        ..pet1
    };
    assert_eq!(pet2.id, 2);
}
```

##### 方法

Rust 中，结构体方法是写在 `impl` 块中的：

```rust
impl Pet {
    fn new(id: i32, tp: i32, level: u32) -> Self {
        Pet {
            id,
            pet_type: tp,
            level,
        }
    }

    fn upgrade(&mut self) -> u32 {
        self.level += 1;
        self.level
    }
}

fn main() {
    let _e = Empty;

    let _p = Vector(1.0, 0.0, 1.0);

    let mut pet1 = Pet::new(1, 1, 1);
    pet1.upgrade();
    assert_eq!(2, pet1.level);
}
```

注意，在 `impl` 块中，你可以使用 `Self` 指代结构体类型（如上面 new 函数的返回值），使用 `self` 指代结构体的具体实例（如 upgrade 函数的入参）。

只有第一个参数是 `self` 的函数才是结构体的方法，其他写在 impl 块中的，例如 new 这样的函数称为 **结构体的关联函数** 类似于其他语言中的静态方法，关联函数需要使用 `::` 调用。

Rust 允许方法名和字段名相同，这样的方法一般称为 `getter` 常用来隐藏私有字段。

并不是一个结构体只能对应一个 impl 块，你可以按功能需求，将结构体方法组织在不同的块中。

也可以为元组结构体添加方法：

```rust
struct RGB(u16,u16,u16);

impl RGB {
    fn to_hex(&self)->String {
        format!("#{:02X}{:02X}{:02X}", self.0, self.1, self.2)
    }
}

fn main() {
    let red = RGB(215, 0, 58);
    println!("{}", red.to_hex());
}
```

##### 结构体解构

```rust
struct Vector {
    x: f64,
    y: f64,
}

fn struct_test() {
    // 结构体解构
    let pos = Vector{x: 1.0, y: 2.0};
    let Vector{x: a, y: b} = pos;
    assert_eq!(a, 1.0);
    assert_eq!(b, 2.0);

    let red = RGB(215, 0, 58);
    let RGB(r, g, b) = red;
    assert!(r == red.0 && g == red.1 && b == red.2);
}
```

#### 动态数组 Vector

创建动态数组

```rust
let mut stack:Vec<i32> = Vec::new();
stack.push(1);
println!("{}", stack[0]);

// 宏
let _stack = vec![1, 2, 3];
```

如果你能预估数组的大小，可以使用 `Vec::with_capactiy(cap)` 来创建，避免扩容导致性能问题

读取元素：可以使用下标或者 get 方法，后者返回 Option 可以避免边界溢出

由于 Vector 会扩容，这个过程中会涉及其中元素的拷贝，因此 Vector 中元素的作用域和 vector 的作用域是相同的，不能在持有其中某个元素的不可变引用时去尝试获取它的可变引用，如以下代码时无法编译通过的：

```rust
let mut x = vec![1, 2, 3];
let first = x.get(0);
x.push(4);
if let Some(v) = first {
    println!("{v}")
}
```

可以使用 for-in 遍历 Vector 中的元素

```rust
for i in &mut x {
    *i += 10;
}
```


#### HashMap

```rust
use std::collections::HashMap;

let mut dict:HashMap<&str, i32> = HashMap::new();
dict.insert("a", 1);
let a = dict.get("a");
if let Some(x) = a {
    println!("{x}")
}
```

* HashMap 不包含在 prelude 中，需要手动引入
* 和其他类型一样，如果写入 HashMap 的键值实现了 `Copy` 特征，写入 HashMap 时该键值会被拷贝一份复制进去，否则所有权就会被移交给 HashMap

```rust
let mut dict = HashMap::new();
let key = String::from("key");
dict.entry(key).or_insert(1);
println!("{key}"); // borrow of moved value: `key`!!
```

* 和 Vector 一样，HashMap 中元素的作用域和 HashMap 的作用域一致：

```rust
let val = dict.get(&k2);
dict.insert("ss".to_string(), 1);
if let Some(x) = val {
    println!("{x}")
}
```

* 修改和遍历 HashMap：

```rust
let mut map = HashMap::with_capacity(2);
let text = "let mut dict = HashMap::new();";
for word in text.split_ascii_whitespace(){
    let count = map.entry(word).or_insert(0);
    *count +=1 ;
}
for (k, v )in map.iter(){
    println!("{k}: {v}")
}
```

* HashMap 的 key 要求实现 `Eq` 特征，因此浮点数不可以做 Key

### 枚举和模式匹配

枚举常用在表示**有限**的状态或选项中，它可以将有限的这些状态和选项抽象成同一种类型，方便统一处理。

```rust
enum Order {
    Attack,
    Demolition,
    Reinforce,
    Build
}

fn is_hostile(order: Order)-> bool {
    match order {
        Order::Attack | Order::Demolition => true,
        _ => false
    }
}
```

Rust 的枚举值可以携带数据：

```rust
struct Square {
    id: i64
}
struct Building {}

enum Order {
    Attack(Square),
    Demolition(Building),
    Reinforce(Building),
    Build(Building)
}

fn main() {
    let order = Order::Attack(Square{id: 1});
    match order {
        Order::Attack(sq) => println!("attack -> {}", sq.id),
        _ => println!("not attack")
    }
}
```

你也可以为枚举实现方法：

```rust
impl Order {
    fn is_hostile(&self)-> bool {
        match self {
            Order::Attack(_) | Order::Demolition(_) => true,
            _ => false
        }
    } 
}

fn main() {
    let order = Order::Attack(Square{id: 1});
    assert!(order.is_hostile());
}
```

#### 模式匹配

当我们在谈论 **模式匹配** 时，我们首先需要知道 「模式」是什么！在 Rust 中，模式（Patterns）是一种特殊的语法，它描述的其实是数据的「形状」，按照模式描述的这种形状，程序将值与数据进行匹配，以此更好地控制程序流程。

模式一般由以下内容组合而成：

* 字面量
* 解构的数组，枚举，结构体或元组
* 变量
* 通配符
* 占位符

考虑最简单的一条赋值语句：

```rust
let _x = 5;
```

这也是一种模式匹配，其中 `_x` 是变量名，一种变量模式，`let` 指示将匹配到的值 `5` 绑定到对应的变量上。

`let` 的语法为：

```rust
let PATTERN = EXPRESSION;
```

因此，由上面说的几种内容组合成的模式都可以作为表达式的赋值对象：

```rust
enum OnlyOne {
    One(i32)
}

let _ = 1; // 占位符
let (_a, _b, _c) = (1, 2, 3); // 解构的元组
let [_a, _b, _c] = [1, 2, 3]; // 解构的数组
let Vector { x: _a, y: _b } = Vector { x: 1.0, y: 2.0 }; // 解构的结构体
let OnlyOne::One(_x) = OnlyOne::One(1); // 解构的枚举
let ([_a, _b], _c) = ([1, 2], 3); // 组合
```

比较特殊的是枚举，因为要求匹配枚举必须穷尽所有可能，所以我们一般使用不会直接使用 let 匹配，除非像上例一样枚举类型中只有一个枚举值，一般我们会选择使用 `if let` 或 `match` 来匹配枚举类型：

```rust
let x = Some(1);
if let Some(_v) = x {
    println!("x")
}

match x {
    Some(_) => println!("x"),
    _ => ()
}
```

由于 Option 枚举包含两个枚举值，None 和 Some 所以我们不能直接使用 `let` 匹配，上例中 `if let` 和 `match` 的效果是一样的，在只处理其中一个类型，忽略其他类型时，我们一般使用 `if let`

与 `if let` 相似的还有 `while let`

```rust
let mut stack = vec![1, 2, 3];
while let Some(x) = stack.pop() {
    println!("{}", x)
}
```

`stack.pop()` 返回值是一个 `Option<T>` 我们使用 `while let` 将其与解构的枚举模式进行匹配，匹配到除 `Some` 外的类型时，跳出循环。

`if let` 和 `while let` 这种只关心其中一种值，而忽略其他的模式匹配被称为 「可驳模式匹配」

除此之外，在 `for` 循环中也有模式匹配的影子：

```rust
for (i, v) in stack.iter().enumerate() {
    println!("{},{}", i, v)
}
```

`enumerate` 方法返回的是一个迭代器，每次循环都会返回一个元组，这里其实是解构的元组模式匹配。

最后，这种模式匹配在函数参数中也是适用的：

```rust
fn foo((x, y):(i32, i32)) {
    println!("{}, {}", x, y);
}
foo((1, 2));
```

#### 模式匹配的一些补充

1. 单分支多模式

```rust
let x = 1;
match x {
    1 | 2 => println!("{}", x),
    _ => ()
}
```

2. 通过序列匹配

```rust
match x {
    1..=5 => println!("{} in [1,5]", x),
    _ => ()
}
```

3. 匹配守卫

```rust
match x {
    1..=20 if x != 7 => println!("{} in [1,20] not 7", x),
    _ => ()
}
```

4. 使用 match 解构

```rust
// 解构结构体
let pos = Vector{x: 1.0, y: 2.0};
match pos {
    Vector{x: vx, y: 0.0} => println!("{}", vx),
    Vector{x: 0.0, y: vy} => println!("{}", vy),
    Vector{x: vx, y: vy} => println!("{} {}", vx, vy)
}

// 解构数组/元组
let array = [1_i32;20];
match array {
    [x,..] => println!("first: {}", x),
    [.., x] => println!("last: {}", x) // 这一行是不可达的，因为上一行一定会匹配成功！
}

// .. 忽略其他项目的方法可以用在任何解构的地方，如
match pos {
    Vector{y: vy, ..} => println!("{}", vy),
    Vector{x: _, y: vy} => println!("{}", vy), // 不可达，和上一行是等价的
}
```

5. @绑定

```rust
let s = Some(1);
match s {
    Some(tmp @ 0..=3) => println!("{}", tmp),
    _ => ()
}
```

@ 的语法是 `new_var @ pattern` 除了 match 你可以用在任何模式匹配的地方，比如 let 

```rust
let pos = Vector{x: 1.0, y: 2.0};
if let p @ Vector{x: 1.0, ..} = pos {
    println!("match {:?}", p)
} else {
    println!("unmatch")
}
```

变量绑定要要绑定到所有模式上：

```rust
if let num @ (1 | 2) = 1 {
    println!("{}", num)
}
```

括号是不能省略的，否则就只能绑定到 1 了。

#### 总结

模式匹配初看非常庞杂，无厘头，match，let，if-let，while-let…… 还有各种诸如@绑定，序列，之类的特性

但它的内核是统一的，模式表示的是某种数据的 「形状」 通过匹配将具体的数据赋值给变量。

这里的数据可能来自字面量，如 `let x = 1;` 也可能稍微复杂一点来自被解构的复合数据结构，这样的数据就称为模式。

这种数据到变量的绑定有两个关键字可以实现，就是 `let` 和 `match` 

Rust 是一门安全的语言，任何未定义的和非预期行为都不被允许，因此，在进行这样的绑定时，你必须保证右边数据是唯一确定的，也就是「可驳的 refutable」，大部分诸如字面量之类的数据（或者叫模式）都是可驳的，因此你可以直接使用 `let` 进行模式匹配。

但当右边的模式是解构的复合解构时，就存在匹配不上的情况，我们就需要明确地告诉程序如何处理这种情况，这个就是 `if let` 或者 `match` 在做的事。前者说「如果匹配上，就执行 xxxx」后者列举了一系列情况，当 xx 的时候执行 xx, 当 yy 的时候执行 yy……

以上，想要理解模式匹配，你要始终记得：
1. 一切的赋值行为本质都是模式匹配
2. 进行匹配的模式必须是可驳的

### 泛型和特征

### 生命周期

### 包和模块

