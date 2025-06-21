#!/usr/bin/env python3
"""
🧪 TEST AGENTS AUDITEURS
Script de démonstration des agents auditeurs spécialisés

Agents testés :
- Agent 18 : Auditeur Sécurité
- Agent 19 : Auditeur Performance  
- Agent Orchestrateur : Coordination globale
"""

import asyncio
import sys
from pathlib import Path

# Ajout du chemin des agents
sys.path.insert(0, str(Path(__file__).parent / "agents"))

async def test_agent_securite():
    """Test de l'Agent 18 - Sécurité"""
    print("\n🔐 === TEST AGENT 18 - SÉCURITÉ ===")
    
    try:
        from agent_18_auditeur_securite import Agent18AuditeurSecurite
        
        agent = Agent18AuditeurSecurite()
        
        # Test sur un répertoire d'agents
        target = "agents"
        if Path(target).exists():
            print(f"🔍 Audit sécurité sur : {target}")
            
            rapport = await agent.auditer_securite_complete(target)
            
            print(f"✅ Score sécurité : {rapport['security_score']}/10")
            print(f"🔍 Vulnérabilités : {rapport['vulnerabilities_count']}")
            print(f"🚨 Critiques : {rapport['critical_count']}")
            
            if rapport['recommendations']:
                print(f"🔧 Recommandations :")
                for rec in rapport['recommendations'][:3]:
                    print(f"  • {rec}")
            
            return True
        else:
            print(f"❌ Répertoire {target} introuvable")
            return False
            
    except ImportError as e:
        print(f"❌ Agent 18 non disponible : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur test Agent 18 : {e}")
        return False

async def test_agent_performance():
    """Test de l'Agent 19 - Performance"""
    print("\n⚡ === TEST AGENT 19 - PERFORMANCE ===")
    
    try:
        from agent_19_auditeur_performance import Agent19AuditeurPerformance
        
        agent = Agent19AuditeurPerformance()
        
        # Test sur un répertoire d'agents
        target = "agents"
        if Path(target).exists():
            print(f"📊 Audit performance sur : {target}")
            
            rapport = await agent.auditer_performance(target)
            
            print(f"✅ Score performance : {rapport['score']}/10")
            print(f"⏱️ Temps exécution : {rapport['execution_time']:.2f}s")
            print(f"📊 Métriques : {len(rapport['metrics'])}")
            
            if rapport['bottlenecks']:
                print(f"🚨 Goulots d'étranglement :")
                for bottleneck in rapport['bottlenecks'][:3]:
                    print(f"  • {bottleneck}")
            
            return True
        else:
            print(f"❌ Répertoire {target} introuvable")
            return False
            
    except ImportError as e:
        print(f"❌ Agent 19 non disponible : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur test Agent 19 : {e}")
        return False

async def test_orchestrateur():
    """Test de l'Orchestrateur d'audit"""
    print("\n🎯 === TEST ORCHESTRATEUR AUDIT ===")
    
    try:
        from agent_orchestrateur_audit import AgentOrchestrateur
        
        orchestrateur = AgentOrchestrateur()
        
        # Définition cibles de test
        targets = ["agents"]
        existing_targets = [t for t in targets if Path(t).exists()]
        
        if not existing_targets:
            print("❌ Aucune cible d'audit disponible")
            return False
        
        print(f"🎯 Orchestration audit sur {len(existing_targets)} cibles")
        
        rapport = await orchestrateur.executer_audit_complet(existing_targets)
        
        if rapport.get('status') == 'ERROR':
            print(f"❌ Erreur orchestration : {rapport.get('error')}")
            return False
        
        print(f"✅ Score global : {rapport['executive_summary']['global_score']}/10")
        print(f"🎯 Statut : {rapport['executive_summary']['overall_status']}")
        
        # Agents déployés
        agents_deployed = rapport['orchestrator']['agents_deployed']
        print(f"🤖 Agents déployés : {', '.join(agents_deployed)}")
        
        # Actions prioritaires
        if rapport['priority_actions']:
            print(f"🚨 Actions prioritaires :")
            for action in rapport['priority_actions'][:3]:
                print(f"  • {action}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Orchestrateur non disponible : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur test Orchestrateur : {e}")
        return False

