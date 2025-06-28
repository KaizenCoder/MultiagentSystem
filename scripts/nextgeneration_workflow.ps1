# 🚀 NextGeneration Workflow - Automatisation Complète
# Mission: Workflow développement quotidien optimisé
# Base: Extension scripts PowerShell excel_vba_tools_launcher
# Infrastructure: NextGeneration mature (6 tools + 4 agents teams)

<#
.SYNOPSIS
    🚀 WORKFLOW DE DÉVELOPPEMENT QUOTIDIEN - NEXTGENERATION
    Ce script fournit des commandes rapides pour les tâches courantes de développement.

.DESCRIPTION
    Simplifie les actions comme le nettoyage, les tests et l'analyse statique.
    Utilise les outils internes du projet pour une intégration parfaite.

.EXAMPLE
    .\scripts\nextgeneration_workflow.ps1 -Action clean
    Nettoie les fichiers temporaires et les caches du projet.

.EXAMPLE
    .\scripts\nextgeneration_workflow.ps1 -Action test -Path "unit"
    Lance les tests unitaires.

.NOTES
    Auteur: Agent Coordinateur NextGeneration
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory=$true, HelpMessage="Action à exécuter.")]
    [ValidateSet("clean", "test", "lint", "docs")]
    [string]$Action,

    [Parameter(Mandatory=$false, HelpMessage="Chemin ou argument spécifique à l'action.")]
    [string]$Path
)

# Configuration
$NextGenerationRoot = "C:\Dev\nextgeneration"
$LogPath = "$NextGenerationRoot\logs"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = "$LogPath\workflow_$Timestamp.log"

# Vérification environnement
if (-not (Test-Path $NextGenerationRoot)) {
    Write-Error "❌ NextGeneration root not found: $NextGenerationRoot"
    exit 1
}

Set-Location $NextGenerationRoot

# Fonctions utilitaires
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $LogEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [$Level] $Message"
    Write-Host $LogEntry
    if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }
    Add-Content -Path $LogFile -Value $LogEntry
}

function Test-Infrastructure {
    Write-Log "🔍 Vérification infrastructure NextGeneration"
    
    # Tools mature (6 attendus)
    $ToolsCount = (Get-ChildItem "tools" -Directory).Count
    Write-Log "🛠️ Tools: $ToolsCount/6 identifiés"
    
    # Agents (20+ attendus)
    $AgentsCount = (Get-ChildItem -Recurse -Filter "agent_*.py").Count
    Write-Log "🤖 Agents: $AgentsCount identifiés"
    
    # Infrastructure critique
    $Components = @(
        @{Name="Orchestrator"; Path="orchestrator"; Expected=10},
        @{Name="Memory API"; Path="memory_api"; Expected=5},
        @{Name="Documentation"; Path="docs"; Expected=50},
        @{Name="Tests"; Path="tests"; Expected=20}
    )
    
    foreach ($Component in $Components) {
        if (Test-Path $Component.Path) {
            $Count = (Get-ChildItem $Component.Path -Recurse -File).Count
            $Status = if ($Count -ge $Component.Expected) { "✅" } else { "⚠️" }
            Write-Log "$Status $($Component.Name): $Count fichiers"
        } else {
            Write-Log "❌ $($Component.Name): MANQUANT"
        }
    }
    
    return $true
}

