#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 START PHASE 2 - ARCHITECTURE NEXTGENERATION
Script de démarrage pour la Phase 2 du refactoring

Mission: Lancer l'orchestrateur Phase 2 pour créer l'architecture modulaire
- Vérifications environnement
- Validation prérequis Phase 1
- Démarrage agents Alpha & Beta
- Coordination architecture complète
- Génération plan architectural final

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
    🎨 Afficher bannière Phase 2
    """
    print("🚀 " + "=" * 58 + " 🚀")
    print("🏗️  NEXTGENERATION - PHASE 2 ARCHITECTURE MODULAIRE  🏗️")
    print("🚀 " + "=" * 58 + " 🚀")
    print()
    print("📅 Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🎯 Objectif: Créer architecture modulaire SRP")
    print("📊 Cibles: 4 fichiers god mode → modules spécialisés")
    print("⚡ Agents: Alpha (Claude) + Beta (GPT-4)")
    print()

def check_environment():
    """
    🔍 Vérifier environnement et prérequis
    """
    print("🔍 VÉRIFICATION ENVIRONNEMENT")
    print("-" * 40)
    
    # Vérifier clés API
    required_keys = {
        'ANTHROPIC_API_KEY': 'Claude Sonnet 4',
        'OPENAI_API_KEY': 'GPT-4 Turbo'
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: ****{value[-4:]} ({description})")
        else:
            print(f"❌ {key}: MANQUANTE ({description})")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"\n❌ ERREUR: Clés API manquantes: {', '.join(missing_keys)}")
        print("💡 Ajoutez-les dans votre fichier .env")
        return False
    
    # Vérifier Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python version insuffisante: {python_version.major}.{python_version.minor}")
        print("💡 Requis: Python 3.8+")
        return False
    else:
        print(f"✅ Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Vérifier modules requis
    required_modules = ['anthropic', 'openai', 'asyncio', 'pathlib', 'dataclasses']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module: {module}")
        except ImportError:
            print(f"❌ Module: {module} (manquant)")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ ERREUR: Modules manquants: {', '.join(missing_modules)}")
        print("💡 Installez avec: pip install anthropic openai")
        return False
    
    print("✅ Environnement validé!")
    return True

def check_phase1_results():
    """
    📊 Vérifier résultats Phase 1
    """
    print("\n📊 VÉRIFICATION PHASE 1")
    print("-" * 40)
    
    workspace = Path(__file__).parent
    phase1_results_path = workspace / "refactoring_workspace" / "results" / "phase1_cloud"
    
    if not phase1_results_path.exists():
        print("❌ Répertoire résultats Phase 1 manquant")
        return False
    
    # Chercher rapport Phase 1
    rapport_files = list(phase1_results_path.glob("phase1_cloud_rapport_*.md"))
    if not rapport_files:
        print("❌ Rapport Phase 1 manquant")
        return False
    
    latest_rapport = max(rapport_files, key=lambda f: f.stat().st_mtime)
    print(f"✅ Rapport Phase 1 trouvé: {latest_rapport.name}")
    
    # Chercher résultats JSON
    json_files = list(phase1_results_path.glob("phase1_cloud_results_*.json"))
    if not json_files:
        print("❌ Résultats JSON Phase 1 manquants")
        return False
    
    latest_json = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"✅ Résultats JSON trouvés: {latest_json.name}")
    
    # Vérifier analyses Alpha et Beta (dans répertoires parents)
    results_parent = phase1_results_path.parent
    alpha_path = results_parent / "alpha_claude"
    beta_path = results_parent / "beta_gemini"
    
    if alpha_path.exists():
        alpha_files = list(alpha_path.glob("*.json"))
        print(f"✅ Analyses Alpha: {len(alpha_files)} fichiers")
    else:
        print("❌ Analyses Alpha manquantes")
        return False
    
    if beta_path.exists():
        beta_files = list(beta_path.glob("*.json"))
        print(f"✅ Analyses Beta: {len(beta_files)} fichiers")
    else:
        print("❌ Analyses Beta manquantes")
        return False
    
    print("✅ Phase 1 validée!")
    return True

def check_workspace_structure():
    """
    📁 Vérifier structure workspace
    """
    print("\n📁 VÉRIFICATION WORKSPACE")
    print("-" * 40)
    
    workspace = Path(__file__).parent
    
    # Vérifier répertoires requis
    required_dirs = [
        "agents_refactoring",
        "refactoring_workspace",
        "orchestrator",
        "orchestrator_green"
    ]
    
    for dir_name in required_dirs:
        dir_path = workspace / dir_name
        if dir_path.exists():
            print(f"✅ Répertoire: {dir_name}")
        else:
            print(f"❌ Répertoire manquant: {dir_name}")
            return False
    
    # Vérifier agents Phase 2
    agents_path = workspace / "agents_refactoring"
    required_agents = [
        "agent_architect_alpha_claude_sonnet4.py",
        "agent_architect_beta_gpt4.py", 
        "orchestrator_phase2_architecture.py"
    ]
    
    for agent_file in required_agents:
        agent_path = agents_path / agent_file
        if agent_path.exists():
            print(f"✅ Agent: {agent_file}")
        else:
            print(f"❌ Agent manquant: {agent_file}")
            return False
    
    # Vérifier backup baseline
    backup_path = workspace / "refactoring_backups"
    if backup_path.exists():
        baseline_dirs = list(backup_path.glob("snapshots/baseline_*"))
        if baseline_dirs:
            latest_baseline = max(baseline_dirs, key=lambda d: d.stat().st_mtime)
            print(f"✅ Backup baseline: {latest_baseline.name}")
        else:
            print("❌ Backup baseline manquant")
            return False
    else:
        print("❌ Répertoire backup manquant")
        return False
    
    print("✅ Workspace structure validée!")
    return True

def show_phase2_objectives():
    """
    🎯 Afficher objectifs Phase 2
    """
    print("\n🎯 OBJECTIFS PHASE 2")
    print("-" * 40)
    
    objectives = [
        ("main.py", "1,990 lignes", "~100 lignes", "~95% réduction"),
        ("advanced_coordination.py", "779 lignes", "~150 lignes", "~81% réduction"), 
        ("redis_cluster_manager.py", "738 lignes", "~150 lignes", "~80% réduction"),
        ("monitoring.py", "709 lignes", "~150 lignes", "~79% réduction")
    ]
    
    print("📊 Fichiers God Mode → Modules SRP:")
    for file, current, target, reduction in objectives:
        print(f"  🔹 {file:<25} {current:>12} → {target:>10} ({reduction})")
    
    print("\n🏛️ Patterns Architecturaux:")
    patterns = [
        "Single Responsibility Principle (SRP)",
        "Dependency Injection Pattern",
        "Repository Pattern", 
        "Service Layer Pattern",
        "Factory Pattern",
        "Clean Architecture Layers"
    ]
    
    for pattern in patterns:
        print(f"  🔸 {pattern}")
    
    print("\n⚡ Agents Phase 2:")
    agents = [
        ("Alpha", "Claude Sonnet 4", "Plans architecturaux SRP"),
        ("Beta", "GPT-4 Turbo", "Architectures alternatives"),
        ("Orchestrateur", "Coordination", "Consensus & validation croisée")
    ]
    
    for name, model, role in agents:
        print(f"  🤖 {name:<12} ({model:<15}) → {role}")

async def execute_phase2():
    """
    🚀 Exécuter Phase 2 Architecture
    """
    print("\n🚀 DÉMARRAGE PHASE 2")
    print("-" * 40)
    
    try:
        # Import orchestrateur
        sys.path.append(str(Path(__file__).parent / "agents_refactoring"))
        from orchestrator_phase2_architecture import OrchestratorPhase2Architecture
        
        # Créer orchestrateur
        orchestrator = OrchestratorPhase2Architecture()
        
        # Exécuter Phase 2 complète
        print("🏗️ Lancement orchestrateur Phase 2...")
        results = await orchestrator.execute_phase2_complete()
        
        if results and results.success:
            print("\n🎉 PHASE 2 TERMINÉE AVEC SUCCÈS!")
            print(f"⏱️  Durée: {results.duration_seconds:.2f} secondes")
            print(f"📊 Plans Alpha: {len(results.alpha_plans)}")
            print(f"🔄 Alternatives Beta: {len(results.beta_alternatives)}")
            print(f"🎯 Plan final généré: {'✅' if results.final_architecture_plan else '❌'}")
            print(f"🚀 Prêt Phase 3: {'✅' if results.next_phase_ready else '❌'}")
            
            return True
        else:
            print("\n❌ ÉCHEC PHASE 2")
            return False
            
    except Exception as e:
        print(f"\n💥 ERREUR Phase 2: {e}")
        return False

async def main():
    """
    🎯 Point d'entrée principal
    """
    # Bannière
    print_banner()
    
    # Vérifications prérequis
    if not check_environment():
        sys.exit(1)
    
    if not check_phase1_results():
        print("\n💡 Exécutez d'abord: python start_phase1_cloud.py")
        sys.exit(1)
    
    if not check_workspace_structure():
        sys.exit(1)
    
    # Afficher objectifs
    show_phase2_objectives()
    
    # Confirmation utilisateur
    print("\n❓ CONFIRMATION")
    print("-" * 40)
    print("🎯 Démarrer Phase 2 Architecture Modulaire ?")
    print("⚡ Agents Alpha (Claude) + Beta (GPT-4) vont analyser 4 fichiers")
    print("🔄 Génération plans architecturaux avec validation croisée")
    
    # Auto-confirmation en mode script
    response = input("\n👉 Continuer ? (O/n): ").strip().lower()
    if response in ['n', 'non', 'no']:
        print("❌ Phase 2 annulée par l'utilisateur")
        sys.exit(0)
    
    # Exécution Phase 2
    success = await execute_phase2()
    
    if success:
        print("\n🎊 FÉLICITATIONS!")
        print("✅ Phase 2 Architecture terminée avec succès")
        print("🎯 Prochaine étape: Phase 3 Implémentation")
        print("📋 Consultez les rapports dans refactoring_workspace/results/phase2_architecture/")
        sys.exit(0)
    else:
        print("\n💥 ÉCHEC Phase 2")
        print("📋 Consultez les logs pour diagnostiquer le problème")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Phase 2 interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        sys.exit(1) 