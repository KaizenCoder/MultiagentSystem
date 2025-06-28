#  wiki:
# 🎯 Wiki du projet : Utilisation et Standards de la RTX 3090

**Avertissement :** Ce document contient des informations techniques sensibles et des standards de configuration stricts. Le respect de ces directives est **obligatoire** pour garantir la performance, la stabilité et la sécurité de l'infrastructure GPU du projet NextGeneration.

## 1. 🚀 Synthèse Exécutive et Mission

La mission principale de ce sous-projet était d'intégrer et d'optimiser une carte graphique **NVIDIA RTX 3090 (24 Go)** comme unique accélérateur pour les tâches d'intelligence artificielle, en garantissant un environnement de production stable, performant et sécurisé.

**Statut du Projet : Mission Accomplie - Production Ready**
- **Validation** : Le système a été entièrement validé par un essaim d'agents autonomes, avec un score de 100%.
- **Performance** : Des performances de **4.9 à 8.2 tokens/seconde** ont été atteintes sur les modèles locaux, en fonction de leur complexité.
- **Optimisation** : **33 Go** d'espace de stockage ont été libérés grâce à la rationalisation des modèles.
- **Sécurité** : Le traitement 100% local des données garantit une confidentialité maximale.

## 2. 🚨 Standards Stricts de Configuration (Règles Non Négociables)

Ces règles ont été établies pour éliminer les problèmes de compatibilité et de performance liés à une configuration multi-GPU hétérogène (RTX 3090 + RTX 5060 Ti). **Aucune exception n'est autorisée.**

### Règle #1 : GPU Exclusif
- **GPU AUTORISÉ** : **NVIDIA RTX 3090 (24 Go)**, physiquement installée sur le **Bus PCI 1**.
- **GPU INTERDIT** : Toute autre carte, et en particulier la RTX 5060 Ti, ne doit pas être utilisée pour les calculs d'IA.

### Règle #2 : Configuration d'Environnement Obligatoire
Chaque script Python utilisant le GPU **doit impérativement** inclure la configuration d'environnement suivante au tout début du fichier, avant même les imports de bibliothèques comme PyTorch ou TensorFlow.

```python
import os

# CONFIGURATION CRITIQUE GPU - RTX 3090 UNIQUEMENT
# Cette configuration assure que seul le bon GPU est visible et utilisé par CUDA.
os.environ['CUDA_VISIBLE_DEVICES'] = '1'        # Cible la RTX 3090 sur le bus PCI 1.
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'  # Assure que l'ID est basé sur le bus physique.
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:1024'  # Optimisation de la fragmentation mémoire.
```

### Règle #3 : Validation Systématique dans le Code
Chaque script doit inclure et appeler une fonction de validation pour s'assurer que l'environnement est correctement configuré avant d'exécuter le moindre calcul.

```python
import torch

def validate_rtx3090_mandatory():
    """Valide que l'environnement respecte les standards stricts pour la RTX 3090."""
    if not torch.cuda.is_available():
        raise RuntimeError("ERREUR CRITIQUE: CUDA n'est pas disponible.")
    
    if os.environ.get('CUDA_VISIBLE_DEVICES') != '1':
        raise RuntimeError("ERREUR DE CONFIGURATION: CUDA_VISIBLE_DEVICES doit être '1'.")
        
    gpu_name = torch.cuda.get_device_name(0) # Doit être 0 car CUDA_VISIBLE_DEVICES mappe le device '1' à l'index '0'
    if "RTX 3090" not in gpu_name:
        raise RuntimeError(f"ERREUR CRITIQUE: Le GPU détecté est '{gpu_name}'. Seule la RTX 3090 est autorisée.")
    
    print("✅ Configuration GPU RTX 3090 validée avec succès.")

# Appeler cette fonction au début de l'exécution principale.
validate_rtx3090_mandatory()
```

## 3. 🏗️ Architecture Technique Détaillée

### Stack Logicielle de Référence
- **Driver NVIDIA**: `550.xx` ou supérieur
- **CUDA Toolkit**: `12.1` ou supérieur
- **PyTorch**: `2.1.0` ou supérieur (compilé pour CUDA 12.1)
- **Ollama**: Service de modèles de langage, configuré pour utiliser exclusivement la RTX 3090.

