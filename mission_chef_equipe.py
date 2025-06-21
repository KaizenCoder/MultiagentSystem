#!/usr/bin/env python3
"""
🚀 MISSION CHEF D'ÉQUIPE - ANALYSE AGENTS FACTORY
================================================================
Coordination de l'équipe de maintenance pour analyser tous les agents
présents dans agent_factory_implementation/agents
"""

import sys
import os
from pathlib import Path

# Import du chef d'équipe coordinateur
from agent_factory_implementation.agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_0_chef_equipe_coordinateur

def main():
    # Configuration de la mission
    mission_analyse = {
        'objectif': 'Analyser tous les agents présents dans le répertoire agent_factory_implementation/agents',
        'repertoire_cible': 'C:/Dev/nextgeneration/agent_factory_implementation/agents',
        'exclusions': ['sous-répertoires', '__pycache__', 'reviews', 'tools', 'concrete'],
        'rapport_destination': 'C:/Dev/nextgeneration/agent_factory_implementation/agents/reviews',
        'coordination_requise': True,
        'equipe_disponible': [
            'analyseur_structure', 
            'evaluateur_utilite', 
            'adaptateur_code', 
            'testeur_anti_faux', 
            'documenteur', 
            'validateur_final'
        ]
    }
    
    print('🚀 LANCEMENT MISSION - CHEF D\'ÉQUIPE COORDINATEUR')
    print(f'📁 Répertoire cible: {mission_analyse["repertoire_cible"]}')
    print(f'📊 Rapport destination: {mission_analyse["rapport_destination"]}')
    print('⚡ Coordination équipe demandée...')
    print()
    
    try:
        # Création du chef d'équipe coordinateur
        print("👨‍💼 Création du Chef d'Équipe Coordinateur...")
        chef_equipe = create_agent_0_chef_equipe_coordinateur(
            target_path=mission_analyse['repertoire_cible'],
            workspace_path='.',
            safe_mode=True
        )
        
        print("✅ Chef d'équipe créé avec succès!")
        print()
        
        # Vérification des méthodes disponibles
        print("🔍 Méthodes disponibles du chef d'équipe:")
        methodes = [m for m in dir(chef_equipe) if not m.startswith('_')]
        for methode in methodes:
            print(f"  - {methode}")
        print()
        
        # Lancement de l'analyse coordonnée
        print("🎯 Lancement de l'analyse coordonnée...")
        
        # Utilisation de la méthode de coordination principale
        if hasattr(chef_equipe, 'coordonner_analyse_complete'):
            resultat = chef_equipe.coordonner_analyse_complete(
                repertoire=mission_analyse['repertoire_cible'],
                destination=mission_analyse['rapport_destination']
            )
        elif hasattr(chef_equipe, 'analyser_agents_repertoire'):
            resultat = chef_equipe.analyser_agents_repertoire(
                repertoire=mission_analyse['repertoire_cible'],
                destination_rapport=mission_analyse['rapport_destination'],
                coordination_equipe=True
            )
        else:
            # Utilisation de la méthode principale de coordination
            resultat = chef_equipe.execute_main_task()
            
        print()
        print('✅ MISSION TERMINÉE!')
        print(f'📋 Résultat: {resultat}')
        
        return resultat
        
    except Exception as e:
        print(f"❌ Erreur durant la mission: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main() 



