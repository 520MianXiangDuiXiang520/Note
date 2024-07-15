
fn main() {
    // let res = Solution::repair_cars(vec![3,3,1,2,1,1,3,2,1], 58);
    // let res = Solution::repair_cars(vec![4, 2, 3, 1], 10);
    let res = Solution::find_intersection_values(vec![4,3,2,3,1], vec![2,2,5,2,3,6]);
    assert_eq!(res, vec![3, 4]);
}

struct Solution {}

impl Solution {
    fn contains<T>(x: &T, nums1: &Vec<T>) -> bool 
    where T: std::cmp::Ord{
        for t in nums1.iter() {
            if t == x {
                return true;
            }
        }
        false
    }
    pub fn find_intersection_values(nums1: Vec<i32>, nums2: Vec<i32>) -> Vec<i32> {
        let x1 = nums1.iter().filter(|&x| Solution::contains(x, &nums2)).count() as i32;
        let x2 = nums2.iter().filter(|&x| Solution::contains(x, &nums1)).count() as i32;

        vec![x1, x2]
        
    }
}