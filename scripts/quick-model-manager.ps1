# Gestionnaire simple de modèles Ollama pour Void Editor
# NextGeneration - RTX 3090 Optimized

$OLLAMA_URL = "http://localhost:11434"

function Test-OllamaConnection {
    try {
        $response = Invoke-RestMethod -Uri "$OLLAMA_URL/api/tags" -Method GET -TimeoutSec 5
        return $true
    }
    catch {
        return $false
    }
}

function Show-Status {
    Write-Host "🔍 Vérification du statut Ollama..." -ForegroundColor Blue
    
    if (Test-OllamaConnection) {
        Write-Host "✅ Ollama est actif sur $OLLAMA_URL" -ForegroundColor Green
        Write-Host "📁 Répertoire des modèles: D:\modeles_llm" -ForegroundColor Cyan
    }
    else {
        Write-Host "❌ Ollama n'est pas accessible" -ForegroundColor Red
        Write-Host "💡 Vérifiez que le service est démarré" -ForegroundColor Yellow
    }
}

function Show-Models {
    Write-Host "🔍 Récupération des modèles..." -ForegroundColor Blue
    
    if (-not (Test-OllamaConnection)) {
        Write-Host "❌ Impossible de se connecter à Ollama" -ForegroundColor Red
        return
    }
    
    try {
        $response = Invoke-RestMethod -Uri "$OLLAMA_URL/api/tags" -Method GET
        $models = $response.models
        
        Write-Host "`n📋 Modèles disponibles:" -ForegroundColor Green
        Write-Host "=" * 50 -ForegroundColor Green
        
        $index = 1
        foreach ($model in $models) {
            $size = [math]::Round($model.size / 1GB, 1)
            
            Write-Host "$index. $($model.name)" -ForegroundColor Cyan
            Write-Host "   📊 Taille: $size GB" -ForegroundColor White
            $index++
        }
    }
    catch {
        Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Switch-ToModel {
    param([string]$ModelName)
    
    if (-not $ModelName) {
        Write-Host "❌ Nom du modèle requis" -ForegroundColor Red
        return
    }
    
    Write-Host "🔄 Activation du modèle: $ModelName..." -ForegroundColor Blue
    
    try {
        $body = @{
            model = $ModelName
            prompt = "Hello"
            stream = $false
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$OLLAMA_URL/api/generate" -Method POST -Body $body -ContentType "application/json"
        
        Write-Host "✅ Modèle $ModelName activé!" -ForegroundColor Green
        Write-Host "🎯 Utilisable dans Void Editor" -ForegroundColor Cyan
    }
    catch {
        Write-Host "❌ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Menu principal
function Show-Menu {
    Write-Host "`n🚀 GESTIONNAIRE DE MODÈLES OLLAMA" -ForegroundColor Green
    Write-Host "=" * 40 -ForegroundColor Green
    Write-Host "1. Voir le statut" -ForegroundColor White
    Write-Host "2. Lister les modèles" -ForegroundColor White
    Write-Host "3. Activer un modèle" -ForegroundColor White
    Write-Host "4. Quitter" -ForegroundColor White
    Write-Host ""
}

# Gestion des paramètres
param([string]$Action, [string]$ModelName)

if ($Action) {
    switch ($Action.ToLower()) {
        "status" { Show-Status }
        "list" { Show-Models }
        "switch" { Switch-ToModel -ModelName $ModelName }
        default { 
            Write-Host "Actions disponibles: status, list, switch [model-name]" -ForegroundColor Yellow
        }
    }
}
else {
    # Menu interactif
    while ($true) {
        Show-Menu
        $choice = Read-Host "Votre choix (1-4)"
        
        switch ($choice) {
            "1" { Show-Status }
            "2" { Show-Models }
            "3" { 
                $model = Read-Host "Nom du modèle à activer"
                Switch-ToModel -ModelName $model
            }
            "4" { 
                Write-Host "👋 Au revoir!" -ForegroundColor Green
                break 
            }
            default { 
                Write-Host "❌ Choix invalide" -ForegroundColor Red 
            }
        }
        
        if ($choice -ne "4") {
            Read-Host "`nAppuyez sur Entrée pour continuer"
        }
    }
} 