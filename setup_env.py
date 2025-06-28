#!/usr/bin/env python3
"""
Script de configuration automatique du fichier .env pour NextGeneration
"""

import os
import secrets
import string

def generate_secret_key(length=32):
    """Gnre une cl secrte alatoire."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Cre le fichier .env avec les configurations par dfaut."""
    
    env_content = f"""# Configuration de l'orchestrateur NextGeneration
# Gnr automatiquement par setup_env.py

# Cls API - REMPLACEZ PAR VOS VRAIES CLS
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
GOOGLE_API_KEY=AIzaSy-your-google-api-key-here
GEMINI_API_KEY=AIzaSy-your-gemini-api-key-here
ORCHESTRATOR_API_KEY={generate_secret_key(32)}

# Configuration de l'API Memory
MEMORY_API_URL=http://localhost:8001

# Configuration PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

# Configuration Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Configuration gnrale
DEBUG=true
ENVIRONMENT=development
MAX_TASK_DESCRIPTION_LENGTH=5000
MAX_CODE_SIZE=50000
MAX_REQUEST_TIMEOUT=30

# Configuration GPU Ollama
OLLAMA_GPU_DEVICE=1
OLLAMA_HOST=http://localhost:11434

# Configuration Docker
DOCKER_HOST=unix:///var/run/docker.sock

# Configuration de scurit
SECRET_KEY={generate_secret_key(64)}
JWT_SECRET={generate_secret_key(32)}

# Configuration des logs
LOG_LEVEL=INFO
LOG_FILE=logs/orchestrator.log

# Configuration de monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Configuration HAProxy
HAPROXY_STATS_PORT=8404
HAPROXY_STATS_USER=admin
HAPROXY_STATS_PASSWORD={generate_secret_key(16)}

# Configuration PgBouncer
PGBOUNCER_PORT=6432
PGBOUNCER_POOL_SIZE=25
PGBOUNCER_MAX_CLIENT_CONN=100
"""

    # crire le fichier .env
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("[CHECK] Fichier .env cr avec succs!")
        print("\n IMPORTANT: Vous devez maintenant:")
        print("1. Ouvrir le fichier .env")
        print("2. Remplacer 'your-openai-api-key-here' par votre vraie cl OpenAI")
        print("3. Remplacer 'your-anthropic-api-key-here' par votre vraie cl Anthropic")
        print("4. Remplacer 'your-google-api-key-here' par votre vraie cl Google/Gemini (optionnel)")
        print("5. Ajuster les autres paramtres selon votre configuration")
        
        # Crer le dossier logs s'il n'existe pas
        os.makedirs('logs', exist_ok=True)
        print("\n[FOLDER] Dossier 'logs' cr pour les fichiers de log")
        
        return True
        
    except Exception as e:
        print(f"[CROSS] Erreur lors de la cration du fichier .env: {e}")
        return False

def check_existing_env():
    """Vrifie si un fichier .env existe dj."""
    if os.path.exists('.env'):
        response = input("  Un fichier .env existe dj. Le remplacer? (y/N): ")
        return response.lower() in ['y', 'yes', 'o', 'oui']
    return True

def main():
    """Fonction principale."""
    print("[ROCKET] Configuration de l'environnement NextGeneration")
    print("="*50)
    
    if not check_existing_env():
        print("[CROSS] Configuration annule.")
        return
    
    if create_env_file():
        print("\n[TARGET] Configuration termine!")
        print("\nPour tester l'agent de diagnostic PostgreSQL:")
        print("python postgresql_diagnostic_agent.py")
    else:
        print("\n[CROSS] chec de la configuration.")

if __name__ == "__main__":
    main() 



