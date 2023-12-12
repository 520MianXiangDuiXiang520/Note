(include "../public/math.scm")
(define (double x)
    (+ x x))

(define (halve x)
    (/ x 2))

(define (fast-muti x y)
    (cond ((= y 0) 0)
        ((= (% y 2) 0) 
         (double (fast-muti x (halve y))))
        (else (+ x 
              (fast-muti x (- y 1))))))

(fast-muti 3 7)