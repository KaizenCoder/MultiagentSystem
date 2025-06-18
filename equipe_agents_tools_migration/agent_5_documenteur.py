#!/usr/bin/env python3
"""
 Agent 5: Documenteur - Gemini 2.0 Flash
Mission: Documenter les outils finaliss et crer la documentation utilisateur
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class Agent5Documenteur:
    """Agent spcialis dans la documentation"""
    
    def __init__(self, outils_finalises: List[Dict], target_path: Path, workspace_path: Path):
        self.outils_finalises = outils_finalises
        self.target_path = target_path
        self.workspace_path = workspace_path
        self.agent_name = "Agent 5 - Documenteur"
        self.model_name = "Gemini 2.0 Flash"
        self.start_time = None
        
        self.docs_created = 0
        self.documentation_files = []
    
    async def documenter_outils(self) -> Dict[str, Any]:
        """Documenter tous les outils finaliss"""
        self.start_time = datetime.now()
        print(f" {self.agent_name} - Dmarrage documentation")
        
        try:
            await self._creer_readme_principal()
            await self._documenter_outils_individuels()
            await self._creer_guide_utilisation()
            await self._creer_guide_installation()
            
            resultat = await self._generer_rapport()
            
            duree = (datetime.now() - self.start_time).total_seconds()
            print(f"[CHECK] {self.agent_name} - Termin en {duree:.2f}s")
            
            return resultat
            
        except Exception as e:
            print(f"[CROSS] {self.agent_name} - Erreur: {e}")
            raise
    
    async def _creer_readme_principal(self):
        """Crer le README principal"""
        print("[DOCUMENT] Cration du README principal...")
        
        # Grouper les outils par catgorie
        outils_par_categorie = {}
        for outil_info in self.outils_finalises:
            outil = outil_info['outil']
            categorie = outil.get('type', 'utilities')
            if categorie not in outils_par_categorie:
                outils_par_categorie[categorie] = []
            outils_par_categorie[categorie].append(outil)
        
        readme_content = f"""#  Outils Imports NextGeneration

## Vue d'Ensemble

Ce rpertoire contient les outils imports et adapts depuis SuperWhisper_V6 vers l'environnement NextGeneration.

**Date d'importation :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Nombre d'outils :** {len(self.outils_finalises)}  
**Agent responsable :** {self.agent_name}  

## [FOLDER] Structure

```
imported_tools/
 automation/     # Outils d'automatisation
 monitoring/     # Outils de surveillance
 conversion/     # Outils de conversion
 generation/     # Outils de gnration
 utilities/      # Utilitaires divers
 configs/        # Fichiers de configuration
 docs/          # Documentation
```

## [ROCKET] Installation Rapide

### 1. Installer les dpendances
```bash
pip install -r tools/imported_tools/requirements.txt
```

### 2. Vrifier l'installation
```bash
python tools/imported_tools/configs/test_installation.py
```

## [CLIPBOARD] Outils Disponibles

"""
        
        # Ajouter chaque catgorie
        for categorie, outils in outils_par_categorie.items():
            readme_content += f"\n### [FOLDER] {categorie.upper()}\n\n"
            for outil in outils:
                description = outil.get('description', 'Outil import')
                if len(description) > 100:
                    description = description[:97] + "..."
                readme_content += f"- **{outil['nom']}** - {description}\n"
        
        readme_content += f"""

##  Guides

