# PowerShell Run Script for ToDo Application

# Determine the installation directory based on the script's location
$ScriptPath = $MyInvocation.MyCommand.Path
$InstallDir = Split-Path -Parent $ScriptPath

# Check for --uninstall option
if ($args[0] -eq "--uninstall") {
    Write-Host "Are you sure you want to uninstall the ToDo application? (y/n)"
    $Response = Read-Host
    if ($Response -eq "y" -or $Response -eq "Y") {
        & "$InstallDir\install.ps1" uninstall
        Write-Host "Application uninstalled."
        exit 0
    } else {
        Write-Host "Uninstallation canceled."
        exit 0
    }
}

# Run git pull silently and overwrite local changes
Write-Host "Checking for updates..."
try {
    git -C $InstallDir fetch --quiet
    git -C $InstallDir reset --hard origin/main
} catch {
    Write-Host "Error: Could not update repository."
}

# Run the application without changing directories
python "$InstallDir\main.py" $args
