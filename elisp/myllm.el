;; small emacs function to call myllm

(defun myllm (arg)
  "Process the current region or line through the myllm command.
If no region is active, use the current line instead.
With prefix argument ARG (C-u), replace the region/line with the result.
Otherwise, insert the result after the region/line."

  (interactive "P")
  (let* ((use-line (not (region-active-p)))
         (begin (if use-line (line-beginning-position) (region-beginning)))
         (end (if use-line (line-end-position) (region-end)))
         (buffer (current-buffer))
         (result-buffer (generate-new-buffer "*myllm-output*"))
         (command "myllm")
         (args nil))
    (unwind-protect
        (progn
          (apply 'call-process-region begin end command nil result-buffer nil args)
          (with-current-buffer result-buffer
            (let ((output (buffer-string)))
              (with-current-buffer buffer
                (if arg
                    ;; Replace the region/line with the output
                    (save-excursion
                      (delete-region begin end)
                      (goto-char begin)
                      (insert output))
                  ;; Insert after the region/line
                  (save-excursion
                    (goto-char end)
                    (insert "\n" output)))))))
      (kill-buffer result-buffer))))

(global-set-key (kbd "C-x C-<return>") 'myllm)
