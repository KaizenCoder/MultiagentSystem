#!/usr/bin/env python3
"""
Agent Adaptateur Documentation - Standardisation et Amlioration
Mission: Adapter et amliorer la documentation selon les standards NextGeneration
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AgentAdaptateurDocumentation:
    """Agent spcialis dans l'adaptation de la documentation"""
    
    def __init__(self):
        self.agent_id = f"ADAPTATEUR_DOC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = Path(__file__).parent
        self.tools_path = self.base_path / "tools"
        
        # Configuration logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du systme de logging"""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentAdaptateurDoc_{self.agent_id}")
        
        # Handler spcifique
        handler = logging.FileHandler(log_dir / f"{self.agent_id}_adaptateur_doc.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def identifier_outils_documentation(self) -> List[Dict[str, Any]]:
        """Identifie les outils ncessitant une adaptation de documentation"""
        self.logger.info("[SEARCH] Identification des outils pour adaptation documentation")
        
        outils_documentation = []
        
        for outil_dir in self.tools_path.iterdir():
            if outil_dir.is_dir() and outil_dir.name not in ["imported_tools", "__pycache__"]:
                # Vrification structure documentation
                docs_dir = outil_dir / "docs"
                readme_file = outil_dir / "README.md"
                config_file = outil_dir / "config" / "config.json"
                
                info_outil = {
                    "nom": outil_dir.name,
                    "repertoire": str(outil_dir),
                    "docs_dir_existe": docs_dir.exists(),
                    "readme_existe": readme_file.exists(),
                    "config_existe": config_file.exists(),
                    "fichiers_documentation": []
                }
                
                # Scan des fichiers de documentation existants
                if docs_dir.exists():
                    for doc_file in docs_dir.glob("*.md"):
                        info_outil["fichiers_documentation"].append(doc_file.name)
                        
                outils_documentation.append(info_outil)
                
        self.logger.info(f"[CHECK] {len(outils_documentation)} outils identifis pour documentation")
        return outils_documentation
        
    def adapter_readme_outil(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Adapte le README d'un outil aux standards NextGeneration"""
        self.logger.info(f" Adaptation README pour: {nom_outil}")
        
        readme_path = Path(info_outil["repertoire"]) / "README.md"
        
        try:
            # Lecture du README existant s'il existe
            contenu_existant = ""
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    contenu_existant = f.read()
                    
            # Gnration du nouveau README adapt
            nouveau_readme = self.generer_readme_ameliore(nom_outil, info_outil, contenu_existant)
            
            # Sauvegarde du README amlior
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(nouveau_readme)
                
            return {
                "fichier": str(readme_path),
                "statut": "ADAPTE",
                "taille_originale": len(contenu_existant),
                "taille_nouvelle": len(nouveau_readme)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur adaptation README {nom_outil}: {e}")
            return {"erreur": str(e), "statut": "ECHEC"}
            
    def generer_readme_ameliore(self, nom_outil: str, info_outil: Dict[str, Any], contenu_existant: str) -> str:
        """Gnre un README amlior selon les standards NextGeneration"""
        
        # Extraction d'informations du contenu existant
        description_existante = self.extraire_description_existante(contenu_existant)
        
        readme_content = f"""# {nom_outil.replace('_', ' ').title()} - NextGeneration

## [TARGET] Vue d'ensemble

{description_existante or f'Outil {nom_outil} adapt et intgr  l\'cosystme NextGeneration.'}

###  Fonctionnalits principales
- [TOOL] Outil spcialis adapt pour NextGeneration
-  Configuration flexible et modulaire
- [CHART] Intgration complte avec le monitoring NextGeneration
-  Scurit et validation intgres

## [CLIPBOARD] Prrequis

- Python 3.8+
- NextGeneration Core Framework
- Dpendances spcifiques (voir requirements.txt)

## [ROCKET] Installation

### Installation rapide
```bash
# Depuis le rpertoire NextGeneration
cd tools/{nom_outil}

# Installation des dpendances
pip install -r requirements.txt

# Test de fonctionnement
python {nom_outil}.py --help
```

### Installation pour dveloppement
```bash
# Installation en mode dveloppement
pip install -e .

# Installation des dpendances de dveloppement
pip install -r requirements-dev.txt
```

##  Utilisation

### Utilisation en ligne de commande

```bash
# Utilisation basique
python tools/{nom_outil}/{nom_outil}.py

# Avec configuration personnalise
python tools/{nom_outil}/{nom_outil}.py --config custom_config.json

# Mode debug
python tools/{nom_outil}/{nom_outil}.py --debug --verbose
```

### Utilisation programmatique

```python
from tools.{nom_outil} import {nom_outil.replace('_', ' ').title().replace(' ', '')}

# Instance avec configuration par dfaut
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}()

# Configuration personnalise
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}(
    config_file="config/custom.json",
    debug=True
)

# Excution
result = tool.execute()
print(f"Rsultat: {{result}}")
```

##  Configuration

### Fichier de configuration principal

Le fichier `config/config.json` contient tous les paramtres configurables :

```json
{{
  "tool_info": {{
    "name": "{nom_outil}",
    "version": "1.0.0",
    "enabled": true
  }},
  "settings": {{
    "debug_mode": false,
    "log_level": "INFO",
    "timeout": 30
  }},
  "nextgeneration_integration": {{
    "use_ng_logging": true,
    "use_ng_monitoring": true
  }}
}}
```

### Variables d'environnement

| Variable | Description | Dfaut |
|----------|-------------|--------|
| `NG_{nom_outil.upper()}_DEBUG` | Active le mode debug | `false` |
| `NG_{nom_outil.upper()}_LOG_LEVEL` | Niveau de logging | `INFO` |
| `NG_{nom_outil.upper()}_CONFIG` | Chemin configuration personnalise | `config/config.json` |

##  Tests

### Tests unitaires
```bash
# Tests unitaires complets
python -m pytest tests/unit/test_{nom_outil}.py -v

# Tests avec couverture
python -m pytest tests/unit/test_{nom_outil}.py --cov={nom_outil}
```

### Tests d'intgration
```bash
# Tests d'intgration NextGeneration
python -m pytest tests/integration/test_{nom_outil}_integration.py -v

# Tests de performance
python -m pytest tests/integration/test_{nom_outil}_performance.py
```

### Tests manuels
```bash
# Test rapide de fonctionnement
python tools/{nom_outil}/{nom_outil}.py --test

# Validation configuration
python tools/{nom_outil}/{nom_outil}.py --validate-config
```

## [CHART] Monitoring et Observabilit

L'outil est intgr avec le systme de monitoring NextGeneration :

- **Logs** : Disponibles dans le systme centralis NextGeneration
- **Mtriques** : Collectes automatiquement
- **Alertes** : Configures selon les seuils NextGeneration

### Consultation des mtriques
```bash
# Logs en temps rel
tail -f logs/{nom_outil}.log

# Mtriques de performance
curl http://localhost:9090/metrics | grep {nom_outil}
```

## [TOOL] Dpannage

### Problmes courants

#### Erreur de configuration
```bash
# Validation de la configuration
python tools/{nom_outil}/{nom_outil}.py --validate-config

# Rgnration configuration par dfaut
python tools/{nom_outil}/{nom_outil}.py --reset-config
```

#### Problmes de permissions
```bash
# Vrification des permissions
ls -la tools/{nom_outil}/

# Correction des permissions (Linux/Mac)
chmod +x tools/{nom_outil}/{nom_outil}.py
```

#### Dpendances manquantes
```bash
# Vrification des dpendances
pip check

# Rinstallation propre
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Logs et diagnostics

```bash
# Logs dtaills
export NG_{nom_outil.upper()}_LOG_LEVEL=DEBUG
python tools/{nom_outil}/{nom_outil}.py

# Mode diagnostic
python tools/{nom_outil}/{nom_outil}.py --diagnostic

# Rapport d'tat
python tools/{nom_outil}/{nom_outil}.py --status
```

##  Documentation

- [Guide d'utilisation dtaill](docs/USAGE.md)
- [Configuration avance](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)
- [Guide de dveloppement](docs/DEVELOPMENT.md)
- [FAQ](docs/FAQ.md)

##  Contribution

### Dveloppement local
```bash
# Clone et setup
git clone <repo>
cd tools/{nom_outil}

# Environnement de dveloppement
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows

pip install -r requirements-dev.txt
```

### Tests avant contribution
```bash
# Tests complets
make test

# Vrification qualit code
make lint
make format

# Tests de scurit
make security-check
```

## [DOCUMENT] Licence

Distribu sous licence NextGeneration. Voir `LICENSE` pour plus d'informations.

##  Liens utiles

- [Documentation NextGeneration](../docs/)
- [Issues et support](https://github.com/nextgeneration/issues)
- [Roadmap](https://github.com/nextgeneration/projects)

---

**Intgr avec  dans l'cosystme NextGeneration**
"""
        
        return readme_content
        
    def extraire_description_existante(self, contenu: str) -> str:
        """Extrait la description existante du README"""
        if not contenu:
            return ""
            
        # Recherche de patterns de description
        lignes = contenu.split('\n')
        for i, ligne in enumerate(lignes):
            if ligne.strip().startswith('##') and 'vue' in ligne.lower():
                # Rcupration du paragraphe suivant
                if i + 1 < len(lignes):
                    return lignes[i + 1].strip()
                    
        return ""
        
    def creer_documentation_manquante(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Cre la documentation manquante pour un outil"""
        self.logger.info(f"[DOCUMENT] Cration documentation manquante pour: {nom_outil}")
        
        docs_dir = Path(info_outil["repertoire"]) / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        fichiers_crees = []
        
        # Documents de base  crer
        documents_base = {
            "USAGE.md": self.generer_guide_usage,
            "CONFIGURATION.md": self.generer_guide_configuration,
            "API.md": self.generer_documentation_api,
            "DEVELOPMENT.md": self.generer_guide_developpement,
            "FAQ.md": self.generer_faq
        }
        
        try:
            for nom_doc, generateur in documents_base.items():
                doc_path = docs_dir / nom_doc
                
                if not doc_path.exists():
                    contenu_doc = generateur(nom_outil, info_outil)
                    
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(contenu_doc)
                        
                    fichiers_crees.append(nom_doc)
                    
            return {
                "statut": "CREE",
                "fichiers_crees": fichiers_crees,
                "repertoire": str(docs_dir)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur cration documentation {nom_outil}: {e}")
            return {"erreur": str(e), "statut": "ECHEC"}
            
    def generer_guide_usage(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre le guide d'utilisation dtaill"""
        return f"""# Guide d'Utilisation - {nom_outil.replace('_', ' ').title()}

## Introduction

Ce guide dtaille l'utilisation de l'outil {nom_outil} dans l'cosystme NextGeneration.

## Utilisation de base

### Ligne de commande
```bash
python tools/{nom_outil}/{nom_outil}.py [options]
```

### Options disponibles
- `--help` : Affiche l'aide
- `--config PATH` : Spcifie un fichier de configuration
- `--debug` : Active le mode debug
- `--verbose` : Mode verbeux

## Exemples pratiques

### Exemple 1: Utilisation standard
```bash
python tools/{nom_outil}/{nom_outil}.py
```

### Exemple 2: Configuration personnalise
```bash
python tools/{nom_outil}/{nom_outil}.py --config config/custom.json
```

## Intgration programmatique

```python
from tools.{nom_outil} import {nom_outil.replace('_', ' ').title().replace(' ', '')}

# Utilisation basique
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}()
result = tool.execute()
```

## Bonnes pratiques

1. Toujours tester en mode debug d'abord
2. Utiliser des configurations spcifiques par environnement
3. Monitorer les logs pour diagnostiquer les problmes
4. Valider les rsultats avant utilisation en production
"""

    def generer_guide_configuration(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre le guide de configuration"""
        return f"""# Configuration - {nom_outil.replace('_', ' ').title()}

## Structure de configuration

Le fichier `config/config.json` utilise la structure suivante :

```json
{{
  "tool_info": {{
    "name": "{nom_outil}",
    "version": "1.0.0",
    "enabled": true
  }},
  "settings": {{
    "debug_mode": false,
    "log_level": "INFO",
    "timeout": 30
  }},
  "nextgeneration_integration": {{
    "use_ng_logging": true,
    "use_ng_monitoring": true
  }}
}}
```

## Paramtres dtaills

### Section tool_info
- `name` : Nom de l'outil
- `version` : Version de l'outil
- `enabled` : Active/dsactive l'outil

### Section settings
- `debug_mode` : Mode debug (true/false)
- `log_level` : Niveau de logging (DEBUG, INFO, WARNING, ERROR)
- `timeout` : Timeout en secondes

### Section nextgeneration_integration
- `use_ng_logging` : Utilise le systme de logging NextGeneration
- `use_ng_monitoring` : Active le monitoring NextGeneration

## Variables d'environnement

Les variables d'environnement ont priorit sur la configuration fichier :

- `NG_{nom_outil.upper()}_DEBUG=true`
- `NG_{nom_outil.upper()}_LOG_LEVEL=DEBUG`
- `NG_{nom_outil.upper()}_TIMEOUT=60`

## Configuration par environnement

### Dveloppement
```json
{{
  "settings": {{
    "debug_mode": true,
    "log_level": "DEBUG",
    "timeout": 60
  }}
}}
```

### Production
```json
{{
  "settings": {{
    "debug_mode": false,
    "log_level": "INFO",
    "timeout": 30
  }}
}}
```
"""

    def generer_documentation_api(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre la documentation API"""
        return f"""# API Reference - {nom_outil.replace('_', ' ').title()}

## Classes principales

### {nom_outil.replace('_', ' ').title().replace(' ', '')}

Classe principale de l'outil {nom_outil}.

#### Constructeur
```python
{nom_outil.replace('_', ' ').title().replace(' ', '')}(config_file=None, debug=False)
```

**Paramtres:**
- `config_file` (str, optionnel) : Chemin vers le fichier de configuration
- `debug` (bool, optionnel) : Active le mode debug

#### Mthodes

##### execute()
Excute l'outil avec la configuration actuelle.

```python
def execute() -> Dict[str, Any]:
    \"\"\"
    Excute l'outil
    
    Returns:
        Dict contenant les rsultats de l'excution
    \"\"\"
```

##### validate_config()
Valide la configuration actuelle.

```python
def validate_config() -> bool:
    \"\"\"
    Valide la configuration
    
    Returns:
        True si la configuration est valide
    \"\"\"
```

## Exceptions

### ToolConfigurationError
Leve en cas de problme de configuration.

### ToolExecutionError
Leve en cas d'erreur d'excution.

## Exemples d'utilisation

```python
from tools.{nom_outil} import {nom_outil.replace('_', ' ').title().replace(' ', '')}

# Instance basique
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}()

# Validation configuration
if tool.validate_config():
    result = tool.execute()
    print(result)
```
"""

    def generer_guide_developpement(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre le guide de dveloppement"""
        return f"""# Guide de Dveloppement - {nom_outil.replace('_', ' ').title()}

## Architecture

L'outil {nom_outil} suit l'architecture modulaire NextGeneration.

## Structure du code

```
tools/{nom_outil}/
 {nom_outil}.py          # Module principal
 __init__.py             # Init package
 config/
    config.json        # Configuration
 docs/                  # Documentation
 tests/                 # Tests
 templates/            # Templates
```

## Standards de dveloppement

### Code Style
- PEP 8 pour Python
- Type hints obligatoires
- Docstrings pour toutes les fonctions publiques

### Tests
- Tests unitaires avec pytest
- Couverture minimale de 80%
- Tests d'intgration obligatoires

### Documentation
- README.md  jour
- Documentation API complte
- Exemples d'utilisation

## Workflow de dveloppement

1. Fork du repository
2. Cration d'une branche feature
3. Dveloppement avec tests
4. Pull request avec review
5. Merge aprs validation

## Debug et profiling

```python
# Mode debug
export NG_{nom_outil.upper()}_DEBUG=true
python tools/{nom_outil}/{nom_outil}.py

# Profiling
python -m cProfile tools/{nom_outil}/{nom_outil}.py
```
"""

    def generer_faq(self, nom_outil: str, info_outil: Dict[str, Any]) -> str:
        """Gnre la FAQ"""
        return f"""# FAQ - {nom_outil.replace('_', ' ').title()}

## Questions frquentes

### Q: Comment installer l'outil ?
R: Suivez les instructions dans le README.md principal.

### Q: L'outil ne dmarre pas, que faire ?
R: 
1. Vrifiez la configuration avec `--validate-config`
2. Consultez les logs en mode debug
3. Vrifiez les dpendances avec `pip check`

### Q: Comment personnaliser la configuration ?
R: Copiez `config/config.json` et adaptez selon vos besoins.

### Q: L'outil est-il compatible avec d'autres outils NextGeneration ?
R: Oui, tous les outils NextGeneration sont conus pour l'interoprabilit.

### Q: Comment contribuer au dveloppement ?
R: Consultez le guide de dveloppement dans docs/DEVELOPMENT.md.

### Q: O trouver de l'aide ?
R: 
- Documentation dans docs/
- Issues GitHub
- Community NextGeneration

## Problmes connus

### Problme de performance
**Symptme** : L'outil est lent
**Solution** : Vrifiez la configuration timeout et les ressources systme

### Erreur de configuration
**Symptme** : Erreur au dmarrage
**Solution** : Validez le fichier config.json avec un validateur JSON

## Contact

Pour toute question non couverte par cette FAQ, consultez la documentation complte ou ouvrez une issue.
"""

    def mettre_a_jour_documentation_globale(self) -> Dict[str, Any]:
        """Met  jour la documentation globale du rpertoire tools"""
        self.logger.info(" Mise  jour documentation globale tools")
        
        try:
            # Cration du README principal tools
            tools_readme = self.tools_path / "README.md"
            contenu_readme = self.generer_readme_tools_global()
            
            with open(tools_readme, 'w', encoding='utf-8') as f:
                f.write(contenu_readme)
                
            return {
                "statut": "MISE_A_JOUR",
                "fichier": str(tools_readme),
                "taille": len(contenu_readme)
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur mise  jour documentation globale: {e}")
            return {"erreur": str(e), "statut": "ECHEC"}
            
    def generer_readme_tools_global(self) -> str:
        """Gnre le README global du rpertoire tools"""
        
        # Scan des outils disponibles
        outils_disponibles = []
        for outil_dir in self.tools_path.iterdir():
            if outil_dir.is_dir() and outil_dir.name not in ["imported_tools", "__pycache__"]:
                config_file = outil_dir / "config" / "config.json"
                info_outil = {"nom": outil_dir.name, "description": f"Outil {outil_dir.name}"}
                
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                            info_outil.update(config.get("tool_info", {}))
                    except:
                        pass
                        
                outils_disponibles.append(info_outil)
                
        readme_content = f"""# NextGeneration Tools

## [TARGET] Vue d'ensemble

Collection d'outils spcialiss pour l'cosystme NextGeneration. Chaque outil est conu pour tre modulaire, configurable et parfaitement intgr avec l'infrastructure NextGeneration.

## [TOOL] Outils disponibles

| Outil | Description | Statut |
|-------|-------------|--------|
"""

        for outil in outils_disponibles:
            nom = outil["nom"]
            description = outil.get("description", f"Outil {nom}")
            readme_content += f"| [{nom}]({nom}/) | {description} | [CHECK] Actif |\n"
            
        readme_content += f"""

## [CLIPBOARD] Installation globale

```bash
# Installation de tous les outils
pip install -r requirements.txt

# Test de tous les outils
python -m pytest tests/ -v
```

## [ROCKET] Utilisation rapide

### Excution d'un outil spcifique
```bash
# Structure gnrale
python tools/[nom_outil]/[nom_outil].py [options]

# Exemple
python tools/install_phase3_dependencies/install_phase3_dependencies.py --help
```

### Utilisation programmatique
```python
# Import d'un outil
from tools.install_phase3_dependencies import InstallPhase3Dependencies

# Utilisation
tool = InstallPhase3Dependencies()
result = tool.execute()
```

##  Architecture

Chaque outil suit la structure standard NextGeneration :

```
tools/[nom_outil]/
 [nom_outil].py         # Module principal
 __init__.py            # Package init
 README.md              # Documentation outil
 config/
    config.json        # Configuration
 docs/                  # Documentation dtaille
    USAGE.md
    CONFIGURATION.md
    API.md
    FAQ.md
 tests/                 # Tests spcifiques
 templates/            # Templates si ncessaire
```

##  Tests

### Tests individuels
```bash
# Test d'un outil spcifique
python -m pytest tests/unit/test_[nom_outil].py
python -m pytest tests/integration/test_[nom_outil]_integration.py
```

### Tests globaux
```bash
# Tous les tests
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest tests/ --cov=tools/
```

## [CHART] Monitoring

Tous les outils sont intgrs avec :
- **Logging centralis** NextGeneration
- **Mtriques automatiques** via Prometheus
- **Alerting** configurable
- **Tracing distribu**

## [TOOL] Configuration

### Configuration globale
Variables d'environnement communes :
- `NG_LOG_LEVEL` : Niveau de logging global
- `NG_DEBUG` : Mode debug global
- `NG_CONFIG_DIR` : Rpertoire de configuration

### Configuration par outil
Chaque outil a sa configuration dans `config/config.json` :
```json
{{
  "tool_info": {{ "name": "...", "version": "..." }},
  "settings": {{ ... }},
  "nextgeneration_integration": {{ ... }}
}}
```

##  Dveloppement

### Ajout d'un nouvel outil

1. **Crer la structure**
```bash
mkdir tools/mon_nouvel_outil
cd tools/mon_nouvel_outil
```

2. **Crer les fichiers de base**
```bash
touch mon_nouvel_outil.py
touch __init__.py
touch README.md
mkdir {{config,docs,tests,templates}}
```

3. **Suivre les standards**
- Code Python avec type hints
- Tests unitaires et d'intgration
- Documentation complte
- Configuration JSON

### Standards qualit
- PEP 8 compliance
- Type hints obligatoires
- Couverture tests > 80%
- Documentation API complte

##  Documentation

- [Guide d'architecture](../docs/architecture/)
- [Standards de dveloppement](../docs/development/)
- [Guide de contribution](../CONTRIBUTING.md)

##  Liens utiles

- **Documentation NextGeneration** : [../docs/](../docs/)
- **Tests globaux** : [../tests/](../tests/)
- **Monitoring** : [../monitoring/](../monitoring/)
- **Configuration** : [../config/](../config/)

---

**cosystme NextGeneration - Outils intgrs et optimiss** [ROCKET]

Nombre d'outils actifs : **{len(outils_disponibles)}**  
Dernire mise  jour : **{datetime.now().strftime('%Y-%m-%d %H:%M')}**
"""

        return readme_content
        
    def executer_adaptation_complete(self) -> Dict[str, Any]:
        """Excute l'adaptation complte de la documentation"""
        self.logger.info("[ROCKET] Dmarrage adaptation complte documentation")
        
        # Identification des outils
        outils_documentation = self.identifier_outils_documentation()
        
        resultats = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "outils_traites": len(outils_documentation),
            "adaptations_readme": {},
            "documentations_creees": {},
            "documentation_globale": {},
            "statut_global": "EN_COURS"
        }
        
        # Adaptation des README
        for outil in outils_documentation:
            nom_outil = outil["nom"]
            try:
                result_readme = self.adapter_readme_outil(nom_outil, outil)
                resultats["adaptations_readme"][nom_outil] = result_readme
                
                result_docs = self.creer_documentation_manquante(nom_outil, outil)
                resultats["documentations_creees"][nom_outil] = result_docs
                
            except Exception as e:
                self.logger.error(f"[CROSS] Erreur adaptation {nom_outil}: {e}")
                resultats["adaptations_readme"][nom_outil] = {"erreur": str(e)}
                
        # Mise  jour documentation globale
        try:
            result_global = self.mettre_a_jour_documentation_globale()
            resultats["documentation_globale"] = result_global
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur documentation globale: {e}")
            resultats["documentation_globale"] = {"erreur": str(e)}
            
        # Dtermination statut
        erreurs = sum(1 for r in resultats["adaptations_readme"].values() if "erreur" in r)
        if erreurs == 0:
            resultats["statut_global"] = "REUSSI"
        elif erreurs < len(outils_documentation):
            resultats["statut_global"] = "PARTIEL"
        else:
            resultats["statut_global"] = "ECHEC"
            
        # Sauvegarde rapport
        self.sauvegarder_rapport_documentation(resultats)
        
        self.logger.info("[CHECK] Adaptation documentation termine")
        return resultats
        
    def sauvegarder_rapport_documentation(self, resultats: Dict[str, Any]) -> None:
        """Sauvegarde le rapport d'adaptation documentation"""
        rapport_file = self.base_path / "logs" / f"{self.agent_id}_adaptation_documentation.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHART] Rapport documentation sauvegard: {rapport_file}")

if __name__ == "__main__":
    agent = AgentAdaptateurDocumentation()
    rapport = agent.executer_adaptation_complete()
    
    print(f"\n Adaptation documentation termine")
    print(f"[CLIPBOARD] Agent ID: {rapport['agent_id']}")
    print(f"[TOOL] Outils traits: {rapport['outils_traites']}")
    print(f" README adapts: {len(rapport['adaptations_readme'])}")
    print(f"[DOCUMENT] Documentations cres: {len(rapport['documentations_creees'])}")
    print(f"[TARGET] Statut global: {rapport['statut_global']}") 