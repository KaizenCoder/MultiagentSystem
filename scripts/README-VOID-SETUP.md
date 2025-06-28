# 🚀 Guide Void Editor + Ollama - NextGeneration

Configuration optimisée pour RTX 3090 avec modèles locaux stockés dans `D:\modeles_llm`

## ✅ Status actuel
- ✅ Ollama installé et fonctionnel (v0.9.2)
- ✅ RTX 3090 détectée (24GB VRAM, 22.8GB disponible)
- ✅ 10 modèles disponibles dans `D:\modeles_llm`
- ✅ Void Editor installé
- ✅ Scripts de gestion créés

## 🎯 Configuration Void Editor

### Étape 1: Ouvrir Void Editor
1. Lancez **Void Editor** 
2. Allez dans **Settings** (Paramètres)
3. Sélectionnez **Providers** (Fournisseurs)

### Étape 2: Configurer Ollama
1. Choisissez **Ollama** dans la liste des fournisseurs
2. URL du serveur: `http://localhost:11434`
3. Les modèles apparaîtront automatiquement

## 🎮 Utilisation des scripts

### Gestionnaire de modèles
```powershell
cd C:\Dev\nextgeneration\scripts
.\quick-model-manager.ps1
```

### Raccourcis rapides
```powershell
# Charger les raccourcis
. .\void-shortcuts.ps1

# Commandes rapides
qwen-fast      # Ultra-rapide (0.9 GB)
code-stral     # Équilibré (8 GB) - RECOMMANDÉ
deepseek       # Puissant (17.5 GB)
llama          # Polyvalent (6.1 GB)
mixtral        # Raisonnement (21 GB)

# Presets optimisés
preset-speed   # Configuration rapide
preset-coding  # Configuration développement
preset-power   # Configuration puissance max
```

## 🏆 Modèles recommandés par usage

### 💻 Développement quotidien
- **`code-stral:latest`** (8 GB) - Parfait équilibre vitesse/qualité
- Temps de réponse: ~2-3 secondes
- Excellent pour autocomplétion et génération de code

### 🚀 Développement ultra-rapide  
- **`qwen2.5-coder:1.5b`** (0.9 GB) - Ultra-rapide
- Temps de réponse: <1 seconde
- Idéal pour autocomplétion en temps réel

### 🧠 Projets complexes
- **`deepseek-coder:33b`** (17.5 GB) - Le plus puissant
- Temps de réponse: ~5-8 secondes
- Excellent pour architecture et code complexe

## ⚡ Optimisations RTX 3090

### Performances attendues
- **Modèles 1-7B**: <3 secondes
- **Modèles 8-13B**: 3-5 secondes  
- **Modèles 20B+**: 5-10 secondes

### VRAM utilisée
- **qwen2.5-coder:1.5b**: ~2 GB VRAM
- **code-stral:latest**: ~10 GB VRAM
- **deepseek-coder:33b**: ~20 GB VRAM
- **mixtral:8x7b**: ~18 GB VRAM

## 🎯 Workflow recommandé

### 1. Démarrage quotidien
```powershell
cd C:\Dev\nextgeneration\scripts
. .\void-shortcuts.ps1
preset-coding  # Charge code-stral
```

### 2. Dans Void Editor
- **Tab** pour autocomplétion
- **Ctrl+K** pour édition inline
- **Chat** pour questions complexes
- **Mode Agent** pour tâches avancées

### 3. Changement de modèle selon le besoin
```powershell
qwen-fast    # Pour du code rapide
deepseek     # Pour du code complexe
mixtral      # Pour du raisonnement
```

## 🔧 Dépannage

### Ollama ne répond pas
```powershell
# Vérifier le statut
status

# Redémarrer Ollama
ollama serve
```

### Modèle introuvable
```powershell
# Lister les modèles disponibles
models

# Vérifier la connexion
status
```

### Performances lentes
1. Utiliser un modèle plus petit (`qwen-fast`)
2. Vérifier l'utilisation VRAM avec `nvidia-smi`
3. Fermer d'autres applications GPU-intensives

## 📝 Fichiers créés

- `quick-model-manager.ps1` - Gestionnaire complet
- `void-shortcuts.ps1` - Raccourcis rapides
- `start-ollama-void.bat` - Script de démarrage
- `README-VOID-SETUP.md` - Ce guide

## 🎉 Vous êtes prêt !

Configuration optimale pour le développement avec Void Editor + Ollama sur RTX 3090.

**Commande de test:**
```powershell
cd C:\Dev\nextgeneration\scripts
. .\void-shortcuts.ps1
preset-coding
```

Puis ouvrez Void Editor et testez l'autocomplétion ! 🚀 