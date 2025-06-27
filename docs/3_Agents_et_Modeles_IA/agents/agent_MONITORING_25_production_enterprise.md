# 📊 AGENT MONITORING – PRODUCTION ENTERPRISE (Monitoring Team)

**Auteur**    : Équipe de Maintenance NextGeneration  
**Version**   : 2.0.0 – Pattern Factory Compliant Enterprise  
**Mission**   : Supervision, analyse et optimisation de la production NextGeneration, avec reporting intelligent et alerting avancé.

---

## 1. Présentation Générale

L'Agent Monitoring, **Production Enterprise**, assure la supervision avancée de la production, l'analyse des anomalies, la génération de dashboards, l'alerting intelligent et le reporting de conformité. Il s'appuie sur une architecture modulaire (Pattern Factory) et l'injection de dépendances (DI) pour garantir la robustesse, la flexibilité et la conformité aux standards du projet.

- **Supervision** : Surveillance temps réel des métriques critiques de production.
- **Analyse** : Détection d'anomalies par ML, prédiction et suivi SLA.
- **Reporting** : Génération de rapports de conformité et de performance.
- **Alerting** : Configuration d'alertes intelligentes et automatisées.

## 2. Capacités Principales

- Détection d'anomalies par ML (`ml_anomaly_setup`)
- Création de dashboards avancés (`advanced_dashboards_creation`)
- Configuration d'alerting intelligent (`intelligent_alerting_config`)
- Suivi des SLA (`sla_monitoring_setup`)
- Analytique prédictive (`predictive_analytics`)
- Reporting conformité (`compliance_reporting`)

## 3. Architecture et Concepts Clés

- **Pattern Factory** : Architecture modulaire, chaque feature est un service injectable.
- **Injection de Dépendances (DI)** : L'agent reçoit une liste de features (services) lors de l'instanciation, conformément à l'ADR-003.
- **Stubs internes** : Les features critiques sont implémentées en interne pour garantir l'autonomie de l'agent.
- **Asynchrone** : Toutes les opérations principales sont asynchrones pour la performance.
- **Conformité** : Respect des standards d'architecture et de robustesse du projet.

## 4. Guide d'Utilisation

L'agent est conçu pour être utilisé via l'injection de dépendances.

### a. Instanciation de l'Agent (Simulation de DI)
```python
from agents.agent_MONITORING_25_production_enterprise import (
    MLAnomalyFeature,
    DashboardFeature,
    AlertingFeature,
    SLAMonitoringFeature,
    PredictiveFeature,
    ComplianceFeature,
    create_agent_25_monitoring
)
features_to_inject = [
    MLAnomalyFeature(config={...}),
    DashboardFeature(config={...}),
    AlertingFeature(config={...}),
    SLAMonitoringFeature(config={...}),
    PredictiveFeature(config={...}),
    ComplianceFeature(config={...}),
]
agent = create_agent_25_monitoring(features=features_to_inject)
```

### b. Exécution d'une tâche de monitoring
```python
from core.agent_factory_architecture import Task
import asyncio

task = Task(type="ml_anomaly_setup", params={"scope": "production"})
result = asyncio.run(agent.execute_task(task))
print(result)
```

## 5. Guide d'Extension

- **Ajout de nouveaux features** : Créer une nouvelle classe de feature (ex : `PerformanceFeature`) et l'ajouter à la liste injectée.
- **Personnalisation des analyses** : Modifier ou remplacer l'implémentation d'un feature existant.
- **Intégration avec d'autres agents** : workflow collaboratif Monitoring/Production.

## 6. Journal des Améliorations

- **Version 2.0.0 (2025-06-25)** : Refactorisation complète pour la conformité Pattern Factory et DI (ADR-003). Création de stubs internes pour toutes les features critiques. Passage à l'asynchrone. Bloc de test intégré validé.
- **2025-06-25** : Mission de réparation documentée dans `MISSION_REPAIR_AGENT_MONITORING_25.md` : nettoyage, stubs, DI, validation asynchrone.

## 7. Recommandations d'Amélioration

- Ajouter des features avancées (ex : monitoring prédictif multi-cluster).
- Intégrer un dashboard de suivi temps réel.
- Automatiser la gestion des alertes critiques.

## 8. Schéma d'Architecture (Pattern Factory & DI)

```mermaid
graph TD
    A["Agent25ProductionMonitoringEnterprise"] -->|"Injection de dépendances"| B["MLAnomalyFeature"]
    A -->|"Injection de dépendances"| C["DashboardFeature"]
    A -->|"Injection de dépendances"| D["AlertingFeature"]
    A -->|"Injection de dépendances"| E["SLAMonitoringFeature"]
    A -->|"Injection de dépendances"| F["PredictiveFeature"]
    A -->|"Injection de dépendances"| G["ComplianceFeature"]
    B -- "execute(task)" --> H["Résultat ML"]
    C -- "execute(task)" --> I["Dashboard"]
    D -- "execute(task)" --> J["Alerting"]
    E -- "execute(task)" --> K["SLA Report"]
    F -- "execute(task)" --> L["Prédiction"]
    G -- "execute(task)" --> M["Rapport conformité"]
```