### Configuration du service Ollama
Ollama est configuré via des variables d'environnement pour s'exécuter **uniquement** sur la RTX 3090. Un script `.bat` est disponible pour lancer le service avec la bonne configuration.
- **Variables Clés**:
  - `CUDA_VISIBLE_DEVICES="1"`
  - `OLLAMA_GPU_DEVICE="1"`
  - `OLLAMA_NUM_GPU="1"`
- **Lancement**: Utiliser le script `start_ollama_rtx3090.bat` pour un démarrage conforme.

### Orchestrateur et Worker (`OllamaLocalWorker`)
L'orchestrateur du projet utilise un `worker` spécialisé, `OllamaLocalWorker`, qui est au cœur de l'intelligence du système.
- **Rôle**: Recevoir des tâches et sélectionner le modèle local le plus approprié pour les traiter.
- **Sélection Intelligente**: Le worker analyse les mots-clés de la tâche (ex: "code", "rapide", "analyse complexe") pour choisir dynamiquement parmi les 4 modèles optimisés.

## 4. 🚀 Guides d'Implémentation et d'Utilisation

### Configuration Initiale de l'Environnement
1.  **Optimisation Windows**: Réglez le plan d'alimentation sur "Performances élevées" et activez la "Planification de processeur graphique à accélération matérielle".
2.  **Panneau NVIDIA**: Réglez le mode de gestion de l'alimentation sur "Privilégier les performances maximales".
3.  **Lancement Ollama**: Exécutez le script `start_ollama_rtx3090.bat` pour démarrer le service de modèles sur le bon GPU.
4.  **Monitoring**: Lancez `start_monitor_rtx3090.bat` pour avoir une vue en temps réel de l'état du GPU (VRAM, température, utilisation).

### Template de Développement
Tous les nouveaux scripts doivent être basés sur le template `TEMPLATE DE CODE OBLIGATOIRE V2.0` défini dans `standards_gpu_rtx3090_definitifs.md`.

## 5. ✅ Validation et Rapports de Performance

Le système a été validé à l'aide de scripts et d'agents autonomes.
- **Script de validation des standards**: `VALIDATION_STANDARDS_RTX3090.py`
- **Rapport final d'intégration**: `RAPPORT_FINAL_INTEGRATION_ORCHESTRATEUR_RTX3090.md`
- **Rapport de validation d'Ollama**: `RAPPORT_FINAL_VALIDATION_OLLAMA_RTX3090.md`

Ces documents attestent que la configuration est stable, performante et conforme aux standards.

## 6. 🧠 Gestion des Modèles (Optimisation & Recommandations)

### Modèles Optimisés et Validés
La configuration de production repose sur 4 modèles principaux, chacun ayant un rôle spécifique :

| Modèle | Performance | Usage Optimal | Nom du modèle Ollama |
| :--- | :--- | :--- | :--- |
| **Qwen-Coder** | 8.2 tok/s | Génération de code, debugging | `qwen2.5-coder:1.5b` |
| **Nous-Hermes** | 6.4 tok/s | Réponses rapides, tâches simples | `nous-hermes-2-mistral-7b-dpo`|
| **Llama3-Q6K** | 4.9 tok/s | Usage général, équilibré | `llama3:8b-instruct-q6_k` |
| **Mixtral-Q3K**| 5.4 tok/s | Analyses complexes, haute qualité | `mixtral:8x7b-instruct-v0.1-q3_k_m` |

### Optimisation de la Mémoire
- Le modèle `Mixtral-8x7b` (26 Go) a été identifié comme étant trop volumineux pour la VRAM de la RTX 3090 (24 Go).
- **Solution**: Il a été remplacé par une version quantizée, `mixtral:8x7b-instruct-v0.1-q3_k_m`, qui offre une qualité similaire pour une empreinte mémoire bien plus faible.
- **Action continue**: Il est recommandé de supprimer les modèles redondants ou non optimisés pour libérer de l'espace disque. 