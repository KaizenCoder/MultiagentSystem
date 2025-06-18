#!/usr/bin/env python3
"""
🎮 Agents de Validation Ollama RTX3090 - NextGeneration
Système multi-agents pour validation autonome des optimisations RTX3090
"""

import asyncio
import os
import sys
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

# Configuration GPU RTX 3090 obligatoire
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class BaseAgent:
    """Agent de base pour validation RTX3090"""
    
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.start_time = None
        self.end_time = None
        self.status = "initialized"
        self.results = {}
        self.errors = []
    
    async def execute(self) -> Dict[str, Any]:
        """Exécute la mission de l'agent"""
        self.start_time = time.time()
        self.status = "running"
        
        try:
            print(f"🤖 Agent {self.name}: Démarrage mission")
            print(f"📋 Mission: {self.mission}")
            
            # Exécution spécifique à chaque agent
            await self._execute_mission()
            
            self.status = "completed"
            print(f"✅ Agent {self.name}: Mission accomplie")
            
        except Exception as e:
            self.status = "failed"
            self.errors.append(str(e))
            print(f"❌ Agent {self.name}: Échec - {e}")
        
        finally:
            self.end_time = time.time()
            self.results["execution_time"] = self.end_time - self.start_time
            self.results["status"] = self.status
            self.results["errors"] = self.errors
        
        return self.results
    
    async def _execute_mission(self):
        """À implémenter par chaque agent spécialisé"""
        raise NotImplementedError

class SelecteurTestAgent(BaseAgent):
    """Agent pour tester le sélecteur Ollama RTX3090"""
    
    def __init__(self):
        super().__init__(
            name="Testeur Sélecteur",
            mission="Valider le fonctionnement du selecteur_ollama_rtx3090.py"
        )
    
    async def _execute_mission(self):
        """Test du sélecteur RTX3090"""
        
        # Vérifier existence du fichier
        if not Path("selecteur_ollama_rtx3090.py").exists():
            raise FileNotFoundError("selecteur_ollama_rtx3090.py non trouvé")
        
        self.results["file_exists"] = True
        
        # Test import du module
        try:
            sys.path.insert(0, ".")
            import selecteur_ollama_rtx3090
            selector = selecteur_ollama_rtx3090.RTX3090OllamaSelector()
            self.results["import_success"] = True
            self.results["models_configured"] = len(selector.models)
            
            # Test analyse de tâche
            test_tasks = [
                "Écris du code Python pour trier une liste",
                "Analyse complexe de données financières", 
                "Réponse rapide: Quelle heure est-il?",
                "Test simple"
            ]
            
            analyses = []
            for task in test_tasks:
                analysis = selector.analyze_task(task)
                analyses.append({
                    "task": task[:50],
                    "recommended_model": analysis["recommended_model"],
                    "confidence": analysis["confidence"]
                })
            
            self.results["task_analyses"] = analyses
            self.results["analysis_test"] = "success"
            
        except Exception as e:
            self.results["import_success"] = False
            self.results["import_error"] = str(e)

class EnvironmentAgent(BaseAgent):
    """Agent pour configurer les variables d'environnement"""
    
    def __init__(self):
        super().__init__(
            name="Config Environnement", 
            mission="Configurer définitivement les variables d'environnement RTX3090"
        )
    
    async def _execute_mission(self):
        """Configuration variables d'environnement"""
        
        # Variables requises
        required_vars = {
            "CUDA_VISIBLE_DEVICES": "1",
            "CUDA_DEVICE_ORDER": "PCI_BUS_ID", 
            "OLLAMA_MODELS": "D:/modeles_llm",
            "OLLAMA_GPU_DEVICE": "1",
            "OLLAMA_BASE_URL": "http://localhost:11434"
        }
        
        current_config = {}
        missing_vars = []
        
        # Vérifier configuration actuelle
        for var, expected in required_vars.items():
            current = os.environ.get(var, "NOT_SET")
            current_config[var] = current
            
            if current != expected:
                missing_vars.append(f"{var}={expected}")
        
        self.results["current_config"] = current_config
        self.results["required_config"] = required_vars
        self.results["missing_vars"] = missing_vars
        
        # Créer script de configuration
        script_content = f"""@echo off
echo 🎮 Configuration Ollama RTX3090 - NextGeneration
echo Définition variables d'environnement permanentes...

setx CUDA_VISIBLE_DEVICES "1"
setx CUDA_DEVICE_ORDER "PCI_BUS_ID"
setx OLLAMA_MODELS "D:\\modeles_llm"
setx OLLAMA_GPU_DEVICE "1"
setx OLLAMA_BASE_URL "http://localhost:11434"

echo ✅ Variables configurées avec succès
echo ⚠️  Redémarrage nécessaire pour prise en compte
pause
"""
        
        script_path = "config_env_rtx3090.bat"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        self.results["script_created"] = script_path
        self.results["config_status"] = "script_ready"

