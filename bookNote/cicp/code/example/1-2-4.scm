(load "../public/math.scm")

(define (expt b n)
    (if (= n 0)
        1
        (* b (expt b (- n 1)))))

(define (expt2 b n)
    (define (expt-iter res i)
        (if (= i n)
            res
            (expt-iter (* res b) 
                       (+ i 1))))
    (expt-iter b 1))

(define (fast-expt b n)
    (cond ((= n 0) 1)
        ((even? n) (square (fast-expt b (/ n 2))))
        (else (* b (fast-expt b (- n 1))))))

(define (fast-expt2 b n)
    (define (expt-iter t res i)
        (cond ((= 0 i) res)
            ((even? i) (expt-iter (square t) res (/ i 2))) 
            (else (expt-iter t (* t res) (- i 1)))))
    (expt-iter b 1 n))

(fast-expt2 2 10)
(= (expt 2 10) (expt2 2 10) (fast-expt 2 10) (fast-expt2 2 10))