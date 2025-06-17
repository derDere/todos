# PowerShell Installation Script for ToDo Application

$InstallDir = "$HOME\AppData\Local\derDere\todos"
$Symlink = "$HOME\AppData\Local\Microsoft\WindowsApps\todos.ps1"
$RepoUrl = "https://github.com/derDere/todos"

# Function to log errors locally
function Log-Error {
    param ([string]$Message)
    $ErrorLog = "$HOME\.todos_install_error.log"
    Add-Content -Path $ErrorLog -Value $Message
}

# Uninstall logic
if ($args[0] -eq "uninstall") {
    Write-Host "Uninstalling ToDo application..."
    if (Test-Path $InstallDir) {
        Remove-Item -Recurse -Force $InstallDir -ErrorAction Stop
    }
    if (Test-Path $Symlink) {
        Remove-Item -Force $Symlink -ErrorAction Stop
    }
    if (Test-Path "$HOME\.todos_install_error.log") {
        Remove-Item -Force "$HOME\.todos_install_error.log"
    }
    Write-Host "Uninstallation complete."
    exit 0
}

# Installation logic
# Check if Python and Git are installed
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}
if (-Not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

Write-Host "Installing ToDo application..."
if (-Not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -ErrorAction Stop
}

if (Test-Path "$InstallDir\.git") {
    Write-Host "Repository already cloned. Pulling latest changes..."
    git -C $InstallDir pull --quiet
} else {
    Write-Host "Cloning repository..."
    git clone $RepoUrl $InstallDir --quiet
}

# Create symlink
if (-Not (Test-Path "$HOME\AppData\Local\Microsoft\WindowsApps")) {
    New-Item -ItemType Directory -Path "$HOME\AppData\Local\Microsoft\WindowsApps" -ErrorAction Stop
}
Copy-Item -Path "$InstallDir\run.ps1" -Destination "$Symlink" -Force -ErrorAction Stop

Write-Host "Installation complete. You can now use the 'todos' command after restarting your terminal session."
