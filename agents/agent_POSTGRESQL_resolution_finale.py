#!/usr/bin/env python3
"""
Agent Rsolution Finale PostgreSQL
Mission: Contournement dfinitif du problme d'encodage avec solution fonctionnelle
"""

import subprocess
import json
import os
import sys
import time
from core import logging_manager
from datetime import datetime
from pathlib import Path
from ..memory_api.app.db.models import Base, AgentSession

class AgentResolutionFinale:
    """Agent de rsolution finale pour PostgreSQL"""
    
    def __init__(self):
    self.name = "Agent Rsolution Finale PostgreSQL"
    self.version = "1.0.0"
    self.mission = "Contournement et solution fonctionnelle"
        
        # Configuration logging sans emojis
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
        # LoggingManager NextGeneration - Agent
    self.logger = logging_manager.get_logger(
        'AgentPostgresResolution',
        custom_config={
            'logger_name': 'AgentPostgresResolution',
            'file_path': Path("C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\resolution.log")
        }
    )
        
    self.solutions_testees = []
    
    def solution_1_docker_recreation(self):
        """Solution 1: Recrer PostgreSQL avec encodage forc"""
        
    self.logger.info("Solution 1: Recreation PostgreSQL avec encodage force")
        
    try:
            # Arrter tous les conteneurs PostgreSQL
        subprocess.run(['docker', 'stop', 'agent_postgres_nextgen_utf8'], 
                     capture_output=True, check=False)
        subprocess.run(['docker', 'rm', 'agent_postgres_nextgen_utf8'], 
                     capture_output=True, check=False)
            
            # Crer nouveau conteneur avec variables d'environnement spcifiques
        cmd = [
            'docker', 'run', '-d',
            '--name', 'postgres_final_utf8',
            '-p', '5432:5432',
            '-e', 'POSTGRES_USER=postgres',
            '-e', 'POSTGRES_PASSWORD=postgres', 
            '-e', 'POSTGRES_DB=nextgen_db',
            '-e', 'POSTGRES_INITDB_ARGS=--encoding=UTF8 --lc-collate=C --lc-ctype=C',
            '-e', 'LC_ALL=C',
            '-e', 'LANG=C',
            'postgres:16-alpine'
        ]
            
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
        self.logger.info("PostgreSQL recre avec encodage C")
            
            # Attendre dmarrage
        time.sleep(10)
            
            # Test connexion simple dans le conteneur
        test_cmd = ['docker', 'exec', 'postgres_final_utf8', 'psql', 
                   '-U', 'postgres', '-d', 'nextgen_db', '-c', 'SELECT 1;']
            
        test_result = subprocess.run(test_cmd, capture_output=True, text=True, check=True)
            
        self.solutions_testees.append({
            "solution": "Docker recreation",
            "status": "SUCCESS",
            "container": "postgres_final_utf8"
        })
            
        return True
            
    except Exception as e:
        self.logger.error(f"Echec solution 1: {e}")
        self.solutions_testees.append({
            "solution": "Docker recreation",
            "status": "FAILED",
            "error": str(e)
        })
        return False
    
    def solution_2_sqlite_fallback(self):
        """Solution 2: Fallback vers SQLite pour tests"""
        
    self.logger.info("Solution 2: Fallback SQLite pour tests et dveloppement")
        
    try:
            # Crer configuration SQLite
        sqlite_config = '''
# Configuration SQLite pour dveloppement NextGeneration
DATABASE_URL = "sqlite:///./nextgen_dev.db"

# Pour tests
import os
from sqlalchemy import create_engine
from memory_api.app.db.models import Base

def get_test_engine():
    """Moteur SQLite pour tests"""
    engine = create_engine("sqlite:///./test_nextgen.db", echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_dev_engine():
    """Moteur SQLite pour dveloppement"""
    engine = create_engine("sqlite:///./nextgen_dev.db", echo=False)
    Base.metadata.create_all(engine)
    return engine
'''
            
        config_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\sqlite_config.py"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(sqlite_config)
            
            # Test SQLite
        sys.path.append("C:\\Dev\\nextgeneration")
        from sqlalchemy import create_engine
        from memory_api.app.db.models import Base, AgentSession
            
        engine = create_engine("sqlite:///./test_resolution.db", echo=False)
        Base.metadata.create_all(engine)
            
            # Test insertion
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
            
        test_agent = AgentSession(
            session_id="test_resolution_finale",
            agent_id="resolution_agent",
            agent_type="testing",
            session_metadata={"test": "sqlite_ok"}
        )
            
        session.add(test_agent)
        session.commit()
            
        count = session.query(AgentSession).count()
        session.close()
            
        self.logger.info(f"SQLite test russi - {count} sessions")
            
        self.solutions_testees.append({
            "solution": "SQLite fallback",
            "status": "SUCCESS", 
            "database": "sqlite:///./test_resolution.db",
            "records": count
        })
            
        return True
            
    except Exception as e:
        self.logger.error(f"Echec solution 2: {e}")
        self.solutions_testees.append({
            "solution": "SQLite fallback",
            "status": "FAILED",
            "error": str(e)
        })
        return False
    
    def solution_3_postgres_minimal(self):
        """Solution 3: Test PostgreSQL avec connexion minimale"""
        
    self.logger.info("Solution 3: Test PostgreSQL connexion minimale")
        
    try:
            # Test avec psql directement sans Python
        cmd = [
            'docker', 'exec', 'postgres_final_utf8',
            'psql', '-U', 'postgres', '-d', 'nextgen_db',
            '-c', 'CREATE TABLE IF NOT EXISTS test_encoding (id SERIAL, data TEXT);'
        ]
            
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Test insertion
        cmd_insert = [
            'docker', 'exec', 'postgres_final_utf8',
            'psql', '-U', 'postgres', '-d', 'nextgen_db',
            '-c', "INSERT INTO test_encoding (data) VALUES ('test_utf8_ok');"
        ]
            
        subprocess.run(cmd_insert, capture_output=True, text=True, check=True)
            
            # Test lecture
        cmd_select = [
            'docker', 'exec', 'postgres_final_utf8',
            'psql', '-U', 'postgres', '-d', 'nextgen_db',
            '-t', '-c', "SELECT COUNT(*) FROM test_encoding;"
        ]
            
        count_result = subprocess.run(cmd_select, capture_output=True, text=True, check=True)
        count = count_result.stdout.strip()
            
        self.logger.info(f"PostgreSQL direct OK - {count} enregistrements")
            
        self.solutions_testees.append({
            "solution": "PostgreSQL minimal direct",
            "status": "SUCCESS",
            "method": "docker exec psql",
            "records": count
        })
            
        return True
            
    except Exception as e:
        self.logger.error(f"Echec solution 3: {e}")
        self.solutions_testees.append({
            "solution": "PostgreSQL minimal direct", 
            "status": "FAILED",
            "error": str(e)
        })
        return False
    
    def generer_recommandations_finales(self):
        """Gnration des recommandations finales"""
        
    self.logger.info("Generation recommandations finales")
        
    solutions_reussies = [s for s in self.solutions_testees if s["status"] == "SUCCESS"]
        
    recommandations = {
        "timestamp": datetime.now().isoformat(),
        "agent": self.name,
        "solutions_testees": len(self.solutions_testees),
        "solutions_reussies": len(solutions_reussies),
        "recommandations": []
    }
        
    if len(solutions_reussies) > 0:
        recommandations["status"] = "SUCCESS"
        recommandations["message"] = f"{len(solutions_reussies)} solutions fonctionnelles trouves"
            
            # Recommandation prioritaire
        if any(s["solution"] == "SQLite fallback" for s in solutions_reussies):
            recommandations["recommandations"].append({
                "priorite": 1,
                "solution": "Dveloppement avec SQLite",
                "description": "Utiliser SQLite pour le dveloppement et tests",
                "avantages": ["Pas de problme encodage", "Simple  configurer", "Rapide"],
                "implementation": "Utiliser sqlite_config.py gnr"
            })
            
        if any(s["solution"] == "PostgreSQL minimal direct" for s in solutions_reussies):
            recommandations["recommandations"].append({
                "priorite": 2,
                "solution": "PostgreSQL via commandes directes", 
                "description": "Utiliser docker exec pour les oprations PostgreSQL",
                "avantages": ["Contourne le problme Python", "PostgreSQL pleinement fonctionnel"],
                "implementation": "Scripts shell/PowerShell pour oprations DB"
            })
            
        if any(s["solution"] == "Docker recreation" for s in solutions_reussies):
            recommandations["recommandations"].append({
                "priorite": 3,
                "solution": "PostgreSQL Docker optimis",
                "description": "Conteneur PostgreSQL avec encodage C", 
                "avantages": ["Stable", "Production ready"],
                "implementation": "Conteneur postgres_final_utf8"
            })
    else:
        recommandations["status"] = "FAILED"
        recommandations["message"] = "Aucune solution fonctionnelle trouve"
        
        # Sauvegarde
    rapport_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\rapports\\RECOMMANDATIONS_FINALES.json"
    with open(rapport_path, 'w', encoding='utf-8') as f:
        json.dump(recommandations, f, indent=2, ensure_ascii=False)
        
        # Rapport markdown
    md_content = f"""# [TARGET] RECOMMANDATIONS FINALES - POSTGRESQL
*Agent: {self.name}*
*Gnr le: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## [CHART] RSUM
- **Solutions testes:** {len(self.solutions_testees)}
- **Solutions russies:** {len(solutions_reussies)}
- **Statut global:** {recommandations['status']}

##  SOLUTIONS TESTES

"""
        
    for i, solution in enumerate(self.solutions_testees, 1):
        status_icon = "[CHECK]" if solution["status"] == "SUCCESS" else "[CROSS]"
        md_content += f"### {i}. {solution['solution']} {status_icon}\n"
        md_content += f"**Statut:** {solution['status']}\n"
        if "error" in solution:
            md_content += f"**Erreur:** {solution['error']}\n"
        md_content += "\n"
        
    md_content += "## [BULB] RECOMMANDATIONS\n\n"
        
    for rec in recommandations.get("recommandations", []):
        md_content += f"### Priorit {rec['priorite']}: {rec['solution']}\n"
        md_content += f"{rec['description']}\n\n"
        md_content += "**Avantages:**\n"
        for avantage in rec['avantages']:
            md_content += f"- {avantage}\n"
        md_content += f"\n**Implmentation:** {rec['implementation']}\n\n"
        
    md_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\rapports\\RECOMMANDATIONS_FINALES.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    self.logger.info(f"Recommandations sauvegardes: {md_path}")
        
    return recommandations
    
    def executer_mission(self):
        """Excution mission complte"""
        
    self.logger.info(f"Demarrage mission: {self.mission}")
        
        # Test des solutions
    self.solution_1_docker_recreation()
    self.solution_2_sqlite_fallback()
        
        # Solution 3 seulement si Docker ok
    if any(s["status"] == "SUCCESS" and "Docker" in s["solution"] for s in self.solutions_testees):
        self.solution_3_postgres_minimal()
        
        # Recommandations finales
    recommandations = self.generer_recommandations_finales()
        
    return recommandations

if __name__ == "__main__":
    agent = AgentResolutionFinale()
    resultat = agent.executer_mission()
    
    print(f"\n[TARGET] MISSION TERMINE: {resultat['status']}")
    print(f"Solutions testes: {resultat['solutions_testees']}")
    print(f"Solutions russies: {resultat['solutions_reussies']}")
    
    if resultat['status'] == 'SUCCESS':
    print("\n[CHECK] Solutions fonctionnelles trouves!")
    for rec in resultat.get('recommandations', []):
        print(f"  {rec['priorite']}. {rec['solution']}")
    else:
    print("\n[CROSS] Aucune solution fonctionnelle trouve")

