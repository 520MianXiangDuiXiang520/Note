fn main() {
    let input: String = String::from("RLRRLLRLRL");
    let res: i32 = Solution::balanced_string_split(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn balanced_string_split(s: String) -> i32 {
        let mut res = 0;
        let mut balanced = 0;
        s.chars().for_each(|c| {
            match c {
                'L' => balanced += 1,
                _ => balanced -= 1,
            }
            if balanced == 0 {res += 1}
        });
        res
    }
}
