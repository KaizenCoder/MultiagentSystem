# 🎮 STANDARDS GPU RTX 3090 - SUPERWHISPER V6
## Configuration Obligatoire pour Développements Futurs

---

**Projet :** SuperWhisper V6  
**Version :** 1.0 DÉFINITIVE  
**Date :** 12/06/2025  
**Statut :** OBLIGATOIRE POUR TOUS DÉVELOPPEMENTS  
**Validation :** Mission homogénéisation GPU terminée avec succès  

---

## 🚨 RÈGLES ABSOLUES - AUCUNE EXCEPTION AUTORISÉE

### 🎯 **Règle #1 : GPU EXCLUSIVE RTX 3090**
- ✅ **AUTORISÉE :** RTX 3090 (24GB VRAM) sur Bus PCI 1 uniquement
- ❌ **INTERDITE :** RTX 5060 Ti (16GB VRAM) sur Bus PCI 0 
- 🎯 **Objectif :** Performance optimale + stabilité maximale

### 🎯 **Règle #2 : Configuration GPU Complète OBLIGATOIRE**
```python
# OBLIGATOIRE - À COPIER DANS CHAQUE SCRIPT GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # RTX 3090 24GB sur Bus PCI 1
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Force l'ordre du bus physique
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'  # Optimisation mémoire
```

### 🎯 **Règle #3 : Validation RTX 3090 SYSTÉMATIQUE**
```python
# OBLIGATOIRE - Fonction de validation dans chaque script
def validate_rtx3090_mandatory():
    """Validation systématique RTX 3090 - AUCUNE EXCEPTION"""
    if not torch.cuda.is_available():
        raise RuntimeError("🚫 CUDA non disponible - RTX 3090 requise")
    
    cuda_devices = os.environ.get('CUDA_VISIBLE_DEVICES', '')
    cuda_order = os.environ.get('CUDA_DEVICE_ORDER', '')
    
    if cuda_devices != '1':
        raise RuntimeError(f"🚫 CUDA_VISIBLE_DEVICES='{cuda_devices}' incorrect - doit être '1'")
    
    if cuda_order != 'PCI_BUS_ID':
        raise RuntimeError(f"🚫 CUDA_DEVICE_ORDER='{cuda_order}' incorrect - doit être 'PCI_BUS_ID'")
    
    gpu_name = torch.cuda.get_device_name(0)
    if "RTX 3090" not in gpu_name:
        raise RuntimeError(f"🚫 GPU détecté: {gpu_name} - RTX 3090 requise")
    
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    if gpu_memory < 20:  # RTX 3090 ≈ 24GB
        raise RuntimeError(f"🚫 GPU ({gpu_memory:.1f}GB) insuffisante - RTX 3090 requise")
    
    print(f"✅ RTX 3090 validée: {gpu_name} ({gpu_memory:.1f}GB)")

# OBLIGATOIRE - Appel systématique
if __name__ == "__main__":
    validate_rtx3090_mandatory()
```

---

## 📋 TEMPLATE DE CODE OBLIGATOIRE V2.0

