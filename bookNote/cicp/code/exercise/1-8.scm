(load "../public/math.scm")

;;立方根
(define (cube x)
    (define (cube-iter guess x)
        
        ;; 近似值估算
        (define (imprive guess)
            (/ (+ (/ x (square guess)) 
                  (* 2 guess)) 
                  3))

        (let ((new-guess (imprive guess))) 
            (define (good-enough? old-guess)
                (< (abs (- old-guess new-guess)) 0.0001))

            (if (good-enough? guess)
                guess
                (cube-iter (imprive guess) x)))
        )
    (cube-iter 1.0 x))

(cube 27)