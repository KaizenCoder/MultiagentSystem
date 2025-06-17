#!/usr/bin/env python3
"""
🎮 Monitoring RTX 3090 - SuperWhisper V6
Surveillance en temps réel de votre GPU principal IA.

Configuration: RTX 5060 Ti (Bus 0) + RTX 3090 (Bus 1 - IA Principal)
Focus: RTX 3090 uniquement pour workloads Ollama/PyTorch
"""

import subprocess
import time
import json
import os
import asyncio
import httpx
from datetime import datetime
from typing import Dict, Any, List

# Configuration RTX 3090
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

class RTX3090Monitor:
    """Monitoring spécialisé pour RTX 3090 SuperWhisper V6."""
    
    def __init__(self):
        self.rtx3090_id = 1  # Bus PCI ID
        self.ollama_url = "http://localhost:11434"
        self.monitoring_active = False
        
        # Seuils d'alerte
        self.thresholds = {
            "temperature_warning": 75,
            "temperature_critical": 85,
            "memory_warning": 80,  # % VRAM
            "memory_critical": 95,
            "utilization_low": 10   # % GPU
        }
        
        print("🎮 RTX 3090 Monitor - SuperWhisper V6 initialisé")
    
    def get_rtx3090_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques RTX 3090."""
        
        try:
            # Commande spécifique RTX 3090 (Bus PCI 1)
            result = subprocess.run([
                'nvidia-smi', 
                '--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw,power.limit,fan.speed',
                '--format=csv,noheader,nounits',
                f'--id={self.rtx3090_id}'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                line = result.stdout.strip()
                parts = line.split(', ')
                
                if len(parts) >= 7:
                    name, util, mem_used, mem_total, temp, power_draw, power_limit = parts[:7]
                    fan_speed = parts[7] if len(parts) > 7 else "N/A"
                    
                    mem_used_mb = int(mem_used)
                    mem_total_mb = int(mem_total)
                    mem_percent = (mem_used_mb / mem_total_mb) * 100
                    
                    return {
                        "success": True,
                        "timestamp": datetime.now(),
                        "gpu_name": name,
                        "utilization_percent": int(util),
                        "memory": {
                            "used_mb": mem_used_mb,
                            "total_mb": mem_total_mb,
                            "used_gb": mem_used_mb / 1024,
                            "total_gb": mem_total_mb / 1024,
                            "usage_percent": mem_percent
                        },
                        "temperature_c": int(temp),
                        "power": {
                            "current_w": float(power_draw),
                            "limit_w": float(power_limit),
                            "usage_percent": (float(power_draw) / float(power_limit)) * 100
                        },
                        "fan_speed": fan_speed,
                        "status": self._get_status(int(util), mem_percent, int(temp))
                    }
            
            return {
                "success": False,
                "error": f"nvidia-smi error: {result.stderr}",
                "timestamp": datetime.now()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "nvidia-smi timeout",
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now()
            }
    
    def _get_status(self, utilization: int, memory_percent: float, temperature: int) -> Dict[str, str]:
        """Détermine le statut du GPU."""
        
        status = {
            "overall": "OK",
            "utilization": "Normal",
            "memory": "Normal", 
            "temperature": "Normal",
            "alerts": []
        }
        
        # Vérification température
        if temperature >= self.thresholds["temperature_critical"]:
            status["temperature"] = "CRITICAL"
            status["overall"] = "CRITICAL"
            status["alerts"].append(f"Température critique: {temperature}°C")
        elif temperature >= self.thresholds["temperature_warning"]:
            status["temperature"] = "WARNING"
            if status["overall"] == "OK":
                status["overall"] = "WARNING"
            status["alerts"].append(f"Température élevée: {temperature}°C")
        
        # Vérification mémoire
        if memory_percent >= self.thresholds["memory_critical"]:
            status["memory"] = "CRITICAL"
            status["overall"] = "CRITICAL"
            status["alerts"].append(f"VRAM critique: {memory_percent:.1f}%")
        elif memory_percent >= self.thresholds["memory_warning"]:
            status["memory"] = "WARNING"
            if status["overall"] == "OK":
                status["overall"] = "WARNING"
            status["alerts"].append(f"VRAM élevée: {memory_percent:.1f}%")
        
        # Vérification utilisation
        if utilization < self.thresholds["utilization_low"]:
            status["utilization"] = "LOW"
            status["alerts"].append(f"Utilisation faible: {utilization}%")
        elif utilization > 95:
            status["utilization"] = "HIGH"
        
        return status
    
    async def get_ollama_status(self) -> Dict[str, Any]:
        """Vérifie le statut d'Ollama."""
        
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                # Test connexion
                response = await client.get(f"{self.ollama_url}/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return {
                        "success": True,
                        "running": True,
                        "models_count": len(models),
                        "models": [m["name"] for m in models],
                        "url": self.ollama_url
                    }
                else:
                    return {
                        "success": False,
                        "running": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "running": False,
                "error": str(e)
            }
    
    def display_stats(self, stats: Dict[str, Any], ollama_status: Dict[str, Any]):
        """Affiche les statistiques formatées."""
        
        if not stats["success"]:
            print(f"❌ Erreur GPU: {stats['error']}")
            return
        
        timestamp = stats["timestamp"].strftime("%H:%M:%S")
        status = stats["status"]
        
        # Header avec statut
        status_icon = {
            "OK": "✅",
            "WARNING": "⚠️",
            "CRITICAL": "🚨"
        }.get(status["overall"], "❓")
        
        print(f"\n{status_icon} RTX 3090 Monitor - {timestamp} - {status['overall']}")
        print("=" * 60)
        
        # Informations GPU
        print(f"🎮 GPU: {stats['gpu_name']}")
        print(f"⚡ Utilisation: {stats['utilization_percent']}% ({status['utilization']})")
        
        # Mémoire avec barre visuelle
        mem = stats["memory"]
        mem_bar = self._create_progress_bar(mem["usage_percent"], 40)
        print(f"🧠 VRAM: {mem['used_gb']:.1f}GB / {mem['total_gb']:.1f}GB ({mem['usage_percent']:.1f}%) {status['memory']}")
        print(f"     {mem_bar}")
        
        # Température avec indicateur visuel
        temp_icon = "🟢" if stats["temperature_c"] < 65 else "🟡" if stats["temperature_c"] < 75 else "🔴"
        print(f"🌡️  Température: {stats['temperature_c']}°C {temp_icon} ({status['temperature']})")
        
        # Puissance
        power = stats["power"]
        print(f"⚡ Puissance: {power['current_w']:.1f}W / {power['limit_w']:.1f}W ({power['usage_percent']:.1f}%)")
        
        # Ventilateur
        if stats["fan_speed"] != "N/A":
            print(f"🌪️  Ventilateur: {stats['fan_speed']}%")
        
        # Statut Ollama
        print(f"\n🤖 Ollama: ", end="")
        if ollama_status["success"] and ollama_status["running"]:
            print(f"✅ Actif ({ollama_status['models_count']} modèles)")
            if ollama_status["models_count"] > 0:
                print(f"     Modèles: {', '.join(ollama_status['models'][:3])}{'...' if ollama_status['models_count'] > 3 else ''}")
        else:
            print(f"❌ Inactif ({ollama_status.get('error', 'Inconnu')})")
        
        # Alertes
        if status["alerts"]:
            print(f"\n🚨 Alertes:")
            for alert in status["alerts"]:
                print(f"   • {alert}")
    
    def _create_progress_bar(self, percent: float, width: int = 40) -> str:
        """Crée une barre de progression visuelle."""
        
        filled = int((percent / 100) * width)
        empty = width - filled
        
        if percent < 50:
            bar_char = "🟢"
        elif percent < 80:
            bar_char = "🟡"
        else:
            bar_char = "🔴"
        
        return f"[{bar_char * filled}{'⚪' * empty}] {percent:.1f}%"
    
    async def continuous_monitoring(self, interval: int = 5, max_iterations: int = None):
        """Monitoring continu de la RTX 3090."""
        
        self.monitoring_active = True
        iteration = 0
        
        print(f"🎮 MONITORING RTX 3090 CONTINU (intervalle: {interval}s)")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("=" * 60)
        
        try:
            while self.monitoring_active:
                if max_iterations and iteration >= max_iterations:
                    break
                
                # Récupérer stats
                stats = self.get_rtx3090_stats()
                ollama_status = await self.get_ollama_status()
                
                # Afficher
                self.display_stats(stats, ollama_status)
                
                # Sauvegarde optionnelle
                if stats["success"]:
                    self._save_stats_log(stats, ollama_status)
                
                iteration += 1
                
                # Attendre
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n✅ Monitoring arrêté après {iteration} mesures")
        except Exception as e:
            print(f"\n❌ Erreur monitoring: {e}")
        finally:
            self.monitoring_active = False
    
    def _save_stats_log(self, stats: Dict[str, Any], ollama_status: Dict[str, Any]):
        """Sauvegarde les logs (optionnel)."""
        
        # Créer le dossier logs s'il n'existe pas
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Fichier log du jour
        today = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(logs_dir, f"rtx3090_monitor_{today}.log")
        
        # Entrée log
        log_entry = {
            "timestamp": stats["timestamp"].isoformat(),
            "gpu_utilization": stats["utilization_percent"],
            "memory_usage_percent": stats["memory"]["usage_percent"],
            "temperature": stats["temperature_c"],
            "power_draw": stats["power"]["current_w"],
            "ollama_running": ollama_status.get("running", False),
            "status": stats["status"]["overall"]
        }
        
        # Écrire
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass  # Ignore silencieusement les erreurs de log
    
    async def single_check(self):
        """Vérification unique du statut."""
        
        print("🎮 VÉRIFICATION RTX 3090 - STATUT ACTUEL")
        print("=" * 60)
        
        stats = self.get_rtx3090_stats()
        ollama_status = await self.get_ollama_status()
        
        self.display_stats(stats, ollama_status)
        
        return stats["success"] if stats else False

