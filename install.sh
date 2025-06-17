#!/bin/bash

INSTALL_DIR="/opt/derDere/todos"
SYMLINK="/usr/local/bin/todos"
REPO_URL="https://github.com/derDere/todos"

# Function to log errors to syslog
log_error() {
    logger -t todos-install "$1"
}

# Uninstall logic
if [ "$1" == "uninstall" ]; then
    echo "Uninstalling ToDo application..."
    if [ -d "$INSTALL_DIR" ]; then
        sudo rm -rf "$INSTALL_DIR" || { log_error "Failed to remove $INSTALL_DIR"; echo "Error: Could not remove $INSTALL_DIR"; exit 1; }
    fi
    if [ -L "$SYMLINK" ]; then
        sudo rm "$SYMLINK" || { log_error "Failed to remove symlink $SYMLINK"; echo "Error: Could not remove symlink $SYMLINK"; exit 1; }
    fi
    echo "Uninstallation complete."
    exit 0
fi

# Installation logic
echo "Installing ToDo application..."
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR" || { log_error "Failed to create directory $INSTALL_DIR"; echo "Error: Could not create $INSTALL_DIR"; exit 1; }
    sudo chown root:root "$INSTALL_DIR"
fi

if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Repository already cloned. Pulling latest changes..."
    sudo git -C "$INSTALL_DIR" pull --quiet || { log_error "Failed to pull latest changes in $INSTALL_DIR"; echo "Error: Could not update repository."; exit 1; }
else
    echo "Cloning repository..."
    sudo git clone "$REPO_URL" "$INSTALL_DIR" --quiet || { log_error "Failed to clone repository to $INSTALL_DIR"; echo "Error: Could not clone repository."; exit 1; }
fi

# Ensure the log file is writable by all users
sudo touch /var/log/todos_git_pull_error.log
sudo chmod 666 /var/log/todos_git_pull_error.log

# Adjust permissions to allow non-root users to perform git pull
sudo chown -R root:users "$INSTALL_DIR/.git"
sudo chmod -R g+rwX "$INSTALL_DIR/.git"
sudo find "$INSTALL_DIR/.git" -type d -exec chmod g+s {} \;

# Mark the installation directory as safe for Git
sudo -u "$SUDO_USER" git config --global --add safe.directory "$INSTALL_DIR"

# Install Python dependencies
sudo python3 -m pip install -r "$INSTALL_DIR/requirements.txt"

# Create symlink
if [ -L "$SYMLINK" ]; then
    sudo rm "$SYMLINK" || { log_error "Failed to remove existing symlink $SYMLINK"; echo "Error: Could not update symlink."; exit 1; }
fi
sudo ln -s "$INSTALL_DIR/run.sh" "$SYMLINK" || { log_error "Failed to create symlink $SYMLINK"; echo "Error: Could not create symlink."; exit 1; }

# Ensure both run.sh and install.sh scripts are executable
sudo chmod +x "$INSTALL_DIR/run.sh"
sudo chmod +x "$INSTALL_DIR/install.sh"

echo "Installation complete. You can now use the 'todos' command."
