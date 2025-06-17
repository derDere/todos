#!/bin/bash

INSTALL_DIR="$HOME/.opt/derDere/todos"
SYMLINK="$HOME/.bin/todos"
REPO_URL="https://github.com/derDere/todos"

# Function to log errors locally
log_error() {
    echo "$1" >> "$HOME/.todos_install_error.log"
}

# Uninstall logic
if [ "$1" == "uninstall" ]; then
    echo "Uninstalling ToDo application..."
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR" || { log_error "Failed to remove $INSTALL_DIR"; echo "Error: Could not remove $INSTALL_DIR"; exit 1; }
    fi
    if [ -L "$SYMLINK" ]; then
        rm "$SYMLINK" || { log_error "Failed to remove symlink $SYMLINK"; echo "Error: Could not remove symlink $SYMLINK"; exit 1; }
    fi
    if [ -f "$HOME/.todos_install_error.log" ]; then
        rm "$HOME/.todos_install_error.log"
    fi
    echo "Uninstallation complete."
    exit 0
fi

# Installation logic
echo "Installing ToDo application..."
if [ ! -d "$INSTALL_DIR" ]; then
    mkdir -p "$INSTALL_DIR" || { log_error "Failed to create directory $INSTALL_DIR"; echo "Error: Could not create $INSTALL_DIR"; exit 1; }
fi

if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Repository already cloned. Pulling latest changes..."
    git -C "$INSTALL_DIR" pull --quiet || { log_error "Failed to pull latest changes in $INSTALL_DIR"; echo "Error: Could not update repository."; exit 1; }
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR" --quiet || { log_error "Failed to clone repository to $INSTALL_DIR"; echo "Error: Could not clone repository."; exit 1; }
fi

# Create symlink
if [ ! -d "$HOME/.bin" ]; then
    mkdir -p "$HOME/.bin" || { log_error "Failed to create $HOME/.bin directory"; echo "Error: Could not create $HOME/.bin directory"; exit 1; }
fi
if [ -L "$SYMLINK" ]; then
    rm "$SYMLINK" || { log_error "Failed to remove existing symlink $SYMLINK"; echo "Error: Could not update symlink."; exit 1; }
fi
ln -s "$INSTALL_DIR/run.sh" "$SYMLINK" || { log_error "Failed to create symlink $SYMLINK"; echo "Error: Could not create symlink."; exit 1; }

chmod +x "$INSTALL_DIR/run.sh"
chmod +x "$INSTALL_DIR/install.sh"

# Detect the user's shell and add $HOME/.bin to the appropriate configuration file
SHELL_NAME=$(basename "$SHELL")
CONFIG_FILE=""
case "$SHELL_NAME" in
    bash)
        CONFIG_FILE="$HOME/.bashrc"
        ;;
    zsh)
        CONFIG_FILE="$HOME/.zshrc"
        ;;
    fish)
        CONFIG_FILE="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo "Unsupported shell: $SHELL_NAME. Please add $HOME/.bin to your PATH manually."
        exit 1
        ;;
esac

if [[ -n "$CONFIG_FILE" && ":$PATH:" != *":$HOME/.bin:"* ]]; then
    echo "export PATH=\"$HOME/.bin:\$PATH\"" >> "$CONFIG_FILE"
fi

echo "Installation complete. You can now use the 'todos' command after restarting your terminal session."
