(define (psk i j)
    (if (or (= j 0) (= i j))
        1
        (+ (psk (- i 1) (- j 1))
           (psk (- i 1) j))))

        
(psk 0 0)
(psk 1 0)
(psk 1 1)
(psk 2 0)
(psk 2 1)
(psk 2 2)
(psk 4 2)

(load "../public/math.scm")

(define (psk2 i j)
    (/ (factorial i)
       (* (factorial j) 
          (factorial (- i j)))))

(psk2 4 2)