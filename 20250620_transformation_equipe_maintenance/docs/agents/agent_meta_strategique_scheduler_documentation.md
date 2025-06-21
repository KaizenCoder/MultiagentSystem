# 📋 Documentation Agent: agent_meta_strategique_scheduler

## 🎯 Informations Générales

- **Nom**: agent_meta_strategique_scheduler
- **Modèle**: Unknown
- **Mission**: Exécuter périodiquement l'analyse stratégique et générer les rapports
- **Type**: Agent NextGeneration

## 🏗️ Architecture

### Classes Principales
- `AgentMetaStrategiqueScheduler`

### Fonctions Clés
- `__init__()`
- `load_config()`
- `save_config()`
- `start_scheduler()`
- `setup_schedules()`
- `execute_daily_analysis()`
- `execute_weekly_deep_analysis()`
- `execute_critical_monitoring()`
- `check_critical_metrics()`
- `handle_critical_insights()`

## 📦 Dépendances

### Imports
```python
import asyncio
import json
import logging
import schedule
import time
```

## 🚀 Utilisation

### Instanciation
```python
agent = AgentMetaStrategiqueScheduler()
```

### Exécution
```python
# Démarrage
await agent.startup()

# Exécution mission
resultats = await agent.mission_principale()

# Arrêt
await agent.shutdown()
```

## 📊 Métriques

- **Classes définies**: 1
- **Fonctions disponibles**: 17
- **Modules importés**: 13

## 📝 Notes

Cette documentation a été générée automatiquement par l'Agent 5 Documenteur.

---
*Généré le 2025-06-20 23:25:54 par Agent 5 Documenteur*
