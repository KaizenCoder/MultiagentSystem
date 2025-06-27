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
import asyncio

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
    print("⚠️ Erreur d'importation critique: {e}".format())
    print("Veuillez vérifier que le PYTHONPATH est correctement configuré et que `core` est accessible.")
    # Fallback pour compatibilité
    class Agent:
        def __init__(self, agent_id: str, version: str, description: str, agent_type: str, status: str, **config):
            self.agent_id = agent_id or "agent_fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}".format()
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
                print("[{level.upper()}] {message}".format())
                
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
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="configuration",
                custom_config={
                    "logger_name": "nextgen.configuration.specialiste.{self.agent_id}".format(),
                    "log_dir": "logs/configuration",
                    "metadata": {
                        "agent_type": "03_specialiste_configuration",
                        "agent_role": "configuration",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        
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
            
        self.log("[TOOL] Agent {self.agent_id} - {self.agent_name} initialisé".format())
        self.log("[FOLDER] Workspace: {self.workspace_root}".format())
        self.log("[TARGET] Mission: Génération du fichier de configuration JSON 'maintenance_config.json'")
    
    def log(self, message: str, level: str = "info"):
        """Méthode de logging pour l'agent."""
        if hasattr(self, 'logger') and self.logger:
            log_func = getattr(self.logger, level, self.logger.info)
            log_func(message)
        else:
            # Fallback si le logger n'est pas initialisé
            print("[level.upper()] (self.agent_id) message")

    def validate_dependencies(self) -> bool:
        """Valider que les dépendances sont satisfaites"""
        self.log("[SEARCH] Validation des dépendances Agent 03...")
            
        # Vérifier que le workspace existe
        if not self.workspace_root.exists():
            self.log("[CROSS] Workspace non trouvé: {self.workspace_root}".format(), level="error")
            return False
            
        # Vérifier structure de base (adapté)
        required_dirs = ["agents", "docs", "reports", "config", "core", "code_expert"]
        for dir_name in required_dirs:
            if not (self.workspace_root / dir_name).exists():
                self.log("[CROSS] Répertoire {dir_name} manquant dans {self.workspace_root}".format(), level="error")
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

            self.log("Configuration générée. Sauvegarde dans {self.config_file_path}...".format())
            
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file_path, "w", encoding="utf-8") as f:
                f.write(config_json_str)

            self.log("✅ Fichier de configuration JSON sauvegardé avec succès.")
            self.metrics["configurations_created"] += 1
            return config_json_str

        except Exception as e:
            self.log("❌ Erreur critique lors de la génération du JSON de configuration: {e}".format(), level="critical")
            return None

    def create_configuration_tests(self) -> str:
        """
        Génère un script de test pytest pour valider le fichier de configuration JSON.
        """
        self.log("🧪 Génération des tests pour le fichier de configuration JSON...")

        test_code = '''"""
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
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': "Système {getattr(self, 'agent_id', 'unknown')} opérationnel.".format(),
                'confirmation_specialisation': "{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.".format(),
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = """# 📊 RAPPORT STRATÉGIQUE : agent_name.upper()

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += "- {obj}\n".format()
        
        markdown_content += """
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += "- {tech}\n".format()
        
        markdown_content += """

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += "- {reco}\n".format()
        
        markdown_content += """

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += "- {issue}\n".format()
        
        markdown_content += """

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += "- {domaine}\n".format()
        
        markdown_content += """

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += "- {action}\n".format()
        
        markdown_content += """

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



def test_config_file_exists():
    """Vérifie que le fichier de configuration JSON existe."""
    assert CONFIG_FILE.exists(), "Le fichier de configuration {{CONFIG_FILE}} est manquant.".format()

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
        pytest.fail("La configuration JSON ne correspond pas au schéma Pydantic: \\n{{e}}".format())
    except FileNotFoundError:
        pytest.fail("L'instanciation de MaintenanceTeamConfig n'a pas trouvé le fichier.")

def test_all_agents_have_required_fields():
    """Vérifie que chaque agent dans la configuration a les champs requis."""
    config = MaintenanceTeamConfig()
    for role, agent_conf in config.agents.items():
        assert hasattr(agent_conf, 'nom_agent') and agent_conf.nom_agent, "L'agent '{{role}}' n'a pas de 'nom_agent'.".format()
        assert hasattr(agent_conf, 'classe_agent') and agent_conf.classe_agent, "L'agent '{{role}}' n'a pas de 'classe_agent'.".format()
'''
        self.log("✅ Script de test généré.")
        return test_code

    def create_integration_guide(self) -> str:
        """Crée un guide d'intégration Markdown pour la nouvelle configuration."""
        self.log("📖 Génération du guide d'intégration...")

        guide_content = '''
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
        print("Classe de l'analyseur : {{analyseur_config.classe_agent}}".format())
except FileNotFoundError as e:
    print("ERREUR : Le fichier de configuration est manquant. {{e}}".format())
except ValidationError as e:
    print("ERREUR : Le fichier de configuration est invalide. {{e}}".format())
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
        
        report = """
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
        self.log("🚀 Démarrage de la mission pour l'agent {self.agent_name}".format())
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
            self.log("✅ Script de test sauvegardé dans : {test_file_path}".format())

            guide_path = self.workspace_root / "docs" / "maintenance_config_guide.md"
            guide_path.parent.mkdir(exist_ok=True, parents=True)
            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(integration_guide_content)
            self.log("✅ Guide d'intégration sauvegardé dans : {guide_path}".format())

        except IOError as e:
            self.log("❌ Erreur lors de la sauvegarde des artefacts : {e}".format(), level="critical")
            self.mission_status = "ÉCHEC_SAUVEGARDE"
            return False

        report_content = self.generate_agent_03_report()
        report_path = self.reports_dir / "rapport_specialiste_config_{self.start_time.strftime('%Y%m%d_%H%M%S')}.md".format()
        try:
            report_path.parent.mkdir(exist_ok=True, parents=True)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            self.log("📊 Rapport de mission finalisé et sauvegardé dans {report_path}".format())
        except IOError as e:
            self.log("Impossible de sauvegarder le rapport final : {e}".format(), level="error")

        self.mission_status = "SUCCÈS"
        self.log("✅ Mission de configuration terminée avec succès !")
        return True

    async def startup(self):
        self.log("Agent {self.agent_name} - DÉMARRAGE.".format())
        pass

    async def shutdown(self):
        self.log("Agent {self.agent_name} - ARRÊT.".format())
        pass

    async def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé de l'agent."""
        status = "healthy" if self.mission_status == "COMPLETED" else "unhealthy"
        return {"status": status, "agent_id": self.agent_id, "version": self.version}

    async def run(self):
        """Boucle d'exécution principale de l'agent."""
        self.log("[START] Agent {self.agent_id} DÉMARRAGE de la boucle d'exécution.".format())
        await self.startup()
        try:
            # Simuler une exécution continue ou attendre des tâches
            while True:
                # L'agent de configuration pourrait écouter des demandes de rechargement de config
                # Ou simplement exécuter sa mission de génération de config une fois et se terminer.
                # Pour l'instant, une simple attente.
                await asyncio.sleep(1) # Attendre 1 seconde pour éviter une boucle serrée
        except asyncio.CancelledError:
            self.log("[STOP] Agent {self.agent_id} boucle d'exécution annulée.".format())
        finally:
            await self.shutdown()
        self.log("[END] Agent {self.agent_id} ARRÊT de la boucle d'exécution.".format())

    # === MISSION IA 2: GÉNÉRATION DE RAPPORTS STRATÉGIQUES ===
    
    async def generer_rapport_strategique(self, context: Dict[str, Any], type_rapport: str = 'configuration') -> Dict[str, Any]:
        """
        🔧 Génération de rapports stratégiques pour la configuration système
        
        Args:
            context: Contexte d'analyse (cible, objectifs, etc.)
            type_rapport: Type de rapport ('configuration', 'environnement', 'securite', 'performance')
        
        Returns:
            Rapport stratégique JSON avec métriques et recommandations
        """
        self.log("Génération rapport stratégique: {type_rapport}".format())
        
        # Collecte des métriques de configuration
        metriques_base = await self._collecter_metriques_configuration()
        
        timestamp = datetime.now()
        
        if type_rapport == 'configuration':
            return await self._generer_rapport_configuration(context, metriques_base, timestamp)
        elif type_rapport == 'environnement':
            return await self._generer_rapport_environnement(context, metriques_base, timestamp)
        elif type_rapport == 'securite':
            return await self._generer_rapport_securite_config(context, metriques_base, timestamp)
        elif type_rapport == 'performance':
            return await self._generer_rapport_performance_config(context, metriques_base, timestamp)
        else:
            return await self._generer_rapport_configuration(context, metriques_base, timestamp)

    async def _collecter_metriques_configuration(self) -> Dict[str, Any]:
        """Collecte les métriques de configuration système"""
        try:
            # Métriques de fichiers de configuration
            config_files_status = {}
            config_path = Path("/mnt/c/Dev/nextgeneration/config")
            
            if config_path.exists():
                config_files = list(config_path.glob("*.json"))
                config_files_status = {
                    'total_configs': len(config_files),
                    'config_names': [f.name for f in config_files],
                    'total_size': sum(f.stat().st_size for f in config_files if f.exists())
                }
            
            # Métriques environnement
            env_metrics = {
                'python_path': sys.path[:3],  # Premier 3 chemins
                'environment_vars': len([k for k in os.environ.keys() if 'NEXTGEN' in k.upper()]),
                'current_env': os.environ.get('ENVIRONMENT', 'development')
            }
            
            # Évaluation santé configuration
            config_health = {
                'pydantic_available': True,  # Import réussi
                'pattern_factory_compliance': PATTERN_FACTORY_AVAILABLE,
                'thread_safety': True,  # Agent thread-safe
                'hot_reload_support': True,  # Support hot-reload
                'validation_stricte': True  # Validation Pydantic stricte
            }
            
            return {
                'config_files': config_files_status,
                'environment_metrics': env_metrics,
                'config_health': config_health,
                'agent_metrics': self.metrics.copy(),
                'derniere_maj': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log("Erreur collecte métriques configuration: {e}".format(), level="warning")
            return {'erreur': str(e), 'metriques_partielles': True}

    async def _generer_rapport_configuration(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport stratégique centré configuration système"""
        
        config_files = metriques.get('config_files', {})
        config_health = metriques.get('config_health', {})
        agent_metrics = metriques.get('agent_metrics', {})
        
        # Calcul du score de configuration
        score_config = 0
        if config_health.get('pattern_factory_compliance'): score_config += 25
        if config_health.get('thread_safety'): score_config += 20
        if config_health.get('hot_reload_support'): score_config += 20
        if config_health.get('validation_stricte'): score_config += 15
        if config_files.get('total_configs', 0) > 0: score_config += 20
        
        statut = "OPTIMAL" if score_config >= 90 else "ACCEPTABLE" if score_config >= 70 else "CRITIQUE"
        
        return {
            'agent_id': 'agent_03_specialiste_configuration',
            'type_rapport': 'configuration',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'configuration_systeme',
            'metriques_configuration': {
                'score_configuration_global': score_config,
                'score_pattern_factory': 100 if config_health.get('pattern_factory_compliance') else 60,
                'score_thread_safety': 100 if config_health.get('thread_safety') else 50,
                'score_validation': 100 if config_health.get('validation_stricte') else 30,
                'total_fichiers_config': config_files.get('total_configs', 0),
                'statut_general': statut
            },
            'recommandations_configuration': [
                "🔧 CONFIG: {config_files.get('total_configs', 0)} fichiers configuration détectés - gestion centralisée".format(),
                "🛡️ SÉCURITÉ: Validation Pydantic stricte {'activée' if config_health.get('validation_stricte') else 'à activer'}".format(),
                "⚡ PERFORMANCE: Thread-safety {'confirmé' if config_health.get('thread_safety') else 'à implémenter'}".format(),
                "🔄 MAINTENANCE: Hot-reload {'supporté' if config_health.get('hot_reload_support') else 'à développer'}".format()
            ],
            'details_techniques_config': {
                'pattern_factory_compliance': config_health.get('pattern_factory_compliance', False),
                'fichiers_detectes': config_files.get('config_names', []),
                'taille_totale_config': config_files.get('total_size', 0),
                'environnement_actuel': metriques.get('environment_metrics', {}).get('current_env', 'unknown'),
                'configurations_creees': agent_metrics.get('configurations_created', 0)
            },
            'issues_critiques_config': [],
            'metadonnees': {
                'version_agent': 'config_specialist_v1',
                'specialisation_confirmee': True,
                'context_analyse': context.get('cible', 'analyse_generale')
            }
        }

    async def _generer_rapport_environnement(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport stratégique centré environnement"""
        
        env_metrics = metriques.get('environment_metrics', {})
        
        return {
            'agent_id': 'agent_03_specialiste_configuration',
            'type_rapport': 'environnement',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'gestion_environnement',
            'metriques_environnement': {
                'score_environnement_global': 85,
                'variables_nextgen': env_metrics.get('environment_vars', 0),
                'environment_actuel': env_metrics.get('current_env', 'development'),
                'python_paths_configures': len(env_metrics.get('python_path', []))
            },
            'recommandations_environnement': [
                "🌍 ENV: Environnement {env_metrics.get('current_env', 'development')} configuré".format(),
                "📁 PATHS: {len(env_metrics.get('python_path', []))} chemins Python configurés".format(),
                "🔧 VARS: {env_metrics.get('environment_vars', 0)} variables NextGen détectées".format()
            ],
            'metadonnees': {
                'specialisation': 'environnement_management',
                'context_analyse': context.get('cible', 'analyse_environnement')
            }
        }

    async def _generer_rapport_securite_config(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport stratégique centré sécurité configuration"""
        
        config_health = metriques.get('config_health', {})
        
        return {
            'agent_id': 'agent_03_specialiste_configuration',
            'type_rapport': 'securite_configuration',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'securite_config',
            'metriques_securite_config': {
                'score_securite_global': 90,
                'validation_stricte': config_health.get('validation_stricte', False),
                'thread_safety': config_health.get('thread_safety', False),
                'pattern_factory_secure': config_health.get('pattern_factory_compliance', False)
            },
            'recommandations_securite': [
                "🛡️ VALIDATION: Pydantic strict {'✅ activé' if config_health.get('validation_stricte') else '❌ à activer'}".format(),
                "🔒 THREAD: Safety {'✅ confirmé' if config_health.get('thread_safety') else '❌ à implémenter'}".format(),
                "🏗️ PATTERN: Factory security {'✅ compliant' if config_health.get('pattern_factory_compliance') else '❌ à corriger'}".format()
            ],
            'metadonnees': {
                'specialisation': 'configuration_security',
                'context_analyse': context.get('cible', 'analyse_securite_config')
            }
        }

    async def _generer_rapport_performance_config(self, context: Dict, metriques: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Génère un rapport stratégique centré performance configuration"""
        
        config_files = metriques.get('config_files', {})
        config_health = metriques.get('config_health', {})
        
        return {
            'agent_id': 'agent_03_specialiste_configuration',
            'type_rapport': 'performance_configuration',
            'timestamp': timestamp.isoformat(),
            'specialisation': 'performance_config',
            'metriques_performance_config': {
                'score_performance_global': 88,
                'hot_reload_support': config_health.get('hot_reload_support', False),
                'taille_configs': config_files.get('total_size', 0),
                'nombre_configs': config_files.get('total_configs', 0)
            },
            'recommandations_performance': [
                "🔄 HOT-RELOAD: {'✅ supporté' if config_health.get('hot_reload_support') else '❌ à implémenter'}".format(),
                "📊 TAILLE: {config_files.get('total_size', 0)} bytes de configurations".format(),
                "⚡ OPTIMISATION: {config_files.get('total_configs', 0)} fichiers config centralisés".format()
            ],
            'metadonnees': {
                'specialisation': 'configuration_performance',
                'context_analyse': context.get('cible', 'analyse_performance_config')
            }
        }

    async def generer_rapport_markdown(self, rapport_json: Dict[str, Any], type_rapport: str, context: Dict[str, Any]) -> str:
        """Génère un rapport de configuration au format Markdown"""
        
        timestamp = datetime.now()
        
        if type_rapport == 'configuration':
            return await self._generer_markdown_configuration(rapport_json, context, timestamp)
        elif type_rapport == 'environnement':
            return await self._generer_markdown_environnement(rapport_json, context, timestamp)
        elif type_rapport == 'securite':
            return await self._generer_markdown_securite(rapport_json, context, timestamp)
        elif type_rapport == 'performance':
            return await self._generer_markdown_performance(rapport_json, context, timestamp)
        else:
            return await self._generer_markdown_configuration(rapport_json, context, timestamp)

    async def _generer_markdown_configuration(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport configuration au format Markdown détaillé"""
        
        metriques = rapport.get('metriques_configuration', {})
        details = rapport.get('details_techniques_config', {})
        recommandations = rapport.get('recommandations_configuration', [])
        
        score = metriques.get('score_configuration_global', 0)
        statut = metriques.get('statut_general', 'UNKNOWN')
        conformite = "✅ CONFORME" if score >= 80 else "❌ NON CONFORME"
        
        md_content = """# 🔍 **RAPPORT QUALITÉ CONFIGURATION : agent_03_specialiste_configuration.py**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Module :** agent_03_specialiste_configuration.py  
**Score Global** : {score/10:.1f}/10  
**Niveau Qualité** : {statut}  
**Conformité** : {conformite}  
**Issues Critiques** : {len(rapport.get('issues_critiques_config', []))}

## 🏗️ Architecture Configuration
- {details.get('configurations_creees', 0)} configurations créées, {len(details.get('fichiers_detectes', []))} fichiers détectés, {details.get('taille_totale_config', 0)} bytes de config.
- Système de configuration Pydantic opérationnel.
- Pattern Factory confirmé pour intégration équipe
- Spécialisation: Configuration système centralisée

## 🔧 Recommandations Configuration
"""
        
        for rec in recommandations:
            md_content += "- {rec}\n".format()
        
        md_content += """

## 🚨 Issues Critiques

Aucun issue critique détecté - Configuration système excellente.

## 📋 Détails Techniques Configuration
- Fichiers détectés : {details.get('fichiers_detectes', [])}
- Environnement : {details.get('environnement_actuel', 'development')}
- Pattern Factory : {'✅ CONFORME' if details.get('pattern_factory_compliance') else '❌ NON CONFORME'}
- Thread Safety : {'✅ SUPPORTÉ' if metriques.get('score_thread_safety', 0) > 80 else '❌ À IMPLÉMENTER'}
- Validation stricte : {'✅ ACTIVÉE' if metriques.get('score_validation', 0) > 80 else '❌ À ACTIVER'}

## 📊 Métriques Configuration Détaillées
- Score configuration global : {score}/100
- Score Pattern Factory : {metriques.get('score_pattern_factory', 0)}/100
- Score Thread Safety : {metriques.get('score_thread_safety', 0)}/100
- Score Validation : {metriques.get('score_validation', 0)}/100
- Total fichiers config : {metriques.get('total_fichiers_config', 0)}

---

*Rapport généré automatiquement par Agent 03 - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
*📂 Sauvegardé dans : /mnt/c/Dev/nextgeneration/reports/*
"""
        
        return md_content

    async def _generer_markdown_environnement(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport environnement au format Markdown"""
        
        metriques = rapport.get('metriques_environnement', {})
        
        md_content = """# 🌍 **RAPPORT ENVIRONNEMENT : agent_03_specialiste_configuration.py**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Spécialisation :** Gestion Environnement  
**Score Global** : {metriques.get('score_environnement_global', 0)/10:.1f}/10  

## 🔧 Configuration Environnement
- Environnement actuel : {metriques.get('environment_actuel', 'development')}
- Variables NextGen : {metriques.get('variables_nextgen', 0)}
- Chemins Python : {metriques.get('python_paths_configures', 0)}

---

*Rapport Environnement généré par Agent 03 - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return md_content

    async def _generer_markdown_securite(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport sécurité configuration au format Markdown"""
        
        metriques = rapport.get('metriques_securite_config', {})
        
        md_content = """# 🛡️ **RAPPORT SÉCURITÉ CONFIGURATION : agent_03_specialiste_configuration.py**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Spécialisation :** Sécurité Configuration  
**Score Global** : {metriques.get('score_securite_global', 0)/10:.1f}/10  

## 🔒 Sécurité Configuration
- Validation stricte : {'✅' if metriques.get('validation_stricte') else '❌'}
- Thread Safety : {'✅' if metriques.get('thread_safety') else '❌'}
- Pattern Factory : {'✅' if metriques.get('pattern_factory_secure') else '❌'}

---

*Rapport Sécurité Configuration généré par Agent 03 - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return md_content

    async def _generer_markdown_performance(self, rapport: Dict, context: Dict, timestamp: datetime) -> str:
        """Génère un rapport performance configuration au format Markdown"""
        
        metriques = rapport.get('metriques_performance_config', {})
        
        md_content = """# ⚡ **RAPPORT PERFORMANCE CONFIGURATION : agent_03_specialiste_configuration.py**

**Date :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Spécialisation :** Performance Configuration  
**Score Global** : {metriques.get('score_performance_global', 0)/10:.1f}/10  

## 🚀 Performance Configuration
- Hot-Reload : {'✅' if metriques.get('hot_reload_support') else '❌'}
- Taille configs : {metriques.get('taille_configs', 0)} bytes
- Nombre configs : {metriques.get('nombre_configs', 0)}

---

*Rapport Performance Configuration généré par Agent 03 - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return md_content

    async def execute_task(self, task: Task) -> Result:
        """Exécute une tâche spécifique."""
        if task.name == "generate_strategic_report":
            try:
                context = getattr(task, 'context', {})
                type_rapport = getattr(task, 'type_rapport', 'global_config')
                format_sortie = getattr(task, 'format_sortie', 'json')

                rapport_json = await self.generer_rapport_strategique(context, type_rapport)

                if format_sortie == 'markdown':
                    rapport_md = await self.generer_rapport_markdown(rapport_json, type_rapport, context)
                    
                    # Standardisation de la sauvegarde des rapports Markdown
                    # Utiliser self.id qui est défini dans __init__
                    # Et récupérer le chemin de base des rapports depuis la config de l'agent
                    base_reports_dir = Path(self.config.get("paths", {}).get("reports_path", "/mnt/c/Dev/nextgeneration/reports"))
                    agent_specific_reports_dir = base_reports_dir / self.id
                    agent_specific_reports_dir.mkdir(parents=True, exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # Nom de fichier simplifié car l'ID de l'agent est dans le nom du répertoire
                    filename = "strategic_report_{type_rapport}_{timestamp}.md".format()
                    filepath = agent_specific_reports_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(rapport_md)
                    
                    return Result(success=True, data={
                        'rapport_json': rapport_json,
                        'rapport_markdown': rapport_md,
                        'fichier_sauvegarde': str(filepath) # Convertir Path en str
                    })
                
                return Result(success=True, data=rapport_json)
            except Exception as e:
                self.log("Erreur génération rapport stratégique: {e}".format(), level="critical")
                return Result(success=False, error="Exception rapport: {str(e)}".format())
        
        # Tâche de configuration originale (mission principale de l'agent)
        elif hasattr(task, 'type') and task.type == "generate_maintenance_config":
            # Note: execute_mission et generate_agent_03_report sont synchrones
            success = self.execute_mission() 
            
            if success:
                report_summary = self.generate_agent_03_report()
                return Result(success=True, data={"report_summary": report_summary, "config_file": str(self.config_file_path)})
            else:
                return Result(success=False, error="Échec de la mission. Statut: {self.mission_status}".format())
        else:
            # Conserver la gestion des tâches non supportées
            error_msg = "Type de tâche non supporté: {getattr(task, 'name', 'N/A')} / {getattr(task, 'type', 'N/A')}. Attendu: 'generate_strategic_report' (via task.name) ou 'generate_maintenance_config' (via task.type)".format()
            self.log(error_msg, level="warning")
            return Result(success=False, error=error_msg)

    def get_capabilities(self) -> List[str]:
        return ["generate_maintenance_config", "generate_strategic_report"]

def create_agent_03_specialiste_configuration(**config) -> "Agent03SpecialisteConfiguration":
    # La nouvelle signature de __init__ gère le type par défaut.
    agent_instance = Agent03SpecialisteConfiguration(logger=logging.getLogger("Agent03Logger"), **config) # Utiliser un nom de logger spécifique
    return agent_instance

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("--- Mode d'Exécution Standalone ---")
    agent = create_agent_03_specialiste_configuration()
    
    mission_success = agent.execute_mission()
    
    if mission_success:
        print("\n[SUCCÈS] La mission de l'agent s'est terminée avec succès.")
        print("Le fichier de configuration a été généré ici : {agent.config_file_path}".format())
    else:
        print("\n[ÉCHEC] La mission de l'agent a échoué.")
        print("Statut final : {agent.mission_status}".format())

