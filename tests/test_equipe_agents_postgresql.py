#!/usr/bin/env python3
"""
🧪 TEST ÉQUIPE AGENTS POSTGRESQL
Test complet de l'équipe d'agents PostgreSQL avec notre système d'évaluation

Équipe analysée:
- agent_workspace_organizer.py
- agent_windows_postgres.py  
- agent_testing_specialist.py
- agent_web_researcher.py
- agent_sqlalchemy_fixer.py
- agent_documentation_manager.py
- agent_resolution_finale.py
- agent_docker_specialist.py
- agent_diagnostic_postgres_final.py
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from agent_testeur_agents import create_agent_testeur_agents
from agent_1_analyseur_structure import create_agent_analyseur_structure
from agent_2_evaluateur_utilite import create_agent_evaluateur_utilite

async def test_equipe_postgresql():
    """Test complet de l'équipe d'agents PostgreSQL"""
    print("🧪 TEST ÉQUIPE AGENTS POSTGRESQL - NEXTGENERATION")
    print("=" * 70)
    
    # Répertoire de l'équipe PostgreSQL
    equipe_dir = Path("docs/agents_postgresql_resolution/agent team")
    
    if not equipe_dir.exists():
        print("❌ Répertoire équipe PostgreSQL non trouvé")
        return
    
    # Lister les agents de l'équipe
    agents_postgresql = list(equipe_dir.glob("agent_*.py"))
    print(f"📁 Équipe PostgreSQL: {len(agents_postgresql)} agents trouvés")
    for agent in agents_postgresql:
        print(f"   - {agent.name}")
    
    # ===== PHASE 1: ANALYSE STRUCTURE =====
    print("\n" + "="*70)
    print("📊 PHASE 1: ANALYSE STRUCTURE DES AGENTS")
    print("="*70)
    
    # Créer l'agent analyseur
    analyseur = create_agent_analyseur_structure()
    
    try:
        await analyseur.startup()
        
        # Analyser chaque agent de l'équipe
        analyses_agents = {}
        
        for i, agent_file in enumerate(agents_postgresql, 1):
            print(f"\n🔍 [{i}/{len(agents_postgresql)}] Analyse: {agent_file.name}")
            
            # Configuration pour analyser ce fichier spécifique
            analyseur.source_path = agent_file.parent
            
            # Analyse du fichier
            with open(agent_file, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            analyse = await analyseur.analyser_fichier_python(agent_file)
            analyses_agents[agent_file.name] = analyse
            
            # Affichage résumé
            print(f"   📋 Classes: {len(analyse.get('classes', []))}")
            print(f"   🔧 Fonctions: {len(analyse.get('functions', []))}")
            print(f"   📦 Imports: {len(analyse.get('imports', []))}")
            print(f"   📏 Lignes: {analyse.get('lines_count', 0)}")
            print(f"   🧠 Complexité: {analyse.get('complexity_score', 0)}")
        
        await analyseur.shutdown()
        
        # Statistiques globales équipe
        print(f"\n📊 STATISTIQUES ÉQUIPE POSTGRESQL:")
        total_lines = sum(a.get('lines_count', 0) for a in analyses_agents.values())
        total_functions = sum(len(a.get('functions', [])) for a in analyses_agents.values())
        total_classes = sum(len(a.get('classes', [])) for a in analyses_agents.values())
        avg_complexity = sum(a.get('complexity_score', 0) for a in analyses_agents.values()) / len(analyses_agents)
        
        print(f"   📏 Total lignes: {total_lines}")
        print(f"   🔧 Total fonctions: {total_functions}")
        print(f"   📋 Total classes: {total_classes}")
        print(f"   🧠 Complexité moyenne: {avg_complexity:.1f}")
        
    except Exception as e:
        print(f"❌ Erreur analyse structure: {e}")
        return
    
    # ===== PHASE 2: ÉVALUATION UTILITÉ =====
    print("\n" + "="*70)
    print("🎯 PHASE 2: ÉVALUATION UTILITÉ DES AGENTS")
    print("="*70)
    
    # Créer l'agent évaluateur
    evaluateur = create_agent_evaluateur_utilite()
    
    try:
        await evaluateur.startup()
        
        # Préparer les données pour l'évaluation
        tools_data = {
            "tools": []
        }
        
        for agent_name, analyse in analyses_agents.items():
            tool_data = {
                "name": agent_name.replace('.py', ''),
                "tool_type": "postgresql_agent",
                "functions": analyse.get('functions', []),
                "classes": analyse.get('classes', []),
                "imports": analyse.get('imports', []),
                "complexity_score": analyse.get('complexity_score', 0),
                "lines_count": analyse.get('lines_count', 0),
                "utility_indicators": await analyser_indicateurs_postgresql(agent_name, analyse),
                "docstring": analyse.get('docstring', ''),
                "postgresql_specialization": await detecter_specialisation_postgresql(agent_name, analyse)
            }
            tools_data["tools"].append(tool_data)
        
        # Évaluation de l'utilité
        print("🎯 Évaluation utilité des agents PostgreSQL...")
        evaluation_results = await evaluateur.evaluate_tools_utility(tools_data)
        
        await evaluateur.shutdown()
        
        # Affichage des résultats d'évaluation
        print(f"\n📊 RÉSULTATS ÉVALUATION:")
        print(f"   ✅ Agents sélectionnés: {len(evaluation_results['selected_tools'])}")
        print(f"   ❌ Agents rejetés: {len(evaluation_results['rejected_tools'])}")
        print(f"   ⚠️ Conflits détectés: {len(evaluation_results.get('conflicted_tools', []))}")
        
        # Top 3 agents les mieux notés
        selected_tools = evaluation_results['selected_tools']
        if selected_tools:
            print(f"\n🏆 TOP 3 AGENTS POSTGRESQL:")
            for i, tool in enumerate(selected_tools[:3], 1):
                print(f"   {i}. {tool['name']}")
                print(f"      Score: {tool['utility_score']}/100")
                print(f"      Priorité: {tool['integration_priority']}")
                print(f"      Spécialisation: {tool.get('postgresql_specialization', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erreur évaluation utilité: {e}")
        return
    
    # ===== PHASE 3: TEST CONFORMITÉ PATTERN FACTORY =====
    print("\n" + "="*70)
    print("🏗️ PHASE 3: TEST CONFORMITÉ PATTERN FACTORY")
    print("="*70)
    
    # Créer l'agent testeur
    testeur = create_agent_testeur_agents(safe_mode=True, test_timeout=30)
    
    try:
        await testeur.startup()
        
        # Tester chaque agent PostgreSQL
        resultats_tests = {}
        
        for i, agent_file in enumerate(agents_postgresql, 1):
            print(f"\n🧪 [{i}/{len(agents_postgresql)}] Test conformité: {agent_file.name}")
            
            # Test de l'agent
            test_result = await testeur.tester_agent(str(agent_file))
            resultats_tests[agent_file.name] = test_result
            
            # Affichage résumé
            score = test_result.get('score_global', 0)
            conformite = test_result.get('conformite_pattern_factory', {})
            
            print(f"   📊 Score global: {score}/100")
            print(f"   🏗️ Pattern Factory: {'✅' if conformite.get('conforme', False) else '❌'}")
            print(f"   ✅ Tests réussis: {test_result.get('tests_reussis', 0)}")
            print(f"   ❌ Tests échoués: {test_result.get('tests_echoues', 0)}")
        
        await testeur.shutdown()
        
        # Statistiques conformité
        agents_conformes = sum(1 for r in resultats_tests.values() 
                             if r.get('conformite_pattern_factory', {}).get('conforme', False))
        score_moyen = sum(r.get('score_global', 0) for r in resultats_tests.values()) / len(resultats_tests)
        
        print(f"\n📊 CONFORMITÉ PATTERN FACTORY:")
        print(f"   ✅ Agents conformes: {agents_conformes}/{len(agents_postgresql)}")
        print(f"   📊 Score moyen: {score_moyen:.1f}/100")
        print(f"   🎯 Taux conformité: {agents_conformes/len(agents_postgresql)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Erreur test conformité: {e}")
        return
    
    # ===== PHASE 4: RECOMMANDATIONS =====
    print("\n" + "="*70)
    print("💡 PHASE 4: RECOMMANDATIONS POUR L'ÉQUIPE")
    print("="*70)
    
    recommendations = await generer_recommandations_equipe(
        analyses_agents, 
        evaluation_results, 
        resultats_tests
    )
    
    print("🎯 RECOMMANDATIONS PRIORITAIRES:")
    for i, rec in enumerate(recommendations['prioritaires'], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🔧 ACTIONS TECHNIQUES:")
    for i, action in enumerate(recommendations['techniques'], 1):
        print(f"   {i}. {action}")
    
    print(f"\n📈 OPTIMISATIONS:")
    for i, opt in enumerate(recommendations['optimisations'], 1):
        print(f"   {i}. {opt}")
    
    # ===== RAPPORT FINAL =====
    print("\n" + "="*70)
    print("📄 GÉNÉRATION RAPPORT FINAL")
    print("="*70)
    
    rapport_final = {
        "test_timestamp": datetime.now().isoformat(),
        "equipe_analysee": "Agents PostgreSQL Resolution",
        "nombre_agents": len(agents_postgresql),
        "analyses_structure": analyses_agents,
        "evaluation_utilite": evaluation_results,
        "tests_conformite": resultats_tests,
        "recommandations": recommendations,
        "statistiques_globales": {
            "total_lignes": total_lines,
            "total_fonctions": total_functions,
            "total_classes": total_classes,
            "complexite_moyenne": avg_complexity,
            "agents_conformes": agents_conformes,
            "score_moyen": score_moyen,
            "taux_conformite": agents_conformes/len(agents_postgresql)*100
        }
    }
    
    # Sauvegarde rapport
    rapport_file = f"test_equipe_postgresql_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport_final, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {rapport_file}")
    
    # ===== RÉSUMÉ EXÉCUTIF =====
    print("\n" + "="*70)
    print("🎯 RÉSUMÉ EXÉCUTIF - ÉQUIPE AGENTS POSTGRESQL")
    print("="*70)
    
    print(f"✅ ANALYSE COMPLÈTE RÉALISÉE:")
    print(f"   📊 {len(agents_postgresql)} agents analysés")
    print(f"   🎯 {len(evaluation_results['selected_tools'])} agents recommandés")
    print(f"   🏗️ {agents_conformes} agents conformes Pattern Factory")
    print(f"   📈 Score équipe: {score_moyen:.1f}/100")
    
    qualite_equipe = "EXCELLENTE" if score_moyen >= 80 else "BONNE" if score_moyen >= 60 else "À AMÉLIORER"
    print(f"\n🎖️ QUALITÉ ÉQUIPE: {qualite_equipe}")
    
    print(f"\n🚀 PRÊT POUR INTÉGRATION NEXTGENERATION!")

async def analyser_indicateurs_postgresql(agent_name, analyse):
    """Analyse les indicateurs spécifiques PostgreSQL"""
    indicateurs = []
    
    # Analyse du nom de l'agent
    if "postgres" in agent_name.lower():
        indicateurs.append("postgresql_specialized")
    if "test" in agent_name.lower():
        indicateurs.append("testing_capability")
    if "docker" in agent_name.lower():
        indicateurs.append("containerization")
    if "documentation" in agent_name.lower():
        indicateurs.append("documentation_generator")
    
    # Analyse des imports
    imports = analyse.get('imports', [])
    if any('psycopg2' in imp for imp in imports):
        indicateurs.append("psycopg2_integration")
    if any('sqlalchemy' in imp for imp in imports):
        indicateurs.append("sqlalchemy_integration")
    if any('docker' in imp for imp in imports):
        indicateurs.append("docker_integration")
    
    # Analyse des fonctions
    functions = analyse.get('functions', [])
    if any('test_' in f.get('name', '') for f in functions):
        indicateurs.append("automated_testing")
    if any('fix_' in f.get('name', '') for f in functions):
        indicateurs.append("repair_capability")
    
    return indicateurs

async def detecter_specialisation_postgresql(agent_name, analyse):
    """Détecte la spécialisation PostgreSQL de l'agent"""
    name_lower = agent_name.lower()
    
    if "workspace_organizer" in name_lower:
        return "workspace_management"
    elif "testing_specialist" in name_lower:
        return "testing_automation"
    elif "web_researcher" in name_lower:
        return "research_documentation"
    elif "sqlalchemy_fixer" in name_lower:
        return "sqlalchemy_repair"
    elif "documentation_manager" in name_lower:
        return "documentation_generation"
    elif "resolution_finale" in name_lower:
        return "final_resolution"
    elif "docker_specialist" in name_lower:
        return "containerization"
    elif "diagnostic_postgres" in name_lower:
        return "postgresql_diagnosis"
    elif "windows_postgres" in name_lower:
        return "windows_postgresql"
    else:
        return "general_postgresql"

