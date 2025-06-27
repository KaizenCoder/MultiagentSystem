# Agent PostgreSQL Diagnostic - Résolution Définitive Encodage

## 1. Identification

- **Nom :** Agent PostgreSQL Diagnostic Final
- **Identifiant :** `agent_POSTGRESQL_diagnostic_postgres_final`
- **Version :** 2.0.0 (Harmonisé Pattern Factory)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#postgresql-team`

## 2. Description Générale

Agent spécialisé dans le diagnostic et la résolution définitive des problèmes PostgreSQL, particulièrement les problèmes d'encodage UTF-8. Il analyse les conteneurs Docker, diagnostique les configurations Python/psycopg2 et propose des solutions complètes.

## 3. Objectifs et Missions

- **Diagnostic Conteneur :** Analyser l'état des conteneurs PostgreSQL Docker
- **Diagnostic Encodage :** Détecter et résoudre les problèmes d'encodage UTF-8
- **Diagnostic Python :** Vérifier la configuration psycopg2 et les variables d'environnement
- **Génération Solutions :** Proposer des corrections définitives
- **Reporting :** Produire des rapports détaillés de diagnostic

## 4. Capacités Techniques

### 4.1 Capacités Principales

```python
capabilities = [
    "diagnostic_conteneur",
    "diagnostic_encodage", 
    "diagnostic_python",
    "generation_solution",
    "execution_mission"
]
```

### 4.2 Types de Tâches Supportées

- **diagnostic_complet :** Exécution de la mission complète de diagnostic
- **diagnostic_conteneur :** Analyse spécifique des conteneurs PostgreSQL
- **diagnostic_encodage :** Diagnostic encodage sur un conteneur spécifique
- **diagnostic_python :** Vérification configuration Python/psycopg2
- **generer_solution :** Génération de solutions d'encodage définitives

## 5. Architecture et Implémentation

### 5.1 Héritage et Structure

```python
class AgentPostgresqlDiagnosticPostgresFinal(AgentPostgreSQLBase):
    def __init__(self, workspace_root: Path = None):
        super().__init__(
            agent_type="postgresql_diagnostic",
            name="Agent Diagnostic PostgreSQL"
        )
```

### 5.2 Pattern Factory

L'agent respecte intégralement le Pattern Factory avec :
- Interface `execute_task(task: Task) -> Result` async
- Héritage de `AgentPostgreSQLBase` 
- Méthodes async pour toutes les opérations
- Gestion d'erreurs standardisée

## 6. Guide d'Utilisation

### 6.1 Instanciation

```python
from agents.agent_POSTGRESQL_diagnostic_postgres_final import AgentPostgresqlDiagnosticPostgresFinal
from core.agent_factory_architecture import Task

agent = AgentPostgresqlDiagnosticPostgresFinal()
await agent.startup()
```

### 6.2 Diagnostic Complet

```python
task = Task(type="diagnostic_complet", params={})
result = await agent.execute_task(task)
print(f"Statut: {result.success}")
print(f"Données: {result.data}")
```

### 6.3 Diagnostic Conteneur Spécifique

```python
task = Task(
    type="diagnostic_encodage", 
    params={"container_name": "postgres_container"}
)
result = await agent.execute_task(task)
```

## 7. Structure des Résultats

### 7.1 Rapport Data Structure

```python
rapport_data = {
    "agent": "Agent Diagnostic PostgreSQL",
    "version": "2.0.0",
    "mission": "Résolution définitive encodage PostgreSQL",
    "timestamp": "2025-06-27T...",
    "diagnostics": [],
    "solutions": [],
    "status": "SUCCESS|FAILED"
}
```

### 7.2 Métriques de Performance

Les résultats incluent des métriques détaillées :
- `diagnostics_count` : Nombre de diagnostics effectués
- `solutions_count` : Nombre de solutions proposées

## 8. Tests et Validation

### 8.1 Tests CLI Disponibles

L'agent est validé via le script de tests :
```bash
python tests/test_agents_postgresql_harmonisation.py
```

### 8.2 Health Check

```python
health = await agent.health_check()
# Retourne: {"status": "healthy", "agent": "...", "timestamp": "..."}
```

## 9. Configuration et Personnalisation

### 9.1 Variables d'Environnement Analysées

- `PYTHONIOENCODING`
- `PYTHONUTF8` 
- `LANG`
- `LC_ALL`

### 9.2 Conteneurs Docker Supportés

L'agent peut diagnostiquer tous les conteneurs PostgreSQL actifs et analyser leur configuration d'encodage.

## 10. Statut et Conformité

- **✅ Pattern Factory :** Conforme async
- **✅ Tests CLI :** Validés 
- **✅ Documentation :** Synchronisée
- **✅ Harmonisation :** Terminée 2025-06-26

---

*Documentation mise à jour - Version 2.0.0 - Harmonisation Pattern Factory*