class OllamaWorkerAgent(BaseAgent):
    """Agent pour développer le OllamaLocalWorker"""
    
    def __init__(self):
        super().__init__(
            name="Développeur Worker",
            mission="Créer et intégrer OllamaLocalWorker dans l'orchestrateur"
        )
    
    async def _execute_mission(self):
        """Développement du worker Ollama"""
        
        # Vérifier structure orchestrateur
        orchestrator_path = Path("orchestrator/app/agents")
        if not orchestrator_path.exists():
            raise FileNotFoundError("Structure orchestrateur non trouvée")
        
        self.results["orchestrator_found"] = True
        
        # Créer le worker Ollama
        worker_code = '''"""
Worker Ollama Local pour modèles RTX3090
"""

import httpx
import os
from typing import Dict, Any, List, Optional
from .workers import BaseWorker

class OllamaLocalWorker(BaseWorker):
    """Worker pour modèles Ollama locaux sur RTX 3090."""
    
    def __init__(self, config):
        super().__init__(config)
        self.ollama_url = getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        
        # Configuration modèles RTX3090
        self.models = {
            "speed": "nous-hermes-2-mistral-7b-dpo:latest",
            "quality": "mixtral-8x7b:latest", 
            "code": "qwen-coder-32b:latest",
            "daily": "llama3:8b-instruct-q6_k",
            "mini": "qwen2.5-coder:1.5b"
        }
    
    async def can_handle_task(self, task: str, requirements: List[str]) -> bool:
        """Gère les tâches locales prioritaires."""
        
        # Priorité modèles locaux
        local_keywords = ["local", "confidential", "private", "offline"]
        if any(keyword in requirements for keyword in local_keywords):
            return True
        
        # Spécialités
        if "code" in task.lower() and "code" in requirements:
            return True
        
        if "fast" in requirements or "quick" in requirements:
            return True
            
        return False
    
    async def process_task(self, task: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Traite avec modèle RTX3090 optimal."""
        
        if requirements is None:
            requirements = []
        
        # Sélection modèle
        if "code" in task.lower():
            model = self.models["code"]
        elif "fast" in requirements:
            model = self.models["speed"]
        elif "complex" in requirements:
            model = self.models["quality"]
        else:
            model = self.models["daily"]
        
        try:
            response = await self._call_ollama(model, task)
            
            return {
                "result": response,
                "model_used": model,
                "agent_type": "ollama_local",
                "gpu": "RTX_3090",
                "privacy": "local_processing",
                "cost": "free"
            }
            
        except Exception as e:
            return {
                "result": f"Erreur Ollama: {str(e)}",
                "success": False,
                "agent_type": "ollama_local"
            }
    
    async def _call_ollama(self, model: str, prompt: str) -> str:
        """Appel API Ollama."""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_gpu": 1
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama error: {response.status_code}")
'''
        
        # Sauvegarder le worker
        worker_path = orchestrator_path / "ollama_worker.py"
        with open(worker_path, 'w', encoding='utf-8') as f:
            f.write(worker_code)
        
        self.results["worker_created"] = str(worker_path)
        self.results["integration_status"] = "file_created"

class MonitoringAgent(BaseAgent):
    """Agent pour validation monitoring RTX3090"""
    
    def __init__(self):
        super().__init__(
            name="Monitoring RTX3090",
            mission="Valider le monitoring continu RTX3090"
        )
    
    async def _execute_mission(self):
        """Validation monitoring"""
        
        # Vérifier existence monitor
        if not Path("monitor_rtx3090.py").exists():
            self.results["monitor_exists"] = False
            self.results["monitor_status"] = "file_missing"
            return
        
        self.results["monitor_exists"] = True
        
        # Test import
        try:
            sys.path.insert(0, ".")
            import monitor_rtx3090
            self.results["monitor_importable"] = True
            
            # Créer script de lancement automatique
            launcher_script = '''@echo off
echo 🎮 Lancement Monitoring RTX3090 - NextGeneration
echo Surveillance continue des performances...

python monitor_rtx3090.py

pause
'''
            
            with open("start_monitor_rtx3090.bat", 'w', encoding='utf-8') as f:
                f.write(launcher_script)
            
            self.results["launcher_created"] = "start_monitor_rtx3090.bat"
            self.results["monitor_status"] = "ready"
            
        except Exception as e:
            self.results["monitor_importable"] = False
            self.results["import_error"] = str(e)

