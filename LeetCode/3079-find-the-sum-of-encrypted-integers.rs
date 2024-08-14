
fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::sum_of_encrypted_int2(vec![1, 2, 3]);
    assert_eq!(res, 1 + 2 + 3);

    let res = Solution::sum_of_encrypted_int2(vec![198, 22, 3]);
    assert_eq!(res, 999 + 22 + 3);
}

struct Solution {}

impl Solution {
    pub fn encrypt(mut num:  i32) -> i32 {
        if num < 10 {
            return num;
        }

        let mut max = -1i32;
        let mut n = 0;
        while num > 0 {
            let x1 = num % 10;
            if x1 > max {
                max = x1;
            }
            num = (num - x1) / 10;
            n+=1;
        }
        let mut res = 0;
        for i in 0..n {
            res += max * (10_i32.pow(i))
        }
        res
    }
    pub fn sum_of_encrypted_int(nums: Vec<i32>) -> i32 {
        let mut res = 0;
        for num in nums {
            res += Solution::encrypt(num);
        }
        res
    }

    pub fn sum_of_encrypted_int2(nums: Vec<i32>) -> i32 {
        let mut res = 0;
        for mut num in nums {
            let  (mut max_num, mut base) = (0, 0);
            while num > 0 {
                max_num = max_num.max(num % 10);
                base = base * 10 + 1; 
                num /= 10;
            }
            res += base * max_num;
        }

        res
    }
}