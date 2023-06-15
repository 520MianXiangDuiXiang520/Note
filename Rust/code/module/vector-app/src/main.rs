use vector_lib::vector::Vector;

fn main() {
    let p0 = Vector{
        x: 1.0,
        y: 0.0,
        z: 2.0,
    };
    let p1 = Vector{
        x: 2.0,
        y: 0.0,
        z: 3.0,
    };
    println!("{}", p0.add(&p1).string());
    println!("{}", p0.distance(&p1));
}
