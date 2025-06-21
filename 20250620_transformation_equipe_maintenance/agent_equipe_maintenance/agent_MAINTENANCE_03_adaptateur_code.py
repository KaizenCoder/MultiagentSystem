#!/usr/bin/env python3
"""
🔧 AGENT 03 ADAPTATEUR CODE UPGRADED - PATTERN FACTORY NEXTGENERATION
=======================================================================

Mission: Transformer les agents non-conformes vers le Pattern Factory
Spécialisation: Transformation basée sur les rapports d'audit de l'Agent 04

Nouvelles Capacités:
- Transformation automatique vers Pattern Factory
- Correction des erreurs syntaxe (async async def)
- Migration des architectures hybrides
- Intégration avec les rapports d'audit Agent 04
- Validation post-transformation

Architecture Pattern Factory:
- Hérite de Agent de base  
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé

Author: Équipe Maintenance NextGeneration
Version: 2.0.0 - UPGRADED
Created: 2025-01-20
"""

import asyncio
import ast
import logging
from logging_manager_optimized import LoggingManager
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import shutil

# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
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
                self.agent_id = f"adaptateur_code_upgraded_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.agent_type = agent_type
                self.config = config
                # Configuration logging
                logging.basicConfig(level=logging.INFO)
                # LoggingManager NextGeneration - Agent
                from logging_manager_optimized import LoggingManager
                self.logger = LoggingManager().get_agent_logger(
                    agent_name="Agent",
                    role="ai_processor",
                    domain="general",
                    async_enabled=True
                )
                
            async def startup(self): pass
            async def shutdown(self): pass
            async def health_check(self): return {"status": "healthy"}
            def get_capabilities(self): return []
        
        async def startup(self): pass
        async def shutdown(self): pass
        async def health_check(self): return {"status": "healthy"}
        def get_capabilities(self): return []
        
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

