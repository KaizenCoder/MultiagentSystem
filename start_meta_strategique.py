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
import sys
from pathlib import Path

# Golden Source Logging
from core import logging_manager

# Ajout du chemin pour les imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "agent_factory_implementation" / "agents"))

from agent_meta_strategique import AgentMetaStrategique
from agent_factory_implementation.agents.agent_meta_strategique_scheduler import AgentMetaStrategiqueScheduler

logger = None

def setup_logging(log_level: str = "INFO", es_enabled: bool = False):
    """Configuration du logging avec la Golden Source."""
    global logger
    logger = logging_manager.get_logger(
        'MetaStrategiqueRunner', 
        custom_config={"log_level": log_level.upper(), "elasticsearch_enabled": es_enabled}
    )
    logger.info(f"Logging initialisé au niveau {log_level.upper()}. Elasticsearch: {'activé' if es_enabled else 'désactivé'}.")

def run_single_analysis():
    """Exécution d'une analyse unique"""
    print("🚧 Exécution d'une analyse stratégique unique (VERSION DRAFT/PROTOTYPE)...")
    print("⚠️  ATTENTION: Version expérimentale - Ne pas utiliser en production")
    
    if not logger:
        setup_logging()
    logger.info("Début de l'analyse stratégique unique.")
    
    agent = AgentMetaStrategique()
    
    # Génération du rapport
    rapport_path = agent.sauvegarder_rapport_strategique()
    print(f"✅ Rapport généré: {rapport_path}")
    
    # Affichage du résumé
    analysis = agent.analyser_performance_globale()
    logger.info(f"Analyse terminée. {len(analysis['strategic_insights'])} insights, {len(analysis['proposed_missions'])} missions, {len(analysis['anomalies_detected'])} anomalies.")
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
    
    if not logger:
        setup_logging()
    logger.info("Démarrage du planificateur de l'agent méta-stratégique.")
    
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
        help='Niveau de logging.'
    )
    
    parser.add_argument(
        '--es',
        action='store_true',
        help="Activer le logging vers Elasticsearch."
    )
    
    parser.add_argument(
        '--config',
        help='Chemin vers le fichier de configuration personnalisé'
    )
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(args.log_level, args.es)
    
    # Création du répertoire logs si nécessaire
    Path('logs').mkdir(exist_ok=True)
    
    try:
        if args.mode == 'single':
            run_single_analysis()
        elif args.mode == 'scheduler':
            run_scheduler()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        if logger:
            logger.warning("Arrêt demandé par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if logger:
            logger.critical(f"Erreur non gérée: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 



