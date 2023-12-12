;; s in [x, y]
;; z = s % m
;; 统计 z == p 的个数
(load "../public/math.scm")
(define (remaindef_n x y m p)
    (define (iter start res)
        (if (> start y)
            res
            (if (= p (% start m))
                (iter (+ start 1) (+ res 1))
                (iter (+ start 1) res))))
    (iter x 0))

(remaindef_n 10 19 3 1)
(remaindef_n 10 19 3 2)
(remaindef_n 10 19 3 0)