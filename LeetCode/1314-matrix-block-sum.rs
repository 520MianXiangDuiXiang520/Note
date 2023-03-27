fn main() {
    let nums = vec![1, 2, 3, 3];
    println!("{:?}", decompress_rl_elist(nums));
}

fn decompress_rl_elist(nums: Vec<i32>) -> Vec<i32> {
    let mut res:Vec<i32> = Vec::new();
    let size = nums.len();
    for i in (0..size).step_by(2) {
        let v = nums[i + 1];
        let n = nums[i];
        res.append(&mut [v].repeat(n as usize))
    }
    res
}