#!/usr/bin/env python3
"""
AGENT 109 - PATTERN FACTORY VERSION (SPECIALIZED)
Agent Factory Pattern - Sprint 4.5

Mission:
- Enforce the Agent Factory design pattern.
- Validate agent compliance with the pattern.
- Provide templates and tools for creating new agents.
- Manage versioning and compatibility of agents within the factory.

This is a meta-agent, responsible for the integrity of the agent ecosystem.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import asyncio
from datetime import datetime
import signal
from pathlib import Path
import json

# --- Configuration Section ---
try:
    ROOT_DIR = Path(__file__).resolve().parents[1]
except NameError:
    ROOT_DIR = Path.cwd()

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Directories
LOGS_DIR = ROOT_DIR / "logs" / "agents"
REPORTS_DIR = ROOT_DIR / "reports" / "factory_pattern"
TEMPLATES_DIR = ROOT_DIR / "templates" / "agents"

# Create directories if they don't exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# --- Agent Class ---
class PatternFactoryAgent:
    """
    A specialized agent to enforce and manage the Agent Factory Pattern.
    """
    def __init__(self, agent_id="pattern_factory_109"):
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="general",
                custom_config={
                    "logger_name": f"nextgen.general.109_pattern_factory_version.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/general",
                    "metadata": {
                        "agent_type": "109_pattern_factory_version",
                        "agent_role": "general",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

        self.agent_id = agent_id
        self.agent_name = "Pattern Factory Version Manager"
        self.version = "2.0.0"
        self.status = "INITIALIZING"
        self.logger = self._setup_logging()
        self.loop = asyncio.get_event_loop()
        self.shutdown_event = asyncio.Event()

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info(f"🚀 {self.agent_name} ({self.agent_id}) initialized.")

    def _setup_logging(self):
        """Sets up a rotating logger for the agent."""
        logger = logging.getLogger(self.agent_id)
        logger.setLevel(logging.INFO)
        log_file = LOGS_DIR / f"{self.agent_id}.log"
        
        if not logger.handlers:
            handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger

    def _signal_handler(self, signum, frame):
        """Handles shutdown signals gracefully."""
        self.logger.warning(f"Signal {signum} received. Initiating shutdown...")
        self.shutdown_event.set()

    async def validate_agent_compliance(self, file_path: str):
        """
        Validates if an agent script complies with the basic factory pattern.
        This is a simplified check.
        """
        self.logger.info(f"Validating compliance for: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            findings = {
                "file_path": file_path,
                "compliant": True,
                "issues": []
            }
            
            if "class" not in content:
                findings["compliant"] = False
                findings["issues"].append("No class definition found.")
            if "def __init__" not in content:
                findings["compliant"] = False
                findings["issues"].append("No __init__ method found in class.")
            if "async def run" not in content and "def run" not in content:
                findings["compliant"] = False
                findings["issues"].append("No run method found for agent execution loop.")

            if findings["compliant"]:
                self.logger.info(f"✅ Agent {file_path} is compliant with basic standards.")
            else:
                self.logger.warning(f"❌ Agent {file_path} has compliance issues.")
                
            return findings

        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return {"file_path": file_path, "compliant": False, "issues": ["File not found."]}
        except Exception as e:
            self.logger.error(f"An error occurred during validation: {e}")
            return {"file_path": file_path, "compliant": False, "issues": [str(e)]}

    async def generate_agent_template(self, new_agent_name: str, is_async: bool = True):
        """
        Generates a basic agent template file.
        """
        self.logger.info(f"Generating template for new agent: {new_agent_name}")
        
        template_name = "async_agent_template.py.txt" if is_async else "sync_agent_template.py.txt"
        template_path = TEMPLATES_DIR / template_name
        
        if not template_path.exists():
            self.logger.error(f"Template file not found: {template_path}")
            return None
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        agent_code = template_content.replace("{{AGENT_NAME}}", new_agent_name)
        
        new_agent_filename = f"agent_{new_agent_name.lower().replace(' ', '_')}.py"
        new_agent_path = ROOT_DIR / "agents" / new_agent_filename
        
        with open(new_agent_path, 'w', encoding='utf-8') as f:
            f.write(agent_code)
            
        self.logger.info(f"✅ Template generated at: {new_agent_path}")
        return str(new_agent_path)

    async def run(self):
        """The main execution loop for the agent."""
        self.status = "RUNNING"
        self.logger.info(f"Agent {self.agent_name} is now running.")
        
        try:
            while not self.shutdown_event.is_set():
                self.logger.info("Heartbeat: Pattern Factory is active. Monitoring agent standards...")
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            self.logger.info("Main task was cancelled.")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Performs a graceful shutdown of the agent."""
        if self.status == "SHUTTING_DOWN":
            return
            
        self.status = "SHUTTING_DOWN"
        self.logger.info("Agent is shutting down.")
        self.logger.info("Goodbye!")
        self.status = "SHUTDOWN"

# --- Main Execution ---
async def main():
    """Main function to run the agent."""
    agent = PatternFactoryAgent()
    try:
        await agent.run()
    except Exception as e:
        agent.logger.critical(f"A critical error occurred: {e}", exc_info=True)
        await agent.shutdown()
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
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
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
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

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
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

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
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down gracefully.")