#!/usr/bin/env python3
"""
🚀 TEST WORKFLOW COMPLET - ÉQUIPE DE MAINTENANCE
================================================================================
Test du workflow de coordination complète avec le Chef d'Équipe orchestrant
tous les agents de maintenance dans un scénario réel.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import traceback

# Golden Source Logging
from core import logging_manager

# Configuration des logs
logger = logging_manager.get_logger('custom_workflow_test', custom_config={
    "logger_name": "test_workflow_complet_equipe",
    "log_level": "DEBUG",
    "async_enabled": False, # Tests synchrones pour la simplicité du log
})

# Import des agents
sys.path.insert(0, str(Path(__file__).parent))
from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur

async def test_workflow_complet():
    """Test du workflow complet de l'équipe de maintenance"""
    logger.info("🚀 TEST WORKFLOW COMPLET - ÉQUIPE DE MAINTENANCE")
    logger.info("=" * 80)
    logger.info(f"📅 Timestamp: {datetime.now().isoformat()}")
    logger.info("🎯 Objectif: Tester coordination complète sur mission réelle")
    
    # Configuration de la mission test
    mission_test = {
        "type": "maintenance_complete",
        "source_directory": "./tools",  # Répertoire à analyser
        "target_agents": ["01", "02", "03", "04", "05", "06"],  # Tous les agents
        "coordination_mode": "sequential",  # Mode de coordination
        "reporting": True,
        "validation": True
    }
    
    resultats = {
        "workflow_id": f"workflow_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp_debut": datetime.now().isoformat(),
        "mission": mission_test,
        "etapes": {},
        "status": "en_cours",
        "erreurs": []
    }
    
    try:
        logger.info("🎖️ ÉTAPE 1: CRÉATION DU CHEF D'ÉQUIPE COORDINATEUR")
        logger.info("-" * 60)
        
        # Création du chef d'équipe
        chef_equipe = create_agent_0_chef_equipe_coordinateur(
            target_path="./tools",
            workspace_path=".",
            safe_mode=True
        )
        
        logger.info("✅ Chef d'équipe créé et opérationnel")
        resultats["etapes"]["creation_chef"] = {"status": "success", "timestamp": datetime.now().isoformat()}
        
        logger.info("🎖️ ÉTAPE 2: DÉMARRAGE CHEF D'ÉQUIPE")
        logger.info("-" * 60)
        
        # Démarrage du chef d'équipe
        await chef_equipe.startup()
        logger.info("✅ Chef d'équipe démarré")
        
        # Vérification santé
        health = await chef_equipe.health_check()
        logger.info(f"🏥 Health Check: {health}")
        resultats["etapes"]["startup_chef"] = {"status": "success", "health": health, "timestamp": datetime.now().isoformat()}
        
        logger.info("🎖️ ÉTAPE 3: MONITORING ÉQUIPE TEMPS RÉEL")
        logger.info("-" * 60)
        
        # Test monitoring temps réel
        if hasattr(chef_equipe, 'real_time_team_monitoring'):
            monitoring = await chef_equipe.real_time_team_monitoring()
            logger.info(f"📊 Monitoring actif: {monitoring}")
            resultats["etapes"]["monitoring"] = {"status": "success", "data": monitoring, "timestamp": datetime.now().isoformat()}
        else:
            logger.warning("⚠️ Monitoring temps réel non disponible")
            resultats["etapes"]["monitoring"] = {"status": "not_available", "timestamp": datetime.now().isoformat()}
            
        logger.info("🎖️ ÉTAPE 4: COORDINATION AVANCÉE DE L'ÉQUIPE")
        logger.info("-" * 60)
        
        # Coordination avancée
        if hasattr(chef_equipe, 'coordinate_team_advanced'):
            logger.info("🚀 Lancement coordination avancée...")
            coordination = await chef_equipe.coordinate_team_advanced()
            logger.info(f"✅ Coordination terminée: {coordination}")
            resultats["etapes"]["coordination_avancee"] = {"status": "success", "resultat": coordination, "timestamp": datetime.now().isoformat()}
        else:
            logger.warning("⚠️ Coordination avancée non disponible, utilisation workflow standard...")
            coordination = await chef_equipe.workflow_maintenance_complete()
            logger.info(f"✅ Workflow maintenance terminé: {coordination}")
            resultats["etapes"]["coordination_standard"] = {"status": "success", "resultat": coordination, "timestamp": datetime.now().isoformat()}
        
        logger.info("🎖️ ÉTAPE 5: ANALYTICS PRÉDICTIFS DE L'ÉQUIPE")
        logger.info("-" * 60)
        
        # Analytics prédictifs
        if hasattr(chef_equipe, 'predictive_team_analytics'):
            analytics = await chef_equipe.predictive_team_analytics()
            logger.info(f"📈 Analytics: {analytics}")
            resultats["etapes"]["analytics"] = {"status": "success", "data": analytics, "timestamp": datetime.now().isoformat()}
        else:
            logger.warning("⚠️ Analytics prédictifs non disponibles")
            resultats["etapes"]["analytics"] = {"status": "not_available", "timestamp": datetime.now().isoformat()}
        
        logger.info("🎖️ ÉTAPE 6: ARRÊT PROPRE DU CHEF D'ÉQUIPE")
        logger.info("-" * 60)
        
        # Arrêt propre
        await chef_equipe.shutdown()
        logger.info("✅ Chef d'équipe arrêté proprement")
        resultats["etapes"]["shutdown"] = {"status": "success", "timestamp": datetime.now().isoformat()}
        
        # Finalisation
        resultats["status"] = "success"
        resultats["timestamp_fin"] = datetime.now().isoformat()
        
        logger.info("🎉 WORKFLOW COMPLET RÉUSSI!")
        logger.info("=" * 80)
        
        return resultats
        
    except Exception as e:
        logger.critical(f"❌ Erreur workflow: {e}", exc_info=True)
        
        resultats["status"] = "error"
        resultats["erreur"] = str(e)
        resultats["timestamp_erreur"] = datetime.now().isoformat()
        
        return resultats

