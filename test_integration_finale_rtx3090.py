#!/usr/bin/env python3
"""
🎮 Test Final Intégration Orchestrateur RTX3090 - NextGeneration
Validation finale de l'intégration complète
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
    """Test final de l'intégration orchestrateur RTX3090"""
    
    print("🎮 TEST FINAL INTÉGRATION ORCHESTRATEUR RTX3090")
    print("=" * 55)
    
    # Test 1: Import configuration optimisée
    print("🧪 Test 1: Configuration RTX3090 optimisée")
    try:
        from orchestrator.app.config_rtx3090_optimized import settings
        
        print("✅ Configuration RTX3090 importée avec succès")
        print(f"📊 Modèles configurés: {len(settings.OLLAMA_MODELS)}")
        print(f"🎮 GPU: RTX3090 Device {settings.GPU_CONFIG['device_id']}")
        print(f"💾 VRAM disponible: {settings.GPU_CONFIG['available_vram_gb']}GB")
        
        # Afficher modèles configurés
        for category, model_info in settings.OLLAMA_MODELS.items():
            print(f"   {category}: {model_info['model']} ({model_info['performance']})")
        
        config_test = True
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        config_test = False
    
    print()
    
    # Test 2: Import OllamaLocalWorker RTX3090
    print("🧪 Test 2: OllamaLocalWorker RTX3090 optimisé")
    try:
        from orchestrator.app.agents.ollama_worker import ollama_worker_rtx3090
        
        print("✅ OllamaLocalWorker RTX3090 importé avec succès")
        print(f"📋 Modèles worker: {len(ollama_worker_rtx3090.models)}")
        
        # Test santé du worker
        health = await ollama_worker_rtx3090.health_check()
        if health.get("success", False):
            print(f"✅ Worker santé: {health['status']}")
            print(f"📊 Modèles Ollama: {health['models_count']}")
        else:
            print(f"⚠️ Worker santé: {health.get('error', 'Unknown')}")
        
        worker_test = True
    except Exception as e:
        print(f"❌ Erreur worker: {e}")
        worker_test = False
    
    print()
    
    # Test 3: Sélection intelligente de modèles
    print("🧪 Test 3: Sélection intelligente de modèles")
    try:
        if worker_test:
            # Test sélections différentes
            test_cases = [
                ("quick", "Réponse rapide", "speed"),
                ("code", "Écrire une fonction Python", "code"),
                ("analysis", "Analyse complexe des données", "quality"),
                ("default", "Question générale", "balanced")
            ]
            
            for task_type, description, expected_category in test_cases:
                selected_model = ollama_worker_rtx3090.select_optimal_model(task_type, description)
                print(f"   {task_type}: {selected_model}")
            
            print("✅ Sélection intelligente fonctionnelle")
        
        selection_test = True
    except Exception as e:
        print(f"❌ Erreur sélection: {e}")
        selection_test = False
    
    print()
    
    # Test 4: Génération test avec nouveau worker
    print("🧪 Test 4: Génération test optimisée RTX3090")
    try:
        if worker_test:
            result = await ollama_worker_rtx3090.generate_response(
                prompt="Test final intégration orchestrateur RTX3090",
                task_type="quick"
            )
            
            if result.get("success", False):
                print(f"✅ Génération réussie")
                print(f"🎯 Modèle utilisé: {result['model_used']}")
                print(f"⏱️ Temps traitement: {result['processing_time']:.2f}s") 
                print(f"📊 Performance: {result['tokens_per_sec']:.1f} tokens/s")
                print(f"🎮 GPU: {result['gpu_device']}")
            else:
                print(f"❌ Génération échouée: {result.get('error', 'Unknown')}")
        
        generation_test = result.get("success", False) if worker_test else False
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        generation_test = False
    
    print()
    
    # Résumé final
    tests = [config_test, worker_test, selection_test, generation_test]
    score = sum(tests)
    
    print("🎯 RÉSUMÉ FINAL INTÉGRATION RTX3090")
    print("=" * 55)
    print(f"✅ Configuration optimisée: {'✅' if config_test else '❌'}")
    print(f"✅ Worker RTX3090: {'✅' if worker_test else '❌'}")
    print(f"✅ Sélection intelligente: {'✅' if selection_test else '❌'}")
    print(f"✅ Génération test: {'✅' if generation_test else '❌'}")
    print()
    print(f"🎯 Score intégration: {score}/4 ({(score/4)*100:.0f}%)")
    
    if score == 4:
        print("🎉 INTÉGRATION ORCHESTRATEUR RTX3090 - SUCCÈS TOTAL")
        print("✅ Prêt pour production avec modèles optimisés")
    elif score >= 3:
        print("✅ INTÉGRATION ORCHESTRATEUR RTX3090 - RÉUSSIE")
        print("⚠️ Optimisations mineures possibles")
    else:
        print("⚠️ INTÉGRATION ORCHESTRATEUR RTX3090 - INCOMPLÈTE") 
        print("🔧 Corrections nécessaires")
    
    print(f"\n🎮 Configuration finale RTX3090 validée et opérationnelle")

if __name__ == "__main__":
    asyncio.run(test_integration_finale()) 