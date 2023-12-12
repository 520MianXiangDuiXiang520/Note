(define (abs x)
  (if (> x 0)
        x
        (- 0 x)))

(define (square x)
  (* x x))

(define (<= x y)
    (or (< x y) (= x y)))

(define (>= x y)
    (or (> x y) (= x y)))

(define (!= x y)
    (not (= x y)))

;; x!
(define (factorial x)
    (define (fac-iter idx res)
        (if (> idx x)
            res
            (fac-iter (+ 1 idx) 
                      (* res idx))))
    (if (<= x 1)
        1
        (fac-iter 1 1)))

(define (% a b)
    (remainder a b))

(define (enev? x)
    (= 0 (% x 2)))