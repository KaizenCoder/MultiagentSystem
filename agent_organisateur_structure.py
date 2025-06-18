#!/usr/bin/env python3
"""
Agent Organisateur - Restructuration des Outils
Mission: Crer la structure modulaire et organiser les fichiers selon les standards NextGeneration
"""

import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AgentOrganisateurStructure:
    """Agent spcialis dans l'organisation et la restructuration"""
    
    def __init__(self):
        self.agent_id = f"ORGANISATEUR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_path = Path(__file__).parent
        self.tools_path = self.base_path / "tools"
        self.imported_tools_path = self.tools_path / "imported_tools"
        
        # Configuration logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du systme de logging"""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentOrganisateur_{self.agent_id}")
        
        # Handler spcifique
        handler = logging.FileHandler(log_dir / f"{self.agent_id}_organisateur.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def analyser_structure_actuelle(self) -> Dict[str, Any]:
        """Analyse la structure actuelle des outils imports"""
        self.logger.info("[SEARCH] Analyse de la structure actuelle...")
        
        structure = {
            "imported_tools_files": [],
            "subdirectories": {},
            "tools_config": None
        }
        
        # Scan des fichiers dans imported_tools
        for item in self.imported_tools_path.iterdir():
            if item.is_file():
                structure["imported_tools_files"].append({
                    "nom": item.name,
                    "chemin": str(item),
                    "taille": item.stat().st_size,
                    "extension": item.suffix
                })
            elif item.is_dir():
                structure["subdirectories"][item.name] = {
                    "chemin": str(item),
                    "fichiers": [f.name for f in item.iterdir() if f.is_file()]
                }
                
        # Lecture de la configuration
        config_file = self.imported_tools_path / "tools_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                structure["tools_config"] = json.load(f)
                
        self.logger.info(f"[CHECK] Structure analyse: {len(structure['imported_tools_files'])} fichiers, {len(structure['subdirectories'])} rpertoires")
        return structure
        
    def planifier_reorganisation(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Planifie la rorganisation selon le principe 'un rpertoire par outil'"""
        self.logger.info("[CLIPBOARD] Planification de la rorganisation...")
        
        plan = {
            "outils_a_creer": [],
            "fichiers_a_deplacer": [],
            "repertoires_a_creer": [],
            "fichiers_a_adapter": [],
            "structure_cible": {}
        }
        
        if structure["tools_config"]:
            for outil in structure["tools_config"]["nextgeneration_tools"]["tools"]:
                nom_outil = outil["name"]
                repertoire_cible = self.tools_path / nom_outil
                
                plan["outils_a_creer"].append({
                    "nom": nom_outil,
                    "repertoire_cible": str(repertoire_cible),
                    "categorie": outil["category"],
                    "priorite": outil["priority"]
                })
                
                # Structure cible pour chaque outil
                plan["structure_cible"][nom_outil] = {
                    "repertoire_principal": str(repertoire_cible),
                    "fichiers_requis": [
                        f"{nom_outil}.py",
                        "README.md",
                        "config.json",
                        "__init__.py"
                    ],
                    "sous_repertoires": [
                        "docs",
                        "tests",
                        "config"
                    ]
                }
                
        self.logger.info(f" Plan tabli: {len(plan['outils_a_creer'])} outils  restructurer")
        return plan
        
    def creer_structure_outil(self, nom_outil: str, info_outil: Dict[str, Any]) -> Dict[str, Any]:
        """Cre la structure complte pour un outil spcifique"""
        self.logger.info(f"[CONSTRUCTION] Cration de la structure pour: {nom_outil}")
        
        repertoire_outil = self.tools_path / nom_outil
        
        # Cration du rpertoire principal
        repertoire_outil.mkdir(exist_ok=True)
        
        # Cration des sous-rpertoires
        sous_repertoires = ["docs", "tests", "config", "templates"]
        for sous_rep in sous_repertoires:
            (repertoire_outil / sous_rep).mkdir(exist_ok=True)
            
        # Cration des fichiers de base
        self.creer_fichier_init(repertoire_outil / "__init__.py", nom_outil)
        self.creer_readme_outil(repertoire_outil / "README.md", nom_outil, info_outil)
        self.creer_config_outil(repertoire_outil / "config" / "config.json", nom_outil, info_outil)
        self.creer_guide_utilisation(repertoire_outil / "docs" / "USAGE.md", nom_outil)
        
        structure_creee = {
            "repertoire_principal": str(repertoire_outil),
            "sous_repertoires_crees": sous_repertoires,
            "fichiers_base_crees": ["__init__.py", "README.md", "config.json", "USAGE.md"],
            "statut": "CREE"
        }
        
        self.logger.info(f"[CHECK] Structure cre pour {nom_outil}")
        return structure_creee
        
    def migrer_fichiers_outil(self, nom_outil: str, chemin_source: str, repertoire_cible: Path) -> Dict[str, Any]:
        """Migre les fichiers d'un outil vers sa nouvelle structure"""
        self.logger.info(f" Migration des fichiers pour: {nom_outil}")
        
        resultats_migration = {
            "fichiers_migres": [],
            "fichiers_adaptes": [],
            "erreurs": []
        }
        
        try:
            # Dtermination du fichier source
            chemin_source_path = Path(chemin_source)
            if not chemin_source_path.exists():
                chemin_source_path = self.base_path / chemin_source
                
            if not chemin_source_path.exists():
                self.logger.error(f"[CROSS] Fichier source introuvable: {chemin_source}")
                resultats_migration["erreurs"].append(f"Fichier source introuvable: {chemin_source}")
                return resultats_migration
                
            # Migration du fichier principal
            fichier_cible = repertoire_cible / f"{nom_outil}.py"
            
            # Copie avec adaptation
            with open(chemin_source_path, 'r', encoding='utf-8') as source:
                contenu_original = source.read()
                
            # Adaptation du contenu
            contenu_adapte = self.adapter_contenu_outil(contenu_original, nom_outil)
            
            with open(fichier_cible, 'w', encoding='utf-8') as cible:
                cible.write(contenu_adapte)
                
            resultats_migration["fichiers_migres"].append(str(fichier_cible))
            
            # Migration des fichiers de documentation s'ils existent
            for doc_file in ["README.md", "DOC.md"]:
                doc_source = chemin_source_path.parent / f"{nom_outil}_{doc_file}"
                if doc_source.exists():
                    doc_cible = repertoire_cible / "docs" / doc_file
                    shutil.copy2(doc_source, doc_cible)
                    resultats_migration["fichiers_migres"].append(str(doc_cible))
                    
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur lors de la migration: {e}")
            resultats_migration["erreurs"].append(str(e))
            
        self.logger.info(f"[CHECK] Migration termine: {len(resultats_migration['fichiers_migres'])} fichiers migrs")
        return resultats_migration
        
    def adapter_contenu_outil(self, contenu: str, nom_outil: str) -> str:
        """Adapte le contenu d'un outil pour NextGeneration"""
        # Adaptations de base
        contenu_adapte = contenu.replace("SuperWhisper", "NextGeneration")
        contenu_adapte = contenu_adapte.replace("superwhisper", "nextgeneration")
        
        # Ajout de l'en-tte NextGeneration si absent
        if not contenu_adapte.startswith("#!/usr/bin/env python3"):
            header = f'''#!/usr/bin/env python3
"""
{nom_outil.replace('_', ' ').title()} - NextGeneration Tool
Adapt pour l'cosystme NextGeneration
"""

'''
            contenu_adapte = header + contenu_adapte
            
        return contenu_adapte
        
    def creer_fichier_init(self, chemin: Path, nom_outil: str) -> None:
        """Cre le fichier __init__.py pour l'outil"""
        contenu = f'''"""
{nom_outil.replace('_', ' ').title()} - NextGeneration Tool
"""

__version__ = "1.0.0"
__author__ = "NextGeneration Team"

# Import principal
try:
    from .{nom_outil} import *
except ImportError:
    pass
'''
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
            
    def creer_readme_outil(self, chemin: Path, nom_outil: str, info_outil: Dict[str, Any]) -> None:
        """Cre le README.md pour l'outil"""
        contenu = f'''# {nom_outil.replace('_', ' ').title()}

## Vue d'ensemble

{info_outil.get('description', f'Outil {nom_outil} adapt pour NextGeneration')}

**Catgorie**: {info_outil.get('category', 'N/A')}  
**Priorit**: {info_outil.get('priority', 'N/A')}  
**Score d'utilit**: {info_outil.get('utility_score', 'N/A')}

## Installation

```bash
# Installation des dpendances
pip install -r requirements.txt

# Test de l'outil
python tools/{nom_outil}/{nom_outil}.py --help
```

## Utilisation

```python
from tools.{nom_outil} import {nom_outil.replace('_', ' ').title().replace(' ', '')}

# Utilisation de base
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}()
result = tool.execute()
```

## Configuration

La configuration se trouve dans `config/config.json`.

## Tests

```bash
# Tests unitaires
python -m pytest tests/unit/test_{nom_outil}.py

# Tests d'intgration
python -m pytest tests/integration/test_{nom_outil}_integration.py
```

## Documentation

- [Guide d'utilisation](docs/USAGE.md)
- [Configuration avance](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)

## Support

Intgr avec le systme de logging NextGeneration.
'''
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
            
    def creer_config_outil(self, chemin: Path, nom_outil: str, info_outil: Dict[str, Any]) -> None:
        """Cre la configuration JSON pour l'outil"""
        config = {
            "tool_info": {
                "name": nom_outil,
                "version": "1.0.0",
                "category": info_outil.get("category", "general"),
                "priority": info_outil.get("priority", "MEDIUM"),
                "description": f"Outil {nom_outil} pour NextGeneration"
            },
            "settings": {
                "enabled": True,
                "debug_mode": False,
                "log_level": "INFO",
                "timeout": 30
            },
            "nextgeneration_integration": {
                "use_ng_logging": True,
                "use_ng_config": True,
                "use_ng_monitoring": True
            }
        }
        
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
    def creer_guide_utilisation(self, chemin: Path, nom_outil: str) -> None:
        """Cre le guide d'utilisation pour l'outil"""
        contenu = f'''# Guide d'Utilisation - {nom_outil.replace('_', ' ').title()}

## Configuration

### Fichier de configuration

Le fichier `config/config.json` contient tous les paramtres configurables.

### Variables d'environnement

- `NG_{nom_outil.upper()}_DEBUG`: Active le mode debug
- `NG_{nom_outil.upper()}_LOG_LEVEL`: Niveau de logging

## Utilisation en ligne de commande

```bash
# Utilisation de base
python tools/{nom_outil}/{nom_outil}.py

# Avec options
python tools/{nom_outil}/{nom_outil}.py --option valeur

# Mode debug
python tools/{nom_outil}/{nom_outil}.py --debug
```

## Utilisation programmatique

```python
from tools.{nom_outil} import {nom_outil.replace('_', ' ').title().replace(' ', '')}

# Instance de base
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}()

# Configuration personnalise
tool = {nom_outil.replace('_', ' ').title().replace(' ', '')}(config_file="custom_config.json")

# Excution
result = tool.execute()
```

## Exemples

### Exemple 1: Utilisation basique

```python
# Code d'exemple  adapter selon l'outil
```

### Exemple 2: Configuration avance

```python
# Code d'exemple avanc  adapter
```

## Dpannage

### Problmes courants

1. **Erreur de configuration**: Vrifier le fichier `config/config.json`
2. **Permissions**: Vrifier les droits d'accs aux fichiers
3. **Dpendances**: Vrifier l'installation avec `pip list`

### Logs

Les logs sont disponibles dans le systme de logging NextGeneration.

```bash
# Consultation des logs
tail -f logs/{nom_outil}.log
```
'''
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
            
    def executer_reorganisation_complete(self) -> Dict[str, Any]:
        """Excute la rorganisation complte des outils"""
        self.logger.info("[ROCKET] Dmarrage de la rorganisation complte")
        
        # Phase 1: Analyse
        structure_actuelle = self.analyser_structure_actuelle()
        
        # Phase 2: Planification
        plan = self.planifier_reorganisation(structure_actuelle)
        
        # Phase 3: Excution
        resultats = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "structure_actuelle": structure_actuelle,
            "plan_reorganisation": plan,
            "resultats_creation": {},
            "resultats_migration": {},
            "erreurs": [],
            "statut_global": "EN_COURS"
        }
        
        # Cration des structures pour chaque outil
        if structure_actuelle["tools_config"]:
            for outil in structure_actuelle["tools_config"]["nextgeneration_tools"]["tools"]:
                nom_outil = outil["name"]
                
                try:
                    # Cration de la structure
                    result_creation = self.creer_structure_outil(nom_outil, outil)
                    resultats["resultats_creation"][nom_outil] = result_creation
                    
                    # Migration des fichiers
                    repertoire_cible = Path(result_creation["repertoire_principal"])
                    result_migration = self.migrer_fichiers_outil(nom_outil, outil["path"], repertoire_cible)
                    resultats["resultats_migration"][nom_outil] = result_migration
                    
                except Exception as e:
                    self.logger.error(f"[CROSS] Erreur pour {nom_outil}: {e}")
                    resultats["erreurs"].append(f"{nom_outil}: {str(e)}")
                    
        # Dtermination du statut final
        if not resultats["erreurs"]:
            resultats["statut_global"] = "REUSSI"
        elif len(resultats["erreurs"]) < len(structure_actuelle["tools_config"]["nextgeneration_tools"]["tools"]):
            resultats["statut_global"] = "PARTIEL"
        else:
            resultats["statut_global"] = "ECHEC"
            
        # Sauvegarde du rapport
        self.sauvegarder_rapport(resultats)
        
        self.logger.info(f"[CHECK] Rorganisation termine: {resultats['statut_global']}")
        return resultats
        
    def sauvegarder_rapport(self, resultats: Dict[str, Any]) -> None:
        """Sauvegarde le rapport de rorganisation"""
        rapport_file = self.base_path / "logs" / f"{self.agent_id}_reorganisation.json"
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"[CHART] Rapport de rorganisation sauvegard: {rapport_file}")

if __name__ == "__main__":
    agent = AgentOrganisateurStructure()
    rapport = agent.executer_reorganisation_complete()
    
    print(f"\n[CONSTRUCTION] Rorganisation termine")
    print(f"[CLIPBOARD] Agent ID: {rapport['agent_id']}")
    print(f"[FOLDER] Structures cres: {len(rapport['resultats_creation'])}")
    print(f" Migrations effectues: {len(rapport['resultats_migration'])}")
    print(f"[TOOL] Statut global: {rapport['statut_global']}")
    if rapport["erreurs"]:
        print(f" Erreurs: {len(rapport['erreurs'])}") 