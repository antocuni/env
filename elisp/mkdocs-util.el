(defun mkdocs-link ()
  "Copy selected code as markdown code block with GitHub permalink.
The code is copied verbatim with proper formatting, line numbers,
and a link to the exact commit on GitHub."
  (interactive)
  (unless (use-region-p)
    (user-error "No region selected"))

  (let* ((file-path (buffer-file-name))
         (repo-root "/home/antocuni/anaconda/spy")
         (start-line (line-number-at-pos (region-beginning)))
         (end-line (line-number-at-pos (region-end)))
         (selected-text (buffer-substring-no-properties (region-beginning) (region-end)))
         (relative-path nil)
         (lang nil)
         (git-commit nil)
         (git-commit-short nil))

    (unless file-path
      (user-error "Buffer is not visiting a file"))

    ;; Make path relative to repo root
    (if (string-prefix-p repo-root file-path)
        (setq relative-path (substring file-path (1+ (length repo-root))))
      (user-error "File is not in repository: %s" file-path))

    ;; Get current git commit SHA
    (let ((default-directory repo-root))
      (setq git-commit (string-trim (shell-command-to-string "git rev-parse HEAD")))
      (setq git-commit-short (string-trim (shell-command-to-string "git rev-parse --short HEAD"))))

    ;; Detect language from file extension
    (setq lang (cond
                ((string-suffix-p ".py" file-path) "python")
                ((string-suffix-p ".js" file-path) "javascript")
                ((string-suffix-p ".ts" file-path) "typescript")
                ((string-suffix-p ".tsx" file-path) "typescript")
                ((string-suffix-p ".jsx" file-path) "javascript")
                ((string-suffix-p ".c" file-path) "c")
                ((string-suffix-p ".cpp" file-path) "cpp")
                ((string-suffix-p ".cc" file-path) "cpp")
                ((string-suffix-p ".h" file-path) "c")
                ((string-suffix-p ".hpp" file-path) "cpp")
                ((string-suffix-p ".rs" file-path) "rust")
                ((string-suffix-p ".go" file-path) "go")
                ((string-suffix-p ".java" file-path) "java")
                ((string-suffix-p ".md" file-path) "markdown")
                ((string-suffix-p ".yaml" file-path) "yaml")
                ((string-suffix-p ".yml" file-path) "yaml")
                ((string-suffix-p ".json" file-path) "json")
                ((string-suffix-p ".sh" file-path) "bash")
                (t "")))

    ;; Generate GitHub permalink
    (let* ((github-url (format "https://github.com/spylang/spy/blob/%s/%s#L%d-L%d"
                               git-commit relative-path start-line end-line))
           (title (format "%s @ %s" relative-path git-commit-short))
           (output (format "<div align=\"right\"><sub><a href=\"%s\">See on GitHub</a></sub></div>\n\n```%s title=\"%s\" linenums=\"%s\"\n%s\n```"
                           github-url
                           lang
                           title
                           start-line
                           selected-text)))

      ;; Copy to clipboard
      (kill-new output)
      (message "Copied code block with GitHub permalink (commit: %s)" git-commit-short))))
