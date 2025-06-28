# 📚 DOCUMENTATION API COMPLÈTE - LOGGING NEXTGENERATION

## 🎯 Vue d'Ensemble

Le système de logging NextGeneration offre une API unifiée et puissante pour la gestion centralisée des logs. Cette documentation présente toutes les APIs publiques, leurs paramètres, exemples d'utilisation et bonnes pratiques.

## 🚀 APIs Principales

### 🔧 LoggingManager - Gestionnaire Principal

Le `LoggingManager` est le point d'entrée principal du système (pattern Singleton).

#### Initialisation

```python
from logging_manager_optimized import LoggingManager

# Obtenir l'instance unique
manager = LoggingManager()

# Le manager se configure automatiquement au premier accès
```

#### `get_logger(config_name, custom_config)` - API Principale

**Description** : Obtient un logger configuré selon les spécifications.

**Paramètres** :
- `config_name` (str, optionnel) : Nom de configuration prédéfinie
- `custom_config` (dict, optionnel) : Configuration personnalisée

**Retour** : `logging.Logger` configuré

```python
# Logger simple
logger = manager.get_logger()

# Logger avec configuration personnalisée
config = {
    "logger_name": "nextgen.api",
    "log_level": "DEBUG",
    "console_enabled": True,
    "file_enabled": True,
    "elasticsearch_enabled": True,
    "encryption_enabled": True
}
logger = manager.get_logger(custom_config=config)

# Logger avec configuration prédéfinie
logger = manager.get_logger(config_name="agent_default")
```

#### `get_agent_logger(agent_name, role, domain, agent_id, async_enabled)` - API Agents

**Description** : Crée un logger spécialisé pour les agents avec métadonnées enrichies.

**Paramètres** :
- `agent_name` (str) : Nom de l'agent
- `role` (str) : Rôle de l'agent
- `domain` (str) : Domaine d'expertise
- `agent_id` (str, optionnel) : Identifiant unique
- `async_enabled` (bool, défaut: False) : Mode asynchrone

**Retour** : `logging.Logger` spécialisé agent

```python
# Logger agent simple
agent_logger = manager.get_agent_logger(
    agent_name="coordinateur_principal",
    role="coordination",
    domain="factory_pattern"
)

# Logger agent avec ID et mode async
agent_logger = manager.get_agent_logger(
    agent_name="analyseur_code",
    role="analysis",
    domain="refactoring",
    agent_id="agent_001",
    async_enabled=True
)

# Utilisation
agent_logger.info("Démarrage de l'analyse", extra={
    "operation": "code_analysis",
    "target": "logging_manager.py"
})
```

#### `create_audit_logger(user_id, action_type)` - API Audit

**Description** : Crée un logger d'audit avec traçabilité utilisateur.

**Paramètres** :
- `user_id` (str) : Identifiant utilisateur
- `action_type` (str) : Type d'action auditée

**Retour** : `logging.Logger` avec adapter d'audit

```python
# Logger d'audit
audit_logger = manager.create_audit_logger(
    user_id="admin_001",
    action_type="configuration_change"
)

# Utilisation automatique des métadonnées d'audit
audit_logger.warning("Modification configuration sécurité", extra={
    "config_section": "encryption",
    "old_value": "disabled",
    "new_value": "enabled"
})
```

#### `get_performance_logger()` - API Performance

**Description** : Obtient un logger spécialisé pour les métriques de performance.

**Retour** : `logging.Logger` optimisé performance

```python
# Logger performance
perf_logger = manager.get_performance_logger()

# Logging de métriques
perf_logger.info("Performance mesurée", extra={
    "operation": "elasticsearch_batch",
    "duration_ms": 45.2,
    "records_processed": 1000,
    "throughput_rps": 22123
})
```

### 📊 Context Manager Performance

#### `log_performance(operation_name, logger)` - Mesure Automatique

**Description** : Context manager pour mesurer automatiquement les performances.

**Paramètres** :
- `operation_name` (str) : Nom de l'opération
- `logger` (logging.Logger, optionnel) : Logger à utiliser

```python
# Mesure automatique avec logger par défaut
with manager.log_performance("database_query"):
    result = execute_complex_query()

# Mesure avec logger personnalisé
with manager.log_performance("file_processing", custom_logger):
    process_large_file("data.csv")

# Mesure avec métadonnées additionnelles
with manager.log_performance("api_call") as perf_context:
    response = api_client.get("/users")
    perf_context.add_metadata({
        "status_code": response.status_code,
        "response_size": len(response.content)
    })
```

### 📈 APIs de Métriques

#### `get_metrics()` - Métriques Globales

**Description** : Obtient toutes les métriques du système de logging.

**Retour** : `Dict[str, Any]` avec métriques complètes

