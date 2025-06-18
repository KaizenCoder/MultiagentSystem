# Guide d'Utilisation - Generate Pitch Document

## Introduction

Ce guide détaille l'utilisation de l'outil generate_pitch_document dans l'écosystème NextGeneration.

## Utilisation de base

### Ligne de commande
```bash
python tools/generate_pitch_document/generate_pitch_document.py [options]
```

### Options disponibles
- `--help` : Affiche l'aide
- `--config PATH` : Spécifie un fichier de configuration
- `--debug` : Active le mode debug
- `--verbose` : Mode verbeux

## Exemples pratiques

### Exemple 1: Utilisation standard
```bash
python tools/generate_pitch_document/generate_pitch_document.py
```

### Exemple 2: Configuration personnalisée
```bash
python tools/generate_pitch_document/generate_pitch_document.py --config config/custom.json
```

## Intégration programmatique

```python
from tools.generate_pitch_document import GeneratePitchDocument

# Utilisation basique
tool = GeneratePitchDocument()
result = tool.execute()
```

## Bonnes pratiques

1. Toujours tester en mode debug d'abord
2. Utiliser des configurations spécifiques par environnement
3. Monitorer les logs pour diagnostiquer les problèmes
4. Valider les résultats avant utilisation en production
