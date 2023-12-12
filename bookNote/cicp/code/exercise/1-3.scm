(define (max-sum a b c)
    (+ (if (> a b) a b) (if (> b c) b c)))

(max-sum 1 2 3)
(max-sum 3 1 2)