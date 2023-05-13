#!clisp

(defun size (lsp)
 (let ((i 0))
  (dolist (obj lsp) 
    (progn 
        (setf i (+ i 1))
        (format t "-- ~A~%" obj)))
  i))

(defun my-length (lsp)
    (if (null lsp)
        0
        (+ 1 (length (cdr lsp)))))

(format t "~A ~%" (size '(1 2 3 4)))

(format t "~A ~%" (my-length '(1 2 3 4)))