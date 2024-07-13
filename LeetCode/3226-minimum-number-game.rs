fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::number_game(vec![5, 4, 2, 3]);
    assert_eq!(res, vec![3, 2, 5,4]);
}

struct Solution {}

impl Solution {
    pub fn number_game(mut nums:Vec<i32>) -> Vec<i32> {
        nums.sort();
        for i in (0..nums.len()-1).step_by(2) {
            nums.swap(i, i+1)
        }
        nums
    }
}