#!/usr/bin/env python3
"""
🔍 Shadow Mode Inspector - Accès aux Agents en Mémoire
=====================================================

Script pour inspecter et accéder aux agents stockés en mémoire 
dans le ShadowModeValidator du projet NextGeneration.

Fonctionnalités:
- Liste des agents en shadow mode
- Statuts de migration détaillés
- Métriques de performance
- Historique des comparaisons
- Export des données pour analyse

Author: NextGeneration Team
Version: 1.0.0
"""

import asyncio
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add core to Python path - Ajusté pour le nouveau répertoire
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'agents'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ShadowModeInspector")

class ShadowModeInspector:
    """
    Inspecteur pour accéder aux agents en mode shadow
    """
    
    def __init__(self):
        self.inspector_id = f"shadow_inspector_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.shadow_validator: Optional[Any] = None
        self.inspection_results = {
            "inspector_id": self.inspector_id,
            "timestamp": datetime.now().isoformat(),
            "agents_discovered": {},
            "metrics": {},
            "recommendations": []
        }
    
    async def initialize_shadow_validator(self):
        """Initialise le ShadowModeValidator pour inspection"""
        
        print("🔍 Initialisation Shadow Mode Inspector")
        print("=" * 60)
        
        try:
            from core.services import (
                create_shadow_validator, ShadowModeConfig,
                create_llm_gateway, create_message_bus,
                GatewayConfig, MessageBusConfig
            )
            
            # Configuration minimale pour inspection
            shadow_config = ShadowModeConfig(
                similarity_threshold_activate=0.999,
                enable_auto_activation=False,
                comparison_sample_size=1
            )
            
            # Services légers pour inspection
            from core.services.llm_gateway_hybrid import LLMGatewayHybrid
            
            gateway_config = GatewayConfig()
            gateway_config.redis_url = None  # Mode inspection sans Redis
            
            llm_gateway = LLMGatewayHybrid(gateway_config)
            llm_gateway.metrics = {
                "requests_total": 0, "cache_hits": 0, "cache_misses": 0,
                "errors": 0, "avg_latency": 0.0
            }
            
            bus_config = MessageBusConfig()
            bus_config.default_backend = "memory"
            bus_config.enable_legacy_bridge = True
            
            message_bus = await create_message_bus(bus_config)
            
            # Créer le ShadowModeValidator
            self.shadow_validator = await create_shadow_validator(
                shadow_config, llm_gateway, message_bus, None
            )
            
            print("✅ ShadowModeValidator initialisé pour inspection")
            return True
            
        except Exception as e:
            print(f"❌ Erreur initialisation: {e}")
            logger.error(f"Initialization failed: {e}")
            return False
    
    async def discover_active_shadow_agents(self):
        """Découvre les agents actifs en mode shadow"""
        
        print("\n📋 Découverte des Agents Shadow Mode")
        print("-" * 50)
        
        if not self.shadow_validator:
            print("❌ ShadowModeValidator non initialisé")
            return
        
        try:
            # Accès direct aux registres en mémoire
            legacy_agents = getattr(self.shadow_validator, 'legacy_agents', {})
            modern_agents = getattr(self.shadow_validator, 'modern_agents', {})
            migration_status = getattr(self.shadow_validator, 'migration_status', {})
            
            print(f"📦 Agents Legacy en mémoire: {len(legacy_agents)}")
            print(f"🔬 Agents Modernes en mémoire: {len(modern_agents)}")
            print(f"📊 Statuts de migration: {len(migration_status)}")
            
            # Analyser chaque agent
            for agent_id in set(list(legacy_agents.keys()) + list(modern_agents.keys())):
                agent_info = await self._analyze_agent(agent_id)
                self.inspection_results["agents_discovered"][agent_id] = agent_info
                
                # Affichage détaillé
                print(f"\n🤖 Agent: {agent_id}")
                print(f"   Status: {agent_info['status']}")
                print(f"   Legacy: {'✅' if agent_info['has_legacy'] else '❌'}")
                print(f"   Modern: {'✅' if agent_info['has_modern'] else '❌'}")
                print(f"   Comparisons: {agent_info['comparisons_count']}")
                print(f"   Avg Similarity: {agent_info['avg_similarity']:.3f}")
                print(f"   Ready for Activation: {'✅' if agent_info['ready_for_activation'] else '❌'}")
            
            return len(legacy_agents) + len(modern_agents)
            
        except Exception as e:
            print(f"❌ Erreur découverte: {e}")
            logger.error(f"Discovery failed: {e}")
            return 0
    
    async def _analyze_agent(self, agent_id: str) -> Dict[str, Any]:
        """Analyse détaillée d'un agent"""
        
        try:
            # Accès aux registres
            legacy_agents = getattr(self.shadow_validator, 'legacy_agents', {})
            modern_agents = getattr(self.shadow_validator, 'modern_agents', {})
            migration_status = getattr(self.shadow_validator, 'migration_status', {})
            
            # Informations de base
            has_legacy = agent_id in legacy_agents
            has_modern = agent_id in modern_agents
            status = migration_status.get(agent_id, "unknown")
            
            # Statut détaillé via méthode officielle
            detailed_status = {}
            if hasattr(self.shadow_validator, 'get_agent_migration_status'):
                detailed_status = self.shadow_validator.get_agent_migration_status(agent_id)
            
            # Informations sur les instances
            legacy_info = {}
            modern_info = {}
            
            if has_legacy:
                legacy_instance = legacy_agents[agent_id]
                legacy_info = {
                    "class": type(legacy_instance).__name__,
                    "version": getattr(legacy_instance, 'version', 'unknown'),
                    "agent_type": getattr(legacy_instance, 'agent_type', 'unknown')
                }
            
            if has_modern:
                modern_instance = modern_agents[agent_id]
                modern_info = {
                    "class": type(modern_instance).__name__,
                    "version": getattr(modern_instance, 'version', 'unknown'),
                    "agent_type": getattr(modern_instance, 'agent_type', 'unknown'),
                    "migration_status": getattr(modern_instance, 'migration_status', 'unknown')
                }
            
            return {
                "agent_id": agent_id,
                "status": status,
                "has_legacy": has_legacy,
                "has_modern": has_modern,
                "legacy_info": legacy_info,
                "modern_info": modern_info,
                "comparisons_count": detailed_status.get('comparisons_count', 0),
                "avg_similarity": detailed_status.get('avg_similarity_score', 0.0),
                "ready_for_activation": detailed_status.get('ready_for_activation', False),
                "last_comparison": detailed_status.get('last_comparison'),
                "detailed_status": detailed_status
            }
            
        except Exception as e:
            logger.error(f"Agent analysis failed for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "status": "error",
                "error": str(e),
                "has_legacy": False,
                "has_modern": False
            }
    
    async def get_shadow_metrics(self):
        """Récupère les métriques globales du shadow mode"""
        
        print("\n📊 Métriques Shadow Mode")
        print("-" * 30)
        
        if not self.shadow_validator:
            print("❌ ShadowModeValidator non accessible")
            return
        
        try:
            # Métriques via méthode officielle
            if hasattr(self.shadow_validator, 'get_metrics'):
                metrics = self.shadow_validator.get_metrics()
                self.inspection_results["metrics"] = metrics
                
                print(f"📈 Comparaisons totales: {metrics.get('comparisons_total', 0)}")
                print(f"🎯 Taux de succès: {metrics.get('success_rate', 0):.1%}")
                print(f"🚀 Activations auto: {metrics.get('activations_auto', 0)}")
                print(f"👤 Activations manuelles: {metrics.get('activations_manual', 0)}")
                print(f"🔙 Rollbacks: {metrics.get('rollbacks', 0)}")
                print(f"📊 Score similarité moyen: {metrics.get('avg_similarity_score', 0):.3f}")
                print(f"⚡ Améliorations performance: {metrics.get('performance_improvements', 0)}")
                print(f"🔬 Agents en shadow: {metrics.get('agents_in_shadow', 0)}")
                print(f"✅ Agents activés: {metrics.get('agents_activated', 0)}")
                print(f"❌ Agents rollback: {metrics.get('agents_rolled_back', 0)}")
                
                return metrics
            else:
                print("⚠️ Méthode get_metrics non disponible")
                return {}
                
        except Exception as e:
            print(f"❌ Erreur métriques: {e}")
            logger.error(f"Metrics retrieval failed: {e}")
            return {}
    
    async def perform_health_check(self):
        """Effectue un health check du shadow mode"""
        
        print("\n🏥 Health Check Shadow Mode")
        print("-" * 35)
        
        if not self.shadow_validator:
            print("❌ ShadowModeValidator non accessible")
            return
        
        try:
            if hasattr(self.shadow_validator, 'health_check'):
                health = await self.shadow_validator.health_check()
                
                print(f"🟢 Status: {health.get('status', 'unknown')}")
                print(f"⏰ Timestamp: {health.get('timestamp', 'unknown')}")
                
                components = health.get('components', {})
                print(f"🔗 LLM Gateway: {components.get('llm_gateway', 'unknown')}")
                print(f"📡 Message Bus: {components.get('message_bus', 'unknown')}")
                print(f"💾 Context Store: {components.get('context_store', 'unknown')}")
                
                agents_health = health.get('agents', {})
                print(f"📦 Legacy registered: {agents_health.get('legacy_registered', 0)}")
                print(f"🔬 Modern registered: {agents_health.get('modern_registered', 0)}")
                print(f"🧪 In shadow testing: {agents_health.get('in_shadow_testing', 0)}")
                
                return health
            else:
                print("⚠️ Méthode health_check non disponible")
                return {}
                
        except Exception as e:
            print(f"❌ Erreur health check: {e}")
            logger.error(f"Health check failed: {e}")
            return {}
    
    async def export_inspection_results(self):
        """Exporte les résultats d'inspection"""
        
        print("\n💾 Export des Résultats")
        print("-" * 25)
        
        try:
            # Nom du fichier d'export
            export_file = f"shadow_mode_inspection_{self.inspector_id}.json"
            
            # Ajouter des recommandations
            self.inspection_results["recommendations"] = self._generate_recommendations()
            
            # Sauvegarder
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.inspection_results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Résultats exportés: {export_file}")
            print(f"📊 Agents découverts: {len(self.inspection_results['agents_discovered'])}")
            print(f"📈 Métriques: {len(self.inspection_results['metrics'])}")
            print(f"💡 Recommandations: {len(self.inspection_results['recommendations'])}")
            
            return export_file
            
        except Exception as e:
            print(f"❌ Erreur export: {e}")
            logger.error(f"Export failed: {e}")
            return None
    
    def _generate_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur l'inspection"""
        
        recommendations = []
        agents_count = len(self.inspection_results["agents_discovered"])
        metrics = self.inspection_results.get("metrics", {})
        
        if agents_count == 0:
            recommendations.append("🔍 Aucun agent shadow détecté - Vérifier le système de migration")
        elif agents_count < 10:
            recommendations.append(f"📈 {agents_count} agents en shadow - Envisager l'accélération des migrations")
        else:
            recommendations.append(f"🚀 {agents_count} agents en shadow - Système de migration actif")
        
        success_rate = metrics.get("success_rate", 0)
        if success_rate < 0.5:
            recommendations.append("⚠️ Taux de succès faible - Revoir les seuils de validation")
        elif success_rate > 0.8:
            recommendations.append("✅ Excellent taux de succès - Continuer la migration")
        
        agents_ready = sum(1 for agent in self.inspection_results["agents_discovered"].values() 
                          if agent.get("ready_for_activation", False))
        if agents_ready > 0:
            recommendations.append(f"🎯 {agents_ready} agents prêts pour activation - Planifier le déploiement")
        
        return recommendations

async def main():
    """Point d'entrée principal"""
    
    print("🔍 SHADOW MODE INSPECTOR - NextGeneration")
    print("=" * 60)
    print(f"Version: 1.0.0")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    inspector = ShadowModeInspector()
    
    try:
        # Phase 1: Initialisation
        if not await inspector.initialize_shadow_validator():
            print("❌ Échec initialisation - Arrêt de l'inspection")
            return
        
        # Phase 2: Découverte des agents
        agents_count = await inspector.discover_active_shadow_agents()
        
        # Phase 3: Métriques
        await inspector.get_shadow_metrics()
        
        # Phase 4: Health Check
        await inspector.perform_health_check()
        
        # Phase 5: Export
        export_file = await inspector.export_inspection_results()
        
        # Résumé final
        print(f"\n🎉 INSPECTION TERMINÉE")
        print("=" * 30)
        print(f"✅ Agents découverts: {agents_count}")
        print(f"💾 Export: {export_file}")
        print(f"🔍 Inspector ID: {inspector.inspector_id}")
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        logger.error(f"Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 