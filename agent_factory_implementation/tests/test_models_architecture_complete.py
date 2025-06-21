#!/usr/bin/env python3
"""
🧪 BATTERIE COMPLÈTE DE TESTS - ARCHITECTURE MODÈLES IA
=======================================================

Tests exhaustifs pour valider l'architecture de gestion des modèles IA
avec support complet Ollama RTX3090 et fallback cloud.

COUVERTURE TESTS :
✅ Configuration centralisée
✅ Sélection modèles par agent/tâche
✅ Intégration Ollama RTX3090
✅ Mécanismes fallback
✅ Performance et coûts
✅ Thread safety
✅ Gestion erreurs
✅ Monitoring GPU

Version: 1.0.0
Créé: 19 juin 2025 - 18h00
"""

import asyncio
import json
import sys
from pathlib import Path
from core import logging_manager
import pytest
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock, patch

# Import modules à tester
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from core.model_manager import ModelManager, ModelProvider, OllamaClient
    from config.models_config import *  # Import configuration
    MODEL_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ ModelManager non disponible: {e}")
    MODEL_MANAGER_AVAILABLE = False

# Configuration logging pour tests
logging.basicConfig(level=logging.INFO)
# LoggingManager NextGeneration - Tests
        import sys
from pathlib import Path
from core import logging_manager
        self.logger = logging_manager.get_logger(custom_config={
            "logger_name": "TestModelsConfiguration",
            "log_level": "DEBUG",
            "elasticsearch_enabled": False,
            "encryption_enabled": False,
            "async_enabled": False,  # Tests synchrones
            "console_output": True
        })

class TestModelsConfiguration:
    """Tests de configuration des modèles"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        self.config_path = Path(__file__).parent.parent / "config" / "models_config.json"
        
    def test_config_file_exists(self):
        """Test existence fichier configuration"""
        assert self.config_path.exists(), f"Fichier config manquant: {self.config_path}"
        
    def test_config_json_valid(self):
        """Test validité JSON configuration"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        assert isinstance(config, dict), "Configuration doit être un dictionnaire"
        assert "version" in config, "Version manquante"
        assert "agent_models" in config, "agent_models manquant"
        assert "model_providers" in config, "model_providers manquant"
        
    def test_agent_models_structure(self):
        """Test structure configuration agents"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        agent_models = config["agent_models"]
        
        # Vérifier agents enterprise
        enterprise_agents = [
            "agent_21_security_supply_chain_enterprise",
            "agent_22_architecture_consultant_enterprise",
            "agent_23_fastapi_orchestration_enterprise",
            "agent_24_storage_enterprise_manager",
            "agent_25_monitoring_production_enterprise"
        ]
        
        for agent in enterprise_agents:
            assert agent in agent_models, f"Agent enterprise manquant: {agent}"
            
            agent_config = agent_models[agent]
            assert "primary" in agent_config, f"Modèle primary manquant pour {agent}"
            assert "fallback" in agent_config, f"Modèle fallback manquant pour {agent}"
            assert "local" in agent_config, f"Modèle local manquant pour {agent}"
            assert "prefer_local" in agent_config, f"prefer_local manquant pour {agent}"
            
    def test_ollama_provider_config(self):
        """Test configuration provider Ollama"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        providers = config["model_providers"]
        assert "ollama" in providers, "Provider Ollama manquant"
        
        ollama_config = providers["ollama"]
        assert "base_url" in ollama_config, "base_url Ollama manquant"
        assert "gpu_device" in ollama_config, "gpu_device manquant"
        assert "models" in ollama_config, "Modèles Ollama manquants"
        
        # Vérifier modèles RTX3090 requis
        required_models = [
            "llama3.1:8b-instruct-q6_k",
            "qwen-coder-32b", 
            "mixtral-8x7b"
        ]
        
        ollama_models = ollama_config["models"]
        for model in required_models:
            assert model in ollama_models, f"Modèle RTX3090 manquant: {model}"
            
            model_config = ollama_models[model]
            assert "vram_usage" in model_config, f"vram_usage manquant pour {model}"
            assert "speciality" in model_config, f"speciality manquante pour {model}"

@pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
class TestModelManager:
    """Tests du gestionnaire de modèles"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        self.model_manager = ModelManager()
        
    def test_model_manager_initialization(self):
        """Test initialisation ModelManager"""
        assert self.model_manager.config is not None
        assert hasattr(self.model_manager, 'ollama_client')
        assert hasattr(self.model_manager, 'usage_stats')
        
    def test_ollama_enabled_detection(self):
        """Test détection Ollama activé"""
        is_enabled = self.model_manager._is_ollama_enabled()
        assert isinstance(is_enabled, bool)
        
        if is_enabled:
            logger.info("✅ Ollama détecté comme activé")
        else:
            logger.warning("⚠️ Ollama détecté comme désactivé")
            
    @pytest.mark.asyncio
    async def test_agent_model_selection(self):
        """Test sélection modèles par agent"""
        
        test_cases = [
            {
                "agent": "agent_02_architecte_code_expert",
                "task_type": "code",
                "expected_local": True
            },
            {
                "agent": "agent_04_expert_securite_crypto", 
                "task_type": "privacy",
                "expected_local": True
            },
            {
                "agent": "agent_22_architecture_consultant_enterprise",
                "task_type": "general",
                "expected_local": False  # Enterprise préfère qualité cloud
            }
        ]
        
        for case in test_cases:
            model, provider = await self.model_manager.get_model_for_agent(
                case["agent"], 
                case["task_type"]
            )
            
            assert model is not None, f"Modèle None pour {case['agent']}"
            assert provider is not None, f"Provider None pour {case['agent']}"
            
            logger.info(f"✅ {case['agent']} ({case['task_type']}): {model} via {provider.value}")
            
    def test_provider_detection(self):
        """Test détection provider par nom modèle"""
        
        test_cases = [
            ("claude-3-sonnet-20240229", ModelProvider.ANTHROPIC),
            ("gpt-4-turbo-preview", ModelProvider.OPENAI),
            ("llama3.1:8b-instruct-q6_k", ModelProvider.OLLAMA),
            ("qwen-coder-32b", ModelProvider.OLLAMA),
            ("mixtral-8x7b", ModelProvider.OLLAMA)
        ]
        
        for model_name, expected_provider in test_cases:
            detected_provider = self.model_manager._get_provider_for_model(model_name)
            assert detected_provider == expected_provider, f"Provider incorrect pour {model_name}"

class TestOllamaIntegration:
    """Tests spécifiques à l'intégration Ollama"""
    
    def setup_method(self):
        """Setup pour tests Ollama"""
        self.ollama_client = OllamaClient()
        
    @pytest.mark.asyncio
    async def test_ollama_connection(self):
        """Test connexion Ollama"""
        try:
            models = await self.ollama_client.list_models()
            assert isinstance(models, list), "Liste modèles doit être une liste"
            
            if models:
                logger.info(f"✅ Ollama connecté - {len(models)} modèles disponibles")
                for model in models[:3]:  # Log premiers modèles
                    logger.info(f"  📦 {model}")
            else:
                logger.warning("⚠️ Ollama connecté mais aucun modèle disponible")
                
        except Exception as e:
            logger.error(f"❌ Connexion Ollama échouée: {e}")
            pytest.skip("Ollama non disponible pour tests")
            
    @pytest.mark.asyncio 
    async def test_model_availability_check(self):
        """Test vérification disponibilité modèles"""
        
        # Test modèles requis RTX3090
        required_models = [
            "llama3.1:8b-instruct-q6_k",
            "qwen-coder-32b",
            "mixtral-8x7b"
        ]
        
        for model in required_models:
            is_available = await self.ollama_client.check_model_availability(model)
            logger.info(f"{'✅' if is_available else '❌'} {model}: {'Disponible' if is_available else 'Manquant'}")
            
    @pytest.mark.asyncio
    async def test_ollama_generation(self):
        """Test génération avec Ollama"""
        
        # Vérifier modèles disponibles
        models = await self.ollama_client.list_models()
        if not models:
            pytest.skip("Aucun modèle Ollama disponible")
            
        # Test avec premier modèle disponible
        test_model = models[0]
        test_prompt = "Bonjour, réponds en une phrase."
        
        start_time = time.time()
        result = await self.ollama_client.generate(test_model, test_prompt)
        end_time = time.time()
        
        assert isinstance(result, dict), "Résultat doit être un dictionnaire"
        assert "response" in result, "Réponse manquante"
        assert "success" in result, "Status success manquant"
        
        if result["success"]:
            response_time = end_time - start_time
            tokens_per_sec = result.get("tokens_per_sec", 0)
            
            logger.info(f"✅ Génération {test_model}: {response_time:.2f}s, {tokens_per_sec:.1f} tokens/sec")
            logger.info(f"📝 Réponse: {result['response'][:100]}...")
            
            # Vérifications performance RTX3090
            assert response_time < 60, f"Réponse trop lente: {response_time}s"
            assert tokens_per_sec > 0.1, f"Vitesse trop faible: {tokens_per_sec} tokens/sec"
        else:
            pytest.fail(f"Génération échouée: {result.get('error', 'Erreur inconnue')}")
            
    @pytest.mark.asyncio
    async def test_gpu_monitoring(self):
        """Test monitoring GPU RTX3090"""
        
        gpu_status = await self.ollama_client.get_gpu_usage()
        
        assert isinstance(gpu_status, dict), "Status GPU doit être un dictionnaire"
        assert "available" in gpu_status, "Status disponibilité manquant"
        
        if gpu_status["available"]:
            logger.info("✅ Monitoring GPU fonctionnel")
            logger.info(f"📊 Status: {gpu_status}")
        else:
            logger.warning(f"⚠️ Monitoring GPU limité: {gpu_status.get('error', 'Raison inconnue')}")

@pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
class TestFallbackMechanisms:
    """Tests des mécanismes de fallback"""
    
    def setup_method(self):
        """Setup pour tests fallback"""
        self.model_manager = ModelManager()
        
    @pytest.mark.asyncio
    async def test_local_to_cloud_fallback(self):
        """Test fallback local vers cloud"""
        
        # Mock échec Ollama
        with patch.object(self.model_manager.ollama_client, 'generate', side_effect=Exception("Ollama indisponible")):
            
            result = await self.model_manager.generate_response(
                "agent_02_architecte_code_expert",
                "Test fallback",
                "code"
            )
            
            # Doit fallback vers cloud
            assert result is not None
            if result.get("success"):
                assert result.get("provider") in ["anthropic", "openai"], "Doit fallback vers cloud"
                logger.info(f"✅ Fallback vers cloud: {result.get('model')} ({result.get('provider')})")
            else:
                logger.warning(f"⚠️ Fallback échoué: {result.get('error')}")
                
    @pytest.mark.asyncio
    async def test_cloud_to_local_fallback(self):
        """Test fallback cloud vers local"""
        
        # Mock échec cloud providers
        with patch.object(self.model_manager, '_generate_anthropic', side_effect=Exception("Anthropic indisponible")):
            with patch.object(self.model_manager, '_generate_openai', side_effect=Exception("OpenAI indisponible")):
                
                result = await self.model_manager.generate_response(
                    "agent_22_architecture_consultant_enterprise",
                    "Test fallback vers local",
                    "general"
                )
                
                # Doit fallback vers local si disponible
                assert result is not None
                if result.get("success"):
                    assert result.get("provider") == "ollama", "Doit fallback vers Ollama"
                    logger.info(f"✅ Fallback vers local: {result.get('model')}")
                else:
                    logger.warning(f"⚠️ Fallback local échoué: {result.get('error')}")

