#!/usr/bin/env python3
"""
🤖 AGENT11AUDITEURQUALITE - PATTERN FACTORY NEXTGENERATION
========================================================

Mission: [Mission extraite de l'agent original]

Architecture Pattern Factory:
    pass  # TODO: Implémenter
- Hérite de Agent de base
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé

Transformé automatiquement par Agent 03 Adaptateur Code Upgraded
Date: 2025-06-21 02:36:28
"""

import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import re
import ast

# Import Pattern Factory (OBLIGATOIRE selon guide)
# Assurez-vous que le chemin vers 'core' est dans le PYTHONPATH
try:
    from core.agent_factory_architecture import Agent, Task, Result
    from core import logging_manager
    PATTERN_FACTORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Pattern Factory non disponible: {e}. Utilisation des classes de fallback.")
    PATTERN_FACTORY_AVAILABLE = False
    # Fallback classes si l'architecture centrale n'est pas disponible
    class Agent:
        pass  # TODO: Implémenter
        def __init__(self, agent_type: str, **config):
            pass  # TODO: Implémenter
        pass  # TODO: Implémenter
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="audit",
                custom_config={
                    "logger_name": f"nextgen.audit.111_auditeur_qualite.{self.agent_id if hasattr(self, 'agent_id') else self.id if hasattr(self, 'id') else 'unknown'}",
                    "log_dir": "logs/audit",
                    "metadata": {
                        "agent_type": "111_auditeur_qualite",
                        "agent_role": "audit",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)

            self.agent_id = f"fallback_{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.agent_type = agent_type
            self.config = config
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(self.agent_id)

        async def startup(self):
            self.logger.info(f"Agent {self.agent_id} démarré (fallback).")

        async def shutdown(self):
            self.logger.info(f"Agent {self.agent_id} arrêté (fallback).")

        async def health_check(self):
            return {"status": "healthy_fallback"}

        def get_capabilities(self):
            return []

    class Task:
        pass  # TODO: Implémenter
        def __init__(self, task_id: str, description: str, **kwargs):
            self.task_id = task_id
            self.description = description
            self.data = kwargs

    class Result:
        pass  # TODO: Implémenter
        def __init__(self, success: bool, data: Any = None, error: str = None):
            self.success = success
            self.data = data
            self.error = error

# --- Helper Function pour une détection de docstring robuste ---
def _has_module_docstring_manual(tree: ast.Module) -> bool:
    """Vérifie manuellement la présence d'un docstring de module."""
    if not hasattr(tree, 'body') or not tree.body:
        return False
    
    first_node = tree.body[0]
    
    # Python < 3.8
    if sys.version_info < (3, 8) and isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
        return True
        
    # Python >= 3.8
    if sys.version_info >= (3, 8) and isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Constant) and isinstance(first_node.value.value, str):
        return True
        
    return False

