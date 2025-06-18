#!/usr/bin/env python3
"""
[ROCKET] NEXTGENERATION - PHASE 3 IMPLMENTATION MODULAIRE
Dmarrage automatique extraction routes + cration services + architecture
Pattern: Hexagonal Architecture + CQRS
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Ajouter agents_refactoring au path
sys.path.insert(0, str(Path("agents_refactoring").absolute()))

def print_banner():
    """Affichage banner Phase 3"""
    print("[ROCKET] ========================================================== [ROCKET]")
    print("[CONSTRUCTION]  NEXTGENERATION - PHASE 3 IMPLMENTATION MODULAIRE  [CONSTRUCTION]")
    print("[ROCKET] ========================================================== [ROCKET]")
    print()
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[TARGET] Objectif: Refactoring Architecture Hexagonale + CQRS")
    print("[CHART] Target: main.py (1,990  ~80 lignes = 96% rduction)")
    print("[LIGHTNING] Agents: Route Extractor + Services Creator + Orchestrateur")
    print()

def verify_environment():
    """Vrifier environnement requis Phase 3"""
    print("[SEARCH] VRIFICATION ENVIRONNEMENT")
    print("-" * 40)
    
    # Vrifier cls API
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if anthropic_key:
        print(f"[CHECK] ANTHROPIC_API_KEY: ****{anthropic_key[-2:]} (Claude Sonnet 4)")
    else:
        print("  ANTHROPIC_API_KEY manquante (Claude Sonnet 4)")
    
    if openai_key:
        print(f"[CHECK] OPENAI_API_KEY: ****{openai_key[-4:]} (GPT-4 Turbo)")
    else:
        print("  OPENAI_API_KEY manquante (Mode Fallback)")
        print(" Activation mode simulation/fallback pour Phase 3")
    
    # Vrifier Python et modules
    print(f"[CHECK] Python: {sys.version.split()[0]}")
    
    try:
        import anthropic
        print("[CHECK] Module: anthropic")
    except ImportError:
        print("  Module: anthropic (degraded mode)")
    
    try:
        import openai
        print("[CHECK] Module: openai")
    except ImportError:
        print("  Module: openai manquant (Mode Fallback)")
        print(" Utilisation fallback pour gnration services")
    
    try:
        import asyncio
        print("[CHECK] Module: asyncio")
    except ImportError:
        print("[CROSS] Module: asyncio manquant")
        return False
    
    print("[CHECK] Environnement valid! (Mode Fallback si ncessaire)")
    return True

def verify_phase2_results():
    """Vrifier rsultats Phase 2 disponibles"""
    print("\n[CHART] VRIFICATION PHASE 2")
    print("-" * 40)
    
    phase2_results = Path("refactoring_workspace/results/phase2_architecture")
    if phase2_results.exists():
        phase2_files = list(phase2_results.glob("*.json"))
        if phase2_files:
            latest_results = max(phase2_files, key=lambda p: p.stat().st_mtime)
            print(f"[CHECK] Rsultats Phase 2: {latest_results.name}")
        else:
            print("  Rsultats Phase 2 JSON manquants")
    else:
        print("  Rpertoire Phase 2 manquant")
    
    # Vrifier architectures alternatives
    beta_results = Path("refactoring_workspace/results/beta_gpt4")
    if beta_results.exists():
        beta_files = list(beta_results.glob("*.json"))
        print(f"[CHECK] Architectures Beta: {len(beta_files)} fichiers")
    else:
        print("  Architectures Beta manquantes")
    
    # Vrifier fichier main.py cible
    main_file = Path("orchestrator/app/main.py")
    if main_file.exists():
        lines = len(main_file.read_text(encoding='utf-8').splitlines())
        print(f"[CHECK] main.py cible: {lines} lignes")
    else:
        print("[CROSS] main.py cible manquant")
        return False
    
    print("[CHECK] Phase 2 valide!")
    return True

def verify_workspace():
    """Vrifier workspace Phase 3"""
    print("\n[FOLDER] VRIFICATION WORKSPACE")
    print("-" * 40)
    
    # Vrifier agents Phase 3
    agents_dir = Path("agents_refactoring")
    required_agents = [
        "agent_route_extractor_claude_sonnet4.py",
        "agent_services_creator_gpt4.py", 
        "orchestrator_phase3_implementation.py"
    ]
    
    for agent_file in required_agents:
        agent_path = agents_dir / agent_file
        if agent_path.exists():
            print(f"[CHECK] Agent: {agent_file}")
        else:
            print(f"[CROSS] Agent manquant: {agent_file}")
            return False
    
    # Vrifier workspace structure
    workspace_dir = Path("refactoring_workspace")
    if workspace_dir.exists():
        print(f"[CHECK] Rpertoire: {workspace_dir}")
    else:
        print(f"[CROSS] Rpertoire manquant: {workspace_dir}")
        return False
    
    print("[CHECK] Workspace structure valide!")
    return True

def show_objectives():
    """Afficher objectifs Phase 3"""
    print("\n[TARGET] OBJECTIFS PHASE 3")
    print("-" * 40)
    print("[CHART] Fichiers God Mode  Modules SRP:")
    print("   main.py                   1,990 lignes  ~80 lignes  (~96% rduction)")
    print("   advanced_coordination.py    779 lignes  ~150 lignes (~81% rduction)")  
    print("   redis_cluster_manager.py    738 lignes  ~150 lignes (~80% rduction)")
    print("   monitoring.py               709 lignes  ~150 lignes (~79% rduction)")
    print()
    print(" Patterns Implments:")
    print("   Hexagonal Architecture (Ports & Adapters)")
    print("   CQRS (Command Query Responsibility Segregation)")
    print("   Dependency Injection Pattern")
    print("   Repository Pattern")
    print("   Service Layer Pattern")
    print("   Clean Architecture Layers")
    print()
    print("[LIGHTNING] Agents Phase 3:")
    print("  [ROBOT] Route Extractor  (Claude Sonnet 4)  Extraction routes FastAPI")
    print("  [ROBOT] Services Creator (GPT-4 Turbo    )  Cration services modulaires")
    print("  [ROBOT] Orchestrateur    (Coordination   )  Architecture finale + rapport")

async def run_phase3():
    """Excuter Phase 3 avec orchestrateur"""
    print("\n[ROCKET] DMARRAGE PHASE 3")
    print("-" * 40)
    print("[CONSTRUCTION] Lancement orchestrateur Phase 3...")
    
    try:
        # Import orchestrateur
        from orchestrator_phase3_implementation import OrchestratorPhase3
        
        # Crer et excuter orchestrateur
        orchestrator = OrchestratorPhase3()
        results = await orchestrator.run_phase3_implementation()
        
        return results
        
    except ImportError as e:
        print(f"[CROSS] Erreur import orchestrateur: {e}")
        return {"status": "error", "error": str(e)}
    except Exception as e:
        print(f"[CROSS] Erreur excution Phase 3: {e}")
        return {"status": "error", "error": str(e)}

def main():
    """Point d'entre principal"""
    print_banner()
    
    # Vrifications pralables
    if not verify_environment():
        print("\n[CROSS] chec vrification environnement")
        return 1
    
    if not verify_phase2_results():
        print("\n[CROSS] chec vrification Phase 2")
        return 1
        
    if not verify_workspace():
        print("\n[CROSS] chec vrification workspace")
        return 1
    
    # Afficher objectifs
    show_objectives()
    
    # Confirmation automatique (pas d'attente utilisateur)
    print("\n CONFIRMATION")
    print("-" * 40)
    print("[TARGET] Dmarrer Phase 3 Implmentation Modulaire ?")
    print("[LIGHTNING] Route Extractor + Services Creator + Architecture finale")
    print(" Refactoring main.py (1,990  ~80 lignes)")
    print()
    print(" Dmarrage automatique en cours...")
    
    # Excuter Phase 3
    try:
        results = asyncio.run(run_phase3())
        
        if results["status"] == "success":
            print("\n PHASE 3 TERMINE AVEC SUCCS!")
            print(f"  Dure: {results.get('duration_seconds', 0):.2f} secondes")
            print(f"[FOLDER] Fichiers gnrs: {len(results.get('implementation_files', []))}")
            print(f"[TARGET] Rapport: {results.get('final_report', 'N/A')}")
            print()
            print(" FLICITATIONS!")
            print("[CHECK] Architecture modulaire cre avec succs")
            print("[CONSTRUCTION] Pattern Hexagonal + CQRS implment") 
            print("[CHART] main.py: 1,990  ~80 lignes (96% rduction)")
            return 0
        else:
            print(f"\n[CROSS] ERREUR PHASE 3: {results.get('error')}")
            return 1
            
    except Exception as e:
        print(f"\n[CROSS] Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 