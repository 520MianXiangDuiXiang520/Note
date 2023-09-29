fn main() {
    let input = vec![vec![1, 3], vec![3, 3], vec![5, 3], vec![2, 2]];
    let que = vec![vec![2, 3, 1], vec![4, 3, 1], vec![1, 1, 2]];
    let res = Solution::count_points(input, que);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn count_points(points: Vec<Vec<i32>>, queries: Vec<Vec<i32>>) -> Vec<i32> {
        queries
            .iter()
            .map(|x: &Vec<i32>| {
                points
                    .iter()
                    .filter(|p: &&Vec<i32>| (p[0] - x[0]).pow(2) + (p[1] - x[1]).pow(2) <= x[2] * x[2])
                    .count() as i32
            })
            .collect()
    }
}
