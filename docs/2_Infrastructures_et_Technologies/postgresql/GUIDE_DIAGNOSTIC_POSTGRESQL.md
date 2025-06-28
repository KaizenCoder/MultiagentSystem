# Guide de Diagnostic PostgreSQL - NextGeneration

## 🎯 Vue d'ensemble

L'agent de diagnostic PostgreSQL NextGeneration est un outil autonome qui utilise l'orchestrateur pour diagnostiquer automatiquement les problèmes courants de PostgreSQL et proposer des solutions basées sur une base de connaissances.

## 🚀 Utilisation

### Lancement du diagnostic

```bash
# Diagnostic avec affichage formaté
python postgresql_diagnostic_agent.py

# Diagnostic avec sortie JSON
python postgresql_diagnostic_agent.py --json
```

### Prérequis

- L'orchestrateur NextGeneration doit être configuré
- Docker doit être installé et accessible
- Un conteneur PostgreSQL nommé `postgres` doit être en cours d'exécution
- Les outils `psql` et `pg_isready` doivent être disponibles

## 🔍 Tests de Diagnostic

L'agent exécute automatiquement les tests suivants :

### 1. Vérification de la disponibilité PostgreSQL
- **Objectif** : Vérifier si PostgreSQL répond aux connexions
- **Outils utilisés** : `pg_isready`, `docker ps`
- **Problèmes détectés** :
  - Service PostgreSQL arrêté
  - Problèmes de connectivité réseau
  - Conteneur Docker non démarré

### 2. Vérification des connexions actives
- **Objectif** : Analyser le nombre de connexions actives
- **Requêtes SQL** : `pg_stat_activity`
- **Problèmes détectés** :
  - Trop de connexions actives
  - Connexions bloquées
  - Répartition des connexions par base de données

### 3. Vérification de l'espace disque
- **Objectif** : Contrôler l'espace disque disponible
- **Outils utilisés** : `df`, requêtes sur `pg_database_size`
- **Problèmes détectés** :
  - Espace disque insuffisant
  - Bases de données trop volumineuses
  - Croissance rapide des données

### 4. Vérification des logs d'erreur
- **Objectif** : Analyser les logs récents pour détecter les erreurs
- **Outils utilisés** : `docker logs`
- **Problèmes détectés** :
  - Erreurs fatales (FATAL)
  - Erreurs générales (ERROR)
  - Limite de connexions dépassée
  - Problèmes de mémoire
  - Checkpoints lents

### 5. Vérification de la configuration
- **Objectif** : Examiner les paramètres de configuration critiques
- **Paramètres vérifiés** :
  - `max_connections`
  - `shared_buffers`
  - `effective_cache_size`
  - `maintenance_work_mem`
  - `checkpoint_completion_target`
  - `wal_buffers`
  - `default_statistics_target`

### 6. Vérification des performances
- **Objectif** : Analyser les métriques de performance
- **Données collectées** :
  - Requêtes lentes (pg_stat_statements)
  - Statistiques des tables (pg_stat_user_tables)
  - Activité des index

## 📊 Rapport de Diagnostic

Le rapport généré contient :

### Résumé Exécutif
- Nombre total de tests exécutés
- Tests réussis vs échoués
- Problèmes critiques identifiés
- Avertissements

### Résultats Détaillés
- Sortie complète de chaque test
- Données brutes collectées
- Métriques de performance

### Recommandations
- Solutions trouvées dans la base de connaissances
- Actions recommandées
- Liens vers la documentation

### Actions Prioritaires
- Liste des actions à effectuer immédiatement
- Ordre de priorité
- Impact estimé

## 🛠️ Problèmes Courants et Solutions

### Problème : PostgreSQL indisponible
**Symptômes** :
- `pg_isready` retourne une erreur
- Impossible de se connecter

**Solutions** :
```bash
# Redémarrer le conteneur
docker restart postgres

# Vérifier les logs
docker logs postgres

# Vérifier la configuration réseau
docker inspect postgres
```

### Problème : Trop de connexions actives
**Symptômes** :
- Erreur "too many connections"
- Performance dégradée

