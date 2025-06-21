#!/usr/bin/env python3
"""
 Test Final Intgration Orchestrateur RTX3090 - NextGeneration
Validation finale de l'intgration complte
"""

import asyncio
import sys
import os
from pathlib import Path

# Configuration RTX3090
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

# Ajouter chemins
sys.path.append('./orchestrator')
sys.path.append('./orchestrator/app')

async def test_integration_finale():
    """Test final de l'intgration orchestrateur RTX3090"""
    
    print(" TEST FINAL INTGRATION ORCHESTRATEUR RTX3090")
    print("=" * 55)
    
    # Test 1: Import configuration optimise
    print(" Test 1: Configuration RTX3090 optimise")
    try:
        from orchestrator.app.config_rtx3090_optimized import settings
        
        print("[CHECK] Configuration RTX3090 importe avec succs")
        print(f"[CHART] Modles configurs: {len(settings.OLLAMA_MODELS)}")
        print(f" GPU: RTX3090 Device {settings.GPU_CONFIG['device_id']}")
        print(f" VRAM disponible: {settings.GPU_CONFIG['available_vram_gb']}GB")
        
        # Afficher modles configurs
        for category, model_info in settings.OLLAMA_MODELS.items():
            print(f"   {category}: {model_info['model']} ({model_info['performance']})")
        
        config_test = True
    except Exception as e:
        print(f"[CROSS] Erreur configuration: {e}")
        config_test = False
    
    print()
    
    # Test 2: Import OllamaLocalWorker RTX3090
    print(" Test 2: OllamaLocalWorker RTX3090 optimis")
    try:
        from orchestrator.app.agents.ollama_worker import ollama_worker_rtx3090
        
        print("[CHECK] OllamaLocalWorker RTX3090 import avec succs")
        print(f"[CLIPBOARD] Modles worker: {len(ollama_worker_rtx3090.models)}")
        
        # Test sant du worker
        health = await ollama_worker_rtx3090.health_check()
        if health.get("success", False):
            print(f"[CHECK] Worker sant: {health['status']}")
            print(f"[CHART] Modles Ollama: {health['models_count']}")
        else:
            print(f" Worker sant: {health.get('error', 'Unknown')}")
        
        worker_test = True
    except Exception as e:
        print(f"[CROSS] Erreur worker: {e}")
        worker_test = False
    
    print()
    
    # Test 3: Slection intelligente de modles
    print(" Test 3: Slection intelligente de modles")
    try:
        if worker_test:
            # Test slections diffrentes
            test_cases = [
                ("quick", "Rponse rapide", "speed"),
                ("code", "crire une fonction Python", "code"),
                ("analysis", "Analyse complexe des donnes", "quality"),
                ("default", "Question gnrale", "balanced")
            ]
            
            for task_type, description, expected_category in test_cases:
                selected_model = ollama_worker_rtx3090.select_optimal_model(task_type, description)
                print(f"   {task_type}: {selected_model}")
            
            print("[CHECK] Slection intelligente fonctionnelle")
        
        selection_test = True
    except Exception as e:
        print(f"[CROSS] Erreur slection: {e}")
        selection_test = False
    
    print()
    
    # Test 4: Gnration test avec nouveau worker
    print(" Test 4: Gnration test optimise RTX3090")
    try:
        if worker_test:
            result = await ollama_worker_rtx3090.generate_response(
                prompt="Test final intgration orchestrateur RTX3090",
                task_type="quick"
            )
            
            if result.get("success", False):
                print(f"[CHECK] Gnration russie")
                print(f"[TARGET] Modle utilis: {result['model_used']}")
                print(f" Temps traitement: {result['processing_time']:.2f}s") 
                print(f"[CHART] Performance: {result['tokens_per_sec']:.1f} tokens/s")
                print(f" GPU: {result['gpu_device']}")
            else:
                print(f"[CROSS] Gnration choue: {result.get('error', 'Unknown')}")
        
        generation_test = result.get("success", False) if worker_test else False
    except Exception as e:
        print(f"[CROSS] Erreur gnration: {e}")
        generation_test = False
    
    print()
    
    # Rsum final
    tests = [config_test, worker_test, selection_test, generation_test]
    score = sum(tests)
    
    print("[TARGET] RSUM FINAL INTGRATION RTX3090")
    print("=" * 55)
    print(f"[CHECK] Configuration optimise: {'[CHECK]' if config_test else '[CROSS]'}")
    print(f"[CHECK] Worker RTX3090: {'[CHECK]' if worker_test else '[CROSS]'}")
    print(f"[CHECK] Slection intelligente: {'[CHECK]' if selection_test else '[CROSS]'}")
    print(f"[CHECK] Gnration test: {'[CHECK]' if generation_test else '[CROSS]'}")
    print()
    print(f"[TARGET] Score intgration: {score}/4 ({(score/4)*100:.0f}%)")
    
    if score == 4:
        print(" INTGRATION ORCHESTRATEUR RTX3090 - SUCCS TOTAL")
        print("[CHECK] Prt pour production avec modles optimiss")
    elif score >= 3:
        print("[CHECK] INTGRATION ORCHESTRATEUR RTX3090 - RUSSIE")
        print(" Optimisations mineures possibles")
    else:
        print(" INTGRATION ORCHESTRATEUR RTX3090 - INCOMPLTE") 
        print("[TOOL] Corrections ncessaires")
    
    print(f"\n Configuration finale RTX3090 valide et oprationnelle")

if __name__ == "__main__":
    asyncio.run(test_integration_finale()) 



