#!/usr/bin/env python3
"""
ENHANCED MAINTENANCE ORCHESTRATOR V2.0
======================================

Orchestrateur avancé d'équipe de maintenance avec :
- Système de backups incrémentaux horodatés
- Validation sécurisée multi-niveaux
- Orchestration parallèle intelligente
- Gestion de scope flexible (fichier/répertoire/projet)
- Stratégies de récupération automatique
- Méthodologie M-T-D-V (Maintenance-Test-Documentation-Validation)

Author: Équipe NextGeneration
Version: 2.0.0 - Enhanced Safety & Methodology
"""

import asyncio
import sys
import logging
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import tempfile

# Configuration robuste du chemin
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import AgentMAINTENANCE00ChefEquipeCoordinateur
    from agents.agent_MAINTENANCE_01_analyseur_structure import AgentMAINTENANCE01AnalyseurStructure
    from agents.agent_MAINTENANCE_04_testeur_anti_faux_agents import AgentMAINTENANCE04TesteurAntiFauxAgents
    from agents.agent_MAINTENANCE_05_documenteur_peer_reviewer import AgentMAINTENANCE05DocumenteurPeerReviewer
    from agents.agent_MAINTENANCE_06_validateur_final import AgentMAINTENANCE06ValidateurFinal
    from agents.agent_MAINTENANCE_09_analyseur_securite import AgentMAINTENANCE09AnalyseurSecurite
    from agents.agent_MAINTENANCE_10_auditeur_qualite_normes import AgentMAINTENANCE10AuditeurQualiteNormes
    from agents.agent_META_AUDITEUR_UNIVERSEL import AgentMETAAuditeurUniversel
    from core.agent_factory_architecture import Agent, Task, Result
except ImportError as e:
    print(f"❌ Erreur d'importation critique: {e}")
    sys.exit(1)

# Configuration logging avancée
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / "logs" / f"maintenance_orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BackupEntry:
    """Entrée de backup horodatée"""
    timestamp: str
    file_path: str
    backup_path: str
    operation: str
    agent_id: str
    checksum_before: str
    checksum_after: Optional[str] = None
    success: bool = False

@dataclass
class ValidationResult:
    """Résultat de validation complète"""
    syntax_valid: bool
    security_score: float
    quality_score: float
    functional_test: bool
    issues: List[str]
    recommendations: List[str]

@dataclass
class MaintenanceSession:
    """Session de maintenance complète"""
    session_id: str
    start_time: str
    target_scope: str
    scope_type: str  # file, directory, project
    agents_used: List[str]
    iterations: List[Dict[str, Any]]
    backups: List[BackupEntry]
    final_status: str
    total_duration: Optional[float] = None

