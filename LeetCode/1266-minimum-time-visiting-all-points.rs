fn main() {
    let input = vec![vec![1, 1], vec![3, 4], vec![-1, 0]];
    let res = Solution::min_time_to_visit_all_points2(input);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn min_time_to_visit_all_points(points: Vec<Vec<i32>>) -> i32 {
        let mut res = 0;
        let size = points.len();
        for idx in 0..size - 1 {
            let p0 = &points[idx];
            let p1 = &points[idx + 1];
            res += (p0[0] - p1[0]).abs().max((p0[1] - p1[1]).abs())
        }
        res
    }

    pub fn min_time_to_visit_all_points2(points: Vec<Vec<i32>>) -> i32 {
        points
            .windows(2)
            .map(|x| (x[0][0] - x[1][0]).abs().max((x[0][1] - x[1][1]).abs()))
            .sum()
    }
}
