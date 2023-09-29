fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::can_place_flowers(vec![1, 0, 0, 0, 0, 1], 2);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn can_place_flowers(flowerbed: Vec<i32>, n: i32) -> bool {
        if n == 0 {
            return true;
        }
        let mut count = 0;
        let size = flowerbed.len();

        let mut i: usize = 0;
        while i < size {
            if flowerbed[i] == 1
                || (i > 0 && flowerbed[i - 1] == 1)
                || (i < size - 1 && flowerbed[i + 1] == 1)
            {
                i += 1;
                continue;
            }

            i += 2;
            count += 1;
            if count >= n {
                return true;
            }
        }

        false
    }
}
