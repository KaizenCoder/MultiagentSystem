# 🐳 GUIDE D'INSTALLATION DOCKER POUR WINDOWS

## Option 1 : Docker Desktop (Recommandé)
1. Téléchargez Docker Desktop depuis : https://www.docker.com/products/docker-desktop/
2. Exécutez l'installateur
3. Redémarrez votre machine
4. Lancez Docker Desktop

## Option 2 : Installation via Chocolatey
```powershell
# Installer Chocolatey si pas déjà fait
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Installer Docker
choco install docker-desktop
```

## Option 3 : Installation via winget
```powershell
winget install Docker.DockerDesktop
```

## Vérification de l'installation
```bash
docker --version
docker-compose --version
```

## Alternative : Lancement Manuel (Sans Docker)
Si vous préférez ne pas installer Docker maintenant, vous pouvez lancer les services manuellement.
