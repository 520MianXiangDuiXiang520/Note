impl Solution {
    pub fn find_ocurrences(text: String, first: String, second: String) -> Vec<String> {
        let mut ret = Vec::new();
        let list:  Vec<&str> = text.split_whitespace().collect();
        if list.len() < 3 {
            return ret
        }
        for i in (0..list.len()-2) {
            if list[i] == first && list[i+1] == second {
                ret.push(list[i+2].to_string())
            }
        }
        return ret
    }
}
