# Script de déploiement production PowerShell pour Windows
# Automatisation complète du setup selon les exigences IA-2

param(
    [string]$Environment = "production",
    [switch]$SkipPrerequisites = $false,
    [switch]$CleanInstall = $false
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$LogFile = Join-Path $ProjectRoot "logs\deployment-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Créer le répertoire de logs s'il n'existe pas
$LogDir = Split-Path -Parent $LogFile
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# Fonctions de logging
function Write-Log {
    param($Message, $Level = "INFO")
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    switch ($Level) {
        "ERROR" { Write-Host $LogEntry -ForegroundColor Red }
        "WARNING" { Write-Host $LogEntry -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $LogEntry -ForegroundColor Green }
        "INFO" { Write-Host $LogEntry -ForegroundColor Cyan }
        default { Write-Host $LogEntry }
    }
    
    Add-Content -Path $LogFile -Value $LogEntry
}

function Write-LogInfo($Message) { Write-Log $Message "INFO" }
function Write-LogSuccess($Message) { Write-Log $Message "SUCCESS" }
function Write-LogWarning($Message) { Write-Log $Message "WARNING" }
function Write-LogError($Message) { Write-Log $Message "ERROR" }

# Vérifications préliminaires
function Test-Prerequisites {
    Write-LogInfo "Vérification des prérequis..."
    
    # Docker Desktop
    try {
        $dockerVersion = docker --version
        Write-LogSuccess "Docker trouvé: $dockerVersion"
    } catch {
        Write-LogError "Docker Desktop n'est pas installé ou n'est pas dans le PATH"
        throw "Docker requis pour le déploiement"
    }
    
    # Docker Compose
    try {
        $composeVersion = docker-compose --version
        Write-LogSuccess "Docker Compose trouvé: $composeVersion"
    } catch {
        Write-LogError "Docker Compose n'est pas installé"
        throw "Docker Compose requis"
    }
    
    # Vérifier que Docker fonctionne
    try {
        docker info | Out-Null
        Write-LogSuccess "Docker Engine fonctionne"
    } catch {
        Write-LogError "Docker Engine ne fonctionne pas. Démarrez Docker Desktop."
        throw "Docker Engine non disponible"
    }
    
    # Vérifier l'espace disque (minimum 10GB)
    $Drive = (Get-Location).Drive
    $FreeSpace = (Get-Volume -DriveLetter $Drive.Name).SizeRemaining
    $RequiredSpace = 10GB
    
    if ($FreeSpace -lt $RequiredSpace) {
        $FreeSpaceGB = [math]::Round($FreeSpace / 1GB, 2)
        Write-LogError "Espace disque insuffisant. Requis: 10GB, disponible: ${FreeSpaceGB}GB"
        throw "Espace disque insuffisant"
    }
    
    # Vérifier les variables d'environnement requises
    if (-not $env:OPENAI_API_KEY) {
        Write-LogError "Variable d'environnement OPENAI_API_KEY non définie"
        throw "OPENAI_API_KEY requis"
    }
    
    if (-not $env:ANTHROPIC_API_KEY) {
        Write-LogError "Variable d'environnement ANTHROPIC_API_KEY non définie"
        throw "ANTHROPIC_API_KEY requis"
    }
    
    Write-LogSuccess "Prérequis validés"
}

# Création des répertoires de données
function New-DataDirectories {
    Write-LogInfo "Création des répertoires de données..."
    
    $DataDirs = @(
        "C:\docker-data\postgres",
        "C:\docker-data\redis", 
        "C:\docker-data\chroma",
        "C:\docker-data\prometheus",
        "C:\docker-data\grafana",
        "C:\docker-data\elasticsearch"
    )
    
    foreach ($Dir in $DataDirs) {
        if (-not (Test-Path $Dir)) {
            New-Item -ItemType Directory -Path $Dir -Force | Out-Null
            Write-LogInfo "Créé: $Dir"
        }
    }
    
    # Répertoires de logs
    $LogsDir = Join-Path $ProjectRoot "logs"
    if (-not (Test-Path $LogsDir)) {
        New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
    }
    
    Write-LogSuccess "Répertoires de données créés"
}

# Configuration des secrets Docker Swarm
function Initialize-DockerSecrets {
    Write-LogInfo "Configuration des secrets Docker..."
    
    # Initialiser Docker Swarm si nécessaire
    try {
        $SwarmInfo = docker info --format "{{.Swarm.LocalNodeState}}"
        if ($SwarmInfo -ne "active") {
            Write-LogInfo "Initialisation de Docker Swarm..."
            docker swarm init --advertise-addr 127.0.0.1
        }
    } catch {
        Write-LogInfo "Initialisation de Docker Swarm..."
        docker swarm init --advertise-addr 127.0.0.1
    }
    
    # Fonction pour générer des mots de passe sécurisés
    function New-SecurePassword($Length = 32) {
        $Bytes = New-Object byte[] $Length
        $Random = [System.Security.Cryptography.RNGCryptoServiceProvider]::new()
        $Random.GetBytes($Bytes)
        return [System.Convert]::ToBase64String($Bytes)
    }
    
    # Générer les secrets
    $Secrets = @{
        "orchestrator_api_key" = New-SecurePassword
        "postgres_user" = "postgres"
        "postgres_password" = New-SecurePassword 24
        "vault_token" = New-SecurePassword
        "grafana_admin_password" = New-SecurePassword 16
        "grafana_secret_key" = New-SecurePassword
        "elastic_password" = New-SecurePassword 16
        "openai_api_key" = $env:OPENAI_API_KEY
        "anthropic_api_key" = $env:ANTHROPIC_API_KEY
        "chroma_credentials" = (@{
            username = "admin"
            password = New-SecurePassword 16
        } | ConvertTo-Json -Compress)
    }
    
    # Créer les secrets Docker
    foreach ($SecretName in $Secrets.Keys) {
        try {
            docker secret inspect $SecretName | Out-Null
            Write-LogInfo "Secret $SecretName existe déjà"
        } catch {
            $SecretValue = $Secrets[$SecretName]
            $SecretValue | docker secret create $SecretName -
            Write-LogSuccess "Secret $SecretName créé"
        }
    }
    
    # Sauvegarder les secrets pour référence (sans les API keys)
    $BackupFile = Join-Path $ProjectRoot ".secrets-backup.json"
    $SecretsBackup = @{}
    
    foreach ($Key in $Secrets.Keys) {
        if ($Key -notlike "*api_key*") {
            $SecretsBackup[$Key] = $Secrets[$Key]
        }
    }
    
    $SecretsBackup | ConvertTo-Json -Depth 10 | Set-Content $BackupFile
    Write-LogSuccess "Backup des secrets sauvegardé dans .secrets-backup.json"
    
    Write-LogSuccess "Secrets Docker configurés"
}

# Configuration SSL/TLS
function Initialize-SSLCertificates {
    Write-LogInfo "Configuration des certificats SSL..."
    
    $SSLDir = Join-Path $ProjectRoot "config\ssl"
    if (-not (Test-Path $SSLDir)) {
        New-Item -ItemType Directory -Path $SSLDir -Force | Out-Null
    }
    
    # Pour le développement/staging, générer un certificat auto-signé
    if ($Environment -ne "production") {
        $CertPath = Join-Path $SSLDir "orchestrator.crt"
        $KeyPath = Join-Path $SSLDir "orchestrator.key"
        $PemPath = Join-Path $SSLDir "orchestrator.pem"
        
        if (-not (Test-Path $CertPath)) {
            # Utiliser OpenSSL si disponible, sinon PowerShell
            try {
                openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
                    -keyout $KeyPath `
                    -out $CertPath `
                    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
                
                # Combiner pour HAProxy
                Get-Content $CertPath, $KeyPath | Set-Content $PemPath
                
                Write-LogSuccess "Certificat SSL auto-signé généré"
            } catch {
                Write-LogWarning "OpenSSL non disponible, utilisation de PowerShell pour générer le certificat"
                
                # Générer avec PowerShell (Windows 10+)
                $Cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\CurrentUser\My"
                $CertPassword = ConvertTo-SecureString -String "temp123" -Force -AsPlainText
                Export-PfxCertificate -Cert $Cert -FilePath (Join-Path $SSLDir "orchestrator.pfx") -Password $CertPassword
                
                Write-LogSuccess "Certificat PowerShell généré"
            }
        }
    } else {
        Write-LogWarning "En production, copiez vos certificats SSL valides dans $SSLDir"
    }
    
    Write-LogSuccess "Certificats SSL configurés"
}

# Configuration des fichiers de configuration
function Initialize-ConfigurationFiles {
    Write-LogInfo "Configuration des fichiers de configuration..."
    
    # Créer les répertoires de configuration
    $ConfigDirs = @("postgres", "redis", "prometheus", "alertmanager", "grafana", "haproxy")
    foreach ($Dir in $ConfigDirs) {
        $ConfigPath = Join-Path $ProjectRoot "config\$Dir"
        if (-not (Test-Path $ConfigPath)) {
            New-Item -ItemType Directory -Path $ConfigPath -Force | Out-Null
        }
    }
    
    Write-LogSuccess "Répertoires de configuration créés"
}

# Construction et déploiement
function Start-Deployment {
    Write-LogInfo "Construction et déploiement des services..."
    
    Set-Location $ProjectRoot
    
    # Build des images
    Write-LogInfo "Construction des images Docker..."
    docker-compose -f docker-compose.production.yml build --no-cache
    
    # Démarrage échelonné des services
    Write-LogInfo "Démarrage des services de base..."
    docker-compose -f docker-compose.production.yml up -d postgres redis-cluster chromadb
    
    # Attendre la disponibilité
    Write-LogInfo "Attente de la disponibilité des services de base..."
    Start-Sleep 30
    
    # Vérifier la santé des services de base
    $BaseServices = @("postgres", "redis-cluster", "chromadb")
    foreach ($Service in $BaseServices) {
        $Timeout = 60
        $Ready = $false
        
        while ($Timeout -gt 0 -and -not $Ready) {
            try {
                $Status = docker-compose -f docker-compose.production.yml ps $Service
                if ($Status -match "healthy|Up") {
                    Write-LogSuccess "Service $Service est prêt"
                    $Ready = $true
                } else {
                    Start-Sleep 5
                    $Timeout -= 5
                }
            } catch {
                Start-Sleep 5
                $Timeout -= 5
            }
        }
        
        if (-not $Ready) {
            Write-LogError "Service $Service n'est pas devenu disponible"
            throw "Service $Service non disponible"
        }
    }
    
    # Démarrer les services de monitoring
    Write-LogInfo "Démarrage des services de monitoring..."
    docker-compose -f docker-compose.production.yml up -d prometheus grafana alertmanager elasticsearch
    Start-Sleep 20
    
    # Démarrer les services applicatifs
    Write-LogInfo "Démarrage des services applicatifs..."
    docker-compose -f docker-compose.production.yml up -d memory-api
    Start-Sleep 15
    
    # Démarrer les orchestrateurs
    Write-LogInfo "Démarrage des orchestrateurs..."
    docker-compose -f docker-compose.production.yml up -d orchestrator-1 orchestrator-2 orchestrator-3
    Start-Sleep 20
    
    # Démarrer le load balancer
    Write-LogInfo "Démarrage du load balancer..."
    docker-compose -f docker-compose.production.yml up -d load-balancer
    
    # Démarrer les services de logging
    Write-LogInfo "Démarrage des services de logging..."
    docker-compose -f docker-compose.production.yml up -d logstash kibana jaeger
    
    Write-LogSuccess "Tous les services sont démarrés"
}

# Vérifications post-déploiement
function Test-Deployment {
    Write-LogInfo "Vérification du déploiement..."
    
    Start-Sleep 30
    
    # Vérifier les services critiques
    $CriticalServices = @("postgres", "redis-cluster", "orchestrator-1", "orchestrator-2", "orchestrator-3", "memory-api", "load-balancer")
    
    foreach ($Service in $CriticalServices) {
        try {
            $Status = docker-compose -f docker-compose.production.yml ps $Service
            if ($Status -match "Up|healthy") {
                Write-LogSuccess "✓ Service $Service fonctionne"
            } else {
                Write-LogError "✗ Service $Service ne fonctionne pas"
                docker-compose -f docker-compose.production.yml logs $Service --tail 20
            }
        } catch {
            Write-LogError "✗ Impossible de vérifier le service $Service"
        }
    }
    
    # Test des endpoints
    Write-LogInfo "Test des endpoints..."
    
    $Endpoints = @{
        "Health Check" = "http://localhost/health"
        "Metrics" = "http://localhost/metrics"
        "Grafana" = "http://localhost:3000/api/health"
        "Prometheus" = "http://localhost:9090/-/healthy"
    }
    
    foreach ($Name in $Endpoints.Keys) {
        try {
            $Response = Invoke-WebRequest -Uri $Endpoints[$Name] -TimeoutSec 10 -UseBasicParsing
            if ($Response.StatusCode -eq 200) {
                Write-LogSuccess "✓ $Name accessible"
            } else {
                Write-LogWarning "⚠ $Name retourne status $($Response.StatusCode)"
            }
        } catch {
            Write-LogWarning "⚠ $Name non accessible: $($_.Exception.Message)"
        }
    }
    
    Write-LogSuccess "Vérification du déploiement terminée"
}

# Affichage des informations de connexion
function Show-ConnectionInfo {
    Write-LogInfo "Informations de connexion:"
    Write-Host ""
    Write-Host "🌐 Application:" -ForegroundColor Cyan
    Write-Host "  - Load Balancer: https://localhost (HTTP redirigé vers HTTPS)"
    Write-Host "  - Health Check: http://localhost/health"
    Write-Host "  - API Documentation: http://localhost/docs"
    Write-Host ""
    Write-Host "📊 Monitoring:" -ForegroundColor Cyan
    Write-Host "  - Grafana: http://localhost:3000"
    Write-Host "  - Prometheus: http://localhost:9090"
    Write-Host "  - AlertManager: http://localhost:9093"
    Write-Host ""
    Write-Host "🔍 Logging:" -ForegroundColor Cyan
    Write-Host "  - Kibana: http://localhost:5601"
    Write-Host "  - Jaeger: http://localhost:16686"
    Write-Host ""
    Write-Host "🔐 Credentials:" -ForegroundColor Cyan
    Write-Host "  - Voir .secrets-backup.json pour les mots de passe"
    Write-Host ""
    Write-Host "📂 Data directories: C:\docker-data\*"
    Write-Host "📝 Logs: $ProjectRoot\logs\"
    Write-Host ""
}

# Nettoyage en cas d'erreur
function Stop-DeploymentOnError {
    Write-LogError "Erreur détectée. Nettoyage en cours..."
    
    if ($Environment -ne "production") {
        try {
            docker-compose -f docker-compose.production.yml down
            Write-LogInfo "Services arrêtés"
        } catch {
            Write-LogWarning "Impossible d'arrêter les services automatiquement"
        }
    } else {
        Write-LogWarning "En production, nettoyage manuel requis"
    }
}

# Script principal
function Invoke-Deployment {
    Write-LogInfo "=== Déploiement Production Multi-Agent Orchestrator ==="
    Write-LogInfo "Environnement: $Environment"
    Write-LogInfo "Démarrage: $(Get-Date)"
    
    $StartTime = Get-Date
    
    try {
        if (-not $SkipPrerequisites) {
            Test-Prerequisites
        }
        
        if ($CleanInstall) {
            Write-LogInfo "Nettoyage de l'installation précédente..."
            docker-compose -f docker-compose.production.yml down -v
            docker system prune -f
        }
        
        New-DataDirectories
        Initialize-DockerSecrets
        Initialize-SSLCertificates
        Initialize-ConfigurationFiles
        Start-Deployment
        Test-Deployment
        Show-ConnectionInfo
        
        $Duration = (Get-Date) - $StartTime
        Write-LogSuccess "=== Déploiement terminé avec succès ==="
        Write-LogInfo "Durée totale: $($Duration.TotalSeconds) secondes"
        Write-Host ""
        Write-LogInfo "Pour arrêter les services: docker-compose -f docker-compose.production.yml down"
        Write-LogInfo "Pour voir les logs: docker-compose -f docker-compose.production.yml logs -f"
        Write-LogInfo "Pour redémarrer: docker-compose -f docker-compose.production.yml restart"
        
    } catch {
        Write-LogError "Erreur pendant le déploiement: $($_.Exception.Message)"
        Stop-DeploymentOnError
        throw
    }
}

# Exécution
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Deployment
}
