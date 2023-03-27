use std::convert::TryInto;

fn remove_duplicates(nums: &mut Vec<i32>) -> i32 {
    let size: i32 = (nums.len()) as i32;
    if size <= 1 {
        return size;
    }
    let mut pre = nums[0];
    let mut cur: usize = 1;
    let mut next: usize = 1;
    while next < nums.len() {
        if pre < nums[next] {
            cur += 1;
            pre = nums[next];
            next += 1;
            continue;
        }
        while next < nums.len() && pre >= nums[next] {
            next += 1;
        }
        if next >= nums.len() {
            return cur as i32;
        }
        nums[cur] = nums[next];
        nums[next] = pre;
        pre = nums[cur];
        cur += 1;
    }
    cur as i32
}

struct TestCase {
    nums: Vec<i32>,
    expect: Vec<i32>,
}

fn main() {
    let mut cases: Vec<TestCase> = Vec::new();
    cases.push(TestCase {
        nums: vec![1],
        expect: vec![1],
    });
    cases.push(TestCase {
        nums: vec![1, 1, 1],
        expect: vec![1],
    });
    cases.push(TestCase {
        nums: vec![1, 1, 1, 2],
        expect: vec![1, 2],
    });
    cases.push(TestCase {
        nums: vec![1, 1, 1, 2, 2, 3],
        expect: vec![1, 2, 3],
    });
    cases.push(TestCase {
        nums: vec![-1, 0, 1, 1, 1, 2],
        expect: vec![-1, 0, 1, 2],
    });
    cases.push(TestCase {
        nums: vec![-3, -3, -2, -1, -1, 0, 0, 0, 0, 0],
        expect: vec![-3, -2, -1, 0],
    });

    for item in cases.iter_mut() {
        run_case(&mut item.nums, &item.expect)
    }
    println!("PASS ALL")
}

fn run_case(nums: &mut Vec<i32>, expect: &Vec<i32>) {
    let length = remove_duplicates(nums);
    if length != expect.len().try_into().unwrap() {
        panic!("length want: {}, got: {}", expect.len(), length)
    }
    for (idx, item) in expect.iter().enumerate() {
        if *item != nums[idx] {
            panic!("want:{}, got: {}, idx: {}", *item, nums[idx], idx)
        }
    }
    println!("PASS: {:?}", nums);
}
