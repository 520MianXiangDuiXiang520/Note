fn main() {
    let mut nums = vec![4, 2, 4, 0, 0, 3, 0, 5, 1, 0];
    move_zeroes(&mut nums);
    println!("{:?}", nums);
}

fn decompress_rl_elist(nums: Vec<i32>) -> Vec<i32> {
    let mut res: Vec<i32> = Vec::new();
    let size = nums.len();
    for i in (0..size).step_by(2) {
        let v = nums[i + 1];
        let n = nums[i];
        res.append(&mut [v].repeat(n as usize))
    }
    res
}

pub fn move_zeroes(nums: &mut Vec<i32>) {
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
            return;
        }
        nums[idx] = nums[not_zero_ptr];
        nums[not_zero_ptr] = 0;
        println!("{idx} {not_zero_ptr}, {:?}", nums);
    }
}
