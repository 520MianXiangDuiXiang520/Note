package main

import (
	"fmt"
	"reflect"
)

type A struct{
	N1 string
	N2 string
}

func (a *A) NamePtr() {}

func (a A) Name() {}

func main() {
	aP := &A{}
	aPt := reflect.TypeOf(aP)
	fmt.Println(aPt.NumMethod()) // 2
	n1, ok := aPt.MethodByName("NamePtr")
	fmt.Println(n1, ok) // {NamePtr  func(*main.A) <func(*main.A) Value> 1} true
	n2, ok2 := aPt.MethodByName("Name")
	fmt.Println(n2, ok2) // {Name  func(*main.A) <func(*main.A) Value> 0} true
	// fmt.Println(aPt.NumField())  // panic: reflect: NumField of non-struct type *main.A
	// f, fok := aPt.FieldByName("N1")  // panic: reflect: NumField of non-struct type *main.A
	// fmt.Println(f, fok)
	aPE := aPt.Elem()
	fmt.Println(aPE.NumField())  // 2
	f3, fok3 := aPE.FieldByName("N1")
	fmt.Println(f3, fok3)  // {N1  string  0 [0] false} true

	a := A{}
	at := reflect.TypeOf(a)
	fmt.Println(at.NumMethod()) // 1
	n3, ok3 := at.MethodByName("NamePtr")
	fmt.Println(n3, ok3)  // {  <nil> <invalid Value> 0} false
	n4, ok4 := at.MethodByName("Name")
	fmt.Println(n4, ok4)  // {Name  func(main.A) <func(main.A) Value> 0} true
	fmt.Println(at.NumField())  // 2
	f2, fok2 := at.FieldByName("N1")  
	fmt.Println(f2, fok2)  // {N1  string  0 [0] false} true
}
