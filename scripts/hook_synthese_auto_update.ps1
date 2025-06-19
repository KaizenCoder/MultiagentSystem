#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Hook Synthèse Auto-Update - Intégration Workflows NextGeneration

.DESCRIPTION
    Script d'intégration pour l'automatisation des mises à jour de SYNTHESE_EXECUTIVE.md et CHANGELOG.md
    - Exécution automatique après commits significatifs
    - Intégration avec Git hooks
    - Déclenchement lors de transmissions coordinateur
    - Support webhook Git

.PARAMETER Mode
    Mode d'exécution: git-hook, coordinateur, webhook, manuel

.PARAMETER TriggerEvent
    Événement déclencheur: post-commit, pre-push, mission-complete, pitch-create

.PARAMETER DryRun
    Mode simulation sans modifications

.EXAMPLE
    .\hook_synthese_auto_update.ps1 -Mode git-hook -TriggerEvent post-commit
    .\hook_synthese_auto_update.ps1 -Mode coordinateur -TriggerEvent mission-complete
    .\hook_synthese_auto_update.ps1 -Mode webhook -DryRun

.NOTES
    Version: 1.0
    Auteur: Système NextGeneration
    Intégration: Agent Synthèse Auto-Update
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("git-hook", "coordinateur", "webhook", "manuel")]
    [string]$Mode = "manuel",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("post-commit", "pre-push", "mission-complete", "pitch-create", "daily")]
    [string]$TriggerEvent = "manual",
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory=$false)]
    [switch]$ShowStatus,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectRoot = $PWD
)

# Configuration
$ErrorActionPreference = "Stop"
$global:CONFIG = @{
    ProjectRoot = $ProjectRoot
    LogsDir = Join-Path $ProjectRoot "tools\documentation_generator\logs"
    AgentScript = Join-Path $ProjectRoot "tools\documentation_generator\agent_synthese_auto_update.py"
    PythonExe = "python"
    HookEnabled = $true
    MinInterval = 300  # 5 minutes minimum entre exécutions
    LastRunFile = Join-Path $ProjectRoot "tools\documentation_generator\logs\last_auto_update.json"
}

# Logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Couleurs selon niveau
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARN"  { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage -ForegroundColor White }
    }
    
    # Log vers fichier
    $logFile = Join-Path $global:CONFIG.LogsDir "hook_synthese_auto_update.log"
    if (!(Test-Path (Split-Path $logFile))) {
        New-Item -ItemType Directory -Path (Split-Path $logFile) -Force | Out-Null
    }
    Add-Content -Path $logFile -Value $logMessage
}

function Test-ShouldExecute {
    """Vérifie si l'exécution est nécessaire"""
    
    # Vérifier si activé
    if (-not $global:CONFIG.HookEnabled) {
        Write-Log "Hook désactivé dans la configuration" "WARN"
        return $false
    }
    
    # Vérifier intervalle minimum
    if (Test-Path $global:CONFIG.LastRunFile) {
        try {
            $lastRun = Get-Content $global:CONFIG.LastRunFile | ConvertFrom-Json
            $lastTime = [DateTime]::Parse($lastRun.timestamp)
            $elapsed = (Get-Date) - $lastTime
            
            if ($elapsed.TotalSeconds -lt $global:CONFIG.MinInterval) {
                Write-Log "Intervalle minimum non atteint ($($elapsed.TotalSeconds)s < $($global:CONFIG.MinInterval)s)" "INFO"
                return $false
            }
        }
        catch {
            Write-Log "Erreur lecture dernière exécution: $_" "WARN"
        }
    }
    
    # Vérifier selon le mode
    switch ($Mode) {
        "git-hook" {
            return Test-GitHookTrigger
        }
        "coordinateur" {
            return Test-CoordinateurTrigger  
        }
        "webhook" {
            return $true  # Toujours exécuter pour webhook
        }
        "manuel" {
            return $true  # Toujours exécuter en manuel
        }
    }
    
    return $false
}

function Test-GitHookTrigger {
    """Teste si le trigger Git hook doit s'exécuter"""
    
    # Vérifier les derniers commits pour mots-clés
    try {
        $recentCommits = git log --since="1 hour ago" --oneline 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Erreur Git log: impossible de vérifier les commits récents" "WARN"
            return $false
        }
        
        $triggerKeywords = @("mission", "accompli", "opérationnel", "validé", "système", "agent", "synthèse")
        
        foreach ($commit in $recentCommits) {
            foreach ($keyword in $triggerKeywords) {
                if ($commit -like "*$keyword*") {
                    Write-Log "Trigger détecté dans commit: $commit" "INFO"
                    return $true
                }
            }
        }
        
        Write-Log "Aucun trigger détecté dans les commits récents" "INFO"
        return $false
    }
    catch {
        Write-Log "Erreur test Git trigger: $_" "ERROR"
        return $false
    }
}

function Test-CoordinateurTrigger {
    """Teste si le trigger coordinateur doit s'exécuter"""
    
    # Vérifier fichiers de transmission récents
    $transmissionPatterns = @(
        "SYNTHESE_FINALE_*.md",
        "RAPPORT_*_*.md", 
        "MISSION_*_ACCOMPLIE.md"
    )
    
    $recentFiles = @()
    foreach ($pattern in $transmissionPatterns) {
        $files = Get-ChildItem -Path $global:CONFIG.ProjectRoot -Filter $pattern -Recurse -ErrorAction SilentlyContinue
        $recentFiles += $files | Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-1) }
    }
    
    if ($recentFiles.Count -gt 0) {
        Write-Log "Fichiers de transmission récents détectés: $($recentFiles.Count)" "INFO"
        return $true
    }
    
    return $false
}

