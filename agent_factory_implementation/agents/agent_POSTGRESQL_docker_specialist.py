#!/usr/bin/env python3
"""
Agent Docker Specialist - Conteneurisation PostgreSQL
Développé par l'équipe de maintenance NextGeneration
"""

import os
import subprocess
from datetime import datetime

class AgentDockerSpecialist:
    def __init__(self):
    self.nom = "agent_POSTGRESQL_docker_specialist"
    self.version = "1.0.0"
    self.logs = []
        
    def diagnostiquer_docker(self):
        """Diagnostic environnement Docker."""
    diagnostic = {
        "docker_disponible": False,
        "containers_postgresql": [],
        "images_disponibles": []
    }
        
    try:
            # Test Docker disponible
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            diagnostic["docker_disponible"] = True
            diagnostic["version_docker"] = result.stdout.strip()
            self.log("Docker détecté")
                
                # Recherche containers PostgreSQL
            result = subprocess.run(['docker', 'ps', '-a'], 
                                  capture_output=True, text=True)
            if 'postgres' in result.stdout:
                diagnostic["containers_postgresql"].append("Container PostgreSQL détecté")
                    
    except FileNotFoundError:
        diagnostic["erreur"] = "Docker non installé"
        self.log("Docker non disponible")
            
    return diagnostic
        
    def creer_docker_compose(self):
        """Crée configuration Docker Compose PostgreSQL."""
    compose_content = """version: '3.8'
services:
  nextgeneration-postgres:
    image: postgres:15-alpine
    container_name: nextgeneration-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: nextgen_password
      POSTGRES_DB: nextgeneration
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
volumes:
  postgres_data:
"""
        
    try:
        with open("docker-compose.postgresql.yml", "w") as f:
            f.write(compose_content)
        self.log("Docker Compose PostgreSQL créé")
        return True
    except Exception as e:
        self.log(f"Erreur création Docker Compose: {e}")
        return False
            
    def demarrer_postgresql_docker(self):
        """Démarre PostgreSQL via Docker."""
    try:
        cmd = ["docker-compose", "-f", "docker-compose.postgresql.yml", "up", "-d"]
        result = subprocess.run(cmd, capture_output=True, text=True)
            
        if result.returncode == 0:
            self.log("PostgreSQL Docker démarré")
            return True
        else:
            self.log(f"Erreur démarrage: {result.stderr}")
            return False
                
    except Exception as e:
        self.log(f"Erreur Docker: {e}")
        return False
            
    def log(self, message):
    entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    self.logs.append(entry)
    print(f"🐳 {entry}")

def create_agent_docker_specialist():
    return AgentDockerSpecialist()

if __name__ == "__main__":
    agent = create_agent_docker_specialist()
    diagnostic = agent.diagnostiquer_docker()
    agent.creer_docker_compose()
    agent.demarrer_postgresql_docker()
    print(f"Agent Docker Specialist opérationnel - {len(agent.logs)} actions")

