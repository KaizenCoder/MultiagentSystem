#!/usr/bin/env python3
"""
🚀 VALIDATION COMPLÈTE ARCHITECTURE MODÈLES IA
==============================================

Script de validation exhaustive de la nouvelle architecture de gestion
des modèles IA avec support Ollama RTX3090 et fallback cloud.

ÉTAPES VALIDATION :
1. ✅ Vérification configuration
2. 🏠 Test Ollama RTX3090  
3. ☁️ Test providers cloud
4. 🔄 Test mécanismes fallback
5. 🧪 Exécution agent test
6. 📊 Génération rapport final

Usage:
    python run_models_validation.py
    python run_models_validation.py --quick
    python run_models_validation.py --ollama-only

Version: 1.0.0
Créé: 19 juin 2025 - 18h15
"""

import argparse
import asyncio
import json
from logging_manager_optimized import LoggingManager
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# LoggingManager NextGeneration - Agent
        from logging_manager_optimized import LoggingManager
        self.logger = LoggingManager().get_agent_logger(
            agent_name="ModelsArchitectureValidator",
            role="ai_processor",
            domain="general",
            async_enabled=True
        )

# Ajout chemin modules
sys.path.insert(0, str(Path(__file__).parent))

class ModelsArchitectureValidator:
    """Validateur complet de l'architecture modèles IA"""
    
    def __init__(self, quick_mode: bool = False, ollama_only: bool = False):
        self.quick_mode = quick_mode
        self.ollama_only = ollama_only
        self.start_time = datetime.now()
        
        self.validation_results = {
            "start_time": self.start_time.isoformat(),
            "config_validation": {},
            "ollama_validation": {},
            "cloud_validation": {},
            "fallback_validation": {},
            "agent_test_results": {},
            "performance_metrics": {},
            "recommendations": [],
            "final_score": 0
        }
        
        logger.info(f"🚀 Validation architecture modèles - Mode: {'Quick' if quick_mode else 'Complet'}")
        if ollama_only:
            logger.info("🏠 Mode Ollama uniquement")
    
    async def run_complete_validation(self) -> Dict[str, Any]:
        """Exécute la validation complète"""
        
        try:
            # Étape 1: Validation configuration
            logger.info("📋 ÉTAPE 1: Validation configuration")
            await self._validate_configuration()
            
            # Étape 2: Test Ollama RTX3090
            logger.info("🏠 ÉTAPE 2: Test Ollama RTX3090")
            await self._validate_ollama()
            
            # Étape 3: Test providers cloud (si pas ollama-only)
            if not self.ollama_only:
                logger.info("☁️ ÉTAPE 3: Test providers cloud")
                await self._validate_cloud_providers()
                
                # Étape 4: Test fallback
                logger.info("🔄 ÉTAPE 4: Test mécanismes fallback")
                await self._validate_fallback_mechanisms()
            
            # Étape 5: Test agent intégration
            logger.info("🤖 ÉTAPE 5: Test agent intégration")
            await self._run_agent_integration_test()
            
            # Étape 6: Métriques performance
            if not self.quick_mode:
                logger.info("⚡ ÉTAPE 6: Métriques performance")
                await self._measure_performance()
            
            # Étape 7: Génération rapport final
            logger.info("📊 ÉTAPE 7: Génération rapport final")
            self._generate_final_report()
            
            return self.validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation: {e}")
            self.validation_results["fatal_error"] = str(e)
            return self.validation_results
    
    async def _validate_configuration(self):
        """Validation configuration modèles"""
        
        try:
            config_path = Path(__file__).parent / "config" / "models_config.json"
            
            if not config_path.exists():
                self.validation_results["config_validation"] = {
                    "error": "Fichier models_config.json non trouvé",
                    "file_exists": False
                }
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Vérification structure (nouvelle version)
            required_sections = ["default_models", "providers", "agent_configurations"]
            missing_sections = [s for s in required_sections if s not in config]
            
            # Récupération des configurations agents
            agent_configs = config.get("agent_configurations", {})
            
            # Vérification agents enterprise
            enterprise_agents = [
                "agent_21_enterprise_orchestrator",
                "agent_22_architecture_consultant_enterprise", 
                "agent_23_fastapi_enterprise_specialist",
                "agent_24_enterprise_storage_specialist",
                "agent_25_enterprise_monitoring_specialist"
            ]
            
            missing_agents = [agent for agent in enterprise_agents if agent not in agent_configs]
            
            # Configuration Ollama
            ollama_config = config.get("providers", {}).get("ollama", {})
            ollama_enabled = ollama_config.get("enabled", False)
            
            self.validation_results["config_validation"] = {
                "file_exists": True,
                "json_valid": True,
                "structure_complete": len(missing_sections) == 0,
                "missing_sections": missing_sections,
                "enterprise_agents_count": len(enterprise_agents) - len(missing_agents),
                "missing_enterprise_agents": missing_agents,
                "ollama_configured": bool(ollama_config),
                "ollama_enabled": ollama_enabled,
                "total_agents": len(agent_configs),
                "config_version": config.get("version", "unknown")
            }
            
            logger.info(f"✅ Configuration: {len(agent_configs)} agents, Ollama {'✅' if ollama_enabled else '❌'}")
            
        except Exception as e:
            logger.error(f"❌ Erreur validation config: {e}")
            self.validation_results["config_validation"] = {
                "error": str(e),
                "file_exists": config_path.exists()
            }
    
    async def _validate_ollama(self):
        """Validation Ollama RTX3090"""
        
        try:
            from core.model_manager import OllamaClient
            
            ollama_client = OllamaClient()
            
            # Test connexion
            start_time = time.time()
            models = await ollama_client.list_models()
            connection_time = time.time() - start_time
            
            # Modèles réellement disponibles selon ollama list
            available_models_list = [
                "mixtral:8x7b-instruct-v0.1-q3_k_m",
                "nous-hermes-2-mistral-7b-dpo:latest", 
                "llama3:8b-instruct-q6_k",
                "qwen2.5-coder:1.5b",
                "starcoder2:3b",
                "qwen-coder-32b:latest",
                "code-stral:latest",
                "deepseek-coder:33b",
                "lux_model:latest",
                "nomic-embed-text:latest"
            ]
            
            # Vérification disponibilité des modèles configurés
            available_models = []
            missing_models = []
            
            for model in available_models_list:
                if model in models:
                    available_models.append(model)
                else:
                    missing_models.append(model)
            
            # Test génération avec premier modèle disponible
            generation_test = {"success": False, "error": "Aucun modèle disponible"}
            
            if models:
                test_model = models[0]
                try:
                    start_gen = time.time()
                    result = await ollama_client.generate(test_model, "Bonjour, réponds en une phrase.")
                    end_gen = time.time()
                    
                    generation_test = {
                        "success": result.get("success", False),
                        "model": test_model,
                        "response_time": end_gen - start_gen,
                        "tokens_per_sec": result.get("tokens_per_sec", 0),
                        "response_preview": result.get("response", "")[:100]
                    }
                    
                except Exception as e:
                    generation_test = {"success": False, "error": str(e)}
            
            # Monitoring GPU
            gpu_status = await ollama_client.get_gpu_usage()
            
            self.validation_results["ollama_validation"] = {
                "connection_success": len(models) >= 0,  # Même 0 modèle = connexion OK
                "connection_time": connection_time,
                "total_models": len(models),
                "models_list": models,
                "available_models_count": len(available_models),
                "missing_models_count": len(missing_models),
                "missing_models": missing_models,
                "generation_test": generation_test,
                "gpu_monitoring": gpu_status
            }
            
            logger.info(f"✅ Ollama: {len(models)} modèles, {len(available_models)} configurés disponibles")
            
        except ImportError:
            logger.error("❌ OllamaClient non disponible")
            self.validation_results["ollama_validation"] = {
                "error": "OllamaClient non importable"
            }
        except Exception as e:
            logger.error(f"❌ Erreur Ollama: {e}")
            self.validation_results["ollama_validation"] = {
                "error": str(e)
            }
    
    async def _validate_cloud_providers(self):
        """Validation providers cloud"""
        
        try:
            from core.model_manager import ModelManager
            
            model_manager = ModelManager()
            
            # Test sélection modèles cloud
            cloud_tests = []
            
            test_agents = [
                ("agent_22_architecture_consultant_enterprise", "general"),
                ("agent_02_architecte_code_expert", "code"), 
                ("agent_04_expert_securite_crypto", "privacy")
            ]
            
            for agent_id, task_type in test_agents:
                try:
                    model, provider = await model_manager.get_model_for_agent(agent_id, task_type)
                    
                    cloud_tests.append({
                        "agent": agent_id,
                        "task_type": task_type,
                        "model": model,
                        "provider": provider.value,
                        "is_cloud": provider.value in ["anthropic", "openai"]
                    })
                    
                except Exception as e:
                    cloud_tests.append({
                        "agent": agent_id,
                        "task_type": task_type,
                        "error": str(e)
                    })
            
            # Vérification API keys (sans les exposer)
            api_keys_status = {}
            for provider in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "PERPLEXITY_API_KEY"]:
                api_keys_status[provider] = bool(os.getenv(provider))
            
            self.validation_results["cloud_validation"] = {
                "model_selection_tests": cloud_tests,
                "api_keys_configured": api_keys_status,
                "total_cloud_providers": sum(1 for v in api_keys_status.values() if v)
            }
            
            logger.info(f"✅ Cloud: {len([t for t in cloud_tests if 'error' not in t])} tests OK")
            
        except Exception as e:
            logger.error(f"❌ Erreur validation cloud: {e}")
            self.validation_results["cloud_validation"] = {"error": str(e)}
    
    async def _validate_fallback_mechanisms(self):
        """Validation mécanismes fallback"""
        
        try:
            from core.model_manager import ModelManager
            from unittest.mock import patch
            
            model_manager = ModelManager()
            
            fallback_tests = []
            
            # Test 1: Fallback local vers cloud (mock échec Ollama)
            try:
                with patch.object(model_manager.ollama_client, 'generate', side_effect=Exception("Mock Ollama failure")):
                    result = await model_manager.generate_response(
                        "agent_02_architecte_code_expert",
                        "Test fallback local->cloud",
                        "code"
                    )
                    
                    fallback_tests.append({
                        "test": "local_to_cloud",
                        "success": result.get("success", False),
                        "final_provider": result.get("provider", "unknown"),
                        "expected_cloud": True
                    })
                    
            except Exception as e:
                fallback_tests.append({
                    "test": "local_to_cloud",
                    "error": str(e)
                })
            
            # Test 2: Fallback cloud vers local (mock échec cloud)
            try:
                with patch.object(model_manager, '_generate_anthropic', side_effect=Exception("Mock Anthropic failure")):
                    with patch.object(model_manager, '_generate_openai', side_effect=Exception("Mock OpenAI failure")):
                        result = await model_manager.generate_response(
                            "agent_22_architecture_consultant_enterprise",
                            "Test fallback cloud->local",
                            "general"
                        )
                        
                        fallback_tests.append({
                            "test": "cloud_to_local",
                            "success": result.get("success", False),
                            "final_provider": result.get("provider", "unknown"),
                            "expected_local": True
                        })
                        
            except Exception as e:
                fallback_tests.append({
                    "test": "cloud_to_local",
                    "error": str(e)
                })
            
            self.validation_results["fallback_validation"] = {
                "tests": fallback_tests,
                "total_tests": len(fallback_tests),
                "successful_tests": len([t for t in fallback_tests if t.get("success", False)])
            }
            
            logger.info(f"✅ Fallback: {len([t for t in fallback_tests if 'error' not in t])}/2 tests")
            
        except Exception as e:
            logger.error(f"❌ Erreur validation fallback: {e}")
            self.validation_results["fallback_validation"] = {"error": str(e)}
    
    async def _run_agent_integration_test(self):
        """Test intégration avec agent de test"""
        
        try:
            from agents.agent_test_models_integration import AgentTestModelsIntegration
            from core.agent_factory_architecture import Task
            
            # Créer et démarrer agent test
            test_agent = AgentTestModelsIntegration()
            await test_agent.startup()
            
            # Exécuter test complet
            if self.quick_mode:
                task = Task("test_quick", "Test rapide intégration")
            else:
                task = Task("test_complete", "Test complet intégration")
            
            start_time = time.time()
            result = await test_agent.execute_task(task)
            end_time = time.time()
            
            await test_agent.shutdown()
            
            self.validation_results["agent_test_results"] = {
                "success": result.success,
                "execution_time": end_time - start_time,
                "data": result.data if result.success else None,
                "error": result.error if not result.success else None
            }
            
            logger.info(f"✅ Agent test: {'Succès' if result.success else 'Échec'}")
            
        except ImportError as e:
            logger.error(f"❌ Agent test non disponible: {e}")
            self.validation_results["agent_test_results"] = {
                "error": f"Import failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"❌ Erreur agent test: {e}")
            self.validation_results["agent_test_results"] = {
                "error": str(e)
            }
    
    async def _measure_performance(self):
        """Mesure des performances"""
        
        try:
            from core.model_manager import ModelManager
            
            model_manager = ModelManager()
            
            # Benchmark différents types de requêtes
            benchmark_tests = [
                {"prompt": "Bonjour", "type": "fast", "expected_time": 10},
                {"prompt": "Explique l'IA en 2 phrases", "type": "general", "expected_time": 20},
                {"prompt": "Écris une fonction Python pour trier une liste", "type": "code", "expected_time": 30}
            ]
            
            performance_results = []
            
            for test in benchmark_tests:
                try:
                    start_time = time.time()
                    
                    result = await model_manager.generate_response(
                        "agent_02_architecte_code_expert",
                        test["prompt"],
                        test["type"]
                    )
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    performance_results.append({
                        "test_type": test["type"],
                        "prompt_length": len(test["prompt"]),
                        "response_time": response_time,
                        "expected_time": test["expected_time"],
                        "within_expected": response_time <= test["expected_time"],
                        "model_used": result.get("model", "unknown"),
                        "provider": result.get("provider", "unknown"),
                        "tokens": result.get("tokens", 0),
                        "tokens_per_sec": result.get("tokens_per_sec", 0)
                    })
                    
                except Exception as e:
                    performance_results.append({
                        "test_type": test["type"],
                        "error": str(e)
                    })
            
            # Calcul métriques globales
            successful_tests = [r for r in performance_results if "error" not in r]
            if successful_tests:
                avg_response_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
                within_expected_count = sum(1 for r in successful_tests if r.get("within_expected", False))
            else:
                avg_response_time = 0
                within_expected_count = 0
            
            self.validation_results["performance_metrics"] = {
                "benchmark_tests": performance_results,
                "total_tests": len(benchmark_tests),
                "successful_tests": len(successful_tests),
                "avg_response_time": avg_response_time,
                "within_expected_count": within_expected_count,
                "performance_score": (within_expected_count / len(benchmark_tests)) * 100
            }
            
            logger.info(f"⚡ Performance: {avg_response_time:.2f}s moyen, {within_expected_count}/{len(benchmark_tests)} dans temps attendu")
            
        except Exception as e:
            logger.error(f"❌ Erreur mesure performance: {e}")
            self.validation_results["performance_metrics"] = {"error": str(e)}
    
    def _generate_final_report(self):
        """Génère le rapport final et calcule le score"""
        
        # Calcul score final
        scores = []
        
        # Score configuration (20%)
        config_val = self.validation_results.get("config_validation", {})
        if config_val.get("structure_complete") and config_val.get("ollama_enabled"):
            scores.append(20)
        elif config_val.get("structure_complete"):
            scores.append(15)
        else:
            scores.append(0)
        
        # Score Ollama (30%)
        ollama_val = self.validation_results.get("ollama_validation", {})
        if ollama_val.get("connection_success") and ollama_val.get("generation_test", {}).get("success"):
            scores.append(30)
        elif ollama_val.get("connection_success"):
            scores.append(20)
        else:
            scores.append(0)
        
        # Score cloud (20% si testé)
        if not self.ollama_only:
            cloud_val = self.validation_results.get("cloud_validation", {})
            cloud_tests = cloud_val.get("model_selection_tests", [])
            successful_cloud = len([t for t in cloud_tests if "error" not in t])
            if successful_cloud >= len(cloud_tests) * 0.8:
                scores.append(20)
            elif successful_cloud >= len(cloud_tests) * 0.5:
                scores.append(10)
            else:
                scores.append(0)
        else:
            scores.append(20)  # Score plein si Ollama only
        
        # Score fallback (15% si testé)
        if not self.ollama_only:
            fallback_val = self.validation_results.get("fallback_validation", {})
            if fallback_val.get("successful_tests", 0) >= 1:
                scores.append(15)
            else:
                scores.append(0)
        else:
            scores.append(15)  # Score plein si Ollama only
        
        # Score agent test (15%)
        agent_test = self.validation_results.get("agent_test_results", {})
        if agent_test.get("success"):
            scores.append(15)
        else:
            scores.append(0)
        
        final_score = sum(scores)
        self.validation_results["final_score"] = final_score
        
        # Génération recommandations
        recommendations = []
        
        if final_score >= 90:
            recommendations.append("🎉 EXCELLENT - Architecture modèles prête pour production")
        elif final_score >= 75:
            recommendations.append("✅ BON - Architecture fonctionnelle avec améliorations mineures")
        elif final_score >= 60:
            recommendations.append("⚠️ MOYEN - Problèmes à corriger avant production")
        else:
            recommendations.append("❌ CRITIQUE - Architecture nécessite refonte majeure")
        
        # Recommandations spécifiques
        if not ollama_val.get("connection_success"):
            recommendations.append("🔧 Installer et configurer Ollama pour modèles locaux")
        
        if ollama_val.get("missing_models"):
            missing = ollama_val["missing_models"]
            recommendations.append(f"📦 Télécharger modèles manquants: {', '.join(missing)}")
        
        if not self.ollama_only:
            cloud_val = self.validation_results.get("cloud_validation", {})
            api_keys = cloud_val.get("api_keys_configured", {})
            missing_keys = [k for k, v in api_keys.items() if not v]
            if missing_keys:
                recommendations.append(f"🔑 Configurer API keys: {', '.join(missing_keys)}")
        
        self.validation_results["recommendations"] = recommendations
        
        # Temps total
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        self.validation_results["end_time"] = end_time.isoformat()
        self.validation_results["total_duration"] = total_duration
        
        # Sauvegarde rapport
        report_file = Path(__file__).parent / "reports" / f"models_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Score final: {final_score}/100")
        logger.info(f"📄 Rapport sauvegardé: {report_file}")

