(define (f n)
    (if (< n 3)
        n
        (+ (f (- n 1))
           (* 2 (f (- n 2)))
           (* 3 (f (- n 3))))))

(f 3)

(define (f-iter n idx a b c)
    (if (> idx n)
        a
        (f-iter n (+ idx 1)
                  (+ a 
                     (* 2 b)
                     (* 3 c))
                a b)))

(define (f2 n)
    (f-iter n 3 2 1 0))

(f2 3)

(= (f 10) (f2 10))

