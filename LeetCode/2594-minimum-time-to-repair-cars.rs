fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::repair_cars(vec![100], 1000000);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn repair_cars(ranks: Vec<i32>, cars: i32) -> i64 {
        let dc = cars as i64 * cars as i64;
        let mut max = ranks[0] as i64 * dc;
        if max < 0 {
            max = i64::MAX;
        }
        let mut min = 0i64;
        while min < max {
            let mid = (min + max) >> 1;

            // let num:i64 = ranks.iter().map(|r| Solution::get_cars_by_t(mid, *r)).sum();
            let mut num = 0i32;
            for rank in &ranks {
                num += ((mid as f64) / (*rank as f64)).sqrt().floor() as i32;
                if num >= cars {
                    break;
                }
            }

            if num < cars {
                min = mid + 1
            } else {
                max = mid
            }
        }
        min
    }
}