class MixtralOptimizationAgent(BaseAgent):
    """Agent pour optimisation Mixtral Q3_K"""
    
    def __init__(self):
        super().__init__(
            name="Optimiseur Mixtral",
            mission="Tester quantization Q3_K pour Mixtral sur RTX3090"
        )
    
    async def _execute_mission(self):
        """Test optimisation Mixtral"""
        
        # Vérification théorique
        self.results["current_mixtral"] = {
            "model": "mixtral-8x7b:latest",
            "estimated_vram": "26GB",
            "rtx3090_capacity": "24GB",
            "status": "oversized"
        }
        
        # Recommandations
        recommendations = [
            "ollama pull mixtral:8x7b-instruct-v0.1-q3_k_m",
            "ollama pull llama3.1:70b-instruct-q4_k_m", 
            "Test alternatif: qwen2.5:32b-instruct-q4_k_m"
        ]
        
        self.results["optimization_recommendations"] = recommendations
        
        # Créer script de test
        test_script = '''#!/usr/bin/env python3
"""
Test optimisation Mixtral RTX3090
"""

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import asyncio
import httpx

async def test_mixtral_variants():
    """Test différentes variantes Mixtral"""
    
    models_to_test = [
        "mixtral:8x7b-instruct-v0.1-q3_k_m",  # Version optimisée
        "llama3.1:70b-instruct-q4_k_m",       # Alternative qualité
    ]
    
    for model in models_to_test:
        print(f"Test modèle: {model}")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Test disponibilité
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    available = any(model in m["name"] for m in response.json()["models"])
                    print(f"Disponible: {available}")
                    
                    if available:
                        # Test simple
                        payload = {
                            "model": model,
                            "prompt": "Dis bonjour en une phrase",
                            "stream": False
                        }
                        
                        test_response = await client.post(
                            "http://localhost:11434/api/generate",
                            json=payload
                        )
                        
                        if test_response.status_code == 200:
                            print(f"✅ {model}: Fonctionnel")
                        else:
                            print(f"❌ {model}: Erreur {test_response.status_code}")
                    else:
                        print(f"⚠️ {model}: Non installé")
                        
        except Exception as e:
            print(f"❌ {model}: Exception {e}")

if __name__ == "__main__":
    asyncio.run(test_mixtral_variants())
'''
        
        with open("test_mixtral_optimization.py", 'w', encoding='utf-8') as f:
            f.write(test_script)
        
        self.results["test_script_created"] = "test_mixtral_optimization.py"
        self.results["optimization_status"] = "script_ready"

class OrchestrateurAgents:
    """Orchestrateur pour agents RTX3090"""
    
    def __init__(self):
        self.agents = [
            SelecteurTestAgent(),
            EnvironmentAgent(), 
            OllamaWorkerAgent(),
            MonitoringAgent(),
            MixtralOptimizationAgent()
        ]
    
    async def execute_all(self) -> Dict[str, Any]:
        """Exécution parallèle de tous les agents"""
        
        print("🚀 ORCHESTRATEUR RTX3090 - Validation Optimisations")
        print("=" * 60)
        print(f"📊 {len(self.agents)} agents en parallèle")
        print(f"🎮 Configuration GPU: RTX 3090 (Device {os.environ.get('CUDA_VISIBLE_DEVICES')})")
        print()
        
        start_time = time.time()
        
        # Exécution parallèle
        tasks = [agent.execute() for agent in self.agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Compilation rapport
        rapport = {
            "execution_info": {
                "timestamp": datetime.now().isoformat(),
                "total_execution_time": total_time,
                "agents_count": len(self.agents),
                "gpu_config": os.environ.get('CUDA_VISIBLE_DEVICES')
            },
            "agents_results": {},
            "global_status": "success",
            "summary": {
                "completed": 0,
                "failed": 0,
                "total_tasks": len(self.agents)
            }
        }
        
        # Traitement résultats
        for i, (agent, result) in enumerate(zip(self.agents, results)):
            if isinstance(result, Exception):
                rapport["agents_results"][agent.name] = {
                    "status": "exception",
                    "error": str(result)
                }
                rapport["summary"]["failed"] += 1
            else:
                rapport["agents_results"][agent.name] = result
                if result.get("status") == "completed":
                    rapport["summary"]["completed"] += 1
                else:
                    rapport["summary"]["failed"] += 1
        
        # Statut global
        if rapport["summary"]["failed"] > 0:
            rapport["global_status"] = "partial_success"
        
        return rapport

async def main():
    """Point d'entrée principal"""
    
    orchestrateur = OrchestrateurAgents()
    rapport = await orchestrateur.execute_all()
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_file = f"rapport_validation_ollama_rtx3090_{timestamp}.json"
    
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    # Affichage résumé
    print("\n🎯 RAPPORT FINAL - Validation Ollama RTX3090")
    print("=" * 60)
    print(f"⏱️  Temps total: {rapport['execution_info']['total_execution_time']:.1f}s")
    print(f"✅ Agents réussis: {rapport['summary']['completed']}")
    print(f"❌ Agents échoués: {rapport['summary']['failed']}")
    print(f"📄 Rapport détaillé: {rapport_file}")
    print()
    
    # Détail par agent
    for agent_name, result in rapport["agents_results"].items():
        status = result.get("status", "unknown")
        exec_time = result.get("execution_time", 0)
        
        if status == "completed":
            print(f"✅ {agent_name}: Succès ({exec_time:.1f}s)")
        else:
            errors = result.get("errors", [])
            print(f"❌ {agent_name}: Échec - {errors[0] if errors else 'Erreur inconnue'}")
    
    print(f"\n🎮 Validation RTX3090 terminée - Rapport: {rapport_file}")

if __name__ == "__main__":
    asyncio.run(main()) 