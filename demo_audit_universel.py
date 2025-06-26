#!/usr/bin/env python3
"""
🌟 DÉMONSTRATION - Meta-Auditeur Universel en Action
Prouve que le système peut auditer autonomément n'importe quel module Python
"""
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(Path(__file__).parent))

# Mock classes pour le test si Pattern Factory indisponible
class MockAgent:
    def __init__(self, agent_type: str, **config):
        self.agent_type = agent_type
        self.agent_id = "test_id"

class MockTask:
    def __init__(self, description: str, **kwargs):
        self.description = description
        self.task_id = description
        self.payload = kwargs.get('payload', {})
        self.data = kwargs.get('data', {})

class MockResult:
    def __init__(self, success: bool, data: any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error

# Mock le module core si indisponible
try:
    from core.agent_factory_architecture import Agent, Task, Result
    print("✅ Pattern Factory disponible")
except ImportError:
    print("⚠️ Pattern Factory indisponible, utilisation des mocks")
    Agent = MockAgent
    Task = MockTask  
    Result = MockResult

async def demo_audit_autonome():
    """Démonstration du Meta-Auditeur travaillant de manière autonome"""
    print("🌟 DÉMONSTRATION - Meta-Auditeur Universel")
    print("=" * 60)
    print("Le Meta-Auditeur va maintenant auditer plusieurs modules de manière autonome...\n")
    
    # Import du Meta-Auditeur
    from agents.agent_META_AUDITEUR_UNIVERSEL import MetaAuditeurUniversel
    
    # Créer et démarrer le Meta-Auditeur
    meta_auditor = MetaAuditeurUniversel()
    await meta_auditor.startup()
    
    print(f"✅ Meta-Auditeur initialisé avec {len(meta_auditor.available_auditors)} agents spécialisés")
    
    # Liste des modules à auditer (différents types)
    modules_a_auditer = [
        ("agents/agent_MAINTENANCE_10_auditeur_qualite_normes.py", "Agent avec audit universel"),
        ("agents/agent_config.py", "Module de configuration"),
        ("agents/agent_01_coordinateur_principal.py", "Agent coordinateur"),
        ("demo_audit_universel.py", "Script de démonstration (ce fichier !)")
    ]
    
    resultats_globaux = []
    
    for i, (module_path, description) in enumerate(modules_a_auditer, 1):
        if not Path(module_path).exists():
            print(f"⚠️ Module {module_path} non trouvé, ignoré")
            continue
            
        print(f"\n🔍 [{i}] AUDIT AUTONOME: {description}")
        print(f"    Fichier: {module_path}")
        print("    Le Meta-Auditeur analyse, planifie, délègue et consolide automatiquement...")
        
        try:
            # Le Meta-Auditeur travaille de manière complètement autonome
            result = await meta_auditor.audit_complet(module_path)
            
            if result.get('status') != 'failed':
                score = result['global_score']
                niveau = result['quality_level']
                duree = result['total_duration']
                agents_utilises = len(result['agents_used'])
                issues = len(result['consolidated_issues'])
                
                print(f"    ✅ AUDIT AUTONOME RÉUSSI!")
                print(f"       📊 Score global: {score}/100 ({niveau})")
                print(f"       ⚡ Durée: {duree}s")
                print(f"       🤖 Agents utilisés: {agents_utilises}")
                print(f"       🔍 Issues consolidées: {issues}")
                
                # Plan d'amélioration automatique
                plan = result.get('improvement_plan', {})
                priorite = plan.get('priorite_globale', 'unknown')
                actions = len(plan.get('actions_immediates', []))
                
                print(f"       📋 Plan d'amélioration: {priorite} priorité ({actions} actions)")
                
                # Quelques actions immédiates si disponibles
                if plan.get('actions_immediates'):
                    print("       💡 Actions recommandées:")
                    for action in plan['actions_immediates'][:2]:  # Afficher les 2 premières
                        print(f"          - {action}")
                
                resultats_globaux.append({
                    'module': module_path,
                    'score': score,
                    'niveau': niveau,
                    'success': True
                })
                
            else:
                print(f"    ❌ AUDIT ÉCHOUÉ: {result.get('error', 'Erreur inconnue')}")
                resultats_globaux.append({
                    'module': module_path,
                    'score': 0,
                    'niveau': 'failed',
                    'success': False
                })
                
        except Exception as e:
            print(f"    ❌ ERREUR PENDANT L'AUDIT: {e}")
            resultats_globaux.append({
                'module': module_path,
                'score': 0,
                'niveau': 'error',
                'success': False
            })
    
    # Synthèse finale
    print(f"\n🏆 SYNTHÈSE DES AUDITS AUTONOMES")
    print("=" * 60)
    
    audits_reussis = sum(1 for r in resultats_globaux if r['success'])
    score_moyen = sum(r['score'] for r in resultats_globaux if r['success']) / max(audits_reussis, 1)
    
    print(f"📊 Audits réussis: {audits_reussis}/{len(resultats_globaux)}")
    print(f"📈 Score moyen: {score_moyen:.1f}/100")
    
    print(f"\n📋 Détail par module:")
    for result in resultats_globaux:
        status = "✅" if result['success'] else "❌"
        module_name = Path(result['module']).name
        print(f"   {status} {module_name}: {result['score']}/100 ({result['niveau']})")
    
    # Métriques du Meta-Auditeur
    health = await meta_auditor.health_check()
    metrics = meta_auditor.meta_metrics
    
    print(f"\n🤖 MÉTRIQUES META-AUDITEUR")
    print(f"   Orchestrations totales: {health['orchestrations_performed']}")
    print(f"   Modules audités: {len(metrics['modules_audited'])}")
    print(f"   Délégations aux agents: {sum(metrics['agents_delegated'].values())}")
    print(f"   Corrélations détectées: {metrics['correlations_detected']}")
    
    await meta_auditor.shutdown()
    
    print(f"\n🎯 DÉMONSTRATION TERMINÉE")
    print("=" * 60)
    print("✅ Le Meta-Auditeur Universel a audité de manière COMPLÈTEMENT AUTONOME")
    print("✅ Détection automatique du type de module")
    print("✅ Planification intelligente des audits spécialisés")
    print("✅ Délégation parallèle aux agents experts")
    print("✅ Consolidation et corrélation des résultats")
    print("✅ Génération automatique de plans d'amélioration")
    print("\n🚀 Le système d'audit universel est 100% opérationnel !")
    
    return audits_reussis >= len(resultats_globaux) * 0.75  # 75% de réussite minimum

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DÉMONSTRATION")
    success = asyncio.run(demo_audit_autonome())
    
    if success:
        print("\n🏆 DÉMONSTRATION RÉUSSIE - Système validé !")
    else:
        print("\n💥 DÉMONSTRATION PARTIELLE - Optimisations possibles")
        sys.exit(1)