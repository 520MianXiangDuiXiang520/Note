package main

import "fmt"

func isValid(s string) bool {
    if len(s) % 2 != 0 {
        return false
    }
    stack := make([]byte, 0)
    for _, b := range []byte(s) {
        if b == '[' || b == '(' || b == '{' {
            stack = append(stack, b)
        } else {
            top := len(stack)
            if top == 0 {
                return false
            }
            s := stack[top-1]
            switch s {
                case '(':
                    if b != ')' {
                        return false
                    }
                case '[':
                    if b != ']' {
                        return false
                    }
                case '{':
                    if b != '}' {
                        return false
                    }
            }
            stack = stack[:top-1]
        }
    }
    return len(stack) == 0
}

func main() {
	fmt.Println(isValid("(){}({}){{[]}}"))
}