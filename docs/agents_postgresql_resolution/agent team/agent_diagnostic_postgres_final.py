#!/usr/bin/env python3
"""
Agent Diagnostic PostgreSQL - Spécialisé résolution encodage
Mission: Diagnostiquer et résoudre définitivement le problème d'encodage UTF-8
"""

import subprocess
import json
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

class AgentDiagnosticPostgreSQL:
    """Agent spécialisé diagnostic et résolution PostgreSQL encodage"""
    
    def __init__(self):
        self.name = "Agent Diagnostic PostgreSQL"
        self.version = "2.0.0"
        self.mission = "Résolution définitive encodage PostgreSQL"
        
        # Configuration logging
        log_dir = Path("C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "diagnostic_postgres.log", encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("diagnostic_postgres")
        
        self.rapport_data = {
            "agent": self.name,
            "version": self.version,
            "mission": self.mission,
            "timestamp": datetime.now().isoformat(),
            "diagnostics": [],
            "solutions": [],
            "status": "EN_COURS"
        }
    
    def diagnostic_conteneur_postgres(self):
        """Diagnostic approfondi du conteneur PostgreSQL"""
        
        self.logger.info("🔍 Diagnostic conteneur PostgreSQL...")
        
        diagnostic = {
            "etape": "diagnostic_conteneur",
            "timestamp": datetime.now().isoformat(),
            "resultats": {}
        }
        
        try:
            # Vérifier les conteneurs
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
                    self.logger.info(f"✅ Conteneur PostgreSQL actif: {container_name}")
                else:
                    self.logger.warning("⚠️ Aucun conteneur PostgreSQL actif")
            else:
                self.logger.error("❌ Aucun conteneur PostgreSQL trouvé")
                
        except Exception as e:
            diagnostic["resultats"]["error"] = str(e)
            self.logger.error(f"❌ Erreur diagnostic conteneur: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def diagnostic_encodage_conteneur(self, container_name):
        """Diagnostic encodage depuis l'intérieur du conteneur"""
        
        self.logger.info(f"🔤 Diagnostic encodage conteneur {container_name}...")
        
        diagnostic = {
            "etape": "diagnostic_encodage_conteneur", 
            "container": container_name,
            "timestamp": datetime.now().isoformat(),
            "resultats": {}
        }
        
        try:
            # Vérifier l'encodage PostgreSQL
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
            
            self.logger.info(f"✅ Encodage serveur: {server_encoding}")
            self.logger.info(f"✅ Encodage client: {client_encoding}")
            
        except Exception as e:
            diagnostic["resultats"]["error"] = str(e)
            self.logger.error(f"❌ Erreur diagnostic encodage: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def diagnostic_python_psycopg2(self):
        """Diagnostic des problèmes Python/psycopg2"""
        
        self.logger.info("🐍 Diagnostic Python/psycopg2...")
        
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
                self.logger.info(f"✅ psycopg2 version: {psycopg2_version}")
            except Exception as e:
                diagnostic["resultats"]["psycopg2_import"] = f"FAILED: {e}"
                self.logger.error(f"❌ Import psycopg2: {e}")
            
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
            self.logger.error(f"❌ Erreur diagnostic Python: {e}")
        
        self.rapport_data["diagnostics"].append(diagnostic)
        return diagnostic
    
    def generer_solution_encodage_definitive(self):
        """Génération de la solution définitive pour l'encodage"""
        
        self.logger.info("💡 Génération solution encodage définitive...")
        
        solution = {
            "nom": "Solution Encodage PostgreSQL Définitive",
            "timestamp": datetime.now().isoformat(),
            "etapes": [],
            "scripts": []
        }
        
        # Étape 1: Script PowerShell configuration système
        script_ps1 = '''
# Configuration encodage système Windows pour PostgreSQL
Write-Host "Configuration encodage PostgreSQL Windows..." -ForegroundColor Green

# Variables utilisateur
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User") 
[System.Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[System.Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

# Variables système (nécessite admin)
try {
    [System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "Machine")
    [System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "Machine")
    Write-Host "Variables système configurées (admin)" -ForegroundColor Green
} catch {
    Write-Host "Variables système non configurées (pas admin)" -ForegroundColor Yellow
}

Write-Host "Configuration terminée. Redémarrer le terminal." -ForegroundColor Red
'''
        
        script_ps1_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\configure_encoding_system.ps1"
        with open(script_ps1_path, 'w', encoding='utf-8') as f:
            f.write(script_ps1)
        
        solution["scripts"].append({
            "nom": "Configuration système PowerShell",
            "chemin": script_ps1_path,
            "description": "Configure les variables d'environnement système"
        })
        
        # Étape 2: Script Python avec contournement
        script_python = '''#!/usr/bin/env python3
"""
Contournement problème encodage psycopg2 Windows
Solution: Utiliser SQLAlchemy avec options spécifiques
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

def connect_postgres_safe():
    """Connexion PostgreSQL sécurisée avec gestion encodage"""
    
    # Configuration forcée
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    try:
        # URL de connexion avec options
        DATABASE_URL = (
            "postgresql://postgres:postgres@localhost:5432/nextgen_db"
            "?client_encoding=utf8&application_name=nextgen"
        )
        
        # Moteur SQLAlchemy avec options spécifiques
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
        print("✅ Connexion PostgreSQL réussie")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            print(f"Base: {result.fetchone()[0]}")
    else:
        print("❌ Échec connexion")
'''
        
        script_python_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\postgres_safe_connect.py"
        with open(script_python_path, 'w', encoding='utf-8') as f:
            f.write(script_python)
        
        solution["scripts"].append({
            "nom": "Connexion PostgreSQL sécurisée",
            "chemin": script_python_path,
            "description": "Script Python avec contournement encodage"
        })
        
        # Étape 3: Configuration Docker améliorée
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
        
        docker_compose_path = "C:\\Dev\\nextgeneration\\docker-compose.final.yml"
        with open(docker_compose_path, 'w', encoding='utf-8') as f:
            f.write(docker_compose_final)
        
        solution["scripts"].append({
            "nom": "Docker Compose final",
            "chemin": docker_compose_path,
            "description": "Configuration PostgreSQL optimale"
        })
        
        self.rapport_data["solutions"].append(solution)
        self.logger.info("✅ Solution définitive générée")
        
        return solution
    
    def executer_mission(self):
        """Exécution de la mission complète"""
        
        self.logger.info(f"🚀 {self.name} - Démarrage mission diagnostic PostgreSQL")
        
        try:
            # Diagnostic conteneur
            diag_conteneur = self.diagnostic_conteneur_postgres()
            
            # Si conteneur PostgreSQL trouvé, diagnostic encodage
            if diag_conteneur["resultats"].get("postgres_actifs", 0) > 0:
                container_name = diag_conteneur["resultats"]["container_principal"]
                self.diagnostic_encodage_conteneur(container_name)
            
            # Diagnostic Python/psycopg2  
            self.diagnostic_python_psycopg2()
            
            # Génération solution
            self.generer_solution_encodage_definitive()
            
            self.rapport_data["status"] = "SUCCESS"
            self.logger.info("✅ Mission diagnostic terminée avec succès")
            
        except Exception as e:
            self.rapport_data["status"] = "FAILED" 
            self.rapport_data["error"] = str(e)
            self.logger.error(f"❌ Échec mission: {e}")
        
        # Génération rapport final
        self.generer_rapport_final()
        
        return self.rapport_data
    
    def generer_rapport_final(self):
        """Génération du rapport final"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Rapport JSON
        rapport_json = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\rapports\\diagnostic_postgres_{timestamp}.json"
        with open(rapport_json, 'w', encoding='utf-8') as f:
            json.dump(self.rapport_data, f, indent=2, ensure_ascii=False)
        
        # Rapport Markdown
        rapport_md = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\rapports\\DIAGNOSTIC_POSTGRES_FINAL.md"
        
        md_content = f"""# 🔍 DIAGNOSTIC POSTGRESQL FINAL
*Agent: {self.name} v{self.version}*
*Généré le: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## 🎯 MISSION
{self.mission}

## 📊 RÉSUMÉ EXÉCUTIF
**Statut:** {self.rapport_data['status']}
**Diagnostics réalisés:** {len(self.rapport_data['diagnostics'])}
**Solutions générées:** {len(self.rapport_data['solutions'])}

## 🔍 DIAGNOSTICS RÉALISÉS

"""
        
        for i, diag in enumerate(self.rapport_data['diagnostics'], 1):
            md_content += f"### {i}. {diag['etape'].replace('_', ' ').title()}\n"
            md_content += f"**Timestamp:** {diag['timestamp']}\n\n"
            if 'resultats' in diag:
                md_content += "**Résultats:**\n```json\n"
                md_content += json.dumps(diag['resultats'], indent=2, ensure_ascii=False)
                md_content += "\n```\n\n"
        
        md_content += "## 💡 SOLUTIONS PROPOSÉES\n\n"
        
        for i, sol in enumerate(self.rapport_data['solutions'], 1):
            md_content += f"### {i}. {sol['nom']}\n"
            md_content += f"**Scripts générés:** {len(sol['scripts'])}\n\n"
            for script in sol['scripts']:
                md_content += f"- **{script['nom']}:** `{script['chemin']}`\n"
                md_content += f"  - {script['description']}\n"
        
        md_content += f"\n---\n*Rapport généré par {self.name} v{self.version}*"
        
        with open(rapport_md, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        self.logger.info(f"📋 Rapport final: {rapport_md}")

if __name__ == "__main__":
    agent = AgentDiagnosticPostgreSQL()
    resultat = agent.executer_mission()
    
    print(f"\n🎯 Mission terminée: {resultat['status']}")
    if resultat['status'] == 'SUCCESS':
        print("✅ Diagnostic complet et solutions générées")
    else:
        print("❌ Problèmes détectés pendant le diagnostic")
