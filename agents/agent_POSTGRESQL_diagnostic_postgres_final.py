#!/usr/bin/env python3
"""
Agent Diagnostic PostgreSQL - Spcialis rsolution encodage
Mission: Diagnostiquer et rsoudre dfinitivement le problme d'encodage UTF-8
"""

import subprocess
import json
import os
import sys
import time
from pathlib import Path
from core import logging_manager
from datetime import datetime
import logging

class AgentDiagnosticPostgreSQL:
    """Agent spcialis diagnostic et rsolution PostgreSQL encodage"""
    
    def __init__(self, workspace_root: Path = None):
        self.name = "Agent Diagnostic PostgreSQL"
        self.version = "2.0.0"
        self.mission = "Rsolution dfinitive encodage PostgreSQL"
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        
        # Configuration logging
        self.logger = self._setup_logging()
        
        self.rapport_data = {
            "agent": self.name,
            "version": self.version,
            "mission": self.mission,
            "timestamp": datetime.now().isoformat(),
            "diagnostics": [],
            "solutions": [],
            "status": "EN_COURS"
        }
    
    def _setup_logging(self):
        """Configuration du logging pour l'agent."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            log_dir = self.workspace_root / "logs" / "agents" / "postgres_diagnostic"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'diagnostic.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger
    
    def diagnostic_conteneur_postgres(self):
        """Diagnostic approfondi du conteneur PostgreSQL"""
        
        self.logger.info("[SEARCH] Diagnostic conteneur PostgreSQL...")
        
        diagnostic = {
            "etape": "diagnostic_conteneur",
            "timestamp": datetime.now().isoformat(),
            "resultats": {}
        }
        
        try:
            # Vrifier les conteneurs
            result = subprocess.run(['docker', 'ps', '-a', '--format', 'json'], 
                                  capture_output=True, text=True, check=True)
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    containers.append(json.loads(line))
            
            postgres_containers = [c for c in containers if 'postgres' in c.get('Image', '')]
            
            diagnostic["resultats"]["total_containers"] = len(containers)
            diagnostic["resultats"]["postgres_containers"] = len(postgres_containers)
            diagnostic["resultats"]["postgres_details"] = postgres_containers
            
            if postgres_containers:
                active_postgres = [c for c in postgres_containers if 'Up' in c.get('Status', '')]
                diagnostic["resultats"]["postgres_actifs"] = len(active_postgres)
                
                if active_postgres:
                    container_name = active_postgres[0]['Names']
                    diagnostic["resultats"]["container_principal"] = container_name
                    self.logger.info(f"[CHECK] Conteneur PostgreSQL actif: {container_name}")
                else:
                    self.logger.warning(" Aucun conteneur PostgreSQL actif")
            else:
                self.logger.error("[CROSS] Aucun conteneur PostgreSQL trouv")
                
        except Exception as e:
            diagnostic["resultats"]["error"] = str(e)
            self.logger.error(f"[CROSS] Erreur diagnostic conteneur: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def diagnostic_encodage_conteneur(self, container_name):
        """Diagnostic encodage depuis l'intrieur du conteneur"""
        
        self.logger.info(f" Diagnostic encodage conteneur {container_name}...")
        
        diagnostic = {
            "etape": "diagnostic_encodage_conteneur", 
            "container": container_name,
            "timestamp": datetime.now().isoformat(),
            "resultats": {}
        }
        
        try:
            # Vrifier l'encodage PostgreSQL
            cmd = ['docker', 'exec', container_name, 'psql', '-U', 'postgres', '-d', 'nextgen_db', '-t', '-c']
            
            # Server encoding
            result = subprocess.run(cmd + ['SHOW server_encoding;'], 
                                  capture_output=True, text=True, check=True)
            server_encoding = result.stdout.strip()
            
            # Client encoding  
            result = subprocess.run(cmd + ['SHOW client_encoding;'],
                                  capture_output=True, text=True, check=True)
            client_encoding = result.stdout.strip()
            
            # LC settings
            result = subprocess.run(cmd + ['SHOW lc_collate;'],
                                  capture_output=True, text=True, check=True)
            lc_collate = result.stdout.strip()
            
            result = subprocess.run(cmd + ['SHOW lc_ctype;'],
                                  capture_output=True, text=True, check=True)
            lc_ctype = result.stdout.strip()
            
            diagnostic["resultats"] = {
                "server_encoding": server_encoding,
                "client_encoding": client_encoding, 
                "lc_collate": lc_collate,
                "lc_ctype": lc_ctype,
                "status": "SUCCESS"
            }
            
            self.logger.info(f"[CHECK] Encodage serveur: {server_encoding}")
            self.logger.info(f"[CHECK] Encodage client: {client_encoding}")
            
        except Exception as e:
            diagnostic["resultats"]["error"] = str(e)
            self.logger.error(f"[CROSS] Erreur diagnostic encodage: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def diagnostic_python_psycopg2(self):
        """Diagnostic des problmes Python/psycopg2"""
        
        self.logger.info(" Diagnostic Python/psycopg2...")
        
        diagnostic = {
            "etape": "diagnostic_python_psycopg2",
            "timestamp": datetime.now().isoformat(),
            "resultats": {}
        }
        
        try:
            # Version Python
            python_version = sys.version
            diagnostic["resultats"]["python_version"] = python_version
            
            # Test import psycopg2
            try:
                import psycopg2
                psycopg2_version = psycopg2.__version__
                diagnostic["resultats"]["psycopg2_version"] = psycopg2_version
                diagnostic["resultats"]["psycopg2_import"] = "SUCCESS"
                self.logger.info(f"[CHECK] psycopg2 version: {psycopg2_version}")
            except Exception as e:
                diagnostic["resultats"]["psycopg2_import"] = f"FAILED: {e}"
                self.logger.error(f"[CROSS] Import psycopg2: {e}")
            
            # Variables d'environnement
            env_vars = {
                'PYTHONIOENCODING': os.environ.get('PYTHONIOENCODING', 'NON_DEFINIE'),
                'PYTHONUTF8': os.environ.get('PYTHONUTF8', 'NON_DEFINIE'),
                'LANG': os.environ.get('LANG', 'NON_DEFINIE'),
                'LC_ALL': os.environ.get('LC_ALL', 'NON_DEFINIE')
            }
            diagnostic["resultats"]["env_vars"] = env_vars
            
        except Exception as e:
            diagnostic["resultats"]["error"] = str(e)
            self.logger.error(f"[CROSS] Erreur diagnostic Python: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def generer_solution_encodage_definitive(self):
        """Gnration de la solution dfinitive pour l'encodage"""
        
        self.logger.info("[BULB] Gnration solution encodage dfinitive...")
        
        solution = {
            "nom": "Solution Encodage PostgreSQL Dfinitive",
            "timestamp": datetime.now().isoformat(),
            "etapes": [],
            "scripts": []
        }
        
        # tape 1: Script PowerShell configuration systme
        script_ps1 = '''
# Configuration encodage systme Windows pour PostgreSQL
Write-Host "Configuration encodage PostgreSQL Windows..." -ForegroundColor Green

# Variables utilisateur
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User") 
[System.Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[System.Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

# Variables systme (ncessite admin)
try {
    [System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "Machine")
    [System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "Machine")
    Write-Host "Variables systme configures (admin)" -ForegroundColor Green
} catch {
    Write-Host "Variables systme non configures (pas admin)" -ForegroundColor Yellow
}

Write-Host "Configuration termine. Redmarrer le terminal." -ForegroundColor Red
'''
        
        solutions_dir = self.workspace_root / "docs" / "agents_postgresql_resolution" / "solutions"
        solutions_dir.mkdir(parents=True, exist_ok=True)
        script_ps1_path = solutions_dir / "configure_encoding_system.ps1"
        with open(script_ps1_path, 'w', encoding='utf-8') as f:
            f.write(script_ps1)
        
        solution["scripts"].append({
            "nom": "Configuration systme PowerShell",
            "chemin": str(script_ps1_path),
            "description": "Configure les variables d'environnement systme"
        })
        
        # tape 2: Script Python avec contournement
        script_python = '''#!/usr/bin/env python3
"""
Contournement problme encodage psycopg2 Windows
Solution: Utiliser SQLAlchemy avec options spcifiques
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

def connect_postgres_safe():
    """Connexion PostgreSQL scurise avec gestion encodage"""
    
    # Configuration force
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        # URL de connexion avec options
        DATABASE_URL = (
            "postgresql://postgres:postgres@localhost:5432/nextgen_db"
            "?client_encoding=utf8&application_name=nextgen"
        )
        
        # Moteur SQLAlchemy avec options spcifiques
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            echo=False,
            connect_args={
                "options": "-c client_encoding=utf8 -c timezone=UTC"
            }
        )
        
        return engine
        
    except Exception as e:
        print(f"Erreur connexion: {e}")
        return None

if __name__ == "__main__":
    engine = connect_postgres_safe()
    if engine:
        print("[CHECK] Connexion PostgreSQL russie")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            print(f"Base: {result.fetchone()[0]}")
    else:
        print("[CROSS] chec connexion")
'''
        
        script_python_path = solutions_dir / "postgres_safe_connect.py"
        with open(script_python_path, 'w', encoding='utf-8') as f:
            f.write(script_python)
        
        solution["scripts"].append({
            "nom": "Connexion PostgreSQL scurise",
            "chemin": str(script_python_path),
            "description": "Script Python avec contournement encodage"
        })
        
        # tape 3: Configuration Docker amliore
        docker_compose_final = '''version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: nextgen_postgres_final
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: nextgen_db
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8"
      LC_ALL: en_US.UTF-8
      LANG: en_US.UTF-8
      PGUSER: postgres
      PGPASSWORD: postgres
      PGDATABASE: nextgen_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data_final:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d nextgen_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    command: >
      postgres
      -c shared_preload_libraries=''
      -c log_statement=all
      -c log_destination=stderr
      -c logging_collector=off
      -c client_encoding=UTF8
      -c default_text_search_config=pg_catalog.english
      -c timezone='UTC'

volumes:
  postgres_data_final:
    driver: local

networks:
  default:
    name: nextgen_network_final
'''
        
        docker_compose_path = self.workspace_root / "docker-compose.final.yml"
        with open(docker_compose_path, 'w', encoding='utf-8') as f:
            f.write(docker_compose_final)
        
        solution["scripts"].append({
            "nom": "Docker Compose final",
            "chemin": str(docker_compose_path),
            "description": "Configuration PostgreSQL optimale"
        })
        
        self.rapport_data["solutions"].append(solution)
        self.logger.info("[CHECK] Solution dfinitive gnre")
        
        return solution
    
    def executer_mission(self):
        """Excution de la mission complte"""
        
        self.logger.info(f"[ROCKET] {self.name} - Dmarrage mission diagnostic PostgreSQL")
        
        try:
            # Diagnostic conteneur
            diag_conteneur = self.diagnostic_conteneur_postgres()
            
            # Si conteneur PostgreSQL trouv, diagnostic encodage
            if diag_conteneur["resultats"].get("postgres_actifs", 0) > 0:
                container_name = diag_conteneur["resultats"]["container_principal"]
                self.diagnostic_encodage_conteneur(container_name)
                
                # Diagnostic Python/psycopg2  
            self.diagnostic_python_psycopg2()
                
                # Gnration solution
            self.generer_solution_encodage_definitive()
                
            self.rapport_data["status"] = "SUCCESS"
            self.logger.info("[CHECK] Mission diagnostic termine avec succs")
                
        except Exception as e:
            self.rapport_data["status"] = "FAILED" 
            self.rapport_data["error"] = str(e)
            self.logger.error(f"[CROSS] chec mission: {e}")
            
            # Gnration rapport final
        self.generer_rapport_final()
            
        return self.rapport_data
    
    def generer_rapport_final(self):
        """Gnration du rapport final"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = self.workspace_root / "reports" / "postgres_diagnostic"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Rapport JSON
        rapport_json_path = reports_dir / f"diagnostic_postgres_{timestamp}.json"
        with open(rapport_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.rapport_data, f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown
        rapport_md_path = reports_dir / "DIAGNOSTIC_POSTGRES_FINAL.md"
        
        md_content = f"""# [SEARCH] DIAGNOSTIC POSTGRESQL FINAL
*Agent: {self.name} v{self.version}*
*Gnr le: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## [TARGET] MISSION
{self.mission}

## [CHART] RSUM EXCUTIF
**Statut:** {self.rapport_data['status']}
**Diagnostics raliss:** {len(self.rapport_data['diagnostics'])}
**Solutions gnres:** {len(self.rapport_data['solutions'])}

## [SEARCH] DIAGNOSTICS RALISS

"""
        
        for i, diag in enumerate(self.rapport_data['diagnostics'], 1):
            md_content += f"### {i}. {diag['etape'].replace('_', ' ').title()}\n"
            md_content += f"**Timestamp:** {diag['timestamp']}\n\n"
            if 'resultats' in diag:
                md_content += "**Rsultats:**\n```json\n"
                md_content += json.dumps(diag['resultats'], indent=2, ensure_ascii=False)
                md_content += "\n```\n\n"
        
        md_content += "## [BULB] SOLUTIONS PROPOSES\n\n"
        
        for i, sol in enumerate(self.rapport_data['solutions'], 1):
            md_content += f"### {i}. {sol['nom']}\n"
            md_content += f"**Scripts gnrs:** {len(sol['scripts'])}\n\n"
            for script in sol['scripts']:
                md_content += f"- **{script['nom']}:** `{script['chemin']}`\\n"
                md_content += f"  - {script['description']}\\n"
        
        md_content += f"\\n---\\n*Rapport gnr par {self.name} v{self.version}*"
        
        with open(rapport_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        self.logger.info(f"[CLIPBOARD] Rapport final: {rapport_md_path}")

if __name__ == "__main__":
    agent = AgentDiagnosticPostgreSQL()
    resultat = agent.executer_mission()
    
    print(f"\n[TARGET] Mission termine: {resultat['status']}")
    if resultat['status'] == 'SUCCESS':
        print("[CHECK] Diagnostic complet et solutions gnres")
    else:
        print("[CROSS] Problmes dtects pendant le diagnostic")

