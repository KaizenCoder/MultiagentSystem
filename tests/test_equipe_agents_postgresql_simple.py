#!/usr/bin/env python3
"""
🧪 TEST ÉQUIPE AGENTS POSTGRESQL - VERSION SIMPLIFIÉE
Test de l'équipe d'agents PostgreSQL avec notre agent testeur uniquement

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

async def test_equipe_postgresql_simple():
    """Test simplifié de l'équipe d'agents PostgreSQL"""
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
    
    # ===== ANALYSE AVEC AGENT TESTEUR =====
    print("\n" + "="*70)
    print("🧪 ANALYSE COMPLÈTE AVEC AGENT TESTEUR")
    print("="*70)
    
    # Créer l'agent testeur
    testeur = create_agent_testeur_agents(safe_mode=True, test_timeout=30)
    
    try:
        await testeur.startup()
        
        print("🏥 Agent Testeur initialisé")
        health = await testeur.health_check()
        print(f"   Status: {health['status']}")
        
        # Analyser chaque agent PostgreSQL
        resultats_analyse = {}
        scores_globaux = []
        
        for i, agent_file in enumerate(agents_postgresql, 1):
            print(f"\n🔍 [{i}/{len(agents_postgresql)}] Analyse: {agent_file.name}")
            print("-" * 50)
            
            # Test complet de l'agent
            test_result = await testeur.tester_agent(str(agent_file))
            resultats_analyse[agent_file.name] = test_result
            
            # Extraction des métriques importantes
            score_global = test_result.get('score_global', 0)
            scores_globaux.append(score_global)
            
            tests_syntaxe = test_result.get('test_syntaxe', {})
            conformite_pf = test_result.get('conformite_pattern_factory', {})
            methodes_obligatoires = test_result.get('test_methodes_obligatoires', {})
            
            # Affichage détaillé
            print(f"   📊 Score global: {score_global}/100")
            print(f"   ✅ Syntaxe: {'✅' if tests_syntaxe.get('valide', False) else '❌'}")
            print(f"   🏗️ Pattern Factory: {'✅' if conformite_pf.get('conforme', False) else '❌'}")
            print(f"   🔧 Méthodes obligatoires: {'✅' if methodes_obligatoires.get('toutes_presentes', False) else '❌'}")
            
            # Détails spécifiques PostgreSQL
            specialisation = analyser_specialisation_postgresql(agent_file.name, test_result)
            print(f"   🎯 Spécialisation: {specialisation}")
            
            # Problèmes détectés
            problemes = []
            if not tests_syntaxe.get('valide', False):
                problemes.extend(tests_syntaxe.get('erreurs', []))
            if not conformite_pf.get('conforme', False):
                problemes.extend(conformite_pf.get('problemes', []))
            
            if problemes:
                print(f"   ⚠️ Problèmes ({len(problemes)}):")
                for probleme in problemes[:3]:  # Max 3 pour lisibilité
                    print(f"      • {probleme}")
                if len(problemes) > 3:
                    print(f"      • ... et {len(problemes) - 3} autres")
            else:
                print(f"   ✅ Aucun problème détecté")
        
        await testeur.shutdown()
        
        # ===== STATISTIQUES GLOBALES =====
        print("\n" + "="*70)
        print("📊 STATISTIQUES ÉQUIPE POSTGRESQL")
        print("="*70)
        
        score_moyen = sum(scores_globaux) / len(scores_globaux) if scores_globaux else 0
        agents_conformes_pf = sum(1 for r in resultats_analyse.values() 
                                 if r.get('conformite_pattern_factory', {}).get('conforme', False))
        agents_syntaxe_ok = sum(1 for r in resultats_analyse.values() 
                               if r.get('test_syntaxe', {}).get('valide', False))
        
        print(f"📈 Score moyen équipe: {score_moyen:.1f}/100")
        print(f"🏗️ Agents conformes Pattern Factory: {agents_conformes_pf}/{len(agents_postgresql)} ({agents_conformes_pf/len(agents_postgresql)*100:.1f}%)")
        print(f"✅ Agents syntaxe valide: {agents_syntaxe_ok}/{len(agents_postgresql)} ({agents_syntaxe_ok/len(agents_postgresql)*100:.1f}%)")
        
        # Classification qualité
        if score_moyen >= 80:
            qualite = "EXCELLENTE"
            emoji = "🏆"
        elif score_moyen >= 60:
            qualite = "BONNE"
            emoji = "👍"
        elif score_moyen >= 40:
            qualite = "MOYENNE"
            emoji = "⚠️"
        else:
            qualite = "À AMÉLIORER"
            emoji = "🔧"
        
        print(f"\n{emoji} QUALITÉ ÉQUIPE: {qualite}")
        
        # ===== TOP/BOTTOM AGENTS =====
        print("\n" + "="*70)
        print("🏆 CLASSEMENT DES AGENTS")
        print("="*70)
        
        # Tri des agents par score
        agents_tries = sorted(
            [(nom, resultats['score_global']) for nom, resultats in resultats_analyse.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        print("🥇 TOP 3 AGENTS:")
        for i, (nom, score) in enumerate(agents_tries[:3], 1):
            specialisation = analyser_specialisation_postgresql(nom, resultats_analyse[nom])
            print(f"   {i}. {nom.replace('.py', '')}")
            print(f"      Score: {score}/100")
            print(f"      Spécialisation: {specialisation}")
        
        if len(agents_tries) > 3:
            print(f"\n🔧 AGENTS À AMÉLIORER:")
            for i, (nom, score) in enumerate(agents_tries[-3:], 1):
                if score < 60:  # Seuil d'amélioration
                    print(f"   {i}. {nom.replace('.py', '')}")
                    print(f"      Score: {score}/100")
                    print(f"      Priorité: HAUTE")
        
        # ===== RECOMMANDATIONS =====
        print("\n" + "="*70)
        print("💡 RECOMMANDATIONS POUR L'ÉQUIPE")
        print("="*70)
        
        recommendations = generer_recommandations_postgresql(resultats_analyse, score_moyen)
        
        print("🎯 PRIORITÉS:")
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
            "resultats_analyses": resultats_analyse,
            "statistiques": {
                "score_moyen": score_moyen,
                "agents_conformes_pf": agents_conformes_pf,
                "agents_syntaxe_ok": agents_syntaxe_ok,
                "taux_conformite_pf": agents_conformes_pf/len(agents_postgresql)*100,
                "qualite_equipe": qualite
            },
            "classement": agents_tries,
            "recommandations": recommendations
        }
        
        # Sauvegarde rapport
        rapport_file = f"test_equipe_postgresql_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(rapport_final, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {rapport_file}")
        
        # ===== RÉSUMÉ EXÉCUTIF =====
        print("\n" + "="*70)
        print("🎯 RÉSUMÉ EXÉCUTIF - ÉQUIPE AGENTS POSTGRESQL")
        print("="*70)
        
        print(f"✅ ANALYSE COMPLÈTE RÉALISÉE:")
        print(f"   📊 {len(agents_postgresql)} agents PostgreSQL analysés")
        print(f"   📈 Score équipe: {score_moyen:.1f}/100")
        print(f"   🏗️ {agents_conformes_pf} agents conformes Pattern Factory")
        print(f"   ✅ {agents_syntaxe_ok} agents syntaxiquement valides")
        
        print(f"\n🎖️ ÉVALUATION: {qualite}")
        
        if score_moyen >= 60:
            print(f"🚀 ÉQUIPE PRÊTE POUR INTÉGRATION NEXTGENERATION!")
        else:
            print(f"🔧 ÉQUIPE NÉCESSITE OPTIMISATIONS AVANT INTÉGRATION")
        
        return rapport_final
        
    except Exception as e:
        print(f"❌ Erreur test équipe PostgreSQL: {e}")
        if 'testeur' in locals():
            await testeur.shutdown()
        return None

def analyser_specialisation_postgresql(agent_name, test_result):
    """Analyse la spécialisation PostgreSQL d'un agent"""
    name_lower = agent_name.lower()
    
    specialisations = {
        "workspace_organizer": "🧹 Gestion workspace",
        "testing_specialist": "🧪 Tests automatisés",
        "web_researcher": "🔍 Recherche documentation",
        "sqlalchemy_fixer": "🔧 Réparation SQLAlchemy",
        "documentation_manager": "📚 Gestion documentation",
        "resolution_finale": "🎯 Résolution finale",
        "docker_specialist": "🐳 Conteneurisation",
        "diagnostic_postgres": "🩺 Diagnostic PostgreSQL",
        "windows_postgres": "🪟 PostgreSQL Windows"
    }
    
    for key, spec in specialisations.items():
        if key in name_lower:
            return spec
    
    return "🔧 Agent PostgreSQL général"

