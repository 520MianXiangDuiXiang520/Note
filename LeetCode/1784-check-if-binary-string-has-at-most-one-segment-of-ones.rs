fn main() {
    let input = String::from("1001");
    let res = Solution::check_ones_segment(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn check_ones_segment(s: String) -> bool {
        !s.contains("01")
    }
}
