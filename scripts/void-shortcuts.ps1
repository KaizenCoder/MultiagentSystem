# Raccourcis rapides pour Void Editor + Ollama
# NextGeneration - RTX 3090 Setup

# Fonction pour charger un modèle rapidement
function Load-Model($modelName) {
    try {
        $body = @{ model = $modelName; prompt = "Ready"; stream = $false } | ConvertTo-Json
        Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -Body $body -ContentType "application/json" | Out-Null
        Write-Host "✅ $modelName chargé et prêt pour Void Editor" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Erreur lors du chargement de $modelName" -ForegroundColor Red
    }
}

# RACCOURCIS RAPIDES - Modèles recommandés pour Void Editor

# 🎯 SOLUTION FINALE: Modèle qui fonctionne parfaitement avec Void Editor
function void-perfect { Load-Model "deepseek-void-ultimate" }

# 🎯 NOUVEAU: Modèle ULTRA-optimisé pour Void Editor (CORRIGÉ)
function void-ultimate { Load-Model "deepseek-void-fixed" }

# 🎯 Modèle optimisé pour Void Editor
function void-best { Load-Model "deepseek-void" }

# 🚀 Ultra-rapide pour autocomplétion
function qwen-fast { Load-Model "qwen2.5-coder:1.5b" }

# ⚡ Équilibré pour développement
function code-balance { Load-Model "code-stral:latest" }

# 🧠 Puissant pour architecture
function deepseek-power { Load-Model "deepseek-coder:33b" }

# 🔥 Extended context 
function deepseek-extended { Load-Model "deepseek-extended" }

# 💎 Mixtral pour raisonnement
function mixtral-smart { Load-Model "mixtral:8x7b-instruct" }

# 🎮 Qwen super puissant
function qwen-mega { Load-Model "qwen2.5-coder:32b" }

# 🦙 Polyvalent pour tout usage
function llama { Load-Model "llama3:8b-instruct-q6_k" }

# 🧠 Raisonnement avancé
function mixtral { Load-Model "mixtral:8x7b-instruct-v0.1-q3_k_m" }

# 💬 Conversationnel
function hermes { Load-Model "nous-hermes-2-mistral-7b-dpo:latest" }

# RACCOURCIS DE GESTION

# 📋 Lister les modèles
function models { .\quick-model-manager.ps1 list }

# 🔍 Voir le statut
function status { .\quick-model-manager.ps1 status }

# 🎛️ Ouvrir le gestionnaire complet
function manager { .\quick-model-manager.ps1 }

# PRESETS OPTIMISÉS RTX 3090

function preset-speed {
    Write-Host "🚀 PRESET VITESSE - Modèles ultra-rapides" -ForegroundColor Cyan
    Write-Host "Chargement de qwen2.5-coder:1.5b..." -ForegroundColor Yellow
    qwen-fast
}

function preset-coding {
    Write-Host "💻 PRESET DÉVELOPPEMENT - Modèle équilibré" -ForegroundColor Cyan
    Write-Host "Chargement de code-stral:latest..." -ForegroundColor Yellow
    code-balance
}

function preset-power {
    Write-Host "🔥 PRESET PUISSANCE - Modèle le plus capable" -ForegroundColor Cyan
    Write-Host "Chargement de deepseek-coder:33b..." -ForegroundColor Yellow
    deepseek-power
}

# AIDE
function void-help {
    Write-Host ""
    Write-Host "🎯 VOID EDITOR - Raccourcis Modèles Ollama" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🌟 SOLUTION FINALE (TESTÉE ET VALIDÉE):" -ForegroundColor Green
    Write-Host "  void-perfect      - deepseek-void-ultimate (FONCTIONNE PARFAITEMENT!)" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔧 AUTRES OPTIONS:" -ForegroundColor Yellow
    Write-Host "  void-ultimate     - deepseek-void-fixed (CORRIGÉ pour fichiers locaux)" -ForegroundColor Yellow
    Write-Host "  void-best         - deepseek-void (OPTIMISÉ pour Void)" -ForegroundColor Yellow
    Write-Host "  deepseek-extended - deepseek-extended (contexte 16K)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚡ MODÈLES RAPIDES:" -ForegroundColor Blue
    Write-Host "  qwen-fast         - qwen2.5-coder:1.5b (1.5B - ultra rapide)"
    Write-Host "  code-balance      - code-stral:latest (7B - équilibré)"
    Write-Host ""
    Write-Host "🧠 MODÈLES PUISSANTS:" -ForegroundColor Magenta
    Write-Host "  deepseek-power    - deepseek-coder:33b (33B - très puissant)"
    Write-Host "  qwen-mega         - qwen2.5-coder:32b (32B - excellent)"
    Write-Host "  mixtral-smart     - mixtral:8x7b-instruct (raisonnement)"
    Write-Host ""
    Write-Host "📋 USAGE:" -ForegroundColor White
    Write-Host "  1. Tapez le raccourci (ex: void-perfect)"
    Write-Host "  2. Le modèle se charge automatiquement"
    Write-Host "  3. Utilisez-le dans Void Editor"
    Write-Host ""
    Write-Host "🎯 Configuration Void Editor:" -ForegroundColor Cyan
    Write-Host "  • Provider: Ollama" 
    Write-Host "  • URL: http://localhost:11434"
    Write-Host "  • Modèle recommandé: deepseek-void-ultimate"
    Write-Host ""
    Write-Host "🎉 PROBLÈME RÉSOLU!" -ForegroundColor Green
    Write-Host "  • Le modèle deepseek-void-ultimate analyse parfaitement les fichiers locaux"
    Write-Host "  • Réponses structurées en français avec emojis"
    Write-Host "  • Plus de refus ou de commandes inexistantes"
    Write-Host "  • Testé et validé sur le projet NextGeneration"
    Write-Host ""
}

Write-Host "🎯 Raccourcis Void Editor chargés! Tapez 'void-help' pour l'aide" -ForegroundColor Green 