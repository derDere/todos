#!/bin/bash

# Determine the installation directory based on the script's location
INSTALL_DIR="$(dirname "$(realpath "$0")")"

# Run git pull silently
GIT_PULL_LOG="/dev/null"
GIT_PULL_ERR="$HOME/.todos_git_pull_error.log"
git -C "$INSTALL_DIR" pull --quiet 1>>"$GIT_PULL_LOG" 2>>"$GIT_PULL_ERR"

# Check for --uninstall option
if [[ "$1" == "--uninstall" ]]; then
    echo "Are you sure you want to uninstall the ToDo application? (y/n)"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        "$INSTALL_DIR/install.sh" uninstall
        echo "Application uninstalled."
        exit 0
    else
        echo "Uninstallation canceled."
        exit 0
    fi
fi

# Run the application without changing directories
python3 "$INSTALL_DIR/main.py" "$@"
