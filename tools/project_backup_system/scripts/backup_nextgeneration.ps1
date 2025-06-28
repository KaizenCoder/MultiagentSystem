# Backup Script pour nextgeneration
# Généré automatiquement par NextGeneration Backup System
# Version: 1.0.0

param(
    [string]$ConfigPath = "C:/Dev/nextgeneration/tools/zip_backup/config/nextgeneration_backup.json",
    [switch]$Verbose = $false,
    [switch]$TestMode = $false
)

# Configuration
$ErrorActionPreference = "Stop"
$VerbosePreference = if ($Verbose) { "Continue" } else { "SilentlyContinue" }

# Chemins
$BackupSystemRoot = "C:\Dev\nextgeneration\tools\zip_backup"
$LogDir = "$BackupSystemRoot\logs"
$LogFile = "$LogDir\backup_nextgeneration_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Fonction logging
function Write-BackupLog {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Output $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry -Encoding UTF8
}

# Début backup
Write-BackupLog "🚀 Début backup nextgeneration" "INFO"

try {
    # Vérification Python disponible
    $PythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonCmd) {
        throw "Python non trouvé dans PATH"
    }
    
    Write-BackupLog "✅ Python trouvé: $($PythonCmd.Source)" "INFO"
    
    # Changement répertoire de travail
    Set-Location -Path $BackupSystemRoot
    Write-BackupLog "📁 Répertoire de travail: $BackupSystemRoot" "INFO"
    
    # Exécution backup principal
    $BackupScript = "$BackupSystemRoot\src\backup_executor.py"
    
    if ($TestMode) {
        Write-BackupLog "🧪 Mode test activé" "INFO"
        $Arguments = @($BackupScript, "--config", $ConfigPath, "--test")
    } else {
        $Arguments = @($BackupScript, "--config", $ConfigPath)
    }
    
    Write-BackupLog "🔧 Commande: python $($Arguments -join ' ')" "INFO"
    
    # Exécution avec capture sortie
    $Process = Start-Process -FilePath "python" -ArgumentList $Arguments -Wait -PassThru -RedirectStandardOutput "$LogDir\backup_nextgeneration_output.log" -RedirectStandardError "$LogDir\backup_nextgeneration_error.log"
    
    if ($Process.ExitCode -eq 0) {
        Write-BackupLog "✅ Backup nextgeneration terminé avec succès" "SUCCESS"
        
        # Notification succès (optionnel)
        if ($env:BACKUP_NOTIFICATIONS -eq "1") {
            $Title = "Backup nextgeneration"
            $Message = "Backup terminé avec succès à $(Get-Date -Format 'HH:mm')"
            # Utilisation msg pour notification simple
            Start-Process -FilePath "msg" -ArgumentList @("console", "/time:10", "$Title - $Message") -NoNewWindow
        }
        
        exit 0
    } else {
        throw "Backup échoué avec code de sortie: $($Process.ExitCode)"
    }
    
} catch {
    $ErrorMsg = $_.Exception.Message
    Write-BackupLog "❌ Erreur backup nextgeneration: $ErrorMsg" "ERROR"
    
    # Notification erreur
    if ($env:BACKUP_NOTIFICATIONS -eq "1") {
        $Title = "Erreur Backup nextgeneration"
        Start-Process -FilePath "msg" -ArgumentList @("console", "/time:15", "$Title - $ErrorMsg") -NoNewWindow
    }
    
    exit 1
}