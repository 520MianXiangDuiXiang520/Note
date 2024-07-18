// fn main() {
//     let x = 1i32;
//     let x = 1f64;
//     println!("{}", x);
//     let mut x = true;
//     x = false;
//     assert_eq!(x, false);
// }

// const PLANCK_CONSTANT: f64 = 6.626E-34;

// struct Square {
//     id: i64,
// }

// fn main() {
//     println!("{}", PLANCK_CONSTANT);
//     let (mut x, y): (i32, f64) = (1, 1f64);
//     x += 1;
//     println!("x:{}, y:{}", x, y); // x:2, y:1

//     let (a, b, c, d, e);
//     (a, b) = (1, 2);
//     [c, .., d, _] = [1, 2, 3, 4, 5, 6, 7];
//     Square { id: e } = Square { id: 99 };
//     assert_eq!([a, b, c, d, e], [1, 2, 1, 6, 99]);
// }

// fn main() {
//     let v = {
//         let x = 1;
//         x + 2
//     };
//     assert_eq!(v, 3)
// }

// fn main() {
//     let x = i8::wrapping_add(127, 3);
//     println!("{}", x); // -126

//     let result = i8::checked_add(127, 3);
//     match result {
//         None => println!("overflowing!!"),
//         Some(x) => println!("{}", x)
//     }

//     let (x,y) = i8::overflowing_add(127, 3);
//     println!("{}, {}", x, y); // -126, true

//     let x = i8::saturating_add(127, 3);
//     println!("{}", x); // 127

//     let x = 16f64/0.0;
//     println!("{}", x);
// }

// fn main() {
//     println!("{}", (1.0/0.0f32).is_infinite());
//     println!("{}", (-1.0/0.0f32).is_infinite());
//     println!("{}", (0.0/0.0f32).is_nan());
// }

// fn main() {
//     let mut s = String::from("hello");
//     append_world(&mut s);
//     assert_eq!(str_len(&s), 12);
//     println!("{}", s);
// }

// fn str_len(s: &String) -> usize {
//     s.len()
// }

// fn append_world(s: &mut String) {
//     s.push_str(", world")
// }

// fn tt() {
//     let mut s = String::from("hello");
//     let _s1 = &mut s;
//     let _s2 = &s;
// }

// fn first_word(s: &String) ->&str {
//     &s[..1]
// }
// fn main() {
//     let mut  s = String::from("hello world");
//     let word = first_word(&s);
//     println!("{} {}", word, s);
//     s.clear();
// }

// fn array_exercise() {
//     let  list:[String;5] = std::array::from_fn(|_i| String::from("value"));
//     let  _list0:&[String] =  &list[0..3];
// println!("{:?}", list);
// list0.clear();
// println!("{}", list0);
// println!("{:?}", list);
// }

// fn array_exercise1() {
//     let list = [1, 1, 1, 1, 1];
//     let list2 = [1; 5];
//     assert_eq!(list, list2)
// }

// fn main() {
//     let x = 12;
//     let x = if x % 10 == 0 {
//         1
//     } else {
//         2
//     };
//     assert_eq!(x, 1)
// }

// fn main() {
//     let s = String::from("holla中国人नमस्ते");
//     for char in s.chars() {
//         println!("{char}");
//     }

//     let mut tup:(f64,i32,i16) =(1.0, 2, 3);
//     tup.0 = 2.0;
//     println!("{}", tup.0);
//     let (x,y,z) = tup;
//     println!("{}, {}, {}", x, y, z);

//     let _u: () = ();

//     let blog = Blog {
//         id: 1,
//         abs: "hello rust".to_string(),
//         tags: vec!["rust".to_string()]
//     };

//     println!("{}", blog.abs);
// }

// struct Blog {
//     id: u64,
//     abs: String,
//     tags: Vec<String>
// }

struct Empty;

// struct Vector(f64, f64, f64);

struct Pet {
    id: i32,
    pet_type: i32,
    level: u32,
}

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

struct Point<T, U> {
    x: T,
    y: U,
}

impl<T, U> Point<T, U> {
    // 实现 mixup，不要修改其它代码！
    fn mixup<X, Y>(self, o: Point<X, Y>) -> Point<T, Y> {
        Point { x: self.x, y: o.y }
    }
}

struct Square {
    id: i64,
}
struct Building {}

enum Order {
    Attack(Square),
    Demolition(Building),
    Reinforce(Building),
    Build(Building),
}

impl Order {
    fn is_hostile(&self) -> bool {
        match self {
            Order::Attack(_) | Order::Demolition(_) => true,
            _ => false,
        }
    }
}

