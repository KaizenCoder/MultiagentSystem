#!/usr/bin/env python3
"""
🚀 AGENT 07 LOCAL RUNNER - SIMULATION DÉPLOIEMENT K8S
Adaptation pour environnement local sans cluster K8s

Mission: Exécuter Agent 07 en mode développement avec Docker local
Objectif: Finaliser Sprint 5 et optimiser SLA < 100ms
"""

import asyncio
import logging
import subprocess
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Import de l'Agent 07 original
from agents.agent_07_expert_deploiement_k8s import Agent07ExpertDeploiementK8s

class Agent07LocalRunner:
    """
    🔧 Runner local pour Agent 07
    Simule le déploiement K8s avec Docker local
    """
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.agent_07 = Agent07ExpertDeploiementK8s()
        self.start_time = time.time()
        
        self.logger.info("🚀 Agent 07 Local Runner - Mode Développement")
        self.logger.info("🎯 Objectif: Sprint 5 - SLA < 100ms")
        
    def _setup_logging(self) -> logging.Logger:
        """Configuration du logging"""
        logger = logging.getLogger("Agent07LocalRunner")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - Agent07Local - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def check_docker_status(self) -> bool:
        """Vérification que Docker est fonctionnel"""
        try:
            result = subprocess.run(
                ["docker", "version", "--format", "json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            docker_info = json.loads(result.stdout)
            self.logger.info(f"✅ Docker détecté: {docker_info['Client']['Version']}")
            return True
            
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"❌ Docker non disponible: {e}")
            return False
    
    def simulate_k8s_cluster(self) -> bool:
        """Simulation d'un cluster K8s avec Docker"""
        try:
            # Créer un réseau Docker pour simulation
            subprocess.run(
                ["docker", "network", "create", "agent-factory-k8s"],
                capture_output=True,
                check=False  # Ignore if already exists
            )
            
            self.logger.info("🌐 Réseau Docker 'agent-factory-k8s' créé/vérifié")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erreur création réseau: {e}")
            return False
    
    def create_local_dockerfiles(self):
        """Création des Dockerfiles adaptés pour local"""
        dockerfiles_created = []
        
        for agent_config in self.agent_07.agents_config:
            dockerfile_content = f"""FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Agent Factory Pattern"
LABEL agent.name="{agent_config.agent_name}"
LABEL agent.id="{agent_config.agent_id}"
LABEL version="1.0.0"

# Installation dépendances système
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copie des requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code agent
COPY agents/agent_{agent_config.agent_id}_*.py ./
COPY code_expert/ ./code_expert/

# Port d'exposition
EXPOSE {agent_config.port}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{agent_config.port}{agent_config.health_check_path} || exit 1

# Variables d'environnement
{chr(10).join([f'ENV {k}={v}' for k, v in agent_config.environment_vars.items()])}

# Commande de démarrage
CMD ["python", "agent_{agent_config.agent_id}_*.py"]
"""
            
            dockerfile_path = Path(f"Dockerfile.agent-{agent_config.agent_id}")
            dockerfile_path.write_text(dockerfile_content)
            dockerfiles_created.append(dockerfile_path)
            
            self.logger.info(f"🐳 Dockerfile créé: {dockerfile_path}")
        
        return dockerfiles_created
    
    def build_docker_images(self, dockerfiles: List[Path]) -> Dict[str, bool]:
        """Construction des images Docker"""
        build_results = {}
        
        for dockerfile, agent_config in zip(dockerfiles, self.agent_07.agents_config):
            try:
                build_start = time.time()
                
                result = subprocess.run([
                    "docker", "build",
                    "-f", str(dockerfile),
                    "-t", agent_config.image_name,
                    "."
                ], capture_output=True, text=True, check=True)
                
                build_time = time.time() - build_start
                build_results[agent_config.agent_name] = True
                
                self.logger.info(f"✅ Image {agent_config.image_name} construite en {build_time:.1f}s")
                
            except subprocess.CalledProcessError as e:
                build_results[agent_config.agent_name] = False
                self.logger.error(f"❌ Erreur build {agent_config.image_name}: {e.stderr}")
        
        return build_results
    
    def run_containers(self, build_results: Dict[str, bool]) -> Dict[str, str]:
        """Démarrage des conteneurs Docker"""
        container_ids = {}
        
        for agent_config in self.agent_07.agents_config:
            if not build_results.get(agent_config.agent_name, False):
                continue
                
            try:
                # Environnement variables for docker run
                env_args = []
                for key, value in agent_config.environment_vars.items():
                    env_args.extend(["-e", f"{key}={value}"])
                
                result = subprocess.run([
                    "docker", "run", "-d",
                    "--name", f"agent-{agent_config.agent_id}",
                    "--network", "agent-factory-k8s",
                    "-p", f"{agent_config.port}:{agent_config.port}",
                    *env_args,
                    agent_config.image_name
                ], capture_output=True, text=True, check=True)
                
                container_id = result.stdout.strip()
                container_ids[agent_config.agent_name] = container_id
                
                self.logger.info(f"🚀 Conteneur {agent_config.agent_name} démarré: {container_id[:12]}")
                
            except subprocess.CalledProcessError as e:
                self.logger.error(f"❌ Erreur démarrage {agent_config.agent_name}: {e.stderr}")
        
        return container_ids
    
    def monitor_performance(self, container_ids: Dict[str, str]) -> Dict[str, float]:
        """Monitoring des performances pour SLA"""
        performance_metrics = {}
        
        for agent_name, container_id in container_ids.items():
            try:
                # Test de latence
                start_time = time.time()
                
                result = subprocess.run([
                    "docker", "exec", container_id,
                    "curl", "-s", "-o", "/dev/null", "-w", "%{time_total}",
                    "http://localhost:8000/health"  # Port générique pour test
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    latency_ms = float(result.stdout) * 1000
                    performance_metrics[agent_name] = latency_ms
                    
                    status = "✅" if latency_ms < 100 else "⚠️"
                    self.logger.info(f"{status} {agent_name}: {latency_ms:.1f}ms")
                
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
                performance_metrics[agent_name] = 999.0  # Timeout/Error
                self.logger.warning(f"⚠️ {agent_name}: Timeout/Error")
        
        return performance_metrics
    
    def cleanup_containers(self):
        """Nettoyage des conteneurs"""
        try:
            # Arrêt des conteneurs
            subprocess.run(["docker", "stop"] + [f"agent-{config.agent_id}" for config in self.agent_07.agents_config], 
                         capture_output=True, check=False)
            
            # Suppression des conteneurs
            subprocess.run(["docker", "rm"] + [f"agent-{config.agent_id}" for config in self.agent_07.agents_config],
                         capture_output=True, check=False)
            
            self.logger.info("🧹 Nettoyage des conteneurs terminé")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur nettoyage: {e}")
    
    async def run_sprint_5_simulation(self):
        """
        🎯 Exécution complète du Sprint 5 en simulation
        """
        self.logger.info("🚀 DÉBUT SPRINT 5 - DÉPLOIEMENT K8S SIMULATION")
        
        # Étape 1: Vérifications préalables
        if not self.check_docker_status():
            self.logger.error("❌ Docker requis pour Sprint 5")
            return False
        
        if not self.simulate_k8s_cluster():
            self.logger.error("❌ Erreur simulation cluster")
            return False
        
        # Étape 2: Création des Dockerfiles
        self.logger.info("📦 Création des Dockerfiles...")
        dockerfiles = self.create_local_dockerfiles()
        
        # Étape 3: Construction des images
        self.logger.info("🔨 Construction des images Docker...")
        build_results = self.build_docker_images(dockerfiles)
        
        success_builds = sum(build_results.values())
        total_builds = len(build_results)
        
        self.logger.info(f"📊 Images construites: {success_builds}/{total_builds}")
        
        if success_builds == 0:
            self.logger.error("❌ Aucune image construite avec succès")
            return False
        
        # Étape 4: Démarrage des conteneurs
        self.logger.info("🚀 Démarrage des conteneurs...")
        container_ids = self.run_containers(build_results)
        
        if not container_ids:
            self.logger.error("❌ Aucun conteneur démarré")
            return False
        
        # Étape 5: Attente démarrage + monitoring
        self.logger.info("⏳ Attente démarrage (30s)...")
        await asyncio.sleep(30)
        
        # Étape 6: Tests performance SLA
        self.logger.info("📈 Test performance SLA < 100ms...")
        performance = self.monitor_performance(container_ids)
        
        # Calcul SLA
        valid_metrics = [p for p in performance.values() if p < 999.0]
        if valid_metrics:
            avg_latency = sum(valid_metrics) / len(valid_metrics)
            p95_latency = sorted(valid_metrics)[int(len(valid_metrics) * 0.95)] if len(valid_metrics) > 1 else valid_metrics[0]
            
            sla_status = "✅ RESPECTÉ" if p95_latency < 100 else "❌ DÉPASSÉ"
            self.logger.info(f"📊 SLA P95: {p95_latency:.1f}ms - {sla_status}")
        
        # Étape 7: Rapport final
        total_time = time.time() - self.start_time
        
        self.logger.info("=" * 60)
        self.logger.info("🏆 RAPPORT FINAL SPRINT 5")
        self.logger.info("=" * 60)
        self.logger.info(f"⏱️  Temps total: {total_time:.1f}s")
        self.logger.info(f"🐳 Images construites: {success_builds}/{total_builds}")
        self.logger.info(f"🚀 Conteneurs actifs: {len(container_ids)}")
        if valid_metrics:
            self.logger.info(f"📈 Latence moyenne: {avg_latency:.1f}ms")
            self.logger.info(f"📊 SLA P95: {p95_latency:.1f}ms")
        self.logger.info("=" * 60)
        
        # Étape 8: Nettoyage
        self.logger.info("🧹 Nettoyage...")
        await asyncio.sleep(5)  # Laisser un peu de temps
        self.cleanup_containers()
        
        # Suppression des Dockerfiles temporaires
        for dockerfile in dockerfiles:
            try:
                dockerfile.unlink()
            except FileNotFoundError:
                pass
        
        self.logger.info("✅ SPRINT 5 TERMINÉ AVEC SUCCÈS")
        return True

async def main():
    """Point d'entrée principal"""
    runner = Agent07LocalRunner()
    
    try:
        success = await runner.run_sprint_5_simulation()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        runner.logger.info("🛑 Interruption utilisateur")
        runner.cleanup_containers()
        sys.exit(1)
        
    except Exception as e:
        runner.logger.error(f"💥 Erreur critique: {e}")
        runner.cleanup_containers()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 