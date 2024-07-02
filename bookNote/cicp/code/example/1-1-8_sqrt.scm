(define (sqrt x)
    (define (sqrt-iter guess x)
        (define (good-enough? guess x)
            (define (abs x)
                (if (> x 0) x (- 0 x)))

            (define (square x)
                (* x x))

            (< (abs (- (square guess) x)) 0.001))

        (define (improve a b) 
            (define (average x y)
                (/ (+ x y) 2))
            (average a (/ b a)))

        (if (good-enough? guess x)
            guess
            (sqrt-iter (improve guess x) 
                       x)))
    (sqrt-iter 1.0 x))

(sqrt 5)