def generer_recommandations_postgresql(resultats_analyse, score_moyen):
    """Génère des recommandations spécifiques pour l'équipe PostgreSQL"""
    recommendations = {
        "prioritaires": [],
        "techniques": [],
        "optimisations": []
    }
    
    # Analyse des problèmes communs
    agents_non_conformes_pf = sum(1 for r in resultats_analyse.values() 
                                 if not r.get('conformite_pattern_factory', {}).get('conforme', False))
    
    agents_syntaxe_problemes = sum(1 for r in resultats_analyse.values() 
                                  if not r.get('test_syntaxe', {}).get('valide', False))
    
    # Recommandations prioritaires
    if agents_non_conformes_pf > 0:
        recommendations["prioritaires"].append(
            f"Migrer {agents_non_conformes_pf} agents vers Pattern Factory"
        )
    
    if agents_syntaxe_problemes > 0:
        recommendations["prioritaires"].append(
            f"Corriger erreurs syntaxe dans {agents_syntaxe_problemes} agents"
        )
    
    if score_moyen < 60:
        recommendations["prioritaires"].append(
            "Score équipe faible - Révision complète nécessaire"
        )
    
    # Actions techniques
    recommendations["techniques"].extend([
        "Standardiser imports PostgreSQL (psycopg2, SQLAlchemy)",
        "Implémenter méthodes abstraites Pattern Factory",
        "Ajouter logging standardisé",
        "Créer fonctions factory pour chaque agent",
        "Valider syntaxe Python avec linter"
    ])
    
    # Optimisations
    recommendations["optimisations"].extend([
        "Mutualiser code commun PostgreSQL",
        "Créer module partagé pour connexions DB",
        "Implémenter tests unitaires automatisés",
        "Ajouter documentation technique",
        "Optimiser performance et gestion mémoire"
    ])
    
    return recommendations

if __name__ == "__main__":
    print("🧪 TEST ÉQUIPE AGENTS POSTGRESQL - NEXTGENERATION")
    print("Mission: Analyse et évaluation complète de l'équipe PostgreSQL")
    print("=" * 70)
    
    asyncio.run(test_equipe_postgresql_simple()) 