async def generer_recommandations_equipe(analyses, evaluation, tests):
    """Génère des recommandations pour l'équipe PostgreSQL"""
    recommendations = {
        "prioritaires": [],
        "techniques": [],
        "optimisations": []
    }
    
    # Analyse conformité Pattern Factory
    agents_non_conformes = sum(1 for r in tests.values() 
                              if not r.get('conformite_pattern_factory', {}).get('conforme', False))
    
    if agents_non_conformes > 0:
        recommendations["prioritaires"].append(
            f"Migrer {agents_non_conformes} agents vers Pattern Factory"
        )
    
    # Analyse utilité
    agents_rejetes = len(evaluation.get('rejected_tools', []))
    if agents_rejetes > 0:
        recommendations["prioritaires"].append(
            f"Optimiser {agents_rejetes} agents avec score utilité faible"
        )
    
    # Recommandations techniques
    recommendations["techniques"].extend([
        "Standardiser les imports PostgreSQL (psycopg2, SQLAlchemy)",
        "Implémenter méthodes abstraites obligatoires Pattern Factory",
        "Ajouter logging standardisé avec self.logger",
        "Créer fonctions factory pour chaque agent"
    ])
    
    # Optimisations
    recommendations["optimisations"].extend([
        "Mutualiser code commun PostgreSQL dans module partagé",
        "Implémenter tests automatisés pour chaque agent",
        "Ajouter monitoring et métriques de performance",
        "Créer documentation technique standardisée"
    ])
    
    return recommendations

if __name__ == "__main__":
    print("🧪 TEST ÉQUIPE AGENTS POSTGRESQL - NEXTGENERATION")
    print("Mission: Analyse complète et évaluation de l'équipe PostgreSQL")
    print("=" * 70)
    
    asyncio.run(test_equipe_postgresql()) 



