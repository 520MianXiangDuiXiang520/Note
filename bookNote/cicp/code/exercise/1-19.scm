(include "../public/math.scm")
(define (fast-fbi n)
    (fib-iter 1 0 0 1 n))

(define (fib-iter a b p q count)
    (cond ((= count 0) b)
        ((= 0 (% count 2)) 
         (fib-iter a 
                   b 
                   (+ (square p) (square q))
                   (+ (* 2 p q) (square q))
                   (/ count 2))) 
        (else (fib-iter (+ (* b q)
                           (* a (+ p q)))
                        (+ (* b p)
                           (* a q))
                        p
                        q
                        (- count 1)))))

(fast-fbi 10)