```python
metrics = manager.get_metrics()

# Structure des métriques
{
    "total_logs": 15847,
    "logs_per_level": {
        "DEBUG": 5234,
        "INFO": 8456,
        "WARNING": 1823,
        "ERROR": 298,
        "CRITICAL": 36
    },
    "performance_stats": {
        "avg_processing_time_ms": 2.3,
        "max_processing_time_ms": 45.1,
        "total_processing_time_ms": 36447.2
    },
    "elasticsearch_stats": {...},
    "security_stats": {...}
}
```

#### `get_advanced_monitoring_metrics()` - Métriques Monitoring

**Description** : Métriques détaillées du système de monitoring avancé.

```python
monitoring_metrics = manager.get_advanced_monitoring_metrics()

# Métriques OpenTelemetry et performance
{
    "tracing_enabled": True,
    "spans_created": 1547,
    "metrics_exported": 2341,
    "performance_alerts": 12,
    "avg_span_duration_ms": 15.7
}
```

#### `get_elasticsearch_metrics()` - Métriques Elasticsearch

**Description** : Métriques spécifiques à l'intégration Elasticsearch.

```python
es_metrics = manager.get_elasticsearch_metrics()

# Métriques cache, compression, performance
{
    "documents_sent": 8456,
    "cache_hit_rate": 73.2,
    "compression_efficiency": 68.4,
    "connection_pool_utilization": 45.2,
    "avg_batch_size": 12.3
}
```

#### `get_security_metrics()` - Métriques Sécurité

**Description** : Métriques de sécurité et chiffrement.

```python
security_metrics = manager.get_security_metrics()

# Métriques chiffrement, rotation clés, détection
{
    "encrypted_logs": 3421,
    "key_rotations": 5,
    "sensitive_data_detections": 156,
    "security_violations": 0,
    "current_key_age_hours": 18.5
}
```

## ⚙️ Configuration Avancée

### LoggingConfig - Classe de Configuration

**Description** : Dataclass pour configuration complète d'un logger.

```python
from logging_manager_optimized import LoggingConfig

# Configuration complète
config = LoggingConfig(
    # Configuration de base
    logger_name="nextgen.advanced",
    log_level="INFO",
    log_dir="logs/advanced",
    filename_pattern="{component}_{date}.log",
    max_file_size=50 * 1024 * 1024,  # 50MB
    backup_count=10,
    console_enabled=True,
    file_enabled=True,
    
    # Configuration avancée
    async_enabled=True,
    compression_enabled=True,
    retention_days=30,
    
    # Elasticsearch
    elasticsearch_enabled=True,
    elasticsearch_host="localhost:9200",
    elasticsearch_index="nextgen-advanced",
    elasticsearch_cache_enabled=True,
    elasticsearch_cache_size=1000,
    elasticsearch_compression_enabled=True,
    elasticsearch_connection_pool_size=5,
    
    # Sécurité
    encryption_enabled=True,
    encryption_key="your-32-byte-key-here",
    key_rotation_hours=24,
    max_keys_history=5,
    enhanced_sensitive_detection=True,
    sensitive_data_masking=True,
    
    # Alertes
    alerting_enabled=True,
    alert_email="admin@company.com",
    alert_webhook="https://hooks.slack.com/webhook",
    
    # Monitoring
    advanced_monitoring_enabled=True
)

logger = manager.get_logger(custom_config=config.__dict__)
```

### Configuration par Environnement

```python
# Configuration développement
dev_config = {
    "log_level": "DEBUG",
    "console_enabled": True,
    "file_enabled": True,
    "elasticsearch_enabled": False,
    "encryption_enabled": False
}

# Configuration production
prod_config = {
    "log_level": "INFO",
    "console_enabled": False,
    "file_enabled": True,
    "elasticsearch_enabled": True,
    "encryption_enabled": True,
    "alerting_enabled": True,
    "advanced_monitoring_enabled": True
}

# Configuration test
test_config = {
    "log_level": "WARNING",
    "console_enabled": True,
    "file_enabled": False,
    "elasticsearch_enabled": False
}
```

## 🎨 Handlers Spécialisés

### AsyncLogHandler - Logging Asynchrone

**Description** : Handler haute performance avec traitement asynchrone par batch.

```python
# Configuration automatique via LoggingConfig
config = {
    "async_enabled": True,
    "logger_name": "async_logger"
}
async_logger = manager.get_logger(custom_config=config)

# Le handler async est configuré automatiquement
async_logger.info("Message traité de façon asynchrone")
```

### ElasticsearchHandler - Intégration Elasticsearch

**Fonctionnalités** :
- Cache intelligent MD5
- Compression GZIP
- Pool de connexions
- Métriques temps réel

