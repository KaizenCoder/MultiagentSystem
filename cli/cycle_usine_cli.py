#!/usr/bin/env python3
"""
🏭 CYCLE-USINE CLI - INTERFACE UTILISATEUR NEXTGENERATION
========================================================

Interface en ligne de commande pour le Cycle-Usine v1:
- Création interactive de projets
- Suivi en temps réel des cycles
- Gestion des templates et configurations
- Historique et métriques

Usage:
    python cycle_usine_cli.py create --project "my_api" --type api
    python cycle_usine_cli.py status --cycle-id abc123
    python cycle_usine_cli.py list
    python cycle_usine_cli.py metrics

Version: 1.0.0
Author: Claude Sonnet 4 (NextGeneration Team)  
Created: 2025-06-28
"""

import asyncio
import argparse
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cycle_usine_v1 import (
    CycleUsineV1,
    CycleRequest,
    create_initialized_cycle_usine
)

class CycleUsineCLI:
    """
    🏭 CLI pour Cycle-Usine v1
    
    Interface complète pour:
    - Création et configuration de projets
    - Monitoring des cycles en cours
    - Gestion des templates
    - Analytics et métriques
    """
    
    def __init__(self):
        self.config_file = Path.home() / ".cycle_usine_config.json"
        self.config = self.load_config()
        self.cycle_usine: Optional[CycleUsineV1] = None
        
    def load_config(self) -> Dict[str, Any]:
        """Charge configuration utilisateur"""
        
        default_config = {
            "workspace_path": "/mnt/c/Dev/nextgeneration",
            "default_complexity": "medium",
            "default_framework": "fastapi",
            "auto_deploy": False,
            "notifications": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Erreur lecture config: {e}")
        
        return default_config
    
    def save_config(self):
        """Sauvegarde configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde config: {e}")
    
    async def initialize_cycle_usine(self):
        """Initialise le cycle-usine"""
        if not self.cycle_usine:
            print("🔧 Initialisation Cycle-Usine...")
            self.cycle_usine = await create_initialized_cycle_usine(self.config)
            print("✅ Cycle-Usine prêt")
    
    async def cmd_create(self, args) -> int:
        """Commande create - Créer nouveau projet"""
        
        try:
            await self.initialize_cycle_usine()
            
            # Collecte des paramètres
            project_name = args.project or self.prompt_input("Nom du projet")
            project_type = args.type or self.prompt_choice(
                "Type de projet", 
                ["api", "service", "agent", "tool"], 
                self.config.get("default_type", "api")
            )
            complexity = args.complexity or self.prompt_choice(
                "Complexité",
                ["simple", "medium", "complex", "enterprise"],
                self.config.get("default_complexity", "medium")
            )
            
            # Requirements
            if args.requirements:
                requirements = args.requirements
            else:
                print("\n📝 Décrivez votre projet (Entrée vide pour terminer):")
                requirements_lines = []
                while True:
                    line = input("> ").strip()
                    if not line:
                        break
                    requirements_lines.append(line)
                requirements = "\n".join(requirements_lines)
            
            # Contraintes optionnelles
            constraints = {}
            if args.framework:
                constraints["framework"] = args.framework
            if args.database:
                constraints["database"] = args.database
            
            # Création de la requête
            request = CycleRequest(
                request_id=f"{project_name}_{int(time.time())}",
                project_name=project_name,
                requirements=requirements,
                target_type=project_type,
                complexity_level=complexity,
                constraints=constraints,
                created_at=datetime.now(),
                priority=args.priority or "medium"
            )
            
            print(f"\n🏭 Démarrage cycle pour '{project_name}'...")
            print(f"📋 Type: {project_type} | Complexité: {complexity}")
            print("-" * 50)
            
            # Exécution avec monitoring
            start_time = time.time()
            result = await self.cycle_usine.execute_cycle(request)
            total_time = time.time() - start_time
            
            # Affichage résultat
            if result.success:
                print(f"\n🎉 SUCCÈS: Projet '{project_name}' créé!")
                print(f"📊 Score qualité: {result.quality_score:.1f}%")
                print(f"⏱️ Temps total: {total_time:.2f}s")
                print(f"📁 Artifacts: {len(result.final_artifacts)}")
                
                if result.final_artifacts:
                    print("\n📁 Fichiers générés:")
                    for artifact in result.final_artifacts:
                        print(f"  - {artifact}")
                
                return 0
            else:
                print(f"\n❌ ÉCHEC: Erreurs lors de la création")
                print(f"📊 Score partiel: {result.quality_score:.1f}%")
                
                # Affichage erreurs par étape
                for stage_name, stage_result in result.stages_results.items():
                    if hasattr(stage_result, 'error') and stage_result.error:
                        print(f"  {stage_name}: {stage_result.error}")
                
                return 1
                
        except Exception as e:
            print(f"❌ Erreur création: {e}")
            return 2
    
    async def cmd_status(self, args) -> int:
        """Commande status - Statut cycle"""
        
        try:
            cycle_id = args.cycle_id
            
            if not cycle_id:
                print("❌ ID de cycle requis")
                return 1
            
            # Recherche résultat cycle
            results_dir = Path(self.config["workspace_path"]) / "cycle_usine" / "results"
            result_files = list(results_dir.glob(f"cycle_result_{cycle_id}*.json"))
            
            if not result_files:
                print(f"❌ Cycle '{cycle_id}' non trouvé")
                return 1
            
            # Lecture résultat
            with open(result_files[0], 'r', encoding='utf-8') as f:
                result_data = json.load(f)
            
            # Affichage statut
            print(f"🏭 CYCLE: {result_data['request_id']}")
            print("=" * 50)
            print(f"Succès: {'✅' if result_data['success'] else '❌'}")
            print(f"Score qualité: {result_data['quality_score']:.1f}%")
            print(f"Temps total: {result_data['total_execution_time_ms']:.0f}ms")
            print(f"Créé: {result_data['created_at']}")
            print(f"Terminé: {result_data.get('completed_at', 'En cours')}")
            
            # Détail étapes
            print(f"\n📋 ÉTAPES:")
            for stage_name, stage_data in result_data['stages_results'].items():
                status_icon = "✅" if stage_data['status'] == "completed" else "❌" if stage_data['status'] == "failed" else "⏳"
                print(f"  {status_icon} {stage_name}: {stage_data['status']}")
                if stage_data.get('error'):
                    print(f"    ↳ Erreur: {stage_data['error']}")
            
            # Artifacts
            if result_data['final_artifacts']:
                print(f"\n📁 ARTIFACTS ({len(result_data['final_artifacts'])}):")
                for artifact in result_data['final_artifacts']:
                    print(f"  - {artifact}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Erreur statut: {e}")
            return 2
    
    async def cmd_list(self, args) -> int:
        """Commande list - Liste cycles"""
        
        try:
            results_dir = Path(self.config["workspace_path"]) / "cycle_usine" / "results"
            
            if not results_dir.exists():
                print("📂 Aucun cycle trouvé")
                return 0
            
            result_files = list(results_dir.glob("cycle_result_*.json"))
            
            if not result_files:
                print("📂 Aucun cycle trouvé")
                return 0
            
            # Tri par date
            result_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            print(f"🏭 CYCLES RÉCENTS ({len(result_files)})")
            print("=" * 80)
            print(f"{'ID':<25} {'Projet':<20} {'Type':<10} {'Succès':<8} {'Score':<8} {'Date':<20}")
            print("-" * 80)
            
            for result_file in result_files[:args.limit or 10]:
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    request_id = data['request_id'][:24]
                    # Extraction nom projet du request_id ou utilisation fallback
                    project_name = request_id.split('_')[0] if '_' in request_id else "unknown"
                    project_name = project_name[:19]
                    
                    # Type depuis stages_results ou fallback
                    target_type = "unknown"
                    if 'target_type' in data:
                        target_type = data['target_type'][:9]
                    
                    success_icon = "✅" if data['success'] else "❌"
                    score = f"{data['quality_score']:.1f}%"
                    created_date = data['created_at'][:19] if 'created_at' in data else "N/A"
                    
                    print(f"{request_id:<25} {project_name:<20} {target_type:<10} {success_icon:<8} {score:<8} {created_date:<20}")
                    
                except Exception as e:
                    print(f"⚠️ Erreur lecture {result_file.name}: {e}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Erreur liste: {e}")
            return 2
    
    async def cmd_metrics(self, args) -> int:
        """Commande metrics - Métriques globales"""
        
        try:
            await self.initialize_cycle_usine()
            
            # Métriques cycle-usine
            metrics = await self.cycle_usine.get_cycle_metrics()
            
            print("📊 MÉTRIQUES CYCLE-USINE")
            print("=" * 40)
            print(f"Version: {metrics['version']}")
            print(f"Cycles exécutés: {metrics['metrics']['cycles_executed']}")
            print(f"Taux de succès: {metrics['metrics']['success_rate']:.1f}%")
            print(f"Temps moyen: {metrics['metrics']['avg_execution_time']:.0f}ms")
            print(f"Agents disponibles: {len(metrics['agents_available'])}")
            print(f"LLM Gateway: {'✅' if metrics['llm_gateway_connected'] else '❌'}")
            
            # Analyse historique
            results_dir = Path(self.config["workspace_path"]) / "cycle_usine" / "results"
            if results_dir.exists():
                result_files = list(results_dir.glob("cycle_result_*.json"))
                
                if result_files:
                    print(f"\n📈 HISTORIQUE ({len(result_files)} cycles)")
                    print("-" * 30)
                    
                    success_count = 0
                    total_quality = 0
                    total_time = 0
                    
                    for result_file in result_files:
                        try:
                            with open(result_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            if data['success']:
                                success_count += 1
                            total_quality += data['quality_score']
                            total_time += data['total_execution_time_ms']
                            
                        except Exception:
                            continue
                    
                    if len(result_files) > 0:
                        print(f"Taux succès historique: {(success_count / len(result_files)) * 100:.1f}%")
                        print(f"Score qualité moyen: {total_quality / len(result_files):.1f}%")
                        print(f"Temps moyen historique: {total_time / len(result_files):.0f}ms")
            
            return 0
            
        except Exception as e:
            print(f"❌ Erreur métriques: {e}")
            return 2
    
    async def cmd_config(self, args) -> int:
        """Commande config - Configuration"""
        
        try:
            if args.set:
                # Format: key=value
                if '=' not in args.set:
                    print("❌ Format: --set key=value")
                    return 1
                
                key, value = args.set.split('=', 1)
                
                # Conversion types
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                
                self.config[key] = value
                self.save_config()
                print(f"✅ Configuration mise à jour: {key} = {value}")
                
            elif args.get:
                if args.get in self.config:
                    print(f"{args.get} = {self.config[args.get]}")
                else:
                    print(f"❌ Clé '{args.get}' non trouvée")
                    return 1
            else:
                # Affichage config complète
                print("⚙️ CONFIGURATION")
                print("=" * 30)
                for key, value in self.config.items():
                    print(f"{key}: {value}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
            return 2
    
    def prompt_input(self, message: str, default: str = None) -> str:
        """Prompt input utilisateur"""
        prompt = f"{message}"
        if default:
            prompt += f" [{default}]"
        prompt += ": "
        
        response = input(prompt).strip()
        return response if response else (default or "")
    
    def prompt_choice(self, message: str, choices: List[str], default: str = None) -> str:
        """Prompt choix utilisateur"""
        print(f"\n{message}:")
        for i, choice in enumerate(choices, 1):
            marker = " (défaut)" if choice == default else ""
            print(f"  {i}. {choice}{marker}")
        
        while True:
            try:
                response = input("Choix [1-{}]: ".format(len(choices))).strip()
                
                if not response and default:
                    return default
                
                if response.isdigit():
                    idx = int(response) - 1
                    if 0 <= idx < len(choices):
                        return choices[idx]
                
                print("❌ Choix invalide")
                
            except KeyboardInterrupt:
                print("\n⚠️ Annulé")
                exit(1)

def create_parser() -> argparse.ArgumentParser:
    """Crée parser CLI"""
    
    parser = argparse.ArgumentParser(
        description="🏭 Cycle-Usine CLI - Automation NextGeneration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s create --project "user_api" --type api --complexity medium
  %(prog)s status --cycle-id user_api_1672531200  
  %(prog)s list --limit 5
  %(prog)s metrics
  %(prog)s config --set default_framework=fastapi
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande create
    create_parser = subparsers.add_parser('create', help='Créer nouveau projet')
    create_parser.add_argument('--project', help='Nom du projet')
    create_parser.add_argument('--type', choices=['api', 'service', 'agent', 'tool'], help='Type de projet')
    create_parser.add_argument('--complexity', choices=['simple', 'medium', 'complex', 'enterprise'], help='Niveau de complexité')
    create_parser.add_argument('--requirements', help='Description des requirements')
    create_parser.add_argument('--framework', help='Framework à utiliser')
    create_parser.add_argument('--database', help='Base de données')
    create_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='Priorité')
    
    # Commande status
    status_parser = subparsers.add_parser('status', help='Statut d\'un cycle')
    status_parser.add_argument('--cycle-id', required=True, help='ID du cycle')
    
    # Commande list
    list_parser = subparsers.add_parser('list', help='Lister les cycles')
    list_parser.add_argument('--limit', type=int, default=10, help='Nombre max de cycles à afficher')
    
    # Commande metrics
    metrics_parser = subparsers.add_parser('metrics', help='Métriques globales')
    
    # Commande config
    config_parser = subparsers.add_parser('config', help='Configuration')
    config_parser.add_argument('--set', help='Définir configuration (key=value)')
    config_parser.add_argument('--get', help='Obtenir valeur configuration')
    
    return parser

async def main():
    """Point d'entrée principal"""
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = CycleUsineCLI()
    
    try:
        # Dispatch commandes
        if args.command == 'create':
            return await cli.cmd_create(args)
        elif args.command == 'status':
            return await cli.cmd_status(args)
        elif args.command == 'list':
            return await cli.cmd_list(args)
        elif args.command == 'metrics':
            return await cli.cmd_metrics(args)
        elif args.command == 'config':
            return await cli.cmd_config(args)
        else:
            print(f"❌ Commande inconnue: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Opération annulée")
        return 130
    except Exception as e:
        print(f"❌ Erreur CLI: {e}")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)