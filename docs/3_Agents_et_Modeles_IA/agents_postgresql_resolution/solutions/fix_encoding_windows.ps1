
# Script de configuration encodage PostgreSQL Windows
Write-Host "Configuration encodage PostgreSQL..." -ForegroundColor Green

# Variables d'environnement système
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
[Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

Write-Host "Variables d'environnement configurées." -ForegroundColor Yellow
Write-Host "Redémarrer le terminal pour appliquer les changements." -ForegroundColor Red