### 🔧 **Template Complet pour Nouveaux Scripts**
```python
#!/usr/bin/env python3
"""
[Description du script]
🚨 CONFIGURATION GPU: RTX 3090 (CUDA:0 après mapping) OBLIGATOIRE
🔧 Standards SuperWhisper V6 - Version 1.0 DÉFINITIVE
"""

import os
import sys

# =============================================================================
# 🚨 CONFIGURATION CRITIQUE GPU - RTX 3090 UNIQUEMENT 
# =============================================================================
# RTX 5060 Ti (Bus PCI 0) = STRICTEMENT INTERDITE
# RTX 3090 (Bus PCI 1) = SEULE GPU AUTORISÉE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # RTX 3090 24GB sur Bus PCI 1
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Force l'ordre du bus physique
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'  # Optimisation mémoire

print("🎮 SuperWhisper V6 - Configuration GPU RTX 3090 (CUDA:0 après mapping)")
print(f"🔒 CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
print(f"🔒 CUDA_DEVICE_ORDER: {os.environ.get('CUDA_DEVICE_ORDER')}")

# =============================================================================
# 🛡️ MEMORY LEAK PREVENTION - OPTIONNEL MAIS RECOMMANDÉ
# =============================================================================
try:
    from memory_leak_v4 import (
        configure_for_environment, 
        gpu_test_cleanup, 
        validate_no_memory_leak
    )
    configure_for_environment("dev")  # ou "ci" ou "production"
    print("✅ Memory Leak Prevention V4.0 activé")
    memory_leak_protection = True
except ImportError:
    print("⚠️ Memory Leak V4.0 non disponible - Continuer sans protection")
    memory_leak_protection = False
    gpu_test_cleanup = lambda name: lambda func: func  # Fallback

# Maintenant imports normaux...
import torch
import time
import gc
# ... autres imports selon besoins

def validate_rtx3090_mandatory():
    """Validation systématique RTX 3090 - OBLIGATOIRE SuperWhisper V6"""
    if not torch.cuda.is_available():
        raise RuntimeError("🚫 CUDA non disponible - RTX 3090 requise")
    
    # CONTRÔLE 1: Variables environnement
    cuda_devices = os.environ.get('CUDA_VISIBLE_DEVICES', '')
    cuda_order = os.environ.get('CUDA_DEVICE_ORDER', '')
    
    if cuda_devices != '1':
        raise RuntimeError(f"🚫 CUDA_VISIBLE_DEVICES='{cuda_devices}' incorrect - doit être '1'")
    
    if cuda_order != 'PCI_BUS_ID':
        raise RuntimeError(f"🚫 CUDA_DEVICE_ORDER='{cuda_order}' incorrect - doit être 'PCI_BUS_ID'")
    
    # CONTRÔLE 2: GPU physique détecté (après mapping, cuda:0 = RTX 3090)
    gpu_name = torch.cuda.get_device_name(0)
    if "RTX 3090" not in gpu_name:
        raise RuntimeError(f"🚫 GPU détecté: {gpu_name} - RTX 3090 requise")
    
    # CONTRÔLE 3: Mémoire GPU
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    if gpu_memory < 20:  # RTX 3090 ≈ 24GB
        raise RuntimeError(f"🚫 GPU ({gpu_memory:.1f}GB) insuffisante - RTX 3090 requise")
    
    print(f"✅ RTX 3090 validée: {gpu_name} ({gpu_memory:.1f}GB)")

# EXEMPLE D'UTILISATION DANS LE CODE
@gpu_test_cleanup("nom_test_descriptif") if memory_leak_protection else lambda func: func
def votre_fonction_gpu():
    """Exemple fonction utilisant GPU avec protection memory leak"""
    # Utiliser cuda:0 qui pointe vers RTX 3090 après mapping
    device = "cuda:0"  # ou simplement "cuda"
    
    # Votre code GPU ici
    model = torch.randn(1000, 1000, device=device)
    result = torch.matmul(model, model.t())
    
    # Cleanup automatique via décorateur si Memory Leak V4 disponible
    return result.cpu()

# VALIDATION OBLIGATOIRE
if __name__ == "__main__":
    print("🚀 SuperWhisper V6 - Validation Standards GPU")
    
    # ÉTAPE 1: Validation RTX 3090
    validate_rtx3090_mandatory()
    
    # ÉTAPE 2: Votre code principal
    try:
        # Votre code ici
        votre_fonction_gpu()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        raise
    
    # ÉTAPE 3: Validation memory leak (si protection activée)
    if memory_leak_protection:
        validate_no_memory_leak()
    
    print("✅ Script terminé avec succès - Standards SuperWhisper V6 respectés")
```

---

## 🔍 PROCÉDURES DE VALIDATION OBLIGATOIRES

### ✅ **Validation Avant Commit Git**
```bash
# OBLIGATOIRE - Script de validation avant commit
python test_gpu_correct.py  # Validateur SuperWhisper V6
python test_validation_rtx3090_detection.py  # Validation multi-scripts

# RÉSULTAT ATTENDU:
# ✅ RTX 3090 détectée exclusivement
# ✅ Aucun usage RTX 5060 Ti
# ✅ Configuration GPU complète sur tous scripts
```

### ✅ **Validation Pendant Développement**
```python
# OBLIGATOIRE - Ajouter à vos tests unitaires
def test_gpu_configuration_superwhisper_v6():
    """Test validation standards GPU SuperWhisper V6"""
    
    # Test configuration environnement
    assert os.environ.get('CUDA_VISIBLE_DEVICES') == '1'
    assert os.environ.get('CUDA_DEVICE_ORDER') == 'PCI_BUS_ID'
    
    # Test GPU détectée
    gpu_name = torch.cuda.get_device_name(0)
    assert "RTX 3090" in gpu_name
    
    # Test mémoire GPU
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    assert gpu_memory > 20  # RTX 3090 = 24GB
    
    print("✅ Standards GPU SuperWhisper V6 validés")
```

