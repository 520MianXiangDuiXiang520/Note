use std::io;
use rand::Rng;
use std::cmp::Ordering;
fn main() {
    println!("猜数游戏！");
    let magic_number = rand::thread_rng().gen_range(1..101);
    // println!("the magic number is: {}", magic_number);

    loop {
        let mut guess = String::new();
        io::stdin().read_line(&mut guess)
        .expect("fail to read line!");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("not a number: {}", guess);
                continue;
            }
        };
        // println!("input: {}", guess);
    
        match guess.cmp(&magic_number) {
            Ordering::Less => println!("too less!"),
            Ordering::Greater => println!("too more"),
            Ordering::Equal => {
                println!("Success!");
                break; 
            }
        }
    }
    
}