```python
# Configuration Elasticsearch optimisée
es_config = {
    "elasticsearch_enabled": True,
    "elasticsearch_host": "cluster.elastic.com:9200",
    "elasticsearch_index": "production-logs",
    "elasticsearch_cache_enabled": True,
    "elasticsearch_compression_enabled": True
}
```

### EncryptionHandler - Chiffrement Avancé

**Fonctionnalités** :
- Chiffrement Fernet
- Rotation automatique des clés
- Détection de données sensibles
- Historique sécurisé des clés

```python
# Configuration chiffrement
crypto_config = {
    "encryption_enabled": True,
    "encryption_key": "your-secure-key",
    "key_rotation_hours": 12,  # Rotation toutes les 12h
    "enhanced_sensitive_detection": True
}
```

### AlertingHandler - Système d'Alertes

**Fonctionnalités** :
- Alertes email SMTP
- Webhooks (Slack, Teams, etc.)
- Cooldown anti-spam
- Filtrage intelligent

```python
# Configuration alertes
alert_config = {
    "alerting_enabled": True,
    "alert_email": "ops@company.com",
    "alert_webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
}
```

## 🏗️ Architecture et Patterns

### Pattern Singleton

Le `LoggingManager` utilise le pattern Singleton thread-safe :

```python
# Toujours la même instance
manager1 = LoggingManager()
manager2 = LoggingManager()
assert manager1 is manager2  # True
```

### Pattern Factory

Le manager agit comme une factory pour les loggers :

```python
# Création automatique selon configuration
logger_a = manager.get_logger(config_name="type_a")
logger_b = manager.get_logger(config_name="type_b")
agent_logger = manager.get_agent_logger("agent", "role", "domain")
```

### Pattern Observer

Système de métriques avec observation des événements :

```python
# Les métriques sont automatiquement mises à jour
logger.info("Message")  # → met à jour total_logs, logs_per_level, etc.
```

## 🚨 Gestion d'Erreurs

### Fallbacks Automatiques

Le système intègre des fallbacks robustes :

```python
# Si Elasticsearch échoue → fallback vers fichier
# Si chiffrement échoue → fallback vers texte clair avec alerte
# Si async échoue → fallback vers synchrone
```

### Logging des Erreurs Internes

```python
# Les erreurs du système de logging sont capturées
# et loggées dans un logger interne séparé
internal_logger = manager._internal_logger
```

## 📋 Exemples d'Usage Complets

### Application Web

```python
# Configuration pour API web
web_config = {
    "logger_name": "nextgen.web.api",
    "log_level": "INFO",
    "elasticsearch_enabled": True,
    "alerting_enabled": True,
    "advanced_monitoring_enabled": True
}

web_logger = manager.get_logger(custom_config=web_config)

# Logging structuré pour API
@app.route('/users/<user_id>')
def get_user(user_id):
    with manager.log_performance("get_user_api"):
        web_logger.info("API call", extra={
            "endpoint": "/users/{user_id}",
            "user_id": user_id,
            "method": "GET"
        })
        
        try:
            user = database.get_user(user_id)
            web_logger.info("User retrieved", extra={
                "user_id": user_id,
                "found": True
            })
            return jsonify(user)
        except UserNotFound:
            web_logger.warning("User not found", extra={
                "user_id": user_id,
                "found": False
            })
            return jsonify({"error": "User not found"}), 404
```

### Agent d'IA

```python
# Logger spécialisé pour agent
agent_logger = manager.get_agent_logger(
    agent_name="code_analyzer",
    role="analysis",
    domain="software_engineering",
    agent_id="agent_001",
    async_enabled=True
)

class CodeAnalyzer:
    def __init__(self):
        self.logger = agent_logger
    
    def analyze_file(self, filepath):
        self.logger.info("Starting file analysis", extra={
            "filepath": filepath,
            "operation": "analyze_file"
        })
        
        with manager.log_performance("file_analysis", self.logger):
            # Analyse du fichier
            results = self._perform_analysis(filepath)
            
            self.logger.info("Analysis completed", extra={
                "filepath": filepath,
                "issues_found": len(results.issues),
                "complexity_score": results.complexity
            })
            
            return results
```

### Système de Batch

```python
# Configuration pour traitement batch
batch_config = {
    "logger_name": "nextgen.batch.processor",
    "async_enabled": True,
    "elasticsearch_enabled": True,
    "compression_enabled": True
}

batch_logger = manager.get_logger(custom_config=batch_config)

def process_batch(items):
    batch_logger.info("Batch processing started", extra={
        "batch_size": len(items),
        "operation": "process_batch"
    })
    
    processed = 0
    errors = 0
    
    for item in items:
        try:
            with manager.log_performance("process_item"):
                process_item(item)
                processed += 1
        except Exception as e:
            batch_logger.error("Item processing failed", extra={
                "item_id": item.id,
                "error": str(e)
            })
            errors += 1
    
    batch_logger.info("Batch processing completed", extra={
        "total_items": len(items),
        "processed": processed,
        "errors": errors,
        "success_rate": processed / len(items) * 100
    })
```

