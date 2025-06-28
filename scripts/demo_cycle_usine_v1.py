#!/usr/bin/env python3
"""
🎯 Démonstration Cycle-Usine v1 - NextGeneration
===============================================

Script de démonstration complète du système Cycle-Usine v1
avec création d'un agent réel de bout en bout.

Auteur: Claude Code  
Date: 2025-06-28
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le chemin des systèmes
sys.path.append(str(Path(__file__).parent.parent / 'systems'))

from cycle_usine_v1 import CycleUsineV1, CycleStage

async def demo_cycle_usine_complet():
    """
    Démonstration complète du Cycle-Usine v1
    Crée un agent NextGeneration de A à Z
    """
    print("🏭 === DÉMONSTRATION CYCLE-USINE V1 ===")
    print()
    
    # Initialiser le système
    usine = CycleUsineV1()
    
    # Définir les requirements d'un agent moderne
    requirements_agent_moderne = {
        'name': 'Agent Moderne Démo',
        'description': 'Agent d\'exemple généré automatiquement par Cycle-Usine v1',
        'type': 'maintenance_agent',
        'architecture': 'nextgeneration',
        'features': [
            'llm_integration',
            'async_processing', 
            'monitoring_integration',
            'auto_healing',
            'performance_optimization',
            'security_validation'
        ],
        'capabilities': {
            'input_formats': ['json', 'yaml', 'plain_text'],
            'output_formats': ['json', 'markdown', 'structured_report'],
            'processing_modes': ['batch', 'stream', 'realtime'],
            'integration_points': ['messagebus', 'context_store', 'llm_gateway']
        },
        'quality_requirements': {
            'performance': {
                'response_time_ms': 500,
                'throughput_rps': 100,
                'memory_limit_mb': 256
            },
            'reliability': {
                'uptime_percentage': 99.9,
                'error_rate_max': 0.001,
                'recovery_time_s': 10
            },
            'security': {
                'input_validation': True,
                'output_sanitization': True,
                'audit_logging': True,
                'encryption_at_rest': True
            }
        },
        'deployment': {
            'container_ready': True,
            'health_checks': True,
            'metrics_export': True,
            'log_structured': True
        }
    }
    
    print("📋 Requirements définis:")
    print(f"   - Nom: {requirements_agent_moderne['name']}")
    print(f"   - Features: {len(requirements_agent_moderne['features'])}")
    print(f"   - Capabilities: {len(requirements_agent_moderne['capabilities'])}")
    print()
    
    # Démarrer le cycle
    print("🚀 Démarrage du cycle de développement...")
    cycle_id = await usine.start_cycle('agent_moderne_demo', requirements_agent_moderne)
    print(f"   ✅ Cycle créé: {cycle_id}")
    print()
    
    # Exécuter le cycle complet
    print("▶️ Exécution du cycle complet (Spec → Code → Test → Doc → Deploy)...")
    print()
    
    results = await usine.execute_cycle()
    
    # Afficher les résultats détaillés
    print("📊 === RÉSULTATS DU CYCLE ===")
    print(f"🎯 Succès global: {results['overall_success_rate']:.1%}")
    print(f"⏱️ Durée totale: {results['total_duration']:.2f}s")
    print()
    
    # Détail par étape
    for stage_name, stage_data in results['stages'].items():
        success_icon = "✅" if stage_data['success_rate'] > 0.8 else "⚠️" if stage_data['success_rate'] > 0.5 else "❌"
        print(f"{success_icon} {stage_name.upper()}")
        print(f"   Tâches: {stage_data['tasks']}")
        print(f"   Succès: {stage_data['success_rate']:.1%}")
        print(f"   Durée: {stage_data['duration']:.2f}s")
        
        # Afficher quelques outputs clés
        if 'outputs' in stage_data and stage_data['outputs']:
            outputs = stage_data['outputs']
            if stage_name == 'specification':
                if 'specifications' in outputs:
                    specs = outputs['specifications']
                    if 'deliverables' in specs:
                        print(f"   📦 Livrables: {len(specs['deliverables'])}")
            elif stage_name == 'code_generation':
                if 'generated_code' in outputs:
                    code_files = outputs['generated_code']
                    print(f"   📄 Fichiers générés: {len(code_files)}")
                if 'syntax_validation' in outputs:
                    validation = outputs['syntax_validation']
                    print(f"   ✓ Validation syntaxe: {validation['score']:.1%}")
            elif stage_name == 'testing':
                if 'test_results' in outputs:
                    tests = outputs['test_results']
                    print(f"   🧪 Tests: {tests['passed']}/{tests['total']} réussis")
                    print(f"   📈 Durée tests: {tests['duration']:.1f}s")
            elif stage_name == 'documentation':
                if 'documentation' in outputs:
                    print(f"   📚 Documentation générée")
                if 'api_docs' in outputs:
                    print(f"   🔌 API docs générées")
            elif stage_name == 'deployment':
                if 'deployment_url' in outputs:
                    print(f"   🌐 URL: {outputs['deployment_url']}")
        print()
    
    # Informations sur les artefacts créés
    print("📁 === ARTEFACTS CRÉÉS ===")
    cycle_path = usine.cycle_dir / cycle_id
    if cycle_path.exists():
        print(f"📂 Répertoire cycle: {cycle_path}")
        
        # Lister les fichiers créés
        for item in cycle_path.rglob('*'):
            if item.is_file():
                relative_path = item.relative_to(cycle_path)
                size_kb = item.stat().st_size / 1024
                print(f"   📄 {relative_path} ({size_kb:.1f}KB)")
    print()
    
    # Statut final
    if results.get('failed_at'):
        print(f"⚠️ Cycle interrompu à l'étape: {results['failed_at']}")
    else:
        print("🎉 Cycle terminé avec succès!")
    
    print(f"🔍 Pour plus de détails: {usine.cycle_dir / cycle_id / 'cycle_results.json'}")
    
    return results

async def demo_gestion_cycles():
    """Démonstration de la gestion des cycles"""
    print("\n🔄 === GESTION DES CYCLES ===")
    
    usine = CycleUsineV1()
    
    # Lister les cycles existants
    cycles = usine.list_cycles()
    print(f"📋 Cycles existants: {len(cycles)}")
    
    for cycle in cycles[:3]:  # Afficher les 3 plus récents
        print(f"   📊 {cycle['cycle_id']}")
        print(f"      Complété: {'✅' if cycle['completed'] else '⏳'}")
        if cycle['completed']:
            print(f"      Succès: {cycle.get('success_rate', 0):.1%}")
        print()

async def demo_quality_gates():
    """Démonstration des quality gates"""
    print("🛡️ === QUALITY GATES ===")
    
    usine = CycleUsineV1()
    
    print("🎯 Seuils de qualité configurés:")
    gates = usine.config['quality_gates']
    print(f"   📋 Spec completeness: {gates['spec_completeness']:.1%}")
    print(f"   💾 Code coverage: {gates['code_coverage']:.1%}")
    print(f"   🧪 Test success rate: {gates['test_success_rate']:.1%}")
    print(f"   📚 Doc coverage: {gates['doc_coverage']:.1%}")
    print(f"   🚀 Deploy success rate: {gates['deploy_success_rate']:.1%}")
    print()

async def main():
    """Point d'entrée principal"""
    print("🌟 CYCLE-USINE V1 - SYSTÈME DE DÉVELOPPEMENT AUTOMATISÉ")
    print("=" * 60)
    print()
    
    try:
        # Démonstration des quality gates
        await demo_quality_gates()
        
        # Démonstration complète
        results = await demo_cycle_usine_complet()
        
        # Gestion des cycles
        await demo_gestion_cycles()
        
        print("\n✨ Démonstration terminée avec succès!")
        print(f"🎯 Taux de succès final: {results['overall_success_rate']:.1%}")
        
    except Exception as e:
        print(f"\n💥 Erreur durant la démonstration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)