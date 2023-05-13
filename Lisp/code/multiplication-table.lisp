#!clisp

(defun my-format 
    (fmt lsp lsp-n)
)

(defun print-multiplication-table 
    (n z)
    (if 
        (> n z)
        (progn 
            (setf tmp z)
            (setf z n)
            (setf n tmp)
            (format t "n: ~A z:~A ~%" n z)))
    (do 
        (
            (i 1 
                (+ i 1))) 
        (
            (> i n) ) 
        (progn 
            (format t "~%")
            (do 
                (
                    (j i 
                        (+ j 1))) 
                (
                    (> j z)) 
                (format t "~A * ~A = ~2:@A  " i j 
                    (* i j))))))

(print-multiplication-table 9 9)