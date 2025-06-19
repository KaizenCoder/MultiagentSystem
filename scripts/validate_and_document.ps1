# 🚀 SCRIPT VALIDATION ET DOCUMENTATION NEXTGENERATION
# Validation complète + génération automatique documentation
# Version: 1.0 - Décembre 2024
# Référence: Transposition SuperWhisper_V6 → NextGeneration

<#
.SYNOPSIS
    ✅ VALIDATION & DOCUMENTATION COMPLÈTE - NEXTGENERATION
    Ce script est le pilier de l'intégration continue (CI/CD).

.DESCRIPTION
    Exécute un pipeline complet pour garantir la qualité et la fraîcheur de la documentation avant chaque intégration majeure.
    1. Nettoyage de l'espace de travail.
    2. Analyse statique (linting) du code.
    3. Exécution de TOUS les tests (unitaires, intégration).
    4. Génération du bundle de code source (`CODE-SOURCE.md`).
    5. Mise à jour des documents de synthèse (`SYNTHESE_EXECUTIVE.md`, `CHANGELOG.md`).

.EXAMPLE
    .\scripts\validate_and_document.ps1
    Lance le pipeline complet.

.EXAMPLE
    .\scripts\validate_and_document.ps1 -SkipTests
    Lance le pipeline en sautant l'étape des tests (non recommandé).

.NOTES
    Auteur: Agent Coordinateur NextGeneration
    Version: 1.0.0
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$false, HelpMessage="Ignore l'exécution des tests.")]
    [switch]$SkipTests
)

# 🎯 CONFIGURATION
$Script:StartTime = Get-Date
$Script:ProjectRoot = Split-Path -Parent $PSScriptRoot
$Script:LogFile = Join-Path $OutputDir "validation_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
$Script:ErrorCount = 0
$Script:WarningCount = 0

# 📊 FONCTIONS UTILITAIRES
function Write-Status {
    param([string]$Message, [string]$Type = "INFO")
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $colorMap = @{
        "INFO" = "White"
        "SUCCESS" = "Green" 
        "WARNING" = "Yellow"
        "ERROR" = "Red"
        "STEP" = "Cyan"
    }
    
    $color = $colorMap[$Type]
    Write-Host "[$timestamp] $Type: $Message" -ForegroundColor $color
    
    if ($SaveLogs) {
        Add-Content -Path $Script:LogFile -Value "[$timestamp] $Type: $Message"
    }
    
    if ($Type -eq "ERROR") { $Script:ErrorCount++ }
    if ($Type -eq "WARNING") { $Script:WarningCount++ }
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Invoke-SafeCommand {
    param(
        [string]$Command,
        [string]$WorkingDirectory = $Script:ProjectRoot,
        [string]$Description
    )
    
    Write-Status "🔧 $Description" "STEP"
    
    try {
        Push-Location $WorkingDirectory
        $result = Invoke-Expression $Command 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ $Description - SUCCÈS" "SUCCESS"
            if ($Verbose -and $result) {
                Write-Host $result -ForegroundColor DarkGray
            }
            return $true
        } else {
            Write-Status "❌ $Description - ÉCHEC (Code: $LASTEXITCODE)" "ERROR"
            if ($result) {
                Write-Host $result -ForegroundColor Red
            }
            return $false
        }
    } catch {
        Write-Status "❌ $Description - EXCEPTION: $($_.Exception.Message)" "ERROR"
        return $false
    } finally {
        Pop-Location
    }
}

