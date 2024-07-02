func new_array(n: Int64):Array<Int64> {
    return Array<Int64>(n, item: 0).clone()
}

main() {
    var l: Array<Array<Int64>> = Array(3, item: new_array(4))

    l[1][1] = 2

    for (line in l) {
        for (cell in line) {
            print("${cell} ")
        }
        println()
    }

    // output
    // 0 2 0 0 
    // 0 2 0 0 
    // 0 2 0 0 
}
