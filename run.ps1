# PowerShell Run Script for ToDo Application

# Determine the installation directory based on the script's location
$ScriptPath = "$HOME\AppData\Local\derDere\todos"

# Check for --uninstall option
if ($args[0] -eq "--uninstall") {
    Write-Host "Are you sure you want to uninstall the ToDo application? (y/n)"
    $Response = Read-Host
    if ($Response -eq "y" -or $Response -eq "Y") {
        & "$ScriptPath\install.ps1" uninstall
        Write-Host "Application uninstalled."
        exit 0
    } else {
        Write-Host "Uninstallation canceled."
        exit 0
    }
}

# Suppress git reset output and make 'Checking for updates...' gray
Write-Host "`e[90mChecking for updates...`e[0m"
try {
    git -C $ScriptPath fetch --quiet
    git -C $ScriptPath reset --hard origin/main > $null 2>&1
} catch {
    Write-Host "Error: Could not update repository."
}

# Run the application without changing directories
python "$ScriptPath\main.py" $args