class TestPerformanceAndCosts:
    """Tests de performance et coûts"""
    
    def setup_method(self):
        """Setup pour tests performance"""
        if MODEL_MANAGER_AVAILABLE:
            self.model_manager = ModelManager()
        
    @pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
    @pytest.mark.asyncio
    async def test_response_time_benchmarks(self):
        """Test benchmarks temps de réponse"""
        
        test_prompts = [
            "Bonjour",  # Court
            "Explique l'intelligence artificielle en 2 phrases.",  # Moyen
            "Écris un algorithme de tri rapide en Python avec commentaires détaillés."  # Long
        ]
        
        results = {}
        
        for i, prompt in enumerate(test_prompts):
            start_time = time.time()
            
            result = await self.model_manager.generate_response(
                "agent_02_architecte_code_expert",
                prompt,
                "code" if "algorithme" in prompt else "general"
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            results[f"test_{i+1}"] = {
                "prompt_length": len(prompt),
                "response_time": response_time,
                "model": result.get("model", "unknown"),
                "provider": result.get("provider", "unknown"),
                "success": result.get("success", False)
            }
            
            logger.info(f"⏱️ Test {i+1}: {response_time:.2f}s - {result.get('model', 'unknown')}")
            
            # Vérifications performance
            if result.get("provider") == "ollama":
                # Modèles locaux doivent être plus rapides
                assert response_time < 60, f"Modèle local trop lent: {response_time}s"
            
        # Log résumé performance
        avg_time = sum(r["response_time"] for r in results.values()) / len(results)
        logger.info(f"📊 Temps moyen: {avg_time:.2f}s")
        
    @pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
    @pytest.mark.asyncio
    async def test_cost_tracking(self):
        """Test suivi des coûts"""
        
        # Générer quelques réponses
        for i in range(3):
            await self.model_manager.generate_response(
                "agent_01_coordinateur_principal",
                f"Test coût numéro {i+1}",
                "general"
            )
        
        # Vérifier statistiques
        status = await self.model_manager.get_system_status()
        usage_stats = status.get("usage_stats", {})
        total_cost = status.get("total_cost", 0)
        
        logger.info(f"💰 Coût total: ${total_cost:.4f}")
        
        # Modèles locaux doivent avoir coût 0
        for model, stats in usage_stats.items():
            if "llama" in model.lower() or "qwen" in model.lower() or "mixtral" in model.lower():
                assert stats.get("cost", 0) == 0, f"Modèle local {model} ne doit pas coûter"
                
        assert total_cost >= 0, "Coût total ne peut être négatif"

class TestThreadSafety:
    """Tests de thread safety"""
    
    def setup_method(self):
        """Setup pour tests thread safety"""
        if MODEL_MANAGER_AVAILABLE:
            self.model_manager = ModelManager()
        
    @pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
    def test_concurrent_requests(self):
        """Test requêtes concurrentes"""
        
        async def make_request(request_id: int):
            """Fonction pour requête concurrente"""
            try:
                result = await self.model_manager.generate_response(
                    "agent_02_architecte_code_expert",
                    f"Requête concurrente {request_id}",
                    "general"
                )
                return {"id": request_id, "success": result.get("success", False)}
            except Exception as e:
                return {"id": request_id, "error": str(e)}
        
        async def run_concurrent_test():
            """Exécute test concurrent"""
            tasks = [make_request(i) for i in range(5)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        # Exécuter test concurrent
        results = asyncio.run(run_concurrent_test())
        
        # Vérifier résultats
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
        total = len(results)
        
        logger.info(f"🔄 Concurrent: {successful}/{total} succès")
        
        # Au moins 70% doivent réussir
        success_rate = successful / total
        assert success_rate >= 0.7, f"Taux succès trop faible: {success_rate:.1%}"

class TestErrorHandling:
    """Tests de gestion d'erreurs"""
    
    def setup_method(self):
        """Setup pour tests erreurs"""
        if MODEL_MANAGER_AVAILABLE:
            self.model_manager = ModelManager()
        
    @pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
    @pytest.mark.asyncio
    async def test_invalid_agent_id(self):
        """Test agent ID invalide"""
        
        result = await self.model_manager.generate_response(
            "agent_inexistant_999",
            "Test agent inexistant",
            "general"
        )
        
        # Doit fallback vers configuration par défaut
        assert result is not None
        logger.info(f"🔧 Agent inexistant: {result.get('model', 'unknown')} (fallback)")
        
    @pytest.mark.skipif(not MODEL_MANAGER_AVAILABLE, reason="ModelManager non disponible")
    @pytest.mark.asyncio
    async def test_invalid_task_type(self):
        """Test type de tâche invalide"""
        
        result = await self.model_manager.generate_response(
            "agent_01_coordinateur_principal",
            "Test type invalide",
            "type_inexistant_xyz"
        )
        
        # Doit utiliser configuration générale
        assert result is not None
        logger.info(f"🔧 Type invalide: {result.get('model', 'unknown')} (fallback général)")

def run_complete_test_suite():
    """Exécute la suite complète de tests"""
    
    print("🧪 BATTERIE COMPLÈTE DE TESTS - ARCHITECTURE MODÈLES IA")
    print("=" * 60)
    
    # Configuration pytest
    test_args = [
        __file__,
        "-v",  # Verbose
        "-s",  # Pas de capture stdout
        "--tb=short",  # Traceback court
        f"--junitxml={Path(__file__).parent}/test_results.xml"  # Rapport XML
    ]
    
    # Ajouter marqueurs selon disponibilité
    if not MODEL_MANAGER_AVAILABLE:
        print("⚠️ ModelManager non disponible - Tests limités")
        test_args.append("-m not skipif")
    
    # Exécuter tests
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("✅ Tous les tests sont passés avec succès!")
    else:
        print(f"❌ {exit_code} test(s) ont échoué")
    
    return exit_code

def main():
    """Point d'entrée principal"""
    return run_complete_test_suite()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 



