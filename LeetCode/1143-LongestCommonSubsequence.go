package main

import (
	`fmt`
)

// 动态规划
// 1. 确定 dp 数组的含义：
//    - dp[i][j] 表示 text1[:i] 与 text2[:j] 的最长公共子序列
// 2. 划分子问题：
//    - 如要求 ac 和 babc 的 LCS, 可以划分成下面三种子问题：
//       1. 计算 a 和 bab 的 LCS, 要求的 ac 和 babc 可以看作 a 和 bab 分别拼接了 c
//          由于拼接的字符相等，所以 LCS(ac, babc) = LCS(a, bab) + 1;
//       2. 如果要拼接的字符不相等，如 ac 和 babd, 可以看作 a 和 bab 分别拼接了 c 和 d
//          由于拼接的字符串不相等，LCS(ac, babd) 应该等于两个字符串没有加 c 和 d 之前的 LCS 的最大值，即
//          LCS(ac, babd) = max(LCS(a, babd), LCS(ac, bab))
//    - 转换成状态转移方程：
//        dp[i][j] = dp[i-1][j-1] + 1              ; text1[i] == text2[j]
//        dp[i][j] = max(dp[i][j-1], dp[i-1][j])   ; text1[i] != text2[j]
// 2. 确定状态
//    - dp 数组最后一个元素表示 text1 和 text2 的最长公共子序列
// 3. 确定计算顺序
//    - 计算 dp[i][j] 需要知道它上面的，左面的和左上角的三个值，所以从上到下，从左到右

func printDP(dp [][]int) {
	for _, i := range dp {
		fmt.Println(i)
	}
	fmt.Println()
}

func longestCommonSubsequence(text1 string, text2 string) int {
	if len(text1) == 0 || len(text2) == 0 {
		return 0
	}
	dp := make([][]int, len(text1) + 1)
	for i := 0; i <= len(text1); i++ {
		dp[i] = make([]int, len(text2) + 1)
	}
	printDP(dp)
	for i := 1; i <= len(text1); i++ {
		for j := 1; j <= len(text2); j++ {
			if text1[i - 1] == text2[j - 1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i][j-1], dp[i-1][j])
			}
		}
		printDP(dp)
	}
	return dp[len(text1)][len(text2)]
}

func max(i, j int) int {
	if i > j {
		return i
	}
	return j
}

func main(){
	fmt.Println(longestCommonSubsequence("123459", "13578"))
}