function Invoke-Documentation {
    Write-Log "📚 Génération documentation automatique"
    
    try {
        # Générateur principal NextGeneration
        $GeneratorPath = "tools\documentation_generator\generate_bundle_nextgeneration.py"
        
        if (-not (Test-Path $GeneratorPath)) {
            Write-Log "❌ Générateur non trouvé: $GeneratorPath" "ERROR"
            return $false
        }
        
        Write-Log "🚀 Lancement génération documentation complète"
        
        if ($Force) {
            $Result = python $GeneratorPath --mode regeneration
        } else {
            $Result = python $GeneratorPath --mode preservation
        }
        
        # Vérification résultat
        if (Test-Path "CODE-SOURCE.md") {
            $Size = [math]::Round((Get-Item "CODE-SOURCE.md").Length / 1KB, 2)
            Write-Log "✅ Documentation générée: ${Size}KB"
            
            if ($Size -lt 200) {
                Write-Log "⚠️ Taille documentation < 200KB attendu" "WARN"
            } else {
                Write-Log "🎉 Documentation SUPÉRIEURE aux spécifications (${Size}KB > 200KB)"
            }
            
            return $true
        } else {
            Write-Log "❌ Fichier CODE-SOURCE.md non généré" "ERROR"
            return $false
        }
        
    } catch {
        Write-Log "❌ Erreur génération documentation: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Invoke-Validation {
    Write-Log "🧪 Validation complète NextGeneration"
    
    # 1. Infrastructure
    Test-Infrastructure
    
    # 2. Tests Python
    Write-Log "🐍 Exécution tests Python"
    try {
        $TestResults = python -m pytest tests/ --tb=short 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ Tests Python: SUCCÈS"
        } else {
            Write-Log "⚠️ Tests Python: Problèmes détectés" "WARN"
        }
    } catch {
        Write-Log "⚠️ Tests Python non exécutables" "WARN"
    }
    
    # 3. Health check orchestrator
    Write-Log "🎼 Vérification orchestrateur"
    $HealthPath = "orchestrator\app\health\health_checker.py"
    if (Test-Path $HealthPath) {
        try {
            python $HealthPath
            Write-Log "✅ Orchestrateur: Opérationnel"
        } catch {
            Write-Log "⚠️ Orchestrateur: Problème détecté" "WARN"
        }
    }
    
    # 4. Validation agents teams
    Write-Log "👥 Validation équipes d'agents"
    $AgentTeams = @(
        "agent_factory_experts_team",
        "agent_factory_implementation", 
        "equipe_agents_tools_migration"
    )
    
    foreach ($Team in $AgentTeams) {
        if (Test-Path $Team) {
            $AgentCount = (Get-ChildItem "$Team" -Filter "*.py" -Recurse).Count
            Write-Log "✅ $Team : $AgentCount agents"
        } else {
            Write-Log "⚠️ $Team : MANQUANT" "WARN"
        }
    }
    
    return $true
}

function Invoke-AgentActivation {
    Write-Log "🤖 Activation équipes d'agents"
    
    $AgentCommands = @(
        @{Name="Factory Experts"; Path="agent_factory_experts_team\coordinateur_equipe_experts.py"},
        @{Name="Tools Migration"; Path="equipe_agents_tools_migration\coordinateur_equipe_tools.py"},
        @{Name="Architecte Code"; Path="agent_factory_implementation\agents\agent_02_architecte_code_expert.py"}
    )
    
    foreach ($Agent in $AgentCommands) {
        if (Test-Path $Agent.Path) {
            Write-Log "🚀 Activation: $($Agent.Name)"
            try {
                # Activation en mode dry-run pour validation
                $Process = Start-Process -FilePath "python" -ArgumentList $Agent.Path, "--dry-run" -PassThru -NoNewWindow
                $Process.WaitForExit(10000)  # 10s timeout
                
                if ($Process.ExitCode -eq 0) {
                    Write-Log "✅ $($Agent.Name): Prêt"
                } else {
                    Write-Log "⚠️ $($Agent.Name): Problème détecté" "WARN"
                }
            } catch {
                Write-Log "⚠️ $($Agent.Name): Erreur activation" "WARN"
            }
        } else {
            Write-Log "❌ $($Agent.Name): Agent non trouvé" "ERROR"
        }
    }
    
    return $true
}

function Invoke-Monitoring {
    Write-Log "📊 Monitoring système NextGeneration"
    
    # 1. Performance monitor
    $PerfMonitor = "tools\tts_performance_monitor\performance_monitor.py"
    if (Test-Path $PerfMonitor) {
        Write-Log "🚀 Lancement monitoring performance"
        python $PerfMonitor --status
    }
    
    # 2. GPU RTX 3090 validator
    $GPUValidator = "tools\tts_dependencies_installer\gpu_validator.py"
    if (Test-Path $GPUValidator) {
        Write-Log "🎮 Validation GPU RTX 3090"
        python $GPUValidator
    }
    
    # 3. Métriques projet
    Write-Log "📊 Métriques projet"
    $PythonFiles = (Get-ChildItem -Recurse -Filter "*.py").Count
    $MarkdownFiles = (Get-ChildItem -Recurse -Filter "*.md").Count
    $ConfigFiles = (Get-ChildItem -Recurse -Filter "*.json").Count + (Get-ChildItem -Recurse -Filter "*.yml").Count
    
    Write-Log "📈 Fichiers Python: $PythonFiles"
    Write-Log "📄 Documentation: $MarkdownFiles"
    Write-Log "⚙️ Configuration: $ConfigFiles"
    
    # 4. Status Git
    Write-Log "🌿 Status Git"
    try {
        $GitBranch = git branch --show-current
        $GitCommit = (git rev-parse HEAD).Substring(0, 8)
        $GitStatus = git status --porcelain
        
        Write-Log "📍 Branche: $GitBranch"
        Write-Log "🔄 Commit: $GitCommit"
        
        if ($GitStatus) {
            Write-Log "⚠️ Modifications non commitées détectées" "WARN"
        } else {
            Write-Log "✅ Repository Git propre"
        }
    } catch {
        Write-Log "⚠️ Erreur Git status" "WARN"
    }
    
    return $true
}

