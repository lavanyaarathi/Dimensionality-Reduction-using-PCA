# PowerShell start script for PCA Project
Write-Host "Starting PCA Project..." -ForegroundColor Green

Write-Host "`nStarting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project\backend'; & 'venv\Scripts\Activate.ps1'; py app.py"

Write-Host "`nWaiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`nStarting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Personal\Sarayu\NITK Surathkal\5th Semester\Software Engineering\pca-project\frontend'; npm start"

Write-Host "`nBoth servers are starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
