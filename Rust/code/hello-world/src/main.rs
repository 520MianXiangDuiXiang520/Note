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


fn main() {
    let count = loop {
        break 1;
    };
    println!("{}", count);
}