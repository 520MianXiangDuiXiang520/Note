package main

import (
	"fmt"
	"os"
)

// test_env=t runtime_args a b c
// test_env=1 dlv debug . -- a b c
func main() { 
	fmt.Println("ENV: ", os.Getenv("test_env"))
	fmt.Println("Args: ", os.Args)
	p, _ := os.Executable()
	fmt.Println("Path: ", p)
}