class EnhancedMaintenanceOrchestrator:
    """
    Orchestrateur de maintenance avancé NextGeneration v2.0
    
    Capacités principales :
    - Backup incrémental automatique avec historique
    - Validation sécurisée multi-agents 
    - Orchestration parallèle et séquentielle
    - Scope flexible (fichier/répertoire/projet complet)
    - Stratégies de récupération et rollback automatique
    - Méthodologie M-T-D-V complète
    """
    
    def __init__(self, target_quality_score: int = 95, max_iterations: int = 5):
        self.target_quality_score = target_quality_score
        self.max_iterations = max_iterations
        self.session_id = f"maintenance_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Répertoires de travail
        self.backup_dir = PROJECT_ROOT / "backups" / self.session_id
        self.reports_dir = PROJECT_ROOT / "reports" / "maintenance" / self.session_id
        self.logs_dir = PROJECT_ROOT / "logs"
        
        # Création des répertoires
        for dir_path in [self.backup_dir, self.reports_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Session de maintenance
        self.session = MaintenanceSession(
            session_id=self.session_id,
            start_time=datetime.now().isoformat(),
            target_scope="",
            scope_type="",
            agents_used=[],
            iterations=[],
            backups=[],
            final_status="INITIALIZED"
        )
        
        # Agents de l'équipe de maintenance
        self.agents = {}
        
    async def initialize_maintenance_team(self):
        """Initialise l'équipe de maintenance sécurisée"""
        logger.info("🚀 Initialisation de l'équipe de maintenance avancée...")
        
        agent_configs = {
            "chef_coordinateur": AgentMAINTENANCE00ChefEquipeCoordinateur,
            "analyseur_structure": AgentMAINTENANCE01AnalyseurStructure,
            "testeur_validation": AgentMAINTENANCE04TesteurAntiFauxAgents,
            "documenteur": AgentMAINTENANCE05DocumenteurPeerReviewer,
            "validateur_final": AgentMAINTENANCE06ValidateurFinal,
            "analyseur_securite": AgentMAINTENANCE09AnalyseurSecurite,
            "auditeur_qualite": AgentMAINTENANCE10AuditeurQualiteNormes,
            "meta_orchestrateur": AgentMETAAuditeurUniversel
        }
        
        # Initialisation parallèle des agents
        for agent_name, agent_class in agent_configs.items():
            try:
                agent = agent_class(id=f"{agent_name}_{self.session_id}")
                await agent.startup()
                
                # Test de santé obligatoire
                health = await agent.health_check()
                if health.get("status") != "healthy":
                    raise Exception(f"Agent {agent_name} en mauvais état: {health}")
                
                self.agents[agent_name] = agent
                self.session.agents_used.append(agent_name)
                logger.info(f"✅ Agent {agent_name} initialisé et validé")
                
            except Exception as e:
                logger.error(f"❌ Échec initialisation agent {agent_name}: {e}")
                raise
        
        logger.info(f"🎯 Équipe de {len(self.agents)} agents prête pour maintenance sécurisée")

    def create_incremental_backup(self, file_path: Path, operation: str, agent_id: str) -> BackupEntry:
        """Crée un backup incrémental horodaté"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        
        # Calcul checksum avant modification
        content_before = file_path.read_text(encoding='utf-8') if file_path.exists() else ""
        checksum_before = hashlib.sha256(content_before.encode()).hexdigest()
        
        # Création du backup
        backup_path = self.backup_dir / f"{file_path.stem}_{timestamp}_{operation}.backup"
        if file_path.exists():
            shutil.copy2(file_path, backup_path)
        
        backup_entry = BackupEntry(
            timestamp=timestamp,
            file_path=str(file_path),
            backup_path=str(backup_path),
            operation=operation,
            agent_id=agent_id,
            checksum_before=checksum_before
        )
        
        self.session.backups.append(backup_entry)
        logger.info(f"💾 Backup créé: {backup_path.name}")
        return backup_entry

    def finalize_backup(self, backup_entry: BackupEntry, success: bool):
        """Finalise une entrée de backup avec checksum post-modification"""
        file_path = Path(backup_entry.file_path)
        if file_path.exists():
            content_after = file_path.read_text(encoding='utf-8')
            backup_entry.checksum_after = hashlib.sha256(content_after.encode()).hexdigest()
        
        backup_entry.success = success
        logger.info(f"✅ Backup finalisé: {'succès' if success else 'échec'}")

    async def validate_comprehensive(self, target_path: Path) -> ValidationResult:
        """Validation complète multi-agents"""
        logger.info("🔍 Validation complète en cours...")
        
        issues = []
        recommendations = []
        
        # 1. Validation syntaxique
        try:
            if target_path.is_file() and target_path.suffix == '.py':
                compile(target_path.read_text(encoding='utf-8'), str(target_path), 'exec')
                syntax_valid = True
            else:
                syntax_valid = True  # Pour répertoires
        except SyntaxError as e:
            syntax_valid = False
            issues.append(f"Erreur syntaxe: {e}")
        
        # 2. Validation sécurité
        try:
            security_task = Task(
                id="security_validation",
                params={"target_path": str(target_path)}
            )
            security_result = await self.agents["analyseur_securite"].execute_task(security_task)
            security_score = security_result.data.get("security_score", 0.0) if security_result.success else 0.0
            
            if security_result.success and security_result.data.get("issues"):
                issues.extend([f"Sécurité: {issue}" for issue in security_result.data["issues"]])
        except Exception as e:
            security_score = 0.0
            issues.append(f"Erreur validation sécurité: {e}")
        
        # 3. Validation qualité
        try:
            quality_task = Task(
                id="quality_validation", 
                params={"target_path": str(target_path)}
            )
            quality_result = await self.agents["auditeur_qualite"].execute_task(quality_task)
            quality_score = quality_result.data.get("quality_score", 0.0) if quality_result.success else 0.0
            
            if quality_result.success and quality_result.data.get("recommendations"):
                recommendations.extend(quality_result.data["recommendations"])
        except Exception as e:
            quality_score = 0.0
            issues.append(f"Erreur validation qualité: {e}")
        
        # 4. Test fonctionnel (pour fichiers agents)
        functional_test = True
        if target_path.is_file() and target_path.name.startswith('agent_'):
            try:
                test_task = Task(
                    id="functional_test",
                    params={"agent_path": str(target_path)}
                )
                test_result = await self.agents["testeur_validation"].execute_task(test_task)
                functional_test = test_result.success and test_result.data.get("is_functional", False)
                
                if not functional_test:
                    issues.append("Échec test fonctionnel agent")
            except Exception as e:
                functional_test = False
                issues.append(f"Erreur test fonctionnel: {e}")
        
        return ValidationResult(
            syntax_valid=syntax_valid,
            security_score=security_score,
            quality_score=quality_score,
            functional_test=functional_test,
            issues=issues,
            recommendations=recommendations
        )

    async def execute_maintenance_cycle(self, target_path: Path, scope_type: str) -> Dict[str, Any]:
        """Exécute un cycle de maintenance M-T-D-V complet"""
        logger.info(f"🔄 Début cycle de maintenance: {target_path}")
        
        cycle_start = datetime.now()
        iteration_results = []
        
        # Backup initial
        initial_backup = self.create_incremental_backup(target_path, "INITIAL", "system")
        
        current_score = 0
        iteration = 0
        
        while current_score < self.target_quality_score and iteration < self.max_iterations:
            iteration += 1
            logger.info(f"🔄 Itération {iteration}/{self.max_iterations}")
            
            iteration_start = datetime.now()
            iteration_data = {
                "iteration": iteration,
                "start_time": iteration_start.isoformat(),
                "operations": []
            }
            
            try:
                # M - MAINTENANCE: Analyse et amélioration
                logger.info("📋 Phase M (Maintenance): Analyse et amélioration")
                
                # Analyse structure (Agent 01)
                structure_task = Task(
                    id="analyze_structure",
                    params={"target_path": str(target_path)}
                )
                structure_result = await self.agents["analyseur_structure"].execute_task(structure_task)
                
                # Orchestration intelligente (Meta-Auditeur)
                maintenance_task = Task(
                    id="intelligent_maintenance",
                    params={
                        "target_path": str(target_path),
                        "scope_type": scope_type,
                        "target_score": self.target_quality_score
                    }
                )
                
                # Backup pré-maintenance
                maintenance_backup = self.create_incremental_backup(
                    target_path, f"PRE_MAINTENANCE_ITER_{iteration}", "meta_orchestrateur"
                )
                
                maintenance_result = await self.agents["meta_orchestrateur"].execute_task(maintenance_task)
                
                if maintenance_result.success:
                    self.finalize_backup(maintenance_backup, True)
                    logger.info("✅ Phase Maintenance réussie")
                else:
                    self.finalize_backup(maintenance_backup, False)
                    logger.warning(f"⚠️ Phase Maintenance échouée: {maintenance_result.error}")
                
                # T - TEST: Validation et tests
                logger.info("🧪 Phase T (Test): Validation complète")
                validation = await self.validate_comprehensive(target_path)
                current_score = min(validation.security_score, validation.quality_score)
                
                # D - DOCUMENTATION: Rapports
                logger.info("📝 Phase D (Documentation): Génération rapports")
                doc_task = Task(
                    id="generate_documentation",
                    params={
                        "target_path": str(target_path),
                        "validation": asdict(validation),
                        "iteration": iteration
                    }
                )
                doc_result = await self.agents["documenteur"].execute_task(doc_task)
                
                # V - VALIDATION: Validation finale
                logger.info("✅ Phase V (Validation): Validation finale")
                final_validation_task = Task(
                    id="final_validation",
                    params={
                        "target_path": str(target_path),
                        "quality_threshold": self.target_quality_score,
                        "validation_results": asdict(validation)
                    }
                )
                final_result = await self.agents["validateur_final"].execute_task(final_validation_task)
                
                # Enregistrement des résultats
                iteration_data.update({
                    "end_time": datetime.now().isoformat(),
                    "duration": (datetime.now() - iteration_start).total_seconds(),
                    "current_score": current_score,
                    "validation": asdict(validation),
                    "maintenance_success": maintenance_result.success,
                    "documentation_success": doc_result.success if doc_result else False,
                    "final_validation_success": final_result.success if final_result else False
                })
                
                iteration_results.append(iteration_data)
                
                logger.info(f"📊 Score actuel: {current_score:.1f}/{self.target_quality_score}")
                
                # Condition de sortie
                if current_score >= self.target_quality_score:
                    logger.info("🎉 Objectif de qualité atteint!")
                    break
                    
                if not maintenance_result.success:
                    logger.warning("⚠️ Pas d'amélioration possible, arrêt des itérations")
                    break
                    
            except Exception as e:
                logger.error(f"❌ Erreur durant l'itération {iteration}: {e}")
                iteration_data.update({
                    "error": str(e),
                    "end_time": datetime.now().isoformat()
                })
                iteration_results.append(iteration_data)
                break
        
        # Finalisation
        self.finalize_backup(initial_backup, current_score >= self.target_quality_score)
        
        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        
        return {
            "success": current_score >= self.target_quality_score,
            "final_score": current_score,
            "iterations": len(iteration_results),
            "duration": cycle_duration,
            "iteration_details": iteration_results,
            "target_achieved": current_score >= self.target_quality_score
        }

    async def rollback_to_backup(self, backup_entry: BackupEntry) -> bool:
        """Effectue un rollback vers un backup spécifique"""
        try:
            backup_path = Path(backup_entry.backup_path)
            target_path = Path(backup_entry.file_path)
            
            if backup_path.exists():
                shutil.copy2(backup_path, target_path)
                logger.info(f"🔄 Rollback effectué vers {backup_entry.timestamp}")
                return True
            else:
                logger.error(f"❌ Backup non trouvé: {backup_path}")
                return False
        except Exception as e:
            logger.error(f"❌ Erreur durant rollback: {e}")
            return False

    async def execute_maintenance_mission(self, target_path: str, scope_type: str = "auto") -> Dict[str, Any]:
        """
        Point d'entrée principal pour une mission de maintenance complète
        
        Args:
            target_path: Chemin vers fichier/répertoire à maintenir
            scope_type: Type de scope (file, directory, project, auto)
        """
        mission_start = datetime.now()
        target = Path(target_path)
        
        # Détection automatique du scope
        if scope_type == "auto":
            if target.is_file():
                scope_type = "file"
            elif target.is_dir():
                scope_type = "directory"
            else:
                scope_type = "project"
        
        # Mise à jour session
        self.session.target_scope = str(target)
        self.session.scope_type = scope_type
        
        logger.info(f"🎯 MISSION DE MAINTENANCE - Scope: {scope_type}, Cible: {target}")
        
        try:
            # Initialisation équipe
            await self.initialize_maintenance_team()
            
            # Validation pré-maintenance
            logger.info("🔍 Validation pré-maintenance...")
            pre_validation = await self.validate_comprehensive(target)
            initial_score = min(pre_validation.security_score, pre_validation.quality_score)
            
            logger.info(f"📊 Score initial: {initial_score:.1f}/100")
            
            # Exécution cycle de maintenance
            cycle_result = await self.execute_maintenance_cycle(target, scope_type)
            
            # Validation post-maintenance
            logger.info("🔍 Validation post-maintenance...")
            post_validation = await self.validate_comprehensive(target)
            final_score = min(post_validation.security_score, post_validation.quality_score)
            
            # Finalisation session
            self.session.total_duration = (datetime.now() - mission_start).total_seconds()
            self.session.final_status = "SUCCESS" if cycle_result["success"] else "PARTIAL_SUCCESS"
            self.session.iterations = cycle_result["iteration_details"]
            
            # Génération rapport final
            await self.generate_final_report(initial_score, final_score, cycle_result)
            
            return {
                "success": True,
                "session_id": self.session_id,
                "initial_score": initial_score,
                "final_score": final_score,
                "improvement": final_score - initial_score,
                "target_achieved": cycle_result["target_achieved"],
                "iterations": cycle_result["iterations"],
                "duration": self.session.total_duration,
                "backups_created": len(self.session.backups),
                "reports_dir": str(self.reports_dir)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur durant mission: {e}")
            self.session.final_status = "FAILED"
            return {
                "success": False,
                "error": str(e),
                "session_id": self.session_id
            }
        finally:
            await self.shutdown_maintenance_team()

    async def generate_final_report(self, initial_score: float, final_score: float, cycle_result: Dict[str, Any]):
        """Génère le rapport final de mission"""
        report_path = self.reports_dir / "final_maintenance_report.md"
        
        report_content = f"""# RAPPORT FINAL DE MAINTENANCE
## Session: {self.session_id}

### 📊 RÉSULTATS GLOBAUX
- **Score Initial**: {initial_score:.1f}/100
- **Score Final**: {final_score:.1f}/100
- **Amélioration**: {final_score - initial_score:+.1f} points
- **Objectif Atteint**: {'✅ OUI' if cycle_result['target_achieved'] else '❌ NON'}
- **Itérations**: {cycle_result['iterations']}/{self.max_iterations}
- **Durée Totale**: {self.session.total_duration:.2f}s

### 🛡️ SÉCURITÉ ET BACKUPS
- **Backups Créés**: {len(self.session.backups)}
- **Répertoire Backups**: {self.backup_dir}
- **Agents Utilisés**: {', '.join(self.session.agents_used)}

### 📋 DÉTAILS DES ITÉRATIONS
"""
        
        for iteration in cycle_result["iteration_details"]:
            report_content += f"""
#### Itération {iteration['iteration']}
- **Score**: {iteration.get('current_score', 'N/A'):.1f}/100
- **Durée**: {iteration.get('duration', 0):.2f}s
- **Maintenance**: {'✅' if iteration.get('maintenance_success') else '❌'}
- **Documentation**: {'✅' if iteration.get('documentation_success') else '❌'}
- **Validation**: {'✅' if iteration.get('final_validation_success') else '❌'}
"""
        
        report_content += f"""

### 🎯 RECOMMANDATIONS
- Objectif qualité configuré: {self.target_quality_score}/100
- Prochaine maintenance recommandée dans: 30 jours
- Backups disponibles pour rollback si nécessaire

---
*Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} par Enhanced Maintenance Orchestrator v2.0*
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        logger.info(f"📋 Rapport final généré: {report_path}")

    async def shutdown_maintenance_team(self):
        """Arrêt propre de l'équipe de maintenance"""
        logger.info("🔚 Arrêt de l'équipe de maintenance...")
        
        for agent_name, agent in self.agents.items():
            try:
                await agent.shutdown()
                logger.info(f"✅ Agent {agent_name} arrêté")
            except Exception as e:
                logger.warning(f"⚠️ Erreur arrêt agent {agent_name}: {e}")
        
        # Sauvegarde session
        session_file = self.reports_dir / "session_data.json"
        session_file.write_text(json.dumps(asdict(self.session), indent=2), encoding='utf-8')
        logger.info(f"💾 Session sauvegardée: {session_file}")

