# Agent PostgreSQL Docker Specialist - Gestion Conteneurs

## 1. Identification

- **Nom :** Agent PostgreSQL Docker Specialist
- **Identifiant :** `agent_POSTGRESQL_docker_specialist`
- **Version :** 2.0.0 (Harmonisé Pattern Factory)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#postgresql-team`

## 2. Description Générale

Agent spécialisé dans la gestion des conteneurs Docker PostgreSQL. Il assure l'inspection, la création, le démarrage, l'arrêt et la suppression des conteneurs, ainsi que la surveillance des logs pour garantir une infrastructure PostgreSQL robuste.

## 3. Objectifs et Missions

- **Gestion Conteneurs :** Création, démarrage, arrêt et suppression de conteneurs PostgreSQL
- **Inspection :** Analyse détaillée de l'état des conteneurs
- **Surveillance :** Monitoring des logs et de l'état de santé
- **Maintenance :** Opérations de maintenance sur les conteneurs
- **Orchestration :** Coordination avec les autres agents PostgreSQL

## 4. Capacités Techniques

### 4.1 Capacités Principales

```python
capabilities = [
    "inspect_container",
    "create_container",
    "start_container",
    "stop_container",
    "remove_container",
    "check_logs"
]
```

### 4.2 Types de Tâches Supportées

- **inspect_container :** Inspection détaillée d'un conteneur spécifique
- **create_container :** Création d'un nouveau conteneur PostgreSQL
- **start_container :** Démarrage d'un conteneur existant
- **stop_container :** Arrêt propre d'un conteneur
- **remove_container :** Suppression d'un conteneur
- **check_logs :** Analyse des logs du conteneur

## 5. Architecture et Implémentation

### 5.1 Héritage et Structure

```python
class AgentPostgresqlDockerSpecialist(AgentPostgreSQLBase):
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_docker",
            name="Agent Docker PostgreSQL"
        )
        self.docker_client = docker.from_env()
```

### 5.2 Pattern Factory

L'agent respecte intégralement le Pattern Factory avec :
- Interface `execute_task(task: Task) -> Result` async
- Héritage de `AgentPostgreSQLBase`
- Client Docker intégré pour toutes les opérations
- Gestion d'erreurs standardisée

## 6. Guide d'Utilisation

### 6.1 Instanciation

```python
from agents.agent_POSTGRESQL_docker_specialist import AgentPostgresqlDockerSpecialist
from core.agent_factory_architecture import Task

agent = AgentPostgresqlDockerSpecialist()
await agent.startup()
```

### 6.2 Inspection de Conteneur

```python
task = Task(
    type="inspect_container", 
    params={"container_name": "postgres-db"}
)
result = await agent.execute_task(task)
```

### 6.3 Création de Conteneur

```python
config = {
    "image": "postgres:13",
    "environment": {
        "POSTGRES_DB": "mydb",
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password"
    },
    "ports": {"5432/tcp": 5432}
}

task = Task(type="create_container", params={"config": config})
result = await agent.execute_task(task)
```

### 6.4 Gestion du Cycle de Vie

```python
# Démarrage
task = Task(type="start_container", params={"container_name": "postgres-db"})
await agent.execute_task(task)

# Arrêt
task = Task(type="stop_container", params={"container_name": "postgres-db"})
await agent.execute_task(task)

# Suppression
task = Task(type="remove_container", params={"container_name": "postgres-db"})
await agent.execute_task(task)
```

## 7. Configuration Docker

### 7.1 Images Supportées

- PostgreSQL 12, 13, 14, 15, 16
- Images officielles Docker Hub
- Images personnalisées avec extensions

### 7.2 Variables d'Environnement

- `POSTGRES_DB` : Nom de la base de données
- `POSTGRES_USER` : Utilisateur PostgreSQL
- `POSTGRES_PASSWORD` : Mot de passe
- `POSTGRES_INITDB_ARGS` : Arguments d'initialisation
- `PGDATA` : Répertoire des données

## 8. Tests et Validation

### 8.1 Tests CLI Disponibles

```bash
python tests/test_agents_postgresql_harmonisation.py
```

### 8.2 Health Check

```python
health = await agent.health_check()
# Retourne: {"status": "healthy", "agent": "Agent Docker PostgreSQL", ...}
```

## 9. Surveillance et Logs

### 9.1 Monitoring des Conteneurs

L'agent surveille automatiquement :
- État de santé des conteneurs
- Utilisation des ressources
- Logs d'erreur et d'avertissement

### 9.2 Analyse des Logs

```python
task = Task(type="check_logs", params={"container_name": "postgres-db"})
result = await agent.execute_task(task)
logs_data = result.data["logs"]
```

## 10. Sécurité et Bonnes Pratiques

### 10.1 Sécurité des Conteneurs

- Gestion sécurisée des mots de passe
- Isolation réseau appropriée
- Volumes persistants pour les données
- Sauvegarde régulière des données

### 10.2 Optimisation des Performances

- Configuration mémoire optimisée
- Paramètres PostgreSQL ajustés
- Monitoring des performances

## 11. Statut et Conformité

- **✅ Pattern Factory :** Conforme async
- **✅ Tests CLI :** Validés
- **✅ Documentation :** Synchronisée
- **✅ Harmonisation :** Terminée 2025-06-26

---

*Documentation mise à jour - Version 2.0.0 - Harmonisation Pattern Factory*