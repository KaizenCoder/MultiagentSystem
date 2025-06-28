# Guide d'Installation - NextGeneration Tools

## Prérequis

- Python 3.8+
- NextGeneration project
- Accès en écriture au répertoire tools/

## Installation Automatique

```bash
# Les outils sont déjà intégrés dans NextGeneration
# Installer uniquement les dépendances
pip install -r tools/imported_tools/requirements.txt
```

## Dépendances (3)

- asyncio
- collections
- threading

## Vérification de l'Installation

```bash
# Vérifier que les outils sont disponibles
python tools/imported_tools/run_tool.py install_phase3_dependencies --help
python tools/imported_tools/run_tool.py monitor_phase3 --help
```

## Dépannage

### Problèmes courants

1. **Erreur de dépendances**: Réinstaller requirements.txt
2. **Erreur de chemin**: Vérifier la structure NextGeneration
3. **Permissions**: Vérifier les droits d'accès aux fichiers

### Support

Consultez les logs NextGeneration pour plus de détails sur les erreurs.
