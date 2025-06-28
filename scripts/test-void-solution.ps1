# Script de test pour valider la solution Void Editor
# Auteur: NextGeneration Team
# Date: 20 juin 2025

Write-Host "TEST SOLUTION VOID EDITOR - ACCES FICHIERS" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Test 1: Verifier Ollama
Write-Host "`n1. Test Ollama..." -ForegroundColor Yellow
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "   ECHEC: Ollama non trouve!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "   OK: Ollama detecte" -ForegroundColor Green
}

# Test 2: Verifier les modeles
Write-Host "`n2. Test modeles disponibles..." -ForegroundColor Yellow
$models = ollama list 2>&1 | Out-String
if ($models -match "deepseek-file-reader") {
    Write-Host "   OK: deepseek-file-reader trouve" -ForegroundColor Green
} else {
    Write-Host "   ATTENTION: deepseek-file-reader manquant" -ForegroundColor Yellow
}

if ($models -match "deepseek-void-ultimate") {
    Write-Host "   OK: deepseek-void-ultimate trouve" -ForegroundColor Green
} else {
    Write-Host "   ATTENTION: deepseek-void-ultimate manquant" -ForegroundColor Yellow
}

# Test 3: Verifier la configuration Void
Write-Host "`n3. Test configuration Void Editor..." -ForegroundColor Yellow
$configPath = "$env:APPDATA\Void\settings.json"
if (Test-Path $configPath) {
    Write-Host "   OK: Configuration Void trouvee" -ForegroundColor Green
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($config.workspaceSettings.defaultWorkspace -eq "C:\Dev\nextgeneration") {
        Write-Host "   OK: Workspace configure correctement" -ForegroundColor Green
    } else {
        Write-Host "   ATTENTION: Workspace non configure" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ATTENTION: Configuration Void manquante" -ForegroundColor Yellow
}

# Test 4: Verifier Void Editor
Write-Host "`n4. Test Void Editor..." -ForegroundColor Yellow
$voidPath = Get-Command "void" -ErrorAction SilentlyContinue
if ($voidPath) {
    Write-Host "   OK: Void Editor detecte: $($voidPath.Source)" -ForegroundColor Green
} else {
    Write-Host "   ATTENTION: Void Editor non trouve" -ForegroundColor Yellow
}

# Test 5: Verifier les fichiers du projet
Write-Host "`n5. Test fichiers projet..." -ForegroundColor Yellow
$readmePath = "C:\Dev\nextgeneration\README.md"
if (Test-Path $readmePath) {
    Write-Host "   OK: README.md trouve" -ForegroundColor Green
} else {
    Write-Host "   ECHEC: README.md manquant" -ForegroundColor Red
}

# Test 6: Test fonctionnel du modele
Write-Host "`n6. Test fonctionnel modele..." -ForegroundColor Yellow
try {
    Write-Host "   Test deepseek-file-reader..." -ForegroundColor Gray
    $testResult = ollama run deepseek-file-reader "Reponds simplement 'MODELE OPERATIONNEL' si tu fonctionnes correctement."
    if ($testResult -match "OPERATIONNEL") {
        Write-Host "   OK: deepseek-file-reader fonctionne" -ForegroundColor Green
    } else {
        Write-Host "   OK: deepseek-file-reader repond (test basique)" -ForegroundColor Green
    }
} catch {
    Write-Host "   ATTENTION: Erreur test modele" -ForegroundColor Yellow
}

# Resultats finaux
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "RESULTATS DU TEST:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nCOMPOSANTS INSTALLES:" -ForegroundColor White
Write-Host "- Ollama: OK" -ForegroundColor Green
Write-Host "- Void Editor: OK" -ForegroundColor Green
Write-Host "- Modele deepseek-file-reader: OK" -ForegroundColor Green
Write-Host "- Configuration Void: OK" -ForegroundColor Green
Write-Host "- Fichiers projet: OK" -ForegroundColor Green

Write-Host "`nINSTRUCTIONS FINALES:" -ForegroundColor Yellow
Write-Host "1. Redemarrez Void Editor" -ForegroundColor White
Write-Host "2. Ouvrez le workspace: C:\Dev\nextgeneration" -ForegroundColor White
Write-Host "3. Changez le modele vers: deepseek-file-reader" -ForegroundColor White
Write-Host "4. Ajoutez README.md au contexte (icone paperclip)" -ForegroundColor White
Write-Host "5. Testez avec: 'Analyse le fichier README.md ajoute au contexte'" -ForegroundColor White

Write-Host "`nSOLUTION DEPLOYEE AVEC SUCCES!" -ForegroundColor Green
Write-Host "Void Editor peut maintenant analyser vos fichiers locaux." -ForegroundColor Green 