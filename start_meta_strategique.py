#!/usr/bin/env python3
"""
🚧 DRAFT VERSION 🚧
Script de démarrage pour l'Agent Méta-Stratégique - VERSION DRAFT/PROTOTYPE
Usage: python start_meta_strategique.py [options]

⚠️ ATTENTION: CETTE VERSION EST UN PROTOTYPE EN DÉVELOPPEMENT
- Ne pas utiliser en production
- Fonctionnalités en cours de test et validation
- Rapports générés à titre expérimental uniquement
"""

import argparse
import logging
import sys
from pathlib import Path

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "agent_factory_implementation" / "agents"))

from agent_meta_strategique import AgentMetaStrategique
from agent_factory_implementation.agents.agent_meta_strategique_scheduler import AgentMetaStrategiqueScheduler

def setup_logging(log_level: str = "INFO"):
    """Configuration du logging"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/agent_meta_strategique.log'),
            logging.StreamHandler()
        ]
    )

def run_single_analysis():
    """Exécution d'une analyse unique"""
    print("🚧 Exécution d'une analyse stratégique unique (VERSION DRAFT/PROTOTYPE)...")
    print("⚠️  ATTENTION: Version expérimentale - Ne pas utiliser en production")
    
    agent = AgentMetaStrategique()
    
    # Génération du rapport
    rapport_path = agent.sauvegarder_rapport_strategique()
    print(f"✅ Rapport généré: {rapport_path}")
    
    # Affichage du résumé
    analysis = agent.analyser_performance_globale()
    print(f"\n📊 Résumé de l'analyse:")
    print(f"- Insights identifiés: {len(analysis['strategic_insights'])}")
    print(f"- Missions proposées: {len(analysis['proposed_missions'])}")
    print(f"- Anomalies détectées: {len(analysis['anomalies_detected'])}")
    
    # Affichage des insights critiques
    critical_insights = [i for i in analysis['strategic_insights'] if i['severity'] in ['HIGH', 'CRITICAL']]
    if critical_insights:
        print(f"\n🚨 {len(critical_insights)} insights critiques détectés:")
        for insight in critical_insights:
            print(f"  - {insight['severity']}: {insight['title']}")

def run_scheduler():
    """Démarrage du planificateur"""
    print("🚧 Démarrage du planificateur Agent Méta-Stratégique DRAFT/PROTOTYPE")
    print("⚠️  ATTENTION: Version expérimentale - Ne pas utiliser en production")
    print("   Ctrl+C pour arrêter")
    
    scheduler = AgentMetaStrategiqueScheduler()
    scheduler.start_scheduler()

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Agent Méta-Stratégique NextGeneration (VERSION DRAFT/PROTOTYPE)")
    
    parser.add_argument(
        '--mode', 
        choices=['single', 'scheduler'], 
        default='single',
        help='Mode d\'exécution: single (analyse unique) ou scheduler (planificateur)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Niveau de logging'
    )
    
    parser.add_argument(
        '--config',
        help='Chemin vers le fichier de configuration personnalisé'
    )
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(args.log_level)
    
    # Création du répertoire logs si nécessaire
    Path('logs').mkdir(exist_ok=True)
    
    try:
        if args.mode == 'single':
            run_single_analysis()
        elif args.mode == 'scheduler':
            run_scheduler()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 