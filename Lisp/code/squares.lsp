#!clisp

(defun println 
    (str)
    (format t "~A~%" str))

(defun squares 
    (start end) 
    (
do
        (
            (i start 
                (+ i 1))) 
        (
            (> i end) 'done) 
        (
formatt"~A -> ~A~%"i
            (* i i)
)
)
)

(defun squares-func 
    (start end)
    (if 
        (> start end)
'done
        (progn 
            (format t "~A -> ~A~%" start 
                (* start start))
            (squares-func 
                (+ start 1) end))))

(squares 2 8)
(println "-----------")
(squares-func 2 8)