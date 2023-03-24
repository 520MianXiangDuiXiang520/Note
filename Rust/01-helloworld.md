# HelloWorld

## 下载

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
echo "export $PATH=$PATH:~/.cargo/bin" >> ~/.bashrc
source ~/.bashrc
```

## HelloWorld

```rs
fn main(){
    println!("Hello,World");
}
```

> println! 是一个宏而不是函数

```sh
rustc helloworld.rs 
./helloworld
```

`rustup doc` `打开本地文档

## Cargo

Cargo 是 Rust 的包管理和构建工具

### 初识

```sh
# 新建 rust 项目
cargo new hellocargo
```

目录结构：

```txt
.
├── hellocargo
│   ├── Cargo.lock              # 追踪项目依赖（生成）
│   ├── Cargo.toml              # 项目依赖描述文件
│   ├── src                     # 源码目录
│   │   └── main.rs
│   └── target                  # 运行后生成的产物
│       ├── CACHEDIR.TAG
│       └── debug               # 调试文件
│           ├── build
│           ├── deps
│           ├── examples
│           ├── hellocargo
│           ├── hellocargo.d
│           └── incremental
```

常用命令

```sh
# 直接运行项目
cargo run

# 编译
cargo build
cargo build --release

# 检查代码
cargo check
```

## 第一个猜数游戏

```sh
cargo new guessing_game
```

```rs
use std::io;

fn main() {
    println!("猜数游戏！");
    
    let mut guess = String::new();
    io::stdin().read_line(&mut guess)
    .expect("fail to read line!");

    println!("input: {}", guess)
}
```

知识点：

1. 使用 `use` 引入包（crate）
2. 使用 `let` 声明变量
3. rust 中所有变量默认只读，使用 `mut` 关键字声明可写，传递给函数的指针也一样
4. 使用 `::` 调用关联函数，类似于静态方法
5. 输出占位符 `{}`

### 引入包 crate

1. 修改 Cargo.toml 的 dependencies 字段：

```toml
[dependencies]
rand = "^0.8.4"
```

^ 表示选取兼容 0.8.4 版本的最新版本

## 基本语法

```rs
const MAX_LENGTH: u32 = 10_000
```

### 数据类型

标量类型：

* 整数类型 u8, i8, u16, i16, u32, i32, u64, i64, arch
* 浮点类型 f32, f64
* 布尔类型 true, false
* 字符类型 char `let c:char = 'z' // 4byte`

复合类型

* 元组：`let t: (i32, f64, u8) = (10, 23.5, 8)`
* 数组: `let a: [i32; 5] = [3; 5]`
