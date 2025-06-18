# 🛠️ GUIDE DÉVELOPPEMENT GPU RTX 3090 - SUPERWHISPER V6
## Manuel Pratique pour Développeurs

---

**Projet :** SuperWhisper V6  
**Audience :** Équipe Développement  
**Date :** 12/06/2025  
**Version :** 1.0 PRATIQUE  
**Prérequis :** [Standards GPU RTX 3090](docs/standards_gpu_rtx3090_definitifs.md)  

---

## 🎯 OBJECTIF DE CE GUIDE

Ce guide vous accompagne **étape par étape** pour développer des scripts compatibles avec les standards GPU SuperWhisper V6. Après lecture, vous saurez :

✅ **Intégrer** la configuration GPU RTX 3090 dans vos scripts  
✅ **Valider** votre code avec les outils fournis  
✅ **Éviter** les erreurs communes  
✅ **Optimiser** les performances GPU  
✅ **Maintenir** la conformité standards  

---

## 🚀 DÉMARRAGE RAPIDE - 5 MINUTES

### 📋 **Checklist Essentielle**
- [ ] 1. **Copier** le template de configuration GPU
- [ ] 2. **Ajouter** la validation RTX 3090  
- [ ] 3. **Utiliser** `cuda:0` dans votre code
- [ ] 4. **Tester** avec les validateurs fournis
- [ ] 5. **Valider** avant commit Git

### 📋 **Template Minimal (Copier-Coller)**
```python
#!/usr/bin/env python3
"""
Votre script SuperWhisper V6
🚨 CONFIGURATION GPU: RTX 3090 OBLIGATOIRE
"""

import os
import torch

# Configuration GPU RTX 3090 - OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

print("🎮 GPU Configuration RTX 3090 activée")

def validate_rtx3090_mandatory():
    """Validation RTX 3090 - OBLIGATOIRE"""
    if not torch.cuda.is_available():
        raise RuntimeError("🚫 CUDA non disponible - RTX 3090 requise")
    
    if os.environ.get('CUDA_VISIBLE_DEVICES') != '1':
        raise RuntimeError("🚫 CUDA_VISIBLE_DEVICES incorrect")
    
    if os.environ.get('CUDA_DEVICE_ORDER') != 'PCI_BUS_ID':
        raise RuntimeError("🚫 CUDA_DEVICE_ORDER incorrect") 
    
    gpu_name = torch.cuda.get_device_name(0)
    if "RTX 3090" not in gpu_name:
        raise RuntimeError(f"🚫 GPU détecté: {gpu_name} - RTX 3090 requise")
    
    print(f"✅ RTX 3090 validée: {gpu_name}")

# Votre code ici
if __name__ == "__main__":
    validate_rtx3090_mandatory()
    
    # Utiliser cuda:0 qui pointe vers RTX 3090
    device = "cuda:0"
    
    # Votre code GPU ici...
    
    print("✅ Script terminé avec succès")
```

---

## 📚 WORKFLOW DÉVELOPPEMENT COMPLET

### 🔄 **Étape 1 : Setup Initial**

#### 1.1 Vérifier l'Environnement
```bash
# Vérifier que RTX 3090 est disponible
nvidia-smi

# Vérifier PyTorch CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

#### 1.2 Récupérer les Outils de Validation
```bash
# S'assurer d'avoir les scripts de validation
ls test_gpu_correct.py
ls test_validation_rtx3090_detection.py
ls memory_leak_v4.py
```

### 🔄 **Étape 2 : Développement Script**

#### 2.1 Créer le Fichier avec Template
```python
# Utiliser le template minimal ci-dessus
# Remplacer "Votre script SuperWhisper V6" par description réelle
# Ajouter vos imports spécifiques après la configuration GPU
```

#### 2.2 Ajouter Votre Logique Métier
```python
# APRÈS validate_rtx3090_mandatory(), ajouter votre code

def votre_fonction_principale():
    """Votre logique métier ici"""
    device = "cuda:0"  # RTX 3090 après mapping
    
    # Exemple : Chargement modèle
    model = torch.nn.Linear(1000, 100).to(device)
    
    # Exemple : Traitement données
    data = torch.randn(32, 1000, device=device)
    output = model(data)
    
    return output.cpu()  # Retourner sur CPU si besoin

