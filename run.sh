#!/bin/bash

# Determine the installation directory based on the script's location
INSTALL_DIR="$(dirname "$(realpath "$0")")"

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

# Run git pull silently and overwrite local changes
echo -e "\e[90mChecking for updates...\e[0m"
GIT_PULL_LOG="/dev/null"
GIT_PULL_ERR="$HOME/.todos_git_pull_error.log"
git -C "$INSTALL_DIR" fetch --quiet 1>>"$GIT_PULL_LOG" 2>>"$GIT_PULL_ERR"
git -C "$INSTALL_DIR" reset --hard origin/main 1>>"$GIT_PULL_LOG" 2>>"$GIT_PULL_ERR"

# Reset executable permissions for run.sh and install.sh
chmod +x "$INSTALL_DIR/run.sh"
chmod +x "$INSTALL_DIR/install.sh"

# Run the application without changing directories
python3 "$INSTALL_DIR/main.py" "$@"
