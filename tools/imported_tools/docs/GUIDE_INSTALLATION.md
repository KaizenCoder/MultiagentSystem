#  Guide d'Installation - Outils Imports

## Prrequis

### Systme
- Python 3.8 ou suprieur
- pip (gestionnaire de packages Python)
- Git (pour les mises  jour)

### Vrification
```bash
python --version  # Doit afficher 3.8+
pip --version     # Doit tre install
```

##  Installation

### 1. Installation automatique (recommande)
```bash
# Depuis la racine du projet NextGeneration
cd tools/imported_tools
pip install -r requirements.txt
```

### 2. Installation manuelle
```bash
# Installer les dpendances une par une
pip install requests
pip install pathlib
pip install json
# ... autres dpendances selon les besoins
```

### 3. Vrification de l'installation
```bash
# Tester l'installation
python configs/test_installation.py

# Lister les outils disponibles
python configs/list_tools.py
```

## [TOOL] Configuration

### Configuration Automatique
Les outils se configurent automatiquement au dmarrage :
- Dtection du rpertoire NextGeneration
- Cration des rpertoires ncessaires
- Configuration des chemins

### Configuration Manuelle (optionnelle)
Si ncessaire, vous pouvez modifier la configuration :

1. **diter un outil spcifique :**
```python
# Dans le fichier de l'outil
NEXTGEN_CONFIG = {
    "project_root": Path("/votre/chemin/nextgeneration"),
    "data_dir": Path("/votre/chemin/data"),
    # ...
}
```

2. **Configuration globale :**
```bash
# Modifier le fichier de configuration
nano tools/imported_tools/configs/config.json
```

##  Tests

### Tests Automatiques
```bash
# Tester tous les outils
python configs/test_all_tools.py

# Tester une catgorie
python configs/test_category.py automation

# Tester un outil spcifique
python configs/test_tool.py nom_outil.py
```

### Tests Manuels
```bash
# Test basique d'un outil
python utilities/exemple_outil.py --help

# Test avec paramtres
python utilities/exemple_outil.py --version
```

##  Rsolution de Problmes

### Problmes Courants

#### 1. ImportError
```
Erreur: ModuleNotFoundError: No module named 'requests'
Solution: pip install requests
```

#### 2. Permission denied
```
Erreur: Permission denied
Solution: chmod +x tools/imported_tools/[outil].py
```

#### 3. Chemin non trouv
```
Erreur: FileNotFoundError
Solution: Vrifier que vous tes dans le bon rpertoire
cd /chemin/vers/nextgeneration
```

### Diagnostic
```bash
# Vrifier l'environnement Python
python -c "import sys; print('\n'.join(sys.path))"

# Vrifier les packages installs
pip list

# Vrifier la configuration NextGeneration
python -c "from pathlib import Path; print(Path.cwd())"
```

##  Mise  Jour

### Mise  jour des dpendances
```bash
pip install --upgrade -r requirements.txt
```

### Mise  jour des outils
Les outils sont mis  jour avec le projet NextGeneration via Git.

## [CHART] Validation de l'Installation

### Checklist
- [ ] Python 3.8+ install
- [ ] Dpendances installes (`pip install -r requirements.txt`)
- [ ] Tests de base russis (`python configs/test_installation.py`)
- [ ] Au moins un outil fonctionne (`python utilities/[outil].py --help`)

### Script de Validation
```bash
#!/bin/bash
# Script de validation complte

echo "[SEARCH] Validation de l'installation..."

# Test Python
python --version || { echo "[CROSS] Python non install"; exit 1; }

# Test dpendances
pip install -r requirements.txt || { echo "[CROSS] Erreur dpendances"; exit 1; }

# Test configuration
python configs/test_installation.py || { echo "[CROSS] Erreur configuration"; exit 1; }

echo "[CHECK] Installation valide avec succs!"
```

---
*Guide cr par Agent 5 - Documenteur - 2025-06-19*