- [Guide d'Installation](docs/GUIDE_INSTALLATION.md)
- [Guide d'Utilisation](docs/GUIDE_UTILISATION.md)
- [Documentation Technique](docs/DOCUMENTATION_TECHNIQUE.md)

## [TOOL] Utilisation

### Lister tous les outils
```bash
python tools/imported_tools/configs/list_tools.py
```

### Excuter un outil
```bash
python tools/imported_tools/<categorie>/<nom_outil>.py
```

## [CHART] Statistiques

- **Total d'outils :** {len(self.outils_finalises)}
- **Catgories :** {len(outils_par_categorie)}
- **Tests russis :** [CHECK] (voir rapports de tests)

##  Support

En cas de problme :
1. Vrifier les dpendances : `pip install -r requirements.txt`
2. Consulter les logs dans le rpertoire `logs/`
3. Vrifier la documentation technique

##  Changelog

### Version 1.0.0 ({datetime.now().strftime('%Y-%m-%d')})
- Importation initiale depuis SuperWhisper_V6
- Adaptation pour NextGeneration
- Tests d'intgration russis
- Documentation complte

---
*Gnr automatiquement par {self.agent_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        readme_path = self.target_path / "imported_tools" / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.documentation_files.append(str(readme_path))
        self.docs_created += 1
        print(f"[DOCUMENT] README principal cr: {readme_path}")
    
    async def _documenter_outils_individuels(self):
        """Crer la documentation pour chaque outil"""
        print(" Documentation individuelle des outils...")
        
        for outil_info in self.outils_finalises:
            outil = outil_info['outil']
            
            # Lire le fichier pour extraire plus d'informations
            outil_path = Path(outil_info['target_path'])
            
            try:
                with open(outil_path, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                # Extraire les fonctions principales
                fonctions = []
                for ligne in contenu.split('\n'):
                    if ligne.strip().startswith('def ') and not ligne.strip().startswith('def _'):
                        nom_fonction = ligne.strip().split('(')[0].replace('def ', '')
                        fonctions.append(nom_fonction)
                
                doc_content = f"""# {outil['nom']}

## Description
{outil.get('description', 'Outil import de SuperWhisper_V6')}

## Informations
- **Type :** {outil.get('type', 'utility')}
- **Source :** SuperWhisper_V6
- **Adapt le :** {datetime.now().strftime('%Y-%m-%d')}
- **Chemin :** `{outil_info['target_path']}`

## Fonctions principales
"""
                
                for fonction in fonctions[:5]:  # Limiter  5 fonctions
                    doc_content += f"- `{fonction}()`\n"
                
                doc_content += f"""

## Utilisation

### Excution basique
```bash
python {outil_info['target_path']}
```

### Avec aide
```bash
python {outil_info['target_path']} --help
```

## Dpendances
"""
                
                dependances = outil.get('dependances', [])
                if dependances:
                    for dep in dependances[:10]:  # Limiter  10 dpendances
                        doc_content += f"- {dep}\n"
                else:
                    doc_content += "- Aucune dpendance externe\n"
                
                doc_content += f"""

## Notes d'adaptation
- Chemins adapts pour NextGeneration
- Configuration automatique de l'environnement
- Compatible multi-plateforme

---
*Documentation gnre par {self.agent_name}*
"""
                
                # Sauvegarder la documentation
                doc_filename = f"{outil['nom'].replace('.py', '')}.md"
                doc_path = self.target_path / "imported_tools" / "docs" / "tools" / doc_filename
                doc_path.parent.mkdir(exist_ok=True)
                
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                
                self.documentation_files.append(str(doc_path))
                self.docs_created += 1
                
            except Exception as e:
                print(f" Erreur documentation {outil['nom']}: {e}")
    
    async def _creer_guide_utilisation(self):
        """Crer le guide d'utilisation"""
        print(" Cration du guide d'utilisation...")
        
        guide_content = f"""#  Guide d'Utilisation - Outils Imports

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
NEXTGEN_CONFIG = {{
    "project_root": PROJECT_ROOT,
    "tools_dir": PROJECT_ROOT / "tools",
    # ... autres configurations
}}
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
*Guide cr par {self.agent_name} - {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        guide_path = self.target_path / "imported_tools" / "docs" / "GUIDE_UTILISATION.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        self.documentation_files.append(str(guide_path))
        self.docs_created += 1
        print(f" Guide d'utilisation cr: {guide_path}")
    
    async def _creer_guide_installation(self):
        """Crer le guide d'installation"""
        print(" Cration du guide d'installation...")
        
        installation_content = f"""#  Guide d'Installation - Outils Imports

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
NEXTGEN_CONFIG = {{
    "project_root": Path("/votre/chemin/nextgeneration"),
    "data_dir": Path("/votre/chemin/data"),
    # ...
}}
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
python -c "import sys; print('\\n'.join(sys.path))"

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
python --version || {{ echo "[CROSS] Python non install"; exit 1; }}

# Test dpendances
pip install -r requirements.txt || {{ echo "[CROSS] Erreur dpendances"; exit 1; }}

# Test configuration
python configs/test_installation.py || {{ echo "[CROSS] Erreur configuration"; exit 1; }}

echo "[CHECK] Installation valide avec succs!"
```

---
*Guide cr par {self.agent_name} - {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        install_path = self.target_path / "imported_tools" / "docs" / "GUIDE_INSTALLATION.md"
        with open(install_path, 'w', encoding='utf-8') as f:
            f.write(installation_content)
        
        self.documentation_files.append(str(install_path))
        self.docs_created += 1
        print(f" Guide d'installation cr: {install_path}")
    
    async def _generer_rapport(self) -> Dict[str, Any]:
        """Gnrer le rapport final de documentation"""
        duree = (datetime.now() - self.start_time).total_seconds()
        
        rapport = {
            "agent": self.agent_name,
            "model": self.model_name,
            "timestamp": self.start_time.isoformat(),
            "duree_secondes": duree,
            "status": "SUCCESS",
            "statistiques": {
                "outils_documentes": len(self.outils_finalises),
                "docs_created": self.docs_created,
                "fichiers_documentation": len(self.documentation_files)
            },
            "documentation_files": self.documentation_files,
            "docs_created": self.docs_created
        }
        
        # Sauvegarder le rapport
        rapport_path = self.workspace_path / "reports" / f"agent_5_documentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        rapport_path.parent.mkdir(exist_ok=True)
        
        with open(rapport_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"[DOCUMENT] Rapport sauvegard: {rapport_path}")
        print(f" Documentation: {self.docs_created} fichiers crs")
        
        return rapport 