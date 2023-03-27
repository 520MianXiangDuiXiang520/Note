package main

import (
	"fmt"
	"strings"
)

func lengthLongestPath(input string) int {
	lengths := make([]int, 0, 5)
	level := 0
	res := 0
	start, end := 0, 0
	for i := 0; i < len(input); i++ {
		if input[i] == '\n' || (end + 1)== len(input){
			if (end + 1)== len(input) {
				end = end + 1
			}
			n := 0
			lPath := end - start
			j := start
			for ; j < end; j++ {
				if input[j] != '\t' {
					break
				}
				n++
			}
			if n <= level {
				l := len(lengths) - (level - n) - 1
				if l < 0 {
					lengths = lengths[:0]
				} else {
					lengths = lengths[:l]
				}

			}
			level = n
			thisLen := lPath - j + start

			if strings.Contains(input[start:end], ".") {
				total := 0
				for _, v := range lengths {
					total += v
				}
				total += thisLen
				if total > res {
					res = total
				}
			} else {
				thisLen += 1
			}
			lengths = append(lengths, thisLen)
			start = i + 1
		}
		end ++
	}
	return res
}

func main() {
	fmt.Println(lengthLongestPath(""))
	fmt.Println(lengthLongestPath("dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"))
	fmt.Println(lengthLongestPath("file1.txt\nfile2.txt\nlongfile.txt"))
}
