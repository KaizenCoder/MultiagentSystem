#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[ROCKET] START PHASE 2 - ARCHITECTURE NEXTGENERATION
Script de dmarrage pour la Phase 2 du refactoring

Mission: Lancer l'orchestrateur Phase 2 pour crer l'architecture modulaire
- Vrifications environnement
- Validation prrequis Phase 1
- Dmarrage agents Alpha & Beta
- Coordination architecture complte
- Gnration plan architectural final

Usage: python start_phase2_architecture.py
"""

import os
import sys
import asyncio
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Charger variables environnement
load_dotenv()

def print_banner():
    """
     Afficher bannire Phase 2
    """
    print("[ROCKET] " + "=" * 58 + " [ROCKET]")
    print("[CONSTRUCTION]  NEXTGENERATION - PHASE 2 ARCHITECTURE MODULAIRE  [CONSTRUCTION]")
    print("[ROCKET] " + "=" * 58 + " [ROCKET]")
    print()
    print(" Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("[TARGET] Objectif: Crer architecture modulaire SRP")
    print("[CHART] Cibles: 4 fichiers god mode  modules spcialiss")
    print("[LIGHTNING] Agents: Alpha (Claude) + Beta (GPT-4)")
    print()

def check_environment():
    """
    [SEARCH] Vrifier environnement et prrequis
    """
    print("[SEARCH] VRIFICATION ENVIRONNEMENT")
    print("-" * 40)
    
    # Vrifier cls API
    required_keys = {
        'ANTHROPIC_API_KEY': 'Claude Sonnet 4',
        'OPENAI_API_KEY': 'GPT-4 Turbo'
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value:
            print(f"[CHECK] {key}: ****{value[-4:]} ({description})")
        else:
            print(f"[CROSS] {key}: MANQUANTE ({description})")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"\n[CROSS] ERREUR: Cls API manquantes: {', '.join(missing_keys)}")
        print("[BULB] Ajoutez-les dans votre fichier .env")
        return False
    
    # Vrifier Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"[CROSS] Python version insuffisante: {python_version.major}.{python_version.minor}")
        print("[BULB] Requis: Python 3.8+")
        return False
    else:
        print(f"[CHECK] Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Vrifier modules requis
    required_modules = ['anthropic', 'openai', 'asyncio', 'pathlib', 'dataclasses']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"[CHECK] Module: {module}")
        except ImportError:
            print(f"[CROSS] Module: {module} (manquant)")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n[CROSS] ERREUR: Modules manquants: {', '.join(missing_modules)}")
        print("[BULB] Installez avec: pip install anthropic openai")
        return False
    
    print("[CHECK] Environnement valid!")
    return True

def check_phase1_results():
    """
    [CHART] Vrifier rsultats Phase 1
    """
    print("\n[CHART] VRIFICATION PHASE 1")
    print("-" * 40)
    
    workspace = Path(__file__).parent
    phase1_results_path = workspace / "refactoring_workspace" / "results" / "phase1_cloud"
    
    if not phase1_results_path.exists():
        print("[CROSS] Rpertoire rsultats Phase 1 manquant")
        return False
    
    # Chercher rapport Phase 1
    rapport_files = list(phase1_results_path.glob("phase1_cloud_rapport_*.md"))
    if not rapport_files:
        print("[CROSS] Rapport Phase 1 manquant")
        return False
    
    latest_rapport = max(rapport_files, key=lambda f: f.stat().st_mtime)
    print(f"[CHECK] Rapport Phase 1 trouv: {latest_rapport.name}")
    
    # Chercher rsultats JSON
    json_files = list(phase1_results_path.glob("phase1_cloud_results_*.json"))
    if not json_files:
        print("[CROSS] Rsultats JSON Phase 1 manquants")
        return False
    
    latest_json = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"[CHECK] Rsultats JSON trouvs: {latest_json.name}")
    
    # Vrifier analyses Alpha et Beta (dans rpertoires parents)
    results_parent = phase1_results_path.parent
    alpha_path = results_parent / "alpha_claude"
    beta_path = results_parent / "beta_gemini"
    
    if alpha_path.exists():
        alpha_files = list(alpha_path.glob("*.json"))
        print(f"[CHECK] Analyses Alpha: {len(alpha_files)} fichiers")
    else:
        print("[CROSS] Analyses Alpha manquantes")
        return False
    
    if beta_path.exists():
        beta_files = list(beta_path.glob("*.json"))
        print(f"[CHECK] Analyses Beta: {len(beta_files)} fichiers")
    else:
        print("[CROSS] Analyses Beta manquantes")
        return False
    
    print("[CHECK] Phase 1 valide!")
    return True

def check_workspace_structure():
    """
    [FOLDER] Vrifier structure workspace
    """
    print("\n[FOLDER] VRIFICATION WORKSPACE")
    print("-" * 40)
    
    workspace = Path(__file__).parent
    
    # Vrifier rpertoires requis
    required_dirs = [
        "agents_refactoring",
        "refactoring_workspace",
        "orchestrator",
        "orchestrator_green"
    ]
    
    for dir_name in required_dirs:
        dir_path = workspace / dir_name
        if dir_path.exists():
            print(f"[CHECK] Rpertoire: {dir_name}")
        else:
            print(f"[CROSS] Rpertoire manquant: {dir_name}")
            return False
    
    # Vrifier agents Phase 2
    agents_path = workspace / "agents_refactoring"
    required_agents = [
        "agent_architect_alpha_claude_sonnet4.py",
        "agent_architect_beta_gpt4.py", 
        "orchestrator_phase2_architecture.py"
    ]
    
    for agent_file in required_agents:
        agent_path = agents_path / agent_file
        if agent_path.exists():
            print(f"[CHECK] Agent: {agent_file}")
        else:
            print(f"[CROSS] Agent manquant: {agent_file}")
            return False
    
    # Vrifier backup baseline
    backup_path = workspace / "refactoring_backups"
    if backup_path.exists():
        baseline_dirs = list(backup_path.glob("snapshots/baseline_*"))
        if baseline_dirs:
            latest_baseline = max(baseline_dirs, key=lambda d: d.stat().st_mtime)
            print(f"[CHECK] Backup baseline: {latest_baseline.name}")
        else:
            print("[CROSS] Backup baseline manquant")
            return False
    else:
        print("[CROSS] Rpertoire backup manquant")
        return False
    
    print("[CHECK] Workspace structure valide!")
    return True

def show_phase2_objectives():
    """
    [TARGET] Afficher objectifs Phase 2
    """
    print("\n[TARGET] OBJECTIFS PHASE 2")
    print("-" * 40)
    
    objectives = [
        ("main.py", "1,990 lignes", "~100 lignes", "~95% rduction"),
        ("advanced_coordination.py", "779 lignes", "~150 lignes", "~81% rduction"), 
        ("redis_cluster_manager.py", "738 lignes", "~150 lignes", "~80% rduction"),
        ("monitoring.py", "709 lignes", "~150 lignes", "~79% rduction")
    ]
    
    print("[CHART] Fichiers God Mode  Modules SRP:")
    for file, current, target, reduction in objectives:
        print(f"   {file:<25} {current:>12}  {target:>10} ({reduction})")
    
    print("\n Patterns Architecturaux:")
    patterns = [
        "Single Responsibility Principle (SRP)",
        "Dependency Injection Pattern",
        "Repository Pattern", 
        "Service Layer Pattern",
        "Factory Pattern",
        "Clean Architecture Layers"
    ]
    
    for pattern in patterns:
        print(f"   {pattern}")
    
    print("\n[LIGHTNING] Agents Phase 2:")
    agents = [
        ("Alpha", "Claude Sonnet 4", "Plans architecturaux SRP"),
        ("Beta", "GPT-4 Turbo", "Architectures alternatives"),
        ("Orchestrateur", "Coordination", "Consensus & validation croise")
    ]
    
    for name, model, role in agents:
        print(f"  [ROBOT] {name:<12} ({model:<15})  {role}")

async def execute_phase2():
    """
    [ROCKET] Excuter Phase 2 Architecture
    """
    print("\n[ROCKET] DMARRAGE PHASE 2")
    print("-" * 40)
    
    try:
        # Import orchestrateur
        sys.path.append(str(Path(__file__).parent / "agents_refactoring"))
        from orchestrator_phase2_architecture import OrchestratorPhase2Architecture
        
        # Crer orchestrateur
        orchestrator = OrchestratorPhase2Architecture()
        
        # Excuter Phase 2 complte
        print("[CONSTRUCTION] Lancement orchestrateur Phase 2...")
        results = await orchestrator.execute_phase2_complete()
        
        if results and results.success:
            print("\n PHASE 2 TERMINE AVEC SUCCS!")
            print(f"  Dure: {results.duration_seconds:.2f} secondes")
            print(f"[CHART] Plans Alpha: {len(results.alpha_plans)}")
            print(f" Alternatives Beta: {len(results.beta_alternatives)}")
            print(f"[TARGET] Plan final gnr: {'[CHECK]' if results.final_architecture_plan else '[CROSS]'}")
            print(f"[ROCKET] Prt Phase 3: {'[CHECK]' if results.next_phase_ready else '[CROSS]'}")
            
            return True
        else:
            print("\n[CROSS] CHEC PHASE 2")
            return False
            
    except Exception as e:
        print(f"\n ERREUR Phase 2: {e}")
        return False

async def main():
    """
    [TARGET] Point d'entre principal
    """
    # Bannire
    print_banner()
    
    # Vrifications prrequis
    if not check_environment():
        sys.exit(1)
    
    if not check_phase1_results():
        print("\n[BULB] Excutez d'abord: python start_phase1_cloud.py")
        sys.exit(1)
    
    if not check_workspace_structure():
        sys.exit(1)
    
    # Afficher objectifs
    show_phase2_objectives()
    
    # Confirmation utilisateur
    print("\n CONFIRMATION")
    print("-" * 40)
    print("[TARGET] Dmarrer Phase 2 Architecture Modulaire ?")
    print("[LIGHTNING] Agents Alpha (Claude) + Beta (GPT-4) vont analyser 4 fichiers")
    print(" Gnration plans architecturaux avec validation croise")
    
    # Auto-confirmation en mode script
    response = input("\n Continuer ? (O/n): ").strip().lower()
    if response in ['n', 'non', 'no']:
        print("[CROSS] Phase 2 annule par l'utilisateur")
        sys.exit(0)
    
    # Excution Phase 2
    success = await execute_phase2()
    
    if success:
        print("\n FLICITATIONS!")
        print("[CHECK] Phase 2 Architecture termine avec succs")
        print("[TARGET] Prochaine tape: Phase 3 Implmentation")
        print("[CLIPBOARD] Consultez les rapports dans refactoring_workspace/results/phase2_architecture/")
        sys.exit(0)
    else:
        print("\n CHEC Phase 2")
        print("[CLIPBOARD] Consultez les logs pour diagnostiquer le problme")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  Phase 2 interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n ERREUR CRITIQUE: {e}")
        sys.exit(1) 