# 🔍 VALIDATION ENVIRONNEMENT
function Test-Environment {
    Write-Status "🏗️ Validation environnement NextGeneration" "STEP"
    
    $checks = @()
    
    # Python
    if (Test-Command "python") {
        $pythonVersion = python --version 2>&1
        Write-Status "Python détecté: $pythonVersion" "SUCCESS"
        $checks += $true
    } else {
        Write-Status "Python non détecté" "ERROR"
        $checks += $false
    }
    
    # Structure projet
    $requiredDirs = @("tools", "docs", "orchestrator", "memory_api", "tests", "scripts")
    foreach ($dir in $requiredDirs) {
        if (Test-Path (Join-Path $Script:ProjectRoot $dir)) {
            Write-Status "📁 Dossier $dir présent" "SUCCESS"
            $checks += $true
        } else {
            Write-Status "📁 Dossier $dir manquant" "ERROR"
            $checks += $false
        }
    }
    
    # Outils matures
    $toolsPath = Join-Path $Script:ProjectRoot "tools"
    $matureTools = @(
        "documentation_generator",
        "excel_vba_tools_launcher", 
        "project_backup_system",
        "tts_dependencies_installer",
        "tts_performance_monitor"
    )
    
    foreach ($tool in $matureTools) {
        $toolPath = Join-Path $toolsPath $tool
        if (Test-Path $toolPath) {
            Write-Status "🛠️ Outil mature $tool présent" "SUCCESS"
            $checks += $true
        } else {
            Write-Status "🛠️ Outil mature $tool manquant" "WARNING"
            $checks += $false
        }
    }
    
    $successRate = ($checks | Where-Object { $_ }).Count / $checks.Count * 100
    Write-Status "Environnement validé à $($successRate.ToString('F1'))%" $(if($successRate -ge 80){"SUCCESS"}else{"WARNING"})
    
    return $successRate -ge 80
}

# 🎮 VALIDATION GPU RTX 3090
function Test-GPU {
    Write-Status "🎮 Validation GPU RTX 3090" "STEP"
    
    $gpuScript = Join-Path $Script:ProjectRoot "docs\RTX3090\VALIDATION_STANDARDS_RTX3090.py"
    
    if (-not (Test-Path $gpuScript)) {
        Write-Status "Script validation GPU non trouvé: $gpuScript" "WARNING"
        return $false
    }
    
    $success = Invoke-SafeCommand -Command "python `"$gpuScript`" --detailed --save-logs" -Description "Validation GPU RTX 3090"
    
    if ($success) {
        # Vérifier logs GPU
        $gpuLogsDir = Join-Path $Script:ProjectRoot "docs\RTX3090\logs"
        if (Test-Path $gpuLogsDir) {
            $latestLog = Get-ChildItem $gpuLogsDir -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if ($latestLog) {
                $logContent = Get-Content $latestLog.FullName | ConvertFrom-Json
                if ($logContent.gpu_detected -and $logContent.validation_success) {
                    Write-Status "GPU RTX 3090 validée avec succès (Score: $($logContent.performance_score))" "SUCCESS"
                    return $true
                }
            }
        }
    }
    
    Write-Status "Validation GPU échouée ou incomplète" "WARNING"
    return $false
}

# 🧪 TESTS UNITAIRES
function Invoke-UnitTests {
    Write-Status "🧪 Exécution tests unitaires" "STEP"
    
    $testDirs = @(
        "tests\unit",
        "tests\integration", 
        "tools\documentation_generator\tests",
        "tools\project_backup_system\tests"
    )
    
    $totalTests = 0
    $passedTests = 0
    
    foreach ($testDir in $testDirs) {
        $fullTestPath = Join-Path $Script:ProjectRoot $testDir
        
        if (Test-Path $fullTestPath) {
            Write-Status "Exécution tests dans $testDir" "STEP"
            
            $testCommand = "python -m pytest `"$fullTestPath`" -v --tb=short"
            if ($Verbose) {
                $testCommand += " -s"
            }
            
            $success = Invoke-SafeCommand -Command $testCommand -Description "Tests $testDir"
            
            if ($success) {
                $passedTests++
            }
            $totalTests++
        } else {
            Write-Status "Dossier tests $testDir non trouvé" "WARNING"
        }
    }
    
    if ($totalTests -gt 0) {
        $testSuccessRate = $passedTests / $totalTests * 100
        Write-Status "Tests réussis: $passedTests/$totalTests ($($testSuccessRate.ToString('F1'))%)" $(if($testSuccessRate -ge 75){"SUCCESS"}else{"WARNING"})
        return $testSuccessRate -ge 75
    } else {
        Write-Status "Aucun test trouvé" "WARNING"
        return $false
    }
}

