#!/usr/bin/env python3
"""
🩺 AGENT DOCTEUR - PATTERN FACTORY NEXTGENERATION
Mission: Diagnostic et réparation automatique des agents défaillants

Architecture Pattern Factory:
- Hérite de Agent de base  
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé

Responsabilités:
- Diagnostic automatique des agents en erreur
- Réparation des erreurs Pattern Factory courantes
- Restauration de la conformité
- Sauvegarde de sécurité avant modification
- Validation post-réparation
- Historique des interventions
"""

import asyncio
import logging
import json
import re
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys

# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent))
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {e}")
        # Fallback pour compatibilité
        class Agent:
            def __init__(self, agent_type: str, **config):
                self.agent_id = f"docteur_reparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.agent_type = agent_type
                self.config = config
                self.logger = logging.getLogger("AgentDocteurReparation")
                
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

class AgentDocteurReparation(Agent):
    """Agent Docteur de Réparation - Pattern Factory NextGeneration"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory
        super().__init__("docteur_reparation", **config)
        
        # Configuration spécialisée
        self.backup_mode = config.get("backup_mode", True)
        self.auto_repair = config.get("auto_repair", True)
        self.max_repair_attempts = config.get("max_repair_attempts", 3)
        
        # Historique des réparations
        self.repair_history = []
        self.backup_directory = Path.cwd() / "backups_docteur"
        
        # Templates de réparation Pattern Factory
        self.repair_templates = self.initialiser_templates_reparation()
        
        # Configuration logging Pattern Factory (avec fallback)
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger("AgentDocteurReparation")
        
        # Assurer que les attributs existent (fallback)
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"docteur_reparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not hasattr(self, 'agent_type'):
            self.agent_type = "docteur_reparation"
            
        self.logger.info(f"🩺 Agent Docteur Réparation initialisé - ID: {self.agent_id}")
        
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage agent docteur réparation"""
        self.logger.info(f"🚀 Agent Docteur Réparation {self.agent_id} - DÉMARRAGE")
        
        # Création répertoire backup
        if self.backup_mode:
            await self.initialiser_backup_directory()
        
        # Chargement historique réparations
        await self.charger_historique_reparations()
        
        self.logger.info("✅ Agent Docteur Réparation démarré avec succès")
        
    async def shutdown(self):
        """Arrêt agent docteur réparation"""
        self.logger.info(f"🛑 Agent Docteur Réparation {self.agent_id} - ARRÊT")
        
        # Sauvegarde historique
        await self.sauvegarder_historique_reparations()
        
        # Génération rapport final
        await self.generer_rapport_interventions()
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent docteur réparation"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "backup_mode": self.backup_mode,
            "auto_repair": self.auto_repair,
            "repairs_performed": len(self.repair_history),
            "backup_directory": str(self.backup_directory),
            "capabilities": self.get_capabilities(),
            "timestamp": datetime.now().isoformat()
        }
    
    # Méthodes abstraites OBLIGATOIRES pour Pattern Factory
    async def execute_task(self, task: Any) -> Any:
        """Exécution d'une tâche spécifique - Méthode abstraite obligatoire"""
        try:
            self.logger.info(f"📋 Exécution tâche docteur: {task}")
            
            if isinstance(task, dict):
                task_type = task.get("type")
                
                if task_type == "diagnose_agent":
                    return await self.diagnostiquer_agent(task.get("agent_path"))
                elif task_type == "repair_agent":
                    return await self.reparer_agent(task.get("agent_path"))
                elif task_type == "repair_all_agents":
                    return await self.reparer_tous_agents()
                elif task_type == "restore_agent":
                    return await self.restaurer_agent(task.get("agent_path"))
            
            # Tâche par défaut - diagnostic et réparation complète
            return await self.executer_mission_complete()
            
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche docteur: {e}")
            return {"error": str(e)}
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent - Méthode abstraite obligatoire"""
        return [
            "agent_diagnosis",
            "automatic_repair",
            "pattern_factory_restoration",
            "backup_management",
            "syntax_correction",
            "import_fixing",
            "method_injection",
            "compliance_restoration",
            "error_detection",
            "rollback_capability"
        ]
    
    # Méthodes métier spécialisées
    def initialiser_templates_reparation(self) -> Dict[str, str]:
        """Initialisation des templates de réparation Pattern Factory"""
        return {
            "pattern_factory_import": '''# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent))
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {e}")
        # Fallback pour compatibilité
        class Agent:
            def __init__(self, agent_type: str, **config):
                self.agent_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.agent_type = agent_type
                self.config = config
                self.logger = logging.getLogger(f"Agent_{agent_type}")
                
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
        
        PATTERN_FACTORY_AVAILABLE = False''',
            
            "required_methods": '''    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage agent"""
        self.logger.info(f"🚀 Agent {self.agent_id} - DÉMARRAGE")
        
    async def shutdown(self):
        """Arrêt agent"""
        self.logger.info(f"🛑 Agent {self.agent_id} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    
    async def execute_task(self, task: Any) -> Any:
        """Exécution d'une tâche spécifique - Méthode abstraite obligatoire"""
        try:
            self.logger.info(f"📋 Exécution tâche: {task}")
            # Logique métier à adapter
            return {"success": True, "result": "Task executed"}
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche: {e}")
            return {"error": str(e)}
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent - Méthode abstraite obligatoire"""
        return ["basic_capability"]''',
            
            "factory_function": '''
# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_{agent_name}(**config):
    """Factory function pour créer un Agent {agent_name} conforme Pattern Factory"""
    return Agent{agent_name}(**config)''',
            
            "main_function": '''
# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    print("🚀 AGENT {agent_name} - PATTERN FACTORY NEXTGENERATION")
    print("=" * 50)
    
    # Créer l'agent via factory
    agent = create_agent_{agent_name}()
    
    try:
        # Démarrage Pattern Factory
        await agent.startup()
        
        # Vérification santé
        health = await agent.health_check()
        print(f"🏥 Health Check: {health['status']}")
        
        # Test exécution
        task_test = {"type": "test"}
        result = await agent.execute_task(task_test)
        print(f"✅ Test: {result}")
        
        # Arrêt propre
        await agent.shutdown()
        
        print("\\n🎯 AGENT OPÉRATIONNEL!")
        
    except Exception as e:
        print(f"❌ Erreur execution agent: {e}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())'''
        }
    
    async def initialiser_backup_directory(self):
        """Initialisation du répertoire de backup"""
        try:
            self.backup_directory.mkdir(exist_ok=True)
            self.logger.info(f"✅ Répertoire backup initialisé: {self.backup_directory}")
        except Exception as e:
            self.logger.error(f"❌ Erreur création backup directory: {e}")
            raise
    
    async def diagnostiquer_agent(self, agent_path: str) -> Dict[str, Any]:
        """Diagnostic complet d'un agent défaillant"""
        try:
            self.logger.info(f"🔍 Diagnostic agent: {agent_path}")
            
            agent_file = Path(agent_path)
            if not agent_file.exists():
                return {"error": f"Agent non trouvé: {agent_path}", "status": "not_found"}
            
            # Lecture du fichier
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            diagnostic = {
                "agent_path": str(agent_file),
                "timestamp": datetime.now().isoformat(),
                "issues_detected": [],
                "severity": "none",
                "repair_recommendations": []
            }
            
            # Diagnostic syntaxe
            syntaxe_issues = await self.diagnostiquer_syntaxe(content, agent_file)
            if syntaxe_issues:
                diagnostic["issues_detected"].extend(syntaxe_issues)
                diagnostic["severity"] = "critical"
            
            # Diagnostic conformité Pattern Factory
            conformity_issues = await self.diagnostiquer_conformite_pattern_factory(content)
            if conformity_issues:
                diagnostic["issues_detected"].extend(conformity_issues)
                if diagnostic["severity"] == "none":
                    diagnostic["severity"] = "warning"
            
            # Diagnostic méthodes obligatoires
            methods_issues = await self.diagnostiquer_methodes_obligatoires(content)
            if methods_issues:
                diagnostic["issues_detected"].extend(methods_issues)
                diagnostic["severity"] = "critical"
            
            # Génération recommandations
            diagnostic["repair_recommendations"] = await self.generer_recommandations_reparation(
                diagnostic["issues_detected"]
            )
            
            # Calcul priorité réparation
            diagnostic["repair_priority"] = await self.calculer_priorite_reparation(diagnostic)
            
            self.logger.info(f"✅ Diagnostic terminé: {len(diagnostic['issues_detected'])} problèmes détectés")
            return diagnostic
            
        except Exception as e:
            self.logger.error(f"❌ Erreur diagnostic agent {agent_path}: {e}")
            return {
                "error": str(e),
                "status": "error",
                "agent_path": agent_path,
                "timestamp": datetime.now().isoformat()
            }
    
    async def diagnostiquer_syntaxe(self, content: str, agent_file: Path) -> List[Dict[str, Any]]:
        """Diagnostic des erreurs de syntaxe"""
        issues = []
        
        try:
            compile(content, str(agent_file), 'exec')
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": e.lineno,
                "message": e.msg,
                "text": e.text.strip() if e.text else "",
                "repair_action": "fix_syntax"
            })
        except Exception as e:
            issues.append({
                "type": "compilation_error",
                "severity": "critical",
                "message": str(e),
                "repair_action": "manual_review"
            })
        
        return issues
    
    async def diagnostiquer_conformite_pattern_factory(self, content: str) -> List[Dict[str, Any]]:
        """Diagnostic de conformité Pattern Factory"""
        issues = []
        
        # Vérification import Pattern Factory
        if ("from core.agent_factory_architecture import" not in content and 
            "from agent_factory_implementation.core" not in content):
            issues.append({
                "type": "missing_pattern_factory_import",
                "severity": "warning",
                "message": "Import Pattern Factory manquant",
                "repair_action": "add_pattern_factory_import"
            })
        
        # Vérification héritage Agent
        if not (re.search(r'class\s+\w+\s*\(\s*Agent\s*\)', content)):
            issues.append({
                "type": "missing_agent_inheritance",
                "severity": "critical",
                "message": "Héritage Agent manquant",
                "repair_action": "add_agent_inheritance"
            })
        
        # Vérification fonction factory
        if not re.search(r'def\s+create_\w+.*factory', content, re.IGNORECASE):
            issues.append({
                "type": "missing_factory_function",
                "severity": "warning",
                "message": "Fonction factory manquante",
                "repair_action": "add_factory_function"
            })
        
        # Vérification docstring Pattern Factory
        if "Pattern Factory" not in content:
            issues.append({
                "type": "missing_pattern_factory_docstring",
                "severity": "minor",
                "message": "Documentation Pattern Factory manquante",
                "repair_action": "add_pattern_factory_docstring"
            })
        
        return issues
    
    async def diagnostiquer_methodes_obligatoires(self, content: str) -> List[Dict[str, Any]]:
        """Diagnostic des méthodes obligatoires Pattern Factory"""
        issues = []
        
        required_methods = {
            "startup": r'async\s+def\s+startup',
            "shutdown": r'async\s+def\s+shutdown',
            "health_check": r'async\s+def\s+health_check',
            "execute_task": r'(async\s+)?def\s+execute_task',
            "get_capabilities": r'def\s+get_capabilities'
        }
        
        for method_name, pattern in required_methods.items():
            if not re.search(pattern, content):
                issues.append({
                    "type": "missing_required_method",
                    "severity": "critical",
                    "method": method_name,
                    "message": f"Méthode obligatoire '{method_name}' manquante",
                    "repair_action": "add_required_method"
                })
        
        return issues
    
    async def generer_recommandations_reparation(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Génération des recommandations de réparation"""
        recommendations = []
        
        # Grouper par type d'action
        actions = {}
        for issue in issues:
            action = issue.get("repair_action", "manual_review")
            if action not in actions:
                actions[action] = []
            actions[action].append(issue)
        
        # Générer recommandations
        for action, action_issues in actions.items():
            if action == "add_pattern_factory_import":
                recommendations.append("Ajouter l'import Pattern Factory standard")
            elif action == "add_agent_inheritance":
                recommendations.append("Corriger l'héritage de la classe Agent")
            elif action == "add_required_method":
                methods = [issue["method"] for issue in action_issues if "method" in issue]
                recommendations.append(f"Ajouter méthodes obligatoires: {', '.join(methods)}")
            elif action == "add_factory_function":
                recommendations.append("Ajouter fonction factory de création")
            elif action == "fix_syntax":
                recommendations.append("Corriger erreurs de syntaxe Python")
            else:
                recommendations.append(f"Révision manuelle requise ({action})")
        
        return recommendations
    
    async def calculer_priorite_reparation(self, diagnostic: Dict[str, Any]) -> str:
        """Calcul de la priorité de réparation"""
        severity = diagnostic.get("severity", "none")
        issues_count = len(diagnostic.get("issues_detected", []))
        
        if severity == "critical":
            return "HIGH"
        elif severity == "warning" and issues_count > 3:
            return "MEDIUM"
        elif severity == "warning":
            return "LOW"
        else:
            return "NONE"
    
    async def reparer_agent(self, agent_path: str) -> Dict[str, Any]:
        """Réparation automatique d'un agent"""
        try:
            self.logger.info(f"🔧 Réparation agent: {agent_path}")
            
            agent_file = Path(agent_path)
            if not agent_file.exists():
                return {"error": f"Agent non trouvé: {agent_path}", "status": "not_found"}
            
            # Diagnostic préalable
            diagnostic = await self.diagnostiquer_agent(agent_path)
            if diagnostic.get("error"):
                return diagnostic
            
            # Backup de sécurité
            backup_path = None
            if self.backup_mode:
                backup_path = await self.creer_backup_agent(agent_file)
            
            # Lecture contenu original
            with open(agent_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            repair_result = {
                "agent_path": str(agent_file),
                "timestamp": datetime.now().isoformat(),
                "backup_path": str(backup_path) if backup_path else None,
                "issues_repaired": [],
                "issues_remaining": [],
                "repair_success": False,
                "modifications_applied": []
            }
            
            # Application des réparations
            modified_content = original_content
            
            for issue in diagnostic.get("issues_detected", []):
                repair_action = issue.get("repair_action")
                
                if repair_action == "add_pattern_factory_import":
                    modified_content = await self.appliquer_reparation_import(modified_content)
                    repair_result["issues_repaired"].append(issue)
                    repair_result["modifications_applied"].append("Pattern Factory import ajouté")
                
                elif repair_action == "add_required_method":
                    method_name = issue.get("method")
                    if method_name:
                        modified_content = await self.appliquer_reparation_methode(
                            modified_content, method_name
                        )
                        repair_result["issues_repaired"].append(issue)
                        repair_result["modifications_applied"].append(f"Méthode {method_name} ajoutée")
                
                elif repair_action == "add_factory_function":
                    agent_name = await self.extraire_nom_agent(agent_file)
                    modified_content = await self.appliquer_reparation_factory(
                        modified_content, agent_name
                    )
                    repair_result["issues_repaired"].append(issue)
                    repair_result["modifications_applied"].append("Fonction factory ajoutée")
                
                else:
                    # Réparation non automatique
                    repair_result["issues_remaining"].append(issue)
            
            # Sauvegarde des modifications
            if modified_content != original_content:
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                repair_result["repair_success"] = True
                
                # Validation post-réparation
                validation = await self.valider_post_reparation(agent_file)
                repair_result["post_repair_validation"] = validation
                
                # Historique
                await self.enregistrer_reparation(repair_result)
                
                self.logger.info(f"✅ Réparation terminée: {len(repair_result['issues_repaired'])} corrections")
            else:
                repair_result["repair_success"] = False
                self.logger.warning("⚠️ Aucune modification automatique possible")
            
            return repair_result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur réparation agent {agent_path}: {e}")
            return {
                "error": str(e),
                "status": "error",
                "agent_path": agent_path,
                "timestamp": datetime.now().isoformat()
            }
    
    async def creer_backup_agent(self, agent_file: Path) -> Path:
        """Création d'un backup de sécurité de l'agent"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{agent_file.stem}_{timestamp}.backup"
            backup_path = self.backup_directory / backup_filename
            
            shutil.copy2(agent_file, backup_path)
            
            self.logger.info(f"💾 Backup créé: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création backup: {e}")
            raise
    
    async def appliquer_reparation_import(self, content: str) -> str:
        """Application de la réparation import Pattern Factory"""
        # Recherche de la position d'insertion
        lines = content.split('\n')
        
        # Chercher après les imports standard
        insert_position = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                insert_position = i + 1
            elif line.strip() == '' and insert_position > 0:
                break
        
        # Insertion du template
        import_template = self.repair_templates["pattern_factory_import"]
        
        # Insertion à la bonne position
        lines.insert(insert_position, "")
        lines.insert(insert_position + 1, import_template)
        lines.insert(insert_position + 2, "")
        
        return '\n'.join(lines)
    
    async def appliquer_reparation_methode(self, content: str, method_name: str) -> str:
        """Application de la réparation méthode obligatoire"""
        method_templates = {
            "startup": '''    async def startup(self):
        """Démarrage agent"""
        self.logger.info(f"🚀 Agent {self.agent_id} - DÉMARRAGE")''',
            
            "shutdown": '''    async def shutdown(self):
        """Arrêt agent"""
        self.logger.info(f"🛑 Agent {self.agent_id} - ARRÊT")''',
            
            "health_check": '''    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé agent"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }''',
            
            "execute_task": '''    async def execute_task(self, task: Any) -> Any:
        """Exécution d'une tâche spécifique - Méthode abstraite obligatoire"""
        try:
            self.logger.info(f"📋 Exécution tâche: {task}")
            # Logique métier à adapter
            return {"success": True, "result": "Task executed"}
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche: {e}")
            return {"error": str(e)}''',
            
            "get_capabilities": '''    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent - Méthode abstraite obligatoire"""
        return ["basic_capability"]'''
        }
        
        if method_name not in method_templates:
            return content
        
        # Recherche de la classe pour insertion
        lines = content.split('\n')
        class_line = -1
        
        for i, line in enumerate(lines):
            if re.match(r'class\s+\w+.*Agent.*:', line):
                class_line = i
                break
        
        if class_line == -1:
            return content
        
        # Recherche de la fin de la classe pour insertion
        insert_position = len(lines) - 1
        
        # Insertion de la méthode
        method_code = method_templates[method_name]
        lines.insert(insert_position, "")
        lines.insert(insert_position + 1, method_code)
        lines.insert(insert_position + 2, "")
        
        return '\n'.join(lines)
    
    async def appliquer_reparation_factory(self, content: str, agent_name: str) -> str:
        """Application de la réparation fonction factory"""
        factory_template = self.repair_templates["factory_function"].format(
            agent_name=agent_name
        )
        
        # Ajout à la fin du fichier
        return content + "\n" + factory_template
    
    async def extraire_nom_agent(self, agent_file: Path) -> str:
        """Extraction du nom de l'agent depuis le fichier"""
        # Tentative d'extraction depuis le nom de fichier
        name = agent_file.stem
        if name.startswith("agent_"):
            name = name[6:]  # Enlever "agent_"
        
        # Conversion en CamelCase
        parts = name.split("_")
        return "".join(word.capitalize() for word in parts)
    
    async def valider_post_reparation(self, agent_file: Path) -> Dict[str, Any]:
        """Validation après réparation"""
        try:
            # Vérification syntaxe
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                compile(content, str(agent_file), 'exec')
                syntax_ok = True
            except:
                syntax_ok = False
            
            # Diagnostic rapide
            diagnostic_post = await self.diagnostiquer_agent(str(agent_file))
            
            return {
                "syntax_valid": syntax_ok,
                "remaining_issues": len(diagnostic_post.get("issues_detected", [])),
                "severity": diagnostic_post.get("severity", "none"),
                "validation_success": syntax_ok and diagnostic_post.get("severity") in ["none", "minor"]
            }
            
        except Exception as e:
            return {
                "syntax_valid": False,
                "error": str(e),
                "validation_success": False
            }
    
    async def reparer_tous_agents(self) -> Dict[str, Any]:
        """Réparation de tous les agents défaillants"""
        try:
            self.logger.info("🔧 Réparation de tous les agents")
            
            workspace = Path.cwd()
            agents = list(workspace.glob("agent_*.py"))
            
            if len(agents) > 10:
                self.logger.warning(f"⚠️ Beaucoup d'agents ({len(agents)}), limitation à 10 premiers")
                agents = agents[:10]
            
            resultats = {
                "timestamp": datetime.now().isoformat(),
                "total_agents": len(agents),
                "repair_results": [],
                "summary": {}
            }
            
            # Réparations séquentielles pour sécurité
            success_count = 0
            failed_count = 0
            
            for agent in agents:
                try:
                    # Diagnostic d'abord
                    diagnostic = await self.diagnostiquer_agent(str(agent))
                    
                    if diagnostic.get("severity") in ["critical", "warning"]:
                        # Réparation nécessaire
                        repair_result = await self.reparer_agent(str(agent))
                        resultats["repair_results"].append(repair_result)
                        
                        if repair_result.get("repair_success"):
                            success_count += 1
                        else:
                            failed_count += 1
                    else:
                        # Agent sain
                        resultats["repair_results"].append({
                            "agent_path": str(agent),
                            "status": "healthy",
                            "repair_needed": False
                        })
                        
                except Exception as e:
                    failed_count += 1
                    resultats["repair_results"].append({
                        "agent_path": str(agent),
                        "error": str(e),
                        "status": "error"
                    })
            
            # Statistiques finales
            resultats["summary"] = {
                "repaired_successfully": success_count,
                "repair_failed": failed_count,
                "total_processed": len(agents),
                "success_rate": round(success_count / len(agents) * 100, 1) if agents else 0
            }
            
            self.logger.info(f"✅ Réparations terminées: {success_count}/{len(agents)} succès")
            return resultats
            
        except Exception as e:
            self.logger.error(f"❌ Erreur réparation tous agents: {e}")
            return {"error": str(e)}
    
    async def restaurer_agent(self, agent_path: str) -> Dict[str, Any]:
        """Restauration d'un agent depuis son backup"""
        try:
            self.logger.info(f"🔄 Restauration agent: {agent_path}")
            
            agent_file = Path(agent_path)
            
            # Recherche du backup le plus récent
            agent_stem = agent_file.stem
            backups = list(self.backup_directory.glob(f"{agent_stem}_*.backup"))
            
            if not backups:
                return {
                    "error": f"Aucun backup trouvé pour {agent_path}",
                    "status": "no_backup"
                }
            
            # Backup le plus récent
            latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
            
            # Restauration
            shutil.copy2(latest_backup, agent_file)
            
            result = {
                "agent_path": str(agent_file),
                "restored_from": str(latest_backup),
                "timestamp": datetime.now().isoformat(),
                "restore_success": True
            }
            
            # Validation post-restauration
            validation = await self.valider_post_reparation(agent_file)
            result["post_restore_validation"] = validation
            
            self.logger.info(f"✅ Restauration terminée: {agent_file.name}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur restauration agent {agent_path}: {e}")
            return {
                "error": str(e),
                "status": "error",
                "agent_path": agent_path,
                "timestamp": datetime.now().isoformat()
            }
    
    async def executer_mission_complete(self) -> Dict[str, Any]:
        """Exécution d'une mission complète de diagnostic et réparation"""
        try:
            self.logger.info("🩺 Mission complète diagnostic et réparation")
            
            resultats = {
                "timestamp": datetime.now().isoformat(),
                "mission_type": "complete",
                "phases": {}
            }
            
            # Phase 1: Diagnostic général
            self.logger.info("🔍 Phase 1: Diagnostic général")
            resultats["phases"]["diagnostic"] = await self.diagnostiquer_tous_agents()
            
            # Phase 2: Réparations automatiques
            self.logger.info("🔧 Phase 2: Réparations automatiques")
            resultats["phases"]["repair"] = await self.reparer_tous_agents()
            
            # Phase 3: Validation finale
            self.logger.info("✅ Phase 3: Validation finale")
            resultats["phases"]["validation"] = await self.valider_tous_agents()
            
            # Résumé global
            resultats["summary"] = await self.generer_resume_mission(resultats["phases"])
            
            self.logger.info("✅ Mission complète terminée")
            return resultats
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mission complète: {e}")
            return {"error": str(e)}
    
    async def diagnostiquer_tous_agents(self) -> Dict[str, Any]:
        """Diagnostic de tous les agents"""
        try:
            workspace = Path.cwd()
            agents = list(workspace.glob("agent_*.py"))
            
            diagnostics = []
            critical_count = 0
            warning_count = 0
            healthy_count = 0
            
            for agent in agents[:10]:  # Limite pour sécurité
                diagnostic = await self.diagnostiquer_agent(str(agent))
                diagnostics.append(diagnostic)
                
                severity = diagnostic.get("severity", "none")
                if severity == "critical":
                    critical_count += 1
                elif severity == "warning":
                    warning_count += 1
                else:
                    healthy_count += 1
            
            return {
                "total_agents": len(diagnostics),
                "critical_issues": critical_count,
                "warning_issues": warning_count,
                "healthy_agents": healthy_count,
                "diagnostics": diagnostics
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def valider_tous_agents(self) -> Dict[str, Any]:
        """Validation de tous les agents après réparation"""
        try:
            workspace = Path.cwd()
            agents = list(workspace.glob("agent_*.py"))
            
            validations = []
            valid_count = 0
            
            for agent in agents[:10]:  # Limite pour sécurité
                validation = await self.valider_post_reparation(agent)
                validation["agent_path"] = str(agent)
                validations.append(validation)
                
                if validation.get("validation_success"):
                    valid_count += 1
            
            return {
                "total_validated": len(validations),
                "valid_agents": valid_count,
                "validation_rate": round(valid_count / len(validations) * 100, 1) if validations else 0,
                "validations": validations
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def generer_resume_mission(self, phases: Dict[str, Any]) -> Dict[str, Any]:
        """Génération du résumé de mission"""
        resume = {
            "mission_success": True,
            "issues_resolved": 0,
            "agents_improved": 0,
            "recommendations": []
        }
        
        # Analyse diagnostic
        if "diagnostic" in phases:
            diagnostic = phases["diagnostic"]
            critical = diagnostic.get("critical_issues", 0)
            warning = diagnostic.get("warning_issues", 0)
            
            if critical > 0:
                resume["recommendations"].append(f"Résoudre {critical} problèmes critiques")
            if warning > 0:
                resume["recommendations"].append(f"Traiter {warning} avertissements")
        
        # Analyse réparations
        if "repair" in phases:
            repair = phases["repair"]
            success_rate = repair.get("summary", {}).get("success_rate", 0)
            
            if success_rate < 80:
                resume["mission_success"] = False
                resume["recommendations"].append("Taux de réparation insuffisant")
            
            resume["agents_improved"] = repair.get("summary", {}).get("repaired_successfully", 0)
        
        # Analyse validation
        if "validation" in phases:
            validation = phases["validation"]
            validation_rate = validation.get("validation_rate", 0)
            
            if validation_rate >= 90:
                resume["recommendations"].append("Excellent ! Agents en bonne santé")
            elif validation_rate >= 70:
                resume["recommendations"].append("Bon état général, surveillance recommandée")
            else:
                resume["mission_success"] = False
                resume["recommendations"].append("Attention ! Plusieurs agents nécessitent une intervention")
        
        return resume
    
    async def enregistrer_reparation(self, repair_result: Dict[str, Any]):
        """Enregistrement dans l'historique des réparations"""
        self.repair_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent_path": repair_result.get("agent_path"),
            "issues_repaired": len(repair_result.get("issues_repaired", [])),
            "success": repair_result.get("repair_success", False),
            "modifications": repair_result.get("modifications_applied", [])
        })
    
    async def charger_historique_reparations(self):
        """Chargement de l'historique des réparations"""
        try:
            history_file = Path.cwd() / "historique_reparations_docteur.json"
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.repair_history = json.load(f)
                self.logger.info(f"✅ Historique chargé: {len(self.repair_history)} réparations")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement historique: {e}")
    
    async def sauvegarder_historique_reparations(self):
        """Sauvegarde de l'historique des réparations"""
        try:
            history_file = Path.cwd() / "historique_reparations_docteur.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.repair_history, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ Historique sauvegardé: {len(self.repair_history)} réparations")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur sauvegarde historique: {e}")
    
    async def generer_rapport_interventions(self):
        """Génération du rapport final des interventions"""
        try:
            rapport = {
                "session_info": {
                    "agent_id": self.agent_id,
                    "session_start": getattr(self, 'start_time', datetime.now().isoformat()),
                    "session_end": datetime.now().isoformat(),
                    "backup_mode": self.backup_mode,
                    "auto_repair": self.auto_repair
                },
                "statistics": {
                    "total_repairs": len(self.repair_history),
                    "successful_repairs": len([r for r in self.repair_history if r.get("success")]),
                    "agents_processed": len(set(r.get("agent_path") for r in self.repair_history if r.get("agent_path")))
                },
                "interventions": self.repair_history,
                "capabilities_used": self.get_capabilities()
            }
            
            rapport_file = Path.cwd() / f"rapport_interventions_docteur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(rapport_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"📄 Rapport interventions généré: {rapport_file}")
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur génération rapport: {e}")

# Fonction factory pour créer l'agent (Pattern Factory)
def create_agent_docteur_reparation(**config) -> AgentDocteurReparation:
    """Factory function pour créer un Agent Docteur Réparation conforme Pattern Factory"""
    return AgentDocteurReparation(**config)

# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    print("🩺 AGENT DOCTEUR RÉPARATION - PATTERN FACTORY NEXTGENERATION")
    print("=" * 70)
    
    # Créer l'agent via factory
    agent = create_agent_docteur_reparation(backup_mode=True, auto_repair=True)
    
    try:
        # Démarrage Pattern Factory
        await agent.startup()
        
        # Vérification santé
        health = await agent.health_check()
        print(f"🏥 Health Check: {health['status']} - Backup: {'On' if health['backup_mode'] else 'Off'}")
        
        # Mission complète de diagnostic et réparation
        print("\n🩺 Mission complète diagnostic et réparation...")
        task_mission = {
            "type": "repair_all_agents"
        }
        
        results = await agent.execute_task(task_mission)
        if "summary" in results:
            summary = results["summary"]
            print(f"✅ Mission terminée:")
            print(f"   - Agents traités: {summary['total_processed']}")
            print(f"   - Réparations réussies: {summary['repaired_successfully']}")
            print(f"   - Taux de succès: {summary['success_rate']}%")
        
        # Arrêt propre
        await agent.shutdown()
        
        print("\n🎯 AGENT DOCTEUR OPÉRATIONNEL!")
        
    except Exception as e:
        print(f"❌ Erreur execution agent docteur: {e}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 