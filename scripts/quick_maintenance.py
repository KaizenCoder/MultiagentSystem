#!/usr/bin/env python3
"""
QUICK MAINTENANCE SCRIPT
========================

Script d'utilisation simplifiée pour l'Enhanced Maintenance Orchestrator.
Interface conviviale pour la maintenance rapide d'agents.

Usage:
    python quick_maintenance.py <target> [options]

Examples:
    python quick_maintenance.py agents/agent_exemple.py
    python quick_maintenance.py agents/ --scope directory
    python quick_maintenance.py . --scope project --target-score 90

Author: Équipe NextGeneration  
Version: Quick Access v1.0.0
"""

import asyncio
import sys
from pathlib import Path
import argparse

# Configuration du chemin
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from scripts.enhanced_maintenance_orchestrator import EnhancedMaintenanceOrchestrator
except ImportError as e:
    print(f"❌ Erreur: Enhanced Maintenance Orchestrator non trouvé: {e}")
    print("💡 Assurez-vous que le script est dans le bon répertoire")
    sys.exit(1)

def setup_argparse():
    """Configure l'analyseur d'arguments"""
    parser = argparse.ArgumentParser(
        description="Maintenance rapide avec Enhanced Orchestrator v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  Maintenance d'un agent spécifique:
    python quick_maintenance.py agents/agent_exemple.py

  Maintenance d'un répertoire d'agents:
    python quick_maintenance.py agents/ --scope directory

  Maintenance complète du projet:
    python quick_maintenance.py . --scope project --target-score 95

  Maintenance rapide avec moins d'itérations:
    python quick_maintenance.py agents/agent_test.py --max-iterations 3

  Mode verbose avec détails:
    python quick_maintenance.py agents/ --verbose
        """
    )
    
    parser.add_argument(
        "target",
        help="Chemin vers fichier/répertoire à maintenir"
    )
    
    parser.add_argument(
        "--scope",
        choices=["file", "directory", "project", "auto"],
        default="auto",
        help="Type de scope de maintenance (défaut: auto)"
    )
    
    parser.add_argument(
        "--target-score",
        type=int,
        default=85,
        metavar="N",
        help="Score de qualité cible 0-100 (défaut: 85)"
    )
    
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3,
        metavar="N",
        help="Nombre maximum d'itérations (défaut: 3)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbose avec détails"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulation sans modifications (analyse seulement)"
    )
    
    parser.add_argument(
        "--backup-only",
        action="store_true",
        help="Créer backup seulement, sans maintenance"
    )
    
    return parser

def validate_target(target_path: Path) -> bool:
    """Valide le chemin cible"""
    if not target_path.exists():
        print(f"❌ Erreur: Chemin non trouvé: {target_path}")
        return False
    
    if target_path.is_file() and not target_path.suffix == '.py':
        print(f"⚠️  Avertissement: {target_path} n'est pas un fichier Python")
        response = input("Continuer quand même? (y/N): ")
        return response.lower().startswith('y')
    
    return True

def print_banner():
    """Affiche la bannière du script"""
    print("=" * 70)
    print("🔧 QUICK MAINTENANCE - Enhanced Orchestrator v2.0")
    print("=" * 70)

def print_target_info(target_path: Path, scope: str):
    """Affiche les informations sur la cible"""
    print(f"🎯 Cible: {target_path}")
    print(f"📋 Scope: {scope}")
    
    if target_path.is_file():
        size = target_path.stat().st_size
        print(f"📊 Taille: {size:,} bytes")
    elif target_path.is_dir():
        py_files = list(target_path.rglob("*.py"))
        print(f"📊 Fichiers Python: {len(py_files)}")

async def create_backup_only(target_path: Path):
    """Mode backup seulement"""
    print("💾 MODE BACKUP SEULEMENT")
    
    orchestrator = EnhancedMaintenanceOrchestrator()
    backup = orchestrator.create_incremental_backup(target_path, "MANUAL_BACKUP", "quick_maintenance")
    
    print(f"✅ Backup créé: {backup.backup_path}")
    print(f"🕐 Timestamp: {backup.timestamp}")
    print(f"🔒 Checksum: {backup.checksum_before[:16]}...")
    
    return True

async def dry_run_analysis(target_path: Path, orchestrator: EnhancedMaintenanceOrchestrator):
    """Mode simulation - analyse seulement"""
    print("🔍 MODE SIMULATION - ANALYSE SEULEMENT")
    
    try:
        # Initialisation pour analyse
        await orchestrator.initialize_maintenance_team()
        
        # Validation pré-maintenance
        validation = await orchestrator.validate_comprehensive(target_path)
        
        print("\n📊 RÉSULTATS D'ANALYSE:")
        print(f"✅ Syntaxe valide: {validation.syntax_valid}")
        print(f"🛡️  Score sécurité: {validation.security_score:.1f}/100")
        print(f"🏆 Score qualité: {validation.quality_score:.1f}/100")
        print(f"⚙️  Test fonctionnel: {validation.functional_test}")
        
        if validation.issues:
            print(f"\n⚠️  Issues détectées ({len(validation.issues)}):")
            for i, issue in enumerate(validation.issues[:5], 1):
                print(f"  {i}. {issue}")
            if len(validation.issues) > 5:
                print(f"  ... et {len(validation.issues) - 5} autres")
        
        if validation.recommendations:
            print(f"\n💡 Recommandations ({len(validation.recommendations)}):")
            for i, rec in enumerate(validation.recommendations[:3], 1):
                print(f"  {i}. {rec}")
            if len(validation.recommendations) > 3:
                print(f"  ... et {len(validation.recommendations) - 3} autres")
        
        score_moyen = (validation.security_score + validation.quality_score) / 2
        
        if score_moyen >= orchestrator.target_quality_score:
            print(f"\n🎉 Qualité suffisante! Score: {score_moyen:.1f}/{orchestrator.target_quality_score}")
            print("ℹ️  Aucune maintenance nécessaire")
        else:
            print(f"\n🔧 Maintenance recommandée. Score actuel: {score_moyen:.1f}/{orchestrator.target_quality_score}")
            improvement_needed = orchestrator.target_quality_score - score_moyen
            print(f"📈 Amélioration nécessaire: +{improvement_needed:.1f} points")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant l'analyse: {e}")
        return False
    finally:
        await orchestrator.shutdown_maintenance_team()

async def execute_maintenance(target_path: Path, args):
    """Exécute la maintenance complète"""
    print("🔧 MODE MAINTENANCE COMPLÈTE")
    
    orchestrator = EnhancedMaintenanceOrchestrator(
        target_quality_score=args.target_score,
        max_iterations=args.max_iterations
    )
    
    try:
        result = await orchestrator.execute_maintenance_mission(
            str(target_path),
            args.scope
        )
        
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS DE LA MAINTENANCE")
        print("=" * 50)
        
        if result['success']:
            print("✅ Mission réussie!")
            print(f"📈 Score initial: {result['initial_score']:.1f}/100")
            print(f"🎯 Score final: {result['final_score']:.1f}/100")
            print(f"⬆️  Amélioration: {result['improvement']:+.1f} points")
            print(f"🎖️  Objectif atteint: {'✅ OUI' if result['target_achieved'] else '❌ NON'}")
            print(f"🔄 Itérations: {result['iterations']}")
            print(f"⏱️  Durée: {result['duration']:.2f}s")
            print(f"💾 Backups créés: {result['backups_created']}")
            
            if args.verbose:
                print(f"📁 Session ID: {result['session_id']}")
                print(f"📋 Rapports: {result['reports_dir']}")
            
            print("\n💡 Conseil: Consultez les rapports détaillés pour plus d'informations")
            
        else:
            print("❌ Mission échouée!")
            print(f"💥 Erreur: {result.get('error', 'Erreur inconnue')}")
            
        return result['success']
        
    except Exception as e:
        print(f"❌ Erreur durant la maintenance: {e}")
        return False

async def main():
    """Point d'entrée principal"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    print_banner()
    
    # Validation des arguments
    target_path = Path(args.target).resolve()
    if not validate_target(target_path):
        return 1
    
    # Validation score cible
    if not 0 <= args.target_score <= 100:
        print("❌ Erreur: Le score cible doit être entre 0 et 100")
        return 1
    
    print_target_info(target_path, args.scope)
    print()
    
    try:
        # Mode backup seulement
        if args.backup_only:
            success = await create_backup_only(target_path)
            return 0 if success else 1
        
        # Mode simulation
        if args.dry_run:
            orchestrator = EnhancedMaintenanceOrchestrator(target_quality_score=args.target_score)
            success = await dry_run_analysis(target_path, orchestrator)
            return 0 if success else 1
        
        # Mode maintenance complète
        success = await execute_maintenance(target_path, args)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Maintenance interrompue par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))