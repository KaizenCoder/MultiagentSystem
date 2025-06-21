#!/usr/bin/env python3
"""
[ROCKET] DMARRAGE PHASE 4 - TESTS & QUALIT NEXTGENERATION
Script automatique pour lancer Phase 4 complte

Mission: Validation qualit enterprise de l'architecture refactorise
- Tests automatiss complets (Agent Test Generator)
- Validation qualit avance (Agent Testing Specialist)
- Certification production-ready
- Score qualit >90% requis

Excution: python start_phase4_testing.py
"""

import asyncio
import sys
import time
from pathlib import Path
from datetime import datetime

def print_header():
    """ Afficher header Phase 4"""
    print("\n" + "="*80)
    print(" NEXTGENERATION REFACTORING - PHASE 4")
    print(" TESTS & QUALIT - VALIDATION ENTERPRISE")
    print("="*80)
    
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[TARGET] Mission: Tests automatiss + Validation qualit")
    print(f"[ROBOT] Agents: Test Generator (Claude) + Testing Specialist (GPT-4)")
    print(f" Objectif: Certification production-ready (>90% qualit)")
    print("-"*80)

def check_prerequisites() -> bool:
    """[SEARCH] Vrifier prrequis Phase 4"""
    print("\n[SEARCH] VRIFICATION PRREQUIS PHASE 4")
    print("-"*50)
    
    all_good = True
    
    # 1. Vrifier Phase 3 termine
    print("1. [CHART] Vrification Phase 3 termine...")
    phase3_results = Path("refactoring_workspace/results/phase3_implementation")
    if phase3_results.exists():
        result_files = list(phase3_results.glob("*implementation_results_*.json"))
        if result_files:
            print("   [CHECK] Phase 3 termine - Architecture modulaire gnre")
        else:
            print("    Phase 3 incomplte - Rsultats manquants")
            all_good = False
    else:
        print("   [CROSS] Phase 3 non trouve - Requis pour Phase 4")
        all_good = False
    
    # 2. Vrifier architecture refactorise
    print("2. [CONSTRUCTION] Vrification architecture refactorise...")
    new_arch = Path("refactoring_workspace/new_architecture")
    if new_arch.exists():
        services = list((new_arch / "services").glob("*.py")) if (new_arch / "services").exists() else []
        routers = list((new_arch / "routers").glob("*.py")) if (new_arch / "routers").exists() else []
        main_file = new_arch / "main.py"
        
        if services and routers and main_file.exists():
            print(f"   [CHECK] Architecture modulaire: {len(services)} services, {len(routers)} routers")
        else:
            print("    Architecture incomplte - Services/routers manquants")
            all_good = False
    else:
        print("   [CROSS] Architecture refactorise manquante")
        all_good = False
    
    # 3. Vrifier agents Phase 4 
    print("3. [ROBOT] Vrification agents Phase 4...")
    agents_dir = Path("agents_refactoring")
    test_generator = agents_dir / "agent_test_generator_claude_sonnet4.py"
    testing_specialist = agents_dir / "agent_testing_specialist_gpt4.py"
    orchestrator = agents_dir / "orchestrator_phase4_testing.py"
    
    if test_generator.exists() and testing_specialist.exists() and orchestrator.exists():
        print("   [CHECK] Agents Phase 4 disponibles")
        print(f"      - Test Generator (Claude Sonnet 4): [CHECK]")
        print(f"      - Testing Specialist (GPT-4): [CHECK]")
        print(f"      - Orchestrateur Phase 4: [CHECK]")
    else:
        print("   [CROSS] Agents Phase 4 manquants")
        missing = []
        if not test_generator.exists(): missing.append("Test Generator")
        if not testing_specialist.exists(): missing.append("Testing Specialist")
        if not orchestrator.exists(): missing.append("Orchestrateur")
        print(f"      Manquants: {', '.join(missing)}")
        all_good = False
    
    # 4. Vrifier espace disque
    print("4.  Vrification espace disque...")
    try:
        import shutil
        free_space = shutil.disk_usage('.').free / (1024**3)  # GB
        if free_space > 1.0:  # 1GB minimum
            print(f"   [CHECK] Espace libre: {free_space:.1f} GB")
        else:
            print(f"    Espace limit: {free_space:.1f} GB")
    except:
        print("    Impossible vrifier espace disque")
    
    # 5. Vrifier modules Python requis
    print("5.  Vrification modules Python...")
    required_modules = ['asyncio', 'json', 'pathlib', 'dataclasses']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if not missing_modules:
        print("   [CHECK] Modules Python disponibles")
    else:
        print(f"   [CROSS] Modules manquants: {', '.join(missing_modules)}")
        all_good = False
    
    print("-"*50)
    if all_good:
        print("[CHECK] TOUS PRREQUIS VALIDS - PHASE 4 PRTE")
    else:
        print("[CROSS] PRREQUIS MANQUANTS - CORRECTION REQUISE")
    
    return all_good

