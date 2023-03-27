package main

import (
	"bytes"
	"fmt"
	"strings"
)

func mostCommonWord(paragraph string, banned []string) string {
	bannedMap := make(map[string]struct{}, len(banned))
	for _, s := range banned {
		bannedMap[s] = struct{}{}
	}
	maxV := -1
	res := ""
	resMap := make(map[string]uint8)
	paragraph = strings.ToLower(paragraph)
	word := bytes.NewBuffer([]byte{})
	for _, char := range paragraph {
		if char >= 'a' && char <= 'z' {
			word.WriteByte(byte(char))
		} else {
			if word.Len() > 0 {
				ws := word.String()
				if _, ok := bannedMap[ws]; !ok {
					n := int(resMap[ws])
					if n+1 > maxV {
						maxV = n + 1
						res = ws
					}
					resMap[ws]++
				}
				word.Reset()
			}

		}
	}
	if word.Len() > 0 {
		ws := word.String()
		if _, ok := bannedMap[ws]; !ok {
			n := int(resMap[ws])
			if n+1 > maxV {
				maxV = n + 1
				res = ws
			}
			resMap[ws]++
		}
	}
	return res
}

func main() {
	res := mostCommonWord("Bob. hIt, baLl", []string{"bob", "hit"})
	fmt.Println(res)
}
