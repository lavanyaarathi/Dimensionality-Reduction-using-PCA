# PowerShell setup script for PCA Project
Write-Host "Setting up PCA Project..." -ForegroundColor Green

Write-Host "`nSetting up Backend..." -ForegroundColor Yellow
Set-Location backend
Write-Host "Creating virtual environment..."
py -m venv venv
Write-Host "Activating virtual environment..."
& "venv\Scripts\Activate.ps1"
Write-Host "Installing Python dependencies..."
py -m pip install -r Requirements.txt
Set-Location ..

Write-Host "`nSetting up Frontend..." -ForegroundColor Yellow
Set-Location frontend
Write-Host "Installing Node.js dependencies..."
npm install
Set-Location ..

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nTo start the project, run: .\start_project.ps1" -ForegroundColor Cyan
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