# ============================================================================
# 🧪 FONCTIONS UTILITAIRES
# ============================================================================

async def benchmark_rtx3090():
    """Benchmark rapide RTX 3090 avec PyTorch."""
    
    print("🧪 BENCHMARK RTX 3090 PYTORCH")
    print("=" * 40)
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA non disponible")
            return False
        
        device = torch.device("cuda:0")  # Après mapping RTX 3090
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"✅ GPU détecté: {gpu_name}")
        print(f"📊 VRAM: {gpu_memory:.1f}GB")
        
        # Test simple
        print("🔄 Test calcul tensoriel...")
        start_time = time.time()
        
        x = torch.randn(1000, 1000, device=device)
        y = torch.randn(1000, 1000, device=device)
        z = torch.matmul(x, y)
        torch.cuda.synchronize()
        
        calc_time = time.time() - start_time
        print(f"✅ Calcul 1000x1000 matmul: {calc_time:.3f}s")
        
        # Nettoyer
        del x, y, z
        torch.cuda.empty_cache()
        
        return True
        
    except ImportError:
        print("❌ PyTorch non installé")
        return False
    except Exception as e:
        print(f"❌ Erreur benchmark: {e}")
        return False

async def test_all_ollama_models():
    """Test rapide de tous vos modèles Ollama."""
    
    models = [
        "nous-hermes-2-mistral-7b-dpo:latest",
        "mixtral-8x7b:latest", 
        "qwen-coder-32b:latest",
        "llama3:8b-instruct-q6_k",
        "qwen2.5-coder:1.5b"
    ]
    
    print("🧪 TEST MODÈLES OLLAMA RTX 3090")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=30) as client:
        for model in models:
            try:
                print(f"🔄 Test {model}...")
                
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": "Hello, test rapide RTX 3090",
                        "stream": False,
                        "options": {"max_tokens": 50}
                    }
                )
                
                if response.status_code == 200:
                    print(f"✅ {model}: OK")
                else:
                    print(f"❌ {model}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {model}: {e}")

# ============================================================================
# 🚀 POINT D'ENTRÉE PRINCIPAL
# ============================================================================

async def main():
    """Menu principal du monitoring RTX 3090."""
    
    monitor = RTX3090Monitor()
    
    print("🎮 RTX 3090 MONITOR - SUPERWHISPER V6")
    print("=" * 50)
    print("1. Vérification unique")
    print("2. Monitoring continu (5s)")
    print("3. Monitoring continu (1s)")
    print("4. Benchmark PyTorch RTX 3090")
    print("5. Test modèles Ollama")
    print("6. Quitter")
    
    while True:
        try:
            choice = input("\n🎯 Votre choix (1-6): ").strip()
            
            if choice == "1":
                await monitor.single_check()
            elif choice == "2":
                await monitor.continuous_monitoring(interval=5)
            elif choice == "3":
                await monitor.continuous_monitoring(interval=1)
            elif choice == "4":
                await benchmark_rtx3090()
            elif choice == "5":
                await test_all_ollama_models()
            elif choice == "6":
                print("👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide, utilisez 1-6")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Programme interrompu")
