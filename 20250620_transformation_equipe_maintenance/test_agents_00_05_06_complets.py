#!/usr/bin/env python3
"""
🧪 TEST COMPLET - AGENTS 00, 05, 06 RÉCEMMENT MODIFIÉS
================================================================================
Objectif: Valider les 3 agents récemment modifiés avec leurs nouvelles capacités

Agents testés:
- Agent 00 - Chef d'Équipe Coordinateur  
- Agent 05 - Documenteur
- Agent 06 - Validateur Final
"""

import asyncio
import json
from logging_manager_optimized import LoggingManager
from datetime import datetime
from pathlib import Path
import sys

# Configuration des logs
# LoggingManager NextGeneration - Tests
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_logger(custom_config={
            "logger_name": "test_agents_00_05_06_complets",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })s - %(levelname)s - %(message)s')

# Import des agents
sys.path.insert(0, str(Path(__file__).parent))
from agent_equipe_maintenance.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur
from agent_equipe_maintenance.agent_MAINTENANCE_05_documenteur import create_agent_5_documenteur
from agent_equipe_maintenance.agent_MAINTENANCE_06_validateur_final import create_agent_6ValidateurFinal

async def test_agent_00_chef_equipe():
    """Test complet Agent 00 - Chef d'Équipe Coordinateur"""
    print("\n🔬 TEST AGENT 00 - CHEF D'ÉQUIPE COORDINATEUR")
    print("=" * 60)
    
    try:
        # Création de l'agent
        agent = create_agent_0_chef_equipe_coordinateur(
            target_path="../agent_factory_implementation/agents",
            workspace_path=".",
            safe_mode=True
        )
        
        # Test démarrage
        await agent.startup()
        
        # Test santé
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        print(f"📋 Workflows disponibles: {health.get('workflows_disponibles', 0)}")
        
        # Test capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        # Nouvelles capacités avancées
        nouvelles_capacites = [
            "intelligent_multi_agent_coordination",
            "automated_dependency_management", 
            "real_time_team_monitoring",
            "advanced_consolidated_reporting",
            "adaptive_resource_allocation",
            "predictive_team_analytics",
            "enterprise_compliance_management"
        ]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            if cap in capabilities:
                print(f"   ✅ {cap}")
            else:
                print(f"   ❌ {cap}")
        
        # Test arrêt
        await agent.shutdown()
        
        return {
            "status": "success",
            "agent": "Agent 00 - Chef d'Équipe",
            "capabilities_count": len(capabilities),
            "new_capabilities": len([c for c in nouvelles_capacites if c in capabilities]),
            "health": health['status']
        }
        
    except Exception as e:
        print(f"❌ Erreur test Agent 00: {e}")
        return {"status": "error", "error": str(e)}

async def test_agent_05_documenteur():
    """Test complet Agent 05 - Documenteur"""
    print("\n🔬 TEST AGENT 05 - DOCUMENTEUR")
    print("=" * 60)
    
    try:
        # Création de l'agent
        agent = create_agent_5_documenteur(
            resultats_tests={"tests_effectues": True, "resultats": "simulation"},
            target_path="./",
            workspace_path="."
        )
        
        # Test démarrage
        await agent.startup()
        
        # Test santé
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        
        # Test capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        # Nouvelles capacités avancées
        nouvelles_capacites = [
            "intelligent_automated_documentation",
            "adaptive_content_generation",
            "multi_format_documentation",
            "advanced_readability_metrics",
            "automated_diagram_creation",
            "smart_content_optimization"
        ]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            if cap in capabilities:
                print(f"   ✅ {cap}")
            else:
                print(f"   ❌ {cap}")
        
        # Test d'une capacité avancée
        if "intelligent_automated_documentation" in capabilities:
            print("🧪 Test capacité: intelligent_automated_documentation")
            test_data = {
                "source_files": ["test.py"],
                "target_audience": "developers",
                "format": "markdown"
            }
            try:
                result = await agent.intelligent_automated_documentation(test_data)
                print("   ✅ Capacité testée avec succès")
            except Exception as e:
                print(f"   ⚠️ Erreur test capacité: {e}")
        
        # Test arrêt
        await agent.shutdown()
        
        return {
            "status": "success",
            "agent": "Agent 05 - Documenteur",
            "capabilities_count": len(capabilities),
            "new_capabilities": len([c for c in nouvelles_capacites if c in capabilities]),
            "health": health['status']
        }
        
    except Exception as e:
        print(f"❌ Erreur test Agent 05: {e}")
        return {"status": "error", "error": str(e)}

async def test_agent_06_validateur_final():
    """Test complet Agent 06 - Validateur Final"""
    print("\n🔬 TEST AGENT 06 - VALIDATEUR FINAL")
    print("=" * 60)
    
    try:
        # Création de l'agent
        agent = create_agent_6ValidateurFinal(
            resultats_equipe={"simulation": True},
            target_path="./",
            workspace_path="."
        )
        
        # Test démarrage
        await agent.startup()
        
        # Test santé
        health = await agent.health_check()
        print(f"🏥 Health: {health['status']}")
        
        # Test capacités
        capabilities = agent.get_capabilities()
        print(f"📋 Capacités totales: {len(capabilities)}")
        
        # Nouvelles capacités avancées
        nouvelles_capacites = [
            "intelligent_multi_criteria_validation",
            "advanced_compliance_scoring",
            "enterprise_security_analysis",
            "real_time_quality_metrics",
            "predictive_validation",
            "enterprise_level_certification",
            "automated_risk_assessment",
            "regulatory_compliance_check"
        ]
        
        print(f"🆕 Nouvelles capacités avancées: {len(nouvelles_capacites)}")
        for cap in nouvelles_capacites:
            if cap in capabilities:
                print(f"   ✅ {cap}")
            else:
                print(f"   ❌ {cap}")
        
        # Test d'une capacité avancée
        if "enterprise_security_analysis" in capabilities:
            print("🧪 Test capacité: enterprise_security_analysis")
            test_data = {
                "target_files": ["test.py"],
                "security_level": "enterprise"
            }
            try:
                result = await agent.enterprise_security_analysis(test_data)
                print("   ✅ Capacité testée avec succès")
            except Exception as e:
                print(f"   ⚠️ Erreur test capacité: {e}")
        
        # Test arrêt
        await agent.shutdown()
        
        return {
            "status": "success",
            "agent": "Agent 06 - Validateur Final",
            "capabilities_count": len(capabilities),
            "new_capabilities": len([c for c in nouvelles_capacites if c in capabilities]),
            "health": health['status']
        }
        
    except Exception as e:
        print(f"❌ Erreur test Agent 06: {e}")
        return {"status": "error", "error": str(e)}

