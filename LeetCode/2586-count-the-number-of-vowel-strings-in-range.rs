fn main() {
    let strs = ["hey", "aeo", "mu", "ooo", "artro"];
    let mut input: Vec<String> = vec![];
    for ele in strs {
        input.push(String::from(ele));
    }
    let res: i32 = Solution::vowel_strings(input, 1, 4);
    println!("{res}")
}

struct Solution {}

impl Solution {
    pub fn vowel_strings(words: Vec<String>, left: i32, right: i32) -> i32 {
        let mut res: i32 = 0;
        let helper = |w: char| -> bool {
            match w {
                'a' | 'o' | 'e' | 'i' | 'u' => true,
                _ => false,
            }
        };
        for idx in left..right + 1 {
            let word = words[idx as usize].as_bytes();
            if helper(word[0] as char) && helper(word[word.len() - 1] as char) {
                res += 1;
            }
        }
        res
    }
}