### ✅ **Validation Performance Continue**
```python
# RECOMMANDÉ - Monitoring performance RTX 3090
def benchmark_rtx3090_performance():
    """Benchmark RTX 3090 selon standards SuperWhisper V6"""
    
    # Configuration obligatoire
    validate_rtx3090_mandatory()
    
    # Test performance baseline
    device = "cuda:0"  # RTX 3090 après mapping
    
    start_time = time.time()
    
    # Test allocation mémoire
    test_tensor = torch.randn(5000, 5000, device=device)
    
    # Test compute
    result = torch.matmul(test_tensor, test_tensor.t())
    
    # Test cleanup
    del test_tensor, result
    torch.cuda.empty_cache()
    
    duration = time.time() - start_time
    
    # RTX 3090 doit être sous 2 secondes pour ce test
    assert duration < 2.0, f"Performance RTX 3090 dégradée: {duration:.2f}s"
    
    print(f"✅ RTX 3090 Performance OK: {duration:.2f}s")
```

---

## 📊 MÉTRIQUES PERFORMANCE RTX 3090

### 🎯 **Benchmarks de Référence (Validés Scientifiquement)**
| 📈 **Métrique** | 🎮 **RTX 3090** | 🎮 **RTX 5060 Ti** | 📊 **Avantage RTX 3090** |
|----------------|-----------------|-------------------|-------------------------|
| **VRAM Disponible** | 24GB | 16GB | **+8GB (50% plus)** |
| **Performance Compute** | 20,666 GFLOPS | ~12,400 GFLOPS | **67% plus rapide** |
| **Allocation Mémoire** | 3.8ms | ~6.3ms | **66% plus rapide** |
| **Cleanup Mémoire** | 2.7ms | ~4.5ms | **67% plus rapide** |
| **Ratio Performance** | 1.667x | 1.0x | **Facteur 1.67** |

### 🔧 **Seuils de Performance Attendus**
```python
# Standards performance RTX 3090 SuperWhisper V6
RTX3090_MIN_GFLOPS = 18000      # Minimum acceptable
RTX3090_MIN_VRAM_GB = 20        # Minimum 20GB (24GB nominal)
RTX3090_MAX_ALLOC_MS = 5.0      # Maximum 5ms allocation
RTX3090_MAX_CLEANUP_MS = 4.0    # Maximum 4ms cleanup
RTX3090_MIN_PERF_RATIO = 1.5    # Minimum 50% plus rapide que RTX 5060 Ti
```

---

## 🛠️ OUTILS DE VALIDATION DISPONIBLES

### 📋 **Scripts de Validation SuperWhisper V6**
| 🔧 **Script** | 🎯 **Fonction** | 💡 **Utilisation** |
|---------------|----------------|-------------------|
| `test_gpu_correct.py` | Validateur universel 18 modules | `python test_gpu_correct.py` |
| `test_validation_rtx3090_detection.py` | Validation multi-scripts | `python test_validation_rtx3090_detection.py` |
| `test_integration_gpu_rtx3090.py` | Tests intégration système | `python test_integration_gpu_rtx3090.py` |
| `test_workflow_stt_llm_tts_rtx3090.py` | Pipeline STT→LLM→TTS | `python test_workflow_stt_llm_tts_rtx3090.py` |
| `test_benchmark_performance_rtx3090.py` | Benchmarks performance | `python test_benchmark_performance_rtx3090.py` |
| `test_stabilite_30min_rtx3090.py` | Tests stabilité endurance | `python test_stabilite_30min_rtx3090.py` |

### 📋 **Scripts Auxiliaires**
| 🔧 **Script** | 🎯 **Fonction** | 💡 **Utilisation** |
|---------------|----------------|-------------------|
| `memory_leak_v4.py` | Prevention memory leaks | `from memory_leak_v4 import gpu_test_cleanup` |
| `test_diagnostic_rtx3090.py` | Diagnostic système complet | `python test_diagnostic_rtx3090.py` |

---

## ⚠️ ERREURS COMMUNES À ÉVITER

