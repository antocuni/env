(provide 'capnproto-mode)
(eval-when-compile
  (require 'generic-x))



(define-generic-mode 
  'capnproto-mode                   ;; name of the mode to create
  '("#") ;; comment
  '("using" "import" "struct" "union" "enum") ;; keywords
  '( ;; additional regexps
    (":[.a-zA-Z0-9()]\+" . font-lock-type-face)    ;; field type
    ("@0x[a-fA-F0-9]+" . font-lock-constant-face)  ;; file id
    ("$[^;()]+" . font-lock-function-name-face)    ;; annotations
    ("@[a-fA-F0-9]+" . font-lock-builtin-face)    ;; field id
    )
  '("\\.capnp$")
  nil
  "A mode for capnproto schema files")



;; debug helpers
;; (progn
;;   (switch-to-buffer-other-window "point.capnp")
;;   (capnproto-mode))