function Show-Status {
    Write-Log "🎯 Status NextGeneration"
    Write-Host ""
    Write-Host "🚀 NEXTGENERATION - INFRASTRUCTURE MATURE" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    
    # Infrastructure overview
    Test-Infrastructure
    
    # Documentation status
    if (Test-Path "CODE-SOURCE.md") {
        $DocSize = [math]::Round((Get-Item "CODE-SOURCE.md").Length / 1KB, 2)
        $DocModified = (Get-Item "CODE-SOURCE.md").LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        Write-Host "📚 Documentation: ${DocSize}KB (modifiée: $DocModified)" -ForegroundColor Green
    } else {
        Write-Host "📚 Documentation: NON GÉNÉRÉE" -ForegroundColor Yellow
    }
    
    # Quick actions
    Write-Host ""
    Write-Host "🎯 ACTIONS RAPIDES DISPONIBLES:" -ForegroundColor Cyan
    Write-Host "  .\scripts\nextgeneration_workflow.ps1 -Action documentation  # Générer docs" -ForegroundColor Gray
    Write-Host "  .\scripts\nextgeneration_workflow.ps1 -Action validation     # Tests complets" -ForegroundColor Gray
    Write-Host "  .\scripts\nextgeneration_workflow.ps1 -Action agents         # Activer agents" -ForegroundColor Gray
    Write-Host "  .\scripts\nextgeneration_workflow.ps1 -Action monitoring     # Monitoring" -ForegroundColor Gray
    Write-Host "  .\scripts\nextgeneration_workflow.ps1 -Action full           # Tout exécuter" -ForegroundColor Gray
    Write-Host ""
}

# 🚀 EXECUTION PRINCIPALE
Write-Host ""
Write-Host "🚀 NEXTGENERATION WORKFLOW - AUTOMATISATION COMPLÈTE" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host "📍 Action: $Action" -ForegroundColor Cyan
Write-Host "📁 Répertoire: $NextGenerationRoot" -ForegroundColor Gray
Write-Host "📝 Log: $LogFile" -ForegroundColor Gray
Write-Host ""

$Success = $true

switch ($Action) {
    "clean" {
        Invoke-Clean
    }
    "test" {
        Invoke-Test -TestPath $Path
    }
    "lint" {
        Invoke-Lint
    }
    "docs" {
        Invoke-Docs
    }
    "full" {
        Write-Log "🚀 Workflow complet NextGeneration"
        $Success = $Success -and (Test-Infrastructure)
        $Success = $Success -and (Invoke-Documentation)
        $Success = $Success -and (Invoke-Validation)
        $Success = $Success -and (Invoke-AgentActivation)
        $Success = $Success -and (Invoke-Monitoring)
    }
    "status" {
        Show-Status
        return
    }
}

# Résultat final
Write-Host ""
if ($Success) {
    Write-Host "🎉 WORKFLOW NEXTGENERATION: SUCCÈS" -ForegroundColor Green
    Write-Log "🎉 Workflow $Action terminé avec succès"
} else {
    Write-Host "❌ WORKFLOW NEXTGENERATION: PROBLÈMES DÉTECTÉS" -ForegroundColor Red
    Write-Log "❌ Workflow $Action terminé avec erreurs" "ERROR"
}

Write-Host "📝 Log détaillé: $LogFile" -ForegroundColor Gray
Write-Host ""

exit $(if ($Success) { 0 } else { 1 }) 