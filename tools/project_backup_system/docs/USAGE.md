# Guide d'Utilisation - Zip Backup

## Introduction

Ce guide détaille l'utilisation de l'outil zip_backup dans l'écosystème NextGeneration.

## Utilisation de base

### Ligne de commande
```bash
python tools/zip_backup/zip_backup.py [options]
```

### Options disponibles
- `--help` : Affiche l'aide
- `--config PATH` : Spécifie un fichier de configuration
- `--debug` : Active le mode debug
- `--verbose` : Mode verbeux

## Exemples pratiques

### Exemple 1: Utilisation standard
```bash
python tools/zip_backup/zip_backup.py
```

### Exemple 2: Configuration personnalisée
```bash
python tools/zip_backup/zip_backup.py --config config/custom.json
```

## Intégration programmatique

```python
from tools.zip_backup import ZipBackup

# Utilisation basique
tool = ZipBackup()
result = tool.execute()
```

## Bonnes pratiques

1. Toujours tester en mode debug d'abord
2. Utiliser des configurations spécifiques par environnement
3. Monitorer les logs pour diagnostiquer les problèmes
4. Valider les résultats avant utilisation en production
