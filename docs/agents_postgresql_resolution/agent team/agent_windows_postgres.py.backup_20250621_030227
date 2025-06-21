#!/usr/bin/env python3
"""
 Agent Windows-PostgreSQL Specialist
Mission: Diagnostic et rsolution des problmes PostgreSQL sur Windows
"""

import os
import sys
import subprocess
import json
import logging
from datetime import datetime
from pathlib import Path

class WindowsPostgreSQLAgent:
    def __init__(self):
        self.name = "Agent Windows-PostgreSQL"
        self.agent_id = "agent_windows_postgres"
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
        
    def diagnostic_environnement_windows(self):
        """Diagnostic complet de l'environnement Windows pour PostgreSQL"""
        self.logger.info("[SEARCH] Dmarrage diagnostic environnement Windows")
        
        diagnostic = {
            "timestamp": datetime.now().isoformat(),
            "systeme": {},
            "postgresql": {},
            "python": {},
            "docker": {},
            "variables_env": {},
            "services": {},
            "problemes_detectes": [],
            "recommandations": []
        }
        
        try:
            # Information systme
            diagnostic["systeme"] = self.get_system_info()
            
            # PostgreSQL natif
            diagnostic["postgresql"] = self.check_postgresql_native()
            
            # Python et packages
            diagnostic["python"] = self.check_python_environment()
            
            # Docker
            diagnostic["docker"] = self.check_docker_environment()
            
            # Variables d'environnement
            diagnostic["variables_env"] = self.check_environment_variables()
            
            # Services Windows
            diagnostic["services"] = self.check_windows_services()
            
            # Analyse des problmes
            self.analyze_problems(diagnostic)
            
        except Exception as e:
            self.logger.error(f"Erreur durant diagnostic: {e}")
            diagnostic["erreur_critique"] = str(e)
            
        return diagnostic
    
    def get_system_info(self):
        """Rcupre les informations systme Windows"""
        try:
            system_info = {
                "os": os.name,
                "platform": sys.platform,
                "version": "",
                "architecture": "",
                "user": os.getenv('USERNAME', 'Unknown'),
                "path": os.getenv('PATH', '').split(';')[:10]  # Premiers 10 lments PATH
            }
            
            # Version Windows
            try:
                result = subprocess.run(['ver'], shell=True, capture_output=True, text=True)
                system_info["version"] = result.stdout.strip()
            except:
                system_info["version"] = "Non dterminable"
                
            # Architecture
            try:
                system_info["architecture"] = os.getenv('PROCESSOR_ARCHITECTURE', 'Unknown')
            except:
                pass
                
            return system_info
        except Exception as e:
            self.logger.error(f"Erreur rcupration info systme: {e}")
            return {"erreur": str(e)}
    
    def check_postgresql_native(self):
        """Vrifie PostgreSQL install nativement sur Windows"""
        postgresql_info = {
            "installe": False,
            "version": None,
            "chemin_binaires": None,
            "service_actif": False,
            "port_ecoute": None,
            "pg_isready": False
        }
        
        try:
            # Test pg_isready
            result = subprocess.run(['pg_isready'], capture_output=True, text=True)
            if result.returncode == 0:
                postgresql_info["pg_isready"] = True
                postgresql_info["installe"] = True
            
            # Version PostgreSQL
            try:
                result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    postgresql_info["version"] = result.stdout.strip()
                    postgresql_info["installe"] = True
            except:
                pass
            
            # Recherche dans PATH
            for path_dir in os.getenv('PATH', '').split(';'):
                pg_path = Path(path_dir) / 'pg_isready.exe'
                if pg_path.exists():
                    postgresql_info["chemin_binaires"] = path_dir
                    postgresql_info["installe"] = True
                    break
                    
        except Exception as e:
            self.logger.warning(f"Erreur vrification PostgreSQL natif: {e}")
            
        return postgresql_info
    
    def check_python_environment(self):
        """Vrifie l'environnement Python et packages PostgreSQL"""
        python_info = {
            "version": sys.version,
            "executable": sys.executable,
            "packages_postgresql": {},
            "sqlalchemy_version": None,
            "psycopg2_version": None
        }
        
        # Vrification packages PostgreSQL
        packages_to_check = ['psycopg2', 'psycopg2-binary', 'sqlalchemy', 'alembic']
        
        for package in packages_to_check:
            try:
                result = subprocess.run([sys.executable, '-m', 'pip', 'show', package], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    # Parse version
                    for line in result.stdout.split('\n'):
                        if line.startswith('Version:'):
                            python_info["packages_postgresql"][package] = line.split(':')[1].strip()
                            
                            # Versions spcifiques importantes
                            if package == 'sqlalchemy':
                                python_info["sqlalchemy_version"] = line.split(':')[1].strip()
                            elif package.startswith('psycopg2'):
                                python_info["psycopg2_version"] = line.split(':')[1].strip()
                else:
                    python_info["packages_postgresql"][package] = "NON_INSTALLE"
            except Exception as e:
                python_info["packages_postgresql"][package] = f"ERREUR: {e}"
                
        return python_info
    
    def check_docker_environment(self):
        """Vrifie l'environnement Docker"""
        docker_info = {
            "installe": False,
            "version": None,
            "service_actif": False,
            "containers_postgresql": [],
            "docker_compose": False
        }
        
        try:
            # Version Docker
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                docker_info["installe"] = True
                docker_info["version"] = result.stdout.strip()
                
                # Containers PostgreSQL
                result = subprocess.run(['docker', 'ps', '-a', '--filter', 'ancestor=postgres'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    docker_info["service_actif"] = True
                    docker_info["containers_postgresql"] = result.stdout.split('\n')[1:]
                    
                # Docker Compose
                result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    docker_info["docker_compose"] = True
                    
        except Exception as e:
            self.logger.warning(f"Erreur vrification Docker: {e}")
            
        return docker_info
    
    def check_environment_variables(self):
        """Vrifie les variables d'environnement importantes"""
        important_vars = [
            'PATH', 'PYTHONPATH', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 
            'POSTGRES_DB', 'DATABASE_URL', 'PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT'
        ]
        
        env_vars = {}
        for var in important_vars:
            value = os.getenv(var)
            if value:
                # Masquer les mots de passe
                if 'PASSWORD' in var or 'PASS' in var:
                    env_vars[var] = "***MASKED***"
                else:
                    env_vars[var] = value[:100] + "..." if len(value) > 100 else value
            else:
                env_vars[var] = "NON_DEFINIE"
                
        return env_vars
    
    def check_windows_services(self):
        """Vrifie les services Windows lis  PostgreSQL"""
        services_info = {
            "postgresql_services": [],
            "service_manager_accessible": False
        }
        
        try:
            # Liste des services PostgreSQL
            result = subprocess.run(['sc', 'query', 'type=service', 'state=all'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                services_info["service_manager_accessible"] = True
                
                # Recherche services PostgreSQL
                lines = result.stdout.split('\n')
                for i, line in enumerate(lines):
                    if 'postgresql' in line.lower() or 'postgres' in line.lower():
                        services_info["postgresql_services"].append(lines[i:i+3])
                        
        except Exception as e:
            self.logger.warning(f"Erreur vrification services Windows: {e}")
            
        return services_info
    
    def analyze_problems(self, diagnostic):
        """Analyse les problmes dtects et propose des recommandations"""
        problemes = []
        recommandations = []
        
        # Analyse PostgreSQL
        if not diagnostic["postgresql"]["installe"]:
            problemes.append(" PostgreSQL non install nativement sur Windows")
            recommandations.append("Installer PostgreSQL Windows ou utiliser exclusivement Docker")
            
        if not diagnostic["postgresql"]["pg_isready"]:
            problemes.append(" pg_isready non fonctionnel")
            recommandations.append("Vrifier installation PostgreSQL ou ajouter au PATH")
            
        # Analyse Python
        if diagnostic["python"]["packages_postgresql"].get("psycopg2", "NON_INSTALLE") == "NON_INSTALLE":
            if diagnostic["python"]["packages_postgresql"].get("psycopg2-binary", "NON_INSTALLE") == "NON_INSTALLE":
                problemes.append(" Aucun driver PostgreSQL Python install")
                recommandations.append("Installer psycopg2-binary avec: pip install psycopg2-binary")
                
        # Analyse SQLAlchemy
        sqlalchemy_version = diagnostic["python"]["sqlalchemy_version"]
        if sqlalchemy_version:
            major_version = int(sqlalchemy_version.split('.')[0])
            if major_version >= 2:
                problemes.append(" SQLAlchemy 2.x peut causer des incompatibilits")
                recommandations.append("Considrer downgrade vers SQLAlchemy 1.4.x ou adapter le code")
                
        # Analyse Docker
        if not diagnostic["docker"]["installe"]:
            problemes.append(" Docker non install")
            recommandations.append("Installer Docker Desktop pour Windows")
        elif not diagnostic["docker"]["service_actif"]:
            problemes.append(" Service Docker non actif")
            recommandations.append("Dmarrer Docker Desktop")
            
        # Variables d'environnement
        if diagnostic["variables_env"]["DATABASE_URL"] == "NON_DEFINIE":
            problemes.append(" Variable DATABASE_URL non dfinie")
            recommandations.append("Dfinir DATABASE_URL dans l'environnement")
            
        diagnostic["problemes_detectes"] = problemes
        diagnostic["recommandations"] = recommandations
    
    def generer_rapport(self, diagnostic):
        """Gnre le rapport Markdown dtaill"""
        rapport_content = f"""#  Rapport Agent Windows-PostgreSQL

**Agent :** {self.name}  
**ID :** {self.agent_id}  
**Version :** {self.version}  
**Date :** {diagnostic['timestamp']}  
**Statut :** {self.status}

---

## [CLIPBOARD] RSUM EXCUTIF

### [TARGET] Mission
Diagnostic complet de l'environnement Windows pour PostgreSQL et identification des problmes bloquants.

### [CHART] Rsultats Globaux
- **Problmes dtects :** {len(diagnostic.get('problemes_detectes', []))}
- **Recommandations :** {len(diagnostic.get('recommandations', []))}
- **PostgreSQL natif :** {'[CHECK] Oprationnel' if diagnostic['postgresql'].get('installe') else '[CROSS] Non fonctionnel'}
- **Environment Python :** {'[CHECK] Correct' if diagnostic['python'].get('sqlalchemy_version') else ' Incomplet'}
- **Docker :** {'[CHECK] Actif' if diagnostic['docker'].get('service_actif') else '[CROSS] Problme'}

---

## [SEARCH] DIAGNOSTIC DTAILL

###  Systme Windows
```json
{json.dumps(diagnostic['systeme'], indent=2, ensure_ascii=False)}
```

###  PostgreSQL Natif
```json
{json.dumps(diagnostic['postgresql'], indent=2, ensure_ascii=False)}
```

###  Environnement Python
```json
{json.dumps(diagnostic['python'], indent=2, ensure_ascii=False)}
```

###  Docker
```json
{json.dumps(diagnostic['docker'], indent=2, ensure_ascii=False)}
```

###  Variables d'Environnement
```json
{json.dumps(diagnostic['variables_env'], indent=2, ensure_ascii=False)}
```

###  Services Windows
```json
{json.dumps(diagnostic['services'], indent=2, ensure_ascii=False)}
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

## [TARGET] PLAN D'ACTION PROPOS

### Priorit 1 - Critique
- [ ] Rsoudre problmes PostgreSQL bloquants
- [ ] Corriger configuration Python/SQLAlchemy
- [ ] Valider environnement Docker

### Priorit 2 - Important
- [ ] Optimiser variables d'environnement
- [ ] Documenter configuration finale
- [ ] Mettre en place monitoring

### Priorit 3 - Amlioration
- [ ] Performance tuning
- [ ] Scurisation accs
- [ ] Documentation utilisateur

---

##  COORDINATION AGENTS

###  Collaboration Requise
- ** Agent Docker :** Validation containers PostgreSQL
- **[TOOL] Agent SQLAlchemy :** Rsolution erreurs ORM  
- ** Agent Testeur :** Validation solutions implmentes

###  Donnes Partages
- Diagnostic environnement Windows complet
- Liste problmes prioriss
- Recommandations techniques

---

## [CHART] MTRIQUES

### [CHECK] Succs
- Diagnostic complet ralis
- Problmes identifis et documents
- Plan d'action structur

###  Points d'Attention
- Coordination avec autres agents requise
- Tests validation ncessaires
- Monitoring implmentation

---

**[ROCKET] Prt pour coordination avec quipe d'agents !**

*Rapport gnr automatiquement par {self.name} v{self.version}*
"""
        
        return rapport_content
    
    def executer_mission(self):
        """Excute la mission complte de l'agent"""
        self.logger.info(f"[ROCKET] {self.name} - Dmarrage mission")
        
        try:
            # Diagnostic complet
            diagnostic = self.diagnostic_environnement_windows()
            
            # Gnration rapport
            rapport = self.generer_rapport(diagnostic)
            
            # Sauvegarde rapport
            self.rapport_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.rapport_file, 'w', encoding='utf-8') as f:
                f.write(rapport)
                
            self.logger.info(f"[CHECK] Rapport sauvegard: {self.rapport_file}")
            
            # Sauvegarde donnes JSON
            json_file = self.rapport_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(diagnostic, f, indent=2, ensure_ascii=False)
                
            return {
                "statut": "SUCCESS",
                "rapport_file": str(self.rapport_file),
                "diagnostic": diagnostic,
                "problemes_count": len(diagnostic.get('problemes_detectes', [])),
                "recommandations_count": len(diagnostic.get('recommandations', []))
            }
            
        except Exception as e:
            self.logger.error(f"[CROSS] Erreur mission: {e}")
            return {
                "statut": "ERROR",
                "erreur": str(e)
            }

if __name__ == "__main__":
    agent = WindowsPostgreSQLAgent()
    resultat = agent.executer_mission()
    print(f"Mission termine: {resultat['statut']}")
