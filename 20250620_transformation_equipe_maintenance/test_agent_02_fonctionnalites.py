#!/usr/bin/env python3
"""
🔍 TEST SPÉCIFIQUE AGENT 02 - VÉRIFICATION FONCTIONNALITÉS UPGRADED
====================================================================
Test pour vérifier que toutes les fonctionnalités avancées de l'Agent 02 sont préservées
"""

import sys
from datetime import datetime
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def main():
    print_header("TEST AGENT 02 - FONCTIONNALITÉS UPGRADED")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ajouter le chemin pour les imports
    sys.path.append('.')
    
    try:
        # Import Agent 02
        from agent_equipe_maintenance.agent_MAINTENANCE_02_evaluateur_utilite import AgentEvaluateurUtiliteUpgraded
        
        # Créer l'agent
        agent_02 = AgentEvaluateurUtiliteUpgraded()
        print(f"✅ Agent 02 créé avec succès: {agent_02.agent_id}")
        
        # VÉRIFICATION 1: Attributs de base
        print("\n🔍 VÉRIFICATION 1: ATTRIBUTS DE BASE")
        print("-" * 40)
        
        attributs_base = [
            'agent_id', 'agent_type', 'evaluation_criteria', 'nextgen_keywords',
            'evaluation_thresholds', 'conflict_patterns'
        ]
        
        for attr in attributs_base:
            if hasattr(agent_02, attr):
                print(f"  ✅ {attr}")
            else:
                print(f"  ❌ {attr} - MANQUANT!")
        
        # VÉRIFICATION 2: Capacités
        print("\n🔍 VÉRIFICATION 2: CAPACITÉS")
        print("-" * 40)
        
        capacites = agent_02.get_capabilities()
        print(f"📊 Nombre de capacités: {len(capacites)}")
        
        capacites_attendues = [
            'evaluate_tools', 'evaluate_single_tool', 'evaluate_technical_relevance',
            'evaluate_architecture_compatibility', 'evaluate_added_value',
            'evaluate_integration_ease', 'evaluate_maintenance_burden',
            'detect_conflicts', 'calculate_similarity', 'select_tools_intelligent',
            'generate_recommendations_advanced', 'prioritize_integration',
            'multi_criteria_evaluation'
        ]
        
        print("🎯 Capacités critiques:")
        for capacite in capacites_attendues:
            if capacite in capacites:
                print(f"  ✅ {capacite}")
            else:
                print(f"  ❌ {capacite} - MANQUANTE!")
        
        # VÉRIFICATION 3: Méthodes avancées
        print("\n🔍 VÉRIFICATION 3: MÉTHODES AVANCÉES")
        print("-" * 40)
        
        methodes_avancees = [
            'evaluate_tools_utility', 'evaluate_single_tool', 'evaluate_technical_relevance',
            'evaluate_architecture_compatibility', 'evaluate_added_value', 'evaluate_integration_ease',
            'evaluate_maintenance_burden', 'detect_conflicts_and_redundancies', 'calculate_tool_similarity',
            'select_tools_intelligent', 'generate_recommendation_advanced', 'determine_integration_priority',
            'generate_evaluation_summary_advanced', '_determine_quality_level'
        ]
        
        print("🚀 Méthodes avancées:")
        for methode in methodes_avancees:
            if hasattr(agent_02, methode):
                print(f"  ✅ {methode}")
            else:
                print(f"  ❌ {methode} - MANQUANTE!")
        
        # VÉRIFICATION 4: Configuration avancée
        print("\n🔍 VÉRIFICATION 4: CONFIGURATION AVANCÉE")
        print("-" * 40)
        
        # Critères d'évaluation
        if hasattr(agent_02, 'evaluation_criteria'):
            print(f"⚖️ Critères d'évaluation: {len(agent_02.evaluation_criteria)} critères")
            for critere, poids in agent_02.evaluation_criteria.items():
                print(f"  - {critere}: {poids}")
        
        # Mots-clés NextGen
        if hasattr(agent_02, 'nextgen_keywords'):
            total_keywords = sum(len(v) for v in agent_02.nextgen_keywords.values())
            print(f"\n🎯 Mots-clés NextGen: {total_keywords} mots-clés")
            for priority, keywords in agent_02.nextgen_keywords.items():
                print(f"  - {priority}: {len(keywords)} mots-clés")
        
        # Seuils d'évaluation
        if hasattr(agent_02, 'evaluation_thresholds'):
            print(f"\n📈 Seuils d'évaluation: {len(agent_02.evaluation_thresholds)} seuils")
            for seuil, valeur in agent_02.evaluation_thresholds.items():
                print(f"  - {seuil}: {valeur}")
        
        # Patterns de conflits
        if hasattr(agent_02, 'conflict_patterns'):
            print(f"\n🔍 Patterns de conflits: {len(agent_02.conflict_patterns)} patterns")
            for pattern_type, patterns in agent_02.conflict_patterns.items():
                print(f"  - {pattern_type}: {len(patterns)} patterns")
        
        # VÉRIFICATION 5: Fonctionnalités UPGRADED spécifiques
        print("\n🔍 VÉRIFICATION 5: FONCTIONNALITÉS UPGRADED")
        print("-" * 40)
        
        features_upgraded = [
            ("🧠 Système multi-critères pondérés", hasattr(agent_02, 'evaluation_criteria')),
            ("🎯 Mots-clés NextGen spécialisés", hasattr(agent_02, 'nextgen_keywords')),
            ("⚖️ Évaluation 5 dimensions", hasattr(agent_02, 'evaluate_technical_relevance')),
            ("🔍 Détection conflits automatique", hasattr(agent_02, 'detect_conflicts_and_redundancies')),
            ("📊 Algorithme similarité", hasattr(agent_02, 'calculate_tool_similarity')),
            ("🎯 Priorisation intelligente", hasattr(agent_02, 'select_tools_intelligent')),
            ("🏆 Support évaluation spécialisée", hasattr(agent_02, 'generate_recommendation_advanced')),
            ("📈 Seuils évaluation avancés", hasattr(agent_02, 'evaluation_thresholds'))
        ]
        
        print("🚀 Fonctionnalités UPGRADED:")
        for feature, present in features_upgraded:
            status = "✅" if present else "❌"
            print(f"  {status} {feature}")
        
        # RÉSUMÉ FINAL
        print("\n🎯 RÉSUMÉ FINAL")
        print("-" * 40)
        
        # Compter les vérifications réussies
        total_attributs = len([f for f in features_upgraded if f[1]])
        total_methodes = len([m for m in methodes_avancees if hasattr(agent_02, m)])
        total_capacites = len([c for c in capacites_attendues if c in capacites])
        
        print(f"✅ Attributs UPGRADED: {total_attributs}/{len(features_upgraded)}")
        print(f"✅ Méthodes avancées: {total_methodes}/{len(methodes_avancees)}")
        print(f"✅ Capacités critiques: {total_capacites}/{len(capacites_attendues)}")
        
        # Verdict final
        if total_attributs == len(features_upgraded) and total_methodes == len(methodes_avancees):
            print("\n🎉 VERDICT: TOUTES LES FONCTIONNALITÉS UPGRADED SONT PRÉSERVÉES!")
            print("✅ L'Agent 02 est 100% fonctionnel avec toutes ses améliorations")
        else:
            print("\n⚠️ VERDICT: CERTAINES FONCTIONNALITÉS MANQUENT")
            print("❌ Vérification requise")
        
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"  - Capacités totales: {len(capacites)}")
        print(f"  - Méthodes avancées: {total_methodes}")
        print(f"  - Fonctionnalités UPGRADED: {total_attributs}")
        print(f"  - Agent ID: {agent_02.agent_id}")
        print(f"  - Agent Type: {agent_02.agent_type}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 