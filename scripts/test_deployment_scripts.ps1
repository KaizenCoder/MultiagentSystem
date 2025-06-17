# Script de test pour valider les scripts de déploiement
# Usage: .\test_deployment_scripts.ps1

Write-Host "🧪 Testing Deployment Scripts Validation" -ForegroundColor Green

# Test 1: Vérifier que tous les scripts existent
$scripts = @(
    "blue-green-deploy.ps1",
    "canary-deploy.ps1", 
    "validate_security_final.ps1"
)

$scriptsPath = "c:\Dev\nextgeneration\scripts"

foreach ($script in $scripts) {
    $fullPath = Join-Path $scriptsPath $script
    if (Test-Path $fullPath) {
        Write-Host "✅ $script exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $script missing" -ForegroundColor Red
    }
}

# Test 2: Validation syntaxe PowerShell
Write-Host "`n🔍 Validating PowerShell Syntax..." -ForegroundColor Blue

foreach ($script in $scripts) {
    $fullPath = Join-Path $scriptsPath $script
    if (Test-Path $fullPath) {
        try {
            $errors = $null
            $tokens = $null
            $ast = [System.Management.Automation.Language.Parser]::ParseFile($fullPath, [ref]$tokens, [ref]$errors)
            
            if ($errors.Count -eq 0) {
                Write-Host "✅ $script syntax valid" -ForegroundColor Green
            } else {
                Write-Host "❌ $script syntax errors: $($errors.Count)" -ForegroundColor Red
            }
        } catch {
            Write-Host "❌ $script parse error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Test 3: Vérifier les paramètres des scripts
Write-Host "`n📋 Checking Script Parameters..." -ForegroundColor Blue

# Test Blue/Green script
try {
    Get-Help "c:\Dev\nextgeneration\scripts\blue-green-deploy.ps1" -Parameter * | Out-Null
    Write-Host "✅ blue-green-deploy.ps1 parameters valid" -ForegroundColor Green
} catch {
    Write-Host "❌ blue-green-deploy.ps1 parameter issue: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Canary script  
try {
    Get-Help "c:\Dev\nextgeneration\scripts\canary-deploy.ps1" -Parameter * | Out-Null
    Write-Host "✅ canary-deploy.ps1 parameters valid" -ForegroundColor Green
} catch {
    Write-Host "❌ canary-deploy.ps1 parameter issue: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Security script
try {
    Get-Help "c:\Dev\nextgeneration\scripts\validate_security_final.ps1" -Parameter * | Out-Null
    Write-Host "✅ validate_security_final.ps1 parameters valid" -ForegroundColor Green
} catch {
    Write-Host "❌ validate_security_final.ps1 parameter issue: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Deployment Scripts Validation Complete!" -ForegroundColor Green
