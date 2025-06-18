#!/usr/bin/env python3
"""
🚀 Démarrage Phase 1 - Refactoring NextGeneration Cloud
🤖 Agents: Claude Sonnet 4 + Gemini 2.5
⚡ Analyse parallèle des fichiers god mode
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
    """🎮 Affichage du banner d'accueil"""
    print("🎮" + "="*68 + "🎮")
    print("🚀           PHASE 1 - ANALYSE PARALLÈLE CLOUD")
    print("🎯           Configuration: APIs Claude + Gemini")
    print("⚡           Agents: Claude Sonnet 4 + Gemini 2.5")
    print("🎮" + "="*68 + "🎮")

def create_env_template():
    """🔧 Création template .env"""
    env_file = Path(".env")
    
    if not env_file.exists():
        env_content = """# Configuration APIs Phase 1 Cloud
# Obtenez vos clés sur:
# - Claude: https://console.anthropic.com/
# - Gemini: https://ai.google.dev/

ANTHROPIC_API_KEY=votre_clé_claude_ici
GEMINI_API_KEY=votre_clé_gemini_ici

# Autres configurations optionnelles
# OPENAI_API_KEY=votre_clé_openai (pour Phase 2)
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"📝 Fichier .env créé: {env_file.absolute()}")
        print("💡 Éditez le fichier .env avec vos vraies clés API")
        return False
    
    return True

def validate_environment():
    """🔍 Validation environnement cloud"""
    print("\n🔍 Validation environnement cloud...")
    
    # Vérification Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    print("✅ Version Python compatible")
    
    # Vérification python-dotenv
    if not DOTENV_AVAILABLE:
        print("❌ python-dotenv manquant")
        print("💡 Installation: pip install python-dotenv")
        return False
    
    print("✅ python-dotenv disponible")
    
    # Vérification/Création .env
    if not create_env_template():
        return False
    
    print("✅ Fichier .env présent")
    
    # Vérification packages requis
    required_packages = [
        ("anthropic", "Claude Sonnet 4"),
        ("google.generativeai", "Gemini 2.5")
    ]
    
    missing_packages = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {description} disponible")
        except ImportError:
            missing_packages.append((package, description))
            print(f"❌ {description} manquant")
    
    if missing_packages:
        print("\n💡 Installation requise:")
        for package, desc in missing_packages:
            if package == "anthropic":
                print("   pip install anthropic")
            elif package == "google.generativeai":
                print("   pip install google-generativeai")
        return False
    
    # Vérification clés API depuis .env
    api_keys = {
        "ANTHROPIC_API_KEY": "Claude Sonnet 4",
        "GEMINI_API_KEY": "Gemini 2.5"
    }
    
    missing_keys = []
    for key, desc in api_keys.items():
        value = os.getenv(key)
        if value and value != f"votre_clé_{key.split('_')[0].lower()}_ici":
            print(f"✅ {desc} configuré")
        else:
            missing_keys.append((key, desc))
            print(f"❌ {desc} non configuré dans .env")
    
    if missing_keys:
        print("\n💡 Configuration .env requise:")
        print(f"   Éditez le fichier .env avec vos vraies clés:")
        for key, desc in missing_keys:
            print(f"   {key}=votre_vraie_clé_api")
        return False
    
    # Vérification workspace
    workspace = Path("refactoring_workspace")
    if workspace.exists():
        print("✅ Workspace prêt")
    else:
        workspace.mkdir(parents=True)
        print("✅ Workspace créé")
    
    # Vérification agents
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
            print(f"✅ {agent}")
        else:
            missing_agents.append(agent)
            print(f"❌ {agent}")
    
    if missing_agents:
        print("❌ Agents manquants")
        return False
    
    print("✅ Agents Phase 1 disponibles")
    return True

def confirm_start():
    """🎯 Confirmation utilisateur"""
    print("\n⚡ Environnement validé - Démarrage Phase 1...")
    print("\n🎯 Configuration Cloud:")
    print("   • Agent Alpha: Claude Sonnet 4 (analyse approfondie)")
    print("   • Agent Beta: Gemini 2.5 (analyse rapide)")
    print("   • Analyse parallèle: 4 fichiers god mode")
    print("   • Durée estimée: 2-5 minutes")
    print("   • Clés API: chargées depuis .env")
    
    while True:
        response = input("\n🎯 Confirmer démarrage Phase 1 Cloud ? (o/N): ").strip().lower()
        if response in ['o', 'oui', 'y', 'yes']:
            return True
        elif response in ['n', 'non', 'no', '']:
            return False
        else:
            print("🤔 Répondez par 'o' pour oui ou 'n' pour non")

async def execute_phase1():
    """🚀 Exécution Phase 1"""
    print("\n🚀 DÉMARRAGE PHASE 1 CONFIRMÉ !")
    print("\n🚀 Lancement Phase 1 - Analyse Parallèle Cloud")
    
    print("\n🎮 Configuration Cloud:")
    print("   • Alpha: Claude Sonnet 4 (précision maximale)")
    print("   • Beta: Gemini 2.5 (vitesse optimisée)")
    print("   • Config: Chargée depuis .env")
    
    try:
        # Création orchestrateur
        orchestrator = OrchestratorPhase1AnalysisCloud()
        
        # Exécution
        success = await orchestrator.validate_cloud_environment()
        if not success:
            print("❌ Validation échouée")
            return False
        
        results = await orchestrator.execute_parallel_analysis()
        
        # Affichage résultats
        print("\n" + "="*70)
        print("🎉 PHASE 1 CLOUD TERMINÉE AVEC SUCCÈS!")
        print("="*70)
        
        print(f"\n📊 Résultats:")
        print(f"   • Fichiers analysés: {len(orchestrator.target_files)}")
        print(f"   • Recommandations: {len(results.recommendations)}")
        print(f"   • Prochaines étapes: {len(results.next_steps)}")
        
        # Recommandations critiques
        critical_recs = [r for r in results.recommendations if r["priority"] == "CRITIQUE"]
        if critical_recs:
            print(f"\n🚨 URGENT: {len(critical_recs)} fichier(s) critique(s)")
            for rec in critical_recs:
                print(f"   • {rec['file']}")
        
        # Prochaines étapes
        print(f"\n🎯 Prochaines étapes:")
        for step in results.next_steps[:3]:  # Top 3
            print(f"   • {step}")
        
        print(f"\n📁 Résultats détaillés dans:")
        print(f"   refactoring_workspace/results/phase1_cloud/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur exécution Phase 1: {str(e)}")
        return False

def main():
    """🎯 Point d'entrée principal"""
    print_banner()
    
    # Validation environnement
    if not validate_environment():
        print("\n❌ Validation environnement échouée")
        print("💡 Corrigez les problèmes ci-dessus et relancez")
        return False
    
    # Confirmation utilisateur
    if not confirm_start():
        print("\n🛑 Démarrage annulé par l'utilisateur")
        return False
    
    # Exécution asynchrone
    try:
        success = asyncio.run(execute_phase1())
        
        if success:
            print("\n✅ Phase 1 Cloud terminée avec succès!")
            print("🎯 Consultez les rapports pour les prochaines étapes")
        else:
            print("\n❌ Phase 1 Cloud échouée")
            print("💡 Vérifiez les logs pour plus de détails")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n🛑 Interruption utilisateur")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {str(e)}")
        return False

if __name__ == "__main__":
    main() 