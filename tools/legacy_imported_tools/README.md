# NextGeneration Tools - Outils Importés

## Vue d'ensemble

Collection de 2 outils professionnels importés depuis SuperWhisper V6 et adaptés pour NextGeneration.

**Statut**: 0/2 outils intégrés avec succès

## Catégories d'Outils

- **File**: 1 outils
- **Monitoring**: 1 outils

## Installation

```bash
# Installer les dépendances
pip install -r tools/imported_tools/requirements.txt

# Vérifier l'installation
python tools/imported_tools/run_tool.py
```

## Utilisation Rapide

```bash
# Lister les outils disponibles
python tools/imported_tools/run_tool.py

# Exécuter un outil
python tools/imported_tools/run_tool.py [nom_outil] [arguments]
```

## Outils Disponibles

| Outil | Catégorie | Statut | Score |
|-------|-----------|--------|-------|
| install_phase3_dependencies | file | ❌ FAIL | 45 |
| monitor_phase3 | monitoring | ❌ FAIL | 45 |

## Exemples d'Usage

### install_phase3_dependencies
```bash
python tools/imported_tools/run_tool.py install_phase3_dependencies --help
```

### monitor_phase3
```bash
python tools/imported_tools/run_tool.py monitor_phase3 --help
```

## Documentation

- [Guide d'Installation](INSTALLATION.md)
- [Guide d'Utilisation](USAGE.md)
- [Changelog](CHANGELOG.md)
- Documentation par catégorie dans chaque répertoire

## Support

Les outils sont intégrés avec le système de logging NextGeneration. Consultez les logs pour le dépannage.
