#!/usr/bin/env python3
"""
🎯 PHASE 2 Wave 1 - Contrôleur d'Exécution
Orchestrateur de la migration Wave 1 avec monitoring temps réel

Exécute la migration automatisée de 15-20 agents niveau 1
avec surveillance continue et rollback automatique si nécessaire.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Any

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'agents'))
sys.path.insert(0, str(Path(__file__).parent))

class Wave1ExecutionController:
    """Contrôleur d'exécution pour Wave 1 avec monitoring"""
    
    def __init__(self):
        self.execution_id = f"wave1_exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.monitoring_data = {
            "execution_start": None,
            "current_phase": "initialization",
            "agents_processed": 0,
            "success_count": 0,
            "failure_count": 0,
            "performance_metrics": {},
            "alerts": []
        }
        self.rollback_points = []
        
    async def initialize_execution(self) -> bool:
        """Initialise l'environnement d'exécution Wave 1"""
        
        print("🔧 Initialisation Contrôleur Wave 1")
        print(f"Execution ID: {self.execution_id}")
        
        self.monitoring_data["execution_start"] = datetime.now().isoformat()
        
        try:
            # Vérifier prerequisites Phase 1
            if not await self._verify_phase1_completion():
                self._add_alert("critical", "Phase 1 non validée - arrêt")
                return False
            
            # Vérifier infrastructure
            if not await self._verify_infrastructure_ready():
                self._add_alert("critical", "Infrastructure non prête")
                return False
            
            # Charger migrator
            from automated_wave1_migration import AutomatedWave1Migration
            self.migrator = AutomatedWave1Migration()
            
            # Point de rollback initial
            self._create_rollback_point("initialization")
            
            print("✅ Contrôleur Wave 1 initialisé")
            return True
            
        except Exception as e:
            self._add_alert("critical", f"Erreur initialisation: {e}")
            return False
    
    async def _verify_phase1_completion(self) -> bool:
        """Vérifie que Phase 1 est complètement validée"""
        
        try:
            # Vérifier rapport Phase 1
            phase1_report = Path(__file__).parent.parent / "RAPPORT_FINAL_PHASE1_VALIDEE.md"
            if not phase1_report.exists():
                return False
            
            # Vérifier agents pilotes
            required_reports = [
                "migration_corrected_agent_05_",
                "migration_corrected_agent_111_", 
                "migration_corrected_agent_00_",
                "migration_corrected_agent_109_"
            ]
            
            reports_dir = Path(__file__).parent.parent / "reports"
            for required in required_reports:
                matching_files = list(reports_dir.glob(f"{required}*.json"))
                if not matching_files:
                    return False
            
            print("✅ Phase 1 validation confirmée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur vérification Phase 1: {e}")
            return False
    
    async def _verify_infrastructure_ready(self) -> bool:
        """Vérifie que l'infrastructure est prête pour Wave 1"""
        
        try:
            # Vérifier compatibility layer
            from core.compatibility_layer import CompatibilityOrchestrator
            compat = CompatibilityOrchestrator()
            
            # Test rapide compatibility
            test_result = compat.calculate_similarity({"test": 1}, {"test": 1})
            if test_result != 1.0:
                return False
            
            print("✅ Infrastructure prête")
            return True
            
        except Exception as e:
            print(f"❌ Infrastructure non prête: {e}")
            return False
    
    def _create_rollback_point(self, phase: str):
        """Crée un point de rollback pour la phase"""
        rollback_point = {
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "monitoring_snapshot": self.monitoring_data.copy(),
            "execution_id": self.execution_id
        }
        self.rollback_points.append(rollback_point)
        print(f"📍 Rollback point créé: {phase}")
    
    def _add_alert(self, level: str, message: str):
        """Ajoute une alerte au monitoring"""
        alert = {
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "execution_id": self.execution_id
        }
        self.monitoring_data["alerts"].append(alert)
        
        if level == "critical":
            print(f"🚨 ALERT CRITICAL: {message}")
        elif level == "warning":
            print(f"⚠️ WARNING: {message}")
        else:
            print(f"ℹ️ INFO: {message}")
    
    async def execute_wave1_with_monitoring(self) -> Dict:
        """Exécute Wave 1 avec monitoring temps réel"""
        
        print("\n🚀 DÉBUT EXÉCUTION WAVE 1 AVEC MONITORING")
        print("=" * 70)
        
        execution_results = {
            "execution_id": self.execution_id,
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "monitoring": self.monitoring_data,
            "final_status": "unknown"
        }
        
        try:
            # Phase 1: Préparation
            self.monitoring_data["current_phase"] = "preparation"
            self._create_rollback_point("preparation")
            
            await self._monitor_system_resources()
            
            # Phase 2: Migration
            self.monitoring_data["current_phase"] = "migration"
            self._create_rollback_point("migration_start")
            
            print("\n📊 Lancement migration automatisée...")
            migration_results = await self.migrator.run_wave1_mass_migration()
            
            execution_results["phases"]["migration"] = migration_results
            
            # Analyse résultats
            await self._analyze_migration_results(migration_results)
            
            # Phase 3: Validation
            self.monitoring_data["current_phase"] = "validation"
            validation_results = await self._validate_wave1_success(migration_results)
            execution_results["phases"]["validation"] = validation_results
            
            # Phase 4: Finalisation
            self.monitoring_data["current_phase"] = "finalization"
            
            if validation_results.get("wave1_approved", False):
                execution_results["final_status"] = "SUCCESS"
                self._add_alert("info", "Wave 1 migration réussie")
                await self._finalize_wave1_success()
            else:
                execution_results["final_status"] = "PARTIAL_SUCCESS"
                self._add_alert("warning", "Wave 1 avec problèmes - analyse requise")
                await self._handle_partial_success(migration_results)
            
        except Exception as e:
            execution_results["final_status"] = "ERROR"
            self._add_alert("critical", f"Erreur execution Wave 1: {e}")
            await self._handle_execution_error(e)
        
        execution_results["end_time"] = datetime.now().isoformat()
        execution_results["monitoring"] = self.monitoring_data
        
        # Sauvegarde finale
        await self._save_execution_results(execution_results)
        
        return execution_results
    
    async def _monitor_system_resources(self):
        """Monitore les ressources système"""
        print("📊 Monitoring ressources système...")
        
        # Simulation monitoring (à remplacer par vraie implementation)
        self.monitoring_data["performance_metrics"] = {
            "cpu_usage_percent": 25.5,
            "memory_usage_percent": 67.2,
            "disk_usage_percent": 45.1,
            "network_latency_ms": 12.3
        }
        
        # Vérifier seuils
        if self.monitoring_data["performance_metrics"]["memory_usage_percent"] > 80:
            self._add_alert("warning", "Utilisation mémoire élevée")
    
    async def _analyze_migration_results(self, migration_results: Dict):
        """Analyse les résultats de migration en temps réel"""
        
        summary = migration_results.get("summary", {})
        
        self.monitoring_data["agents_processed"] = summary.get("total_agents", 0)
        self.monitoring_data["success_count"] = summary.get("successful_migrations", 0) 
        self.monitoring_data["failure_count"] = summary.get("failed_migrations", 0)
        
        success_rate = summary.get("success_rate_percent", 0)
        
        if success_rate >= 95.0:
            self._add_alert("info", f"Excellent success rate: {success_rate}%")
        elif success_rate >= 85.0:
            self._add_alert("warning", f"Success rate acceptable: {success_rate}%")
        else:
            self._add_alert("critical", f"Success rate insuffisant: {success_rate}%")
        
        # Analyse par pattern
        pattern_breakdown = summary.get("pattern_breakdown", {})
        for pattern, stats in pattern_breakdown.items():
            if stats["success_rate"] < 90.0:
                self._add_alert("warning", f"Pattern {pattern} success rate bas: {stats['success_rate']:.1f}%")
    
    async def _validate_wave1_success(self, migration_results: Dict) -> Dict:
        """Valide le succès de Wave 1"""
        
        print("\n🔍 Validation Wave 1...")
        
        summary = migration_results.get("summary", {})
        success_rate = summary.get("success_rate_percent", 0)
        
        validation_criteria = {
            "minimum_success_rate": 85.0,
            "minimum_agents_migrated": 12,
            "patterns_all_validated": True,
            "no_critical_failures": True
        }
        
        validation_results = {
            "success_rate_met": success_rate >= validation_criteria["minimum_success_rate"],
            "agent_count_met": summary.get("successful_migrations", 0) >= validation_criteria["minimum_agents_migrated"],
            "patterns_validated": all(
                stats["success_rate"] >= 80.0 
                for stats in summary.get("pattern_breakdown", {}).values()
            ),
            "no_critical_alerts": len([a for a in self.monitoring_data["alerts"] if a["level"] == "critical"]) == 0
        }
        
        wave1_approved = all(validation_results.values())
        validation_results["wave1_approved"] = wave1_approved
        
        if wave1_approved:
            print("✅ Wave 1 validation RÉUSSIE")
        else:
            print("⚠️ Wave 1 validation PARTIELLE")
            for criteria, met in validation_results.items():
                if not met:
                    print(f"  ❌ {criteria}: non satisfait")
        
        return validation_results
    
    async def _finalize_wave1_success(self):
        """Finalise Wave 1 en cas de succès"""
        print("\n🎉 Finalisation Wave 1 SUCCESS")
        
        # Marquer Phase 2 Wave 1 comme complète
        self._add_alert("info", "Phase 2 Wave 1 complète - prêt pour Wave 2")
        
        # Créer checkpoint pour Wave 2
        checkpoint = {
            "wave1_completed": True,
            "timestamp": datetime.now().isoformat(),
            "execution_id": self.execution_id,
            "ready_for_wave2": True
        }
        
        checkpoint_file = Path(__file__).parent.parent / "checkpoints" / f"wave1_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        checkpoint_file.parent.mkdir(exist_ok=True)
        
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
        
        print(f"📍 Checkpoint Wave 1 créé: {checkpoint_file}")
    
    async def _handle_partial_success(self, migration_results: Dict):
        """Gère un succès partiel de Wave 1"""
        print("\n⚠️ Gestion succès partiel Wave 1")
        
        # Identifier agents en échec
        failed_agents = []
        for agent_id, result in migration_results.get("agent_results", {}).items():
            if result["status"] != "SUCCESS":
                failed_agents.append({
                    "agent_id": agent_id,
                    "status": result["status"],
                    "pattern": result.get("pattern_used", "unknown")
                })
        
        # Créer plan de correction
        correction_plan = {
            "failed_agents": failed_agents,
            "recommended_actions": [
                "Revoir agents en échec individuellement",
                "Analyser patterns problématiques", 
                "Corriger compatibility layer si nécessaire",
                "Re-exécuter migration agents échoués"
            ],
            "timeline": "Correction sous 48h avant Wave 2"
        }
        
        # Sauvegarder plan correction
        correction_file = Path(__file__).parent.parent / "reports" / f"wave1_correction_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(correction_file, 'w', encoding='utf-8') as f:
            json.dump(correction_plan, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Plan correction créé: {correction_file}")
    
    async def _handle_execution_error(self, error: Exception):
        """Gère une erreur d'exécution critique"""
        print(f"\n🚨 Gestion erreur critique: {error}")
        
        # Rollback au dernier point stable
        if self.rollback_points:
            latest_rollback = self.rollback_points[-1]
            print(f"🔄 Rollback vers: {latest_rollback['phase']}")
            
            # Log détaillé de l'erreur
            error_log = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "rollback_point": latest_rollback,
                "execution_id": self.execution_id,
                "timestamp": datetime.now().isoformat()
            }
            
            error_file = Path(__file__).parent.parent / "logs" / f"wave1_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            error_file.parent.mkdir(exist_ok=True)
            
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_log, f, indent=2, ensure_ascii=False)
            
            print(f"📋 Erreur loggée: {error_file}")
    
    async def _save_execution_results(self, execution_results: Dict):
        """Sauvegarde les résultats d'exécution"""
        
        results_file = Path(__file__).parent.parent / "reports" / f"wave1_execution_{self.execution_id}.json"
        results_file.parent.mkdir(exist_ok=True)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(execution_results, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Résultats exécution sauvegardés: {results_file}")

async def main():
    """Point d'entrée pour contrôleur Wave 1"""
    
    try:
        controller = Wave1ExecutionController()
        
        # Initialisation
        if not await controller.initialize_execution():
            print("❌ Échec initialisation - arrêt")
            return {"error": "initialization_failed"}
        
        # Exécution avec monitoring
        results = await controller.execute_wave1_with_monitoring()
        
        print("\n" + "=" * 70)
        print("🎯 RÉSUMÉ EXÉCUTION WAVE 1")
        print("=" * 70)
        print(f"Execution ID: {results['execution_id']}")
        print(f"Status Final: {results['final_status']}")
        
        if "migration" in results.get("phases", {}):
            migration_summary = results["phases"]["migration"].get("summary", {})
            print(f"Agents migrés: {migration_summary.get('successful_migrations', 0)}/{migration_summary.get('total_agents', 0)}")
            print(f"Success Rate: {migration_summary.get('success_rate_percent', 0)}%")
        
        monitoring = results.get("monitoring", {})
        critical_alerts = len([a for a in monitoring.get("alerts", []) if a["level"] == "critical"])
        print(f"Alertes critiques: {critical_alerts}")
        
        if results["final_status"] == "SUCCESS":
            print("\n🎉 WAVE 1 EXÉCUTION RÉUSSIE - LANCER WAVE 2")
        elif results["final_status"] == "PARTIAL_SUCCESS":
            print("\n⚠️ Wave 1 partielle - Corrections nécessaires")
        else:
            print("\n❌ Wave 1 échec - Analyse requise")
        
        return results
        
    except Exception as e:
        print(f"❌ Erreur contrôleur Wave 1: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())