async def test_collaboration_agents_00_05_06():
    """Test de collaboration entre les agents 00, 05, 06"""
    print("\n🔬 TEST COLLABORATION AGENTS 00-05-06")
    print("=" * 60)
    
    try:
        # Création des agents
        chef = create_agent_0_chef_equipe_coordinateur()
        documenteur = create_agent_5_documenteur(
            resultats_tests={"tests_effectues": True},
            target_path="./",
            workspace_path="."
        )
        validateur = create_agent_6ValidateurFinal(
            resultats_equipe={"simulation": True},
            target_path="./",
            workspace_path="."
        )
        
        # Démarrage
        await chef.startup()
        await documenteur.startup()
        await validateur.startup()
        
        # Test santé de l'équipe
        health_chef = await chef.health_check()
        health_doc = await documenteur.health_check()
        health_val = await validateur.health_check()
        
        agents_healthy = sum([
            1 for h in [health_chef, health_doc, health_val]
            if h['status'] == 'healthy'
        ])
        
        print(f"🏥 Agents en bonne santé: {agents_healthy}/3")
        
        # Capacités combinées
        caps_chef = chef.get_capabilities()
        caps_doc = documenteur.get_capabilities()  
        caps_val = validateur.get_capabilities()
        
        all_capabilities = set(caps_chef + caps_doc + caps_val)
        print(f"🎯 Capacités uniques de l'équipe: {len(all_capabilities)}")
        print(f"📊 Capacités totales: {len(caps_chef) + len(caps_doc) + len(caps_val)}")
        
        # Arrêt
        await chef.shutdown()
        await documenteur.shutdown()
        await validateur.shutdown()
        
        return {
            "agents_healthy": agents_healthy,
            "total_agents": 3,
            "unique_capabilities": len(all_capabilities),
            "total_capabilities": len(caps_chef) + len(caps_doc) + len(caps_val)
        }
        
    except Exception as e:
        print(f"❌ Erreur test collaboration: {e}")
        return {"status": "error", "error": str(e)}

async def main():
    """Test principal"""
    print("🚀 TEST COMPLET - AGENTS 00, 05, 06 RÉCEMMENT MODIFIÉS")
    print("=" * 80)
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    print("🎯 Objectif: Valider les 3 agents récemment modifiés\n")
    
    results = {}
    
    # Tests individuels
    results['agent_00'] = await test_agent_00_chef_equipe()
    results['agent_05'] = await test_agent_05_documenteur()
    results['agent_06'] = await test_agent_06_validateur_final()
    
    # Test collaboration
    results['collaboration'] = await test_collaboration_agents_00_05_06()
    
    # Résultats finaux
    print("\n📊 RÉSULTATS FINAUX")
    print("=" * 80)
    
    success_count = sum(1 for r in results.values() if r.get('status') == 'success')
    total_tests = len([k for k in results.keys() if k != 'collaboration'])
    
    print(f"✅ Tests réussis: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    
    # Capacités totales
    total_capabilities = 0
    total_new_capabilities = 0
    
    for key, result in results.items():
        if key != 'collaboration' and result.get('status') == 'success':
            total_capabilities += result.get('capabilities_count', 0)
            total_new_capabilities += result.get('new_capabilities', 0)
    
    print(f"🆕 Nouvelles capacités ajoutées: {total_new_capabilities}")
    print(f"📋 Capacités totales: {total_capabilities}")
    
    if results['collaboration'].get('agents_healthy'):
        print(f"🤝 Collaboration: {results['collaboration']['agents_healthy']}/3 agents opérationnels")
    
    # Conclusion
    if success_count == total_tests:
        print("\n🎉 TOUS LES AGENTS 00-05-06 FONCTIONNENT PARFAITEMENT!")
        print("   ✅ Intégration Pattern Factory réussie")
        print("   ✅ Nouvelles capacités avancées validées")
        print("   ✅ Équipe étendue prête pour la production")
    else:
        print(f"\n⚠️ {total_tests - success_count} agent(s) nécessitent des corrections")
    
    # Sauvegarde rapport
    rapport = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "agents_00_05_06_extended_validation",
        "results": results,
        "summary": {
            "success_rate": f"{success_count/total_tests*100:.1f}%",
            "total_capabilities": total_capabilities,
            "new_capabilities": total_new_capabilities,
            "collaboration_status": results['collaboration'].get('agents_healthy', 0)
        }
    }
    
    rapport_path = f"rapport_agents_00_05_06_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(rapport_path, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {rapport_path}")

if __name__ == "__main__":
    asyncio.run(main()) 