mod opmap;
mod util {
    pub mod vector;
}

fn main() {
    println!("{MAX_LENGTH }");
    let num = "22";
    // 必须标注
    let num: u32 = num.parse().expect("not a number");
    println!("{num}");

    // 整数溢出
    // debug 模式下会 panic release 模式下会 循环

    // 元组
    let t = (12, "12", true);
    let a = t.0;
    let b = t.1;
    let c = t.2;
    let (w1, w2, w3) = t; // 元组解构
    println!("{a} {b} {c} {w1} {w2} {w3}");

    // 数组
    let a:[i32; 3] = [1, 2, 34]; // 数组在栈上
    let a = [1;5];
    println!("{}", a[2]);

    // 函数
    my_fun();
    let sum = add(5, 8);
    test();
    println!("{sum}");

    // if 是表达式
    let s:&str = if sum == 0 { "is zero" } else { "not zero" };
    println!("{}", s);

    // loop, for, while 循环
    let mut s = 1;
    loop {
        if s > 10 {
            break;
        }
        s += 1; 
    }

    for item in a.iter() {
        println!("{}", item);
    }

    class_4_scope();

    struct_demo();

    enum_demo2();

    call_map();
    call_ln();

}


fn my_fun() {
    println!("other func")
}

fn add(x: i32, y: i32) -> i32 {
    return x + y;
}

fn test() -> usize {
    // 要区分语句和表达式
    // 语句 ； 结尾
    let s = "ppp";

    let x = 1;
    let y = {
        let x = x + 1 ;
        x + 2
    };
    println!("{y}");

    // 函数可以以一个表达式结束，作为返回值，如
    s.len()
}

const MAX_LENGTH: i8 = 8;


fn class_4_scope() {
    let mut s = String::from("Hello");
    s.push_str(" World");
    println!("{}", s);

    // 变量走出作用域时 rust 调用 drop 函数清理内存
    // 变量与数据交互的方式：
    //  1. Move: 
    let x = 5;
    let y = x;
    println!("{}, {}", x, y); // x y 都是简单数据类型，在栈上分配，所以都可以使用，

    let s2 = s;
    // println!("{}", s); // s2 借用了 s，这里 s 已经失效，不能使用了
    println!("{}", s2);

    let s3 = s2.clone();
    println!("{} {}", s2, s3); // clone 克隆整个堆内存后就变量是可用的。

    // 限制的原因是主要是避免重复释放
    // 实现了 copy trait 在被借用后就是可以继续用的
    // 实现了 drop trait 在被借用后就不能用了
    // 两个不能同时实现

    // 函数穿参同样会发生移动和复制
    class_4_scope_fn(s3);
    // 这里 s3 已经失效
    // println!("{}", s3); ERROR

    /////////////// 所有权与函数 ///////////////
    let mut str = String::from("Hello World");
    let first = first_word(&str); // 不可变借用，所有权返回给了调用者
    println!("{}", first);
    str.clear(); // 可变借用
    // println!("{}", first); // 这里 first 的声明周期还没有结束，不可变借用还存在，所以上一行会报错，不能同时持有可变借用和不可变借用
}

fn first_word(s: &String) -> &str {
    for (i, &word) in s.as_bytes().iter().enumerate() {
        if word == b' ' {
            return &s[..i]
        }
    }
    &s[..]
}

fn class_4_scope_fn(s: String) {
    println!("{}", s)
}

#[derive(Debug)] // 派生自 Debug
struct Vector {
    x: f64,
    y: f64,
    z: f64,
}

fn struct_demo() {
    let mut pos = Vector{
        y: 2.0,
        x: 3.0,
        z: 1.0,
    }; // 所以字段必须都赋值
    // struct 一点被声明是可变的，那结构体中所有字段都是可变的
    println!("{:?}", pos);
    // 字段出事化简写
    let x = 3.7;
    let pos2 = Vector{
        x,
        ..pos
    };

    // tuple struct
    // 整体有名，里面的元素没有名
    struct RGB(i32, i32, i32);
    let black = RGB(255,255,255);

    // unit like struct
    // 没任何字段的 struct
    struct Empty {};

    let s = pos.Add(&pos2);
    println!("{:#?}", s);

    let t = Vector::new(1.0, 2.0, 3.0);
}

// 方法
impl Vector {
    fn Add(&self, p: &Vector)-> Vector {
        Vector { x: self.x + p.x, y: self.y + p.y, z: self.z + p.z }
    }

    // 关联方法，第一个参数不是 self 
    fn new(x: f64, y: f64, z: f64) -> Vector {
        Vector { x, y, z }
    }
}

// 枚举
enum IpAddrKind {
    V4, // 变体
    V6,
}

fn enum_demo(kind: IpAddrKind) {
    let v4 = IpAddrKind::V4;
}

// 枚举允许数据附加到枚举的变体中
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

impl IpAddr {
    fn str(&self) -> String {
        match self {
            IpAddr::V4(a,b ,c,d ) => {
                 format!("{}.{}.{}.{}", a, b, c, d)
            }
            IpAddr::V6(s) => s.to_string(),
        }
    }
}

fn enum_demo2() {
    let v4 = IpAddr::V4(127, 0, 0, 1);
    let v6 = IpAddr::V6(String::from("::1"));
    println!("{}", v4.str());
    println!("{}", v6.str());
}

// option 枚举
fn option_demo() {
    let v = Some(3);
    let i = match v {
        None => 0,
        Some(1) => 1,
        _ => -1,
    };

    let idx: i32 = 8;
    let j: i32 = match idx {
        8 => 9,
        _ => 0,
    };

    let v = Some(0i32);
    if let Some(3) = v {
        println!("three");
    } else {
        println!("others")
    };
}

/*
Rust 模块系统
  Package
  Crate 单元包
    binary
    libary
  Module 模块
  Path
 */

use crate::opmap::OpMap;

fn call_map() {
    let map_name = String::from("Normal_Map_S1");
    let mut opmap:OpMap = OpMap::new_normal_map(&map_name);
    opmap.init_map();
    println!("{}, {:#?}", opmap.no_ghost(), opmap)
}

use crate::util::vector::Vector as OtherVector;

fn call_ln() {
    let p1 = OtherVector{x:1.0, y:2.0, z:3.0};
    println!("{}", p1.length())
}