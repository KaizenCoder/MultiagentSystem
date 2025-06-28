# 🚀 GUIDE D'UTILISATION - PROJET NEXTGENERATION

**Version :** v1.4.0  
**Date :** 17 juin 2025  
**Objectif :** Guide complet pour tester et utiliser l'environnement de développement multi-agent  

---

## 🎯 APERÇU DU PROJET

Le projet **NextGeneration** est un environnement de développement assisté par des agents IA multiples, conçu pour améliorer la productivité des développeurs à travers une collaboration intelligente entre agents spécialisés.

### Architecture Services
- **🎮 Orchestrateur** : `http://localhost:8000` - Coordination des agents et workflow
- **🧠 Memory API** : `http://localhost:8001` - Gestion mémoire et RAG  
- **🔌 Extension Cursor** : Interface VS Code intégrée
- **📊 Monitoring** : Prometheus/Grafana/Jaeger pour observabilité

---

## 📋 PRÉREQUIS SYSTÈME

### Logiciels Requis
- **Docker Desktop** (version 20.10+)
- **Docker Compose** (version 3.8+)
- **Node.js** (version 18+)
- **VS Code ou Cursor** (pour l'extension)
- **Git** (pour cloner le repository)

### Configuration Recommandée
- **RAM** : 8GB minimum, 16GB recommandé
- **CPU** : 4 cœurs minimum
- **Disque** : 10GB d'espace libre
- **OS** : Windows 10/11, macOS 11+, Ubuntu 20.04+

---

## 🛠️ INSTALLATION RAPIDE

### 1. Cloner le Repository

```bash
# Cloner le projet
git clone <repository-url>
cd nextgeneration

# Vérifier la structure
ls -la
```

### 2. Configuration des Variables d'Environnement

```bash
# Copier le fichier d'exemple
cp env.example .env

# Éditer avec vos clés API
notepad .env  # Windows
nano .env     # Linux/macOS
```

#### Variables à Configurer

```env
# ⚠️ OBLIGATOIRE - Clés API LLM
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 🔐 Base de Données (optionnel, valeurs par défaut)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=agent_memory

# 🌐 URLs Services (optionnel)
MEMORY_API_URL=http://memory_api:8001
ORCHESTRATOR_URL=http://orchestrator:8000

# 📊 ChromaDB (optionnel)
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

### 3. Lancement des Services

```bash
# Construire et démarrer tous les services
docker-compose up --build -d

# Vérifier le statut des containers
docker-compose ps

# Suivre les logs (optionnel)
docker-compose logs -f
```

### 4. Vérification de l'Installation

```bash
# Test health check des services
curl http://localhost:8000/health    # Orchestrateur
curl http://localhost:8001/health    # Memory API

# Vérifier que tous les services répondent
docker-compose ps
```

---

## 🧪 TESTS FONCTIONNELS

### Test 1 : API Orchestrateur

#### Endpoint Principal - Exécution de Tâche

```bash
# Test de base avec curl
curl -X POST "http://localhost:8000/invoke" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key-here" \
  -d '{
    "task_description": "Analyser ce code Python et suggérer des améliorations",
    "code_context": "def hello():\n    print(\"Hello World\")\n    return None"
  }'
```

#### Endpoint Status - Suivi de Tâche

```bash
# Vérifier le statut d'une tâche
curl -X GET "http://localhost:8000/status/{task_id}" \
  -H "X-API-KEY: your-api-key-here"
```

#### Endpoint Monitoring - Métriques

```bash
# Métriques système
curl -X GET "http://localhost:8000/metrics" \
  -H "X-API-KEY: your-api-key-here"

# Métriques business
curl -X GET "http://localhost:8000/business-metrics" \
  -H "X-API-KEY: your-api-key-here"
```

### Test 2 : Memory API

#### RAG Query - Recherche Sémantique

```bash
# Query RAG
curl -X POST "http://localhost:8001/rag_query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Comment optimiser une fonction Python?",
    "top_k": 5
  }'
```

#### State Management - Gestion d'État

```bash
# Stocker un état de session
curl -X POST "http://localhost:8001/state" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "state_data": {"current_task": "code_review", "progress": 50}
  }'

# Récupérer un état
curl -X GET "http://localhost:8001/state/test-session-123"
```

### Test 3 : Endpoints de Performance

#### Cache Management

```bash
# Statistiques du cache Redis
curl -X GET "http://localhost:8000/cache/stats" \
  -H "X-API-KEY: your-api-key-here"

# Clear cache
curl -X POST "http://localhost:8000/cache/clear" \
  -H "X-API-KEY: your-api-key-here"
