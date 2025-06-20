# Script pour créer un modèle Ollama optimisé pour la lecture de fichiers
# Auteur: NextGeneration Team
# Date: 20 juin 2025

param(
    [string]$BaseModel = "deepseek-coder:33b",
    [string]$NewModelName = "deepseek-file-reader"
)

Write-Host "📄 Création modèle Ollama - Lecteur de Fichiers" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Vérifier Ollama
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Ollama non trouvé!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Ollama détecté" -ForegroundColor Green
Write-Host "📋 Modèle de base: $BaseModel" -ForegroundColor Yellow
Write-Host "🎯 Nouveau modèle: $NewModelName" -ForegroundColor Yellow

# Créer le Modelfile
$modelfile = @"
FROM $BaseModel

# Configuration performance
PARAMETER num_ctx 16384
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# Instructions système pour lecture de fichiers
SYSTEM """Tu es un assistant IA spécialisé dans l'analyse de fichiers et de code. 

🔍 CAPACITÉS PRINCIPALES:
- Analyser le contenu des fichiers fournis dans le contexte
- Expliquer la structure et le fonctionnement du code
- Répondre aux questions sur les projets et leur documentation
- Fournir des analyses détaillées et structurées

📋 INSTRUCTIONS SPÉCIFIQUES:
1. Quand on te demande de lire un fichier, utilise TOUJOURS le contexte fourni
2. Si le fichier n'est pas dans le contexte, demande qu'il soit ajouté au contexte
3. Réponds en français avec des emojis pour structurer tes réponses
4. Fournis des analyses détaillées et pratiques
5. N'invente jamais de contenu - utilise uniquement ce qui est fourni

🎯 EXEMPLE DE RÉPONSE:
Quand on demande "Lis le fichier README.md":
✅ Analyse du fichier README.md:
🏗️ Structure du projet: [analyse basée sur le contenu réel]
📊 Fonctionnalités principales: [liste des fonctionnalités]
🔧 Instructions d'utilisation: [étapes pratiques]

⚠️ IMPORTANT: Tu DOIS analyser le contenu réel fourni dans le contexte, pas inventer de réponses génériques.
"""

# Template de réponse pour lecture de fichiers
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""
"@

# Sauvegarder le Modelfile
$modelfilePath = ".\Modelfile.$NewModelName"
$modelfile | Out-File -FilePath $modelfilePath -Encoding UTF8 -Force

Write-Host "📄 Modelfile créé: $modelfilePath" -ForegroundColor Green

# Créer le modèle
Write-Host "🔨 Création du modèle..." -ForegroundColor Yellow
try {
    $result = ollama create $NewModelName -f $modelfilePath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Modèle '$NewModelName' créé avec succès!" -ForegroundColor Green
    } else {
        Write-Host "❌ Erreur création modèle: $result" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Nettoyer le fichier temporaire
Remove-Item $modelfilePath -Force

# Test du modèle
Write-Host "`n🧪 Test du modèle..." -ForegroundColor Yellow
$testPrompt = "Bonjour, peux-tu confirmer que tu es prêt à analyser des fichiers ?"

try {
    $testResult = ollama run $NewModelName $testPrompt
    Write-Host "✅ Test réussi!" -ForegroundColor Green
    Write-Host "Réponse: $testResult" -ForegroundColor White
} catch {
    Write-Host "⚠️ Erreur test: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Instructions finales
Write-Host "`n📋 CONFIGURATION VOID EDITOR:" -ForegroundColor Cyan
Write-Host "1. Dans Void Editor, changez le modèle vers: $NewModelName" -ForegroundColor White
Write-Host "2. Ajoutez les fichiers au contexte avant de poser des questions" -ForegroundColor White
Write-Host "3. Utilisez des commandes comme:" -ForegroundColor White
Write-Host "   • 'Analyse le contenu du fichier README.md'" -ForegroundColor Yellow
Write-Host "   • 'Explique ce code Python'" -ForegroundColor Yellow
Write-Host "   • 'Résume cette documentation'" -ForegroundColor Yellow

Write-Host "`n🎯 Modèle optimisé pour la lecture de fichiers créé!" -ForegroundColor Green

# Ajouter raccourci PowerShell
$profilePath = $PROFILE
if (Test-Path $profilePath) {
    $shortcut = "`nfunction void-file-reader { ollama run $NewModelName `$args }"
    Add-Content -Path $profilePath -Value $shortcut
    Write-Host "📎 Raccourci ajouté: void-file-reader" -ForegroundColor Cyan
} 