**Solutions** :
```sql
-- Augmenter max_connections
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();

-- Identifier les connexions inactives
SELECT pid, state, query_start, query 
FROM pg_stat_activity 
WHERE state = 'idle in transaction';

-- Fermer les connexions inactives
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle in transaction' 
AND query_start < NOW() - INTERVAL '1 hour';
```

### Problème : Espace disque insuffisant
**Symptômes** :
- Erreurs d'écriture
- Base de données en lecture seule

**Solutions** :
```bash
# Nettoyer les logs anciens
docker exec postgres find /var/lib/postgresql/data/log -name "*.log" -mtime +7 -delete

# Analyser l'utilisation de l'espace
docker exec postgres du -sh /var/lib/postgresql/data/*

# Vacuum des tables volumineuses
docker exec postgres psql -U postgres -c "VACUUM FULL;"
```

### Problème : Requêtes lentes
**Symptômes** :
- Temps de réponse élevé
- CPU élevé

**Solutions** :
```sql
-- Activer pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Identifier les requêtes lentes
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Analyser les index manquants
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public'
AND n_distinct > 100;
```

## 🔧 Configuration Avancée

### Variables d'environnement
```bash
# Configuration de l'orchestrateur
export ORCHESTRATOR_API_KEY="your-api-key"
export MEMORY_API_URL="http://localhost:8001"

# Configuration PostgreSQL
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_USER="postgres"
export POSTGRES_DB="postgres"
```

### Personnalisation des tests
Vous pouvez modifier le fichier `postgresql_diagnostic_agent.py` pour :
- Ajouter de nouveaux tests
- Modifier les seuils d'alerte
- Personnaliser les recommandations
- Intégrer d'autres outils de monitoring

## 📈 Intégration avec le Monitoring

### Automatisation
```bash
# Exécution périodique avec cron
# Ajouter dans crontab -e :
0 */6 * * * /usr/bin/python3 /path/to/postgresql_diagnostic_agent.py --json > /var/log/postgresql_diagnostic.json

# Intégration avec Prometheus
# Le rapport JSON peut être parsé par un exporter personnalisé
```

### Alertes
```bash
# Exemple de script d'alerte basé sur le rapport
#!/bin/bash
REPORT=$(python3 postgresql_diagnostic_agent.py --json)
CRITICAL_ISSUES=$(echo $REPORT | jq '.diagnostic_summary.critical_issues | length')

if [ $CRITICAL_ISSUES -gt 0 ]; then
    echo "ALERTE: $CRITICAL_ISSUES problèmes critiques détectés"
    # Envoyer notification (email, Slack, etc.)
fi
```

## 🔒 Sécurité

L'agent utilise les outils sécurisés de l'orchestrateur :
- Validation des commandes shell
- Sanitisation des entrées
- Logging sécurisé
- Gestion des erreurs

### Commandes autorisées
- `psql` : Requêtes SQL
- `pg_isready` : Test de disponibilité
- `docker` : Gestion des conteneurs
- `echo` : Affichage de messages

## 🐛 Dépannage

### Erreur : "Command not allowed for security reasons"
**Cause** : Commande non autorisée par la whitelist de sécurité
**Solution** : Modifier la liste `allowed_commands` dans `tools.py`

### Erreur : "Memory API connection failed"
**Cause** : API de mémoire indisponible
**Solution** : Vérifier que l'API de mémoire est démarrée

### Erreur : "Docker command failed"
**Cause** : Docker non accessible ou conteneur inexistant
**Solution** : 
```bash
# Vérifier Docker
docker ps

# Vérifier le conteneur PostgreSQL
docker ps --filter name=postgres
```

## 📚 Ressources Supplémentaires

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Guide de performance PostgreSQL](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Monitoring PostgreSQL](https://www.postgresql.org/docs/current/monitoring.html)
- [Troubleshooting PostgreSQL](https://wiki.postgresql.org/wiki/Troubleshooting)

## 🤝 Contribution

Pour contribuer à l'amélioration de l'agent de diagnostic :
1. Identifier de nouveaux tests à ajouter
2. Proposer des améliorations des analyses
3. Enrichir la base de connaissances
4. Optimiser les performances

---

*Agent de diagnostic PostgreSQL NextGeneration - Version 1.0* 