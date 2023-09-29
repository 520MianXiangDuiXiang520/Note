fn main() {
    let input = String::from("658878000");
    let res = Solution::remove_trailing_zeros(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn remove_trailing_zeros(num: String) -> String {
        num.trim_end_matches('0').to_owned()
    }
}
