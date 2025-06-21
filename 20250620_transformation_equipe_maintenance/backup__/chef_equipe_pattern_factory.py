#!/usr/bin/env python3
"""
🎖️ Chef d'Équipe Pattern Factory - NextGeneration Maintenance
Mission: Orchestration d'équipe via Pattern Factory
Architecture: Pattern Factory NextGeneration

Fonctionnalités:
- Création d'agents via TemplateManager
- Orchestration complète selon Pattern Factory
- Workflows standardisés
- Monitoring et métriques avancées
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

from maintenance_template_manager import (
    create_maintenance_template_manager, 
    MaintenanceTemplateManager,
    MaintenanceFactoryConfig
)

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ChefEquipePatternFactory:
    """Chef d'Équipe utilisant le Pattern Factory pour orchestrer l'équipe de maintenance"""
    
    def __init__(self, agent_id: str = None, agent_type: str = "pattern_factory_coordinator", target_path: str = None, workspace_path: str = None, **config):
        # Configuration TemplateManager
        self.agent_id = agent_id or f"chef_pattern_factory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agent_type = agent_type
        self.config = config
        # Compatibilité avec l'ancien nom
        self.chef_id = self.agent_id
        self.chef_type = self.agent_type
        # LoggingManager NextGeneration - Core System
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "ChefEquipePatternFactory",
            "log_level": "INFO",
            "elasticsearch_enabled": True,
            "encryption_enabled": True,
            "async_enabled": True,
            "audit_enabled": True,
            "high_throughput": True
        })
        
        # Configuration
        self.target_path = Path(target_path) if target_path else Path("../agent_factory_implementation/agents")
        self.workspace_path = Path(workspace_path) if workspace_path else Path(".")
        self.reports_path = self.workspace_path / "reports"
        
        # Template Manager
        factory_config = MaintenanceFactoryConfig(
            templates_dir=str(self.workspace_path / "templates" / "maintenance"),
            cache_ttl=config.get("cache_ttl", 3600),
            enable_hot_reload=config.get("hot_reload", True),
            max_cache_size=config.get("max_cache", 50)
        )
        self.template_manager = MaintenanceTemplateManager(factory_config)
        
        # Équipe d'agents (créés via factory)
        self.equipe_agents: Dict[str, Any] = {}
        self.agent_templates = [
            "agent_1_analyseur_structure",
            "agent_2_evaluateur_utilite", 
            "agent_3_adaptateur_code",
            "agent_4_testeur_integration",
            "agent_5_documenteur",
            "agent_6_validateur_final"
        ]
        
        # Configuration workflows
        self.config_workflows = {
            "timeout_default": config.get("timeout", 300),
            "safe_mode": config.get("safe_mode", True),
            "max_agents_parallel": config.get("max_agents_parallel", 6),
            "rapport_detaille": config.get("rapport_detaille", True),
            "enable_validation": config.get("enable_validation", True)
        }
        
        # Métriques Pattern Factory
        self.metrics = {
            "agents_created_via_factory": 0,
            "templates_loaded": 0,
            "workflows_executed": 0,
            "factory_cache_hits": 0,
            "total_execution_time": 0.0
        }
        
        self.logger.info(f"🎖️ Chef d'Équipe Pattern Factory initialisé - ID: {self.chef_id}")
        
    async def execute_task(self, task_config: Dict = None) -> Dict[str, Any]:
        """Exécuter la tâche principale - Interface TemplateManager"""
        return await self.workflow_maintenance_pattern_factory()
        
    async def startup(self):
        """Démarrage Chef d'Équipe Pattern Factory"""
        self.logger.info(f"🚀 Chef d'Équipe Pattern Factory {self.chef_id} - DÉMARRAGE")
        
        # Démarrer le Template Manager
        await self.template_manager.startup()
        
        # Vérifier les templates disponibles
        templates_disponibles = self.template_manager.list_templates()
        self.metrics["templates_loaded"] = len(templates_disponibles)
        
        self.logger.info(f"📋 Templates chargés: {templates_disponibles}")
        self.logger.info(f"🎯 Configuration: {self.config_workflows}")
        
        # Créer le répertoire de rapports
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("✅ Chef d'Équipe Pattern Factory prêt")
        return {"status": "started", "agent_id": self.agent_id}
        
    async def shutdown(self):
        """Arrêt Chef d'Équipe Pattern Factory"""
        self.logger.info(f"🛑 Chef d'Équipe Pattern Factory {self.chef_id} - ARRÊT")
        
        # Arrêter tous les agents créés
        for nom_agent, agent in self.equipe_agents.items():
            try:
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
                self.logger.info(f"✅ Agent {nom_agent} arrêté proprement")
            except Exception as e:
                self.logger.error(f"❌ Erreur arrêt agent {nom_agent}: {e}")
        
        # Arrêter le Template Manager
        await self.template_manager.shutdown()
        
        self.equipe_agents.clear()
        return {"status": "stopped", "agent_id": self.agent_id}
        
    async def health_check(self) -> Dict[str, Any]:
        """Vérification santé chef équipe Pattern Factory"""
        template_manager_health = self.template_manager.health_check()
        
        health_status = {
            "chef_id": self.chef_id,
            "chef_type": self.chef_type,
            "status": "healthy",
            "pattern_factory": {
                "template_manager_status": template_manager_health["status"],
                "templates_loaded": template_manager_health["templates_loaded"],
                "cache_hit_rate": template_manager_health["metrics"]["cache_hit_rate"]
            },
            "agents_actifs": len(self.equipe_agents),
            "templates_disponibles": len(self.template_manager.list_templates()),
            "configuration": {
                "target_path": str(self.target_path),
                "workspace_path": str(self.workspace_path),
                "safe_mode": self.config_workflows["safe_mode"]
            },
            "metrics": self.metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"🏥 Health Check Pattern Factory: {health_status['status']}")
        return health_status
    
    async def workflow_maintenance_pattern_factory(self, config: Dict = None) -> Dict[str, Any]:
        """Workflow complet utilisant Pattern Factory pour créer et orchestrer l'équipe"""
        self.logger.info("🔄 WORKFLOW MAINTENANCE PATTERN FACTORY - Démarrage")
        
        workflow_start = datetime.now()
        resultats_workflow = {
            "workflow_id": f"pattern_factory_maintenance_{workflow_start.strftime('%Y%m%d_%H%M%S')}",
            "chef_id": self.chef_id,
            "pattern_factory": True,
            "target_path": str(self.target_path),
            "agents_creation_method": "template_factory",
            "etapes": {},
            "status": "en_cours",
            "resultats_consolides": {},
            "metrics_factory": {},
            "timestamp_debut": workflow_start.isoformat()
        }
        
        try:
            # Créer l'équipe via Pattern Factory
            self.logger.info("🏭 CRÉATION ÉQUIPE VIA PATTERN FACTORY")
            await self._creer_equipe_via_factory()
            
            # Étape 1: Analyse Structure via Factory
            self.logger.info("📊 ÉTAPE 1/6: Analyse Structure (Pattern Factory)")
            agent_1 = self.equipe_agents["agent_1_analyseur_structure"]
            resultat_1 = await agent_1.analyser_structure()
            
            resultats_workflow["etapes"]["etape_1_analyse"] = {
                "status": "complete",
                "method": "pattern_factory",
                "agent_template": "agent_1_analyseur_structure",
                "resultats": resultat_1,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 1 terminée via Pattern Factory")
            
            # Étape 2: Évaluation Utilité via Factory
            self.logger.info("🎯 ÉTAPE 2/6: Évaluation Utilité (Pattern Factory)")
            agent_2 = self.equipe_agents["agent_2_evaluateur_utilite"]
            # Configurer l'agent avec les résultats de l'étape 1
            agent_2.analyse_structure = resultat_1
            resultat_2 = await agent_2.evaluer_utilite()
            
            resultats_workflow["etapes"]["etape_2_evaluation"] = {
                "status": "complete",
                "method": "pattern_factory",
                "agent_template": "agent_2_evaluateur_utilite",
                "resultats": resultat_2,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 2 terminée via Pattern Factory")
            
            # Étape 3: Adaptation Code via Factory
            self.logger.info("🔧 ÉTAPE 3/6: Adaptation Code (Pattern Factory)")
            agent_3 = self.equipe_agents["agent_3_adaptateur_code"]
            # Configurer l'agent avec les outils sélectionnés
            outils_selectionnes = resultat_2.get("outils_utiles", [])
            agent_3.outils_selectionnes = outils_selectionnes
            agent_3.source_path = self.target_path
            agent_3.target_path = self.target_path / "adapted_tools"
            agent_3.workspace_path = self.workspace_path
            resultat_3 = await agent_3.adapter_outils()
            
            resultats_workflow["etapes"]["etape_3_adaptation"] = {
                "status": "complete", 
                "method": "pattern_factory",
                "agent_template": "agent_3_adaptateur_code",
                "resultats": resultat_3,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 3 terminée via Pattern Factory")
            
            # Étape 4: Tests Intégration via Factory
            self.logger.info("🧪 ÉTAPE 4/6: Tests Intégration (Pattern Factory)")
            agent_4 = self.equipe_agents["agent_4_testeur_integration"]
            # Configurer l'agent avec les outils adaptés
            outils_adaptes = resultat_3.get("outils_adaptes", [])
            agent_4.outils_adaptes = outils_adaptes
            agent_4.target_path = self.target_path / "adapted_tools"
            agent_4.workspace_path = self.workspace_path
            resultat_4 = await agent_4.tester_integration()
            
            resultats_workflow["etapes"]["etape_4_tests"] = {
                "status": "complete",
                "method": "pattern_factory", 
                "agent_template": "agent_4_testeur_integration",
                "resultats": resultat_4,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 4 terminée via Pattern Factory")
            
            # Étape 5: Documentation via Factory
            self.logger.info("📚 ÉTAPE 5/6: Documentation (Pattern Factory)")
            agent_5 = self.equipe_agents["agent_5_documenteur"]
            # Configurer l'agent avec les résultats des tests
            agent_5.resultats_tests = resultat_4
            agent_5.target_path = self.target_path
            agent_5.workspace_path = self.workspace_path
            resultat_5 = await agent_5.documenter_complete()
            
            resultats_workflow["etapes"]["etape_5_documentation"] = {
                "status": "complete",
                "method": "pattern_factory",
                "agent_template": "agent_5_documenteur", 
                "resultats": resultat_5,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 5 terminée via Pattern Factory")
            
            # Étape 6: Validation Finale via Factory
            self.logger.info("✅ ÉTAPE 6/6: Validation Finale (Pattern Factory)")
            agent_6 = self.equipe_agents["agent_6_validateur_final"]
            # Configurer l'agent avec tous les résultats
            resultats_equipe = {
                "analyse": resultat_1,
                "evaluation": resultat_2,
                "adaptation": resultat_3,
                "tests": resultat_4,
                "documentation": resultat_5
            }
            agent_6.resultats_equipe = resultats_equipe
            agent_6.target_path = str(self.target_path)
            agent_6.workspace_path = str(self.workspace_path)
            resultat_6 = await agent_6.valider_mission()
            
            resultats_workflow["etapes"]["etape_6_validation"] = {
                "status": "complete",
                "method": "pattern_factory",
                "agent_template": "agent_6_validateur_final",
                "resultats": resultat_6,
                "timestamp": datetime.now().isoformat()
            }
            self.logger.info("✅ ÉTAPE 6 terminée via Pattern Factory")
            
            # Consolidation finale avec métriques Pattern Factory
            workflow_end = datetime.now()
            duree_totale = (workflow_end - workflow_start).total_seconds()
            self.metrics["total_execution_time"] = duree_totale
            self.metrics["workflows_executed"] += 1
            
            # Métriques du Template Manager
            template_metrics = self.template_manager.get_metrics()
            self.metrics["factory_cache_hits"] = template_metrics["cache_hits"]
            
            resultats_workflow.update({
                "status": "complete",
                "timestamp_fin": workflow_end.isoformat(),
                "duree_totale_sec": duree_totale,
                "pattern_factory_success": True,
                "resultats_consolides": {
                    "agents_analyses": resultat_1.get("tools_count", 0),
                    "agents_valides": len(resultat_2.get("outils_utiles", [])),
                    "adaptations_realisees": resultat_3.get("tools_adapted", 0),
                    "tests_executes": resultat_4.get("tests_passed", 0),
                    "documents_generes": resultat_5.get("nombre_documents", 0),
                    "score_final": resultat_6.get("mission_validation", {}).get("quality_score", 0)
                },
                "metrics_factory": {
                    "agents_created_via_templates": self.metrics["agents_created_via_factory"],
                    "templates_utilises": len(self.agent_templates),
                    "cache_hit_rate": template_metrics.get("cache_hit_rate", 0),
                    "factory_performance": "optimal" if template_metrics.get("cache_hit_rate", 0) > 0.8 else "good"
                },
                "recommandations_pattern_factory": self._generer_recommandations_pattern_factory(resultats_workflow),
                "actions_suivantes": self._generer_actions_pattern_factory(resultats_workflow)
            })
            
            # Sauvegarde rapport final Pattern Factory
            await self._sauvegarder_rapport_pattern_factory(resultats_workflow)
            
            self.logger.info(f"🎉 WORKFLOW PATTERN FACTORY TERMINÉ en {duree_totale:.1f}s")
            return resultats_workflow
            
        except Exception as e:
            self.logger.error(f"❌ Erreur workflow Pattern Factory: {e}")
            resultats_workflow.update({
                "status": "erreur",
                "pattern_factory_error": str(e),
                "timestamp_erreur": datetime.now().isoformat()
            })
            return resultats_workflow
    
    async def _creer_equipe_via_factory(self):
        """Créer l'équipe d'agents via Pattern Factory"""
        self.logger.info("🏭 Création d'équipe via Template Factory")
        
        # Spécifications des agents à créer
        agent_specs = []
        for template_name in self.agent_templates:
            agent_specs.append({
                "template": template_name,
                "suffix": "factory",
                "config": {
                    "target_path": str(self.target_path),
                    "workspace_path": str(self.workspace_path),
                    "created_via_factory": True
                }
            })
        
        # Créer les agents en lot via factory
        try:
            agents_crees = await self.template_manager.bulk_create_agents(agent_specs)
            
            # Organiser les agents par nom
            for i, agent in enumerate(agents_crees):
                template_name = self.agent_templates[i]
                self.equipe_agents[template_name] = agent
                self.metrics["agents_created_via_factory"] += 1
                self.logger.info(f"✅ Agent créé via factory: {template_name}")
            
            self.logger.info(f"🎉 Équipe Pattern Factory créée: {len(agents_crees)} agents")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création équipe via factory: {e}")
            raise
    
    def _generer_recommandations_pattern_factory(self, workflow_result: Dict) -> List[str]:
        """Générer des recommandations spécifiques au Pattern Factory"""
        recommandations = []
        
        try:
            metrics_factory = workflow_result.get("metrics_factory", {})
            
            # Recommandations sur la performance du Pattern Factory
            cache_hit_rate = metrics_factory.get("cache_hit_rate", 0)
            if cache_hit_rate < 0.8:
                recommandations.append("🚀 Optimiser le cache des templates pour améliorer les performances")
            else:
                recommandations.append("✅ Pattern Factory optimisé - Excellent taux de cache")
            
            # Recommandations sur l'utilisation des templates
            agents_created = metrics_factory.get("agents_created_via_templates", 0)
            if agents_created == len(self.agent_templates):
                recommandations.append("🏭 Pattern Factory utilisé de manière optimale pour tous les agents")
            else:
                recommandations.append("⚠️ Certains agents non créés via Pattern Factory - Standardiser")
            
            # Recommandations générales
            recommandations.extend([
                "📋 Maintenir les templates JSON à jour avec les évolutions des agents",
                "🔄 Utiliser systématiquement le Pattern Factory pour toutes les créations d'agents",
                "📊 Surveiller les métriques de performance du TemplateManager"
            ])
            
        except Exception as e:
            recommandations.append(f"⚠️ Erreur génération recommandations Pattern Factory: {e}")
        
        return recommandations
    
    def _generer_actions_pattern_factory(self, workflow_result: Dict) -> List[str]:
        """Générer des actions spécifiques au Pattern Factory"""
        actions = []
        
        try:
            resultats = workflow_result.get("resultats_consolides", {})
            score_final = resultats.get("score_final", 0)
            
            if score_final >= 90:
                actions.extend([
                    "🎯 Pattern Factory validé - Déployer sur d'autres équipes",
                    "📚 Documenter les meilleures pratiques Pattern Factory identifiées",
                    "🏭 Créer des templates additionnels pour nouvelles spécialisations"
                ])
            elif score_final >= 70:
                actions.extend([
                    "🔧 Affiner les templates JSON selon les retours d'expérience",
                    "🧪 Tester l'extension du Pattern Factory à d'autres domaines",
                    "📊 Optimiser les performances du TemplateManager"
                ])
            else:
                actions.extend([
                    "⚠️ Réviser la stratégie Pattern Factory",
                    "🔍 Analyser les échecs de création via factory",
                    "🛠️ Corriger les templates défaillants"
                ])
            
        except Exception as e:
            actions.append(f"⚠️ Erreur génération actions Pattern Factory: {e}")
        
        return actions
    
    async def _sauvegarder_rapport_pattern_factory(self, workflow_result: Dict):
        """Sauvegarder le rapport spécialisé Pattern Factory"""
        try:
            rapport_path = self.reports_path / f"pattern_factory_maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(rapport_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_result, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"💾 Rapport Pattern Factory sauvegardé: {rapport_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde rapport Pattern Factory: {e}")

# Factory function pour compatibilité TemplateManager
def create_chefEquipePatternFactory(**config):
    """Factory function pour créer l'agent"""
    return ChefEquipePatternFactory(**config)

# Fonction factory pour compatibilité
def create_chef_equipe_pattern_factory(target_path: str = None, workspace_path: str = None, **config):
    """Factory pour créer un Chef d'Équipe Pattern Factory"""
    return ChefEquipePatternFactory(target_path=target_path, workspace_path=workspace_path, **config)

# Point d'entrée direct
async def main():
    """Point d'entrée principal Chef d'Équipe Pattern Factory"""
    print("🎖️ CHEF D'ÉQUIPE PATTERN FACTORY")
    print("=" * 60)
    
    try:
        # Création et exécution
        chef_equipe = create_chef_equipe_pattern_factory()
        await chef_equipe.startup()
        
        # Health check
        health = await chef_equipe.health_check()
        print(f"🏥 Statut Pattern Factory: {health['status']}")
        print(f"📋 Templates chargés: {health['pattern_factory']['templates_loaded']}")
        
        await chef_equipe.shutdown()
        print("✅ Chef d'équipe Pattern Factory prêt")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result) 