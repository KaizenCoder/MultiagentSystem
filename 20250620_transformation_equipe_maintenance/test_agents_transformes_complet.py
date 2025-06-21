#!/usr/bin/env python3
"""
🧪 TEST COMPLET - TOUS LES AGENTS TRANSFORMÉS (00-06)
====================================================

Test de validation pour s'assurer que TOUS les agents (00, 01, 02, 03, 04, 05, 06)
respectent le même Pattern Factory NextGeneration.

Author: Équipe de Maintenance NextGeneration
Created: 2025-01-19
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Import des agents transformés - TOUS
from agent_equipe_maintenance.agent_MAINTENANCE_00_chef_equipe_coordinateur import ChefEquipeCoordinateurEnterprise
from agent_equipe_maintenance.agent_MAINTENANCE_01_analyseur_structure import create_agent_analyseur_structure
from agent_equipe_maintenance.agent_MAINTENANCE_02_evaluateur_utilite import create_agent_evaluateur_utilite  
from agent_equipe_maintenance.agent_MAINTENANCE_03_adaptateur_code import create_agent_3_adaptateur_code
from agent_equipe_maintenance.agent_MAINTENANCE_04_testeur_anti_faux_agents import create_agent_testeur_anti_faux
from agent_equipe_maintenance.agent_MAINTENANCE_05_documenteur import DocumenteurEnterprise
from agent_equipe_maintenance.agent_MAINTENANCE_06_validateur_final import ValidateurFinalEnterprise

async def test_agent_pattern_factory_compliance(agent, agent_name: str) -> Dict[str, Any]:
    """Test de conformité Pattern Factory pour un agent"""
    print(f"\n🔬 TEST {agent_name.upper()}")
    print("=" * 60)
    
    test_result = {
        "agent_name": agent_name,
        "pattern_factory_compliant": True,
        "required_methods": {},
        "capabilities_count": 0,
        "new_capabilities": [],
        "health_status": {},
        "errors": []
    }
    
    try:
        # Test 1: Méthode startup()
        try:
            await agent.startup()
            test_result["required_methods"]["startup"] = "✅ OK"
            print("✅ startup() - OK")
        except Exception as e:
            test_result["required_methods"]["startup"] = f"❌ ERREUR: {e}"
            test_result["errors"].append(f"startup(): {e}")
            print(f"❌ startup() - ERREUR: {e}")
        
        # Test 2: Méthode health_check()
        try:
            health = await agent.health_check()
            test_result["required_methods"]["health_check"] = "✅ OK"
            test_result["health_status"] = health
            print(f"✅ health_check() - Status: {health.get('status', 'unknown')}")
        except Exception as e:
            test_result["required_methods"]["health_check"] = f"❌ ERREUR: {e}"
            test_result["errors"].append(f"health_check(): {e}")
            print(f"❌ health_check() - ERREUR: {e}")
        
        # Test 3: Méthode get_capabilities()
        try:
            capabilities = agent.get_capabilities()
            test_result["required_methods"]["get_capabilities"] = "✅ OK"
            test_result["capabilities_count"] = len(capabilities)
            
            # Identifier les nouvelles capacités avancées
            advanced_keywords = [
                "intelligent", "advanced", "enterprise", "automated", "predictive",
                "multi", "smart", "adaptive", "real_time", "compliance"
            ]
            
            new_capabilities = []
            for cap in capabilities:
                if any(keyword in cap.lower() for keyword in advanced_keywords):
                    new_capabilities.append(cap)
            
            test_result["new_capabilities"] = new_capabilities
            print(f"✅ get_capabilities() - {len(capabilities)} capacités totales")
            print(f"🆕 Nouvelles capacités avancées: {len(new_capabilities)}")
            for cap in new_capabilities[:5]:  # Afficher les 5 premières
                print(f"   ✅ {cap}")
            if len(new_capabilities) > 5:
                print(f"   ... et {len(new_capabilities) - 5} autres")
                
        except Exception as e:
            test_result["required_methods"]["get_capabilities"] = f"❌ ERREUR: {e}"
            test_result["errors"].append(f"get_capabilities(): {e}")
            print(f"❌ get_capabilities() - ERREUR: {e}")
        
        # Test 4: Méthode execute_task() (si disponible)
        if hasattr(agent, 'execute_task'):
            try:
                # Créer une tâche de test simple
                class TestTask:
                    def __init__(self, task_id: str):
                        self.task_id = task_id
                
                test_task = TestTask("test_task")
                result = await agent.execute_task(test_task)
                test_result["required_methods"]["execute_task"] = "✅ OK"
                print("✅ execute_task() - OK")
            except Exception as e:
                test_result["required_methods"]["execute_task"] = f"⚠️ PARTIEL: {e}"
                print(f"⚠️ execute_task() - PARTIEL: {e}")
        else:
            test_result["required_methods"]["execute_task"] = "❌ MANQUANT"
            print("❌ execute_task() - MANQUANT")
        
        # Test 5: Méthode shutdown()
        try:
            await agent.shutdown()
            test_result["required_methods"]["shutdown"] = "✅ OK"
            print("✅ shutdown() - OK")
        except Exception as e:
            test_result["required_methods"]["shutdown"] = f"❌ ERREUR: {e}"
            test_result["errors"].append(f"shutdown(): {e}")
            print(f"❌ shutdown() - ERREUR: {e}")
        
        # Évaluation globale
        required_methods_ok = sum(1 for status in test_result["required_methods"].values() if "✅" in status)
        total_required = len(test_result["required_methods"])
        compliance_rate = (required_methods_ok / total_required) * 100
        
        test_result["pattern_factory_compliant"] = compliance_rate >= 80.0
        test_result["compliance_rate"] = compliance_rate
        
        print(f"📊 Conformité Pattern Factory: {compliance_rate:.1f}% ({required_methods_ok}/{total_required})")
        
        if test_result["pattern_factory_compliant"]:
            print("🎉 AGENT CONFORME PATTERN FACTORY")
        else:
            print("⚠️ AGENT NON CONFORME - Corrections nécessaires")
        
    except Exception as e:
        test_result["pattern_factory_compliant"] = False
        test_result["errors"].append(f"Test général: {e}")
        print(f"❌ ERREUR GÉNÉRALE: {e}")
    
    return test_result

async def main():
    """Test principal de tous les agents transformés"""
    print("🧪 TEST COMPLET - TOUS LES AGENTS TRANSFORMÉS (00-06)")
    print("=" * 80)
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    print("🎯 Objectif: Valider la conformité Pattern Factory de TOUS les agents")
    
    # Configuration des agents à tester
    agents_config = [
        ("AGENT 00 - CHEF D'ÉQUIPE COORDINATEUR", lambda: ChefEquipeCoordinateurEnterprise()),
        ("AGENT 01 - ANALYSEUR STRUCTURE", lambda: create_agent_analyseur_structure()),
        ("AGENT 02 - ÉVALUATEUR UTILITÉ", lambda: create_agent_evaluateur_utilite()),
        ("AGENT 03 - ADAPTATEUR CODE", lambda: create_agent_3_adaptateur_code()),
        ("AGENT 04 - TESTEUR ANTI-FAUX", lambda: create_agent_testeur_anti_faux()),
        ("AGENT 05 - DOCUMENTEUR", lambda: DocumenteurEnterprise()),
        ("AGENT 06 - VALIDATEUR FINAL", lambda: ValidateurFinalEnterprise())
    ]
    
    results = []
    total_agents = len(agents_config)
    compliant_agents = 0
    
    # Test de chaque agent
    for agent_name, agent_factory in agents_config:
        try:
            agent = agent_factory()
            result = await test_agent_pattern_factory_compliance(agent, agent_name)
            results.append(result)
            
            if result["pattern_factory_compliant"]:
                compliant_agents += 1
                
        except Exception as e:
            print(f"\n❌ ERREUR CRÉATION {agent_name}: {e}")
            results.append({
                "agent_name": agent_name,
                "pattern_factory_compliant": False,
                "errors": [f"Création agent: {e}"]
            })
    
    # Résultats finaux
    print("\n📊 RÉSULTATS FINAUX - CONFORMITÉ PATTERN FACTORY")
    print("=" * 80)
    
    compliance_rate = (compliant_agents / total_agents) * 100
    print(f"✅ Agents conformes: {compliant_agents}/{total_agents} ({compliance_rate:.1f}%)")
    
    # Détail par agent
    for result in results:
        status = "✅ CONFORME" if result["pattern_factory_compliant"] else "❌ NON CONFORME"
        capabilities = result.get("capabilities_count", 0)
        new_caps = len(result.get("new_capabilities", []))
        print(f"   {status} - {result['agent_name']} ({capabilities} capacités, {new_caps} nouvelles)")
    
    # Capacités totales
    total_capabilities = sum(result.get("capabilities_count", 0) for result in results)
    total_new_capabilities = sum(len(result.get("new_capabilities", [])) for result in results)
    
    print(f"\n📋 Capacités totales équipe: {total_capabilities}")
    print(f"🆕 Nouvelles capacités avancées: {total_new_capabilities}")
    
    # Sauvegarde rapport
    rapport = {
        "test_timestamp": datetime.now().isoformat(),
        "test_type": "pattern_factory_compliance_all_agents",
        "agents_tested": total_agents,
        "agents_compliant": compliant_agents,
        "compliance_rate": compliance_rate,
        "total_capabilities": total_capabilities,
        "total_new_capabilities": total_new_capabilities,
        "detailed_results": results
    }
    
    with open("rapport_conformite_pattern_factory_complet.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📄 Rapport sauvegardé: rapport_conformite_pattern_factory_complet.json")
    
    # Conclusion
    if compliance_rate == 100.0:
        print("\n🎉 SUCCÈS COMPLET!")
        print("   ✅ TOUS les agents respectent le Pattern Factory NextGeneration")
        print("   ✅ Équipe entièrement transformée et conforme")
        print("   ✅ Prêt pour déploiement enterprise")
    elif compliance_rate >= 80.0:
        print("\n✅ SUCCÈS MAJORITAIRE!")
        print("   ✅ La plupart des agents sont conformes")
        print("   ⚠️ Quelques corrections mineures nécessaires")
    else:
        print("\n⚠️ TRANSFORMATIONS INCOMPLÈTES")
        print("   ❌ Plusieurs agents nécessitent des corrections")
        print("   🔧 Poursuivre la transformation")
    
    return compliance_rate

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result >= 80.0 else 1) 