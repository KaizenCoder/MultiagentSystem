#!/usr/bin/env python3
"""
🧪 TEST AGENT 03 ADAPTATEUR CODE UPGRADED
=========================================

Script de test pour démontrer les nouvelles capacités de transformation
de l'Agent 03 vers le Pattern Factory.

Author: Équipe Maintenance NextGeneration
Version: 1.0.0
Created: 2025-01-20
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire des agents au PATH
sys.path.insert(0, str(Path(__file__).parent / "agent_equipe_maintenance"))

from agent_MAINTENANCE_03_adaptateur_code import create_adaptateur_code_upgraded

async def test_agent_03_upgraded():
    """Test complet de l'Agent 03 Upgraded"""
    
    print("🧪 TEST AGENT 03 ADAPTATEUR CODE UPGRADED")
    print("=" * 60)
    
    # Créer l'agent
    agent = create_adaptateur_code_upgraded()
    
    try:
        # 1. Démarrage
        print("\n🚀 PHASE 1: DÉMARRAGE AGENT")
        await agent.startup()
        
        # 2. Health Check
        print("\n🏥 PHASE 2: HEALTH CHECK")
        health = await agent.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Agent ID: {health['agent_id']}")
        print(f"   Pattern Factory Available: {health['pattern_factory_available']}")
        
        # 3. Capacités
        print("\n🛠️ PHASE 3: CAPACITÉS AVANCÉES")
        capabilities = agent.get_capabilities()
        print(f"   Total capacités: {len(capabilities)}")
        
        # Afficher les nouvelles capacités de transformation
        transformation_capabilities = [cap for cap in capabilities if any(keyword in cap for keyword in ['transform', 'fix', 'migrate', 'pattern_factory'])]
        print(f"   Capacités de transformation: {len(transformation_capabilities)}")
        for cap in transformation_capabilities:
            print(f"      • {cap}")
        
        # 4. Test simulation transformation (sans fichier réel)
        print("\n🔧 PHASE 4: SIMULATION TRANSFORMATION")
        
        # Simuler un rapport d'audit de l'Agent 04
        mock_audit_report = {
            "agents_analysis": {
                "agent_example.py": {
                    "conformity_status": "critical_errors",
                    "critical_issues": [
                        "CRITIQUE ligne 46: 'async async def' - Syntaxe Python invalide",
                        "CRITIQUE: Import Pattern Factory manquant"
                    ],
                    "recommendations": [
                        "Corriger syntaxe async async def",
                        "Ajouter imports Pattern Factory"
                    ]
                }
            }
        }
        
        # Créer fichier temporaire pour test
        temp_dir = Path("temp_test")
        temp_dir.mkdir(exist_ok=True)
        
        temp_audit_file = temp_dir / "mock_audit_report.json"
        with open(temp_audit_file, 'w', encoding='utf-8') as f:
            json.dump(mock_audit_report, f, indent=2, ensure_ascii=False)
        
        # Créer un agent exemple avec erreur syntaxe
        temp_agent_file = temp_dir / "agent_example.py"
        with open(temp_agent_file, 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""Agent exemple avec erreurs"""

import asyncio

class AgentExample:
    def __init__(self):
        self.name = "example"
    
    # Erreur syntaxe intentionnelle
    async async def problematic_method(self):
        return "This has syntax error"
    
    def normal_method(self):
        return "This is fine"

if __name__ == "__main__":
    agent = AgentExample()
    print("Agent example created")
''')
        
        print(f"   📁 Fichiers temporaires créés dans: {temp_dir}")
        print(f"   📋 Rapport d'audit: {temp_audit_file}")
        print(f"   🤖 Agent exemple: {temp_agent_file}")
        
        # Tester correction d'erreurs critiques
        print("\n🚨 PHASE 5: TEST CORRECTION ERREURS CRITIQUES")
        critical_issues = mock_audit_report["agents_analysis"]["agent_example.py"]["critical_issues"]
        
        fix_result = await agent.fix_critical_errors(str(temp_agent_file), critical_issues)
        
        print(f"   Fichier traité: {fix_result['agent_file']}")
        print(f"   Erreurs originales: {fix_result['original_issues_count']}")
        print(f"   Corrections appliquées: {fix_result['fixes_count']}")
        print(f"   Source modifiée: {fix_result['source_modified']}")
        print(f"   Succès: {fix_result['success']}")
        
        if fix_result['fixes_applied']:
            print("   Corrections détaillées:")
            for fix in fix_result['fixes_applied']:
                print(f"      • {fix['type']}: {fix.get('pattern', 'N/A')}")
        
        # 5. Statistiques finales
        print("\n📊 PHASE 6: STATISTIQUES TRANSFORMATION")
        final_health = await agent.health_check()
        stats = final_health.get('transformation_stats', {})
        
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # 6. Arrêt propre
        print("\n🛑 PHASE 7: ARRÊT AGENT")
        await agent.shutdown()
        
        # Nettoyage
        print("\n🧹 NETTOYAGE")
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"   Répertoire temporaire supprimé: {temp_dir}")
        
        print("\n" + "=" * 60)
        print("✅ TEST AGENT 03 UPGRADED TERMINÉ AVEC SUCCÈS!")
        print("🎯 L'agent est prêt pour les transformations Pattern Factory")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur durant le test: {e}")
        await agent.shutdown()
        raise

def main():
    """Point d'entrée principal"""
    try:
        asyncio.run(test_agent_03_upgraded())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 