## 🔍 Debugging et Diagnostics

### Mode Debug

```python
# Activation du debug
debug_config = {
    "log_level": "DEBUG",
    "console_enabled": True
}
debug_logger = manager.get_logger(custom_config=debug_config)

# Informations de debug détaillées
debug_logger.debug("Variable state", extra={
    "variables": {"x": 42, "y": "hello"},
    "function": "process_data",
    "line": 156
})
```

### Métriques de Diagnostic

```python
# Diagnostic complet du système
def system_health_check():
    metrics = manager.get_metrics()
    es_metrics = manager.get_elasticsearch_metrics()
    security_metrics = manager.get_security_metrics()
    
    health = {
        "logging_system": "healthy" if metrics["errors_count"] == 0 else "degraded",
        "elasticsearch": "healthy" if es_metrics["elasticsearch_errors"] == 0 else "degraded",
        "security": "healthy" if security_metrics["security_violations"] == 0 else "alert"
    }
    
    return health
```

## 🎯 Bonnes Pratiques

### Structuration des Logs

```python
# ✅ Bon : logs structurés avec extra
logger.info("User login successful", extra={
    "user_id": "user_123",
    "ip_address": "192.168.1.100",
    "session_id": "sess_abc123"
})

# ❌ Éviter : logs non structurés
logger.info(f"User {user_id} logged in from {ip}")
```

### Gestion des Niveaux

```python
# DEBUG : Informations détaillées pour développement
logger.debug("Variable values", extra={"vars": locals()})

# INFO : Événements normaux d'application
logger.info("Process completed successfully")

# WARNING : Situations anormales mais récupérables
logger.warning("API rate limit approaching", extra={"current_rate": 95})

# ERROR : Erreurs qui affectent une opération
logger.error("Database connection failed", extra={"db_host": "localhost"})

# CRITICAL : Erreurs qui peuvent arrêter l'application
logger.critical("Out of memory", extra={"memory_usage": "99%"})
```

### Performance

```python
# ✅ Bon : utiliser le context manager
with manager.log_performance("expensive_operation"):
    result = expensive_computation()

# ✅ Bon : logging asynchrone pour haute charge
config = {"async_enabled": True}
high_volume_logger = manager.get_logger(custom_config=config)
```

## 🔒 Sécurité

### Données Sensibles

Le système détecte automatiquement et masque :
- Mots de passe
- Clés API
- Numéros de carte de crédit
- Emails
- Adresses IP
- Tokens d'authentification

```python
# Automatiquement masqué
logger.info("User authentication", extra={
    "password": "secret123",  # → "password": "***MASKED***"
    "api_key": "sk-1234567890abcdef"  # → "api_key": "***MASKED***"
})
```

### Chiffrement

```python
# Configuration chiffrement recommandée
secure_config = {
    "encryption_enabled": True,
    "key_rotation_hours": 24,
    "enhanced_sensitive_detection": True
}
```

## 📊 Monitoring Production

### Métriques Clés

```python
# Vérifications régulières recommandées
def monitor_logging_health():
    metrics = manager.get_metrics()
    
    # Vérifier les erreurs
    if metrics["errors_count"] > 100:
        alert("High error count in logging system")
    
    # Vérifier les performances
    if metrics["performance_stats"]["avg_processing_time_ms"] > 50:
        alert("Logging performance degraded")
    
    # Vérifier Elasticsearch
    es_metrics = manager.get_elasticsearch_metrics()
    if es_metrics["cache_hit_rate"] < 50:
        alert("Elasticsearch cache efficiency low")
```

### Alertes Recommandées

- Taux d'erreur > 1%
- Temps de traitement > 100ms
- Cache hit rate < 60%
- Violations de sécurité > 0
- Espace disque < 10%

---

## 📚 Référence Rapide

### Import Principal
```python
from logging_manager_optimized import LoggingManager
```

### APIs Essentielles
```python
manager = LoggingManager()
logger = manager.get_logger(custom_config=config)
agent_logger = manager.get_agent_logger(name, role, domain)
metrics = manager.get_metrics()
```

### Configuration Minimale
```python
config = {"logger_name": "my_app", "log_level": "INFO"}
```

### Configuration Production
```python
config = {
    "logger_name": "production_app",
    "elasticsearch_enabled": True,
    "encryption_enabled": True,
    "alerting_enabled": True,
    "advanced_monitoring_enabled": True
}
```

---

*Documentation générée pour NextGeneration Logging System v1.1.0*
*Dernière mise à jour : 2025-06-20* 