class Agent111AuditeurQualite(Agent):
    """Agent111AuditeurQualite - Pattern Factory NextGeneration"""

    def __init__(self, **config):
        # Pré-initialisation pour satisfaire les dépendances de la classe de base `Agent`
        self.agent_id = config.get("agent_id", f"agent_111_auditeur_qualite_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.agent_type = "agent_111_auditeur_qualite"
        # Définir self.workspace_root tôt car il est utilisé pour le logger fallback
        self.workspace_root = Path(__file__).resolve().parents[1]
        
        self.logger = logging.getLogger(f"Agent111AuditeurQualite_{self.agent_id}")
        
        if not PATTERN_FACTORY_AVAILABLE:
            # Configuration du logger fichier en mode fallback
            log_file_dir = self.workspace_root / "logs" / "agents"
            log_file_dir.mkdir(parents=True, exist_ok=True)
            # Utiliser self.agent_id qui est déjà défini et unique en mode fallback
            log_file_path = log_file_dir / f"{self.agent_id}_execution.log"
            
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            # S'assurer que le logger n'a pas déjà ce handler (évite duplication si __init__ est appelé plusieurs fois)
            if not any(isinstance(h, logging.FileHandler) and h.baseFilename == str(log_file_path) for h in self.logger.handlers):
                self.logger.addHandler(file_handler)
            
            self.logger.setLevel(logging.INFO) # Assurer que le niveau du logger est INFO
            self.logger.propagate = False # Éviter que les messages remontent au root logger si basicConfig a été appelé
            self.logger.info(f"Logger fallback configuré. Journalisation fichier activée: {log_file_path}")

        # L'appel à super() se fait APRÈS la création des attributs dont il dépend.
        super().__init__(self.agent_type, **config)
        
        self.logger.info(f"🤖 Agent111AuditeurQualite initialisé - ID: {self.agent_id}")
        
        # Ce code était orphelin à la fin du fichier, je le déplace ici.
        self.code_expert_path = self.workspace_root / "code_expert"

        try:
            sys.path.insert(0, str(self.code_expert_path.parent))
            from code_expert.enhanced_agent_templates import AgentTemplate
            from code_expert.optimized_template_manager import OptimizedTemplateManager
            self.code_expert_available = True
            self.logger.info("[BOOT] Code expert Claude Phase 2 (templates, manager) chargé.")
        except ImportError as e:
            self.code_expert_available = False
            self.logger.warning(f"[BOOT] Code expert non disponible: {e}")

        self.quality_report = {}
        self.dod_status = {}


    async def startup(self):
        """Démarrage agent_111_auditeur_qualite"""
        self.logger.info(f"🚀 Agent111AuditeurQualite {self.agent_id} - DÉMARRAGE")
        await super().startup()
        self.logger.info("✅ Agent démarré avec succès")

    async def shutdown(self):
        """Arrêt agent_111_auditeur_qualite"""
        self.logger.info(f"🛑 Agent111AuditeurQualite {self.agent_id} - ARRÊT")
        await super().shutdown()

    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent_111_auditeur_qualite"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "ready": True,
            "pattern_factory_available": PATTERN_FACTORY_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }

    async def _audit_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """Effectue un audit de qualité robuste en utilisant l'AST."""
        self.logger.info(f"Début de l'audit de qualité AST pour {file_path}")
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.logger.error(f"Erreur de syntaxe dans {file_path}: {e}")
            return {
                "file_path": file_path,
                "quality_score": 0,
                "issues": [{"severity": "CRITICAL", "description": f"SyntaxError: {e}", "code": "SYNTAX_ERROR"}],
                "error": f"SyntaxError: {e}"
            }

        score = 100
        issues = []
        
        # 1. Vérification du docstring de module
        has_module_docstring = _has_module_docstring_manual(tree)
        if not has_module_docstring:
            score -= 20
            issues.append({
                "severity": "HIGH", 
                "description": "Docstring de module manquant.",
                "code": "MISSING_MODULE_DOCSTRING"
            })

        # 2. Vérification des docstrings de fonction et de classe
        total_funcs = 0
        total_classes = 0
        funcs_without_docstrings = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_classes +=1
                # On pourrait aussi vérifier les docstrings de classe ici
            
            if isinstance(node, ast.FunctionDef):
                total_funcs += 1
                if not ast.get_docstring(node):
                    self.logger.warning(f"Fonction '{node.name}' sans docstring.")
                    funcs_without_docstrings.append({"function": node.name})
        
        if funcs_without_docstrings:
            score -= len(funcs_without_docstrings) * 5
            issues.append({
                "severity": "MEDIUM", 
                "description": f"{len(funcs_without_docstrings)} fonction(s) sans docstring.",
                "code": "MISSING_FUNCTION_DOCSTRING",
                "details": funcs_without_docstrings
            })

        return {
            "file_path": file_path,
            "quality_score": max(0, score),
            "metrics": {
                "total_lines": len(code.splitlines()),
                "total_functions": total_funcs,
                "total_classes": total_classes,
                "module_docstring": "✅ Oui" if has_module_docstring else "❌ Non",
                "functions_no_docstring": len(funcs_without_docstrings),
            },
            "issues": issues
        }

    async def audit_code_quality(self, file_path: str) -> Dict[str, Any]:
        """
        Tâche publique pour auditer la qualité d'un fichier de code.
        """
        self.logger.info(f"Audit public de qualité demandé pour {file_path}")
        try:
            code = Path(file_path).read_text(encoding='utf-8')
            report = await self._audit_code(code, file_path)
            return report
        except FileNotFoundError:
            self.logger.error(f"Fichier non trouvé pour l'audit : {file_path}")
            return {"error": "File not found", "quality_score": 0}
        except Exception as e:
            self.logger.error(f"Erreur durant l'audit de {file_path}: {e}", exc_info=True)
            return {"error": str(e), "quality_score": 0}

    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches - Pattern Factory OBLIGATOIRE"""
        self.logger.info(f"🎯 Exécution tâche: {task.type if hasattr(task, 'type') else task.description}")
        try:
            task_type = task.type if hasattr(task, 'type') else task.description
            # raw_params sera task.params si l'attribut existe, sinon task.data
            raw_params = task.params if hasattr(task, 'params') else task.data

            if task_type == "audit_universal_quality":
                file_path = None
                if isinstance(raw_params, dict):
                    # Essayer d'accéder directement à file_path
                    file_path = raw_params.get('file_path')
                    # Si non trouvé, et si 'params' est une clé dans raw_params (cas du fallback Task)
                    if not file_path and 'params' in raw_params and isinstance(raw_params['params'], dict):
                        file_path = raw_params['params'].get('file_path')
                
                if not file_path:
                    self.logger.error(f"DEBUG execute_task - raw_params pour audit: {raw_params}")
                    return Result(success=False, error="file_path est requis pour audit_universal_quality (n'a pas pu être extrait des paramètres).")
                
                report_obj = await self.audit_code_quality(file_path=file_path)
                return Result(success=True, data={"audit_report": report_obj})

            elif task_type == "execute_mission":
                mission_data = raw_params.get('mission_data', None)
                results = await self.execute_mission(mission_data)
                return Result(success=True, data={"mission_results": results})

            elif task_type == "process_data":
                data_to_process = raw_params.get('data', None)
                if data_to_process is None:
                    return Result(success=False, error="Données requises pour 'process_data'")
                processed = await self.process_data(data_to_process)
                return Result(success=True, data=processed)

            else:
                return Result(success=False, error=f"Tâche non reconnue: {task_type}")

        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {task.type if hasattr(task, 'type') else task.task_id}: {e}", exc_info=True)
            return Result(success=False, error=str(e))

    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent"""
        return [
            "audit_universal_quality",
            "execute_mission",
            "process_data",
            "health_monitoring",
            "pattern_factory_compliance"
        ]

    # Méthodes métier (à adapter selon l'agent original)
    async def execute_mission(self, mission_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Exécution de la mission principale de l'agent"""
        self.logger.info("🎯 Début exécution mission")
        try:
            # TODO: Implémenter la logique métier spécifique de l'agent original
            result = {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "agent_id": self.agent_id
            }
            self.logger.info("✅ Mission terminée avec succès")
            return result
        except Exception as e:
            self.logger.error(f"❌ Erreur mission: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    async def process_data(self, data: Any) -> Dict[str, Any]:
        """Traitement des données spécifique à l'agent"""
        self.logger.info("🔄 Traitement des données")
        try:
            # TODO: Implémenter le traitement spécifique
            return {
                "processed": True,
                "data_type": type(data).__name__,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement données: {e}", exc_info=True)
            return {"processed": False, "error": str(e)}

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_111_auditeur_qualite(**config) -> 'Agent111AuditeurQualite':
    """Factory function pour créer un Agent111AuditeurQualite conforme Pattern Factory"""
    return Agent111AuditeurQualite(**config)
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



# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    print("🚀 Démarrage test agent_111_auditeur_qualite...")
    # Passer un agent_id fixe pour des noms de log prévisibles pendant le test
    agent = create_agent_111_auditeur_qualite(agent_id="test_agent_111")

    try:
        await agent.startup()
        health = await agent.health_check()
        print(f"🏥 Health Check: {health}")
        agent.logger.info(f"MAIN_TEST - Health Check: {health}")

        # Test d'une tâche
        print("\n🔬 Test de la tâche 'execute_mission'...")
        task_mission = Task(task_id="test_mission_01", description="execute_mission", params={'mission_data': None})
        result_mission = await agent.execute_task(task_mission)
        print(f"   Résultat de la mission: {'Succès' if result_mission.success else 'Échec'}")
        if not result_mission.success:
            print(f"   Erreur mission: {result_mission.error}")
        agent.logger.info(f"MAIN_TEST - Mission Task ID: {task_mission.task_id}, Description: {task_mission.description}")
        agent.logger.info(f"MAIN_TEST - Mission Result Success: {result_mission.success}")
        agent.logger.info(f"MAIN_TEST - Mission Result Data: {result_mission.data}")
        if result_mission.error:
            agent.logger.error(f"MAIN_TEST - Mission Result Error: {result_mission.error}")

        print("\n🔬 Test de la tâche 'audit_universal_quality'...")
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                # test_code n'est plus lu ici car la méthode d'audit s'en charge
                pass # Garder le bloc with open pour ne pas trop changer la structure, même si test_code n'est plus utilisé ici
            
            # Mettre à jour la création de la tâche pour ne plus passer 'code'
            audit_task = Task(task_id="audit_quality_test_01", description="audit_universal_quality", params={"file_path": __file__})
            
            agent.logger.info(f"MAIN_TEST - Lancement de la tâche d'audit pour: {__file__}")
            audit_result = await agent.execute_task(audit_task)

            # Log détaillé des résultats de l'audit
            agent.logger.info(f"MAIN_TEST - Audit Task ID: {audit_task.task_id}, Description: {audit_task.description}")
            agent.logger.info(f"MAIN_TEST - Audit Result Success: {audit_result.success}")
            agent.logger.info(f"MAIN_TEST - Audit Result Data: {audit_result.data}")
            if audit_result.error:
                agent.logger.error(f"MAIN_TEST - Audit Result Error: {audit_result.error}")

            print(f"   Résultat de l'audit: {'Succès' if audit_result.success else 'Échec'}")
            if audit_result.success and audit_result.data:
                report_data = audit_result.data.get('audit_report', {})
                print(f"   Score de qualité de ce fichier: {report_data.get('quality_score', 'N/A')}/100")
                if report_data.get('issues'):
                    print("   Problèmes trouvés:")
                    for issue_dict in report_data.get('issues', []):
                        print(f"     - L{issue_dict.get('line', 'N/A')}:{issue_dict.get('column', 'N/A')} [{issue_dict.get('code', 'N/A')}] {issue_dict.get('description', 'N/A')} ({issue_dict.get('severity', 'N/A')})")
                else:
                    print("   Aucun problème substantiel trouvé par l'audit.") # Message plus précis
            elif not audit_result.success:
                print(f"   Erreur audit: {audit_result.error}")

        except Exception as e:
            print(f"   Erreur durant le test d'audit (bloc try/except externe): {e}")
            agent.logger.error(f"MAIN_TEST - Erreur Exception dans le bloc de test d'audit: {e}", exc_info=True)

    except Exception as e:
        print(f"❌ Erreur durant l'exécution de l'agent (bloc try/except principal): {e}")
        agent.logger.error(f"MAIN_TEST - Erreur Exception dans main(): {e}", exc_info=True)
    finally:
        await agent.shutdown()
        print("\n✅ Test terminé.")


if __name__ == "__main__":
    asyncio.run(main())


