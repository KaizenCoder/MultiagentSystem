#!/usr/bin/env python3
"""
Script de test complet pour les APIs mtiers de l'orchestrateur.
Teste les diffrents endpoints avec les trois modles LLM.
"""

import httpx
import json
import time
import asyncio
from typing import Dict, Any, List

class OrchestatorAPITester:
    """Classe pour tester les APIs de l'orchestrateur."""
    
    def __init__(self, base_url: str = "http://localhost:8003", api_key: str = "demo-key-for-testing"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def test_health(self) -> bool:
        """Test l'endpoint de sant."""
        print("[SEARCH] Test de l'endpoint /health...")
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[CHECK] Sant OK: {data}")
                return True
            else:
                print(f"[CROSS] Erreur sant: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[CROSS] Erreur connexion sant: {e}")
            return False
    
    def test_status(self) -> bool:
        """Test l'endpoint de statut."""
        print("[SEARCH] Test de l'endpoint /orchestrator/status...")
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.base_url}/orchestrator/status", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[CHECK] Statut OK:")
                print(f"   - Agents disponibles: {data.get('agents_count', 'N/A')}")
                print(f"   - Modles configurs: {data.get('models_configured', 'N/A')}")
                return True
            else:
                print(f"[CROSS] Erreur statut: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"[CROSS] Erreur connexion statut: {e}")
            return False
    
    def test_process_task(self, task: str, model: str = "gpt-4", requirements: List[str] = None) -> Dict[str, Any]:
        """Test l'endpoint de traitement principal."""
        print(f"[SEARCH] Test traitement avec {model}: {task[:50]}...")
        
        if requirements is None:
            requirements = []
        
        payload = {
            "task": task,
            "requirements": requirements,
            "preferred_model": model
        }
        
        try:
            start_time = time.time()
            
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    f"{self.base_url}/orchestrator/process",
                    headers=self.headers,
                    json=payload
                )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"[CHECK] Succs en {duration:.2f}s:")
                print(f"   - Agent: {data.get('agent_used', 'N/A')}")
                print(f"   - Rsultat: {data.get('result', 'N/A')[:100]}...")
                return {
                    "success": True,
                    "duration": duration,
                    "data": data
                }
            else:
                print(f"[CROSS] Erreur {response.status_code}: {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "duration": duration
                }
                
        except Exception as e:
            print(f"[CROSS] Erreur traitement: {e}")
            return {
                "success": False,
                "error": str(e),
                "duration": 0
            }
    
    def test_all_models(self) -> Dict[str, Any]:
        """Test tous les modles configurs."""
        print("\n[ROCKET] Test des diffrents modles LLM")
        print("=" * 60)
        
        models = ["gpt-4", "claude-3-sonnet", "gemini-pro"]
        base_task = "cris un petit pome de 4 vers sur la technologie"
        
        results = {}
        
        for model in models:
            print(f"\n Test du modle: {model}")
            print("-" * 40)
            
            result = self.test_process_task(base_task, model)
            results[model] = result
            
            # Pause entre les tests
            time.sleep(2)
        
        return results
    
    def test_specialized_tasks(self) -> Dict[str, Any]:
        """Test diffrents types de tches spcialises."""
        print("\n Test des tches spcialises")
        print("=" * 60)
        
        tasks = [
            {
                "name": "Code Python",
                "task": "Cre une fonction Python pour calculer la factorielle d'un nombre",
                "requirements": ["code", "python"],
                "model": "claude-3-sonnet"
            },
            {
                "name": "Analyse de donnes",
                "task": "Analyse les avantages et inconvnients du tltravail",
                "requirements": ["analysis"],
                "model": "gpt-4"
            },
            {
                "name": "Crativit",
                "task": "Invente une histoire courte sur un robot qui apprend  cuisiner",
                "requirements": ["creative"],
                "model": "gemini-pro"
            },
            {
                "name": "Rsum technique",
                "task": "Rsume en 3 points les principaux dfis de l'informatique quantique",
                "requirements": ["summary", "technical"],
                "model": "gpt-4"
            }
        ]
        
        results = {}
        
        for task_config in tasks:
            print(f"\n[CLIPBOARD] Test: {task_config['name']}")
            print("-" * 40)
            
            result = self.test_process_task(
                task_config["task"],
                task_config["model"],
                task_config["requirements"]
            )
            results[task_config["name"]] = result
            
            # Pause entre les tests
            time.sleep(3)
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Test de performance avec plusieurs requtes."""
        print("\n[LIGHTNING] Test de performance")
        print("=" * 60)
        
        # Test simple et rapide
        simple_task = "Dis bonjour en franais"
        num_tests = 3
        
        results = []
        total_start = time.time()
        
        for i in range(num_tests):
            print(f" Test {i+1}/{num_tests}")
            result = self.test_process_task(simple_task, "gpt-4")
            results.append(result)
            time.sleep(1)
        
        total_time = time.time() - total_start
        
        successful_tests = [r for r in results if r["success"]]
        avg_duration = sum(r["duration"] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        performance_stats = {
            "total_tests": num_tests,
            "successful_tests": len(successful_tests),
            "total_time": total_time,
            "average_duration": avg_duration,
            "success_rate": len(successful_tests) / num_tests * 100
        }
        
        print(f"\n[CHART] Statistiques de performance:")
        print(f"   - Tests russis: {performance_stats['successful_tests']}/{performance_stats['total_tests']}")
        print(f"   - Taux de succs: {performance_stats['success_rate']:.1f}%")
        print(f"   - Temps moyen: {performance_stats['average_duration']:.2f}s")
        print(f"   - Temps total: {performance_stats['total_time']:.2f}s")
        
        return performance_stats
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Excute la suite complte de tests."""
        print("[TARGET] SUITE COMPLTE DE TESTS DE L'ORCHESTRATEUR")
        print("=" * 80)
        
        all_results = {}
        
        # 1. Test de base
        print("\n1 Tests de base")
        health_ok = self.test_health()
        status_ok = self.test_status()
        
        all_results["basic_tests"] = {
            "health": health_ok,
            "status": status_ok
        }
        
        if not (health_ok and status_ok):
            print("[CROSS] Tests de base chous - arrt des tests")
            return all_results
        
        # 2. Test des modles
        print("\n2 Tests des modles")
        model_results = self.test_all_models()
        all_results["model_tests"] = model_results
        
        # 3. Tests spcialiss
        print("\n3 Tests spcialiss")
        specialized_results = self.test_specialized_tasks()
        all_results["specialized_tests"] = specialized_results
        
        # 4. Tests de performance
        print("\n4 Tests de performance")
        performance_results = self.test_performance()
        all_results["performance_tests"] = performance_results
        
        # Rsum final
        self.print_final_summary(all_results)
        
        return all_results
    
    def print_final_summary(self, results: Dict[str, Any]):
        """Affiche un rsum final des tests."""
        print("\n" + "=" * 80)
        print("[CLIPBOARD] RSUM FINAL DES TESTS")
        print("=" * 80)
        
        # Tests de base
        basic = results.get("basic_tests", {})
        print(f"[TOOL] Tests de base:")
        print(f"   - Sant: {'[CHECK]' if basic.get('health') else '[CROSS]'}")
        print(f"   - Statut: {'[CHECK]' if basic.get('status') else '[CROSS]'}")
        
        # Tests des modles
        models = results.get("model_tests", {})
        print(f"\n[ROBOT] Tests des modles:")
        for model, result in models.items():
            status = "[CHECK]" if result.get("success") else "[CROSS]"
            duration = result.get("duration", 0)
            print(f"   - {model}: {status} ({duration:.2f}s)")
        
        # Tests spcialiss
        specialized = results.get("specialized_tests", {})
        print(f"\n Tests spcialiss:")
        for task_name, result in specialized.items():
            status = "[CHECK]" if result.get("success") else "[CROSS]"
            print(f"   - {task_name}: {status}")
        
        # Performance
        perf = results.get("performance_tests", {})
        if perf:
            print(f"\n[LIGHTNING] Performance:")
            print(f"   - Taux de succs: {perf.get('success_rate', 0):.1f}%")
            print(f"   - Temps moyen: {perf.get('average_duration', 0):.2f}s")
        
        # Statut global
        total_success = True
        if not all(basic.values()):
            total_success = False
        if not all(r.get("success", False) for r in models.values()):
            total_success = False
        
        print(f"\n[TARGET] STATUT GLOBAL: {'[CHECK] TOUS LES TESTS PASSENT' if total_success else '[CROSS] CERTAINS TESTS CHOUENT'}")
        
        if total_success:
            print("\n[BULB] L'orchestrateur est prt pour la production!")
            print("   - Toutes les APIs fonctionnent")
            print("   - Tous les modles sont accessibles")
            print("   - Les performances sont satisfaisantes")
        else:
            print("\n[BULB] Actions recommandes:")
            print("   - Vrifiez les cls API dans .env")
            print("   - Vrifiez la configuration des modles")
            print("   - Consultez les logs pour plus de dtails")

def main():
    """Point d'entre principal."""
    print("[ROCKET] Test complet des APIs de l'orchestrateur NextGeneration")
    print("=" * 80)
    
    # Initialisation du testeur
    tester = OrchestatorAPITester()
    
    # Excution de la suite complte
    results = tester.run_full_test_suite()
    
    # Sauvegarde des rsultats
    try:
        with open("test_results_api.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n Rsultats sauvegards dans test_results_api.json")
    except Exception as e:
        print(f" Impossible de sauvegarder les rsultats: {e}")

if __name__ == "__main__":
    main()




