# Script pour configurer l'accès aux fichiers dans Void Editor
# Auteur: NextGeneration Team
# Date: 20 juin 2025

Write-Host "🔧 Configuration Void Editor - Accès Fichiers" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Vérifier si Void Editor est installé
$voidPath = Get-Command "void" -ErrorAction SilentlyContinue
if (-not $voidPath) {
    Write-Host "❌ Void Editor non trouvé. Installez-le d'abord." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Void Editor détecté: $($voidPath.Source)" -ForegroundColor Green

# Configuration du workspace
$workspacePath = "C:\Dev\nextgeneration"
$configPath = "$env:APPDATA\Void\settings.json"

Write-Host "📁 Configuration workspace: $workspacePath" -ForegroundColor Yellow

# Créer la configuration Void Editor
$voidConfig = @{
    "workspaceSettings" = @{
        "defaultWorkspace" = $workspacePath
        "enableFileAccess" = $true
        "contextFiles" = @(
            "$workspacePath\README.md",
            "$workspacePath\agent_factory_implementation\documentation\*.md",
            "$workspacePath\docs\**\*.md"
        )
    }
    "ai" = @{
        "provider" = "ollama"
        "baseUrl" = "http://localhost:11434"
        "model" = "deepseek-void-ultimate"
        "enableFileContext" = $true
        "maxContextFiles" = 10
        "contextInstructions" = "Tu as acces aux fichiers du workspace NextGeneration. Utilise le contexte fourni pour repondre aux questions sur les fichiers."
    }
} | ConvertTo-Json -Depth 5

# Créer le répertoire de config si nécessaire
$configDir = Split-Path $configPath -Parent
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Sauvegarder la configuration
$voidConfig | Out-File -FilePath $configPath -Encoding UTF8 -Force

Write-Host "✅ Configuration sauvegardee: $configPath" -ForegroundColor Green

# Instructions pour l'utilisateur
Write-Host "`n📋 INSTRUCTIONS VOID EDITOR:" -ForegroundColor Cyan
Write-Host "1. Redémarrez Void Editor" -ForegroundColor White
Write-Host "2. Ouvrez le workspace: $workspacePath" -ForegroundColor White
Write-Host "3. Utilisez ces commandes dans le chat:" -ForegroundColor White
Write-Host "   • 'Analyse le README.md'" -ForegroundColor Yellow
Write-Host "   • 'Explique la structure du projet'" -ForegroundColor Yellow
Write-Host "   • 'Résume la documentation'" -ForegroundColor Yellow

Write-Host "`n🎯 Le modele aura maintenant acces au contexte des fichiers!" -ForegroundColor Green 