if __name__ == "__main__":
    validate_rtx3090_mandatory()
    
    try:
        result = votre_fonction_principale()
        print(f"✅ Traitement terminé: {result.shape}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        raise
```

### 🔄 **Étape 3 : Tests et Validation**

#### 3.1 Test Initial Script
```bash
# Tester votre script
python votre_script.py

# Résultat attendu:
# 🎮 GPU Configuration RTX 3090 activée
# ✅ RTX 3090 validée: NVIDIA GeForce RTX 3090
# ✅ Traitement terminé: torch.Size([32, 100])
# ✅ Script terminé avec succès
```

#### 3.2 Validation avec Outils SuperWhisper V6
```bash
# Validation complète
python test_gpu_correct.py

# Validation multi-scripts (inclut votre nouveau script)
python test_validation_rtx3090_detection.py

# Test performance (optionnel)
python test_benchmark_performance_rtx3090.py
```

### 🔄 **Étape 4 : Optimisation Performance**

#### 4.1 Intégration Memory Leak V4.0 (Recommandé)
```python
# Ajouter après la configuration GPU de base
try:
    from memory_leak_v4 import gpu_test_cleanup, configure_for_environment
    configure_for_environment("dev")
    memory_leak_protection = True
    print("✅ Memory Leak Prevention activé")
except ImportError:
    memory_leak_protection = False
    gpu_test_cleanup = lambda name: lambda func: func

# Utiliser le décorateur pour vos fonctions GPU
@gpu_test_cleanup("votre_fonction_principale") if memory_leak_protection else lambda func: func
def votre_fonction_principale():
    # Votre code ici - cleanup automatique
    pass
```

#### 4.2 Monitoring Performance
```python
import time

def benchmark_votre_fonction():
    """Benchmark performance de votre fonction"""
    validate_rtx3090_mandatory()
    
    start_time = time.time()
    
    # Votre fonction
    result = votre_fonction_principale()
    
    duration = time.time() - start_time
    
    # RTX 3090 doit être performante
    if duration > seuil_acceptable:
        print(f"⚠️ Performance potentiellement dégradée: {duration:.2f}s")
    else:
        print(f"✅ Performance RTX 3090 OK: {duration:.2f}s")
    
    return result
```

### 🔄 **Étape 5 : Finalisation et Commit**

#### 5.1 Tests Finaux
```bash
# Tests obligatoires avant commit
python votre_script.py
python test_gpu_correct.py
python test_validation_rtx3090_detection.py

# Tous doivent afficher "✅" pour RTX 3090
```

#### 5.2 Commit Git
```bash
# Commit avec message descriptif
git add votre_script.py
git commit -m "feat(gpu): Nouveau script avec standards RTX 3090 SuperWhisper V6

- Configuration GPU RTX 3090 complète
- Validation obligatoire implémentée  
- Tests validateurs réussis
- Conformité standards SuperWhisper V6"
```

---

## 🔧 EXEMPLES PRATIQUES PAR CAS D'USAGE

### 📋 **Cas 1 : Module STT (Speech-to-Text)**
```python
#!/usr/bin/env python3
"""
Module STT SuperWhisper V6 avec RTX 3090
🚨 CONFIGURATION GPU: RTX 3090 OBLIGATOIRE
"""

import os
import torch
# Configuration GPU RTX 3090 - OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

try:
    import whisper  # ou faster-whisper
except ImportError:
    print("⚠️ Module Whisper non disponible")

def validate_rtx3090_mandatory():
    """Validation RTX 3090 pour STT"""
    # [Code validation standard ici]
    pass

class STTHandler:
    def __init__(self):
        validate_rtx3090_mandatory()
        
        # RTX 3090 après mapping
        self.device = "cuda:0"
        
        # Charger modèle sur RTX 3090
        self.model = whisper.load_model("large-v2", device=self.device)
        
        print(f"✅ STT Handler initialisé sur RTX 3090")
    
    def transcribe(self, audio_path):
        """Transcription audio sur RTX 3090"""
        result = self.model.transcribe(audio_path)
        return result["text"]

if __name__ == "__main__":
    stt = STTHandler()
    # Tests...
```

### 📋 **Cas 2 : Module TTS (Text-to-Speech)**
```python
#!/usr/bin/env python3
"""
Module TTS SuperWhisper V6 avec RTX 3090
🚨 CONFIGURATION GPU: RTX 3090 OBLIGATOIRE
"""

import os
import torch
# Configuration GPU RTX 3090 - OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

try:
    from TTS.api import TTS
except ImportError:
    print("⚠️ Module TTS non disponible")

def validate_rtx3090_mandatory():
    """Validation RTX 3090 pour TTS"""
    # [Code validation standard ici]
    pass

class TTSHandler:
    def __init__(self, model_name="tts_models/fr/css10/vits"):
        validate_rtx3090_mandatory()
        
        # RTX 3090 après mapping
        self.device = "cuda:0"
        
        # Initialiser TTS sur RTX 3090
        self.tts = TTS(model_name=model_name, gpu=True)
        self.tts.to(self.device)
        
        print(f"✅ TTS Handler initialisé sur RTX 3090")
    
    def synthesize(self, text, output_path="output.wav"):
        """Synthèse vocale sur RTX 3090"""
        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path

if __name__ == "__main__":
    tts = TTSHandler()
    # Tests...
```

### 📋 **Cas 3 : Module LLM (Large Language Model)**
```python
#!/usr/bin/env python3
"""
Module LLM SuperWhisper V6 avec RTX 3090
🚨 CONFIGURATION GPU: RTX 3090 OBLIGATOIRE
"""

import os
import torch
# Configuration GPU RTX 3090 - OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
except ImportError:
    print("⚠️ Module Transformers non disponible")

def validate_rtx3090_mandatory():
    """Validation RTX 3090 pour LLM"""
    # [Code validation standard ici]
    pass

class LLMHandler:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        validate_rtx3090_mandatory()
        
        # RTX 3090 après mapping
        self.device = "cuda:0"
        
        # Charger modèle sur RTX 3090
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        
        print(f"✅ LLM Handler initialisé sur RTX 3090")
    
    def generate_response(self, input_text, max_length=100):
        """Génération réponse sur RTX 3090"""
        inputs = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs, 
                max_length=max_length,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

if __name__ == "__main__":
    llm = LLMHandler()
    # Tests...
```

### 📋 **Cas 4 : Script de Test/Validation**
```python
#!/usr/bin/env python3
"""
Script de test SuperWhisper V6 avec RTX 3090
🚨 CONFIGURATION GPU: RTX 3090 OBLIGATOIRE
"""

import os
import torch
import unittest
# Configuration GPU RTX 3090 - OBLIGATOIRE
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

def validate_rtx3090_mandatory():
    """Validation RTX 3090 pour tests"""
    # [Code validation standard ici]
    pass

class TestGPUConfiguration(unittest.TestCase):
    def setUp(self):
        """Setup tests avec validation RTX 3090"""
        validate_rtx3090_mandatory()
        self.device = "cuda:0"  # RTX 3090 après mapping
    
    def test_gpu_available(self):
        """Test GPU disponible"""
        self.assertTrue(torch.cuda.is_available())
    
    def test_rtx3090_detected(self):
        """Test RTX 3090 détectée"""
        gpu_name = torch.cuda.get_device_name(0)
        self.assertIn("RTX 3090", gpu_name)
    
    def test_memory_sufficient(self):
        """Test mémoire GPU suffisante"""
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        self.assertGreater(gpu_memory, 20)  # RTX 3090 = 24GB
    
    def test_tensor_operations(self):
        """Test opérations tensor sur RTX 3090"""
        x = torch.randn(100, 100, device=self.device)
        y = torch.matmul(x, x.t())
        self.assertEqual(y.device.type, 'cuda')

if __name__ == "__main__":
    print("🧪 Tests GPU SuperWhisper V6")
    unittest.main()
```

---

## ⚠️ RÉSOLUTION PROBLÈMES COURANTS

### 🚨 **Erreur : "RTX 3090 non détectée"**

#### **Diagnostic**
```python
# Script diagnostic rapide
import torch
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
print(f"CUDA_DEVICE_ORDER: {os.environ.get('CUDA_DEVICE_ORDER')}")
if torch.cuda.is_available():
    print(f"GPU détectée: {torch.cuda.get_device_name(0)}")
```

#### **Solutions**
1. **Vérifier configuration environnement**
   ```python
   # Ajouter AVANT imports torch
   os.environ['CUDA_VISIBLE_DEVICES'] = '1'
   os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
   ```

2. **Vérifier ordre dans le script**
   ```python
   # ✅ CORRECT - Configuration AVANT import torch
   import os
   os.environ['CUDA_VISIBLE_DEVICES'] = '1'
   import torch
   
   # ❌ INCORRECT - Configuration APRÈS import torch
   import torch
   os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # Trop tard !
   ```

3. **Redémarrer Python/Kernel**
   ```bash
   # Redémarrer complètement l'environnement Python
   exit()  # Quitter Python
   python votre_script.py  # Relancer
   ```

### 🚨 **Erreur : "CUDA out of memory"**

#### **Solutions**
1. **Optimiser allocation mémoire**
   ```python
   # Ajouter optimisation mémoire
   os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'
   
   # Cleanup périodique
   torch.cuda.empty_cache()
   ```

2. **Réduire taille batch**
   ```python
   # Réduire taille des tensors
   batch_size = 16  # Au lieu de 32 ou 64
   ```

3. **Monitoring mémoire**
   ```python
   def check_gpu_memory():
       if torch.cuda.is_available():
           allocated = torch.cuda.memory_allocated(0) / 1024**3
           cached = torch.cuda.memory_reserved(0) / 1024**3
           print(f"GPU Mémoire - Allouée: {allocated:.2f}GB, Cache: {cached:.2f}GB")
   ```

### 🚨 **Erreur : "Module not found"**

#### **Solutions**
1. **Imports conditionnels**
   ```python
   try:
       import whisper
   except ImportError:
       print("⚠️ Whisper non disponible - Tests limités")
       whisper = None
   
   # Utiliser avec vérification
   if whisper is not None:
       model = whisper.load_model("base")
   ```

2. **Installation dépendances**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install openai-whisper
   pip install TTS
   ```

---

## 🔍 VALIDATION ET DEBUGGING

### 📋 **Checklist Debug Étape par Étape**

#### **Étape 1 : Configuration GPU**
- [ ] `CUDA_VISIBLE_DEVICES='1'` défini AVANT import torch
- [ ] `CUDA_DEVICE_ORDER='PCI_BUS_ID'` défini
- [ ] `torch.cuda.is_available()` retourne `True`
- [ ] `torch.cuda.get_device_name(0)` contient "RTX 3090"

#### **Étape 2 : Code GPU**
- [ ] Utilisation `device = "cuda:0"` ou `device = "cuda"`
- [ ] Tensors/modèles bien transférés sur GPU avec `.to(device)`
- [ ] Pas d'utilisation `cuda:1` après mapping

#### **Étape 3 : Performance**
- [ ] Pas de memory leak détecté
- [ ] Performance conforme aux benchmarks RTX 3090
- [ ] Cleanup mémoire après usage

#### **Étape 4 : Tests**
- [ ] Script fonctionne en standalone
- [ ] Validation `test_gpu_correct.py` réussie
- [ ] Validation `test_validation_rtx3090_detection.py` réussie

### 📋 **Scripts Debug Personnalisés**

#### **Script Debug Minimal**
```python
#!/usr/bin/env python3
"""Debug GPU Configuration SuperWhisper V6"""

import os
# Configuration GPU AVANT import torch
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

import torch

def debug_gpu_config():
    print("🔍 DEBUG GPU CONFIGURATION")
    print("=" * 40)
    
    print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    print(f"CUDA_DEVICE_ORDER: {os.environ.get('CUDA_DEVICE_ORDER')}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"Device Count: {torch.cuda.device_count()}")
        print(f"Current Device: {torch.cuda.current_device()}")
        print(f"Device Name: {torch.cuda.get_device_name(0)}")
        
        props = torch.cuda.get_device_properties(0)
        print(f"Total Memory: {props.total_memory / 1024**3:.1f}GB")
        print(f"Allocated: {torch.cuda.memory_allocated(0) / 1024**3:.1f}GB")
        
        # Test simple
        x = torch.randn(100, 100, device="cuda:0")
        y = torch.matmul(x, x.t())
        print(f"Test Tensor OK: {y.shape}")
        
        if "RTX 3090" in torch.cuda.get_device_name(0):
            print("✅ RTX 3090 DÉTECTÉE ET FONCTIONNELLE")
        else:
            print("❌ RTX 3090 NON DÉTECTÉE")
    else:
        print("❌ CUDA NON DISPONIBLE")

if __name__ == "__main__":
    debug_gpu_config()
```

---

## 📊 BONNES PRATIQUES PERFORMANCE

### 🎯 **Optimisations RTX 3090**

#### **1. Gestion Mémoire Optimale**
```python
# Configuration mémoire optimisée pour RTX 3090
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'

# Cleanup périodique
def cleanup_gpu_memory():
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

# Monitoring mémoire
def monitor_gpu_memory(label=""):
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / 1024**3
        reserved = torch.cuda.memory_reserved(0) / 1024**3
        print(f"{label} - Allocated: {allocated:.2f}GB, Reserved: {reserved:.2f}GB")
```

#### **2. Batch Sizes Optimaux RTX 3090**
```python
# Tailles recommandées pour RTX 3090 (24GB)
OPTIMAL_BATCH_SIZES = {
    "whisper-large": 8,   # STT
    "tts-models": 16,     # TTS  
    "llm-7b": 4,          # LLM 7B
    "llm-13b": 2,         # LLM 13B
    "general": 32         # Opérations générales
}

def get_optimal_batch_size(task_type="general"):
    return OPTIMAL_BATCH_SIZES.get(task_type, 16)
```

#### **3. Context Managers pour Sécurité**
```python
from contextlib import contextmanager

@contextmanager
def rtx3090_context():
    """Context manager sécurisé pour RTX 3090"""
    validate_rtx3090_mandatory()
    
    initial_memory = torch.cuda.memory_allocated(0)
    
    try:
        yield "cuda:0"
    finally:
        # Cleanup automatique
        torch.cuda.empty_cache()
        
        final_memory = torch.cuda.memory_allocated(0)
        if final_memory > initial_memory + 100*1024*1024:  # 100MB tolerance
            print(f"⚠️ Possible memory leak: {(final_memory-initial_memory)/1024**3:.2f}GB")

# Utilisation
with rtx3090_context() as device:
    model = torch.nn.Linear(1000, 100).to(device)
    # Votre code ici
    # Cleanup automatique
```

---

## 📚 RESSOURCES ET RÉFÉRENCES

### 📋 **Documentation SuperWhisper V6**
- [Standards GPU RTX 3090 Définitifs](docs/standards_gpu_rtx3090_definitifs.md)
- [Journal Phase 4 Validation](docs/journal_phase4_validation.md)
- [Suivi Mission GPU](docs/suivi_mission_gpu.md)

### 📋 **Scripts de Validation**
- `test_gpu_correct.py` - Validateur universel
- `test_validation_rtx3090_detection.py` - Validation multi-scripts
- `test_integration_gpu_rtx3090.py` - Tests intégration
- `test_workflow_stt_llm_tts_rtx3090.py` - Pipeline complet
- `test_benchmark_performance_rtx3090.py` - Benchmarks performance
- `memory_leak_v4.py` - Prevention memory leaks

### 📋 **Commandes Utiles**
```bash
# Validation avant commit
python test_gpu_correct.py
python test_validation_rtx3090_detection.py

# Debug GPU
nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0))"

# Monitoring en temps réel
watch -n 1 nvidia-smi
```

---

## 🎯 CONCLUSION

Ce guide vous donne tous les outils pour développer efficacement avec les standards GPU SuperWhisper V6. **Points clés à retenir :**

✅ **Toujours** utiliser le template de configuration GPU  
✅ **Systématiquement** valider RTX 3090 avec `validate_rtx3090_mandatory()`  
✅ **Uniquement** utiliser `cuda:0` après mapping  
✅ **Obligatoirement** tester avec les validateurs fournis  
✅ **Maintenir** les performances RTX 3090  

**En cas de doute :** Consultez les exemples pratiques ou utilisez les scripts de debug fournis.

**Support :** Documentation complète + scripts validation + équipe SuperWhisper V6

---

**🎯 AVEC CE GUIDE, VOUS MAÎTRISEZ LES STANDARDS GPU SUPERWHISPER V6 !**  
**🚀 DÉVELOPPEMENT EFFICACE + PERFORMANCE RTX 3090 + CONFORMITÉ GARANTIE**

---

*Guide créé le 12/06/2025 par l'équipe Mission GPU SuperWhisper V6*  
*Version 1.0 PRATIQUE - Pour développeurs* 