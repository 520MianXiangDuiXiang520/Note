fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::sum_of_the_digits_of_harshad_number(18);
    assert_eq!(res, 9);
}

struct Solution {}

impl Solution {
    pub fn sum_of_the_digits_of_harshad_number(x: i32) -> i32 {
        let mut sum = 0_i32;
        let mut t = x;
        while t >= 10 {
            sum += x % 10;
            t /= 10;
        }
        sum += t;
        if x % sum == 0 {
            sum
        } else {
            -1
        }
    }
}