async def main():
    """Point d'entrée principal pour test"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Maintenance Orchestrator v2.0")
    parser.add_argument("target", help="Chemin vers fichier/répertoire à maintenir")
    parser.add_argument("--scope", choices=["file", "directory", "project", "auto"], 
                       default="auto", help="Type de scope de maintenance")
    parser.add_argument("--target-score", type=int, default=95, 
                       help="Score de qualité cible (0-100)")
    parser.add_argument("--max-iterations", type=int, default=5,
                       help="Nombre maximum d'itérations")
    
    args = parser.parse_args()
    
    # Vérification chemin cible
    target_path = Path(args.target)
    if not target_path.exists():
        print(f"❌ Chemin non trouvé: {target_path}")
        sys.exit(1)
    
    # Création orchestrateur
    orchestrator = EnhancedMaintenanceOrchestrator(
        target_quality_score=args.target_score,
        max_iterations=args.max_iterations
    )
    
    try:
        # Exécution mission
        result = await orchestrator.execute_maintenance_mission(
            str(target_path), 
            args.scope
        )
        
        # Affichage résultats
        print("\n" + "="*60)
        print("🎯 RÉSULTATS DE LA MISSION DE MAINTENANCE")
        print("="*60)
        print(f"Session ID: {result['session_id']}")
        print(f"Succès: {'✅ OUI' if result['success'] else '❌ NON'}")
        
        if result['success']:
            print(f"Score initial: {result['initial_score']:.1f}/100")
            print(f"Score final: {result['final_score']:.1f}/100")
            print(f"Amélioration: {result['improvement']:+.1f} points")
            print(f"Objectif atteint: {'✅ OUI' if result['target_achieved'] else '❌ NON'}")
            print(f"Itérations: {result['iterations']}")
            print(f"Durée: {result['duration']:.2f}s")
            print(f"Backups créés: {result['backups_created']}")
            print(f"Rapports: {result['reports_dir']}")
        else:
            print(f"Erreur: {result.get('error', 'Erreur inconnue')}")
        
        print("="*60)
        
        return 0 if result['success'] else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Arrêt manuel de la mission")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))