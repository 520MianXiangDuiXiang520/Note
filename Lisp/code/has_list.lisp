#!clisp

(defun has-lisp (lsp)
    (if (null lsp)
        nil
        (if (listp (car lsp))
            T
            (has-lisp (cdr lsp)))))

(pprint (has-lisp '(1 2 3 '(1))))