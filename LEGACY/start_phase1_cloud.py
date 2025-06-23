#!/usr/bin/env python3
"""
[ROCKET] Dmarrage Phase 1 - Refactoring NextGeneration Cloud
[ROBOT] Agents: Claude Sonnet 4 + Gemini 2.5
[LIGHTNING] Analyse parallle des fichiers god mode
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Configuration .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Import de l'orchestrateur cloud
sys.path.append(str(Path(__file__).parent / "agents_refactoring"))
from orchestrator_phase1_analysis_cloud import OrchestratorPhase1AnalysisCloud

def print_banner():
    """ Affichage du banner d'accueil"""
    print("" + "="*68 + "")
    print("[ROCKET]           PHASE 1 - ANALYSE PARALLLE CLOUD")
    print("[TARGET]           Configuration: APIs Claude + Gemini")
    print("[LIGHTNING]           Agents: Claude Sonnet 4 + Gemini 2.5")
    print("" + "="*68 + "")

def create_env_template():
    """[TOOL] Cration template .env"""
    env_file = Path(".env")
    
    if not env_file.exists():
        env_content = """# Configuration APIs Phase 1 Cloud
# Obtenez vos cls sur:
# - Claude: https://console.anthropic.com/
# - Gemini: https://ai.google.dev/

ANTHROPIC_API_KEY=votre_cl_claude_ici
GEMINI_API_KEY=votre_cl_gemini_ici

# Autres configurations optionnelles
# OPENAI_API_KEY=votre_cl_openai (pour Phase 2)
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f" Fichier .env cr: {env_file.absolute()}")
        print("[BULB] ditez le fichier .env avec vos vraies cls API")
        return False
    
    return True

def validate_environment():
    """[SEARCH] Validation environnement cloud"""
    print("\n[SEARCH] Validation environnement cloud...")
    
    # Vrification Python
    if sys.version_info < (3, 8):
        print("[CROSS] Python 3.8+ requis")
        return False
    
    print("[CHECK] Version Python compatible")
    
    # Vrification python-dotenv
    if not DOTENV_AVAILABLE:
        print("[CROSS] python-dotenv manquant")
        print("[BULB] Installation: pip install python-dotenv")
        return False
    
    print("[CHECK] python-dotenv disponible")
    
    # Vrification/Cration .env
    if not create_env_template():
        return False
    
    print("[CHECK] Fichier .env prsent")
    
    # Vrification packages requis
    required_packages = [
        ("anthropic", "Claude Sonnet 4"),
        ("google.generativeai", "Gemini 2.5")
    ]
    
    missing_packages = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"[CHECK] {description} disponible")
        except ImportError:
            missing_packages.append((package, description))
            print(f"[CROSS] {description} manquant")
    
    if missing_packages:
        print("\n[BULB] Installation requise:")
        for package, desc in missing_packages:
            if package == "anthropic":
                print("   pip install anthropic")
            elif package == "google.generativeai":
                print("   pip install google-generativeai")
        return False
    
    # Vrification cls API depuis .env
    api_keys = {
        "ANTHROPIC_API_KEY": "Claude Sonnet 4",
        "GEMINI_API_KEY": "Gemini 2.5"
    }
    
    missing_keys = []
    for key, desc in api_keys.items():
        value = os.getenv(key)
        if value and value != f"votre_cl_{key.split('_')[0].lower()}_ici":
            print(f"[CHECK] {desc} configur")
        else:
            missing_keys.append((key, desc))
            print(f"[CROSS] {desc} non configur dans .env")
    
    if missing_keys:
        print("\n[BULB] Configuration .env requise:")
        print(f"   ditez le fichier .env avec vos vraies cls:")
        for key, desc in missing_keys:
            print(f"   {key}=votre_vraie_cl_api")
        return False
    
    # Vrification workspace
    workspace = Path("refactoring_workspace")
    if workspace.exists():
        print("[CHECK] Workspace prt")
    else:
        workspace.mkdir(parents=True)
        print("[CHECK] Workspace cr")
    
    # Vrification agents
    agents_dir = Path("agents_refactoring")
    required_agents = [
        "agent_analyzer_alpha_claude_sonnet4.py",
        "agent_analyzer_beta_gemini25.py",
        "orchestrator_phase1_analysis_cloud.py"
    ]
    
    missing_agents = []
    for agent in required_agents:
        agent_path = agents_dir / agent
        if agent_path.exists():
            print(f"[CHECK] {agent}")
        else:
            missing_agents.append(agent)
            print(f"[CROSS] {agent}")
    
    if missing_agents:
        print("[CROSS] Agents manquants")
        return False
    
    print("[CHECK] Agents Phase 1 disponibles")
    return True

def confirm_start():
    """[TARGET] Confirmation utilisateur"""
    print("\n[LIGHTNING] Environnement valid - Dmarrage Phase 1...")
    print("\n[TARGET] Configuration Cloud:")
    print("    Agent Alpha: Claude Sonnet 4 (analyse approfondie)")
    print("    Agent Beta: Gemini 2.5 (analyse rapide)")
    print("    Analyse parallle: 4 fichiers god mode")
    print("    Dure estime: 2-5 minutes")
    print("    Cls API: charges depuis .env")
    
    while True:
        response = input("\n[TARGET] Confirmer dmarrage Phase 1 Cloud ? (o/N): ").strip().lower()
        if response in ['o', 'oui', 'y', 'yes']:
            return True
        elif response in ['n', 'non', 'no', '']:
            return False
        else:
            print(" Rpondez par 'o' pour oui ou 'n' pour non")

async def execute_phase1():
    """[ROCKET] Excution Phase 1"""
    print("\n[ROCKET] DMARRAGE PHASE 1 CONFIRM !")
    print("\n[ROCKET] Lancement Phase 1 - Analyse Parallle Cloud")
    
    print("\n Configuration Cloud:")
    print("    Alpha: Claude Sonnet 4 (prcision maximale)")
    print("    Beta: Gemini 2.5 (vitesse optimise)")
    print("    Config: Charge depuis .env")
    
    try:
        # Cration orchestrateur
        orchestrator = OrchestratorPhase1AnalysisCloud()
        
        # Excution
        success = await orchestrator.validate_cloud_environment()
        if not success:
            print("[CROSS] Validation choue")
            return False
        
        results = await orchestrator.execute_parallel_analysis()
        
        # Affichage rsultats
        print("\n" + "="*70)
        print(" PHASE 1 CLOUD TERMINE AVEC SUCCS!")
        print("="*70)
        
        print(f"\n[CHART] Rsultats:")
        print(f"    Fichiers analyss: {len(orchestrator.target_files)}")
        print(f"    Recommandations: {len(results.recommendations)}")
        print(f"    Prochaines tapes: {len(results.next_steps)}")
        
        # Recommandations critiques
        critical_recs = [r for r in results.recommendations if r["priority"] == "CRITIQUE"]
        if critical_recs:
            print(f"\n URGENT: {len(critical_recs)} fichier(s) critique(s)")
            for rec in critical_recs:
                print(f"    {rec['file']}")
        
        # Prochaines tapes
        print(f"\n[TARGET] Prochaines tapes:")
        for step in results.next_steps[:3]:  # Top 3
            print(f"    {step}")
        
        print(f"\n[FOLDER] Rsultats dtaills dans:")
        print(f"   refactoring_workspace/results/phase1_cloud/")
        
        return True
        
    except Exception as e:
        print(f"\n[CROSS] Erreur excution Phase 1: {str(e)}")
        return False

def main():
    """[TARGET] Point d'entre principal"""
    print_banner()
    
    # Validation environnement
    if not validate_environment():
        print("\n[CROSS] Validation environnement choue")
        print("[BULB] Corrigez les problmes ci-dessus et relancez")
        return False
    
    # Confirmation utilisateur
    if not confirm_start():
        print("\n Dmarrage annul par l'utilisateur")
        return False
    
    # Excution asynchrone
    try:
        success = asyncio.run(execute_phase1())
        
        if success:
            print("\n[CHECK] Phase 1 Cloud termine avec succs!")
            print("[TARGET] Consultez les rapports pour les prochaines tapes")
        else:
            print("\n[CROSS] Phase 1 Cloud choue")
            print("[BULB] Vrifiez les logs pour plus de dtails")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n Interruption utilisateur")
        return False
    except Exception as e:
        print(f"\n[CROSS] Erreur inattendue: {str(e)}")
        return False

if __name__ == "__main__":
    main() 



