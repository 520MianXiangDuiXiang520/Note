fn main() {
    let input = 0b11111111111111111111111111111101;
    let res = Solution::reverse_bits(input);
    println!("{res}");
    let exp = 0b10111111111111111111111111111111;
    if exp != res {
        println!("error")
    }
}

struct Solution {}

impl Solution {
    pub fn reverse_bits(x: u32) -> u32 {
        let mut res:u32 = 0;
        for i in 0..32 {
            let high = x >> i & 1;
            res |= high << (32 - i - 1);
        }
        res
    }
}
