#!/bin/bash

INSTALL_DIR="$HOME/.opt/derDere/todos"

# Run git pull silently
GIT_PULL_LOG="/dev/null"
GIT_PULL_ERR="$HOME/.todos_git_pull_error.log"
git -C "$INSTALL_DIR" pull --quiet 1>>"$GIT_PULL_LOG" 2>>"$GIT_PULL_ERR"

# Run the application without changing directories
python3 "$INSTALL_DIR/main.py" $@
