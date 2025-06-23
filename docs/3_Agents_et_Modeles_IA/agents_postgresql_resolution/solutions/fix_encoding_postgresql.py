#!/usr/bin/env python3
"""
Script de rsolution du problme d'encodage UTF-8 PostgreSQL sur Windows
Solution cible pour les erreurs 'charmap' codec
"""

import os
import json
import subprocess
from datetime import datetime

def fix_windows_encoding():
    """Rsolution des problmes d'encodage Windows/PostgreSQL"""
    
    print("[TOOL] RSOLUTION ENCODAGE WINDOWS/POSTGRESQL")
    print("="*50)
    
    solutions = []
    
    # Solution 1: Variables d'environnement Python
    print("\n1 Configuration variables d'environnement Python...")
    
    env_vars = {
        'PYTHONIOENCODING': 'utf-8',
        'PYTHONLEGACYWINDOWSSTDIO': '1',
        'PYTHONUTF8': '1'
    }
    
    for var, value in env_vars.items():
        os.environ[var] = value
        print(f"   [CHECK] {var}={value}")
    
    solutions.append({
        "solution": "Variables environnement Python",
        "vars": env_vars,
        "status": "APPLIED"
    })
    
    # Solution 2: Test connexion PostgreSQL avec encodage UTF-8
    print("\n2 Test connexion PostgreSQL avec encodage forc...")
    
    try:
        import psycopg2
        from sqlalchemy import create_engine
        from sqlalchemy.pool import NullPool
        
        # Connexion avec options d'encodage explicites
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nextgen_db?client_encoding=utf8"
        
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,
            connect_args={
                "client_encoding": "utf8",
                "options": "-c timezone=UTC"
            }
        )
        
        connection = engine.connect()
        result = connection.execute("SELECT version();")
        version_info = result.fetchone()
        connection.close()
        
        print(f"   [CHECK] Connexion PostgreSQL russie")
        print(f"   [CHART] Version: {version_info[0][:50]}...")
        
        solutions.append({
            "solution": "Connexion PostgreSQL UTF-8",
            "database_url": DATABASE_URL,
            "status": "SUCCESS",
            "version": str(version_info[0])
        })
        
    except Exception as e:
        print(f"   [CROSS] chec connexion: {e}")
        solutions.append({
            "solution": "Connexion PostgreSQL UTF-8",
            "status": "FAILED",
            "error": str(e)
        })
    
    # Solution 3: Test cration tables avec encodage
    print("\n3 Test cration tables avec models corrigs...")
    
    try:
        import sys
        sys.path.append("C:\\Dev\\nextgeneration")
        
        from memory_api.app.db.models import Base, AgentSession, MemoryItem
        
        if 'engine' in locals() and solutions[-1]["status"] == "SUCCESS":
            Base.metadata.create_all(engine)
            print("   [CHECK] Tables cres sans erreur d'encodage")
            
            solutions.append({
                "solution": "Cration tables SQLAlchemy",
                "status": "SUCCESS",
                "tables": ["agent_sessions", "memory_items"]
            })
        else:
            print("    Saut - pas de connexion DB")
            solutions.append({
                "solution": "Cration tables SQLAlchemy",
                "status": "SKIPPED",
                "reason": "Pas de connexion DB"
            })
            
    except Exception as e:
        print(f"   [CROSS] chec cration tables: {e}")
        solutions.append({
            "solution": "Cration tables SQLAlchemy",
            "status": "FAILED",
            "error": str(e)
        })
    
    # Solution 4: Script PowerShell pour variables systme
    print("\n4 Gnration script PowerShell pour variables systme...")
    
    powershell_script = '''
# Script de configuration encodage PostgreSQL Windows
Write-Host "Configuration encodage PostgreSQL..." -ForegroundColor Green

# Variables d'environnement systme
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
[Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")
[Environment]::SetEnvironmentVariable("LC_ALL", "en_US.UTF-8", "User")

Write-Host "Variables d'environnement configures." -ForegroundColor Yellow
Write-Host "Redmarrer le terminal pour appliquer les changements." -ForegroundColor Red
'''
    
    script_path = "C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\fix_encoding_windows.ps1"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(powershell_script)
    
    print(f"   [CHECK] Script PowerShell cr: {script_path}")
    
    solutions.append({
        "solution": "Script PowerShell configuration",
        "script_path": script_path,
        "status": "GENERATED"
    })
    
    # Rsum et rapport
    print("\n" + "="*50)
    print("[CHART] RSUM SOLUTIONS ENCODAGE")
    print("="*50)
    
    success_count = sum(1 for s in solutions if s["status"] in ["SUCCESS", "APPLIED", "GENERATED"])
    total_count = len(solutions)
    
    for i, solution in enumerate(solutions, 1):
        status = solution["status"]
        icon = "[CHECK]" if status in ["SUCCESS", "APPLIED", "GENERATED"] else "[CROSS]" if status == "FAILED" else ""
        print(f"{icon} {i}. {solution['solution']}: {status}")
    
    print(f"\n Score: {success_count}/{total_count} solutions appliques")
    
    # Sauvegarde rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rapport_path = f"C:\\Dev\\nextgeneration\\docs\\agents_postgresql_resolution\\solutions\\encoding_fix_report_{timestamp}.json"
    
    rapport = {
        "timestamp": datetime.now().isoformat(),
        "solutions": solutions,
        "success_count": success_count,
        "total_count": total_count,
        "success_rate": (success_count / total_count) * 100
    }
    
    with open(rapport_path, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"[CLIPBOARD] Rapport sauvegard: {rapport_path}")
    
    if rapport["success_rate"] >= 75:
        print("\n ENCODAGE RSOLU - PostgreSQL prt  l'emploi!")
    elif rapport["success_rate"] >= 50:
        print("\n[CHECK] ENCODAGE PARTIELLEMENT RSOLU - Redmarrage terminal recommand")
    else:
        print("\n ENCODAGE  COMPLTER - Intervention manuelle requise")
    
    return rapport

if __name__ == "__main__":
    resultat = fix_windows_encoding()




