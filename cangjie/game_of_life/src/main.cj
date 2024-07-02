from std import random.*
from std import time.*
from std import sync.*

foreign func system(fmt: CString, ...): Int32

struct Field {
    let width: Int64
    let height: Int64
    var cells: Array<Bool>

    public init(w: Int64, h: Int64) {
        this.width = w
        this.height = h
        this.cells = Array<Bool>(this.width * this.height, item: false)
    }

    public func rand_init() {
        for (_ in 0..this.cells.size/8) {
            let idx = Random().nextUInt32(UInt32(this.cells.size))
            this.cells[Int64(idx)] = true
        }
        // this.cells[this.get_pos(0, 2)] = true
        // this.cells[this.get_pos(1, 0)] = true
        // this.cells[this.get_pos(1, 2)] = true
        // this.cells[this.get_pos(2, 1)] = true
        // this.cells[this.get_pos(2, 2)] = true
    }

    func get_pos(i: Int64, j: Int64): Int64 {
        i * this.width + j
    }

    public func show() {
        for (i in 0..this.height) {
            for (j in 0..this.width) {
                let char = if (this.cells[this.get_pos(i, j)]) {
                    "●"
                } else {
                    " "
                }
                print("${char} ")
            }
            println()
        }
    }

    public func alive(i: Int64, j: Int64): Bool {
        var alive_num = 0

        for ( x in i - 1..i+2 where x >= 0 && x < this.height) {
            for (y in j - 1..j+2 where y >= 0 && y < this.width) {
                if (x == i && y == j) {
                    continue
                }
                if (this.cells[this.get_pos(x, y)]) {
                    alive_num++
                }
            }
        }
        // println("${i} ${j} ${alive_num} ")
        alive_num == 3 || (this.cells[this.get_pos(i, j)] && alive_num == 2)
    }

    public mut func set(i: Int64, j: Int64, s: Bool) {
        // println("${i} ${j} ${i*this.width +j} ${s}")
        this.cells[this.get_pos(i, j)] = s
    }
}

struct Map {
    public var width: Int64
    public var height: Int64
    var f1: Field
    var f2: Field

    public init(w: Int64, h: Int64) {
        this.width = w
        this.height = h
        this.f1 = Field(w, h)
        this.f2 = Field(w, h)
    }

    public func clear() {
        unsafe {
            var fmt = LibC.mallocCString("clear")
            system(fmt)
            LibC.free(fmt)
        }
    }

    public mut func update() {
        for (i in 0..this.height) {
            for (j in 0..this.width) {
                this.f2.set(i, j, this.f1.alive(i, j))
            }
        }
        (this.f1, this.f2) = (this.f2, this.f1)
    }
}

main() {
    var map = Map(90, 40)
    
    map.f1.rand_init()
    map.f1.show()
    for( _ in 0..20000) {
        sleep(100 * Duration.millisecond)
        map.update()
        map.clear()
        map.f1.show()
    }
}
