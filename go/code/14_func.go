package main

type A struct {}

func (a *A) New() {
	return &A{}
}

func main() {
	var a *A

	if a == nil {
		a = a.New()
	}
}