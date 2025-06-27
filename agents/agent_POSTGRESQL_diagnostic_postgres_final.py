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
from pathlib import Path
from datetime import datetime
import logging

# Import avec fallback
try:
    from .agent_POSTGRESQL_base import AgentPostgreSQLBase
except ImportError:
    try:
        from agent_POSTGRESQL_base import AgentPostgreSQLBase
    except ImportError:
        # Fallback pour AgentPostgreSQLBase
        class AgentPostgreSQLBase:
            def __init__(self, *args, **kwargs):
                pass
from core.agent_factory_architecture import Task, Result

class AgentPostgresqlDiagnosticPostgresFinal(AgentPostgreSQLBase):
    """Agent spécialisé diagnostic et résolution PostgreSQL encodage"""
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_diagnostic",
            name="Agent Diagnostic PostgreSQL"
        )
        
        # ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ
        try:
            from core.manager import LoggingManager
            logging_manager = LoggingManager()
            self.logger = logging_manager.get_logger(
                config_name="postgresql",
                custom_config={
                    "logger_name": f"nextgen.postgresql.POSTGRESQL_diagnostic_postgres_final.{getattr(self, 'agent_id', 'unknown')}",
                    "log_dir": "logs/postgresql",
                    "metadata": {
                        "agent_type": "POSTGRESQL_diagnostic_postgres_final",
                        "agent_role": "postgresql",
                        "system": "nextgeneration"
                    }
                }
            )
        except ImportError:
            # Fallback en cas d'indisponibilité du LoggingManager
            self.logger = logging.getLogger(self.__class__.__name__)
        self.mission = "Résolution définitive encodage PostgreSQL"
        self.workspace_root = workspace_root if workspace_root else Path(__file__).parent.parent
        
        self.rapport_data = {
            "agent": self.name,
            "version": self.version,
            "mission": self.mission,
            "timestamp": datetime.now().isoformat(),
            "diagnostics": [],
            "solutions": [],
            "status": "EN_COURS"
        }
    
    def get_capabilities(self) -> list:
        """Liste des capacités spécifiques de l'agent"""
        return [
            "diagnostic_conteneur",
            "diagnostic_encodage",
            "diagnostic_python",
            "generation_solution",
            "execution_mission"
        ]

    async def execute_task(self, task: Task) -> Result:
        """Exécution d'une tâche selon le Pattern Factory"""
        try:
            if task.type == "diagnostic_complet":
                # Exécuter la mission complète
                resultats = await self.executer_mission()
                return Result(
                    success=True,
                    data=resultats,
                    metrics={
                        "diagnostics_count": len(resultats["diagnostics"]),
                        "solutions_count": len(resultats["solutions"])
                    }
                )
            elif task.type == "diagnostic_conteneur":
                resultats = await self.diagnostic_conteneur_postgres()
                return Result(success=True, data=resultats)
            elif task.type == "diagnostic_encodage":
                container = task.params.get("container_name")
                if not container:
                    return Result(success=False, error="Nom du conteneur requis")
                resultats = await self.diagnostic_encodage_conteneur(container)
                return Result(success=True, data=resultats)
            elif task.type == "diagnostic_python":
                resultats = await self.diagnostic_python_psycopg2()
                return Result(success=True, data=resultats)
            elif task.type == "generer_solution":
                resultats = await self.generer_solution_encodage_definitive()
                return Result(success=True, data=resultats)
            else:
                return Result(
                    success=False,
                    error=f"Type de tâche non supporté: {task.type}"
                )
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la tâche: {e}")
            return Result(
                success=False,
                error=str(e),
                error_code="EXECUTION_ERROR"
            )
    
    async def diagnostic_conteneur_postgres(self):
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
    
    async def diagnostic_encodage_conteneur(self, container_name):
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
    
    async def diagnostic_python_psycopg2(self):
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
    
    async def generer_solution_encodage_definitive(self):
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
    # ✅ MÉTHODES STANDARDISÉES DE RAPPORT

    def _calculate_report_score(self, metrics: Dict[str, Any]) -> int:
        """Calcule le score global du rapport basé sur les métriques."""
        score = 0
        issues_critiques = []
        
        # Logique de scoring spécifique à l'agent
        # À adapter selon le type d'agent
        
        return score
    
    def _assess_conformity(self, score: int) -> str:
        """Évalue la conformité basée sur le score."""
        if score >= 90:
            return "✅ CONFORME - OPTIMAL"
        elif score >= 70:
            return "✅ CONFORME - ACCEPTABLE"
        else:
            return "❌ NON CONFORME - CRITIQUE"
    
    def _get_quality_level(self, score: int) -> str:
        """Détermine le niveau de qualité."""
        if score >= 90:
            return "OPTIMAL"
        elif score >= 70:
            return "ACCEPTABLE"
        else:
            return "CRITIQUE"
    
    def _generate_recommendations(self, metrics: Dict[str, Any], issues: List[str]) -> List[str]:
        """Génère les recommandations basées sur l'analyse."""
        recommendations = []
        
        # Logique de génération de recommandations
        # À adapter selon le type d'agent
        
        return recommendations
    
    def _generate_standard_report(self, context: Dict, metrics: Dict, timestamp) -> Dict[str, Any]:
        """Génère un rapport selon le format standard de l'agent 06."""
        
        score = self._calculate_report_score(metrics)
        conformity = self._assess_conformity(score)
        quality_level = self._get_quality_level(score)
        
        agent_filename = Path(__file__).name
        
        # Issues critiques (à personnaliser selon l'agent)
        issues_critiques = []
        
        return {
            'agent_id': getattr(self, 'agent_id', 'unknown'),
            'agent_file_name': agent_filename,
            'type_rapport': 'standard',  # À personnaliser
            'timestamp': timestamp.isoformat(),
            'specialisation': 'Agent Spécialisé',  # À personnaliser
            'score_global': score,
            'niveau_qualite': quality_level,
            'conformite': conformity,
            'signature_cryptographique': 'N/A (Fonctionnalité non implémentée pour cet agent)',
            'issues_critiques_identifies': len(issues_critiques),
            'architecture': {
                'description': "Description de l'architecture de l'agent",
                'statut_operationnel': f"Système {getattr(self, 'agent_id', 'unknown')} opérationnel.",
                'confirmation_specialisation': f"{getattr(self, 'agent_id', 'unknown')} confirmé comme spécialiste.",
                'objectifs_principaux': [
                    "Objectif principal 1",
                    "Objectif principal 2",
                    "Objectif principal 3"
                ],
                'technologies_cles': ["Technologie 1", "Technologie 2"]
            },
            'recommandations': self._generate_recommendations(metrics, issues_critiques),
            'issues_critiques_details': issues_critiques if issues_critiques else [
                "Aucun issue critique majeur détecté. Le système fonctionne dans les paramètres attendus."
            ],
            'details_techniques': {
                'strategie': "Stratégie technique de l'agent",
                'composants_actifs': [],
                'metriques_collectees': metrics
            },
            'metriques_detaillees': {
                'score_global': {'actuel': score, 'cible': 100},
                'conformite_pourcentage': {'actuel': score, 'cible': 100, 'unite': '%'}
            },
            'impact_business': {
                'criticite': 'MOYENNE' if score >= 70 else 'HAUTE',
                'domaines_impactes': [],
                'actions_requises': []
            }
        }


    def _generate_markdown_report(self, rapport_json: Dict, context: Dict, timestamp) -> str:
        """Génère un rapport Markdown selon le format standard."""
        
        agent_name = rapport_json.get('agent_id', 'Agent Inconnu')
        type_rapport = rapport_json.get('type_rapport', 'standard')
        score = rapport_json.get('score_global', 0)
        quality = rapport_json.get('niveau_qualite', 'UNKNOWN')
        conformity = rapport_json.get('conformite', 'NON ÉVALUÉ')
        
        markdown_content = f"""# 📊 RAPPORT STRATÉGIQUE : {agent_name.upper()}

## 🎯 RÉSUMÉ EXÉCUTIF

**Agent :** {agent_name}  
**Type de Rapport :** {type_rapport}  
**Date de Génération :** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Score Global :** {score}/100  
**Niveau de Qualité :** {quality}  
**Conformité :** {conformity}  

## 📈 ANALYSE GLOBALE

### Score de Performance
- **Score Actuel :** {score}/100
- **Objectif :** 100/100
- **Statut :** {'🟢 ACCEPTABLE' if score >= 70 else '🔴 CRITIQUE'}

### Architecture
{rapport_json.get('architecture', {}).get('description', 'Description non disponible')}

**Objectifs Principaux :**
"""
        
        # Ajouter les objectifs
        for obj in rapport_json.get('architecture', {}).get('objectifs_principaux', []):
            markdown_content += f"- {obj}\n"
        
        markdown_content += f"""
**Technologies Clés :**
"""
        
        # Ajouter les technologies
        for tech in rapport_json.get('architecture', {}).get('technologies_cles', []):
            markdown_content += f"- {tech}\n"
        
        markdown_content += f"""

## 🔍 RECOMMANDATIONS

"""
        
        # Ajouter les recommandations
        for reco in rapport_json.get('recommandations', []):
            markdown_content += f"- {reco}\n"
        
        markdown_content += f"""

## ⚠️ ISSUES CRITIQUES

"""
        
        # Ajouter les issues critiques
        for issue in rapport_json.get('issues_critiques_details', []):
            markdown_content += f"- {issue}\n"
        
        markdown_content += f"""

## 📊 MÉTRIQUES DÉTAILLÉES

### Performance Globale
- **Score Global :** {rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('actuel', 0)}/{rapport_json.get('metriques_detaillees', {}).get('score_global', {}).get('cible', 100)}
- **Conformité :** {rapport_json.get('metriques_detaillees', {}).get('conformite_pourcentage', {}).get('actuel', 0)}%

## 🎯 IMPACT BUSINESS

**Criticité :** {rapport_json.get('impact_business', {}).get('criticite', 'NON ÉVALUÉ')}

### Domaines Impactés
"""
        
        # Ajouter les domaines impactés
        for domaine in rapport_json.get('impact_business', {}).get('domaines_impactes', []):
            markdown_content += f"- {domaine}\n"
        
        markdown_content += f"""

### Actions Requises
"""
        
        # Ajouter les actions requises
        for action in rapport_json.get('impact_business', {}).get('actions_requises', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""

---
*Rapport généré automatiquement par {agent_name} - NextGeneration System*  
*Timestamp: {timestamp.isoformat()}*
"""
        
        return markdown_content



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
    
    async def executer_mission(self):
        """Excution de la mission complte"""
        
        self.logger.info(f"[ROCKET] {self.name} - Dmarrage mission diagnostic PostgreSQL")
        
        try:
            # Diagnostic conteneur
            diag_conteneur = await self.diagnostic_conteneur_postgres()
            
            # Si conteneur PostgreSQL trouvé, diagnostic encodage
            if diag_conteneur["resultats"].get("postgres_actifs", 0) > 0:
                container_name = diag_conteneur["resultats"]["container_principal"]
                await self.diagnostic_encodage_conteneur(container_name)
                
            # Diagnostic Python/psycopg2  
            await self.diagnostic_python_psycopg2()
                
            # Génération solution
            await self.generer_solution_encodage_definitive()
                
            self.rapport_data["status"] = "SUCCESS"
            self.logger.info("[CHECK] Mission diagnostic terminé avec succès")
                
        except Exception as e:
            self.rapport_data["status"] = "FAILED" 
            self.rapport_data["error"] = str(e)
            self.logger.error(f"[CROSS] Échec mission: {e}")
            
        # Génération rapport final
        await self.generer_rapport_final()
            
        return self.rapport_data
    
    async def generer_rapport_final(self):
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
    agent = AgentPostgresqlDiagnosticPostgresFinal()
    resultat = agent.executer_mission()
    
    print(f"\n[TARGET] Mission termine: {resultat['status']}")
    if resultat['status'] == 'SUCCESS':
        print("[CHECK] Diagnostic complet et solutions gnres")
    else:
        print("[CROSS] Problmes dtects pendant le diagnostic")

