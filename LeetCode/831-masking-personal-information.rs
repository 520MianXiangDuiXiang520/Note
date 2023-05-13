fn main() {
    let input = String::from("junebao@Junebbao.TOP");
    let res = Solution::mask_pii(input);
    println!("{res}");
}

struct Solution {}

impl Solution {
    pub fn mask_pii(s: String) -> String {
        const COUNTRY_CODE: [&str; 4] = ["", "+*-", "+**-", "+＊＊＊-"];
        match s.find("@") {
            None => {
               let numbers:String = s.matches(char::is_numeric).collect();
               let n = numbers.len();
               COUNTRY_CODE[n-10].to_string() + "***-***" + &numbers[n-4..]
            }
            Some(idx) => {
                s[0..1].to_lowercase() +"*****"+ &s[idx - 1..].to_lowercase()
            }
        }
    }
}
