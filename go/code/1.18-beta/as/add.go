package main

func demo(a int64, b int32, c int16, d int8, e, f, g, h, i, j int64) (int64, int32, int16, int8, int64,
    int64, int64, int64, int64, int64) {
    a += 111
    b += 222
    c += 333
    d += 89
    e += 99
    f += 88
    g += 999
    h += 898
    i += 989
    j += 787

    return a, b, c, d, e, f, g, h, i, j
}

func main() {
    demo(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
}