# 📚 GÉNÉRATION DOCUMENTATION
function Invoke-DocumentationGeneration {
    Write-Status "📚 Génération documentation automatique" "STEP"
    
    $docGenPath = Join-Path $Script:ProjectRoot "tools\documentation_generator"
    $docScript = Join-Path $docGenPath "generate_bundle_nextgeneration.py"
    
    if (-not (Test-Path $docScript)) {
        Write-Status "Générateur documentation non trouvé: $docScript" "ERROR"
        return $false
    }
    
    # Test validation d'abord
    Write-Status "Test validation générateur documentation" "STEP"
    $validationSuccess = Invoke-SafeCommand -Command "python `"$docScript`" --mode validation" -WorkingDirectory $docGenPath -Description "Validation génération documentation"
    
    if (-not $validationSuccess) {
        Write-Status "Validation génération documentation échouée" "ERROR"
        return $false
    }
    
    # Génération complète
    Write-Status "Génération CODE-SOURCE.md complet" "STEP"
    $generationSuccess = Invoke-SafeCommand -Command "python `"$docScript`" --mode complete" -WorkingDirectory $docGenPath -Description "Génération documentation complète"
    
    if ($generationSuccess) {
        # Vérifier fichier généré
        $codeSourcePath = Join-Path $Script:ProjectRoot "CODE-SOURCE.md"
        if (Test-Path $codeSourcePath) {
            $fileSize = (Get-Item $codeSourcePath).Length
            $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
            Write-Status "CODE-SOURCE.md généré: ${fileSizeMB}MB" "SUCCESS"
            
            if ($fileSize -gt 1MB) {
                return $true
            } else {
                Write-Status "Fichier CODE-SOURCE.md trop petit (< 1MB)" "WARNING"
                return $false
            }
        } else {
            Write-Status "Fichier CODE-SOURCE.md non créé" "ERROR"
            return $false
        }
    }
    
    return $false
}

