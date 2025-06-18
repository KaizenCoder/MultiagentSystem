#!/usr/bin/env python3
"""
🚀 SCRIPT LANCEMENT PHASE 1 - ANALYSE PARALLÈLE RTX3090
Usage: python start_phase1_rtx3090.py
Configuration: RTX 3090 + Modèles Ollama locaux
"""

import os
import sys
import asyncio
from pathlib import Path

# Configuration RTX3090 OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

def print_banner():
    """Affiche bannière démarrage"""
    print("🎮" + "=" * 68 + "🎮")
    print("🚀           PHASE 1 - ANALYSE PARALLÈLE RTX3090")
    print("🎯           Configuration: Modèles Ollama Locaux")
    print("⚡           Agents: Mixtral + Qwen-Coder simultanés")
    print("🎮" + "=" * 68 + "🎮")
    print()

def validate_environment():
    """Valide environnement RTX3090"""
    print("🔍 Validation environnement RTX3090...")
    
    # Variables CUDA
    cuda_device = os.environ.get('CUDA_VISIBLE_DEVICES')
    if cuda_device != '1':
        print(f"❌ CUDA_VISIBLE_DEVICES incorrect: {cuda_device}")
        print("💡 Exécutez config_env_rtx3090.bat avant ce script")
        return False
    
    # Vérification workspace
    workspace = Path("refactoring_workspace")
    if not workspace.exists():
        print("⚠️ Workspace refactoring non trouvé, création...")
        workspace.mkdir(parents=True, exist_ok=True)
    
    # Vérification agents
    agents_dir = Path("agents_refactoring") 
    if not agents_dir.exists():
        print("❌ Répertoire agents_refactoring non trouvé")
        return False
    
    alpha_agent = agents_dir / "agent_analyzer_alpha_mixtral_rtx3090.py"
    beta_agent = agents_dir / "agent_analyzer_beta_qwen_rtx3090.py"
    orchestrator = agents_dir / "orchestrator_phase1_analysis_rtx3090.py"
    
    if not alpha_agent.exists():
        print(f"❌ Agent Alpha non trouvé: {alpha_agent}")
        return False
    
    if not beta_agent.exists():
        print(f"❌ Agent Beta non trouvé: {beta_agent}")
        return False
    
    if not orchestrator.exists():
        print(f"❌ Orchestrateur non trouvé: {orchestrator}")
        return False
    
    print("✅ Environnement RTX3090 validé")
    print("✅ Agents Phase 1 disponibles")
    print("✅ Workspace prêt")
    return True

async def launch_phase1():
    """Lance Phase 1 avec orchestrateur RTX3090"""
    print("🚀 Lancement Phase 1 - Analyse Parallèle RTX3090")
    print()
    
    try:
        # Import dynamique de l'orchestrateur
        sys.path.append(str(Path("agents_refactoring")))
        
        from orchestrator_phase1_analysis_rtx3090 import OrchestratorPhase1RTX3090
        
        # Création et exécution orchestrateur
        orchestrator = OrchestratorPhase1RTX3090()
        
        print("🎮 Configuration RTX3090:")
        print(f"   • GPU: {orchestrator.gpu_device}")
        print(f"   • Mixtral: {orchestrator.models_config['mixtral']['model']}")
        print(f"   • Qwen: {orchestrator.models_config['qwen']['model']}")
        print()
        
        # Exécution Phase 1 complète
        result = await orchestrator.execute_phase_1()
        
        # Affichage résultats
        print()
        print("🎉 PHASE 1 TERMINÉE !")
        print("═" * 50)
        print(f"📊 Status: {result.status}")
        print(f"⏱️ Durée: {result.duration:.2f}s")
        print(f"🤖 Agents: {len(result.agents_executed)}")
        print(f"🎯 Recommandations Phase 2: {len(result.next_phase_recommendations)}")
        print()
        
        if result.status == "SUCCESS":
            print("✅ SUCCÈS - Phase 1 terminée avec succès !")
            print("📄 Rapports disponibles dans refactoring_workspace/")
            print()
            print("🎯 PROCHAINES ÉTAPES:")
            for i, rec in enumerate(result.next_phase_recommendations[:3], 1):
                print(f"   {i}. {rec}")
            print()
            print("👤 VALIDATION HUMAINE REQUISE POUR PHASE 2")
        else:
            print("❌ ÉCHEC - Erreurs détectées")
            print("🔍 Consultez les logs pour plus d'informations")
        
        return result.status == "SUCCESS"
        
    except ImportError as e:
        print(f"❌ Erreur import orchestrateur: {e}")
        print("💡 Vérifiez que les agents Phase 1 sont créés")
        return False
    
    except Exception as e:
        print(f"❌ Erreur exécution Phase 1: {e}")
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    # Validation environnement
    if not validate_environment():
        print("❌ Environnement invalide - Arrêt")
        sys.exit(1)
    
    print("⚡ Environnement validé - Démarrage Phase 1...")
    print()
    
    # Confirmation utilisateur
    response = input("🎯 Confirmer démarrage Phase 1 RTX3090 ? (o/N): ").strip().lower()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("⏹️ Démarrage annulé par utilisateur")
        sys.exit(0)
    
    print()
    print("🚀 DÉMARRAGE PHASE 1 CONFIRMÉ !")
    print()
    
    # Lancement asynchrone
    try:
        success = asyncio.run(launch_phase1())
        
        if success:
            print("🎉 Phase 1 réussie - Prêt pour Phase 2 !")
            sys.exit(0)
        else:
            print("❌ Phase 1 échouée")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Interruption utilisateur")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 