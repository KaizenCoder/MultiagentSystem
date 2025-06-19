# 🚀 PROMPT MISSION : REFACTORING - CONFIGURATION EXTERNALISÉE DES AGENTS

## 🎯 **CONTEXTE**

Les agents de documentation (`agent_synthese_auto_update.py` et `generate_bundle_nextgeneration.py`) contiennent actuellement des règles de configuration (listes d'exclusion, mots-clés, etc.) directement dans leur code source.

Cette mission a pour objectif de refactoriser ces agents pour externaliser leur configuration dans un fichier JSON unique, afin d'améliorer leur flexibilité et leur maintenabilité.

## ✅ **OBJECTIFS TECHNIQUES**

### **1. Création du Fichier de Configuration Centralisé**

-   **Action :** Créer un nouveau fichier de configuration.
-   **Chemin :** `tools/documentation_generator/config/config.json`
-   **Contenu Initial :**
    ```json
    {
      "agent_synthese": {
        "git_log_timeframe": "2 weeks ago",
        "detection_keywords": [
          "mission", "accompli", "opérationnel", "validé", "feat", 
          "sprint", "refactor", "implémenté"
        ]
      },
      "generate_bundle": {
        "output_filename": "CODE-SOURCE.md",
        "exclude_dirs": [
          ".git", "__pycache__", "node_modules", "dist", "build", 
          "logs", "backups", "chroma_db", ".vscode", ".idea", 
          "agent_factory_implementation"
        ],
        "exclude_files": [
          "CODE-SOURCE.md", "CODE-SOURCE.md.backup", ".gitignore"
        ],
        "exclude_extensions": [
          ".pyc", ".pyo", ".pyd", ".log", ".tmp", ".DS_Store", ".db", ".bak"
        ]
      }
    }
    ```

### **2. Refactoring des Agents**

-   **`agent_synthese_auto_update.py` :**
    -   Modifier l'agent pour qu'il lise les paramètres `git_log_timeframe` et `detection_keywords` depuis le fichier `config.json` au lieu de les avoir en dur.

-   **`generate_bundle_nextgeneration.py` :**
    -   Modifier l'agent pour qu'il utilise les listes `exclude_dirs`, `exclude_files`, et `exclude_extensions` provenant du fichier `config.json`.

## 🏆 **CRITÈRES DE SUCCÈS**

-   Le fichier `config.json` est créé et contient toutes les configurations externalisées.
-   Les deux agents Python sont modifiés pour charger et utiliser ces configurations externes.
-   Toutes les valeurs de configuration codées en dur ont été supprimées des scripts Python.
-   Les deux agents fonctionnent exactement comme avant le refactoring. Une exécution en `dry-run` des deux scripts doit produire des résultats identiques à la version précédente.
-   La modification est transparente pour les scripts qui appellent les agents (ex: `hook_synthese_auto_update.ps1`). 