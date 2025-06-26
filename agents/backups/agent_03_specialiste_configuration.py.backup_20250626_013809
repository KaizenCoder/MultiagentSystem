#!/usr/bin/env python3
"""
[TOOL] AGENT 03 - SPECIALISTE CONFIGURATION
Partie de l'équipe Agent Factory Pattern - 17 Agents Spécialisés

MISSION : Configuration Pydantic centralisée selon plan Sprint 0
RESPONSABILITÉS :
- Implémentation agent_config.py selon spécifications expertes
- Configuration environnements (dev/staging/prod)
- Variables environnement sécurisées
- TTL adaptatif (60s dev, 600s prod)
- Configuration cache LRU + ThreadPool
- Coordination avec workspace organizer

CONTRAINTES :
- UTILISATION OBLIGATOIRE spécifications du prompt parfait
- Configuration thread-safe et production-ready
- Support hot-reload et validation stricte
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging

# --- Configuration Robuste du Chemin d'Importation ---
try:
    # Ajustement pour pointer vers la racine du projet (nextgeneration/)
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    # Fallback si la structure des dossiers change
    if '.' not in sys.path:
        sys.path.insert(0, '.')

# --- Imports Post-Path-Correction ---
try:
    from core.agent_factory_architecture import Agent, Task, Result
    # NOUVEAU: Importer le schéma de configuration statique et le chemin du fichier
    from core.config_models_agent.config_models_maintenance import MaintenanceTeamConfig, AgentConfig, CONFIG_FILE_PATH
    PATTERN_FACTORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erreur d'importation critique: {e}")
    print("Veuillez vérifier que le PYTHONPATH est correctement configuré et que `core` est accessible.")
    # Fallback pour compatibilité
    class Agent:
        def __init__(self, agent_id: str, version: str, description: str, agent_type: str, status: str, **config):
            self.agent_id = agent_id or f"agent_fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.agent_type = agent_type
            self.version = version
            self.description = description
            self.status = status
            self.config = config
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(self.agent_id)
        
        def log(self, message, level="info"):
            if hasattr(self, 'logger'):
                log_func = getattr(self.logger, level, self.logger.info)
                log_func(message)
            else:
                print(f"[{level.upper()}] {message}")
                
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
        
    class Task:
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
                
    class Result:
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error
        
    PATTERN_FACTORY_AVAILABLE = False


class Agent03SpecialisteConfiguration(Agent):
    """
    Agent 03 - Spécialiste Configuration Pydantic
    
    Responsable de la configuration centralisée de l'Agent Factory
    avec support multi-environnement et validation stricte.
    """
    
    def __init__(self, agent_type: str = "specialiste_configuration", **kwargs):
        """Initialisation standardisée de l'agent."""
        # On passe l'argument explicite et le reste des kwargs à la classe de base.
        super().__init__(agent_type=agent_type, **kwargs)
        
        # Attributs spécifiques à cet agent
        self.agent_name = "Spécialiste Configuration"
        self.workspace_root = Path(__file__).resolve().parents[1]
        self.reports_dir = self.workspace_root / "reports"
        
        self.config_file_path = CONFIG_FILE_PATH
        
        self.metrics = {
            "configurations_created": 0,
            "environments_configured": 0,
            "validations_passed": 0,
            "security_features_implemented": 0,
            "performance_optimizations": 0
        }
            
        self.mission_status = "INITIALISATION"
        self.start_time = datetime.now()
            
        self.log(f"[TOOL] Agent {self.agent_id} - {self.agent_name} initialisé")
        self.log(f"[FOLDER] Workspace: {self.workspace_root}")
        self.log(f"[TARGET] Mission: Génération du fichier de configuration JSON 'maintenance_config.json'")
    
    def log(self, message: str, level: str = "info"):
        """Méthode de logging pour l'agent."""
        if hasattr(self, 'logger') and self.logger:
            log_func = getattr(self.logger, level, self.logger.info)
            log_func(message)
        else:
            # Fallback si le logger n'est pas initialisé
            print(f"[{level.upper()}] ({self.agent_id}) {message}")

    def validate_dependencies(self) -> bool:
        """Valider que les dépendances sont satisfaites"""
        self.log("[SEARCH] Validation des dépendances Agent 03...")
            
        # Vérifier que le workspace existe
        if not self.workspace_root.exists():
            self.log(f"[CROSS] Workspace non trouvé: {self.workspace_root}", level="error")
            return False
            
        # Vérifier structure de base (adapté)
        required_dirs = ["agents", "docs", "reports", "config", "core", "code_expert"]
        for dir_name in required_dirs:
            if not (self.workspace_root / dir_name).exists():
                self.log(f"[CROSS] Répertoire {dir_name} manquant dans {self.workspace_root}", level="error")
                return False
            
        self.log("[CHECK] Toutes les dépendances satisfaites")
        self.mission_status = "DÉPENDANCES_VALIDES"
        return True

    def generate_json_config(self) -> Optional[str]:
        """
        Génère le fichier de configuration JSON pour l'équipe de maintenance.
        
        Cette méthode définit la configuration statique de l'équipe,
        crée une instance du modèle Pydantic `MaintenanceTeamConfig`,
        et la sérialise en un fichier JSON.
        """
        self.log("🔧 Génération de la configuration JSON pour l'équipe de maintenance...")

        team_definition = {
            "analyseur": {
                "nom_agent": "agent_MAINTENANCE_01_analyseur_structure.py",
                "classe_agent": "AgentMAINTENANCE01AnalyseurStructure",
                "description": "Analyse la structure du code des agents cibles."
            },
            "evaluateur": {
                "nom_agent": "agent_MAINTENANCE_02_evaluateur_utilite.py",
                "classe_agent": "AgentMAINTENANCE02EvaluateurUtilite",
                "description": "Évalue l'utilité et la pertinence d'un agent pour une tâche."
            },
            "adaptateur": {
                "nom_agent": "agent_MAINTENANCE_03_adaptateur_code.py",
                "classe_agent": "AgentMAINTENANCE03AdaptateurCode",
                "description": "Adapte le code d'un agent pour correction ou amélioration."
            },
            "testeur": {
                "nom_agent": "agent_MAINTENANCE_04_testeur_anti_faux_agents.py",
                "classe_agent": "AgentMAINTENANCE04TesteurAntiFauxAgents",
                "description": "Teste les agents pour détecter les comportements anormaux ou 'faux'."
            },
            "documenteur": {
                "nom_agent": "agent_MAINTENANCE_05_documenteur_peer_reviewer.py",
                "classe_agent": "AgentMAINTENANCE05DocumenteurPeerReviewer",
                "description": "Génère de la documentation et effectue une peer-review."
            },
            "validateur": {
                "nom_agent": "agent_MAINTENANCE_06_validateur_final.py",
                "classe_agent": "AgentMAINTENANCE06ValidateurFinal",
                "description": "Valide la solution finale et s'assure de sa conformité."
            }
        }
        
        try:
            agents_config = {
                role: AgentConfig(**data) for role, data in team_definition.items()
            }

            full_config = MaintenanceTeamConfig(
                agents=agents_config,
            )
            
            config_json_str = full_config.model_dump_json(indent=4)

            self.log(f"Configuration générée. Sauvegarde dans {self.config_file_path}...")
            
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file_path, "w", encoding="utf-8") as f:
                f.write(config_json_str)

            self.log("✅ Fichier de configuration JSON sauvegardé avec succès.")
            self.metrics["configurations_created"] += 1
            return config_json_str

        except Exception as e:
            self.log(f"❌ Erreur critique lors de la génération du JSON de configuration: {e}", level="critical")
            return None

    def create_configuration_tests(self) -> str:
        """
        Génère un script de test pytest pour valider le fichier de configuration JSON.
        """
        self.log("🧪 Génération des tests pour le fichier de configuration JSON...")

        test_code = f'''"""
Tests de validation pour la configuration de maintenance (maintenance_config.json)
Généré par Agent 03 - Spécialiste Configuration
"""

import pytest
import json
from pathlib import Path
import sys

try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.config_models_agent.config_models_maintenance import MaintenanceTeamConfig, CONFIG_FILE_PATH
from pydantic import ValidationError

CONFIG_FILE = CONFIG_FILE_PATH

def test_config_file_exists():
    """Vérifie que le fichier de configuration JSON existe."""
    assert CONFIG_FILE.exists(), f"Le fichier de configuration {{CONFIG_FILE}} est manquant."

def test_config_is_valid_json():
    """Vérifie que le fichier est un JSON valide."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Le fichier de configuration n'est pas un JSON valide.")

def test_config_conforms_to_schema():
    """Vérifie que la configuration est conforme au schéma Pydantic."""
    try:
        MaintenanceTeamConfig()
    except ValidationError as e:
        pytest.fail(f"La configuration JSON ne correspond pas au schéma Pydantic: \\n{{e}}")
    except FileNotFoundError:
        pytest.fail("L'instanciation de MaintenanceTeamConfig n'a pas trouvé le fichier.")

def test_all_agents_have_required_fields():
    """Vérifie que chaque agent dans la configuration a les champs requis."""
    config = MaintenanceTeamConfig()
    for role, agent_conf in config.agents.items():
        assert hasattr(agent_conf, 'nom_agent') and agent_conf.nom_agent, f"L'agent '{{role}}' n'a pas de 'nom_agent'."
        assert hasattr(agent_conf, 'classe_agent') and agent_conf.classe_agent, f"L'agent '{{role}}' n'a pas de 'classe_agent'."
'''
        self.log("✅ Script de test généré.")
        return test_code

    def create_integration_guide(self) -> str:
        """Crée un guide d'intégration Markdown pour la nouvelle configuration."""
        self.log("📖 Génération du guide d'intégration...")

        guide_content = f'''
# Guide d'Intégration de la Configuration de Maintenance

Document généré par l'Agent 03 - Spécialiste Configuration le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

## 1. Vue d'ensemble

La configuration de l'équipe de maintenance est désormais gérée de manière centralisée et statique pour améliorer la robustesse et éviter les dépendances circulaires au démarrage.

- **Schéma de configuration** : La structure est définie dans `core/config_models_agent/config_models_maintenance.py`.
- **Fichier de valeurs** : Les valeurs de configuration sont stockées dans `{self.config_file_path.name}`, situé dans le répertoire `config/`.

## 2. Comment Accéder à la Configuration

Pour charger la configuration dans n'importe quel agent ou service, utilisez la fonction utilitaire `get_maintenance_config()`.

### Exemple d'utilisation

```python
from core.config_models_agent.config_models_maintenance import get_maintenance_config
from pydantic import ValidationError

try:
    config = get_maintenance_config()
    analyseur_config = config.agents.get("analyseur")
    if analyseur_config:
        print(f"Classe de l'analyseur : {{analyseur_config.classe_agent}}")
except FileNotFoundError as e:
    print(f"ERREUR : Le fichier de configuration est manquant. {{e}}")
except ValidationError as e:
    print(f"ERREUR : Le fichier de configuration est invalide. {{e}}")
```

## 3. Mise à jour de la Configuration

Pour modifier la composition de l'équipe, ré-exécutez la mission de l'Agent 03.
'''
        self.log("✅ Guide d'intégration généré.")
        return guide_content

    def generate_agent_03_report(self) -> str:
        """
        Génère le rapport de mission final de l'agent.
        """
        self.log("📊 Génération du rapport de mission final...")
        duration = (datetime.now() - self.start_time).total_seconds()
        
        report = f"""
# RAPPORT DE MISSION - AGENT 03 : SPÉCIALISTE CONFIGURATION
- **Statut Final** : {self.mission_status}
- **Durée** : {duration:.2f} secondes
- **Date** : {datetime.now().isoformat()}

## Actions Réalisées
1.  **Génération du Fichier de Configuration** : `{self.config_file_path}`
2.  **Génération des Tests de Validation** : `tests/unit/test_maintenance_config.py`
3.  **Génération du Guide d'Intégration** : `docs/maintenance_config_guide.md`

## Prochaines Étapes
1.  Adapter le Chef d'Équipe pour utiliser `get_maintenance_config()`.
2.  Lancer `pytest tests/unit/test_maintenance_config.py`.
3.  Valider le workflow complet avec `test_maintenance_workflow.py`.
"""
        return report

    def execute_mission(self) -> bool:
        """Exécute la mission complète de l'agent."""
        self.log(f"🚀 Démarrage de la mission pour l'agent {self.agent_name}")
        self.mission_status = "EN_COURS"

        if not self.validate_dependencies():
            self.mission_status = "ÉCHEC_DÉPENDANCES"
            self.log("Mission annulée.", level="error")
            return False

        if not self.generate_json_config():
            self.mission_status = "ÉCHEC_GÉNÉRATION_CONFIG"
            return False

        test_script_content = self.create_configuration_tests()
        integration_guide_content = self.create_integration_guide()

        try:
            test_file_path = self.workspace_root / "tests" / "unit" / "test_maintenance_config.py"
            test_file_path.parent.mkdir(exist_ok=True, parents=True)
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(test_script_content)
            self.log(f"✅ Script de test sauvegardé dans : {test_file_path}")

            guide_path = self.workspace_root / "docs" / "maintenance_config_guide.md"
            guide_path.parent.mkdir(exist_ok=True, parents=True)
            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(integration_guide_content)
            self.log(f"✅ Guide d'intégration sauvegardé dans : {guide_path}")

        except IOError as e:
            self.log(f"❌ Erreur lors de la sauvegarde des artefacts : {e}", level="critical")
            self.mission_status = "ÉCHEC_SAUVEGARDE"
            return False

        report_content = self.generate_agent_03_report()
        report_path = self.reports_dir / f"rapport_specialiste_config_{self.start_time.strftime('%Y%m%d_%H%M%S')}.md"
        try:
            report_path.parent.mkdir(exist_ok=True, parents=True)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            self.log(f"📊 Rapport de mission finalisé et sauvegardé dans {report_path}")
        except IOError as e:
            self.log(f"Impossible de sauvegarder le rapport final : {e}", level="error")

        self.mission_status = "SUCCÈS"
        self.log("✅ Mission de configuration terminée avec succès !")
        return True

    async def startup(self):
        self.log(f"Agent {self.agent_name} - DÉMARRAGE.")
        pass

    async def shutdown(self):
        self.log(f"Agent {self.agent_name} - ARRÊT.")
        pass

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "agent_id": self.agent_id}

    async def execute_task(self, task: Any) -> Any:
        self.log(f"Tâche reçue : {getattr(task, 'id', 'N/A')}")
        
        if not hasattr(task, 'type') or task.type != "generate_maintenance_config":
            error_msg = "Type de tâche non supporté. Attendu: 'generate_maintenance_config'"
            self.log(error_msg, level="warning")
            return Result(success=False, error=error_msg)
            
        success = self.execute_mission()
        
        if success:
            report = self.generate_agent_03_report()
            return Result(success=True, data={"report_summary": report, "config_file": str(self.config_file_path)})
        else:
            return Result(success=False, error=f"Échec de la mission. Statut: {self.mission_status}")

    def get_capabilities(self) -> List[str]:
        return ["generate_maintenance_config"]

def create_agent_03_specialiste_configuration(**config) -> "Agent03SpecialisteConfiguration":
    # La nouvelle signature de __init__ gère le type par défaut.
    return Agent03SpecialisteConfiguration(**config)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("--- Mode d'Exécution Standalone ---")
    agent = create_agent_03_specialiste_configuration()
    
    mission_success = agent.execute_mission()
    
    if mission_success:
        print("\n[SUCCÈS] La mission de l'agent s'est terminée avec succès.")
        print(f"Le fichier de configuration a été généré ici : {agent.config_file_path}")
    else:
        print("\n[ÉCHEC] La mission de l'agent a échoué.")
        print(f"Statut final : {agent.mission_status}")

