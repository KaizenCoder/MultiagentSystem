# Installateur Service Backup NextGeneration
# Requires Administrator privileges

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Status
)

$ServiceName = "NextGenerationBackup"
$ServiceDisplayName = "NextGeneration Backup System"
$ServiceDescription = "Service automatique de sauvegarde NextGeneration"
$WorkingDirectory = "C:\Dev\nextgeneration\tools\zip_backup"
$ServiceExecutable = "python"
$ServiceArguments = "$WorkingDirectory\src\backup_service.py"

if ($Install) {
    Write-Host "🔧 Installation service NextGeneration Backup..."
    
    # Vérification privilèges admin
    if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "❌ Privilèges administrateur requis"
        exit 1
    }
    
    # Création service
    New-Service -Name $ServiceName -BinaryPathName "$ServiceExecutable $ServiceArguments" -DisplayName $ServiceDisplayName -Description $ServiceDescription -StartupType Manual
    
    Write-Host "✅ Service installé avec succès"
} elseif ($Uninstall) {
    Write-Host "🗑️ Désinstallation service..."
    
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
    Remove-Service -Name $ServiceName -ErrorAction SilentlyContinue
    
    Write-Host "✅ Service désinstallé"
} elseif ($Status) {
    Get-Service -Name $ServiceName -ErrorAction SilentlyContinue | Format-Table
} else {
    Write-Host "Usage: -Install | -Uninstall | -Status"
}