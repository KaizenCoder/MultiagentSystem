# Agent MAINTENANCE 00 – Chef d'Équipe Coordinateur Enterprise

## 1. Identification

- **Nom :** Chef d'Équipe Coordinateur Enterprise
- **Identifiant :** `agent_MAINTENANCE_00_chef_equipe_coordinateur`
- **Version :** 4.3.0 (Harmonisation Standards Pattern Factory NextGeneration)
- **Responsable Principal :** Équipe de Maintenance NextGeneration
- **Contact Technique :** `#canal-maintenance-ia`

## 2. Description Générale

🎖️ Agent spécialisé dans l'orchestration centrale de l'équipe de maintenance NextGeneration. Responsable de la coordination des workflows complexes avec boucle de réparation itérative et génération de rapports stratégiques détaillés.

Cet agent supervise une équipe de 12 agents spécialisés pour garantir la maintenance automatisée et la réparation intelligente du code source.

## 3. Objectifs et Missions

- **Orchestration d'Équipe :** Coordination centrale de 12 agents de maintenance spécialisés
- **Boucle de Réparation Itérative :** Système intelligent de réparation avec classification d'erreurs (max 5 tentatives)
- **Workflow Séquentiel :** Analyse → Adaptation → Test → Validation
- **Reporting Mission :** Génération de rapports complets (JSON + Markdown)
- **Monitoring Temps Réel :** Surveillance de santé d'équipe et métriques de performance

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory NextGeneration et expose les méthodes suivantes :

- **`startup()`** : Initialise l'agent et recrute automatiquement l'équipe de maintenance (12 agents)
- **`health_check()`** : Vérifie l'état de santé de l'agent et de toute son équipe. Retourne `{"status": "healthy"}` si tous les agents sont opérationnels
- **`execute_task(task: Task)`** : Point d'entrée principal pour les missions de maintenance
  - **Action `workflow_maintenance_complete`** :
    - **`task.params` attendus** :
      - `target_files` (List[str]) : Liste des chemins vers les agents/fichiers à traiter
    - **Résultat** : Rapport complet de mission avec statuts détaillés par agent
- **`shutdown()`** : Arrête l'agent et toute son équipe de manière propre

### Capacités Spécialisées

```python
get_capabilities() -> [
    "workflow_maintenance_complete",
    "orchestration_equipe_maintenance", 
    "boucle_reparation_iterative",
    "coordination_agents_maintenance",
    "reporting_mission_json_md"
]
```

## 5. Architecture et Workflow

### Équipe Coordonnée (12 Agents)

1. **analyseur_structure** - Analyse de structure de code
2. **evaluateur** - Évaluation de qualité et utilité
3. **correcteur_semantique** - Correction sémantique
4. **adaptateur** - Adaptation de code intelligente
5. **testeur** - Tests et validation
6. **documenteur** - Génération de documentation
7. **analyseur_performance** - Analyse de performance
8. **dependency_manager** - Gestion des dépendances
9. **security_manager** - Sécurité et audit
10. **correcteur_logique** - Correction logique métier
11. **auditeur_qualite** - Audit qualité et normes
12. **harmonisateur_style** - Harmonisation de style

### Workflow de Maintenance

```
1. 🚀 Startup → Recrutement équipe
2. 📋 Analyse mission_config (target_files)
3. 🔁 Pour chaque fichier :
   a. 📖 Lecture code source
   b. 🧪 Test initial
   c. Si échec → Boucle réparation (max 5×)
      - Classification erreur
      - Adaptation par agent spécialisé
      - Re-test
   d. ✅ Validation finale
4. 📊 Génération rapports (JSON + MD)
5. 🛑 Shutdown équipe
```

### Boucle de Réparation Intelligente

- **Classification automatique** des erreurs (indentation, import, name, generic)
- **Stratégie adaptée** selon le type d'erreur détecté
- **Mécanisme d'abandon** après 5 tentatives pour éviter les boucles infinies
- **Traçabilité complète** de toutes les tentatives et adaptations

## 6. Configuration

Configuration via `config/maintenance_config.json` :
- Factory d'agents avec rôles spécialisés
- Paramètres de workspace et chemins de rapport
- Seuils de performance et timeout

## 7. Rapports Générés

### Format JSON
```json
{
  "mission_id": "mission_YYYYMMDD_HHMMSS",
  "statut_mission": "SUCCÈS - Terminée",
  "duree_totale_sec": 45.67,
  "agents_reports": {
    "agent_name.py": {
      "status": "REPAIRED|SUCCESS|CRITICAL_ERROR",
      "original_code": "...",
      "final_code": "..."
    }
  },
  "equipe_maintenance_roles": ["analyseur_structure", ...]
}
```

### Format Markdown
Rapport détaillé avec sections structurées générées par l'agent documenteur.

## 8. Dépendances

- **Python 3.8+**
- **core.agent_factory_architecture** (Agent, Task, Result, AgentFactory)
- **Modules standard** : asyncio, datetime, pathlib, json, logging
- **Configuration** : `config/maintenance_config.json`

## 9. Journal des Modifications (Changelog)

- **v4.3.0 (2025-06-26)** :
  - Harmonisation avec standards Pattern Factory NextGeneration
  - Enrichissement docstrings classe et méthodes
  - Amélioration `get_capabilities()` avec 5 capacités détaillées
  - Documentation .md complète créée
- **v4.2.0** :
  - Report Enrichment
- **Versions antérieures** : Évolution progressive du système de coordination

## 10. Procédure de Test CLI

```python
# test_agent_maintenance_00_coordination.py
import asyncio
from agents.agent_MAINTENANCE_00_chef_equipe_coordinateur import create_agent_MAINTENANCE_00_chef_equipe_coordinateur
from core.agent_factory_architecture import Task

async def test_coordination_workflow():
    # 1. Création et startup
    chef = create_agent_MAINTENANCE_00_chef_equipe_coordinateur(
        workspace_path="/mnt/c/Dev/nextgeneration"
    )
    await chef.startup()
    
    # 2. Test health check
    health = await chef.health_check()
    print(f"Santé équipe: {health}")
    
    # 3. Test mission complète
    mission_task = Task(
        type="workflow_maintenance_complete",
        params={
            "target_files": [
                "./agents/agent_exemple_test.py"  # fichier test
            ]
        }
    )
    
    result = await chef.execute_task(mission_task)
    print(f"Mission terminée: {result.success}")
    if result.success:
        print(f"Rapport: {result.data}")
    
    # 4. Shutdown
    await chef.shutdown()

# Exécution
# python -c "import asyncio; asyncio.run(test_coordination_workflow())"
```

## 11. Statut et Validation

- ✅ **Pattern Factory** : Conforme (Agent, Task, Result)
- ✅ **Méthodes async** : startup, shutdown, execute_task, health_check
- ✅ **Capabilities** : 5 capacités spécialisées définies
- ✅ **Documentation** : Docstrings enrichies et .md complet
- ✅ **Tests CLI** : Procédure de validation définie

**Agent MAINTENANCE 00 - État : PRÊT POUR VALIDATION**