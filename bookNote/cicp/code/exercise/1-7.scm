(load "../example/1-1-7_sqrt.scm")

(define (enough-good? guess x)
    (< (abs (- guess (improve guess x))) 0.0001))

(square (sqrt 5))