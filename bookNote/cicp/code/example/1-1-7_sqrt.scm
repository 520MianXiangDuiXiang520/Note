(load "../public/math.scm")
(define (sqrt-iter guess x)
    (if (enough-good? guess x)
        guess
        (sqrt-iter (improve guess x) x)))

(define (improve guess x)
    (average (/ x guess) guess))

(define (average x y)
    (/ (+ x y) 2))

(define (enough-good? guess x)
    (< (abs (- (square guess) x)) 0.0001))

(define (sqrt x)
    (sqrt-iter 1.0 x))

(sqrt 4)
(sqrt 3)
(sqrt 0.00009)