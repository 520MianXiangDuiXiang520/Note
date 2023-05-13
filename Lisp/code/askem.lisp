#!clisp

(defparameter *author* "JuneBoa")

(defun ask-number ()
    (format t "Plaese input a number: ")
    (let ((var (read)))
        (if (numberp var)
            var
            (ask-number))))

(format t "you number is ~A ~%" (+ (ask-number) 1))
(format t "~A~%" *author*)
(setf *author* "JuneBao")
(format t "~A~%" *author*)