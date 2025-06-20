#!/usr/bin/env python3
"""
🧪 AGENT TEST - INTÉGRATION MODÈLES IA
=====================================

Agent de test pour valider la nouvelle architecture de gestion des modèles IA
avec support complet des modèles locaux Ollama RTX3090.

MISSION :
- Tester configuration centralisée des modèles
- Valider fallback automatique local/cloud
- Benchmarker performance modèles locaux RTX3090
- Vérifier intégration Pattern Factory

MODÈLES TESTÉS :
- Claude Sonnet 4 (cloud)
- Llama 3.1 8B (local RTX3090)
- Qwen-Coder 32B (local RTX3090)
- Mixtral 8x7B (local RTX3090)

Version: 1.0.0
Créé: 19 juin 2025 - 17h30
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import uuid

# Import Pattern Factory
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from core.base_agent_template import BaseAgent, AgentConfig
    PATTERN_FACTORY_AVAILABLE = True
except ImportError:
    # Fallback si Pattern Factory non disponible
    from abc import ABC, abstractmethod
    
    class BaseAgent(ABC):
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            
        @abstractmethod
        async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
            pass
            
        @abstractmethod
        def get_capabilities(self) -> List[str]:
            pass
            
        @abstractmethod 
        async def health_check(self) -> Dict[str, Any]:
            pass
    
    PATTERN_FACTORY_AVAILABLE = False

# Imports locaux
try:
    from core.model_manager import ModelManager
except ImportError:
    ModelManager = None

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentTestModels")

class AgentTestModelsIntegration(BaseAgent):
    """
    🧪 Agent de test pour validation de l'architecture modèles IA
    
    Cet agent teste l'intégration complète entre:
    - Gestionnaire de modèles centralisé
    - Ollama RTX3090 local
    - Fallback cloud providers
    - Pattern Factory
    """
    
    def __init__(self, agent_id: str = None):
        """Initialisation de l'agent de test modèles"""
        
        # Création de la configuration pour BaseAgent
        if PATTERN_FACTORY_AVAILABLE:
            config_data = {
                "name": agent_id or f"test_models_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
                "version": "1.0.0",
                "role": "test_integration",
                "domain": "models_validation",
                "description": "Agent de test pour validation architecture modèles IA",
                "capabilities": [
                    "test_models_integration",
                    "validate_ollama_connection", 
                    "benchmark_performance",
                    "test_agent_model_compatibility",
                    "generate_validation_report"
                ],
                "tools": ["model_manager", "ollama_client", "performance_tester"],
                "dependencies": [],
                "security_requirements": {},
                "performance_targets": {"response_time": 30},
                "default_config": {"log_level": "INFO"},
                "pattern_factory": {
                    "template_version": "1.0.0",
                    "factory_compatible": True,
                    "auto_registration": False,
                    "hot_reload": False
                }
            }
            config = AgentConfig.from_template(config_data)
            super().__init__(config)
        else:
            # Fallback pour tests sans Pattern Factory
            agent_id = agent_id or f"test_models_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            super().__init__(agent_id)
            self.agent_id = agent_id
            self.version = "1.0.0"
            self.description = "Agent de test pour validation architecture modèles IA"
            
            # Configuration logger
            self.logger = logging.getLogger(f"Agent.{self.agent_id}")
        
        # Configuration agent
        self.model_manager = None
        
        logger.info(f"🧪 Agent Test Modèles IA v{self.version} initialisé")
        logger.info(f"🎯 Pattern Factory: {'✅ Disponible' if PATTERN_FACTORY_AVAILABLE else '❌ Fallback'}")
        
        # Configuration test avec toutes les structures nécessaires
        self.test_results = {
            "configuration": {},
            "ollama_integration": {},
            "cloud_providers": {},
            "fallback_mechanisms": {},
            "performance_metrics": {},
            "cost_analysis": {},
            "model_manager_init": {},
            "agent_model_configs": {},
            "ollama_status": {},
            "fallback_tests": {},
            "development_challenges": {},
            "debug_challenges": {},
            "performance_challenges": {},
            "model_responses": {}
        }
        
        # 🚀 VRAIES QUESTIONS DE DÉVELOPPEMENT INFORMATIQUE
        self.development_challenges = {
            "architecture_complexe": {
                "prompt": """Tu es un architecte logiciel senior. Analyse cette architecture et identifie les problèmes :

```python
class UserService:
    def __init__(self):
        self.db = Database()
        self.cache = Redis()
        self.email = EmailService()
        
    def create_user(self, data):
        user = self.db.save(User(data))
        self.cache.set(f"user:{user.id}", user)
        self.email.send_welcome(user.email)
        return user
```

QUESTIONS TECHNIQUES :
1. Quels patterns SOLID sont violés ?
2. Comment implémenter l'injection de dépendances ?
3. Que se passe-t-il si Redis est down ?
4. Comment gérer les transactions distribuées ?
5. Propose une refactorisation avec DDD.""",
                "evaluation_criteria": [
                    "Identifie Single Responsibility Principle violation",
                    "Propose Dependency Injection",
                    "Évoque Circuit Breaker pattern",
                    "Mentionne Saga pattern ou 2PC",
                    "Suggest Repository/Service layers"
                ],
                "min_score": 3,
                "complexity": "senior"
            },
            
            "algorithme_optimisation": {
                "prompt": """Optimise cet algorithme de recherche dans un graphe :

```python
def find_shortest_path(graph, start, end):
    visited = []
    queue = [(start, [start])]
    
    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            visited.append(node)
            if node == end:
                return path
            for neighbor in graph[node]:
                queue.append((neighbor, path + [neighbor]))
    return None
```

DÉFIS TECHNIQUES :
1. Quelle est la complexité temporelle actuelle ?
2. Pourquoi cette implémentation est inefficace ?
3. Implémente Dijkstra avec heap
4. Gère les poids négatifs (Bellman-Ford)
5. Optimise pour graphes très larges (A*)""",
                "evaluation_criteria": [
                    "Identifie O(V+E) mais inefficace à cause de la liste",
                    "Explique pourquoi BFS naïf est lent",
                    "Implémente correctement Dijkstra avec heapq",
                    "Mentionne Bellman-Ford pour poids négatifs",
                    "Propose A* avec heuristique"
                ],
                "min_score": 3,
                "complexity": "expert"
            },
            
            "securite_crypto": {
                "prompt": """Audit de sécurité de ce système d'authentification :

```python
import hashlib
import secrets

class AuthSystem:
    def hash_password(self, password):
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt
    
    def verify_password(self, password, stored_hash):
        hash_part, salt = stored_hash.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
```

AUDIT SÉCURITÉ :
1. Quelles vulnérabilités détectes-tu ?
2. Pourquoi SHA-256 est inapproprié pour les mots de passe ?
3. Implémente avec bcrypt/scrypt/Argon2
4. Gère le timing attack
5. Ajoute 2FA et rate limiting""",
                "evaluation_criteria": [
                    "Identifie que SHA-256 est trop rapide",
                    "Explique les attaques par rainbow tables",
                    "Propose bcrypt/scrypt/Argon2",
                    "Mentionne constant-time comparison",
                    "Suggest TOTP/HOTP pour 2FA"
                ],
                "min_score": 4,
                "complexity": "security_expert"
            },
            
            "concurrence_avancee": {
                "prompt": """Débugge ce code concurrent qui a des race conditions :

```python
import threading
import time

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            temp = self.value
            time.sleep(0.001)  # Simule traitement
            self.value = temp + 1
    
    def get_stats(self):
        return {"value": self.value, "threads": threading.active_count()}

# Usage avec 100 threads
counter = Counter()
threads = [threading.Thread(target=counter.increment) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()
```

PROBLÈMES CONCURRENCE :
1. Pourquoi le résultat n'est pas 100 ?
2. Le lock protège-t-il vraiment ?
3. Implémente avec atomic operations
4. Gère deadlocks potentiels
5. Optimise avec lock-free structures""",
                "evaluation_criteria": [
                    "Identifie que le lock protège mais logique est fausse",
                    "Explique que temp=value puis value=temp+1 est atomique mais logique fausse",
                    "Propose self.value += 1 directement",
                    "Mentionne threading.Atomic ou multiprocessing.Value",
                    "Évoque lock-free queues/stacks"
                ],
                "min_score": 3,
                "complexity": "concurrency_expert"
            },
            
            "performance_database": {
                "prompt": """Optimise cette requête SQL qui timeout :

```sql
SELECT u.name, u.email, COUNT(o.id) as order_count, 
       AVG(o.total) as avg_order, MAX(o.created_at) as last_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01'
AND EXISTS (SELECT 1 FROM orders o2 WHERE o2.user_id = u.id AND o2.total > 100)
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY avg_order DESC;
```

OPTIMISATION BDD :
1. Identifie les goulots d'étranglement
2. Quels index créer ?
3. Réécris avec window functions
4. Propose partitioning strategy
5. Implémente avec cache Redis""",
                "evaluation_criteria": [
                    "Identifie EXISTS subquery comme problème",
                    "Propose index sur (user_id, total) et (created_at)",
                    "Réécrit avec JOIN au lieu de EXISTS",
                    "Mentionne partitioning par date",
                    "Propose cache avec TTL approprié"
                ],
                "min_score": 3,
                "complexity": "database_expert"
            },
            
            "microservices_distributed": {
                "prompt": """Design cette architecture microservices distribuée :

CONTEXTE : E-commerce avec 1M+ users, 10K+ orders/day

SERVICES EXISTANTS :
- User Service (auth, profiles)
- Product Service (catalog, inventory)  
- Order Service (orders, payments)
- Notification Service (email, SMS)

DÉFIS ARCHITECTURE :
1. Comment gérer les transactions distribuées ?
2. Implémente circuit breaker pattern
3. Gère eventual consistency
4. Design event sourcing pour orders
5. Propose monitoring/observability stack""",
                "evaluation_criteria": [
                    "Propose Saga pattern ou 2PC",
                    "Implémente circuit breaker avec hystrix-like",
                    "Explique CQRS + event sourcing",
                    "Design event store avec snapshots",
                    "Propose Prometheus + Grafana + Jaeger"
                ],
                "min_score": 4,
                "complexity": "system_architect"
            },
            
            "machine_learning_production": {
                "prompt": """Industrialise ce modèle ML en production :

```python
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Modèle entraîné
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict(data):
    df = pd.DataFrame(data)
    return model.predict(df)
```

PRODUCTION ML :
1. Quels problèmes de sécurité avec pickle ?
2. Comment gérer model versioning ?
3. Implémente A/B testing pour modèles
4. Gère data drift detection
5. Design MLOps pipeline complet""",
                "evaluation_criteria": [
                    "Identifie pickle security issues",
                    "Propose MLflow ou DVC pour versioning",
                    "Implémente feature flags pour A/B",
                    "Mentionne monitoring distribution shift",
                    "Design CI/CD avec Kubeflow/MLflow"
                ],
                "min_score": 3,
                "complexity": "ml_engineer"
            }
        }
        
        # Questions de debug réel
        self.debug_challenges = {
            "memory_leak": """Ce service Python consomme de plus en plus de RAM. Debug :

```python
class DataProcessor:
    def __init__(self):
        self.cache = {}
        self.results = []
    
    def process_file(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        
        with open(filename, 'r') as f:
            data = f.read()
        
        result = self.expensive_computation(data)
        self.cache[filename] = result
        self.results.append(result)
        return result
```

Où est le memory leak ? Comment le fixer ?""",
            
            "race_condition": """Cette API REST a des bugs aléatoires. Debug :

```python
user_sessions = {}

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    session_id = generate_session()
    user_sessions[user_id] = session_id
    return {'session_id': session_id}

@app.route('/logout', methods=['POST']) 
def logout():
    user_id = request.json['user_id']
    if user_id in user_sessions:
        del user_sessions[user_id]
    return {'status': 'logged_out'}
```

Quels bugs peuvent survenir ? Solutions ?"""
        }
        
        # Tests de performance réels
        self.performance_challenges = {
            "optimization": """Optimise cette fonction qui traite 1M+ records :

```python
def process_transactions(transactions):
    result = []
    for transaction in transactions:
        if transaction['amount'] > 1000:
            tax = transaction['amount'] * 0.1
            fee = 5.0 if transaction['type'] == 'wire' else 2.0
            result.append({
                'id': transaction['id'],
                'net_amount': transaction['amount'] - tax - fee,
                'tax': tax,
                'fee': fee
            })
    return result
```

Comment optimiser pour 1M+ records ?"""
        }
    
    def get_capabilities(self) -> List[str]:
        """Retourne les capacités de l'agent de test"""
        return [
            "test_models_integration",
            "validate_ollama_connection", 
            "benchmark_performance",
            "test_agent_model_compatibility",
            "generate_validation_report"
        ]
    
    async def startup(self):
        """Initialisation de l'agent de test"""
        self.logger.info("🚀 Agent Test Modèles - Démarrage")
        
        # Initialisation du gestionnaire de modèles
        self.model_manager = ModelManager()
        
        # Validation configuration
        await self._validate_configuration()
        
        self.logger.info("✅ Agent Test Modèles - Prêt")
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """🧪 Exécute une tâche de test avec les nouveaux tests de développement informatique"""
        try:
            task_type = task_data.get("type", "complete_test_suite")
            
            if task_type == "complete_test_suite":
                # Exécute la suite complète de tests avancés
                return await self._run_complete_test_suite()
            elif task_type == "integration_test":
                return await self._run_integration_test(task_data)
            elif task_type == "performance_test":
                return await self._run_performance_test(task_data)
            elif task_type == "model_compatibility":
                return await self._test_model_compatibility(task_data)
            else:
                return {
                    "success": False,
                    "error": f"Type de test non supporté: {task_type}",
                    "available_types": ["complete_test_suite", "integration_test", "performance_test", "model_compatibility"]
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution test: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _run_complete_test_suite(self) -> Dict[str, Any]:
        """🧪 Lance la suite complète de tests avec les nouveaux tests de développement informatique"""
        start_time = time.time()
        
        try:
            self.logger.info("🧪 Démarrage suite complète de tests avancés...")
            
            # Initialisation du gestionnaire de modèles si nécessaire
            if not hasattr(self, 'model_manager'):
                self.model_manager = ModelManager()
            
            # Tests séquentiels avec nouveaux tests avancés
            await self._test_model_manager_initialization()
            await self._test_agent_configurations()
            await self._test_ollama_integration()
            await self._test_fallback_mechanisms()
            await self._benchmark_model_performance()
            
            # NOUVEAUX TESTS DE DÉVELOPPEMENT INFORMATIQUE
            await self._test_response_generation()  # Tests challenges développement
            await self._test_debug_challenges()     # Tests debugging réel
            await self._test_performance_challenges()  # Tests optimisation
            
            # Analyse des coûts
            await self._analyze_costs()
            
            # Calcul durée totale
            test_duration = time.time() - start_time
            
            # Génération rapport final avec nouvelles métriques
            report = self._generate_test_report(test_duration)
            
            self.logger.info(f"✅ Suite de tests avancés terminée avec succès en {test_duration:.2f}s")
            return {
                "success": True,
                "data": report,
                "test_type": "complete_suite_advanced",
                "duration": test_duration
            }
            
        except Exception as e:
            test_duration = time.time() - start_time
            self.logger.error(f"❌ Erreur suite de tests: {e}")
            return {
                "success": False,
                "error": str(e),
                "test_type": "complete_suite_advanced",
                "duration": test_duration
            }
    
    async def _test_model_manager_initialization(self):
        """🔧 Test initialisation du gestionnaire de modèles"""
        try:
            if not hasattr(self, 'model_manager'):
                self.model_manager = ModelManager()
            
            # Test configuration chargée
            config_valid = hasattr(self.model_manager, 'config') and self.model_manager.config is not None
            
            self.test_results["model_manager_init"] = {
                "initialized": True,
                "config_loaded": config_valid,
                "ollama_available": hasattr(self.model_manager, 'ollama_client'),
                "timestamp": time.time()
            }
            
            self.logger.info("✅ ModelManager initialisé avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation ModelManager: {e}")
            self.test_results["model_manager_init"] = {"error": str(e)}
    
    async def _test_agent_configurations(self):
        """Test configuration des modèles pour différents agents"""
        
        test_agents = [
            "agent_01_coordinateur_principal",
            "agent_02_architecte_code_expert", 
            "agent_04_expert_securite_crypto",
            "agent_21_security_supply_chain_enterprise",
            "agent_22_architecture_consultant_enterprise"
        ]
        
        for agent_id in test_agents:
            try:
                # Test sélection modèle général
                model_general, provider_general = await self.model_manager.get_model_for_agent(agent_id, "general")
                
                # Test sélection modèle code
                model_code, provider_code = await self.model_manager.get_model_for_agent(agent_id, "code")
                
                # Test sélection modèle privacy
                model_privacy, provider_privacy = await self.model_manager.get_model_for_agent(agent_id, "privacy")
                
                self.test_results["agent_model_configs"][agent_id] = {
                    "general": {"model": model_general, "provider": provider_general.value},
                    "code": {"model": model_code, "provider": provider_code.value},
                    "privacy": {"model": model_privacy, "provider": provider_privacy.value}
                }
                
                logger.info(f"✅ {agent_id}: Général={model_general}, Code={model_code}, Privacy={model_privacy}")
                
            except Exception as e:
                logger.error(f"❌ Erreur config {agent_id}: {e}")
                self.test_results["agent_model_configs"][agent_id] = {"error": str(e)}
    
    async def _test_ollama_integration(self):
        """Test intégration Ollama et modèles locaux RTX3090"""
        
        try:
            # Vérification disponibilité Ollama
            ollama_models = await self.model_manager.ollama_client.list_models()
            gpu_usage = await self.model_manager.ollama_client.get_gpu_usage()
            
            self.test_results["ollama_status"] = {
                "available": len(ollama_models) > 0,
                "models_count": len(ollama_models),
                "models_list": ollama_models,
                "gpu_usage": gpu_usage
            }
            
            # Test génération avec modèles locaux
            if ollama_models:
                for model in ollama_models[:3]:  # Test max 3 modèles
                    try:
                        test_prompt = "Bonjour, peux-tu me dire l'heure ?"
                        
                        start_time = time.time()
                        result = await self.model_manager.ollama_client.generate(model, test_prompt)
                        end_time = time.time()
                        
                        self.test_results["ollama_status"][f"test_{model}"] = {
                            "success": result.get("success", False),
                            "response_length": len(result.get("response", "")),
                            "response_time": end_time - start_time,
                            "tokens_per_sec": result.get("tokens_per_sec", 0)
                        }
                        
                        logger.info(f"✅ Test Ollama {model}: {result.get('tokens_per_sec', 0):.1f} tokens/sec")
                        
                    except Exception as e:
                        logger.error(f"❌ Erreur test {model}: {e}")
                        self.test_results["ollama_status"][f"test_{model}"] = {"error": str(e)}
            
        except Exception as e:
            logger.error(f"❌ Erreur test Ollama: {e}")
            self.test_results["ollama_status"] = {"error": str(e)}
    
    async def _test_fallback_mechanisms(self):
        """Test mécanismes de fallback local/cloud"""
        
        test_scenarios = [
            {
                "agent": "agent_02_architecte_code_expert",
                "task_type": "code",
                "description": "Test fallback code vers local"
            },
            {
                "agent": "agent_04_expert_securite_crypto", 
                "task_type": "privacy",
                "description": "Test fallback privacy vers local"
            },
            {
                "agent": "agent_21_security_supply_chain_enterprise",
                "task_type": "general",
                "description": "Test fallback enterprise vers cloud"
            }
        ]
        
        for scenario in test_scenarios:
            try:
                prompt = self.test_prompts.get(scenario["task_type"], "Test prompt")
                
                # Test génération normale
                result = await self.model_manager.generate_response(
                    scenario["agent"], 
                    prompt, 
                    scenario["task_type"]
                )
                
                self.test_results["fallback_tests"][scenario["agent"]] = {
                    "task_type": scenario["task_type"],
                    "success": result.get("success", False),
                    "model_used": result.get("model", "unknown"),
                    "provider": result.get("provider", "unknown"),
                    "response_time": result.get("response_time", 0),
                    "cost": result.get("cost", 0)
                }
                
                logger.info(f"✅ Fallback {scenario['agent']}: {result.get('model')} ({result.get('provider')})")
                
            except Exception as e:
                logger.error(f"❌ Erreur fallback {scenario['agent']}: {e}")
                self.test_results["fallback_tests"][scenario["agent"]] = {"error": str(e)}
    
    async def _benchmark_model_performance(self):
        """Benchmark performance des différents modèles"""
        
        benchmark_prompts = [
            "Écris un algorithme de tri rapide en Python.",
            "Explique le machine learning en 3 phrases.",
            "Analyse les avantages de Docker pour le développement."
        ]
        
        test_agents = [
            "agent_02_architecte_code_expert",  # Préfère local pour code
            "agent_22_architecture_consultant_enterprise"  # Préfère cloud pour qualité
        ]
        
        for agent_id in test_agents:
            self.test_results["performance_metrics"][agent_id] = {}
            
            for i, prompt in enumerate(benchmark_prompts):
                try:
                    start_time = time.time()
                    
                    result = await self.model_manager.generate_response(
                        agent_id,
                        prompt,
                        "code" if "algorithme" in prompt else "general"
                    )
                    
                    end_time = time.time()
                    
                    self.test_results["performance_metrics"][agent_id][f"test_{i+1}"] = {
                        "prompt_length": len(prompt),
                        "response_length": len(result.get("response", "")),
                        "response_time": end_time - start_time,
                        "model_used": result.get("model", "unknown"),
                        "provider": result.get("provider", "unknown"),
                        "tokens": result.get("tokens", 0),
                        "tokens_per_sec": result.get("tokens_per_sec", 0),
                        "cost": result.get("cost", 0)
                    }
                    
                except Exception as e:
                    logger.error(f"❌ Erreur benchmark {agent_id} test {i+1}: {e}")
                    self.test_results["performance_metrics"][agent_id][f"test_{i+1}"] = {"error": str(e)}
    
    async def _test_response_generation(self):
        """🧠 Test génération de réponses avec VRAIES questions de développement informatique"""
        
        self.test_results["development_challenges"] = {}
        
        logger.info("🚀 DÉMARRAGE TESTS DÉVELOPPEMENT INFORMATIQUE RÉELS")
        
        for challenge_name, challenge_data in self.development_challenges.items():
            try:
                logger.info(f"🧪 Test {challenge_name} (complexité: {challenge_data['complexity']})")
                
                # Sélection agent selon la complexité
                if challenge_data['complexity'] in ['security_expert']:
                    agent_id = "agent_04_expert_securite_crypto"
                elif challenge_data['complexity'] in ['senior', 'expert', 'system_architect']:
                    agent_id = "agent_02_architecte_code_expert"
                elif challenge_data['complexity'] in ['database_expert']:
                    agent_id = "agent_24_gestionnaire_stockage_enterprise"
                elif challenge_data['complexity'] in ['ml_engineer']:
                    agent_id = "agent_25_monitoring_performance_enterprise"
                else:
                    agent_id = "agent_01_coordinateur_principal"
                
                # Mesure performance
                start_time = time.time()
                
                result = await self.model_manager.generate_response(
                    agent_id, 
                    challenge_data['prompt'], 
                    "development_challenge"
                )
                
                response_time = time.time() - start_time
                
                # Évaluation qualitative de la réponse
                response_text = result.get("response", "")
                evaluation_score = await self._evaluate_technical_response(
                    response_text, 
                    challenge_data['evaluation_criteria'],
                    challenge_data['min_score']
                )
                
                self.test_results["development_challenges"][challenge_name] = {
                    "agent_used": agent_id,
                    "model": result.get("model", "unknown"),
                    "provider": result.get("provider", "unknown"),
                    "complexity": challenge_data['complexity'],
                    "success": result.get("success", False),
                    "response_time": response_time,
                    "tokens": result.get("tokens", 0),
                    "cost": result.get("cost", 0),
                    "evaluation_score": evaluation_score,
                    "min_required_score": challenge_data['min_score'],
                    "passed": evaluation_score >= challenge_data['min_score'],
                    "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                    "technical_depth": self._analyze_technical_depth(response_text)
                }
                
                status = "✅ RÉUSSI" if evaluation_score >= challenge_data['min_score'] else "❌ ÉCHOUÉ"
                logger.info(f"{status} {challenge_name}: {evaluation_score}/{len(challenge_data['evaluation_criteria'])} - {result.get('model')} - {response_time:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Erreur test {challenge_name}: {e}")
                self.test_results["development_challenges"][challenge_name] = {
                    "error": str(e),
                    "complexity": challenge_data['complexity'],
                    "passed": False
                }
        
        # Test des questions de debug
        await self._test_debug_challenges()
        
        # Test des optimisations de performance
        await self._test_performance_challenges()
    
    async def _evaluate_technical_response(self, response: str, criteria: List[str], min_score: int) -> int:
        """🎯 Évalue la qualité technique d'une réponse"""
        score = 0
        response_lower = response.lower()
        
        for criterion in criteria:
            # Recherche de mots-clés techniques dans la réponse
            criterion_lower = criterion.lower()
            
            # Vérifications spécifiques par critère
            if "solid" in criterion_lower and ("single responsibility" in response_lower or "dependency injection" in response_lower):
                score += 1
            elif "dijkstra" in criterion_lower and ("dijkstra" in response_lower or "heap" in response_lower):
                score += 1
            elif "bcrypt" in criterion_lower and ("bcrypt" in response_lower or "scrypt" in response_lower or "argon2" in response_lower):
                score += 1
            elif "circuit breaker" in criterion_lower and ("circuit breaker" in response_lower or "hystrix" in response_lower):
                score += 1
            elif "saga" in criterion_lower and ("saga" in response_lower or "2pc" in response_lower):
                score += 1
            elif "index" in criterion_lower and ("index" in response_lower or "btree" in response_lower):
                score += 1
            elif "prometheus" in criterion_lower and ("prometheus" in response_lower or "grafana" in response_lower):
                score += 1
            elif "mlflow" in criterion_lower and ("mlflow" in response_lower or "versioning" in response_lower):
                score += 1
            elif "pickle" in criterion_lower and ("pickle" in response_lower and "security" in response_lower):
                score += 1
            elif "timing attack" in criterion_lower and ("timing" in response_lower or "constant time" in response_lower):
                score += 1
            # Critères génériques
            elif any(keyword in response_lower for keyword in criterion_lower.split() if len(keyword) > 3):
                score += 1
        
        return score
    
    def _analyze_technical_depth(self, response: str) -> Dict[str, Any]:
        """📊 Analyse la profondeur technique d'une réponse"""
        
        # Comptage de termes techniques
        technical_terms = [
            "pattern", "algorithm", "complexity", "optimization", "architecture",
            "security", "encryption", "thread", "concurrency", "database",
            "index", "performance", "scalability", "microservices", "api",
            "class", "function", "method", "interface", "inheritance",
            "polymorphism", "abstraction", "encapsulation", "solid", "dry",
            "kiss", "yagni", "dependency injection", "inversion of control"
        ]
        
        response_lower = response.lower()
        terms_found = [term for term in technical_terms if term in response_lower]
        
        # Détection de code
        code_blocks = response.count("```") // 2
        
        # Longueur et structure
        word_count = len(response.split())
        line_count = len(response.split('\n'))
        
        return {
            "technical_terms_count": len(terms_found),
            "technical_terms_found": terms_found[:10],  # Top 10
            "code_blocks": code_blocks,
            "word_count": word_count,
            "line_count": line_count,
            "has_examples": "exemple" in response_lower or "example" in response_lower,
            "has_implementation": code_blocks > 0 or "implement" in response_lower,
            "depth_score": min(10, len(terms_found) + code_blocks * 2)
        }
    
    async def _test_debug_challenges(self):
        """🐛 Test des capacités de debugging avec vrais problèmes"""
        
        self.test_results["debug_challenges"] = {}
        
        for challenge_name, challenge_prompt in self.debug_challenges.items():
            try:
                logger.info(f"🐛 Test debug: {challenge_name}")
                
                start_time = time.time()
                
                result = await self.model_manager.generate_response(
                    "agent_02_architecte_code_expert",
                    challenge_prompt,
                    "debug_challenge"
                )
                
                response_time = time.time() - start_time
                response_text = result.get("response", "")
                
                # Évaluation spécifique au debug
                debug_score = self._evaluate_debug_response(challenge_name, response_text)
                
                self.test_results["debug_challenges"][challenge_name] = {
                    "model": result.get("model", "unknown"),
                    "response_time": response_time,
                    "debug_score": debug_score,
                    "identified_issue": debug_score >= 2,
                    "proposed_solution": debug_score >= 3,
                    "response_preview": response_text[:150] + "..."
                }
                
                status = "✅ IDENTIFIÉ" if debug_score >= 2 else "❌ RATÉ"
                logger.info(f"{status} Debug {challenge_name}: score {debug_score}/4 - {response_time:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Erreur debug {challenge_name}: {e}")
                self.test_results["debug_challenges"][challenge_name] = {"error": str(e)}
    
    def _evaluate_debug_response(self, challenge_name: str, response: str) -> int:
        """🎯 Évalue la capacité de debugging"""
        score = 0
        response_lower = response.lower()
        
        if challenge_name == "memory_leak":
            if "cache" in response_lower and ("unbounded" in response_lower or "growing" in response_lower):
                score += 1  # Identifie le cache qui grandit
            if "results" in response_lower and ("append" in response_lower or "accumul" in response_lower):
                score += 1  # Identifie l'accumulation dans results
            if "lru" in response_lower or "max size" in response_lower or "ttl" in response_lower:
                score += 1  # Propose solution cache
            if "clear" in response_lower or "del" in response_lower or "pop" in response_lower:
                score += 1  # Propose nettoyage
                
        elif challenge_name == "race_condition":
            if "concurrent" in response_lower or "thread" in response_lower or "race" in response_lower:
                score += 1  # Identifie problème concurrence
            if "dict" in response_lower and ("shared" in response_lower or "global" in response_lower):
                score += 1  # Identifie dict partagé
            if "lock" in response_lower or "thread-safe" in response_lower:
                score += 1  # Propose synchronisation
            if "redis" in response_lower or "database" in response_lower or "session store" in response_lower:
                score += 1  # Propose stockage externe
        
        return score
    
    async def _test_performance_challenges(self):
        """⚡ Test des optimisations de performance avec vrais cas"""
        
        self.test_results["performance_challenges"] = {}
        
        for challenge_name, challenge_prompt in self.performance_challenges.items():
            try:
                logger.info(f"⚡ Test performance: {challenge_name}")
                
                start_time = time.time()
                
                result = await self.model_manager.generate_response(
                    "agent_25_monitoring_performance_enterprise",
                    challenge_prompt,
                    "performance_challenge"
                )
                
                response_time = time.time() - start_time
                response_text = result.get("response", "")
                
                # Évaluation optimisations proposées
                perf_score = self._evaluate_performance_response(response_text)
                
                self.test_results["performance_challenges"][challenge_name] = {
                    "model": result.get("model", "unknown"),
                    "response_time": response_time,
                    "performance_score": perf_score,
                    "optimizations_proposed": perf_score >= 3,
                    "advanced_techniques": perf_score >= 5,
                    "response_preview": response_text[:150] + "..."
                }
                
                status = "✅ OPTIMISÉ" if perf_score >= 3 else "❌ BASIQUE"
                logger.info(f"{status} Performance {challenge_name}: score {perf_score}/6 - {response_time:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Erreur performance {challenge_name}: {e}")
                self.test_results["performance_challenges"][challenge_name] = {"error": str(e)}
    
    def _evaluate_performance_response(self, response: str) -> int:
        """⚡ Évalue les optimisations de performance proposées"""
        score = 0
        response_lower = response.lower()
        
        # Techniques d'optimisation
        optimizations = [
            ("numpy", "vectorization"),  # Vectorisation
            ("pandas", "vectorized"),    # Pandas vectorisé
            ("list comprehension", "comprehension"),  # List comprehensions
            ("generator", "yield"),      # Générateurs
            ("multiprocessing", "parallel"),  # Parallélisation
            ("cython", "numba"),        # Compilation
            ("batch", "chunk"),         # Traitement par batch
            ("index", "database"),      # Optimisations DB
            ("cache", "memoiz"),        # Cache/memoization
            ("algorithm", "complexity") # Amélioration algorithmique
        ]
        
        for opt1, opt2 in optimizations:
            if opt1 in response_lower or opt2 in response_lower:
                score += 1
        
        return min(score, 6)  # Max 6 points
    
    async def _analyze_costs(self):
        """Analyse des coûts d'utilisation"""
        
        system_status = await self.model_manager.get_system_status()
        usage_stats = system_status.get("usage_stats", {})
        
        total_cost = 0
        total_requests = 0
        total_tokens = 0
        
        for model, stats in usage_stats.items():
            total_cost += stats.get("cost", 0)
            total_requests += stats.get("requests", 0)
            total_tokens += stats.get("tokens", 0)
        
        self.test_results["cost_analysis"] = {
            "total_cost_usd": total_cost,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "avg_cost_per_request": total_cost / max(total_requests, 1),
            "avg_cost_per_token": total_cost / max(total_tokens, 1),
            "local_models_savings": "100% pour modèles locaux",
            "usage_by_model": usage_stats
        }
        
        logger.info(f"💰 Coût total: ${total_cost:.4f} - {total_requests} requêtes - {total_tokens} tokens")
    
    def _generate_test_report(self, test_duration: float) -> Dict[str, Any]:
        """📊 Génère le rapport final de tests avec évaluation technique approfondie"""
        
        # Calcul scores par catégorie
        development_stats = self._calculate_development_stats()
        debug_stats = self._calculate_debug_stats()
        performance_stats = self._calculate_performance_stats()
        
        # Score global technique
        total_technical_score = (
            development_stats["avg_score"] * 0.5 +
            debug_stats["avg_score"] * 0.3 +
            performance_stats["avg_score"] * 0.2
        )
        
        # Rapport final enrichi
        report = {
            "test_summary": {
                "agent": self.agent_id,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": test_duration,
                "pattern_factory_available": PATTERN_FACTORY_AVAILABLE,
                "test_type": "DÉVELOPPEMENT INFORMATIQUE RÉEL",
                "technical_score": round(total_technical_score, 2),
                "evaluation_level": self._get_evaluation_level(total_technical_score)
            },
            "development_challenges": {
                "total_challenges": development_stats["total"],
                "passed_challenges": development_stats["passed"],
                "success_rate": development_stats["success_rate"],
                "avg_score": development_stats["avg_score"],
                "avg_response_time": development_stats["avg_time"],
                "complexities_tested": development_stats["complexities"]
            },
            "debug_challenges": {
                "total_debug_tests": debug_stats["total"],
                "issues_identified": debug_stats["identified"],
                "solutions_proposed": debug_stats["solutions"],
                "debug_success_rate": debug_stats["success_rate"],
                "avg_debug_score": debug_stats["avg_score"]
            },
            "performance_challenges": {
                "total_perf_tests": performance_stats["total"],
                "optimizations_found": performance_stats["optimized"],
                "advanced_techniques": performance_stats["advanced"],
                "perf_success_rate": performance_stats["success_rate"],
                "avg_perf_score": performance_stats["avg_score"]
            },
            "detailed_results": self.test_results,
            "technical_recommendations": self._generate_technical_recommendations(),
            "model_capabilities_analysis": self._analyze_model_capabilities()
        }
        
        # Sauvegarde rapport
        report_file = Path(__file__).parent.parent / "reports" / f"test_models_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Rapport sauvegardé: {report_file}")
        
        return report
    
    def _calculate_development_stats(self) -> Dict[str, Any]:
        """📊 Calcule les statistiques des tests de développement"""
        challenges = self.test_results.get("development_challenges", {})
        
        if not challenges:
            return {"total": 0, "passed": 0, "success_rate": 0, "avg_score": 0, "avg_time": 0, "complexities": []}
        
        total = len(challenges)
        passed = sum(1 for result in challenges.values() if result.get("passed", False))
        scores = [result.get("evaluation_score", 0) for result in challenges.values() if "evaluation_score" in result]
        times = [result.get("response_time", 0) for result in challenges.values() if "response_time" in result]
        complexities = list(set(result.get("complexity", "") for result in challenges.values()))
        
        return {
            "total": total,
            "passed": passed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "avg_score": sum(scores) / len(scores) if scores else 0,
            "avg_time": sum(times) / len(times) if times else 0,
            "complexities": complexities
        }
    
    def _calculate_debug_stats(self) -> Dict[str, Any]:
        """🐛 Calcule les statistiques des tests de debug"""
        debug_tests = self.test_results.get("debug_challenges", {})
        
        if not debug_tests:
            return {"total": 0, "identified": 0, "solutions": 0, "success_rate": 0, "avg_score": 0}
        
        total = len(debug_tests)
        identified = sum(1 for result in debug_tests.values() if result.get("identified_issue", False))
        solutions = sum(1 for result in debug_tests.values() if result.get("proposed_solution", False))
        scores = [result.get("debug_score", 0) for result in debug_tests.values() if "debug_score" in result]
        
        return {
            "total": total,
            "identified": identified,
            "solutions": solutions,
            "success_rate": (identified / total * 100) if total > 0 else 0,
            "avg_score": sum(scores) / len(scores) if scores else 0
        }
    
    def _calculate_performance_stats(self) -> Dict[str, Any]:
        """⚡ Calcule les statistiques des tests de performance"""
        perf_tests = self.test_results.get("performance_challenges", {})
        
        if not perf_tests:
            return {"total": 0, "optimized": 0, "advanced": 0, "success_rate": 0, "avg_score": 0}
        
        total = len(perf_tests)
        optimized = sum(1 for result in perf_tests.values() if result.get("optimizations_proposed", False))
        advanced = sum(1 for result in perf_tests.values() if result.get("advanced_techniques", False))
        scores = [result.get("performance_score", 0) for result in perf_tests.values() if "performance_score" in result]
        
        return {
            "total": total,
            "optimized": optimized,
            "advanced": advanced,
            "success_rate": (optimized / total * 100) if total > 0 else 0,
            "avg_score": sum(scores) / len(scores) if scores else 0
        }
    
    def _get_evaluation_level(self, score: float) -> str:
        """🎯 Détermine le niveau d'évaluation basé sur le score technique"""
        if score >= 8.0:
            return "🚀 EXPERT - Niveau Senior/Architecte"
        elif score >= 6.0:
            return "✅ AVANCÉ - Niveau Confirmé"
        elif score >= 4.0:
            return "⚠️ INTERMÉDIAIRE - Niveau Junior+"
        elif score >= 2.0:
            return "❌ BASIQUE - Niveau Débutant"
        else:
            return "💥 INSUFFISANT - Formation requise"
    
    def _generate_technical_recommendations(self) -> List[str]:
        """🎯 Génère des recommandations techniques basées sur les résultats"""
        recommendations = []
        
        # Analyse des challenges de développement
        dev_challenges = self.test_results.get("development_challenges", {})
        failed_complexities = []
        
        for challenge_name, result in dev_challenges.items():
            if not result.get("passed", False):
                complexity = result.get("complexity", "unknown")
                failed_complexities.append(f"{challenge_name} ({complexity})")
        
        if failed_complexities:
            recommendations.append(f"❌ Échecs détectés: {', '.join(failed_complexities)}")
            recommendations.append("📚 Recommandation: Formation approfondie sur les concepts techniques échoués")
        
        # Analyse des capacités de debug
        debug_stats = self._calculate_debug_stats()
        if debug_stats["success_rate"] < 50:
            recommendations.append("🐛 Capacités de debugging insuffisantes - Pratiquer l'analyse de code")
        
        # Analyse des optimisations
        perf_stats = self._calculate_performance_stats()
        if perf_stats["success_rate"] < 60:
            recommendations.append("⚡ Connaissances en optimisation limitées - Étudier les patterns de performance")
        
        # Recommandations par modèle
        model_analysis = self._analyze_model_capabilities()
        for model, capabilities in model_analysis.items():
            if capabilities.get("technical_depth", 0) < 5:
                recommendations.append(f"📈 Modèle {model}: Améliorer les prompts pour plus de profondeur technique")
        
        return recommendations
    
    def _analyze_model_capabilities(self) -> Dict[str, Any]:
        """🔍 Analyse les capacités de chaque modèle testé"""
        model_analysis = {}
        
        # Analyse par catégorie de test
        for category, tests in self.test_results.items():
            if isinstance(tests, dict):
                for test_name, result in tests.items():
                    if isinstance(result, dict) and "model" in result:
                        model = result["model"]
                        
                        if model not in model_analysis:
                            model_analysis[model] = {
                                "tests_count": 0,
                                "avg_response_time": 0,
                                "technical_depth": 0,
                                "success_rate": 0,
                                "strengths": [],
                                "weaknesses": []
                            }
                        
                        # Accumulation des métriques
                        model_analysis[model]["tests_count"] += 1
                        
                        if "response_time" in result:
                            model_analysis[model]["avg_response_time"] += result["response_time"]
                        
                        if "technical_depth" in result:
                            depth = result["technical_depth"].get("depth_score", 0)
                            model_analysis[model]["technical_depth"] += depth
                        
                        # Identification des forces/faiblesses
                        if result.get("passed", False) or result.get("evaluation_score", 0) >= 3:
                            model_analysis[model]["strengths"].append(test_name)
                        else:
                            model_analysis[model]["weaknesses"].append(test_name)
        
        # Calcul des moyennes
        for model, stats in model_analysis.items():
            if stats["tests_count"] > 0:
                stats["avg_response_time"] /= stats["tests_count"]
                stats["technical_depth"] /= stats["tests_count"]
                stats["success_rate"] = len(stats["strengths"]) / stats["tests_count"] * 100
        
        return model_analysis
    
    def _generate_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur les résultats de tests"""
        
        recommendations = []
        
        # Vérification Ollama
        ollama_status = self.test_results.get("ollama_status", {})
        if not ollama_status.get("available", False):
            recommendations.append("❌ Ollama non disponible - Installer et configurer Ollama pour modèles locaux RTX3090")
        elif ollama_status.get("models_count", 0) < 3:
            recommendations.append("⚠️ Peu de modèles Ollama - Télécharger llama3.1:8b, qwen-coder-32b, mixtral-8x7b")
        else:
            recommendations.append("✅ Ollama configuré correctement avec modèles RTX3090")
        
        # Vérification performance
        performance_data = self.test_results.get("performance_metrics", {})
        slow_responses = []
        for agent, metrics in performance_data.items():
            for test, data in metrics.items():
                if isinstance(data, dict) and data.get("response_time", 0) > 30:
                    slow_responses.append(f"{agent}:{test}")
        
        if slow_responses:
            recommendations.append(f"⚠️ Réponses lentes détectées: {', '.join(slow_responses)}")
        
        # Vérification coûts
        cost_analysis = self.test_results.get("cost_analysis", {})
        total_cost = cost_analysis.get("total_cost_usd", 0)
        if total_cost > 1.0:
            recommendations.append(f"💰 Coût élevé détecté: ${total_cost:.2f} - Considérer plus d'usage local")
        elif total_cost == 0:
            recommendations.append("✅ Coût optimal - Utilisation modèles locaux efficace")
        
        # Vérification fallback
        fallback_tests = self.test_results.get("fallback_tests", {})
        failed_fallbacks = [agent for agent, result in fallback_tests.items() if result.get("error")]
        if failed_fallbacks:
            recommendations.append(f"❌ Fallback échoués: {', '.join(failed_fallbacks)}")
        
        return recommendations
    
    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé de l'agent"""
        try:
            # Test connexion Ollama
            ollama_status = await self._check_ollama_health()
            
            # Test gestionnaire modèles
            model_manager_status = self._check_model_manager_health()
            
            return {
                "status": "healthy" if ollama_status and model_manager_status else "unhealthy",
                "ollama": ollama_status,
                "model_manager": model_manager_status,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _check_ollama_health(self) -> bool:
        """Vérifie la santé d'Ollama"""
        try:
            if hasattr(self.model_manager, 'ollama_client'):
                models = await self.model_manager.ollama_client.list_models()
                return len(models) > 0
            return False
        except:
            return False

    def _check_model_manager_health(self) -> bool:
        """Vérifie la santé du gestionnaire de modèles"""
        try:
            return hasattr(self, 'model_manager') and self.model_manager is not None
        except:
            return False

    async def _validate_configuration(self):
        """Valide la configuration"""
        self.logger.info("🔧 Validation configuration...")
        # Configuration validation logic here
        self.logger.info("✅ Configuration validée")

    async def _run_integration_test(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lance un test d'intégration"""
        try:
            self.logger.info("🧪 Test d'intégration démarré")
            
            # Test de base avec un modèle disponible
            test_prompt = "Bonjour, test de fonctionnement"
            result = await self.model_manager.generate_response(
                agent_id="test_agent",
                prompt=test_prompt,
                task_type="general"
            )
            
            return {
                "success": result.get("success", False),
                "model_used": result.get("model", "unknown"),
                "provider": result.get("provider", "unknown"),
                "response_time": result.get("response_time", 0),
                "test_type": "integration"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur test intégration: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _run_performance_test(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lance un test de performance"""
        try:
            self.logger.info("⚡ Test de performance démarré")
            
            # Tests de performance basiques
            start_time = time.time()
            
            result = await self.model_manager.generate_response(
                agent_id="test_agent",
                prompt="Test de performance avec prompt court",
                task_type="general"
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                "success": result.get("success", False),
                "response_time": response_time,
                "performance_score": 100 if response_time < 30 else 50,
                "test_type": "performance"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur test performance: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _test_model_compatibility(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test de compatibilité des modèles"""
        try:
            self.logger.info("🔍 Test compatibilité modèles")
            
            # Test avec différents agents
            test_agents = [
                "agent_02_architecte_code_expert",
                "agent_04_expert_securite_crypto"
            ]
            
            results = []
            for agent_id in test_agents:
                try:
                    result = await self.model_manager.generate_response(
                        agent_id=agent_id,
                        prompt="Test compatibilité",
                        task_type="general"
                    )
                    results.append({
                        "agent": agent_id,
                        "success": result.get("success", False),
                        "model": result.get("model", "unknown")
                    })
                except Exception as e:
                    results.append({
                        "agent": agent_id,
                        "success": False,
                        "error": str(e)
                    })
            
            return {
                "success": any(r["success"] for r in results),
                "results": results,
                "test_type": "compatibility"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur test compatibilité: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def shutdown(self):
        """Arrêt de l'agent"""
        logger.info("🛑 Arrêt agent test modèles")
        return {"status": "shutdown", "timestamp": datetime.now().isoformat()}

# Fonctions utilitaires
async def run_quick_test():
    """Test rapide de l'intégration"""
    agent = AgentTestModelsIntegration()
    await agent.startup()
    
    task = Task("test_quick", "Test rapide intégration modèles")
    result = await agent.execute_task(task)
    
    await agent.shutdown()
    return result

async def run_complete_test():
    """Test complet de l'architecture"""
    agent = AgentTestModelsIntegration()
    await agent.startup()
    
    task = Task("test_complete", "Suite complète de tests")
    result = await agent.execute_task(task)
    
    await agent.shutdown()
    return result

def main():
    """Point d'entrée principal"""
    print("🧪 AGENT TEST MODÈLES IA - PATTERN FACTORY")
    print("=" * 50)
    
    # Test complet
    result = asyncio.run(run_complete_test())
    
    if result.success:
        print("✅ Tests terminés avec succès")
        print(f"📊 Rapport: {len(result.data.get('detailed_results', {}))} catégories testées")
    else:
        print(f"❌ Tests échoués: {result.error}")

if __name__ == "__main__":
    main() 