# Change System DNS Script
# Run this script as Administrator if you want to change system DNS

Write-Host "=== System DNS Configuration ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternatively, manually change DNS via:" -ForegroundColor Yellow
    Write-Host "Settings > Network > Change adapter options > Properties > IPv4 > Use custom DNS" -ForegroundColor White
    exit 1
}

# Get active network adapter
$adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Where-Object { $_.InterfaceDescription -like "*Wi-Fi*" -or $_.InterfaceDescription -like "*Ethernet*" }

if ($adapters.Count -eq 0) {
    Write-Host "No active network adapter found!" -ForegroundColor Red
    exit 1
}

$adapter = $adapters[0]
Write-Host "Active adapter: $($adapter.Name)" -ForegroundColor Green
Write-Host "Current DNS:" -ForegroundColor Yellow
Get-DnsClientServerAddress -InterfaceAlias $adapter.Name -AddressFamily IPv4 | Format-Table

Write-Host ""
Write-Host "Do you want to change DNS to Google DNS (8.8.8.8, 8.8.4.4)?" -ForegroundColor Yellow
Write-Host "WARNING: This will change your system DNS. Make sure your network allows it." -ForegroundColor Red
$confirm = Read-Host "Type 'yes' to continue"

if ($confirm -ne "yes") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

# Set DNS
Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ("8.8.8.8", "8.8.4.4")

Write-Host ""
Write-Host "DNS changed successfully!" -ForegroundColor Green
Write-Host "New DNS settings:" -ForegroundColor Yellow
Get-DnsClientServerAddress -InterfaceAlias $adapter.Name -AddressFamily IPv4 | Format-Table

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Restart Docker Desktop" -ForegroundColor White
Write-Host "2. Test with: docker pull mysql:8.0" -ForegroundColor White
Write-Host ""
Write-Host "To revert to automatic DNS:" -ForegroundColor Yellow
Write-Host "Set-DnsClientServerAddress -InterfaceAlias '$($adapter.Name)' -ResetServerAddresses" -ForegroundColor Gray

