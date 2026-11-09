Prefer ASD-STE100 Simplified Technical English

For persistent Emacs config changes: always edit the source under ~/env
(dotfiles/emacs or elisp/*.el) AND apply the change to the running session with
emacsclient. See the `emacs` skill.

Do not use pytest-xdist (`-n`, `--numprocesses`, `-n auto`). It makes the machine
unusable. Run tests in one process. To go faster, run fewer tests.

NEVER run processes in the background. Do not use the `background_process` tool. Do
not use `&`, `nohup`, `setsid`, `disown` or any similar method in the shell. Run all
commands in the foreground, so that the user can interrupt them easily. If a command
is too slow, run fewer tests or split the work into smaller commands.
