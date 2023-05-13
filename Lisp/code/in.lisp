#!clisp

# 判断 obj 是否在 lsp 中
(defun in (obj lsp)
    (if (null lsp)
        nil
        (if (eql (car lsp) obj)
            T
            (in obj (cdr lsp))
        )
    )
)

(pprint (in 3 '(1 2 3)))