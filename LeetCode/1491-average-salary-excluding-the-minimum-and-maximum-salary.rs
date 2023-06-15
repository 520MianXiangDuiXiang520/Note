fn main() {
    let input: Vec<i32> = [3, 2, 4, 1, 5].to_vec();
    let res: f64 = Solution::average(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn average(salary: Vec<i32>) -> f64 {
        let n = salary.len();
        let mut total: i32 = 0;
        let (mut min, mut max) = (salary[0], 0);
        for idx in 0..n {
            let elem = salary[idx];
            min = min.min(elem);
            max = max.max(elem);
            total += elem;
        }
        total -= min;
        total -= max;
        print!("{total} {min} {max}");
        total as f64 / (n - 2) as f64
    }
}
