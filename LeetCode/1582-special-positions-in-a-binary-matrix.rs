fn main() {
    
    let res = Solution::num_special(vec![
        vec![1,0,0],
        vec![0,0,1],
        vec![1,0,0],
    ]);
    println!("{:?}", res)
}

struct Solution {}

impl Solution {
    pub fn num_special(mat: Vec<Vec<i32>>) -> i32 {
        
        let mut res: i32 = 0;
        
        let lines: Vec<i32> = mat.iter().map(|line: &Vec<i32>| line.iter().sum::<i32>()).collect::<Vec<_>>();
        let rows: Vec<i32> = (0..mat[0].len()).map(|idx| mat.iter().map(move |line| line[idx])).map(|x| x.sum::<i32>()).collect();

        for i in 0..mat.len() {
            for j in 0..mat[0].len() {
                if mat[i][j] == 1 && lines[i] == 1 && rows[j] == 1{
                    res += 1;
                }
            }
        }

        res
    }
}
