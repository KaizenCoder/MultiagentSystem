#!/usr/bin/env python3
"""
 Agent Docker Specialist
Mission: Diagnostic et rsolution des problmes Docker PostgreSQL
"""

import os
import sys
import subprocess
import json
import logging
import yaml
from datetime import datetime
from pathlib import Path

class DockerSpecialistAgent:
    def __init__(self):
        self.name = "Agent Docker Specialist"
        self.agent_id = "agent_docker_specialist"
        self.version = "1.0.0"
        self.status = "ACTIVE"
        self.workspace = Path(__file__).parent
        self.rapport_file = self.workspace / "rapports" / f"{self.agent_id}_rapport.md"
        
        # Configuration logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.workspace / "logs" / f"{self.agent_id}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.agent_id)
        
    def diagnostic_docker_complet(self):
        """Diagnostic complet de l'environnement Docker pour PostgreSQL"""
        self.logger.info("[SEARCH] Dmarrage diagnostic Docker PostgreSQL")
        
        diagnostic = {
            "timestamp": datetime.now().isoformat(),
            "docker_system": {},
            "containers": {},
            "images": {},
            "volumes": {},
            "networks": {},
            "compose_configs": {},
            "postgresql_specifique": {},
            "problemes_detectes": [],
            "recommandations": []
        }
        
        try:
            # tat gnral Docker
            diagnostic["docker_system"] = self.check_docker_system()
            
            # Containers
            diagnostic["containers"] = self.analyze_containers()
            
            # Images PostgreSQL
            diagnostic["images"] = self.analyze_postgresql_images()
            
            # Volumes PostgreSQL
            diagnostic["volumes"] = self.analyze_volumes()
            
            # Networks
            diagnostic["networks"] = self.analyze_networks()
            
            # Configurations Docker Compose
            diagnostic["compose_configs"] = self.analyze_compose_files()
            
            # Analyse spcifique PostgreSQL
            diagnostic["postgresql_specifique"] = self.analyze_postgresql_containers()
            
            # Analyse des problmes
            self.analyze_docker_problems(diagnostic)
            
        except Exception as e:
            self.logger.error(f"Erreur durant diagnostic Docker: {e}")
            diagnostic["erreur_critique"] = str(e)
            
        return diagnostic
    
    def check_docker_system(self):
        """Vrifie l'tat gnral du systme Docker"""
        docker_system = {
            "docker_installed": False,
            "docker_version": None,
            "docker_compose_version": None,
            "docker_daemon_running": False,
            "docker_info": {},
            "disk_usage": {}
        }
        
        try:
            # Version Docker
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                docker_system["docker_installed"] = True
                docker_system["docker_version"] = result.stdout.strip()
                
                # Test daemon Docker
                result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
                if result.returncode == 0:
                    docker_system["docker_daemon_running"] = True
                    # Parse quelques infos importantes
                    for line in result.stdout.split('\n'):
                        if 'Server Version:' in line:
                            docker_system["docker_info"]["server_version"] = line.split(':')[1].strip()
                        elif 'Storage Driver:' in line:
                            docker_system["docker_info"]["storage_driver"] = line.split(':')[1].strip()
                            
                # Docker Compose
                result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    docker_system["docker_compose_version"] = result.stdout.strip()
                    
                # Utilisation disque
                result = subprocess.run(['docker', 'system', 'df'], capture_output=True, text=True)
                if result.returncode == 0:
                    docker_system["disk_usage"] = result.stdout
                    
        except Exception as e:
            self.logger.warning(f"Erreur vrification systme Docker: {e}")
            
        return docker_system
    
    def analyze_containers(self):
        """Analyse tous les containers Docker"""
        containers_info = {
            "total_containers": 0,
            "running_containers": 0,
            "postgresql_containers": [],
            "all_containers": []
        }
        
        try:
            # Tous les containers
            result = subprocess.run(['docker', 'ps', '-a', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            container = json.loads(line)
                            containers.append(container)
                        except json.JSONDecodeError:
                            continue
                            
                containers_info["all_containers"] = containers
                containers_info["total_containers"] = len(containers)
                
                # Containers actifs
                running = [c for c in containers if c.get('State') == 'running']
                containers_info["running_containers"] = len(running)
                
                # Containers PostgreSQL
                pg_containers = [c for c in containers 
                               if 'postgres' in c.get('Image', '').lower() or 
                                  'postgres' in c.get('Names', '').lower()]
                containers_info["postgresql_containers"] = pg_containers
                
        except Exception as e:
            self.logger.warning(f"Erreur analyse containers: {e}")
            
        return containers_info
    
    def analyze_postgresql_images(self):
        """Analyse les images PostgreSQL disponibles"""
        images_info = {
            "postgresql_images": [],
            "total_images": 0,
            "dangling_images": []
        }
        
        try:
            # Images PostgreSQL
            result = subprocess.run(['docker', 'images', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                images = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            image = json.loads(line)
                            images.append(image)
                            if 'postgres' in image.get('Repository', '').lower():
                                images_info["postgresql_images"].append(image)
                        except json.JSONDecodeError:
                            continue
                            
                images_info["total_images"] = len(images)
                
                # Images orphelines
                dangling = [img for img in images if img.get('Repository') == '<none>']
                images_info["dangling_images"] = dangling
                
        except Exception as e:
            self.logger.warning(f"Erreur analyse images: {e}")
            
        return images_info
    
    def analyze_volumes(self):
        """Analyse les volumes Docker PostgreSQL"""
        volumes_info = {
            "total_volumes": 0,
            "postgresql_volumes": [],
            "dangling_volumes": []
        }
        
        try:
            # Tous les volumes
            result = subprocess.run(['docker', 'volume', 'ls', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                volumes = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            volume = json.loads(line)
                            volumes.append(volume)
                            # Volumes PostgreSQL (par nom)
                            if 'postgres' in volume.get('Name', '').lower():
                                volumes_info["postgresql_volumes"].append(volume)
                        except json.JSONDecodeError:
                            continue
                            
                volumes_info["total_volumes"] = len(volumes)
                
            # Volumes orphelins
            result = subprocess.run(['docker', 'volume', 'ls', '-f', 'dangling=true'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                volumes_info["dangling_volumes"] = result.stdout.split('\n')[1:]
                
        except Exception as e:
            self.logger.warning(f"Erreur analyse volumes: {e}")
            
        return volumes_info
    
    def analyze_networks(self):
        """Analyse les rseaux Docker"""
        networks_info = {
            "total_networks": 0,
            "custom_networks": [],
            "default_networks": []
        }
        
        try:
            result = subprocess.run(['docker', 'network', 'ls', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                networks = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            network = json.loads(line)
                            networks.append(network)
                            
                            # Classification
                            if network.get('Driver') == 'bridge' and network.get('Name') not in ['bridge', 'host', 'none']:
                                networks_info["custom_networks"].append(network)
                            elif network.get('Name') in ['bridge', 'host', 'none']:
                                networks_info["default_networks"].append(network)
                                
                        except json.JSONDecodeError:
                            continue
                            
                networks_info["total_networks"] = len(networks)
                
        except Exception as e:
            self.logger.warning(f"Erreur analyse rseaux: {e}")
            
        return networks_info
    
    def analyze_compose_files(self):
        """Analyse les fichiers Docker Compose du projet"""
        compose_info = {
            "compose_files_found": [],
            "postgresql_configs": [],
            "environment_variables": {},
            "ports_mapping": [],
            "volumes_mapping": []
        }
        
        # Recherche fichiers compose
        project_root = Path(__file__).parent.parent.parent  # Remonte  la racine du projet
        compose_patterns = ['docker-compose*.yml', 'docker-compose*.yaml']
        
        for pattern in compose_patterns:
            for compose_file in project_root.glob(pattern):
                compose_info["compose_files_found"].append(str(compose_file))
                
                try:
                    with open(compose_file, 'r', encoding='utf-8') as f:
                        compose_data = yaml.safe_load(f)
                        
                    # Analyse services PostgreSQL
                    if 'services' in compose_data:
                        for service_name, service_config in compose_data['services'].items():
                            if 'postgres' in service_config.get('image', '').lower():
                                pg_config = {
                                    "file": str(compose_file),
                                    "service_name": service_name,
                                    "image": service_config.get('image'),
                                    "ports": service_config.get('ports', []),
                                    "environment": service_config.get('environment', {}),
                                    "volumes": service_config.get('volumes', []),
                                    "networks": service_config.get('networks', [])
                                }
                                compose_info["postgresql_configs"].append(pg_config)
                                
                                # Extraction des variables d'environnement
                                if isinstance(service_config.get('environment'), dict):
                                    compose_info["environment_variables"].update(
                                        service_config['environment']
                                    )
                                    
                                # Mapping des ports
                                for port in service_config.get('ports', []):
                                    compose_info["ports_mapping"].append({
                                        "service": service_name,
                                        "mapping": port
                                    })
                                    
                                # Mapping des volumes
                                for volume in service_config.get('volumes', []):
                                    compose_info["volumes_mapping"].append({
                                        "service": service_name,
                                        "mapping": volume
                                    })
                                    
                except Exception as e:
                    self.logger.warning(f"Erreur lecture {compose_file}: {e}")
                    
        return compose_info
    
    def analyze_postgresql_containers(self):
        """Analyse spcifique des containers PostgreSQL"""
        pg_analysis = {
            "active_postgresql_containers": [],
            "container_logs": {},
            "container_inspect": {},
            "connectivity_tests": {}
        }
        
        try:
            # Containers PostgreSQL actifs
            result = subprocess.run(['docker', 'ps', '--filter', 'ancestor=postgres', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            container = json.loads(line)
                            pg_analysis["active_postgresql_containers"].append(container)
                            
                            container_id = container.get('ID')
                            
                            # Logs rcents
                            log_result = subprocess.run(['docker', 'logs', '--tail', '20', container_id], 
                                                      capture_output=True, text=True)
                            if log_result.returncode == 0:
                                pg_analysis["container_logs"][container_id] = log_result.stdout
                                
                            # Inspection container
                            inspect_result = subprocess.run(['docker', 'inspect', container_id], 
                                                          capture_output=True, text=True)
                            if inspect_result.returncode == 0:
                                try:
                                    inspect_data = json.loads(inspect_result.stdout)[0]
                                    pg_analysis["container_inspect"][container_id] = {
                                        "status": inspect_data.get('State', {}).get('Status'),
                                        "ip_address": inspect_data.get('NetworkSettings', {}).get('IPAddress'),
                                        "ports": inspect_data.get('NetworkSettings', {}).get('Ports'),
                                        "environment": inspect_data.get('Config', {}).get('Env', [])
                                    }
                                except json.JSONDecodeError:
                                    pass
                                    
                            # Test de connectivit
                            connectivity_result = subprocess.run([
                                'docker', 'exec', container_id, 'pg_isready', '-U', 'postgres'
                            ], capture_output=True, text=True)
                            
                            pg_analysis["connectivity_tests"][container_id] = {
                                "pg_isready": connectivity_result.returncode == 0,
                                "output": connectivity_result.stdout + connectivity_result.stderr
                            }
                            
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            self.logger.warning(f"Erreur analyse containers PostgreSQL: {e}")
            
        return pg_analysis
    
    def analyze_docker_problems(self, diagnostic):
        """Analyse les problmes Docker dtects"""
        problemes = []
        recommandations = []
        
        # Vrification Docker de base
        if not diagnostic["docker_system"]["docker_installed"]:
            problemes.append(" Docker non install")
            recommandations.append("Installer Docker Desktop pour Windows")
            
        if not diagnostic["docker_system"]["docker_daemon_running"]:
            problemes.append(" Docker daemon non actif")
            recommandations.append("Dmarrer Docker Desktop et vrifier le service")
            
        # Analyse containers PostgreSQL
        pg_containers = diagnostic["containers"]["postgresql_containers"]
        if not pg_containers:
            problemes.append(" Aucun container PostgreSQL trouv")
            recommandations.append("Dmarrer les containers PostgreSQL avec docker-compose up")
        else:
            running_pg = [c for c in pg_containers if c.get('State') == 'running']
            if not running_pg:
                problemes.append(" Containers PostgreSQL arrts")
                recommandations.append("Redmarrer containers PostgreSQL")
                
        # Analyse connectivit
        for container_id, connectivity in diagnostic["postgresql_specifique"]["connectivity_tests"].items():
            if not connectivity["pg_isready"]:
                problemes.append(f" Container {container_id[:12]} - PostgreSQL non accessible")
                recommandations.append(f"Vrifier configuration et logs du container {container_id[:12]}")
                
        # Analyse volumes
        if not diagnostic["volumes"]["postgresql_volumes"]:
            problemes.append(" Aucun volume PostgreSQL ddi dtect")
            recommandations.append("Configurer volumes persistants pour donnes PostgreSQL")
            
        # Analyse fichiers compose
        if not diagnostic["compose_configs"]["compose_files_found"]:
            problemes.append(" Aucun fichier docker-compose trouv")
            recommandations.append("Crer configuration docker-compose pour PostgreSQL")
        elif not diagnostic["compose_configs"]["postgresql_configs"]:
            problemes.append(" PostgreSQL non configur dans docker-compose")
            recommandations.append("Ajouter service PostgreSQL dans docker-compose.yml")
            
        # Analyse variables d'environnement
        env_vars = diagnostic["compose_configs"]["environment_variables"]
        required_vars = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
        for var in required_vars:
            if var not in env_vars:
                problemes.append(f" Variable {var} non dfinie dans docker-compose")
                recommandations.append(f"Dfinir {var} dans la configuration docker-compose")
                
        diagnostic["problemes_detectes"] = problemes
        diagnostic["recommandations"] = recommandations
    
    def generer_rapport(self, diagnostic):
        """Gnre le rapport Markdown dtaill"""
        rapport_content = f"""#  Rapport Agent Docker Specialist

**Agent :** {self.name}  
**ID :** {self.agent_id}  
**Version :** {self.version}  
**Date :** {diagnostic['timestamp']}  
**Statut :** {self.status}

---

## [CLIPBOARD] RSUM EXCUTIF

### [TARGET] Mission
Diagnostic complet de l'infrastructure Docker pour PostgreSQL et rsolution des problmes de conteneurisation.

### [CHART] Rsultats Globaux
- **Problmes dtects :** {len(diagnostic.get('problemes_detectes', []))}
- **Recommandations :** {len(diagnostic.get('recommandations', []))}
- **Docker install :** {'[CHECK] Oui' if diagnostic['docker_system'].get('docker_installed') else '[CROSS] Non'}
- **Docker actif :** {'[CHECK] Oui' if diagnostic['docker_system'].get('docker_daemon_running') else '[CROSS] Non'}
- **Containers PostgreSQL :** {len(diagnostic['containers'].get('postgresql_containers', []))}
- **Containers actifs :** {len([c for c in diagnostic['containers'].get('postgresql_containers', []) if c.get('State') == 'running'])}

---

## [SEARCH] DIAGNOSTIC DTAILL

###  Systme Docker
```json
{json.dumps(diagnostic['docker_system'], indent=2, ensure_ascii=False)}
```

###  Containers
```json
{json.dumps(diagnostic['containers'], indent=2, ensure_ascii=False)}
```

###  Images PostgreSQL
```json
{json.dumps(diagnostic['images'], indent=2, ensure_ascii=False)}
```

###  Volumes
```json
{json.dumps(diagnostic['volumes'], indent=2, ensure_ascii=False)}
```

###  Rseaux
```json
{json.dumps(diagnostic['networks'], indent=2, ensure_ascii=False)}
```

###  Configurations Docker Compose
```json
{json.dumps(diagnostic['compose_configs'], indent=2, ensure_ascii=False)}
```

###  Analyse PostgreSQL Spcifique
```json
{json.dumps(diagnostic['postgresql_specifique'], indent=2, ensure_ascii=False)}
```

---

##  PROBLMES IDENTIFIS

"""
        
        for i, probleme in enumerate(diagnostic.get('problemes_detectes', []), 1):
            rapport_content += f"{i}. {probleme}\n"
            
        rapport_content += f"""
---

## [BULB] RECOMMANDATIONS

"""
        
        for i, recommandation in enumerate(diagnostic.get('recommandations', []), 1):
            rapport_content += f"{i}. {recommandation}\n"
            
        rapport_content += f"""
---

## [TOOL] SOLUTIONS DOCKER PROPOSES

### 1. Configuration Docker Compose Optimise
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    container_name: nextgen_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: agent_memory_nextgen
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
```

### 2. Scripts de Gestion Docker
```bash
# Dmarrage propre
docker-compose up -d postgres

# Vrification sant
docker exec nextgen_postgres pg_isready -U postgres

# Logs en temps rel
docker logs -f nextgen_postgres

# Backup volume
docker run --rm -v postgres_data:/data -v $PWD:/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### 3. Troubleshooting Rapide
```bash
# Reset complet (ATTENTION: Supprime donnes)
docker-compose down -v
docker-compose up -d

# Test connectivit
docker exec -it nextgen_postgres psql -U postgres -d agent_memory_nextgen -c "SELECT version();"
```

---

## [TARGET] PLAN D'ACTION DOCKER

### Priorit 1 - Infrastructure de base
- [ ] Valider installation Docker Desktop
- [ ] Configurer docker-compose.yml optimis
- [ ] Crer volumes persistants
- [ ] Tester connectivit PostgreSQL

### Priorit 2 - Configuration avance
- [ ] Optimiser variables d'environnement
- [ ] Configurer healthchecks
- [ ] Mettre en place monitoring
- [ ] Documenter procdures

### Priorit 3 - Production ready
- [ ] Scuriser configuration
- [ ] Automatiser backups
- [ ] Performance tuning
- [ ] Intgration CI/CD

---

##  COORDINATION AGENTS

###  Collaboration Requise
- ** Agent Windows :** Validation environnement hte
- **[TOOL] Agent SQLAlchemy :** Test connexions containers  
- ** Agent Testeur :** Validation infrastructure Docker

###  Donnes Partages
- Configuration Docker Compose valide
- Procdures de dmarrage/arrt
- Scripts de troubleshooting
- Mtriques de performance containers

---

## [CHART] MTRIQUES DOCKER

### [CHECK] Indicateurs de Succs
- Docker daemon oprationnel
- Containers PostgreSQL running
- Connectivit valide
- Volumes persistants configurs

###  Points de Surveillance
- Utilisation ressources containers
- Logs d'erreur PostgreSQL
- Performance rseau
- Espace disque volumes

---

** Infrastructure Docker PostgreSQL analyse et optimise !**

*Rapport gnr automatiquement par {self.name} v{self.version}*
"""
        
        return rapport_content
    
    def executer_mission(self):
        """Excute la mission complte de l'agent Docker"""
        self.logger.info(f"[ROCKET] {self.name} - Dmarrage mission")
        
        try:
            # Diagnostic complet Docker
            diagnostic = self.diagnostic_docker_complet()
            
            # Gnration rapport
            rapport = self.generer_rapport(diagnostic)
            
            # Sauvegarde rapport
            self.rapport_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.rapport_file, 'w', encoding='utf-8') as f:
                f.write(rapport)
                
            self.logger.info(f"[CHECK] Rapport Docker sauvegard: {self.rapport_file}")
            
            # Sauvegarde donnes JSON
            json_file = self.rapport_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(diagnostic, f, indent=2, ensure_ascii=False)
                
            return {
                "statut": "SUCCESS",
                "rapport_file": str(self.rapport_file),
                "diagnostic": diagnostic,
                "problemes_count": len(diagnostic.get('problemes_detectes', [])),
                "recommandations_count": len(diagnostic.get('recommandations', [])),
                "containers_postgresql": len(diagnostic['containers'].get('postgresql_containers', []))
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur mission Docker: {e}")
            return {
                "statut": "ERROR",
                "erreur": str(e)
            }

if __name__ == "__main__":
    agent = DockerSpecialistAgent()
    resultat = agent.executer_mission()
    print(f"Mission Docker termine: {resultat['statut']}")
