fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::max_increase_keeping_skyline(vec![
        vec![3, 0, 8, 4], vec![2, 4, 5, 7], 
        vec![9, 2, 6, 3], vec![0, 3, 1, 0]
    ]);
    assert_eq!(res, 35);
}

struct Solution {}

impl Solution {
    pub fn max_increase_keeping_skyline(grid: Vec<Vec<i32>>) -> i32 {
        let n = grid.len();
        let mut row_max = vec![0;n];
        let mut line_max = vec![0;n];

        for x in 0..n {
            for y in 0..n {
                let item = grid[x][y];
                if item > row_max[x] {
                    row_max[x] = item;
                }
                if item > line_max[y] {
                    line_max[y] = item;
                }
            }
        }
        let mut res = 0_i32;
        for x in 0..n {
            for y in 0..n {
                res += row_max[x].min(line_max[y]) - grid[x][y];
            }
        }
        res
    }
}