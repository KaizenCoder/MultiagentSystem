# 🚀 Générateur de Document Pitch - NextGeneration

## Vue d'ensemble

Outil de génération automatique de documents de présentation (pitch) pour le projet NextGeneration, avec support de plusieurs modes de génération selon les besoins.

## 🎯 Nouvelles Fonctionnalités

### **Modes de Génération**

1. **`minimal`** : Fichiers essentiels uniquement (agents, README, config)
2. **`selective`** : Patterns personnalisés (par défaut)
3. **`full`** : Intégralité du codebase (attention : documents volumineux)

### **Configuration Flexible**

- **Patterns d'inclusion** : Spécifiez quels fichiers/dossiers inclure
- **Fichiers de configuration JSON** : Sauvegardez vos paramètres
- **Métadonnées automatiques** : Suivi des fichiers inclus et mode utilisé

## 📖 Utilisation

### **Ligne de Commande**

```bash
# Mode minimal (fichiers essentiels)
python generate_pitch_document.py --mode minimal

# Mode sélectif avec patterns personnalisés
python generate_pitch_document.py --mode selective --include "agent_factory_experts_team/" "coordinateur_equipe_experts.py"

# Mode complet (tout le codebase - ATTENTION : gros fichier)
python generate_pitch_document.py --mode full

# Avec fichier de configuration
python generate_pitch_document.py --config agent_factory_config.json

# Créer un template de configuration
python generate_pitch_document.py --create-config
```

### **Exemples Concrets**

#### **1. Document Agent Factory (Recommandé)**
```bash
python generate_pitch_document.py \
  --template "../agent_factory_experts_team/PITCH_AGENT_FACTORY_PATTERN.md" \
  --output "../agent_factory_experts_team/PITCH_AGENT_FACTORY_FINAL.md" \
  --config "agent_factory_config.json"
```

#### **2. Document Complet NextGeneration**
```bash
python generate_pitch_document.py \
  --template "PITCH_NEXTGENERATION.md" \
  --output "PITCH_NEXTGENERATION_FULL.md" \
  --mode full
```

#### **3. Document Personnalisé**
```bash
python generate_pitch_document.py \
  --mode selective \
  --include "orchestrator/" "memory_api/" "tests/unit/"
```

## ⚙️ Configuration JSON

### **Exemple : agent_factory_config.json**
```json
{
  "mode": "selective",
  "include_patterns": [
    "agent_factory_experts_team/",
    "coordinateur_equipe_experts.py",
    "expert_claude_architecture.py",
    "expert_chatgpt_robustesse.py",
    "orchestrator/app/agents/",
    "tests/unit/test_agent_factory"
  ],
  "description": "Configuration Agent Factory - Éléments obligatoires"
}
```

### **Template de Configuration**
```bash
# Générer un template
python generate_pitch_document.py --create-config

# Éditer pitch_config.json selon vos besoins
# Utiliser avec --config pitch_config.json
```

## 🎛️ Options Disponibles

| Option | Description | Exemple |
|--------|-------------|---------|
| `--template` | Fichier modèle source | `PITCH_AGENT_FACTORY.md` |
| `--output` | Fichier de sortie | `PITCH_FINAL.md` |
| `--mode` | Mode de génération | `minimal`, `selective`, `full` |
| `--include` | Patterns d'inclusion | `"agent_factory/" "tests/"` |
| `--config` | Fichier de configuration JSON | `config.json` |
| `--create-config` | Créer template de config | - |

## 📊 Comparaison des Modes

| Mode | Taille Document | Temps Génération | Usage Recommandé |
|------|----------------|------------------|------------------|
| **minimal** | ~50-100 lignes | < 30s | Présentation rapide |
| **selective** | ~200-500 lignes | 1-2 min | **Recommandé pour experts** |
| **full** | 3000+ lignes | 5-10 min | Documentation complète |

## 🔧 Personnalisation Avancée

### **Patterns d'Inclusion Intelligents**

```json
{
  "include_patterns": [
    "agent_factory_experts_team/",    // Dossier complet
    "coordinateur_equipe_experts.py", // Fichier spécifique
    "tests/unit/test_agent",          // Pattern partiel
    "README.md",                      // Documentation
    "orchestrator/app/agents/"        // Module spécifique
  ]
}
```

### **Exclusions Automatiques**

L'outil exclut automatiquement :
- `.git/`, `__pycache__/`, `node_modules/`
- `.DS_Store`, fichiers temporaires
- Anciens documents pitch générés
- Base de données (`chroma_db/`)

## 🚀 Utilisation dans le Workflow

### **1. Développement Agent Factory**
```bash
# Document de travail (éléments obligatoires)
python generate_pitch_document.py --config agent_factory_config.json
```

### **2. Présentation Externe**
```bash
# Document concis pour experts
python generate_pitch_document.py --mode minimal
```

### **3. Documentation Technique**
```bash
# Annexe technique complète
python generate_pitch_document.py --mode full --output "ANNEXE_TECHNIQUE.md"
```

## 📈 Métriques et Suivi

Chaque document généré inclut automatiquement :
- **Mode utilisé** : `minimal`, `selective`, `full`
- **Nombre de fichiers inclus** : Compteur automatique
- **Patterns appliqués** : Liste des patterns d'inclusion
- **Timestamp** : Date/heure de génération

## 🔍 Dépannage

### **Document trop volumineux ?**
- Utilisez `--mode minimal` ou `--mode selective`
- Créez une config JSON avec patterns spécifiques
- Vérifiez les patterns d'inclusion/exclusion

### **Fichiers manquants ?**
- Vérifiez les patterns d'inclusion dans votre config
- Utilisez `--mode full` pour débugger
- Consultez les métadonnées en haut du document généré

### **Performance lente ?**
- Évitez `--mode full` sur de gros codebases
- Utilisez des patterns d'inclusion précis
- Excluez les dossiers volumineux dans la config

---

**💡 Conseil :** Pour les présentations d'experts, utilisez toujours le mode `selective` avec une configuration adaptée. C'est le meilleur compromis entre complétude et lisibilité. 