def print_phase4_info():
    """[CLIPBOARD] Afficher informations Phase 4"""
    print("\n[CLIPBOARD] INFORMATIONS PHASE 4")
    print("-"*50)
    print("[TARGET] **OBJECTIFS:**")
    print("    Gnration tests automatiss enterprise")
    print("    Validation qualit >90% (mutation, coverage, performance)")
    print("    Tests charge 1000+ utilisateurs")
    print("    Tests scurit et vulnrabilits")
    print("    Certification production-ready")
    
    print("\n[ROBOT] **AGENTS COORDONNS:**")
    print("    Test Generator (Claude Sonnet 4) - Gnration tests")
    print("    Testing Specialist (GPT-4) - Validation qualit avance")
    print("    Orchestrateur Phase 4 - Coordination et certification")
    
    print("\n[CHART] **MTRIQUES CIBLES:**")
    print("    Score mutation: >95%")
    print("    Coverage tests: >85%")
    print("    Performance: >85% (charge 1000+ users)")
    print("    Scurit: >95%")
    print("    Rgression: 100%")
    
    print("\n **DURE ESTIME:** 30-60 secondes")
    print("-"*50)

def get_user_confirmation() -> bool:
    """ Demander confirmation utilisateur"""
    print("\n VALIDATION HUMAINE REQUISE")
    print("-"*40)
    print("La Phase 4 va:")
    print(" Analyser l'architecture refactorise Phase 3")
    print(" Gnrer suite complte de tests automatiss")
    print(" Excuter validation qualit enterprise")
    print(" Certifier architecture pour production")
    
    while True:
        response = input("\n[ROCKET] Dmarrer Phase 4 Tests & Qualit ? (o/n): ").lower().strip()
        if response in ['o', 'oui', 'y', 'yes']:
            return True
        elif response in ['n', 'non', 'no']:
            return False
        else:
            print(" Rponse invalide. Veuillez saisir 'o' ou 'n'")

async def execute_phase4():
    """
    [ROCKET] Excuter Phase 4 Tests & Qualit
    """
    print("\n[ROCKET] DMARRAGE PHASE 4")
    print("-" * 40)
    
    try:
        # Import orchestrateur
        sys.path.append(str(Path(__file__).parent / "agents_refactoring"))
        from orchestrator_phase4_testing import OrchestratorPhase4Testing
        
        # Crer orchestrateur
        orchestrator = OrchestratorPhase4Testing()
        
        # Excuter Phase 4 complte
        print(" Lancement orchestrateur Phase 4...")
        results = await orchestrator.execute_phase4_complete()
        
        if results and results.success:
            print("\n PHASE 4 TERMINE AVEC SUCCS!")
            print(f"  Dure: {results.duration_seconds:.2f} secondes")
            print(f" Tests gnrs: {results.test_generation.get('total_tests', 0)}")
            print(f"[CHART] Score qualit: {results.overall_quality_score:.1f}%")
            print(f" Certification: {results.certification_status}")
            print(f"[ROCKET] Production ready: {'[CHECK]' if results.production_ready else '[CROSS]'}")
            
            # Rsum succs
            print("\n" + "="*60)
            print(" RSUM REFACTORING NEXTGENERATION")
            print("="*60)
            print("[CHECK] Phase 0: Setup & Backup")
            print("[CHECK] Phase 1: Analyse God Mode Files")
            print("[CHECK] Phase 2: Architecture Modulaire")
            print("[CHECK] Phase 3: Implmentation (96.4% rduction)")
            print("[CHECK] Phase 4: Tests & Qualit")
            print("\n MISSION REFACTORING ACCOMPLIE!")
            
            return True
        else:
            print("\n[CROSS] CHEC PHASE 4")
            if results:
                print(f"Dure: {results.duration_seconds:.2f} secondes")
                print(f"Certification: {results.certification_status}")
            return False
            
    except Exception as e:
        print(f"\n ERREUR Phase 4: {e}")
        print("\n Vrifications suggres:")
        print(" Architecture Phase 3 complte")
        print(" Agents Phase 4 disponibles")
        print(" Modules Python installs")
        return False

