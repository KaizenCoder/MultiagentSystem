#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 SCRIPT DE VALIDATION AUTOMATIQUE GPU - NEXTGENERATION
   Vérifie la compatibilité et la performance de l'environnement GPU.
"""

import sys
import logging
import torch

# --- Configuration Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("GPU_Validator")

def validate_gpu_environment():
    """
    Exécute une série de tests pour valider l'environnement GPU.
    """
    logger.info("--- 🚀 DÉMARRAGE DE LA VALIDATION GPU POUR NEXTGENERATION ---")

    # --- Test 1: Disponibilité de CUDA ---
    logger.info("--- Étape 1/4: Vérification de la disponibilité de CUDA ---")
    if torch.cuda.is_available():
        logger.info("✅ SUCCÈS: CUDA est disponible. Périphérique GPU détecté.")
    else:
        logger.error("❌ ÉCHEC: CUDA n'est pas disponible. Vérifiez l'installation de PyTorch et des drivers NVIDIA.")
        sys.exit(1)

    # --- Test 2: Informations sur le Périphérique ---
    logger.info("\n--- Étape 2/4: Récupération des informations sur le GPU ---")
    try:
        device_id = torch.cuda.current_device()
        gpu_name = torch.cuda.get_device_name(device_id)
        total_memory_gb = torch.cuda.get_device_properties(device_id).total_memory / (1024**3)
        
        logger.info(f"  - ID du Périphérique: {device_id}")
        logger.info(f"  - Modèle du GPU: {gpu_name}")
        logger.info(f"  - Mémoire Totale: {total_memory_gb:.2f} Go")

        if "RTX 3090" not in gpu_name:
            logger.warning("⚠️ AVERTISSEMENT: Le GPU détecté n'est pas une RTX 3090, modèle de référence du projet.")
        else:
            logger.info("✅ SUCCÈS: GPU de référence (NVIDIA RTX 3090) détecté.")
            
    except Exception as e:
        logger.error(f"❌ ÉCHEC: Impossible de récupérer les informations du GPU. Erreur: {e}")
        sys.exit(1)

    # --- Test 3: Opération Tensorielle Simple ---
    logger.info("\n--- Étape 3/4: Test d'une opération tensorielle sur le GPU ---")
    try:
        tensor_cpu = torch.rand(3, 3)
        logger.info("  - Tenseur créé sur le CPU.")
        
        tensor_gpu = tensor_cpu.to("cuda")
        logger.info("  - Tenseur déplacé vers le GPU.")
        
        result_gpu = tensor_gpu * tensor_gpu + 2
        logger.info("  - Opération (multiplication + addition) exécutée sur le GPU.")
        
        result_cpu = result_gpu.to("cpu")
        logger.info("  - Résultat rapatrié sur le CPU.")
        
        logger.info("✅ SUCCÈS: Les opérations tensorielles de base sur le GPU fonctionnent.")
    except Exception as e:
        logger.error(f"❌ ÉCHEC: L'opération tensorielle sur le GPU a échoué. Erreur: {e}")
        sys.exit(1)
        
    # --- Test 4: Disponibilité de cuDNN ---
    logger.info("\n--- Étape 4/4: Vérification de la disponibilité de cuDNN ---")
    if torch.backends.cudnn.is_available():
        logger.info(f"✅ SUCCÈS: cuDNN est disponible (Version: {torch.backends.cudnn.version()}).")
        if not torch.backends.cudnn.enabled:
            logger.warning("⚠️ AVERTISSEMENT: cuDNN est disponible mais n'est pas activé par défaut.")
    else:
        logger.warning("⚠️ AVERTISSEMENT: cuDNN n'est pas disponible. Les performances pour les réseaux de neurones profonds peuvent être réduites.")


    logger.info("\n--- ✅ VALIDATION GPU TERMINÉE AVEC SUCCÈS ---")
    logger.info("Votre environnement semble correctement configuré pour l'utilisation du GPU avec NextGeneration.")

if __name__ == "__main__":
    validate_gpu_environment() 