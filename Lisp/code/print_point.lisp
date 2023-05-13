#!clisp

(let ((n (read)))
    (
        do ((i 0 (+ i 1))) ((> i n) 'quit)
            (format t ".")
    )
)
    