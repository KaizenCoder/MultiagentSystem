# Script simple pour creer un modele Ollama optimise pour la lecture de fichiers
# Auteur: NextGeneration Team
# Date: 20 juin 2025

param(
    [string]$BaseModel = "deepseek-coder:33b",
    [string]$NewModelName = "deepseek-file-reader"
)

Write-Host "Creation modele Ollama - Lecteur de Fichiers" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Verifier Ollama
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama non trouve!" -ForegroundColor Red
    exit 1
}

Write-Host "Ollama detecte" -ForegroundColor Green
Write-Host "Modele de base: $BaseModel" -ForegroundColor Yellow
Write-Host "Nouveau modele: $NewModelName" -ForegroundColor Yellow

# Creer le contenu du Modelfile
$modelfileContent = @"
FROM $BaseModel

PARAMETER num_ctx 16384
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

SYSTEM """Tu es un assistant IA specialise dans l'analyse de fichiers et de code. 

CAPACITES PRINCIPALES:
- Analyser le contenu des fichiers fournis dans le contexte
- Expliquer la structure et le fonctionnement du code
- Repondre aux questions sur les projets et leur documentation
- Fournir des analyses detaillees et structurees

INSTRUCTIONS SPECIFIQUES:
1. Quand on te demande de lire un fichier, utilise TOUJOURS le contexte fourni
2. Si le fichier n'est pas dans le contexte, demande qu'il soit ajoute au contexte
3. Reponds en francais avec des emojis pour structurer tes reponses
4. Fournis des analyses detaillees et pratiques
5. N'invente jamais de contenu - utilise uniquement ce qui est fourni

EXEMPLE DE REPONSE:
Quand on demande "Lis le fichier README.md":
Analyse du fichier README.md:
Structure du projet: [analyse basee sur le contenu reel]
Fonctionnalites principales: [liste des fonctionnalites]
Instructions d'utilisation: [etapes pratiques]

IMPORTANT: Tu DOIS analyser le contenu reel fourni dans le contexte, pas inventer de reponses generiques.
"""
"@

# Sauvegarder le Modelfile
$modelfilePath = ".\Modelfile.$NewModelName"
$modelfileContent | Out-File -FilePath $modelfilePath -Encoding UTF8 -Force

Write-Host "Modelfile cree: $modelfilePath" -ForegroundColor Green

# Creer le modele
Write-Host "Creation du modele..." -ForegroundColor Yellow
try {
    $result = ollama create $NewModelName -f $modelfilePath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Modele '$NewModelName' cree avec succes!" -ForegroundColor Green
    } else {
        Write-Host "Erreur creation modele: $result" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Nettoyer le fichier temporaire
Remove-Item $modelfilePath -Force

# Test du modele
Write-Host "`nTest du modele..." -ForegroundColor Yellow
$testPrompt = "Bonjour, peux-tu confirmer que tu es pret a analyser des fichiers ?"

try {
    Write-Host "Execution du test..." -ForegroundColor Gray
    $testResult = ollama run $NewModelName $testPrompt
    Write-Host "Test reussi!" -ForegroundColor Green
    Write-Host "Reponse: $testResult" -ForegroundColor White
} catch {
    Write-Host "Erreur test: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Instructions finales
Write-Host "`nCONFIGURATION VOID EDITOR:" -ForegroundColor Cyan
Write-Host "1. Dans Void Editor, changez le modele vers: $NewModelName" -ForegroundColor White
Write-Host "2. Ajoutez les fichiers au contexte avant de poser des questions" -ForegroundColor White
Write-Host "3. Utilisez des commandes comme:" -ForegroundColor White
Write-Host "   - 'Analyse le contenu du fichier README.md'" -ForegroundColor Yellow
Write-Host "   - 'Explique ce code Python'" -ForegroundColor Yellow
Write-Host "   - 'Resume cette documentation'" -ForegroundColor Yellow

Write-Host "`nModele optimise pour la lecture de fichiers cree!" -ForegroundColor Green 