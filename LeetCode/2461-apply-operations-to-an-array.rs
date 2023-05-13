struct Solution {}

impl Solution {
    pub fn apply_operations(mut nums: Vec<i32>) -> Vec<i32> {
        for idx in 0..nums.len() - 1 {
            if nums[idx] == nums[idx + 1] {
                nums[idx] = 2 * nums[idx];
                nums[idx + 1] = 0;
            }
        }

        let mut not_zero_ptr: usize = 1;
        for idx in 0..nums.len() {
            if nums[idx] != 0 {
                not_zero_ptr += 1;
                continue;
            }
            let mut find = false;
            for nzp in not_zero_ptr..nums.len() {
                if nums[nzp] != 0 {
                    not_zero_ptr = nzp;
                    find = true;
                    break;
                }
            }
            if !find {
                return nums;
            }
            nums[idx] = nums[not_zero_ptr];
            nums[not_zero_ptr] = 0;
        }
        nums
    }
}

fn main() {
    let mut nums = vec![2, 2, 0];
    let s = Solution{};
    let res = Solution::apply_operations(nums);
    println!("{:?}", res);
}