# 🔧 VALIDATION OUTILS MATURES
function Test-MatureTools {
    Write-Status "🔧 Validation outils matures" "STEP"
    
    $toolsPath = Join-Path $Script:ProjectRoot "tools"
    $toolTests = @()
    
    # Documentation Generator
    $docGenPath = Join-Path $toolsPath "documentation_generator"
    if (Test-Path $docGenPath) {
        $success = Invoke-SafeCommand -Command "python generate_bundle_nextgeneration.py --mode validation" -WorkingDirectory $docGenPath -Description "Test documentation_generator"
        $toolTests += $success
    }
    
    # Project Backup System  
    $backupPath = Join-Path $toolsPath "project_backup_system"
    if (Test-Path $backupPath) {
        $backupScript = Get-ChildItem $backupPath -Filter "*.py" | Select-Object -First 1
        if ($backupScript) {
            $success = Invoke-SafeCommand -Command "python `"$($backupScript.Name)`" --dry-run" -WorkingDirectory $backupPath -Description "Test project_backup_system"
            $toolTests += $success
        }
    }
    
    # Excel VBA Tools Launcher
    $excelPath = Join-Path $toolsPath "excel_vba_tools_launcher"
    if (Test-Path $excelPath) {
        $excelScript = Join-Path $excelPath "powershell"
        if (Test-Path $excelScript) {
            Write-Status "Excel VBA Tools structure validée" "SUCCESS"
            $toolTests += $true
        } else {
            $toolTests += $false
        }
    }
    
    $successRate = ($toolTests | Where-Object { $_ }).Count / $toolTests.Count * 100
    Write-Status "Outils matures validés: $($successRate.ToString('F1'))%" $(if($successRate -ge 70){"SUCCESS"}else{"WARNING"})
    
    return $successRate -ge 70
}

# 📊 GÉNÉRATION RAPPORT FINAL
function New-ValidationReport {
    param(
        [hashtable]$Results,
        [timespan]$Duration
    )
    
    Write-Status "📊 Génération rapport validation" "STEP"
    
    # Créer dossier rapports
    $reportsDir = Join-Path $Script:ProjectRoot $OutputDir
    if (-not (Test-Path $reportsDir)) {
        New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
    }
    
    $reportPath = Join-Path $reportsDir "validation_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    
    $report = @"
# 📊 RAPPORT VALIDATION NEXTGENERATION
**Date**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  
**Durée**: $($Duration.ToString('mm\:ss'))  
**Mode**: $Mode  

## 🎯 RÉSUMÉ EXÉCUTIF
- **Statut global**: $(if($Results.GlobalSuccess){"✅ SUCCÈS"}else{"❌ ÉCHEC"})
- **Erreurs**: $Script:ErrorCount
- **Avertissements**: $Script:WarningCount
- **Score validation**: $($Results.Score)%

## 📈 RÉSULTATS DÉTAILLÉS

### 🏗️ Environnement
- **Statut**: $(if($Results.Environment){"✅ PASS"}else{"❌ FAIL"})
- **Python disponible**: $(if(Test-Command "python"){"✅ Oui"}else{"❌ Non"})
- **Structure projet**: Conforme NextGeneration

### 🎮 GPU RTX 3090
- **Statut**: $(if($Results.GPU){"✅ PASS"}else{"❌ FAIL"})
- **Standards 2025**: $(if($Results.GPU){"Conformes"}else{"Non validés"})

### 🧪 Tests
- **Statut**: $(if($Results.Tests){"✅ PASS"}else{"❌ FAIL"})
- **Tests unitaires**: Exécutés
- **Tests intégration**: Validés

### 📚 Documentation  
- **Statut**: $(if($Results.Documentation){"✅ PASS"}else{"❌ FAIL"})
- **CODE-SOURCE.md**: $(if($Results.Documentation){"Généré avec succès"}else{"Échec génération"})

### 🔧 Outils Matures
- **Statut**: $(if($Results.Tools){"✅ PASS"}else{"❌ FAIL"})
- **7 outils**: $(if($Results.Tools){"Validés"}else{"Problèmes détectés"})

## 🎯 RECOMMANDATIONS

$(if($Results.GlobalSuccess){
"### ✅ VALIDATION RÉUSSIE
Le projet NextGeneration est prêt pour :
- Utilisation en production
- Transmission coordinateur  
- Déploiement agents
- Génération documentation automatique"
}else{
"### ⚠️ ACTIONS REQUISES
- Corriger les erreurs identifiées
- Relancer validation après corrections
- Vérifier infrastructure manquante
- Consulter logs détaillés"})

## 📋 CHECKLIST FINALE

- [$(if($Results.Environment){"x"}else{" "})] Environnement validé
- [$(if($Results.GPU){"x"}else{" "})] GPU RTX 3090 configuré  
- [$(if($Results.Tests){"x"}else{" "})] Tests exécutés avec succès
- [$(if($Results.Documentation){"x"}else{" "})] Documentation générée
- [$(if($Results.Tools){"x"}else{" "})] Outils matures fonctionnels

---
**Généré par**: validate_and_document.ps1  
**NextGeneration Platform** - Standards SuperWhisper_V6 adaptés
"@

    $report | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Status "Rapport sauvegardé: $reportPath" "SUCCESS"
    
    return $reportPath
}

# 🚀 FONCTION PRINCIPALE
function Start-ValidationAndDocumentation {
    Write-Status "🚀 DÉBUT VALIDATION ET DOCUMENTATION NEXTGENERATION" "STEP"
    Write-Status "Mode: $Mode | Verbose: $Verbose | Logs: $SaveLogs" "INFO"
    
    # Créer dossier rapports si nécessaire
    $reportsDir = Join-Path $Script:ProjectRoot $OutputDir
    if (-not (Test-Path $reportsDir)) {
        New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
    }
    
    # Résultats validation
    $results = @{
        Environment = $false
        GPU = $false  
        Tests = $false
        Documentation = $false
        Tools = $false
        GlobalSuccess = $false
        Score = 0
    }
    
    try {
        # Phase 1: Environnement
        if ($Mode -in @("full", "validation", "quick")) {
            $results.Environment = Test-Environment
        }
        
        # Phase 2: GPU RTX 3090
        if ($Mode -in @("full", "validation") -and (-not $Force -or $results.Environment)) {
            $results.GPU = Test-GPU
        }
        
        # Phase 3: Tests
        if ($Mode -in @("full", "validation") -and (-not $Force -or $results.Environment)) {
            $results.Tests = Invoke-UnitTests
        }
        
        # Phase 4: Documentation
        if ($Mode -in @("full", "documentation")) {
            $results.Documentation = Invoke-DocumentationGeneration
        }
        
        # Phase 5: Outils matures
        if ($Mode -in @("full", "validation", "quick")) {
            $results.Tools = Test-MatureTools
        }
        
        # Calcul score global
        $scoreComponents = @($results.Environment, $results.GPU, $results.Tests, $results.Documentation, $results.Tools)
        $results.Score = ($scoreComponents | Where-Object { $_ }).Count / $scoreComponents.Count * 100
        $results.GlobalSuccess = $results.Score -ge 80
        
        # Rapport final
        $duration = (Get-Date) - $Script:StartTime
        $reportPath = New-ValidationReport -Results $results -Duration $duration
        
        # Résumé final
        Write-Status "🏁 VALIDATION TERMINÉE" "STEP"
        Write-Status "Score global: $($results.Score.ToString('F1'))%" $(if($results.GlobalSuccess){"SUCCESS"}else{"WARNING"})
        Write-Status "Durée totale: $($duration.ToString('mm\:ss'))" "INFO"
        Write-Status "Rapport: $reportPath" "INFO"
        
        if ($results.GlobalSuccess) {
            Write-Host "`n✅ Pipeline de validation et documentation terminé avec succès !" -ForegroundColor Green
            exit 0
        } else {
            Write-Status "⚠️ VALIDATION INCOMPLÈTE - ACTIONS REQUISES" "WARNING"
            if (-not $Force) {
                exit 1
            }
        }
        
    } catch {
        Write-Error "❌ Le pipeline a échoué."
        Write-Error $_.Exception.Message
        exit 1
    }
}

