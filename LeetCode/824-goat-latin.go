package main

import (
	"fmt"
	"strings"
)

func toGoatLatin(sentence string) string {
	res := ""
	index := 0
	start, end := 0, 0
	size := len(sentence)
	for end <= size {
		if end >= size || sentence[end] == ' ' {
			index++
			var v string
			sp := " "
			if end >= size {
				v = sentence[start:]
				sp = ""
			} else {
				v = sentence[start:end]
			}
			si := v[0]
			if !(si == 'a' || si == 'o' ||
			si == 'e' || si == 'i' || si == 'u'|| si == 'A' || si == 'O' ||
			si == 'E' || si == 'I' || si == 'U') {
				v = v[1:] + v[:1]
			}
			v += "ma"
			v = addAs(v, index)
			res += v + sp
			start = end +1
		}
		end ++
	}
	return res
}

func addAs(s string, n int) string {
	buf := strings.Builder{}
	buf.WriteString(s)
	for n > 0 {
		buf.WriteByte('a')
		n--
	}
	return buf.String()
}

func main() {
	fmt.Println(toGoatLatin("The quick brown fox jumped over the lazy dog"))
}