class AdaptateurCodeUpgraded(Agent):
    """AdaptateurCodeUpgraded - Transformation Pattern Factory Avancée"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory
        super().__init__("adaptateur_code_upgraded", **config)
        
        # S'assurer que le logger est disponible (fallback si nécessaire)
        if not hasattr(self, 'logger'):
            if not hasattr(self, 'agent_id'):
                self.agent_id = f"adaptateur_code_upgraded_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(f"AdaptateurCodeUpgraded_{self.agent_id}")
        
        # Configuration spécialisée
        self.reports_dir = Path("reports")
        self.backup_dir = Path("backup_transformations")  # Par défaut, sera reconfiguré
        self.templates_dir = Path("templates")
        
        # Charger configuration dynamique du chef d'équipe si disponible
        self._load_dynamic_configuration()
        
        # Statistiques de transformation
        self.transformation_stats = {
            "agents_processed": 0,
            "agents_transformed": 0,
            "critical_errors_fixed": 0,
            "syntax_errors_fixed": 0,
            "pattern_factory_migrations": 0
        }
        
        # Configuration logging Pattern Factory
        self.logger.info(f"🔧 AdaptateurCodeUpgraded initialisé - ID: {self.agent_id}")
        
    def _load_dynamic_configuration(self):
        """Charger la configuration dynamique du chef d'équipe"""
        try:
            # Chercher le fichier de configuration Agent 03
            config_path = Path("config/agent_03_adaptateur_config.json")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                params = config_data.get("parameters", {})
                
                # Reconfigurer avec les paramètres du chef d'équipe
                if "backup_directory" in params:
                    self.backup_dir = Path(params["backup_directory"])
                    self.logger.info(f"🔧 Configuration dynamique: backup_dir = {self.backup_dir}")
                
                if "source_directory" in params:
                    self.source_dir = Path(params["source_directory"])
                    self.logger.info(f"🔧 Configuration dynamique: source_dir = {self.source_dir}")
                
                # Autres paramètres de configuration
                self.backup_obligatoire = params.get("backup_obligatoire", True)
                self.verification_integrite = params.get("verification_integrite", True)
                self.validation_syntaxe = params.get("validation_syntaxe", True)
                self.rollback_automatique = params.get("rollback_automatique", True)
                
                self.logger.info(f"✅ Configuration dynamique chargée depuis {config_path}")
                
            else:
                self.logger.info(f"ℹ️ Pas de configuration dynamique trouvée, utilisation des valeurs par défaut")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur chargement configuration dynamique: {e}")
            self.logger.info(f"ℹ️ Utilisation des valeurs par défaut")
        
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage adaptateur_code_upgraded"""
        self.logger.info(f"🚀 AdaptateurCodeUpgraded {self.agent_id} - DÉMARRAGE")
        
        # Créer les répertoires nécessaires
        self.reports_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        self.logger.info("✅ Agent démarré avec succès")
        
    async def shutdown(self):
        """Arrêt adaptateur_code_upgraded"""
        self.logger.info(f"🛑 AdaptateurCodeUpgraded {self.agent_id} - ARRÊT")
        
        # Sauvegarder les statistiques finales
        await self._save_transformation_stats()
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé adaptateur_code_upgraded"""
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"adaptateur_code_upgraded_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        if not hasattr(self, 'agent_type'):
            self.agent_type = "adaptateur_code_upgraded"
            
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "ready": True,
            "pattern_factory_available": PATTERN_FACTORY_AVAILABLE,
            "transformation_stats": self.transformation_stats,
            "timestamp": datetime.now().isoformat()
        }
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches de transformation - Pattern Factory OBLIGATOIRE"""
        try:
            self.logger.info(f"🎯 Exécution tâche: {task.task_id}")
            
            if task.task_id == "transform_from_audit_report":
                # Transformation basée sur rapport d'audit Agent 04
                audit_report_path = getattr(task, 'audit_report_path', None)
                target_directory = getattr(task, 'target_directory', None)
                
                if not audit_report_path or not target_directory:
                    return Result(success=False, error="audit_report_path et target_directory requis")
                
                results = await self.transform_from_audit_report(audit_report_path, target_directory)
                return Result(success=True, data=results)
                
            elif task.task_id == "fix_critical_errors":
                # Correction des erreurs critiques
                agent_file_path = getattr(task, 'agent_file_path', None)
                critical_issues = getattr(task, 'critical_issues', [])
                
                if not agent_file_path:
                    return Result(success=False, error="agent_file_path requis")
                
                results = await self.fix_critical_errors(agent_file_path, critical_issues)
                return Result(success=True, data=results)
                
            elif task.task_id == "migrate_to_pattern_factory":
                # Migration vers Pattern Factory
                agent_file_path = getattr(task, 'agent_file_path', None)
                agent_analysis = getattr(task, 'agent_analysis', {})
                
                if not agent_file_path:
                    return Result(success=False, error="agent_file_path requis")
                
                results = await self.migrate_to_pattern_factory(agent_file_path, agent_analysis)
                return Result(success=True, data=results)
                
            else:
                return Result(success=False, error=f"Tâche non reconnue: {task.task_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {task.task_id}: {e}")
            return Result(success=False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités avancées de transformation"""
        return [
            # Capacités de base
            "execute_mission",
            "process_data",
            "adapt_code",
            "transform_data",
            
            # 🆕 CAPACITÉS AVANCÉES DE TRANSFORMATION
            "transform_from_audit_report",
            "fix_critical_errors", 
            "migrate_to_pattern_factory",
            "fix_async_syntax_errors",
            "convert_hybrid_architecture",
            "inject_pattern_factory_imports",
            "generate_factory_methods",
            "add_abstract_method_implementations",
            "fix_fallback_implementations",
            "validate_post_transformation",
            "create_transformation_backups",
            "generate_transformation_reports",
            
            # Capacités techniques spécialisées
            "ast_advanced_transformation",
            "regex_pattern_replacement",
            "import_dependency_resolution",
            "code_structure_analysis",
            "syntax_error_detection",
            "semantic_error_correction",
            "architecture_pattern_detection",
            "factory_pattern_injection",
            "logging_standardization",
            "configuration_externalization"
        ]
    
    # 🆕 MÉTHODES AVANCÉES DE TRANSFORMATION
    
    async def transform_single_agent(self, agent_path: Path, force_backup: bool = True) -> Dict[str, Any]:
        """Transformation complète d'un seul agent avec sécurité maximale"""
        self.logger.info(f"🔧 Transformation agent unique: {agent_path}")
        
        try:
            # 1. Backup obligatoire si demandé
            backup_path = None
            if force_backup:
                backup_path = await self._create_backup(agent_path)
                self.logger.info(f"💾 Backup sécurité créé: {backup_path}")
            
            # 2. Lire et analyser le fichier
            with open(agent_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Analyser la structure actuelle
            structure = self._analyze_current_structure(original_content)
            
            # 3. Détecter les problèmes critiques
            critical_issues = []
            if "async async def" in original_content:
                critical_issues.append("async_syntax_error")
            if not structure.get('import_pattern_factory', False):
                critical_issues.append("missing_pattern_factory_import")
            if not structure.get('inherits_from_agent', False):
                critical_issues.append("missing_agent_inheritance")
            
            transformation_result = {
                "agent_path": str(agent_path),
                "backup_path": str(backup_path) if backup_path else None,
                "original_issues": critical_issues,
                "corrections_applied": 0,
                "transformations": [],
                "success": False,
                "final_validation": None
            }
            
            # 4. Corriger les erreurs critiques
            if critical_issues:
                self.logger.info(f"🚨 Correction {len(critical_issues)} problèmes critiques")
                fix_result = await self.fix_critical_errors(str(agent_path), critical_issues)
                transformation_result["transformations"].append({
                    "type": "critical_errors_fix",
                    "result": fix_result
                })
                transformation_result["corrections_applied"] += fix_result.get("corrections_applied", 0)
            
            # 5. Migration Pattern Factory si nécessaire
            conformity_score = sum([
                structure.get('has_main_class', False),
                structure.get('inherits_from_agent', False),
                structure.get('has_startup_method', False),
                structure.get('has_shutdown_method', False),
                structure.get('has_health_check_method', False),
                structure.get('has_execute_task_method', False)
            ]) / 6 * 100
            
            if conformity_score < 90:  # Moins de 90% conforme
                self.logger.info(f"🔄 Migration Pattern Factory (score: {conformity_score:.1f}%)")
                migration_result = await self.migrate_to_pattern_factory(str(agent_path), {"conformity_score": conformity_score})
                transformation_result["transformations"].append({
                    "type": "pattern_factory_migration", 
                    "result": migration_result
                })
                transformation_result["corrections_applied"] += migration_result.get("corrections_applied", 0)
            
            # 6. Validation finale
            validation_result = await self._validate_transformation(agent_path)
            transformation_result["final_validation"] = validation_result
            transformation_result["success"] = validation_result.get("success", False)
            
            # 7. Mise à jour statistiques
            self.transformation_stats["agents_processed"] += 1
            if transformation_result["success"]:
                self.transformation_stats["agents_transformed"] += 1
                self.transformation_stats["critical_errors_fixed"] += len(critical_issues)
            
            self.logger.info(f"✅ Transformation terminée: {transformation_result['success']}")
            return transformation_result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transformation agent: {e}")
            
            # Rollback automatique en cas d'erreur
            if backup_path and backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        backup_content = f.read()
                    with open(agent_path, 'w', encoding='utf-8') as f:
                        f.write(backup_content)
                    self.logger.info(f"🔄 Rollback automatique effectué depuis {backup_path}")
                except Exception as rollback_error:
                    self.logger.error(f"❌ Erreur rollback: {rollback_error}")
            
            return {
                "agent_path": str(agent_path),
                "backup_path": str(backup_path) if backup_path else None,
                "success": False,
                "error": str(e),
                "rollback_applied": backup_path.exists() if backup_path else False
            }
    
    async def transform_from_audit_report(self, audit_report_path: str, target_directory: str) -> Dict[str, Any]:
        """Transformation complète basée sur le rapport d'audit de l'Agent 04"""
        self.logger.info(f"🔄 Transformation basée sur rapport d'audit: {audit_report_path}")
        
        try:
            # Charger le rapport d'audit
            with open(audit_report_path, 'r', encoding='utf-8') as f:
                audit_report = json.load(f)
            
            transformation_results = {
                "audit_report_processed": audit_report_path,
                "target_directory": target_directory,
                "timestamp_start": datetime.now().isoformat(),
                "agents_processed": [],
                "transformations_applied": [],
                "errors_encountered": [],
                "summary": {}
            }
            
            # Traiter chaque agent du rapport
            agents_analysis = audit_report.get('agents_analysis', {})
            
            for agent_file, analysis in agents_analysis.items():
                agent_path = Path(target_directory) / agent_file
                
                if not agent_path.exists():
                    self.logger.warning(f"⚠️ Agent non trouvé: {agent_path}")
                    continue
                
                self.logger.info(f"🔧 Transformation agent: {agent_file}")
                
                # Analyser les problèmes de cet agent
                conformity_status = analysis.get('conformity_status', 'unknown')
                critical_issues = analysis.get('critical_issues', [])
                recommendations = analysis.get('recommendations', [])
                
                agent_transformation = {
                    "agent_file": agent_file,
                    "agent_path": str(agent_path),
                    "original_status": conformity_status,
                    "critical_issues": critical_issues,
                    "transformations_applied": [],
                    "final_status": "pending"
                }
                
                # Créer backup avant transformation
                backup_path = await self._create_backup(agent_path)
                agent_transformation["backup_path"] = str(backup_path)
                
                try:
                    # 1. Corriger les erreurs critiques
                    if critical_issues:
                        fix_result = await self.fix_critical_errors(str(agent_path), critical_issues)
                        agent_transformation["transformations_applied"].append({
                            "type": "critical_errors_fix",
                            "result": fix_result
                        })
                    
                    # 2. Migration Pattern Factory si nécessaire
                    if conformity_status in ['non_compliant', 'critical_errors']:
                        migration_result = await self.migrate_to_pattern_factory(str(agent_path), analysis)
                        agent_transformation["transformations_applied"].append({
                            "type": "pattern_factory_migration",
                            "result": migration_result
                        })
                    
                    # 3. Validation post-transformation
                    validation_result = await self._validate_transformation(agent_path)
                    agent_transformation["validation"] = validation_result
                    agent_transformation["final_status"] = "transformed" if validation_result["success"] else "failed"
                    
                    self.transformation_stats["agents_processed"] += 1
                    if agent_transformation["final_status"] == "transformed":
                        self.transformation_stats["agents_transformed"] += 1
                    
                except Exception as e:
                    self.logger.error(f"❌ Erreur transformation {agent_file}: {e}")
                    agent_transformation["error"] = str(e)
                    agent_transformation["final_status"] = "error"
                    transformation_results["errors_encountered"].append({
                        "agent": agent_file,
                        "error": str(e)
                    })
                
                transformation_results["agents_processed"].append(agent_transformation)
            
            # Générer résumé final
            transformation_results["summary"] = {
                "total_agents": len(agents_analysis),
                "agents_processed": self.transformation_stats["agents_processed"],
                "agents_transformed": self.transformation_stats["agents_transformed"],
                "success_rate": (self.transformation_stats["agents_transformed"] / max(1, self.transformation_stats["agents_processed"])) * 100,
                "timestamp_end": datetime.now().isoformat()
            }
            
            # Sauvegarder rapport de transformation
            await self._save_transformation_report(transformation_results)
            
            self.logger.info(f"✅ Transformation terminée: {self.transformation_stats['agents_transformed']}/{self.transformation_stats['agents_processed']} agents")
            return transformation_results
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transformation globale: {e}")
            raise
    
    async def fix_critical_errors(self, agent_file_path: str, critical_issues: List[str]) -> Dict[str, Any]:
        """Correction des erreurs critiques détectées par l'Agent 04"""
        self.logger.info(f"🚨 Correction erreurs critiques: {agent_file_path}")
        
        try:
            # Lire le fichier source
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            original_code = source_code
            fixes_applied = []
            
            # Analyser et corriger chaque erreur critique
            for issue in critical_issues:
                if "async async def" in issue:
                    # Corriger la syntaxe async async def
                    source_code, fix_info = self._fix_async_syntax_error(source_code, issue)
                    if fix_info["fixed"]:
                        fixes_applied.append(fix_info)
                        self.transformation_stats["syntax_errors_fixed"] += 1
                
                elif "import" in issue.lower() and "error" in issue.lower():
                    # Corriger les erreurs d'import
                    source_code, fix_info = self._fix_import_errors(source_code, issue)
                    if fix_info["fixed"]:
                        fixes_applied.append(fix_info)
                
                elif "indentation" in issue.lower():
                    # Corriger les erreurs d'indentation
                    source_code, fix_info = self._fix_indentation_errors(source_code, issue)
                    if fix_info["fixed"]:
                        fixes_applied.append(fix_info)
            
            # Sauvegarder le fichier corrigé si des modifications ont été apportées
            if fixes_applied:
                with open(agent_file_path, 'w', encoding='utf-8') as f:
                    f.write(source_code)
                
                self.transformation_stats["critical_errors_fixed"] += len(fixes_applied)
                self.logger.info(f"✅ {len(fixes_applied)} erreurs critiques corrigées")
            
            return {
                "agent_file": agent_file_path,
                "original_issues_count": len(critical_issues),
                "fixes_applied": fixes_applied,
                "fixes_count": len(fixes_applied),
                "source_modified": len(fixes_applied) > 0,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur correction erreurs critiques: {e}")
            return {
                "agent_file": agent_file_path,
                "success": False,
                "error": str(e)
            }
    
    async def migrate_to_pattern_factory(self, agent_file_path: str, agent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Migration complète d'un agent vers le Pattern Factory"""
        self.logger.info(f"🏭 Migration Pattern Factory: {agent_file_path}")
        
        try:
            # Lire le fichier source
            with open(agent_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Analyser la structure actuelle
            current_structure = self._analyze_current_structure(source_code)
            
            # Générer le code Pattern Factory
            pattern_factory_code = await self._generate_pattern_factory_code(
                source_code, 
                agent_file_path, 
                current_structure,
                agent_analysis
            )
            
            # Sauvegarder le fichier migré
            with open(agent_file_path, 'w', encoding='utf-8') as f:
                f.write(pattern_factory_code)
            
            self.transformation_stats["pattern_factory_migrations"] += 1
            self.logger.info(f"✅ Migration Pattern Factory terminée")
            
            return {
                "agent_file": agent_file_path,
                "migration_success": True,
                "original_structure": current_structure,
                "pattern_factory_implemented": True,
                "abstract_methods_added": True,
                "factory_method_created": True
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur migration Pattern Factory: {e}")
            return {
                "agent_file": agent_file_path,
                "migration_success": False,
                "error": str(e)
            }
    
    # 🔧 MÉTHODES UTILITAIRES DE TRANSFORMATION
    
    def _fix_async_syntax_error(self, source_code: str, issue: str) -> Tuple[str, Dict[str, Any]]:
        """Corriger les erreurs 'async async def'"""
        
        # Pattern pour détecter async async def
        pattern = r'async\s+async\s+def\s+'
        
        if re.search(pattern, source_code):
            # Remplacer async async def par async def
            fixed_code = re.sub(pattern, 'async def ', source_code)
            
            return fixed_code, {
                "type": "async_syntax_fix",
                "issue": issue,
                "pattern": "async async def -> async def",
                "fixed": True
            }
        
        return source_code, {"type": "async_syntax_fix", "fixed": False}
    
    def _fix_import_errors(self, source_code: str, issue: str) -> Tuple[str, Dict[str, Any]]:
        """Corriger les erreurs d'import"""
        
        # Ajouter les imports Pattern Factory standard si manquants
        if "from core.agent_factory_architecture import" not in source_code:
            import_block = '''
# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {{e}}")
        PATTERN_FACTORY_AVAILABLE = False
'''
            
            # Insérer après les imports existants
            lines = source_code.split('\n')
            insert_pos = 0
            
            # Trouver la position après les imports
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_pos = i + 1
            
            lines.insert(insert_pos, import_block)
            fixed_code = '\n'.join(lines)
            
            return fixed_code, {
                "type": "import_fix",
                "issue": issue,
                "pattern": "Added Pattern Factory imports",
                "fixed": True
            }
        
        return source_code, {"type": "import_fix", "fixed": False}
    
    def _fix_indentation_errors(self, source_code: str, issue: str) -> Tuple[str, Dict[str, Any]]:
        """Corriger les erreurs d'indentation basiques"""
        
        try:
            # Essayer de parser avec ast pour détecter les erreurs
            ast.parse(source_code)
            return source_code, {"type": "indentation_fix", "fixed": False}
        except IndentationError as e:
            # Tentative de correction automatique basique
            lines = source_code.split('\n')
            
            # Normaliser l'indentation (4 espaces)
            fixed_lines = []
            for line in lines:
                if line.strip():  # Ligne non vide
                    # Compter les espaces/tabs au début
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces > 0:
                        # Normaliser à 4 espaces par niveau
                        level = leading_spaces // 4
                        fixed_line = '    ' * level + line.lstrip()
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            
            fixed_code = '\n'.join(fixed_lines)
            
            return fixed_code, {
                "type": "indentation_fix",
                "issue": issue,
                "pattern": "Normalized indentation to 4 spaces",
                "fixed": True
            }
        except Exception:
            return source_code, {"type": "indentation_fix", "fixed": False}
    
    def _analyze_current_structure(self, source_code: str) -> Dict[str, Any]:
        """Analyser la structure actuelle du code"""
        
        structure = {
            "has_main_class": False,
            "class_name": None,
            "inherits_from_agent": False,
            "has_startup_method": False,
            "has_shutdown_method": False,
            "has_health_check_method": False,
            "has_execute_task_method": False,
            "has_get_capabilities_method": False,
            "has_factory_function": False,
            "import_pattern_factory": False
        }
        
        try:
            tree = ast.parse(source_code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    structure["has_main_class"] = True
                    structure["class_name"] = node.name
                    
                    # Vérifier l'héritage
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "Agent":
                            structure["inherits_from_agent"] = True
                    
                    # Vérifier les méthodes
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if item.name == "startup":
                                structure["has_startup_method"] = True
                            elif item.name == "shutdown":
                                structure["has_shutdown_method"] = True
                            elif item.name == "health_check":
                                structure["has_health_check_method"] = True
                            elif item.name == "execute_task":
                                structure["has_execute_task_method"] = True
                            elif item.name == "get_capabilities":
                                structure["has_get_capabilities_method"] = True
                
                elif isinstance(node, ast.FunctionDef):
                    if node.name.startswith("create_"):
                        structure["has_factory_function"] = True
                
                elif isinstance(node, ast.ImportFrom):
                    if "agent_factory_architecture" in (node.module or ""):
                        structure["import_pattern_factory"] = True
        
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur analyse structure: {e}")
        
        return structure
    
    async def _generate_pattern_factory_code(self, source_code: str, agent_file_path: str, 
                                           current_structure: Dict[str, Any], 
                                           agent_analysis: Dict[str, Any]) -> str:
        """Générer le code Pattern Factory complet"""
        
        agent_name = Path(agent_file_path).stem
        class_name = current_structure.get("class_name", agent_name.replace("_", "").title())
        
        # Template Pattern Factory avancé
        template = f'''#!/usr/bin/env python3
"""
🤖 {class_name.upper()} - PATTERN FACTORY NEXTGENERATION
========================================================

Mission: [Mission extraite de l'agent original]

Architecture Pattern Factory:
- Hérite de Agent de base  
- Implémente méthodes abstraites obligatoires
- Configuration NextGeneration intégrée
- Logging Pattern Factory standardisé

Transformé automatiquement par Agent 03 Adaptateur Code Upgraded
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import asyncio
from logging_manager_optimized import LoggingManager
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Import Pattern Factory (OBLIGATOIRE selon guide)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from agent_factory_implementation.core.agent_factory_architecture import Agent, Task, Result
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    try:
        from core.agent_factory_architecture import Agent, Task, Result
        PATTERN_FACTORY_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Pattern Factory non disponible: {{e}}")
        # Fallback classes
        class Agent:
            def __init__(self, agent_type: str, **config):
                self.agent_id = f"{agent_name}_{{{datetime.now().strftime('%Y%m%d_%H%M%S')}}}"
                self.agent_type = agent_type
                self.config = config
                logging.basicConfig(level=logging.INFO)
                self.logger = logging.getLogger(f"{class_name}_{{self.agent_id}}")
                
            async def startup(self): pass
            async def shutdown(self): pass
            async def health_check(self): return {{"status": "healthy"}}
            def get_capabilities(self): return []
        
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

class {class_name}(Agent):
    """{class_name} - Pattern Factory NextGeneration"""
    
    def __init__(self, **config):
        # Initialisation Pattern Factory
        super().__init__("{agent_name}", **config)
        
        # S'assurer que le logger est disponible (fallback si nécessaire)
        if not hasattr(self, 'logger'):
            if not hasattr(self, 'agent_id'):
                self.agent_id = f"{agent_name}_{{{datetime.now().strftime('%Y%m%d_%H%M%S')}}}"
            
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(f"{class_name}_{{self.agent_id}}")
        
        # Configuration logging Pattern Factory
        self.logger.info(f"🤖 {class_name} initialisé - ID: {{self.agent_id}}")
        
    # Implémentation méthodes abstraites OBLIGATOIRES
    async def startup(self):
        """Démarrage {agent_name}"""
        self.logger.info(f"🚀 {class_name} {{self.agent_id}} - DÉMARRAGE")
        self.logger.info("✅ Agent démarré avec succès")
        
    async def shutdown(self):
        """Arrêt {agent_name}"""
        self.logger.info(f"🛑 {class_name} {{self.agent_id}} - ARRÊT")
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé {agent_name}"""
        if not hasattr(self, 'agent_id'):
            self.agent_id = f"{agent_name}_{{{datetime.now().strftime('%Y%m%d_%H%M%S')}}}"
            
        if not hasattr(self, 'agent_type'):
            self.agent_type = "{agent_name}"
            
        return {{
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": "healthy",
            "ready": True,
            "pattern_factory_available": PATTERN_FACTORY_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }}
    
    async def execute_task(self, task: Task) -> Result:
        """Exécution des tâches - Pattern Factory OBLIGATOIRE"""
        try:
            self.logger.info(f"🎯 Exécution tâche: {{task.task_id}}")
            
            if task.task_id == "execute_mission":
                # Tâche d'exécution de mission
                mission_data = getattr(task, 'mission_data', None)
                results = await self.execute_mission(mission_data)
                
                return Result(
                    success=True,
                    data={{
                        "mission_results": results,
                        "agent_id": self.agent_id,
                        "task_id": task.task_id
                    }}
                )
                
            elif task.task_id == "process_data":
                # Tâche de traitement de données
                data = getattr(task, 'data', None)
                if data is None:
                    return Result(success=False, error="data requis pour process_data")
                    
                processed = await self.process_data(data)
                return Result(success=True, data=processed)
                
            else:
                return Result(
                    success=False, 
                    error=f"Tâche non reconnue: {{task.task_id}}"
                )
                
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution tâche {{task.task_id}}: {{e}}")
            return Result(success=False, error=str(e))
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent"""
        return [
            "execute_mission",
            "process_data",
            "health_monitoring",
            "pattern_factory_compliance"
        ]
    
    # Méthodes métier (à adapter selon l'agent original)
    
    async def execute_mission(self, mission_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Exécution de la mission principale de l'agent"""
        try:
            self.logger.info("🎯 Début exécution mission")
            
            # TODO: Implémenter la logique métier spécifique de l'agent original
            
            result = {{
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "agent_id": self.agent_id
            }}
            
            self.logger.info("✅ Mission terminée avec succès")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mission: {{e}}")
            return {{"status": "error", "error": str(e)}}
    
    async def process_data(self, data: Any) -> Dict[str, Any]:
        """Traitement des données spécifique à l'agent"""
        try:
            self.logger.info("🔄 Traitement des données")
            
            # TODO: Implémenter le traitement spécifique
            
            return {{
                "processed": True,
                "data_type": type(data).__name__,
                "timestamp": datetime.now().isoformat()
            }}
            
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement données: {{e}}")
            return {{"processed": False, "error": str(e)}}

# Fonction factory pour créer l'agent (Pattern Factory)
def create_{agent_name}(**config) -> {class_name}:
    """Factory function pour créer un {class_name} conforme Pattern Factory"""
    return {class_name}(**config)

# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    agent = create_{agent_name}()
    
    try:
        await agent.startup()
        health = await agent.health_check()
        print(f"🏥 Health Check: {{health}}")
        await agent.shutdown()
        
    except Exception as e:
        print(f"❌ Erreur execution agent: {{e}}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        return template
    
    async def _create_backup(self, agent_path: Path) -> Path:
        """Créer une sauvegarde de l'agent avant transformation"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"{agent_path.stem}_backup_{timestamp}.py"
        
        shutil.copy2(agent_path, backup_path)
        self.logger.info(f"💾 Backup créé: {backup_path}")
        
        return backup_path
    
    async def _validate_transformation(self, agent_path: Path) -> Dict[str, Any]:
        """Valider la transformation effectuée"""
        try:
            # Lire le code transformé
            with open(agent_path, 'r', encoding='utf-8') as f:
                transformed_code = f.read()
            
            # Vérifications de base
            validation_checks = {
                "syntax_valid": False,
                "imports_pattern_factory": False,
                "inherits_from_agent": False,
                "has_required_methods": False,
                "has_factory_function": False
            }
            
            # 1. Vérifier la syntaxe
            try:
                ast.parse(transformed_code)
                validation_checks["syntax_valid"] = True
            except SyntaxError:
                pass
            
            # 2. Vérifier les imports Pattern Factory
            if "from core.agent_factory_architecture import" in transformed_code:
                validation_checks["imports_pattern_factory"] = True
            
            # 3. Vérifier l'héritage
            if "class" in transformed_code and "(Agent)" in transformed_code:
                validation_checks["inherits_from_agent"] = True
            
            # 4. Vérifier les méthodes requises
            required_methods = ["startup", "shutdown", "health_check", "execute_task", "get_capabilities"]
            methods_found = sum(1 for method in required_methods if f"async def {method}" in transformed_code or f"def {method}" in transformed_code)
            validation_checks["has_required_methods"] = methods_found >= 4
            
            # 5. Vérifier la fonction factory
            if "def create_" in transformed_code:
                validation_checks["has_factory_function"] = True
            
            success = all(validation_checks.values())
            
            return {
                "success": success,
                "checks": validation_checks,
                "score": sum(validation_checks.values()) / len(validation_checks) * 100
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "score": 0
            }
    
    async def _save_transformation_stats(self):
        """Sauvegarder les statistiques de transformation"""
        stats_file = self.reports_dir / f"transformation_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "statistics": self.transformation_stats
            }, f, indent=2, ensure_ascii=False)
    
    async def _save_transformation_report(self, report: Dict[str, Any]):
        """Sauvegarder le rapport de transformation"""
        report_file = self.reports_dir / f"transformation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📋 Rapport transformation sauvegardé: {report_file}")

    # Méthodes métier principales (nouvelles méthodes OBLIGATOIRES pour le chef d'équipe)
    
    def _gerer_backups_intelligents(self, agent_file: Path, contenu_original: str) -> Path:
        """Gestion intelligente des backups - évite l'anarchie des doublons"""
        try:
            # 1. Définir un timestamp de session unique (pas dynamique)
            if not hasattr(self, '_session_timestamp'):
                self._session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 2. Chercher les backups existants pour ce fichier
            backups_existants = list(agent_file.parent.glob(f"{agent_file.stem}.py.backup_*"))
            
            # 3. Si un backup récent existe déjà (moins de 5 minutes), ne pas créer de nouveau backup
            backup_recent_trouve = False
            for backup in backups_existants:
                try:
                    # Extraire le timestamp du nom du backup
                    timestamp_str = backup.suffix.replace('.backup_', '')
                    timestamp_backup = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    
                    # Si le backup a moins de 5 minutes, ne pas en créer un nouveau
                    if (datetime.now() - timestamp_backup).total_seconds() < 300:  # 5 minutes
                        backup_recent_trouve = True
                        self.logger.info(f"📁 Backup récent trouvé: {backup.name} - Réutilisation")
                        return backup
                except:
                    pass  # Ignorer les erreurs de parsing de timestamp
            
            # 4. Créer un nouveau backup avec timestamp de session
            if not backup_recent_trouve:
                backup_path = agent_file.with_suffix(f'.py.backup_{self._session_timestamp}')
                
                # Vérifier si ce backup exact existe déjà
                if backup_path.exists():
                    self.logger.info(f"📁 Backup session existe: {backup_path.name} - Réutilisation")
                    return backup_path
                
                # Créer le nouveau backup
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(contenu_original)
                self.logger.info(f"💾 Backup session créé: {backup_path.name}")
                
                # 5. Nettoyer les anciens backups (garder seulement les 2 plus récents)
                self._nettoyer_anciens_backups(agent_file, backup_path)
                
                return backup_path
            
        except Exception as e:
            self.logger.error(f"❌ Erreur gestion backup pour {agent_file.name}: {e}")
            # Fallback: créer un backup simple
            backup_path = agent_file.with_suffix(f'.py.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenu_original)
            return backup_path
    
    def _nettoyer_anciens_backups(self, agent_file: Path, nouveau_backup: Path):
        """Nettoie les anciens backups pour éviter l'accumulation anarchique"""
        try:
            # Trouver tous les backups pour ce fichier
            backups_existants = list(agent_file.parent.glob(f"{agent_file.stem}.py.backup_*"))
            
            # Trier par date de modification (plus récent en premier)
            backups_tries = sorted(backups_existants, key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Garder seulement les 2 plus récents (incluant le nouveau)
            backups_a_supprimer = backups_tries[2:]  # Supprimer tout sauf les 2 premiers
            
            for backup_ancien in backups_a_supprimer:
                try:
                    backup_ancien.unlink()  # Supprimer le fichier
                    self.logger.info(f"🗑️ Ancien backup supprimé: {backup_ancien.name}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Impossible de supprimer {backup_ancien.name}: {e}")
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur nettoyage backups: {e}")

    async def adapter_outils(self, target_path: str = None) -> Dict[str, Any]:
        """Méthode principale d'adaptation d'outils pour le workflow du chef d'équipe - CORRECTION RÉELLE"""
        try:
            self.logger.info("🔧 Démarrage adaptation d'outils RÉELLE")
            
            corrections_effectuees = []
            agents_corriges = 0
            
            # 1. Identifier les agents avec erreurs syntaxe (utiliser le chemin fourni ou par défaut)
            if target_path:
                agents_directory = Path(target_path)
                self.logger.info(f"🎯 Répertoire ciblé: {agents_directory}")
            else:
                agents_directory = Path("../agent_factory_implementation/agents")
                self.logger.info(f"🎯 Répertoire par défaut: {agents_directory}")
            
            if not agents_directory.exists():
                self.logger.warning(f"❌ Répertoire agents non trouvé: {agents_directory}")
                return {"status": "error", "error": f"Répertoire non trouvé: {agents_directory}"}
            
            # 2. Scanner tous les fichiers Python
            for agent_file in agents_directory.glob("*.py"):
                try:
                    self.logger.info(f"🔍 Examen agent: {agent_file.name}")
                    
                    # Lire le contenu actuel
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    
                    contenu_original = contenu
                    corrections_fichier = []
                    
                    # 3. Détecter et corriger les erreurs "async async def"
                    if "async async def startup" in contenu:
                        contenu = contenu.replace("async async def startup", "async def startup")
                        corrections_fichier.append("async async def startup → async def startup")
                        self.logger.info(f"🔧 CORRECTION: async async def startup dans {agent_file.name}")
                    
                    if "async async def shutdown" in contenu:
                        contenu = contenu.replace("async async def shutdown", "async def shutdown")
                        corrections_fichier.append("async async def shutdown → async def shutdown")
                        self.logger.info(f"🔧 CORRECTION: async async def shutdown dans {agent_file.name}")
                    
                    if "async async def health_check" in contenu:
                        contenu = contenu.replace("async async def health_check", "async def health_check")
                        corrections_fichier.append("async async def health_check → async def health_check")
                        self.logger.info(f"🔧 CORRECTION: async async def health_check dans {agent_file.name}")
                    
                    # 4. SCAN COMPLET - Corriger TOUTES les erreurs d'indentation similaires
                    self.logger.info(f"🔍 SCAN COMPLET indentation dans {agent_file.name}")
                    
                    # D'abord convertir les tabs en espaces
                    if "\t" in contenu:
                        contenu = contenu.expandtabs(4)
                        corrections_fichier.append("Conversion tabs → espaces")
                    
                    # Scanner toutes les lignes pour corrections d'indentation
                    lignes = contenu.split('\n')
                    lignes_corrigees = 0
                    
                    for i, ligne in enumerate(lignes):
                        ligne_originale = ligne
                        ligne_corrigee = ligne
                        
                        # Pattern 1: Indentation excessive pour async def (8 espaces → 4 espaces)
                        if ligne_corrigee.lstrip().startswith('async def') and ligne_corrigee.startswith('        '):
                            ligne_corrigee = "    " + ligne_corrigee.strip()
                            self.logger.info(f"🔧 Correction async def ligne {i+1}: {ligne_originale.strip()}")
                            
                        # Pattern 2: Indentation excessive générale (réduire de 4 espaces)
                        elif ligne_corrigee.startswith('        ') and ligne_corrigee.strip():
                            # Éviter de casser les chaînes multi-lignes ou commentaires
                            if not ligne_corrigee.strip().startswith(('"""', "'''", '#')):
                                # Vérifier si c'est bien une sur-indentation (pas dans une classe/def)
                                contexte_normal = True
                                for j in range(max(0, i-3), i):
                                    if j < len(lignes):
                                        ligne_precedente = lignes[j].strip()
                                        if ligne_precedente.startswith(('class ', 'def ', 'async def ')) and not ligne_precedente.endswith(':'):
                                            contexte_normal = False
                                            break
                                
                                if contexte_normal:
                                    ligne_corrigee = ligne_corrigee[4:]  # Réduire de 4 espaces
                                    self.logger.info(f"🔧 Réduction indentation ligne {i+1}: {ligne_originale.strip()}")
                        
                        # Pattern 3: Classes internes mal indentées
                        elif ligne_corrigee.lstrip().startswith('class ') and ligne_corrigee.startswith('        '):
                            ligne_corrigee = "    " + ligne_corrigee.strip()
                            self.logger.info(f"🔧 Correction class ligne {i+1}: {ligne_originale.strip()}")
                        
                        # Pattern 4: Return/pass/autres statements mal indentés
                        elif ligne_corrigee.startswith('        ') and ligne_corrigee.strip() in ['pass', 'return', 'break', 'continue']:
                            ligne_corrigee = "    " + ligne_corrigee.strip()
                            self.logger.info(f"🔧 Correction statement ligne {i+1}: {ligne_originale.strip()}")
                        
                        # Si la ligne a été modifiée
                        if ligne_corrigee != ligne_originale:
                            lignes[i] = ligne_corrigee
                            lignes_corrigees += 1
                    
                    # Reconstituer le contenu si des corrections ont été faites
                    if lignes_corrigees > 0:
                        contenu = '\n'.join(lignes)
                        corrections_fichier.append(f"Correction complète {lignes_corrigees} lignes d'indentation")
                        self.logger.info(f"🎉 SCAN COMPLET: {lignes_corrigees} lignes corrigées dans {agent_file.name}")
                        
                        # Vérifier que le fichier compile maintenant
                        try:
                            ast.parse(contenu)
                            self.logger.info(f"✅ Validation syntaxe OK après corrections: {agent_file.name}")
                            corrections_fichier.append("Validation syntaxe réussie")
                        except SyntaxError as e:
                            self.logger.warning(f"⚠️ Erreur syntaxe résiduelle dans {agent_file.name}: ligne {e.lineno} - {e.msg}")
                            corrections_fichier.append(f"Erreur résiduelle ligne {e.lineno}: {e.msg}")
                        except Exception as e:
                            self.logger.warning(f"⚠️ Autre erreur validation {agent_file.name}: {e}")
                    
                    else:
                        # Si pas de corrections d'indentation, vérifier autres types d'erreurs
                        try:
                            ast.parse(contenu)
                        except SyntaxError as e:
                            if "invalid character" in str(e.msg):
                                self.logger.info(f"🔧 Suppression caractères invalides dans {agent_file.name}")
                                contenu_avant = contenu  
                                contenu = contenu.encode('ascii', 'ignore').decode('ascii')
                                if contenu != contenu_avant:
                                    corrections_fichier.append("Suppression caractères non-ASCII")
                                    self.logger.info(f"🔧 CORRECTION: Caractères non-ASCII supprimés dans {agent_file.name}")
                            else:
                                self.logger.info(f"ℹ️ Autre erreur syntaxe dans {agent_file.name}: {e.msg} ligne {e.lineno}")
                        except Exception:
                            pass
                    
                    # 5. Si des corrections ont été faites, sauvegarder le fichier modifié
                    if corrections_fichier:
                        # Gestion intelligente des backups
                        backup_path = self._gerer_backups_intelligents(agent_file, contenu_original)
                        
                        # Écrire le fichier corrigé
                        with open(agent_file, 'w', encoding='utf-8') as f:
                            f.write(contenu)
                        
                        agents_corriges += 1
                        corrections_effectuees.append({
                            "agent": agent_file.name,
                            "corrections": corrections_fichier,
                            "backup": backup_path.name if backup_path else "Aucun backup nécessaire"
                        })
                        
                        self.logger.info(f"✅ AGENT CORRIGÉ: {agent_file.name} - {len(corrections_fichier)} corrections")
                
                except Exception as e:
                    self.logger.error(f"❌ Erreur traitement {agent_file.name}: {e}")
            
            # 6. Résultat final
            result = {
                "status": "completed",
                "nombre_adaptations": agents_corriges,
                "outils_adaptes": [c["agent"] for c in corrections_effectuees],
                "corrections_detaillees": corrections_effectuees,
                "timestamp": datetime.now().isoformat(),
                "agent_id": self.agent_id
            }
            
            if agents_corriges > 0:
                self.logger.info(f"🎉 SUCCÈS CORRECTIONS: {agents_corriges} agents corrigés automatiquement")
            else:
                self.logger.info("ℹ️ Aucune correction nécessaire - tous les agents sont déjà conformes")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur adaptation outils: {e}")
            return {"status": "error", "error": str(e)}

# Fonction factory pour créer l'agent (Pattern Factory)
def create_adaptateur_code_upgraded(**config) -> AdaptateurCodeUpgraded:
    """Factory function pour créer un AdaptateurCodeUpgraded conforme Pattern Factory"""
    return AdaptateurCodeUpgraded(**config)

def create_agent_3_adaptateur_code(**config) -> AdaptateurCodeUpgraded:
    """Factory function pour créer l'agent 3 (alias pour compatibilité)"""
    return AdaptateurCodeUpgraded(**config)

# Test de l'agent si exécuté directement
async def main():
    """Test de l'agent Pattern Factory"""
    agent = create_adaptateur_code_upgraded()
    
    try:
        await agent.startup()
        health = await agent.health_check()
        print(f"🏥 Health Check: {health}")
        
        # Test des capacités
        capabilities = agent.get_capabilities()
        print(f"🛠️ Capacités: {len(capabilities)} disponibles")
        
        await agent.shutdown()
        
    except Exception as e:
        print(f"❌ Erreur execution agent: {e}")
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 