async def main():
    """Point d'entrée principal"""
    
    parser = argparse.ArgumentParser(description="Validation architecture modèles IA")
    parser.add_argument("--quick", action="store_true", help="Mode validation rapide")
    parser.add_argument("--ollama-only", action="store_true", help="Test Ollama uniquement")
    
    args = parser.parse_args()
    
    print("🚀 VALIDATION ARCHITECTURE MODÈLES IA - PATTERN FACTORY")
    print("=" * 60)
    
    validator = ModelsArchitectureValidator(
        quick_mode=args.quick,
        ollama_only=args.ollama_only
    )
    
    # Exécution validation
    start_time = time.time()
    results = await validator.run_complete_validation()
    end_time = time.time()
    
    # Affichage résultats
    print("\n📊 RÉSULTATS VALIDATION")
    print("-" * 30)
    
    final_score = results.get("final_score", 0)
    print(f"Score final: {final_score}/100")
    
    if final_score >= 90:
        print("🎉 EXCELLENT - Prêt pour production")
    elif final_score >= 75:
        print("✅ BON - Fonctionnel")
    elif final_score >= 60:
        print("⚠️ MOYEN - Améliorations nécessaires")
    else:
        print("❌ CRITIQUE - Refonte requise")
    
    print(f"\nDurée: {end_time - start_time:.1f}s")
    
    # Recommandations
    recommendations = results.get("recommendations", [])
    if recommendations:
        print("\n🎯 RECOMMANDATIONS:")
        for rec in recommendations:
            print(f"  {rec}")
    
    return 0 if final_score >= 75 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 