def print_next_steps(success: bool):
    """[CLIPBOARD] Afficher prochaines tapes"""
    print("\n[CLIPBOARD] PROCHAINES TAPES")
    print("-"*40)
    
    if success:
        print(" **REFACTORING TERMIN AVEC SUCCS!**")
        print("\n[ROCKET] **Actions recommandes:**")
        print("   1. [CHART] Consulter rapport qualit Phase 4")
        print("   2.  Excuter tests gnrs:")
        print("      cd refactoring_workspace/results/phase4_tests/generated_tests")
        print("      pip install pytest pytest-cov")
        print("      pytest -v --cov")
        print("   3.  Prparer dploiement production")
        print("   4.  Surveiller mtriques en continu")
        
        print("\n **Accomplissements:**")
        print("    Architecture modulaire enterprise [CHECK]")
        print("    Rduction 96.4% complexity (1,99071 lignes) [CHECK]")
        print("    Patterns Hexagonal + CQRS + DI [CHECK]")
        print("    Suite tests automatiss [CHECK]")
        print("    Certification qualit enterprise [CHECK]")
    else:
        print(" **PHASE 4 NCESSITE CORRECTIONS**")
        print("\n[TOOL] **Actions requises:**")
        print("   1. [CHART] Analyser rapport d'erreurs Phase 4")
        print("   2. [SEARCH] Vrifier prrequis manquants")
        print("   3.  Corriger problmes identifis")
        print("   4.  Re-excuter Phase 4")
        
        print("\n[FOLDER] **Fichiers utiles:**")
        print("    refactoring_workspace/results/phase4_orchestrator/")
        print("    refactoring_workspace/results/phase4_tests/")
        print("    refactoring_workspace/results/phase4_quality/")

async def main():
    """[TARGET] Fonction principale"""
    start_time = time.time()
    
    # Header
    print_header()
    
    # Prrequis
    if not check_prerequisites():
        print("\n[CROSS] PRREQUIS NON SATISFAITS")
        print("Veuillez corriger les problmes identifis avant de continuer.")
        return False
    
    # Informations Phase 4
    print_phase4_info()
    
    # Confirmation utilisateur
    if not get_user_confirmation():
        print("\n PHASE 4 ANNULE PAR L'UTILISATEUR")
        return False
    
    print("\n" + "="*60)
    print("[ROCKET] LANCEMENT PHASE 4 - TESTS & QUALIT")
    print("="*60)
    
    # Excution Phase 4
    success = await execute_phase4()
    
    # Dure totale
    total_duration = time.time() - start_time
    print(f"\n DURE TOTALE: {total_duration:.2f} secondes")
    
    # Prochaines tapes
    print_next_steps(success)
    
    return success

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n INTERRUPTION UTILISATEUR")
        print("Phase 4 interrompue. tat:")
        print(" Architecture Phase 3 prserve")
        print(" Aucune modification systme")
        print(" Relancer: python start_phase4_testing.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n ERREUR CRITIQUE: {e}")
        sys.exit(1) 



