
fn main() {
    let i1: i64 = 10;
    let i2 = 10i64;

    // 元组
    let t = (3i32, false, 'c');


    let a1 = [1, 2, 3];

    // 定长数组
    let a2: [f64;2] = [1.1, 2.2];

    // 类似于 python a3=[1]*100
    let a3: [i32;100] = [1;100];
    let size = a3.len();
    println!("{}", size);
    greet_world();
}

fn greet_world() {
    let southern_germany = "Grüß Gott!";
    let chinese = "世界，你好";
    let english = "World, hello";
    let regions = [southern_germany, chinese,english];
    for region in regions.iter() {
        println!("{}", region);
    }
}
