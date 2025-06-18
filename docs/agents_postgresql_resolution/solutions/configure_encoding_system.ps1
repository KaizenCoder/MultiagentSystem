
# Configuration encodage système Windows pour PostgreSQL
Write-Host "Configuration encodage PostgreSQL Windows..." -ForegroundColor Green

# Variables utilisateur
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User") 
[System.Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[System.Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

# Variables système (nécessite admin)
try {
    [System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "Machine")
    [System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "Machine")
    Write-Host "Variables système configurées (admin)" -ForegroundColor Green
} catch {
    Write-Host "Variables système non configurées (pas admin)" -ForegroundColor Yellow
}

Write-Host "Configuration terminée. Redémarrer le terminal." -ForegroundColor Red
