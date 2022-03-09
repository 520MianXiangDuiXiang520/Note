package main

import (
	"encoding/json"
	"fmt"
)

type A struct {
	Name string
}

type A1 struct {
	A
}

type B struct {
	Name string
}


type C struct {
	A1
	B
}

// https://golang.org/ref/spec#Selectors

func main() {
	c := C{}
	c.A1.A.Name = "A1"
	c.B.Name = "B2"
	b, _ := json.Marshal(c)

	fmt.Println(string(b)) // {"Name":"B2"}
	fmt.Println(c.Name) // B2
}