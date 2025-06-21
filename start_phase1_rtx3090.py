#!/usr/bin/env python3
"""
[ROCKET] SCRIPT LANCEMENT PHASE 1 - ANALYSE PARALLLE RTX3090
Usage: python start_phase1_rtx3090.py
Configuration: RTX 3090 + Modles Ollama locaux
"""

import os
import sys
import asyncio
from pathlib import Path

# Configuration RTX3090 OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # RTX 3090 uniquement
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

def print_banner():
    """Affiche bannire dmarrage"""
    print("" + "=" * 68 + "")
    print("[ROCKET]           PHASE 1 - ANALYSE PARALLLE RTX3090")
    print("[TARGET]           Configuration: Modles Ollama Locaux")
    print("[LIGHTNING]           Agents: Mixtral + Qwen-Coder simultans")
    print("" + "=" * 68 + "")
    print()

def validate_environment():
    """Valide environnement RTX3090"""
    print("[SEARCH] Validation environnement RTX3090...")
    
    # Variables CUDA
    cuda_device = os.environ.get('CUDA_VISIBLE_DEVICES')
    if cuda_device != '1':
        print(f"[CROSS] CUDA_VISIBLE_DEVICES incorrect: {cuda_device}")
        print("[BULB] Excutez config_env_rtx3090.bat avant ce script")
        return False
    
    # Vrification workspace
    workspace = Path("refactoring_workspace")
    if not workspace.exists():
        print(" Workspace refactoring non trouv, cration...")
        workspace.mkdir(parents=True, exist_ok=True)
    
    # Vrification agents
    agents_dir = Path("agents_refactoring") 
    if not agents_dir.exists():
        print("[CROSS] Rpertoire agents_refactoring non trouv")
        return False
    
    alpha_agent = agents_dir / "agent_analyzer_alpha_mixtral_rtx3090.py"
    beta_agent = agents_dir / "agent_analyzer_beta_qwen_rtx3090.py"
    orchestrator = agents_dir / "orchestrator_phase1_analysis_rtx3090.py"
    
    if not alpha_agent.exists():
        print(f"[CROSS] Agent Alpha non trouv: {alpha_agent}")
        return False
    
    if not beta_agent.exists():
        print(f"[CROSS] Agent Beta non trouv: {beta_agent}")
        return False
    
    if not orchestrator.exists():
        print(f"[CROSS] Orchestrateur non trouv: {orchestrator}")
        return False
    
    print("[CHECK] Environnement RTX3090 valid")
    print("[CHECK] Agents Phase 1 disponibles")
    print("[CHECK] Workspace prt")
    return True

async def launch_phase1():
    """Lance Phase 1 avec orchestrateur RTX3090"""
    print("[ROCKET] Lancement Phase 1 - Analyse Parallle RTX3090")
    print()
    
    try:
        # Import dynamique de l'orchestrateur
        sys.path.append(str(Path("agents_refactoring")))
        
        from orchestrator_phase1_analysis_rtx3090 import OrchestratorPhase1RTX3090
        
        # Cration et excution orchestrateur
        orchestrator = OrchestratorPhase1RTX3090()
        
        print(" Configuration RTX3090:")
        print(f"    GPU: {orchestrator.gpu_device}")
        print(f"    Mixtral: {orchestrator.models_config['mixtral']['model']}")
        print(f"    Qwen: {orchestrator.models_config['qwen']['model']}")
        print()
        
        # Excution Phase 1 complte
        result = await orchestrator.execute_phase_1()
        
        # Affichage rsultats
        print()
        print(" PHASE 1 TERMINE !")
        print("" * 50)
        print(f"[CHART] Status: {result.status}")
        print(f" Dure: {result.duration:.2f}s")
        print(f"[ROBOT] Agents: {len(result.agents_executed)}")
        print(f"[TARGET] Recommandations Phase 2: {len(result.next_phase_recommendations)}")
        print()
        
        if result.status == "SUCCESS":
            print("[CHECK] SUCCS - Phase 1 termine avec succs !")
            print("[DOCUMENT] Rapports disponibles dans refactoring_workspace/")
            print()
            print("[TARGET] PROCHAINES TAPES:")
            for i, rec in enumerate(result.next_phase_recommendations[:3], 1):
                print(f"   {i}. {rec}")
            print()
            print(" VALIDATION HUMAINE REQUISE POUR PHASE 2")
        else:
            print("[CROSS] CHEC - Erreurs dtectes")
            print("[SEARCH] Consultez les logs pour plus d'informations")
        
        return result.status == "SUCCESS"
        
    except ImportError as e:
        print(f"[CROSS] Erreur import orchestrateur: {e}")
        print("[BULB] Vrifiez que les agents Phase 1 sont crs")
        return False
    
    except Exception as e:
        print(f"[CROSS] Erreur excution Phase 1: {e}")
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    # Validation environnement
    if not validate_environment():
        print("[CROSS] Environnement invalide - Arrt")
        sys.exit(1)
    
    print("[LIGHTNING] Environnement valid - Dmarrage Phase 1...")
    print()
    
    # Confirmation utilisateur
    response = input("[TARGET] Confirmer dmarrage Phase 1 RTX3090 ? (o/N): ").strip().lower()
    if response not in ['o', 'oui', 'y', 'yes']:
        print(" Dmarrage annul par utilisateur")
        sys.exit(0)
    
    print()
    print("[ROCKET] DMARRAGE PHASE 1 CONFIRM !")
    print()
    
    # Lancement asynchrone
    try:
        success = asyncio.run(launch_phase1())
        
        if success:
            print(" Phase 1 russie - Prt pour Phase 2 !")
            sys.exit(0)
        else:
            print("[CROSS] Phase 1 choue")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n Interruption utilisateur")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n[CROSS] Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 



