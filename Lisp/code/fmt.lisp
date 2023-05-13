#!clisp

(defun println (str)
 (format t "~A~%" str))

(defun printf (str lsp)
    (apply #'format t str lsp))

(printf "ZJB ~A ~A ~%" '(1 2))