## 9. Exemple de Workflow Typique

1. **Déclenchement** : Un événement de production (ex : pic de latence) déclenche une tâche de monitoring.
2. **Création de la tâche** : Un objet `Task` est instancié avec le type approprié (ex : `ml_anomaly_setup`).
3. **Exécution asynchrone** : L'agent reçoit la tâche et la transmet à la feature concernée via `await feature.execute(task)`.
4. **Traitement** : La feature effectue l'analyse (ex : détection d'anomalie) et retourne un objet `Result` enrichi de métriques.
5. **Collecte des résultats** : L'agent centralise les résultats, les logs et les métriques pour reporting ou alerting.
6. **Reporting** : Génération automatique d'un rapport ou d'une alerte selon le résultat.

## 10. Focus : Validation Asynchrone

L'agent 25 exploite l'asynchrone pour garantir la réactivité et la scalabilité, même sous forte charge.

**Avantages :**
- Exécution non bloquante des analyses et des features.
- Possibilité de paralléliser plusieurs tâches de monitoring.
- Réduction du temps de latence pour le reporting et l'alerting.

**Exemple :**
```python
import asyncio
from core.agent_factory_architecture import Task
from agents.agent_MONITORING_25_production_enterprise import (
    MLAnomalyFeature, create_agent_25_monitoring
)

features = [MLAnomalyFeature()]
agent = create_agent_25_monitoring(features=features)

task = Task(type="ml_anomaly_setup", params={"scope": "prod"})

async def main():
    result = await agent.execute_task(task)
    print(result)

asyncio.run(main())
```

**Bonnes pratiques :**
- Toujours utiliser `await` pour l'exécution des features.
- Préférer `asyncio.run()` pour les tests ou scripts de validation.
- S'assurer que chaque feature implémente bien des méthodes asynchrones (`async def`).

---

**Statut :** Production Ready – Monitoring & reporting de production actif.

---

*Document généré automatiquement par l'IA de maintenance NextGeneration.*

# Agent Spécialiste Monitoring Production

## Objectif
Assurer le suivi en temps réel de la santé, de la performance et de la fiabilité du système **Adaptateur V4** en production.

## Responsabilités
1.  **Exporter les Métriques** : Utilise `MetricsExporter` pour collecter et exposer les métriques clés de l'application au format Prometheus.
2.  **Surveiller la Santé du Système** : Analyse en continu la latence, le taux d'erreurs, l'utilisation mémoire et l'efficacité du cache.
3.  **Déclencher des Alertes** : S'appuie sur la configuration de Prometheus Alertmanager pour notifier les équipes en cas de dépassement des seuils critiques.
4.  **Fournir des Données de Visualisation** : Alimente le dashboard Grafana pour une analyse visuelle et intuitive des performances.

## Infrastructure de Monitoring

- **Prometheus** :
  - **Fichier de configuration** : `prometheus-production.yml`
  - **Responsabilité** : Scrape (collecte) les métriques exposées par l'application.
- **Grafana** :
  - **URL** : `http://localhost:3000`
  - **Responsabilité** : Visualise les données de Prometheus via des dashboards pré-configurés.
- **Alertmanager** :
  - **Fichier de règles** : `alerts.yml`
  - **Responsabilité** : Gère les règles de déclenchement des alertes.

## Métriques Clés Collectées

- `requests_total` : Compteur total des tâches reçues.
- `responses_total` : Compteur des tâches terminées (par statut : succès/échec).
- `request_duration_seconds` : Histogramme de la latence des tâches.
- `memory_usage_bytes` : Utilisation actuelle de la mémoire par le processus.
- `cache_total` : Nombre total d'appels au cache.
- `cache_hits` : Nombre de succès (hits) dans le cache.
- `cache_hit_rate_percent` : Pourcentage de hits par rapport au total des appels.

## Seuils d'Alerte Actifs

- **Taux d'erreur élevé** : Déclenché si le taux d'erreur sur 5 minutes est supérieur à 10%.
- **Latence anormale** : Déclenché si le 95ème percentile (P95) de la latence dépasse 500ms.
- **Utilisation mémoire excessive** : Déclenché si la consommation de mémoire dépasse 1GB.
- **Hit rate du cache trop bas** : Déclenché si le hit rate du cache descend en dessous de 80% pendant plus de 10 minutes.

## Intégration
- L'agent s'intègre directement dans le code de `adaptateur.py` pour instrumenter les fonctions clés et collecter les métriques au plus près de l'exécution.
- Il collabore étroitement avec l'**Agent Analyseur de Performance** en lui fournissant les données brutes nécessaires à l'analyse des tendances et à l'identification des goulots d'étranglement.
- La méthode `shutdown()` a été implémentée dans `MetricsExporter` pour garantir une libération propre des ports et éviter les processus orphelins. 