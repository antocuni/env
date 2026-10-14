---
name: emacs
description: Use for any Emacs or Emacs-Lisp task in this user's setup, e.g. .emacs, elisp, keybindings, packages, modes, hooks, faces, or emacsclient. For persistent config changes, always edit the source AND apply the change to the running Emacs session.
---

# Emacs config workflow

## Where the config lives

- Main dotfile (git-tracked): `/home/antocuni/env/dotfiles/emacs`
  (`~/.emacs` is a symlink to it).
- Custom elisp (git-tracked): `/home/antocuni/env/elisp/*.el` (on `load-path`;
  some loaded via `load-file`, e.g. `myllm.el`).
- Edit these git-tracked sources. Do not create `/home/antocuni/.emacs.d/init.el`.

## Rule: always do BOTH steps

1. Edit the source file: the dotfile `/home/antocuni/env/dotfiles/emacs`, or the
   relevant `/home/antocuni/env/elisp/*.el` file.
2. Apply the same change live with `emacsclient`, without restarting Emacs.

Do not stop after editing the file. Do not only evaluate live without editing
the file. Both, every time.

## Scope of the two-step rule

The rule applies to **persistent config changes** (dotfile or elisp source).

For ad-hoc requests that do not change config, use `emacsclient` only and do not
edit any file:

- Open a file: `emacsclient -n /path/to/file`
- Run a one-off snippet: `emacsclient -e '(...)'`

## Step 1 - edit the dotfile

- Match the existing style: `;` line comments, `(setq ...)`,
  `(global-set-key ...)`, `(require ...)`.
- Keep parentheses balanced.

Validate syntax before applying:

```sh
emacs -Q --batch --eval '(progn (find-file "/home/antocuni/env/dotfiles/emacs") (emacs-lisp-mode) (check-parens))'
```

`check-parens` needs `emacs-lisp-mode` (the file has no `.el` extension), or it
reports false "unmatched bracket or quote" errors.

## Step 2 - apply live with emacsclient

Confirm a server is running:

```sh
emacsclient -e '(emacs-pid)'
```

If this fails with "can't find socket", there is no running session; tell the
user the change applies on next start, and stop.

Evaluate the changed top-level form(s) directly. Prefer only the new/changed
form, not the whole file:

```sh
emacsclient -e '(some-new-form)'
```

Several forms in one `progn`:

```sh
emacsclient -e '(progn (form-1) (form-2))'
```

Full reload as a fallback (re-runs the whole file, can trigger side effects):

```sh
emacsclient -e '(load-file "/home/antocuni/env/dotfiles/emacs")'
```

For a change in an elisp file under `~/env/elisp/`, reload that file (or
re-evaluate only the changed `defun`):

```sh
emacsclient -e '(load-file "/home/antocuni/env/elisp/foo.el")'
```

Caveats:

- Quote the elisp in single quotes so the shell does not expand it.
- `emacsclient -e` prints the return value on success and `*ERROR*: ...` on
  stderr with exit code 1. Always read the output.
- For a changed `defun`, re-evaluating the `defun` form redefines the function.
- For an already-bound variable, re-evaluate the `setq`/`defvar`.
- Do not restart Emacs; do not use `--kill`.

## Step 3 - verify

- Confirm `emacsclient` printed no `*ERROR*`.
- Report exactly what was applied so the user can try it immediately.
