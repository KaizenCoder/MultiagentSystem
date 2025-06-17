# Security Validation Script for Windows
# Phase 1 Sprint 1.4 - Production-Ready Security Audit
# Date: June 17, 2025

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [string]$ReportPath = "security_audit_report.json",
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Configuration
$ORCHESTRATOR_URL = $env:ORCHESTRATOR_URL ?? "http://localhost:8002"
$MEMORY_API_URL = $env:MEMORY_API_URL ?? "http://localhost:8001"

# Security test results
$SecurityResults = @{
    Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Environment = $Environment
    Tests = @()
    Summary = @{
        Total = 0
        Passed = 0
        Failed = 0
        Critical = 0
        High = 0
        Medium = 0
        Low = 0
    }
}

Write-Host "🔒 Starting Security Validation Audit" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Target URLs:" -ForegroundColor Yellow
Write-Host "  - Orchestrator: $ORCHESTRATOR_URL" -ForegroundColor White
Write-Host "  - Memory API: $MEMORY_API_URL" -ForegroundColor White

# Function to add test result
function Add-TestResult {
    param(
        [string]$TestName,
        [string]$Category,
        [string]$Severity,
        [bool]$Passed,
        [string]$Description,
        [string]$Details = ""
    )
    
    $result = @{
        Name = $TestName
        Category = $Category
        Severity = $Severity
        Passed = $Passed
        Description = $Description
        Details = $Details
        Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    }
    
    $SecurityResults.Tests += $result
    $SecurityResults.Summary.Total++
    
    if ($Passed) {
        $SecurityResults.Summary.Passed++
        $status = "✅ PASS"
        $color = "Green"
    } else {
        $SecurityResults.Summary.Failed++
        $status = "❌ FAIL"
        $color = "Red"
        
        switch ($Severity) {
            "Critical" { $SecurityResults.Summary.Critical++ }
            "High" { $SecurityResults.Summary.High++ }
            "Medium" { $SecurityResults.Summary.Medium++ }
            "Low" { $SecurityResults.Summary.Low++ }
        }
    }
    
    Write-Host "$status [$Severity] $TestName" -ForegroundColor $color
    if ($Verbose -and $Details) {
        Write-Host "    Details: $Details" -ForegroundColor Gray
    }
}

# Function to test HTTP endpoint
function Test-HTTPEndpoint {
    param(
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [int]$ExpectedStatus = 200,
        [int]$TimeoutSeconds = 10
    )
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $Headers
            TimeoutSec = $TimeoutSeconds
            UseBasicParsing = $true
        }
        
        if ($Body) {
            $params.Body = $Body
        }
        
        $response = Invoke-WebRequest @params
        
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            Headers = $response.Headers
            Content = $response.Content
        }
    }
    catch {
        return @{
            Success = $false
            StatusCode = $_.Exception.Response.StatusCode.value__ ?? 0
            Error = $_.Exception.Message
        }
    }
}
    
    $script:TotalChecks++
    if ($Passed) {
        $script:PassedChecks++
        Write-Host "✅ $TestName" -ForegroundColor Green
        if ($Message) { Write-Host "   $Message" -ForegroundColor Gray }
    } else {
        Write-Host "❌ $TestName" -ForegroundColor Red
        if ($Message) { Write-Host "   $Message" -ForegroundColor Yellow }
        $script:CriticalIssues += $TestName
    }
}