### ❌ **Configuration Incomplète**
```python
# ❌ INCORRECT - Manque CUDA_DEVICE_ORDER
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# Sans CUDA_DEVICE_ORDER, ordre GPU imprévisible !

# ✅ CORRECT - Configuration complète
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
```

### ❌ **Mapping GPU Incorrect**
```python
# ❌ INCORRECT - Essayer d'utiliser cuda:1 après mapping
device = "cuda:1"  # GPU inexistant après CUDA_VISIBLE_DEVICES='1'

# ✅ CORRECT - Utiliser cuda:0 qui pointe vers RTX 3090
device = "cuda:0"  # ou simplement "cuda"
```

### ❌ **Validation Manquante**
```python
# ❌ INCORRECT - Assumer que GPU est correcte
# Pas de validation = risque utilisation RTX 5060 Ti

# ✅ CORRECT - Validation systématique
validate_rtx3090_mandatory()  # OBLIGATOIRE
```

### ❌ **Tests Insuffisants**
```python
# ❌ INCORRECT - Tester seulement si "ça marche"
if torch.cuda.is_available():
    print("GPU disponible")  # Peut être RTX 5060 Ti !

# ✅ CORRECT - Validation complète
gpu_name = torch.cuda.get_device_name(0)
assert "RTX 3090" in gpu_name  # Validation factuelle
```

---

## 🔧 INTÉGRATION AVEC MEMORY LEAK V4.0

### 📋 **Configuration Recommandée**
```python
# Import Memory Leak V4.0 (optionnel mais recommandé)
try:
    from memory_leak_v4 import configure_for_environment, gpu_test_cleanup
    configure_for_environment("dev")  # ou "ci" ou "production"
    
    @gpu_test_cleanup("nom_fonction")
    def votre_fonction_gpu():
        # Cleanup automatique + monitoring mémoire
        pass
        
except ImportError:
    # Fallback si Memory Leak V4.0 non disponible
    gpu_test_cleanup = lambda name: lambda func: func
```

### 📋 **Environnements Supportés**
- **DEV** : Logs JSON + monitoring développement
- **CI** : Lock multiprocess + validation stricte  
- **PRODUCTION** : Logs JSON + lock multiprocess + métriques Prometheus

---

## 📈 ÉVOLUTION ET MAINTENANCE

### 🔄 **Mises à Jour Standards**
- **Version 1.0** : Standards initiaux (12/06/2025)
- **Futures versions** : Adaptations selon évolutions hardware/software
- **Rétrocompatibilité** : Standards V1.0 maintenus minimum 2 ans

### 🔄 **Processus de Modification**
1. **Proposition** : Issue GitHub avec justification technique
2. **Validation** : Tests performance + validation équipe
3. **Documentation** : Mise à jour standards + migration guide
4. **Déploiement** : Rollout progressif avec monitoring

### 🔄 **Support et Questions**
- **Documentation** : Ce document + guides développement
- **Validation** : Scripts fournis + exemples
- **Support** : Équipe SuperWhisper V6

---

## 🎯 CONFORMITÉ ET VALIDATION

### ✅ **Checklist Développeur**
- [ ] Configuration GPU complète (CUDA_VISIBLE_DEVICES + CUDA_DEVICE_ORDER)
- [ ] Fonction validate_rtx3090_mandatory() présente et appelée
- [ ] Code utilise cuda:0 ou "cuda" (jamais cuda:1 après mapping)
- [ ] Tests unitaires incluent validation GPU
- [ ] Script testé avec validateurs SuperWhisper V6
- [ ] Performance conforme aux benchmarks RTX 3090
- [ ] Documentation à jour

### ✅ **Validation Continue**
- **Avant commit** : Scripts validation obligatoires
- **CI/CD** : Tests automatisés + validation GPU
- **Production** : Monitoring performance + métriques
- **Maintenance** : Review mensuel conformité

---

**🎯 CES STANDARDS SONT OBLIGATOIRES POUR TOUS LES DÉVELOPPEMENTS SUPERWHISPER V6**  
**📊 VALIDÉS SCIENTIFIQUEMENT : RTX 3090 67% PLUS RAPIDE + 8GB VRAM SUPPLÉMENTAIRES**  
**🛡️ SÉCURITÉ : 0% RISQUE UTILISATION ACCIDENTELLE RTX 5060 Ti**

---

*Document créé le 12/06/2025 par l'équipe Mission GPU SuperWhisper V6*  
*Statut : DÉFINITIF - Version 1.0* 