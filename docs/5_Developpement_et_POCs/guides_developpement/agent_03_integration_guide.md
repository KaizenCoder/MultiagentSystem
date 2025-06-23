# Guide d'Intgration Configuration Agent Factory

## [TARGET] Objectif
Configuration Pydantic centralise pour l'Agent Factory Pattern avec support multi-environnement et validation stricte.

## [CLIPBOARD] Composants Crs

### 1. Configuration Principal
- **Fichier:** `agent_config.py`
- **Description:** Modles Pydantic avec validation stricte
- **Classes principales:**
  - `AgentFactoryConfig` : Configuration principale
  - `EnvironmentConfig` : Configuration par environnement
  - `ConfigurationManager` : Gestionnaire singleton thread-safe

### 2. Fichiers Environnement
- **`.env.development`** : Configuration dveloppement (TTL: 60s)
- **`.env.staging`** : Configuration staging (TTL: 300s)
- **`.env.production`** : Configuration production (TTL: 600s)

### 3. Configuration JSON
- **Fichier:** `agent_config.json`
- **Description:** Configuration de base exportable

### 4. Tests
- **Fichier:** `tests/test_agent_config.py`
- **Coverage:** Validation Pydantic, environnements, singleton

## [ROCKET] Utilisation

### Import et Initialisation
```python
from agents.agent_config import config_manager, AgentFactoryConfig
import json

# Charger la configuration depuis JSON
with open('agents/agent_config.json') as f:
    config_data = json.load(f)

config = config_manager.load_config(config_data)
```

### Accs Configuration Environnement
```python
# Configuration environnement actuel
env_config = config.get_environment_config()
print(f"TTL: {env_config.ttl_seconds}s")
print(f"Threads: {env_config.thread_pool_size}")

# Configuration spcifique
prod_config = config.get_environment_config('production')
```

### Configuration Cache
```python
# TTL adaptatif selon environnement
ttl = config.get_cache_ttl()
thread_pool_size = config.get_thread_pool_size()

# Configuration cache
cache_config = config.cache
print(f"LRU activ: {cache_config.lru_enabled}")
print(f"Mmoire max: {cache_config.max_memory_mb}MB")
```

##  Scurit

### Variables d'Environnement
```bash
# Dveloppement
export ENVIRONMENT=development
export SECRET_KEY=your-dev-secret

# Production
export ENVIRONMENT=production
export SECRET_KEY=${PROD_SECRET_KEY}
export ENCRYPTION_KEY=${PROD_ENCRYPTION_KEY}
```

### Configuration Scurit
```python
security = config.security
print(f"Signature RSA: {security.signature_required}")
print(f"Cl RSA: {security.rsa_key_size} bits")
print(f"Hash: {security.hash_algorithm}")
```

## [CHART] Mtriques Intgration

### Agent 03 - Performance
- Configurations cres : 6
- Environnements configurs : 3
- Validations passes : 1
- Fonctionnalits scurit : 0

### Environnements Supports
| Environnement | TTL | Cache | Threads | Hot-Reload |
|---------------|-----|-------|---------|------------|
| Development   | 60s | 100   | 2       | [CHECK]         |
| Staging       | 300s| 500   | 4       | [CHECK]         |
| Production    | 600s| 1000  | 8       | [CROSS]         |

##  Tests

### Excution Tests
```bash
# Tests configuration
python -m pytest tests/test_agent_config.py -v

# Tests avec coverage
python -m pytest tests/test_agent_config.py --cov=agents.agent_config
```

### Validation Pydantic
```python
# Test validation environnement
env_config = EnvironmentConfig(
    ttl_seconds=300,
    cache_max_size=500,
    thread_pool_size=4,
    hot_reload=True,
    debug=False,
    log_level="INFO"
)
```

##  Intgration avec Autres Agents

### Agent 02 (Code Expert)
- Configuration utilise pour TTL cache
- Thread pool pour performance
- Validation stricte active

### Agent 05 (Tests)
- Configuration tests avec environnement ddi
- Validation environnements multiples

### Agent 06 (Monitoring)  
- Port Prometheus configur
- Mtriques actives selon environnement

## [LIGHTNING] Optimisations Performance

### TTL Adaptatif
- **Dveloppement:** 60s (tests rapides)
- **Staging:** 300s (quilibre test/perf)
- **Production:** 600s (performance optimale)

### Pool Threads
- Auto-ajustement selon CPU disponible
- Maximum 2  CPU cores
- Configuration par environnement

### Cache LRU
- Compression active (Zstandard)
- Nettoyage automatique
- Limitation mmoire configurable

## [TARGET] Statut Intgration

**[CHECK] CONFIGURATION PYDANTIC CENTRALISE OPRATIONNELLE**

- Configuration multi-environnement : [CHECK]
- Validation Pydantic stricte : [CHECK]  
- Gestionnaire singleton thread-safe : [CHECK]
- Variables environnement scurises : [CHECK]
- Tests complets avec coverage : [CHECK]
- Documentation intgration : [CHECK]
- Performance optimise : [CHECK]

**Cr par Agent 03 - Spcialiste Configuration**
**Date:** 2025-06-23 17:52:14
