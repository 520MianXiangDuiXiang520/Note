(include "./1-17.scm")
(include "../public/math.scm")

(define (muti a b)
    (muti-iter a b 0))

(define (muti-iter a b x)
    (cond ((= b 0) x)
          ((= 0 (% b 2)) (muti-iter (double a) (halve b) x))
          (else (muti-iter a (- b 1) (+ a x)))))

(muti 3 7)