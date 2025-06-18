# Guide d'Utilisation - Outils NextGeneration

## Vue d'ensemble

Ce guide vous explique comment utiliser les 2 outils importés depuis SuperWhisper V6 et adaptés pour NextGeneration.

## Méthodes d'Exécution

### 1. Exécution Directe

```bash
# Depuis le répertoire de l'outil
cd tools/imported_tools/[category]/
python [tool_name].py [arguments]
```

### 2. Exécution via le Lanceur

```bash
# Depuis n'importe où dans NextGeneration
python tools/imported_tools/run_tool.py [tool_name] [arguments]
```

### 3. Exécution depuis Python

```python
import sys
sys.path.append('tools/imported_tools')
from [category] import [tool_name]

# Utiliser l'outil...
```

## Outils par Catégorie

### File

- **install_phase3_dependencies** ⚠️ - Score: 45/100

### Monitoring

- **monitor_phase3** ⚠️ - Score: 45/100

## Exemples d'Usage Courants

#### Exemple 1: install_phase3_dependencies
```bash
python tools/imported_tools/run_tool.py install_phase3_dependencies
```

#### Exemple 2: monitor_phase3
```bash
python tools/imported_tools/run_tool.py monitor_phase3
```

## Configuration

Tous les outils sont configurés avec:
- Auto-détection du projet NextGeneration
- Logging intégré
- Chemins portables
- Configuration centralisée

## Dépannage

### Problèmes Courants

1. **Import Error**: Vérifiez que les dépendances sont installées
2. **Path Error**: Les outils détectent automatiquement le projet root
3. **Permission Error**: Vérifiez les permissions d'exécution

### Support

Consultez la documentation individuelle de chaque outil ou les logs NextGeneration.