struct RGB(u16, u16, u16);

impl RGB {
    fn to_hex(&self) -> String {
        format!("#{:02X}{:02X}{:02X}", self.0, self.1, self.2)
    }
}

// fn main() {
//     let red = RGB(215, 0, 58);
//     println!("{}", red.to_hex());

//     let _e = Empty;

//     let _p = Vector(1.0, 0.0, 1.0);

//     let mut pet1 = Pet::new(1, 1, 1);
//     pet1.upgrade();
//     assert_eq!(2, pet1.level);
//     let pet2 = Pet { id: 2, ..pet1 };
//     assert_eq!(pet2.id, 2);
// }

#[derive(Debug)]
struct Vector {
    x: f64,
    y: f64,
}

fn struct_test() {
    // 结构体解构
    let pos = Vector { x: 1.0, y: 2.0 };
    let Vector { x: a, y: b } = pos;
    assert_eq!(a, 1.0);
    assert_eq!(b, 2.0);

    let red = RGB(215, 0, 58);
    let RGB(r, g, b) = red;
    assert!(r == red.0 && g == red.1 && b == red.2);
}

enum OnlyOne {
    One(i32)
}

fn match_test() {
    let order = Order::Attack(Square { id: 1 });
    assert!(order.is_hostile());

    let u = Some(3);

    // matches 宏匹配表达式和模式
    assert!(matches!(u, Some(3)));

    let alphabets = ['a', 'E', 'Z', '0', 'x', '9', 'Y'];
    for ab in alphabets {
        assert!(matches!(ab, 'a'..='z' | 'A'..='Z' | '0'..='9'))
    }

    // 只处理一个选项时，可以使用 if let
    if let Some(v) = u {
        println!("{}", v)
    }

    // match 是一个表达式，可以用于变量赋值
    let boolean = true;
    let binary = match boolean {
        true => 1,
        false => 0,
    };
    assert_eq!(binary, 1);

    // let PATTERN = EXPRESSION
    let (_a, _b, _c) = (1, 2, 3); // 解构的元组
    let [_a, _b, _c] = [1, 2, 3]; // 解构的数组
    let Vector { x: _a, y: _b } = Vector { x: 1.0, y: 2.0 }; // 解构的结构体
    let ([_a, _b], _c) = ([1, 2], 3); // 组合
    let OnlyOne::One(_x) = OnlyOne::One(1); // 解构的枚举

    let x = Some(1);
    if let Some(_v) = x {}

    match x {
        Some(_) => println!("x"),
        _ => ()
    }

    // while let
    let mut stack = vec![1, 2, 3];
    while let Some(x) = stack.pop() {
        println!("{}", x)
    }

    // for 循环也有模式匹配
    for (i, v) in stack.iter().enumerate() {
        println!("{},{}", i, v)
    }

    fn foo((x, y):(i32, i32)) {
        println!("{}, {}", x, y);
    }
    foo((1, 2));

    let x = 1;
    match x {
        1 | 2 => println!("{}", x),
        _ => ()
    }

    match x {
        1..=5 => println!("{} in [1,5]", x),
        _ => ()
    }

    match x {
        1..=20 if x != 7 => println!("{} in [1,20] not 7", x),
        _ => ()
    }

    let pos = Vector{x: 1.0, y: 2.0};
    match pos {
        Vector{x: vx, y: 0.0} => println!("{}", vx),
        Vector{x: 0.0, y: vy} => println!("{}", vy),
        Vector{x: vx, y: vy} => println!("{} {}", vx, vy)
    }

    match pos {
        Vector{y: vy, ..} => println!("{}", vy),
        Vector{x: _, y: vy} => println!("{}", vy),
    }

    let array = [1_i32;20];
    match array {
        [x,..] => println!("first: {}", x),
        [.., x] => println!("last: {}", x)
    }

    let s = Some(1);
    match s {
        Some(tmp @ 0..=3) => println!("{}", tmp),
        _ => ()
    }

    match 1 {
        num @ (1 | 2) => println!("{}", num),
        _ => ()
    }

    if let num @ (1 | 2) = 1 {
        println!("{}", num)
    }

    let pos = Vector{x: 1.0, y: 2.0};
    if let p @ Vector{x: 1.0, ..} = pos {
        println!("match {:?}", p)
    } else {
        println!("unmatch")
    }

}

fn main() {
    struct_test();

    match_test();

    let p1 = Point { x: 5, y: 10 };
    let p2 = Point {
        x: "Hello",
        y: '中',
    };

    let p3 = p1.mixup(p2);

    assert_eq!(p3.x, 5);
    assert_eq!(p3.y, '中');
}
