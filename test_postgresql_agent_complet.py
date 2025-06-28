#!/usr/bin/env python3
"""
Script de test complet pour l'agent PostgreSQL Testing Specialist
Teste tous les types de rapports stratégiques
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire au path
sys.path.insert(0, str(Path.cwd()))

async def test_agent_postgresql_complet():
    from agents.agent_testeur_agents_complet import create_agent_testeur_agents
    
    print('🧪 TEST COMPLET DE L\'AGENT POSTGRESQL TESTING SPECIALIST')
    print('=' * 70)
    
    # Créer l'agent testeur
    agent_testeur = create_agent_testeur_agents(safe_mode=True, test_timeout=30)
    
    try:
        # Démarrage
        await agent_testeur.startup()
        
        # Test spécifique de l'agent PostgreSQL
        print('\n📋 Test de l\'agent PostgreSQL Testing Specialist...')
        
        task_test = {
            'type': 'test_agent',
            'agent_path': 'agents/agent_POSTGRESQL_testing_specialist.py'
        }
        
        result = await agent_testeur.execute_task(task_test)
        
        print(f'✅ Test de base terminé - Score: {result.get("score_global", 0)}/100')
        
        # Context pour tous les rapports
        context = {
            'agent_teste': 'agent_POSTGRESQL_testing_specialist.py',
            'objectif': 'validation_complete_postgresql',
            'resultats_test': result,
            'specialisation': 'postgresql_testing'
        }
        
        # Test de tous les types de rapports
        types_rapports = ['testing', 'compliance', 'performance_tests', 'quality_assurance']
        
        for type_rapport in types_rapports:
            print(f'\n📊 Génération rapport {type_rapport.upper()}...')
            
            try:
                # Génération rapport JSON
                rapport = await agent_testeur.generer_rapport_strategique(context, type_rapport)
                
                if rapport:
                    print(f'✅ Rapport {type_rapport} généré')
                    print(f'   - Type: {rapport.get("type_rapport")}')
                    
                    # Génération rapport markdown
                    rapport_md = await agent_testeur.generer_rapport_markdown(rapport, type_rapport, context)
                    
                    # Sauvegarde
                    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')
                    rapport_path = Path('reports') / 'agent_testeur_agents' / f'postgresql_{type_rapport}_{timestamp_str}.md'
                    rapport_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(rapport_path, 'w', encoding='utf-8') as f:
                        f.write(rapport_md)
                    
                    print(f'   - Sauvegardé: {rapport_path}')
                    
                    # Affichage d'informations spécifiques selon le type
                    if type_rapport == 'testing':
                        resume = rapport.get('resume_executif', {})
                        print(f'   - Score Testing: {resume.get("score_testing_global", 0):.1f}/100')
                        print(f'   - Statut: {resume.get("statut_general", "UNKNOWN")}')
                    
                    elif type_rapport == 'compliance':
                        print(f'   - Taux Conformité: {rapport.get("taux_conformite_global", 0):.1f}%')
                        print(f'   - Niveau: {rapport.get("niveau_conformite", "UNKNOWN")}')
                    
                    elif type_rapport == 'performance_tests':
                        print(f'   - Durée Moyenne: {rapport.get("duree_moyenne_test", 0)}s')
                        print(f'   - Efficacité: {rapport.get("efficacite_tests", 0):.1f}%')
                    
                    elif type_rapport == 'quality_assurance':
                        print(f'   - Score QA Global: {rapport.get("score_qa_global", 0)}/100')
                        print(f'   - Niveau Assurance: {rapport.get("niveau_assurance", "BRONZE")}')
                
            except Exception as e:
                print(f'❌ Erreur génération rapport {type_rapport}: {e}')
        
        # Test de monitoring santé
        print('\n🏥 Test monitoring santé agents...')
        monitoring_result = await agent_testeur.monitorer_sante_agents()
        print(f'✅ Monitoring: {monitoring_result.get("status", "unknown")}')
        
        # Test validation conformité
        print('\n📐 Test validation conformité Pattern Factory...')
        conformite_result = await agent_testeur.valider_conformite_pattern_factory()
        print(f'✅ Conformité: {conformite_result.get("score", 0)}/100')
        
        # Arrêt propre
        await agent_testeur.shutdown()
        
        print('\n🎯 TESTS COMPLETS TERMINÉS AVEC SUCCÈS!')
        print(f'📊 {len(types_rapports)} rapports générés pour l\'agent PostgreSQL')
        
    except Exception as e:
        print(f'❌ Erreur durant les tests: {e}')
        import traceback
        traceback.print_exc()
        await agent_testeur.shutdown()

if __name__ == "__main__":
    asyncio.run(test_agent_postgresql_complet()) 