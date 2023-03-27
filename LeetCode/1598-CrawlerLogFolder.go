package main

import "fmt"

func minOperations(logs []string) int {
    n := 0
    for _, log := range logs {
        if log == "./" {
            continue
        }
        if log == "../" {
            if n == 0 {
                continue
            }
            n --
        } else {
            n ++
        }
    }
    if n > 0 {
        return n
    }
    return 0-n
}



func main() {
	fmt.Println(minOperations([]string{"d1/","d2/","../","../","../","../","../","../","../","../","../","../","../","d21/","./"}))
}