```

#### Load Testing

```bash
# Configurations disponibles
curl -X GET "http://localhost:8000/load-test/configs" \
  -H "X-API-KEY: your-api-key-here"

# Exécuter un test de charge
curl -X POST "http://localhost:8000/load-test/run/basic_workflow" \
  -H "X-API-KEY: your-api-key-here"
```

---

## 🔌 EXTENSION CURSOR/VS CODE

### Installation de l'Extension

```bash
# Naviguer vers le dossier extension
cd cursor_extension

# Installer les dépendances
npm install

# Compiler l'extension
npm run compile

# Générer le package VSIX
npm run package

# Installer l'extension (VS Code)
code --install-extension cursor-extension-0.0.1.vsix

# Installer l'extension (Cursor)
cursor --install-extension cursor-extension-0.0.1.vsix
```

### Utilisation de l'Extension

1. **Ouvrir VS Code/Cursor** dans votre projet
2. **Sélectionner du code** à analyser/améliorer
3. **Commande Palette** : `Ctrl+Shift+P`
4. **Exécuter** : `Multi-Agent: Orchestrate Task`
5. **Décrire la tâche** : "Optimise cette fonction et ajoute des tests"
6. **Observer** le streaming des résultats en temps réel

### Configuration Extension

```json
// settings.json
{
  "multiAgent.orchestratorUrl": "http://localhost:8000",
  "multiAgent.apiKey": "your-api-key-here",
  "multiAgent.enableStreaming": true,
  "multiAgent.maxResponseTime": 30000
}
```

---

## 📊 INTERFACE DE MONITORING

### Documentation API Interactive

Accédez aux interfaces Swagger pour explorer les APIs :

- **Orchestrateur** : http://localhost:8000/docs
- **Memory API** : http://localhost:8001/docs

### Métriques Prometheus

```bash
# Endpoints de métriques
curl http://localhost:8000/metrics          # Métriques orchestrateur
curl http://localhost:8001/metrics          # Métriques memory API
```

### Dashboards Disponibles

```bash
# Dashboard de performance complet
curl -X GET "http://localhost:8000/performance/comprehensive" \
  -H "X-API-KEY: your-api-key-here"

# Vue d'ensemble architecture
curl -X GET "http://localhost:8000/architecture/overview" \
  -H "X-API-KEY: your-api-key-here"
```

---

## 🎮 SCENARIOS D'UTILISATION

### Scenario 1 : Analyse de Code Simple

```bash
# 1. Soumettre du code pour analyse
TASK_ID=$(curl -s -X POST "http://localhost:8000/invoke" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-key" \
  -d '{
    "task_description": "Analyser cette fonction et suggérer des améliorations",
    "code_context": "def calculate_total(items):\n    total = 0\n    for item in items:\n        total = total + item[\"price\"]\n    return total"
  }' | jq -r '.task_id')

echo "Task ID: $TASK_ID"

# 2. Suivre le statut
curl -X GET "http://localhost:8000/status/$TASK_ID" \
  -H "X-API-KEY: demo-key"

# 3. Obtenir le feedback final
curl -X POST "http://localhost:8000/feedback/$TASK_ID" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-key" \
  -d '{"rating": 5, "comments": "Excellent analysis!"}'
```

### Scenario 2 : Workflow Complet avec Memory

```bash
# 1. Indexer des fichiers dans la memory
curl -X POST "http://localhost:8001/index_files" \
  -H "Content-Type: application/json" \
  -d '{
    "directory": "/app/codebase_docs",
    "file_extensions": [".py", ".md", ".js"],
    "force_reindex": false
  }'

# 2. Query RAG pour contexte
curl -X POST "http://localhost:8001/rag_query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Meilleures pratiques pour FastAPI",
    "top_k": 3
  }'

# 3. Utiliser le contexte dans une tâche
curl -X POST "http://localhost:8000/invoke" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-key" \
  -d '{
    "task_description": "Créer une API FastAPI en suivant les meilleures pratiques trouvées",
    "code_context": "# Contexte des meilleures pratiques récupéré du RAG"
  }'
```

### Scenario 3 : Test de Performance

```bash
# 1. Vérifier l'état du système
curl -X GET "http://localhost:8000/performance/comprehensive" \
  -H "X-API-KEY: demo-key"

# 2. Exécuter un test de charge
curl -X POST "http://localhost:8000/load-test/run/api_endpoints" \
  -H "X-API-KEY: demo-key"

# 3. Surveiller les métriques
curl -X GET "http://localhost:8000/metrics" \
  -H "X-API-KEY: demo-key"