async def test_creation_fichier_exemple():
    """Crée un fichier d'exemple pour les tests"""
    print("\n📝 === CRÉATION FICHIER EXEMPLE ===")
    
    # Création d'un fichier Python avec problèmes volontaires
    exemple_code = '''#!/usr/bin/env python3
"""
Fichier d'exemple avec problèmes de sécurité et performance
"""

import pickle
import os
import time

# Problème sécurité : mot de passe en dur
password = "mon_super_secret_123"
api_key = "sk-1234567890abcdef"

def fonction_non_documentee():
    # Problème performance : boucles imbriquées
    result = []
    for i in range(1000):
        for j in range(1000):
            result.append(i * j)
    
    # Problème sécurité : désérialisation unsafe
    data = pickle.loads(open("data.pkl", "rb").read())
    
    # Problème performance : concaténation inefficace
    message = ""
    for item in result[:100]:
        message += str(item) + ", "
    
    # Problème performance : sleep dans le code
    time.sleep(0.1)
    
    return message

class mauvaise_classe:  # Problème conformité : nom de classe
    def __init__(self):
        self.VARIABLE_MAL_nommee = "test"  # Problème conformité
        
    def FonctionMalNommee(self):  # Problème conformité
        # Ligne trop longue pour test conformité PEP 8
        super_longue_ligne = "Cette ligne est volontairement très très très très très très très longue pour dépasser 79 caractères"
        return super_longue_ligne

# Variables globales (potentiel memory leak)
global_list = []
global_dict = {}

def ajouter_donnees():
    global global_list, global_dict
    global_list.append(range(10000))
    global_dict[len(global_dict)] = list(range(10000))
'''
    
    # Sauvegarde du fichier exemple
    exemple_file = Path("exemple_problematique.py")
    exemple_file.write_text(exemple_code, encoding='utf-8')
    
    print(f"✅ Fichier exemple créé : {exemple_file}")
    print("   - Problèmes sécurité : secrets en dur, pickle unsafe")
    print("   - Problèmes performance : boucles imbriquées, concaténation inefficace")
    print("   - Problèmes conformité : PEP 8, nommage")
    
    return str(exemple_file)

async def test_sur_fichier_exemple():
    """Test des agents sur le fichier d'exemple"""
    print("\n🧪 === TEST SUR FICHIER EXEMPLE ===")
    
    # Création du fichier
    fichier_exemple = await test_creation_fichier_exemple()
    
    # Test Agent Sécurité
    try:
        from agent_18_auditeur_securite import Agent18AuditeurSecurite
        agent_sec = Agent18AuditeurSecurite()
        
        rapport_sec = await agent_sec.auditer_securite_complete(fichier_exemple)
        print(f"\n🔐 Sécurité - Score : {rapport_sec['security_score']}/10")
        print(f"   Vulnérabilités : {rapport_sec['vulnerabilities_count']}")
        
    except Exception as e:
        print(f"❌ Erreur test sécurité sur exemple : {e}")
    
    # Test Agent Performance
    try:
        from agent_19_auditeur_performance import Agent19AuditeurPerformance
        agent_perf = Agent19AuditeurPerformance()
        
        rapport_perf = await agent_perf.auditer_performance(fichier_exemple)
        print(f"\n⚡ Performance - Score : {rapport_perf['score']}/10")
        print(f"   Métriques : {len(rapport_perf['metrics'])}")
        
    except Exception as e:
        print(f"❌ Erreur test performance sur exemple : {e}")
    
    # Nettoyage
    try:
        Path(fichier_exemple).unlink()
        print(f"\n🧹 Fichier exemple supprimé")
    except Exception:
        pass

async def main():
    """Point d'entrée principal des tests"""
    print("🧪 DÉMARRAGE TESTS AGENTS AUDITEURS")
    print("=" * 50)
    
    resultats = {
        'agent_securite': False,
        'agent_performance': False,
        'orchestrateur': False
    }
    
    # Tests individuels
    resultats['agent_securite'] = await test_agent_securite()
    resultats['agent_performance'] = await test_agent_performance()
    resultats['orchestrateur'] = await test_orchestrateur()
    
    # Test sur fichier exemple
    await test_sur_fichier_exemple()
    
    # Résumé des tests
    print("\n📊 === RÉSUMÉ DES TESTS ===")
    total_tests = len(resultats)
    tests_reussis = sum(resultats.values())
    
    for test_name, success in resultats.items():
        status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 SCORE GLOBAL : {tests_reussis}/{total_tests} tests réussis")
    
    if tests_reussis == total_tests:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
    elif tests_reussis > 0:
        print("⚠️ TESTS PARTIELLEMENT RÉUSSIS")
    else:
        print("❌ AUCUN TEST RÉUSSI - Vérifier les agents")
    
    print("\n📋 PROCHAINES ÉTAPES :")
    print("  1. Corriger les agents en échec si nécessaire")
    print("  2. Intégrer les agents dans le workflow principal")
    print("  3. Automatiser les audits périodiques")
    print("  4. Configurer les alertes sur issues critiques")

if __name__ == "__main__":
    asyncio.run(main()) 