function Invoke-AgentSynthese {
    """Exécute l'agent de synthèse auto-update"""
    
    Write-Log "Démarrage Agent Synthèse Auto-Update" "INFO"
    Write-Log "Mode: $Mode | Event: $TriggerEvent | DryRun: $DryRun" "INFO"
    
    # Vérifier prérequis
    if (!(Test-Path $global:CONFIG.AgentScript)) {
        Write-Log "Script agent introuvable: $($global:CONFIG.AgentScript)" "ERROR"
        return $false
    }
    
    # Construire arguments
    $args = @("$($global:CONFIG.AgentScript)", "--mode", "complet")
    if ($DryRun) {
        $args += "--dry-run"
    }
    
    try {
        # Exécuter agent Python
        Write-Log "Exécution: $($global:CONFIG.PythonExe) $($args -join ' ')" "INFO"
        
        $process = Start-Process -FilePath $global:CONFIG.PythonExe -ArgumentList $args -WorkingDirectory $global:CONFIG.ProjectRoot -Wait -PassThru -NoNewWindow -RedirectStandardOutput "temp_output.txt" -RedirectStandardError "temp_error.txt"
        
        # Lire sorties
        $output = Get-Content "temp_output.txt" -ErrorAction SilentlyContinue
        $errors = Get-Content "temp_error.txt" -ErrorAction SilentlyContinue
        
        # Nettoyer fichiers temporaires
        Remove-Item "temp_output.txt", "temp_error.txt" -ErrorAction SilentlyContinue
        
        if ($process.ExitCode -eq 0) {
            Write-Log "Agent exécuté avec succès" "SUCCESS"
            if ($output) {
                Write-Log "Sortie: $($output -join '; ')" "INFO"
            }
            return $true
        }
        else {
            Write-Log "Erreur exécution agent (exit: $($process.ExitCode))" "ERROR"
            if ($errors) {
                Write-Log "Erreurs: $($errors -join '; ')" "ERROR"
            }
            return $false
        }
    }
    catch {
        Write-Log "Exception lors de l'exécution: $_" "ERROR"
        return $false
    }
}

function Save-LastRun {
    """Sauvegarde l'horodatage de la dernière exécution"""
    
    $lastRun = @{
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.ffffff")
        mode = $Mode
        trigger = $TriggerEvent
        success = $true
    }
    
    try {
        $lastRun | ConvertTo-Json | Set-Content $global:CONFIG.LastRunFile -Encoding UTF8
        Write-Log "Dernière exécution sauvegardée" "INFO"
    }
    catch {
        Write-Log "Erreur sauvegarde dernière exécution: $_" "WARN"
    }
}

function Show-Status {
    """Affiche le statut du système d'auto-update"""
    
    Write-Host "`n🤖 HOOK SYNTHÈSE AUTO-UPDATE - STATUS" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Configuration
    Write-Host "`n📋 Configuration:" -ForegroundColor Yellow
    Write-Host "  Mode: $Mode"
    Write-Host "  Trigger: $TriggerEvent" 
    Write-Host "  Projet: $($global:CONFIG.ProjectRoot)"
    Write-Host "  Agent: $(Split-Path $global:CONFIG.AgentScript -Leaf)"
    Write-Host "  Hook activé: $($global:CONFIG.HookEnabled)"
    
    # Dernière exécution
    if (Test-Path $global:CONFIG.LastRunFile) {
        try {
            $lastRun = Get-Content $global:CONFIG.LastRunFile | ConvertFrom-Json
            Write-Host "`n🕐 Dernière exécution:" -ForegroundColor Yellow
            Write-Host "  Date: $($lastRun.timestamp)"
            Write-Host "  Mode: $($lastRun.mode)"
            Write-Host "  Trigger: $($lastRun.trigger)"
            Write-Host "  Succès: $($lastRun.success)"
        }
        catch {
            Write-Host "`n⚠️  Erreur lecture dernière exécution" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "`n🆕 Première exécution" -ForegroundColor Yellow
    }
    
    # Tests
    Write-Host "`n🔍 Tests d'environnement:" -ForegroundColor Yellow
    Write-Host "  Python disponible: $(Test-Path (Get-Command python -ErrorAction SilentlyContinue))"
    Write-Host "  Script agent: $(Test-Path $global:CONFIG.AgentScript)"
    Write-Host "  Dossier logs: $(Test-Path $global:CONFIG.LogsDir)"
    Write-Host "  Repository Git: $(Test-Path '.git')"
}

# MAIN EXECUTION
function Main {
    Write-Host "🚀 HOOK SYNTHÈSE AUTO-UPDATE - NEXTGENERATION" -ForegroundColor Green
    Write-Host "Mode: $Mode | Event: $TriggerEvent" -ForegroundColor Cyan
    
    if ($ShowStatus) {
        Show-Status
    }
    
    # Test si exécution nécessaire
    if (!(Test-ShouldExecute)) {
        Write-Log "Exécution non nécessaire - conditions non remplies" "INFO"
        return
    }
    
    # Exécuter l'agent
    $success = Invoke-AgentSynthese
    
    if ($success) {
        Write-Log "Hook exécuté avec succès" "SUCCESS"
        Save-LastRun
        
        # Actions post-exécution selon mode
        switch ($Mode) {
            "git-hook" {
                Write-Log "Documents mis à jour automatiquement via Git hook" "SUCCESS"
            }
            "coordinateur" {
                Write-Log "Synthèse mise à jour suite à transmission coordinateur" "SUCCESS"  
            }
            "webhook" {
                Write-Log "Mise à jour déclenchée par webhook" "SUCCESS"
            }
        }
    }
    else {
        Write-Log "Échec exécution hook" "ERROR"
        exit 1
    }
}

# Point d'entrée
if ($MyInvocation.InvocationName -ne '.') {
    Main
} 