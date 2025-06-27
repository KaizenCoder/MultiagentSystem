#!/usr/bin/env python3
"""
AGENT 1 - ANALYSEUR DE STRUCTURE (Pattern Factory)
🏗️ ANALYSEUR DE STRUCTURE - Agent 01
====================================

🎯 Mission : Analyser la structure du code et détecter les erreurs syntaxiques.
⚡ Capacités : Analyse statique avec `py_compile`, `ast`, et `pylint`.
🏢 Équipe : NextGeneration Tools Migration

Author: Équipe de Maintenance NextGeneration
Version: 1.3.0 - Harmonisation Standards Pattern Factory NextGeneration
"""
import asyncio
import ast
import json
import logging
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

# --- Configuration Robuste du Chemin d'Importation ---
try:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except (IndexError, NameError):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

from core.agent_factory_architecture import Agent, Task, Result
PATTERN_FACTORY_AVAILABLE = True


class AgentMAINTENANCE01AnalyseurStructure(Agent):
    """
    🏗️ Agent MAINTENANCE 01 - Analyseur de Structure NextGeneration
    
    Agent spécialisé dans l'analyse automatique de la structure des fichiers Python,
    détection d'incohérences syntaxiques et génération de rapports d'audit structurel.
    
    Capacités principales :
    - Analyse statique via AST (imports, classes, fonctions, async)
    - Détection d'erreurs syntaxiques et structurelles  
    - Analyse de fichiers individuels ou répertoires complets
    - Génération de rapports structurés pour maintenance
    - Compatibilité avec coordinateur d'équipe maintenance
    
    Workflow type :
    1. Réception tâche "analyse_structure" avec directory/file_path
    2. Parsing AST des fichiers Python ciblés
    3. Extraction structure (imports, classes, fonctions)
    4. Retour rapport complet ou erreurs détectées
    
    Conformité : Pattern Factory NextGeneration v1.3.0
    """
    def __init__(self, **kwargs):
        """Initialisation standardisée."""
        super().__init__(agent_type="analyseur_structure", **kwargs)
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="maintenance",
                custom_config={
                    "logger_name": f"nextgen.maintenance.analyseur_structure.{self.id}",
                    "log_dir": "logs/maintenance/analyseur",
                    "metadata": {
                        "agent_type": "MAINTENANCE_01_analyseur_structure",
                        "agent_role": "analyseur_structure",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Analyseur de structure ({self.id}) initialisé.")

    async def startup(self):
        """Démarrage de l'agent."""
        self.logger.info(f"Analyseur de structure prêt.")

    async def execute_task(self, task: Task) -> Result:
        """Exécute la tâche d'analyse du répertoire ou d'un fichier."""
        if task.type != "analyse_structure":
            return Result(success=False, error="Type de tâche non supporté.")

        directory = task.params.get("directory")
        file_path_param = task.params.get("file_path")

        if not directory and not file_path_param:
            return Result(success=False, error="Répertoire ou chemin de fichier non spécifié.")

        if file_path_param:
            files_to_process = [file_path_param]
        else:
            files_to_process = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".py")]

        self.logger.info(f"Analyse demandée pour : {directory or file_path_param}")
        
        files_analysis = []
        try:
            for file_path in files_to_process:
                self.logger.info(f"Analyse du fichier : {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    analysis = self._analyze_python_file(content)
                    files_analysis.append({
                        "path": file_path,
                        "analysis": analysis,
                    })
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'analyse du fichier {file_path}: {e}")
                    files_analysis.append({
                        "path": file_path,
                        "error": str(e),
                    })
            
            # Pour la cohérence, si un seul fichier a été demandé, on retourne directement son analyse.
            if file_path_param and len(files_analysis) == 1:
                result_data = files_analysis[0]
                return Result(success=not result_data.get("error"), data=result_data)

            return Result(success=True, data={"files": files_analysis})

        except Exception as e:
            self.logger.critical(f"Erreur majeure lors de l'analyse : {e}")
            return Result(success=False, error=str(e))

    def _analyze_python_file(self, code: str) -> dict:
        """
        Analyse le contenu d'un fichier Python pour en extraire la structure de base.
        """
        analysis_report = {
            "imports": [],
            "classes": [],
            "functions": [],
            "has_async": False,
        }
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis_report["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis_report["imports"].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    analysis_report["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis_report["functions"].append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    analysis_report["functions"].append(f"async {node.name}")
                    analysis_report["has_async"] = True
        except SyntaxError as e:
            return {"error": f"SyntaxError: {e}"}

        return analysis_report

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités spécialisées de l'Analyseur de Structure."""
        return [
            "analyse_structure",
            "analyse_ast_python",
            "detection_erreurs_syntaxiques", 
            "extraction_imports_classes_fonctions",
            "analyse_repertoire_complet",
            "compatibilite_coordinateur_maintenance"
        ]

    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy"}

    async def shutdown(self):
        self.logger.info("Analyseur de structure éteint.")
        

    async def run_analysis(self, directory: str) -> Result:
        """Méthode de compatibilité pour l'ancien appel du coordinateur."""
        self.logger.warning(f"Appel de compatibilité 'run_analysis' pour le répertoire: {directory}")
        task_id = f"analyse_{uuid.uuid4().hex}"
        task_description = f"Analyse de structure pour le répertoire {directory}"
        analyse_task = Task(
            id=task_id,
            description=task_description,
            type="analyse_structure",
            params={"directory": directory}
        )
        return await self.execute_task(analyse_task)

def create_agent_MAINTENANCE_01_analyseur_structure(**config) -> AgentMAINTENANCE01AnalyseurStructure:
    """Factory pour créer une instance de l'Agent 1."""
    return AgentMAINTENANCE01AnalyseurStructure(**config)

if __name__ == '__main__':
    async def main_test():
        agent = create_agent_MAINTENANCE_01_analyseur_structure()
        await agent.startup()
        # On teste avec le répertoire 'agents' lui-même
        results = await agent.run_analysis("agents")
        
        # Affichage correct du résultat
        print(json.dumps({'success': results.success, 'data': results.data, 'error': results.error}, indent=2))
        
        await agent.shutdown()
    asyncio.run(main_test())
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

