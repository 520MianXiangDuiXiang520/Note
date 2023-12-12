(include "../public/math.scm")
(define (gcd a b)
    (if (= 0 b)
        a
        (gcd b (% a b))))

(gcd 40 6)