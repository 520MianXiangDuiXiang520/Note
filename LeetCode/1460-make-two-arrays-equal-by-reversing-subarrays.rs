use std::collections::HashMap;

fn main() {
    let input = vec![1, 2, 3,4];
    let arr = vec![4, 2, 3, 1];
    let res: bool = Solution::can_be_equal(input, arr);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn can_be_equal(target: Vec<i32>, arr: Vec<i32>) -> bool {
        let size = target.len();
        if size != arr.len() {
            return false;
        }
        let mut dict: HashMap<i32, i32> = HashMap::new();
        for idx in 0..size {
            let v1 = dict.entry(target[idx]).or_insert(0);
            *v1 +=1;
            let v2 = dict.entry(arr[idx]).or_insert(0);
            *v2 -= 1;
            if v2.abs() > (size - idx) as i32 {
                return false;
            }
        }
        for ele in dict.values() {
            if *ele != 0 {
                return false;
            }
        }
        true
    }
}