function Test-PythonCommand {
    param([string]$Command)
    
    try {
        $result = Invoke-Expression "python -c `"$Command`""
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Test-Dependencies {
    Write-Host "🔍 Vérification des dépendances..." -ForegroundColor Blue
    
    $requiredPackages = @(
        "bandit", "safety", "pytest", "pytest-cov", 
        "structlog", "cryptography", "fastapi", "httpx"
    )
    
    $missingPackages = @()
    foreach ($package in $requiredPackages) {
        if (-not (Test-PythonCommand "import $package")) {
            $missingPackages += $package
        }
    }
    
    if ($missingPackages.Count -gt 0) {
        Write-CheckResult "Dependencies Check" $false "Packages manquants: $($missingPackages -join ', ')"
        
        if (-not $SkipInstall) {
            Write-Host "📦 Installation des dépendances manquantes..." -ForegroundColor Yellow
            try {
                & python -m pip install -r (Join-Path $OrchestratorPath "requirements.txt")
                & python -m pip install -r (Join-Path $OrchestratorPath "requirements-dev.txt")
                Write-Host "✅ Dépendances installées" -ForegroundColor Green
                return $true
            } catch {
                Write-Host "❌ Erreur d'installation: $_" -ForegroundColor Red
                return $false
            }
        } else {
            return $false
        }
    } else {
        Write-CheckResult "Dependencies Check" $true "Toutes les dépendances sont disponibles"
        return $true
    }
}

function Test-BanditScan {
    Write-Host "🛡️ Scan Bandit (SAST)..." -ForegroundColor Blue
    
    try {
        # Scan avec rapport JSON
        $banditArgs = @(
            "-r", $OrchestratorPath,
            "-f", "json",
            "-o", (Join-Path $ProjectPath "bandit-report.json")
        )
        
        & bandit @banditArgs 2>$null
        $banditExitCode = $LASTEXITCODE
        
        # Analyse du rapport
        $reportFile = Join-Path $ProjectPath "bandit-report.json"
        if (Test-Path $reportFile) {
            $report = Get-Content $reportFile | ConvertFrom-Json
            $highIssues = $report.results | Where-Object { $_.issue_severity -eq "HIGH" }
            $mediumIssues = $report.results | Where-Object { $_.issue_severity -eq "MEDIUM" }
            
            if ($highIssues.Count -gt 0) {
                Write-CheckResult "Bandit SAST Scan" $false "$($highIssues.Count) vulnérabilités HIGH détectées"
                return $false
            } else {
                Write-CheckResult "Bandit SAST Scan" $true "Aucune vulnérabilité HIGH (Medium: $($mediumIssues.Count))"
                return $true
            }
        } else {
            Write-CheckResult "Bandit SAST Scan" $false "Rapport non généré"
            return $false
        }
    } catch {
        Write-CheckResult "Bandit SAST Scan" $false "Erreur d'exécution: $_"
        return $false
    }
}

function Test-SafetyCheck {
    Write-Host "📦 Scan Safety (dépendances)..." -ForegroundColor Blue
    
    try {
        $safetyArgs = @(
            "check",
            "--json",
            "--output", (Join-Path $ProjectPath "safety-report.json")
        )
        
        & safety @safetyArgs 2>$null
        $safetyExitCode = $LASTEXITCODE
        
        if ($safetyExitCode -eq 0) {
            Write-CheckResult "Safety Dependencies Scan" $true "Aucune vulnérabilité connue"
            return $true
        } else {
            $reportFile = Join-Path $ProjectPath "safety-report.json"
            if (Test-Path $reportFile) {
                $report = Get-Content $reportFile | ConvertFrom-Json
                $vulnCount = $report.vulnerabilities.Count
                Write-CheckResult "Safety Dependencies Scan" $false "$vulnCount vulnérabilités détectées"
            } else {
                Write-CheckResult "Safety Dependencies Scan" $false "Vulnérabilités détectées (voir rapport)"
            }
            return $false
        }
    } catch {
        Write-CheckResult "Safety Dependencies Scan" $false "Erreur d'exécution: $_"
        return $false
    }
}

function Test-SecurityTests {
    Write-Host "🧪 Tests de sécurité critiques..." -ForegroundColor Blue
    
    $securityTests = @(
        "tests\security\test_rce_prevention.py",
        "tests\security\test_ssrf_prevention.py"
    )
    
    $allPassed = $true
    foreach ($testFile in $securityTests) {
        $testPath = Join-Path $ProjectPath $testFile
        
        if (-not (Test-Path $testPath)) {
            Write-Host "   ❌ Test manquant: $testFile" -ForegroundColor Red
            $allPassed = $false
            continue
        }
        
        try {
            Write-Host "   Running $testFile..." -ForegroundColor Gray
            & pytest $testPath -v --tb=short 2>$null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ $testFile - PASSED" -ForegroundColor Green
            } else {
                Write-Host "   ❌ $testFile - FAILED" -ForegroundColor Red
                $allPassed = $false
            }
        } catch {
            Write-Host "   ❌ $testFile - ERROR: $_" -ForegroundColor Red
            $allPassed = $false
        }
    }
    
    Write-CheckResult "Security Tests" $allPassed "Tests RCE/SSRF"
    return $allPassed
}

function Test-Coverage {
    if ($Quick) {
        Write-Host "⏩ Skip coverage test (mode quick)" -ForegroundColor Yellow
        return $true
    }
    
    Write-Host "📊 Couverture de tests..." -ForegroundColor Blue
    
    try {
        $coverageArgs = @(
            "--cov=orchestrator",
            "--cov-report=term-missing",
            "--cov-fail-under=40",
            (Join-Path $ProjectPath "tests")
        )
        
        & pytest @coverageArgs 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-CheckResult "Test Coverage" $true "Couverture ≥ 40%"
            return $true
        } else {
            Write-CheckResult "Test Coverage" $false "Couverture < 40%"
            return $false
        }
    } catch {
        Write-CheckResult "Test Coverage" $false "Erreur d'exécution: $_"
        return $false
    }
}

function Test-HardcodedSecrets {
    Write-Host "🔑 Recherche de secrets hardcodés..." -ForegroundColor Blue
    
    $dangerousPatterns = @(
        "sk-[a-zA-Z0-9]+",           # OpenAI API keys
        "xoxb-[a-zA-Z0-9-]+",       # Slack tokens
        "ghp_[a-zA-Z0-9]+",         # GitHub tokens
        "your_secret_key_here",
        "api[_-]key.*=.*[`"'][^`"']*[`"']",
        "secret.*=.*[`"'][^`"']*[`"']"
    )
    
    $foundSecrets = @()
    foreach ($pattern in $dangerousPatterns) {
        try {
            $matches = Select-String -Path (Join-Path $OrchestratorPath "*") -Pattern $pattern -Recurse 2>$null
            if ($matches) {
                $foundSecrets += $matches
            }
        } catch {
            # Ignorer les erreurs de recherche
        }
    }
    
    if ($foundSecrets.Count -gt 0) {
        Write-CheckResult "Hardcoded Secrets Check" $false "$($foundSecrets.Count) secrets potentiels détectés"
        return $false
    } else {
        Write-CheckResult "Hardcoded Secrets Check" $true "Aucun secret hardcodé détecté"
        return $true
    }
}

function Test-HealthChecks {
    Write-Host "💓 Vérification des health checks..." -ForegroundColor Blue
    
    $healthFiles = @(
        "orchestrator\app\health\comprehensive_health.py",
        "orchestrator\app\observability\structured_logging.py",
        "orchestrator\app\security\secure_analyzer.py"
    )
    
    $allExist = $true
    foreach ($healthFile in $healthFiles) {
        $healthPath = Join-Path $ProjectPath $healthFile
        if (-not (Test-Path $healthPath)) {
            Write-Host "   ❌ Fichier manquant: $healthFile" -ForegroundColor Red
            $allExist = $false
        }
    }
    
    Write-CheckResult "Health Checks Components" $allExist "Fichiers de monitoring"
    return $allExist
}

function Generate-SecurityReport {
    $report = @{
        timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        version = "quick-wins-sprint-1"
        status = if ($PassedChecks -eq $TotalChecks) { "PASS" } else { "FAIL" }
        total_checks = $TotalChecks
        passed_checks = $PassedChecks
        critical_issues = $CriticalIssues
        windows_environment = $true
        powershell_version = $PSVersionTable.PSVersion.ToString()
    }
    
    $reportFile = Join-Path $ProjectPath "security-validation-report.json"
    $report | ConvertTo-Json -Depth 3 | Set-Content $reportFile
    
    Write-Host "📋 Rapport généré: $reportFile" -ForegroundColor Gray
}

# ============================================================================
# EXÉCUTION PRINCIPALE
# ============================================================================

Write-Host "🎯 Mode: $(if ($Quick) { 'QUICK' } else { 'COMPLET' })" -ForegroundColor Cyan
Write-Host "📁 Projet: $ProjectPath" -ForegroundColor Gray
Write-Host ""

# Changement vers le répertoire du projet
Set-Location $ProjectPath

try {
    # Exécution des validations
    $validations = @(
        { Test-Dependencies },
        { Test-BanditScan },
        { Test-SafetyCheck },
        { Test-SecurityTests },
        { Test-Coverage },
        { Test-HardcodedSecrets },
        { Test-HealthChecks }
    )
    
    foreach ($validation in $validations) {
        try {
            & $validation
        } catch {
            Write-Host "❌ Erreur lors de la validation: $_" -ForegroundColor Red
            $TotalChecks++
        }
        Write-Host ""
    }
    
    # Génération du rapport
    Generate-SecurityReport
    
    # Résumé final
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host "📋 RÉSUMÉ DE LA VALIDATION" -ForegroundColor Cyan
    Write-Host "✅ Checks passés: $PassedChecks/$TotalChecks" -ForegroundColor Green
    
    if ($PassedChecks -eq $TotalChecks) {
        Write-Host "🎉 VALIDATION RÉUSSIE - Prêt pour déploiement staging" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "❌ VALIDATION ÉCHOUÉE - Correctifs requis" -ForegroundColor Red
        Write-Host "Issues critiques:" -ForegroundColor Yellow
        foreach ($issue in $CriticalIssues) {
            Write-Host "   • $issue" -ForegroundColor Red
        }
        exit 1
    }
    
} catch {
    Write-Host "💥 Erreur fatale: $_" -ForegroundColor Red
    exit 1
}
