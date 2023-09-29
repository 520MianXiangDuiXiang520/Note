fn main() {
    
    let res = Solution::count_odds(3, 8);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn count_odds(low: i32, high: i32) -> i32 {
        (low & 1) + (high & 1) + (high - low) >> 1
    }
}
