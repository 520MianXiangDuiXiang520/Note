fn main() {
    let input = 0b11111111111111111111111111111101;
    let res = Solution::hammingWeight(input);
    println!("{res}");
    let exp = 31;
    if exp != res {
        println!("error")
    }
}

struct Solution {}

impl Solution {
    pub fn hammingWeight (n: u32) -> i32 {
        let mut res = 0;
        for i in 0..32 {
            if (n >> i) & 1 == 1 {
                res = res + 1;
            }
        }
        res
    }
}
