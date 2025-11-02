# Docker DNS Fix Script
# This script helps configure Docker Desktop DNS settings

Write-Host "=== Docker DNS Configuration Fix ===" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Desktop is running
$dockerRunning = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue

if ($dockerRunning) {
    Write-Host "Docker Desktop is currently running." -ForegroundColor Yellow
    Write-Host "Please QUIT Docker Desktop completely before proceeding." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "1. Right-click Docker Desktop icon in system tray" -ForegroundColor White
    Write-Host "2. Click 'Quit Docker Desktop'" -ForegroundColor White
    Write-Host "3. Wait for it to fully close" -ForegroundColor White
    Write-Host "4. Then run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter when Docker Desktop is closed"
}

# Configure daemon.json
$daemonPath = "$env:USERPROFILE\.docker\daemon.json"
Write-Host "Configuring Docker daemon DNS settings..." -ForegroundColor Green

if (Test-Path $daemonPath) {
    $json = Get-Content $daemonPath | ConvertFrom-Json
} else {
    $json = @{} | ConvertTo-Json | ConvertFrom-Json
}

# Add DNS settings
if (-not $json.dns) {
    $json | Add-Member -MemberType NoteProperty -Name "dns" -Value @("8.8.8.8", "8.8.4.4") -Force
} else {
    $json.dns = @("8.8.8.8", "8.8.4.4")
}

$json | ConvertTo-Json -Depth 10 | Set-Content $daemonPath
Write-Host "DNS settings added to daemon.json:" -ForegroundColor Green
Get-Content $daemonPath | Write-Host

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Open Docker Desktop" -ForegroundColor White
Write-Host "2. Go to Settings (gear icon)" -ForegroundColor White
Write-Host "3. Navigate to: Resources > Network" -ForegroundColor White
Write-Host "4. Set DNS Server to: Manual" -ForegroundColor White
Write-Host "5. Enter: 8.8.8.8, 8.8.4.4" -ForegroundColor White
Write-Host "6. Click 'Apply & Restart'" -ForegroundColor White
Write-Host ""
Write-Host "OR alternatively, just restart Docker Desktop and the daemon.json changes should apply." -ForegroundColor Yellow
Write-Host ""
Write-Host "After restart, test with: docker pull mysql:8.0" -ForegroundColor Cyan

