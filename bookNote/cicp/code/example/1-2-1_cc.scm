(define (count-change amount)
    
    (cc amount 5))

(define (cc amount kinds-of-coins)
    (cond ((= 0 amount) 1)
          ((or (= 0 kinds-of-coins)
               (< amount 0)) 0)
          (else (+ (cc amount 
                      (- kinds-of-coins 1))
                 (cc (- amount 
                          (get-value-by-koc kinds-of-coins))
                      kinds-of-coins)))))

(define (get-value-by-koc koc)
    (cond ((= 1 koc) 1)
          ((= 2 koc) 5)
          ((= 3 koc) 10)
          ((= 4 koc) 25)
          ((= 5 koc) 50)))


(get-value-by-koc 5)
(cc 100 5)