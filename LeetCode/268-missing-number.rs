fn main() {
    let input = vec![3, 0, 1];
    let res = Solution::missing_number(input);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn missing_number(nums: Vec<i32>) -> i32 {
        let n: i32 = nums.len() as i32;
        (1 + n) * n / 2 - nums.iter().sum::<i32>()
    }
}