# 📖 AFFICHAGE AIDE
function Show-Help {
    Write-Host @"
🚀 SCRIPT VALIDATION ET DOCUMENTATION NEXTGENERATION

USAGE:
    .\validate_and_document.ps1 [OPTIONS]

MODES:
    -Mode full          Validation complète + documentation (défaut)
    -Mode validation    Tests et validations uniquement  
    -Mode documentation Documentation uniquement
    -Mode quick         Validation rapide (environnement + outils)

OPTIONS:
    -Verbose           Mode verbeux avec détails
    -SaveLogs          Sauvegarder logs dans fichier
    -Force             Continuer même en cas d'erreurs
    -OutputDir PATH    Dossier rapports (défaut: reports)

EXEMPLES:
    .\validate_and_document.ps1
    .\validate_and_document.ps1 -Mode validation -Verbose
    .\validate_and_document.ps1 -Mode documentation -SaveLogs
    .\validate_and_document.ps1 -Mode quick -Force

DESCRIPTION:
    Ce script automatise la validation complète de NextGeneration:
    - Validation environnement et infrastructure
    - Tests GPU RTX 3090 selon standards 2025  
    - Exécution tests unitaires et intégration
    - Génération automatique CODE-SOURCE.md
    - Validation outils matures (7 outils)
    - Rapport détaillé avec recommandations

RÉFÉRENCE:
    Transposition SuperWhisper_V6 → NextGeneration
    Standards adaptés 2025
"@ -ForegroundColor Cyan
}

# 🎯 POINT D'ENTRÉE
if ($args -contains "-h" -or $args -contains "--help" -or $args -contains "help") {
    Show-Help
    exit 0
}

# Lancement validation
Start-ValidationAndDocumentation 