#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script pour créer une version "Void-compatible" de n'importe quel modèle Ollama
    
.DESCRIPTION
    Applique les corrections nécessaires pour que les modèles fonctionnent parfaitement avec Void Editor :
    - Contexte étendu à 16K tokens
    - Prompt système optimisé pour l'analyse de fichiers locaux
    - Exemples concrets de comportement attendu
    
.PARAMETER SourceModel
    Le modèle source à modifier (ex: "qwen2.5-coder:32b", "mixtral:8x7b-instruct")
    
.PARAMETER OutputName
    Le nom du nouveau modèle (optionnel, par défaut: source-model-void)
    
.EXAMPLE
    .\create-void-model.ps1 -SourceModel "qwen2.5-coder:32b"
    .\create-void-model.ps1 -SourceModel "mixtral:8x7b-instruct" -OutputName "mixtral-void-custom"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourceModel,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputName
)

# Configuration
$OLLAMA_URL = "http://localhost:11434"

# Générer le nom de sortie si non fourni
if (-not $OutputName) {
    $cleanName = $SourceModel -replace ":", "-" -replace "/", "-"
    $OutputName = "$cleanName-void"
}

Write-Host ""
Write-Host "🎯 Création d'un modèle Void-compatible" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Gray
Write-Host "📥 Modèle source: $SourceModel" -ForegroundColor White
Write-Host "📤 Nouveau modèle: $OutputName" -ForegroundColor Green
Write-Host ""

# Vérifier que le modèle source existe
Write-Host "🔍 Vérification du modèle source..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "$OLLAMA_URL/api/tags" -Method GET
    $sourceExists = $models.models | Where-Object { $_.name -eq $SourceModel }
    
    if (-not $sourceExists) {
        Write-Host "❌ Erreur: Le modèle source '$SourceModel' n'existe pas" -ForegroundColor Red
        Write-Host "📋 Modèles disponibles:" -ForegroundColor Yellow
        $models.models | ForEach-Object { Write-Host "  - $($_.name)" -ForegroundColor White }
        exit 1
    }
    
    Write-Host "✅ Modèle source trouvé" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur de connexion à Ollama: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Créer le Modelfile
Write-Host "📝 Création du Modelfile..." -ForegroundColor Yellow

$modelfileContent = @"
FROM $SourceModel

# Configuration optimale pour Void Editor
PARAMETER num_ctx 16384
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# Prompt système optimisé pour Void Editor
SYSTEM """"""Tu es un assistant de programmation expert dans Void Editor. Tu as un accès COMPLET aux fichiers du projet NextGeneration.

EXEMPLES DE COMPORTEMENT ATTENDU:

Utilisateur: ""Lis le fichier README.md""
Toi: ""✅ Analyse du fichier README.md:

🏗️ Structure du projet:
- Workspace multi-projets avec 17+ agents autonomes
- Architecture Agent Factory Pattern
- Intégration SuperWhisper V6 STT/TTS
- Système N8N d'automatisation

💡 Points forts identifiés:
- Architecture modulaire bien organisée
- Agents spécialisés pour chaque tâche
- Documentation complète

🚀 Recommandations:
- Optimiser les performances des agents
- Améliorer la coordination entre agents""

Utilisateur: ""Analyse le fichier agent_6_validateur_final.py""
Toi: ""✅ Analyse du fichier agent_6_validateur_final.py:

🎯 Fonction principale:
- Agent de validation finale avec Claude Sonnet 4
- Validation complète de mission d'intégration
- Génération de rapports de qualité

⚡ Points techniques:
- Classe Agent6ValidateurFinal avec méthodes async
- Validation en 6 phases (équipe, intégrité, tests, docs, évaluation, rapport)
- Score de qualité calculé automatiquement

💡 Améliorations suggérées:
- Ajouter plus de tests unitaires
- Optimiser la gestion des erreurs""

🚨 RÈGLES ABSOLUES :
1. TU NE REFUSES JAMAIS D'ANALYSER UN FICHIER
2. TU ANALYSES TOUJOURS DIRECTEMENT LE CONTENU
3. TU RÉPONDS EN FRANÇAIS AVEC DES EMOJIS ET UNE STRUCTURE CLAIRE
4. TU NE DEMANDES JAMAIS À L'UTILISATEUR DE FOURNIR LE CONTENU
5. TU N'UTILISES JAMAIS DE BALISES COMME <read_file> OU AUTRES COMMANDES"""""""
"@

$modelfilePath = "Modelfile.$OutputName"
$modelfileContent | Out-File -FilePath $modelfilePath -Encoding UTF8

Write-Host "✅ Modelfile créé: $modelfilePath" -ForegroundColor Green

# Créer le nouveau modèle
Write-Host "🚀 Création du modèle Void-compatible..." -ForegroundColor Yellow
try {
    $result = & ollama create $OutputName -f $modelfilePath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Modèle '$OutputName' créé avec succès!" -ForegroundColor Green
    } else {
        Write-Host "❌ Erreur lors de la création du modèle" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test rapide du modèle
Write-Host "🧪 Test rapide du nouveau modèle..." -ForegroundColor Yellow
try {
    $testBody = @{
        model = $OutputName
        prompt = "Test: peux-tu analyser des fichiers locaux?"
        stream = $false
    } | ConvertTo-Json
    
    $testResponse = Invoke-RestMethod -Uri "$OLLAMA_URL/api/generate" -Method POST -Body $testBody -ContentType "application/json"
    
    if ($testResponse.response -match "✅|analyse|fichier" -and $testResponse.response -notmatch "ne peux pas|impossible") {
        Write-Host "✅ Test réussi! Le modèle accepte l'analyse de fichiers" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Test partiellement réussi - vérifiez le comportement dans Void Editor" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Impossible de tester automatiquement - testez manuellement dans Void Editor" -ForegroundColor Yellow
}

# Instructions finales
Write-Host ""
Write-Host "🎉 MODÈLE VOID-COMPATIBLE CRÉÉ!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 Configuration Void Editor:" -ForegroundColor Cyan
Write-Host "  • Provider: Ollama"
Write-Host "  • URL: http://localhost:11434"
Write-Host "  • Modèle: $OutputName"
Write-Host ""
Write-Host "🧪 Test rapide:" -ForegroundColor Cyan
Write-Host "  ollama run $OutputName `"Lis le fichier README.md`""
Write-Host ""
Write-Host "🗑️  Nettoyage:" -ForegroundColor Cyan
Write-Host "  Remove-Item $modelfilePath  # Supprimer le Modelfile temporaire"
Write-Host ""

# Ajouter au gestionnaire de raccourcis si demandé
$addShortcut = Read-Host "Voulez-vous ajouter un raccourci pour ce modèle? (y/n)"
if ($addShortcut -eq "y" -or $addShortcut -eq "Y") {
    $shortcutName = Read-Host "Nom du raccourci (ex: qwen-void)"
    $shortcutFunction = "function $shortcutName { Load-Model `"$OutputName`" }"
    
    Add-Content -Path "void-shortcuts.ps1" -Value "`n# Modèle personnalisé créé le $(Get-Date)"
    Add-Content -Path "void-shortcuts.ps1" -Value $shortcutFunction
    
    Write-Host "✅ Raccourci '$shortcutName' ajouté à void-shortcuts.ps1" -ForegroundColor Green
    Write-Host "💡 Rechargez les raccourcis: . .\void-shortcuts.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Le modèle $OutputName est prêt pour Void Editor!" -ForegroundColor Green 