```

---

## 🔧 CONFIGURATION AVANCÉE

### Variables d'Environnement Complètes

```env
# === CLÉS API ===
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# === BASE DE DONNÉES ===
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=agent_memory
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# === SERVICES ===
MEMORY_API_URL=http://memory_api:8001
ORCHESTRATOR_URL=http://orchestrator:8000

# === CHROMADB ===
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# === SÉCURITÉ ===
API_KEY_SECRET=your-secret-key-here
JWT_SECRET=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# === PERFORMANCE ===
REDIS_URL=redis://redis:6379
MAX_WORKERS=4
CACHE_TTL=3600

# === OBSERVABILITÉ ===
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
PROMETHEUS_GATEWAY=http://prometheus:9091
LOG_LEVEL=INFO
```

### Ports Utilisés

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Orchestrateur | 8000 | http://localhost:8000 | API principale |
| Memory API | 8001 | http://localhost:8001 | Gestion mémoire |
| PostgreSQL | 5432 | localhost:5432 | Base de données |
| ChromaDB | 8000 | container:8000 | Vector database |
| Redis | 6379 | container:6379 | Cache |

---

## 🚨 DÉPANNAGE

### Problèmes Communs

#### Services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Redémarrer les services
docker-compose down
docker-compose up --build -d

# Vérifier l'espace disque
df -h
```

#### API Key manquante

```bash
# Vérifier le fichier .env
cat .env | grep API_KEY

# Ajouter une clé temporaire
export OPENAI_API_KEY="sk-your-key-here"
```

#### Timeout de connexion

```bash
# Vérifier la connectivité des services
curl -m 5 http://localhost:8000/health
curl -m 5 http://localhost:8001/health

# Vérifier les containers
docker ps -a
```

### Logs Utiles

```bash
# Logs détaillés par service
docker-compose logs orchestrator
docker-compose logs memory_api
docker-compose logs postgres
docker-compose logs chromadb

# Logs en temps réel
docker-compose logs -f --tail=100
```

### Reset Complet

```bash
# Arrêter et supprimer tout
docker-compose down -v --remove-orphans

# Nettoyer les images
docker system prune -af

# Redémarrer complètement
docker-compose up --build -d
```

---

## 📈 MÉTRIQUES ET MONITORING

### Health Checks

```bash
# Vérification automatique
#!/bin/bash
services=("orchestrator:8000" "memory_api:8001")

for service in "${services[@]}"; do
    url="http://localhost:${service#*:}/health"
    if curl -f -s "$url" > /dev/null; then
        echo "✅ $service OK"
    else
        echo "❌ $service FAIL"
    fi
done
```

### Métriques de Performance

```bash
# Script de monitoring
#!/bin/bash
echo "=== PERFORMANCE METRICS ==="
curl -s "http://localhost:8000/performance/comprehensive" | jq '{
    memory: .memory_management.memory_usage_mb,
    active_sessions: .memory_management.active_sessions,
    redis_status: .cache.status,
    response_time: .system.avg_response_time_ms
}'
```

### Alertes Recommandées

- **Memory Usage** > 1GB
- **Response Time** > 5 secondes
- **Error Rate** > 5%
- **Active Sessions** > 100

---

## 🎯 PROCHAINES ÉTAPES

### Après Installation Réussie

1. **Explorer la documentation API** : http://localhost:8000/docs
2. **Tester l'extension VS Code** avec du code réel
3. **Configurer monitoring** (Prometheus/Grafana)
4. **Créer des workflows** personnalisés
5. **Intégrer à votre pipeline** de développement

### Développement Avancé

1. **Personnaliser les agents** dans `/orchestrator/app/agents/`
2. **Ajouter des outils** dans `/orchestrator/app/agents/tools/`
3. **Configurer RAG** avec vos documents
4. **Adapter l'extension** à vos besoins

### Production

1. **Configurer HTTPS** et certificats
2. **Mettre en place monitoring** complet
3. **Configurer backup** des données
4. **Implémenter CI/CD** pipeline

---

## 📞 SUPPORT

### Resources Utiles

- **Documentation** : Voir fichiers `livrable*.md`
- **Architecture** : `PEER_REVIEW_COMPLET_NEXTGENERATION.md`
- **Troubleshooting** : `ANALYSE_TECHNIQUE_FICHIERS.md`

### Contact

- **Issues GitHub** : Pour bugs et features
- **Documentation** : Tous les guides sont dans le repository
- **Logs** : Toujours joindre les logs pour le support

---

**🎉 Félicitations ! Votre environnement NextGeneration est prêt à l'emploi !**

*Testez, explorez, et développez avec l'assistance de vos agents IA !*
