package main

func demo(a int64, b int32, c int16, d int8) (int64, int32, int16, int8) {
	a += 111
	b += 222
	c += 333
	d += 89
	return a, b, c, d
}

func main() {
	demo(0, 0, 0, 0)
}