def test_workflow_synchrone():
    """Test synchrone du workflow pour comparaison"""
    logger.info("🔄 TEST WORKFLOW SYNCHRONE DE COMPARAISON")
    logger.info("=" * 80)
    
    try:
        # Création du chef d'équipe
        chef_equipe = create_agent_0_chef_equipe_coordinateur(
            target_path="./tools",
            workspace_path=".",
            safe_mode=True
        )
        
        logger.info("✅ Chef d'équipe créé (mode synchrone)")
        
        # Test des capacités disponibles
        if hasattr(chef_equipe, 'get_capabilities'):
            capacites = chef_equipe.get_capabilities()
            logger.info(f"📋 Capacités disponibles: {len(capacites)}")
            for cap in capacites[:5]:  # Afficher les 5 premières
                logger.debug(f"   ✅ {cap}")
            
        # Test health check synchrone
        health = chef_equipe.health_check()
        logger.info(f"🏥 Health (synchrone): {health}")
        
        return {"status": "success", "synchrone": True}
        
    except Exception as e:
        logger.error(f"❌ Erreur workflow synchrone: {e}", exc_info=True)
        return {"status": "error", "erreur": str(e)}

async def main():
    """Fonction principale de test"""
    logger.info("🎯 SUITE DE TESTS - WORKFLOW ÉQUIPE DE MAINTENANCE")
    logger.info("=" * 80)
    
    # Test workflow complet asynchrone
    resultats_async = await test_workflow_complet()
    
    # Test workflow synchrone
    resultats_sync = test_workflow_synchrone()
    
    # Consolidation des résultats
    rapport_final = {
        "suite_tests": "workflow_equipe_maintenance",
        "timestamp": datetime.now().isoformat(),
        "tests": {
            "workflow_asynchrone": resultats_async,
            "workflow_synchrone": resultats_sync
        },
        "synthese": {
            "async_success": resultats_async.get("status") == "success",
            "sync_success": resultats_sync.get("status") == "success",
            "etapes_completees": len([e for e in resultats_async.get("etapes", {}).values() if e.get("status") == "success"])
        }
    }
    
    # Sauvegarde du rapport
    fichier_rapport = f"rapport_workflow_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fichier_rapport, 'w', encoding='utf-8') as f:
        json.dump(rapport_final, f, indent=2, ensure_ascii=False)
    
    logger.info("📊 RÉSULTATS FINAUX - WORKFLOW ÉQUIPE")
    logger.info("=" * 80)
    logger.info(f"✅ Workflow Asynchrone: {'SUCCESS' if rapport_final['synthese']['async_success'] else 'FAILED'}")
    logger.info(f"✅ Workflow Synchrone: {'SUCCESS' if rapport_final['synthese']['sync_success'] else 'FAILED'}")
    logger.info(f"📋 Étapes completées: {rapport_final['synthese']['etapes_completees']}")
    logger.info(f"📄 Rapport sauvegardé: {fichier_rapport}")
    
    return rapport_final

if __name__ == "__main__":
    # Lancement du test complet
    resultat = asyncio.run(main())
    
    if resultat['synthese']['async_success'] and resultat['synthese']['sync_success']:
        logger.info("🎉 WORKFLOW ÉQUIPE DE MAINTENANCE VALIDÉ!")
        logger.info("🚀 L'équipe est prête pour toutes les missions de production!")
    else:
        logger.warning("⚠️ Workflow partiellement validé - Optimisations possibles") 



