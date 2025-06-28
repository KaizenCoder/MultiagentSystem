#  Guide d'Utilisation - Outils Imports

## Introduction

Ce guide vous explique comment utiliser efficacement les outils imports dans NextGeneration.

## [ROCKET] Dmarrage Rapide

### 1. Vrification de l'installation
```bash
# Vrifier que Python est install
python --version

# Vrifier les dpendances
pip list | grep -E "(requests|numpy|pandas)"
```

### 2. Premier test
```bash
# Lister tous les outils disponibles
python tools/imported_tools/configs/list_tools.py

# Tester un outil simple
python tools/imported_tools/utilities/[nom_outil].py --help
```

## [FOLDER] Navigation dans les Outils

### Par Catgorie

#### [ROBOT] Automation
Les outils d'automatisation vous permettent de :
- Automatiser des tches rptitives
- Crer des scripts de dploiement
- Grer les processus en arrire-plan

#### [CHART] Monitoring
Les outils de surveillance pour :
- Surveiller les performances systme
- Collecter des mtriques
- Gnrer des alertes

####  Conversion
Les outils de conversion pour :
- Transformer des formats de donnes
- Migrer des configurations
- Convertir des fichiers

#### [CONSTRUCTION] Generation
Les outils de gnration pour :
- Crer des templates
- Gnrer du code
- Produire des rapports

####  Utilities
Utilitaires divers pour :
- Tches systme
- Manipulation de fichiers
- Outils de dveloppement

## [BULB] Conseils d'Utilisation

### Bonnes Pratiques
1. **Toujours tester** avec `--help` avant d'utiliser un outil
2. **Vrifier les dpendances** si un outil ne fonctionne pas
3. **Consulter les logs** en cas de problme
4. **Utiliser des chemins relatifs** quand possible

### Rsolution de Problmes
```bash
# Si un outil ne dmarre pas
python -c "import sys; print(sys.path)"

# Si les imports chouent
pip install -r tools/imported_tools/requirements.txt

# Si les permissions sont refuses
chmod +x tools/imported_tools/[categorie]/[outil].py
```

## [TOOL] Configuration Avance

### Variables d'Environnement
Les outils utilisent automatiquement la configuration NextGeneration :
- `NEXTGEN_CONFIG["project_root"]` - Racine du projet
- `NEXTGEN_CONFIG["data_dir"]` - Rpertoire de donnes
- `NEXTGEN_CONFIG["logs_dir"]` - Rpertoire de logs

### Personnalisation
Vous pouvez modifier la configuration dans chaque outil en ditant la section :
```python
NEXTGEN_CONFIG = {
    "project_root": PROJECT_ROOT,
    "tools_dir": PROJECT_ROOT / "tools",
    # ... autres configurations
}
```

## [CHART] Exemples d'Utilisation

### Exemple 1 : Outil de Monitoring
```bash
# Surveiller l'utilisation CPU
python tools/imported_tools/monitoring/cpu_monitor.py --interval 5

# Gnrer un rapport
python tools/imported_tools/monitoring/cpu_monitor.py --report
```

### Exemple 2 : Outil de Conversion
```bash
# Convertir un fichier
python tools/imported_tools/conversion/file_converter.py input.txt output.json

# Conversion en lot
python tools/imported_tools/conversion/file_converter.py --batch input_dir/ output_dir/
```

##  Aide et Support

### Obtenir de l'aide
```bash
# Aide gnrale
python tools/imported_tools/configs/help.py

# Aide spcifique  un outil
python tools/imported_tools/[categorie]/[outil].py --help

# Version d'un outil
python tools/imported_tools/[categorie]/[outil].py --version
```

### Logs et Dbogage
- Les logs sont automatiquement crs dans `logs/`
- Utiliser `--verbose` ou `-v` pour plus de dtails
- Consulter `docs/DOCUMENTATION_TECHNIQUE.md` pour le dbogage avanc

---
*Guide cr par Agent 5 - Documenteur - 2025-06-19*
