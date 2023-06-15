fn main() {
    let input: Vec<i32> = [3, 2, 4, 1, 5].to_vec();
    let res: i32 = Solution::num_times_all_blue(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn num_times_all_blue(flips: Vec<i32>) -> i32 {
        let (n, mut max, mut res) = (flips.len(), 0, 0);
        for idx in 0..flips.len() {
            max = max.max(flips[idx]);
            if max == (idx as i32 + 1) {
                res += 1;
            }
        }
        res
    }
}
