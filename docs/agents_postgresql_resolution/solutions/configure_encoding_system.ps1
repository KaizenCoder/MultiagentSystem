
# Configuration encodage systme Windows pour PostgreSQL
Write-Host "Configuration encodage PostgreSQL Windows..." -ForegroundColor Green

# Variables utilisateur
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User") 
[System.Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[System.Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

# Variables systme (ncessite admin)
try {
    [System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "Machine")
    [System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "Machine")
    Write-Host "Variables systme configures (admin)" -ForegroundColor Green
} catch {
    Write-Host "Variables systme non configures (pas admin)" -ForegroundColor Yellow
}

Write-Host "Configuration termine. Redmarrer le terminal." -ForegroundColor Red
