# ⚡ AGENT MAINTENANCE 08 – ANALYSEUR PERFORMANCE (Maintenance Team)

**Auteur**    : Équipe de Maintenance NextGeneration  
**Version**   : 2.0 – Audit Universel Performance (Mission Claudecode)  
**Mission**   : Analyse, détection et optimisation des performances des modules et projets complets pour garantir la robustesse et la scalabilité de NextGeneration.

---

## 1. Présentation Générale

L’Agent Maintenance 08, **Analyseur Performance**, analyse les performances des modules, détecte les goulots d’étranglement et propose des optimisations. Il génère des rapports pour l’équipe de maintenance et coordonne les actions correctives.

**🚀 NOUVEAUTÉ V2.1 (Travaux claudecode) :** Intégration complète du système de logging uniforme + capacité d'audit universel de performance étendue pour analyser des **projets Python complets** (répertoires entiers) en plus des fichiers individuels.

### 🔧 Système de Logging Uniforme V2.1
```python
# ✅ MIGRATION SYSTÈME LOGGING UNIFIÉ (claudecode)
try:
    from core.manager import LoggingManager
    logging_manager = LoggingManager()
    self.logger = logging_manager.get_logger(
        config_name="maintenance",
        custom_config={
            "logger_name": f"nextgen.maintenance.analyseur_performance.{self.id}",
            "log_dir": "logs/maintenance/performance",
            "metadata": {
                "agent_type": "MAINTENANCE_08_analyseur_performance",
                "agent_role": "analyseur_performance",
                "system": "nextgeneration"
            }
        }
    )
except ImportError:
    # Fallback en cas d'indisponibilité du LoggingManager
    self.logger = logging.getLogger(self.__class__.__name__)
```

### Capacités Principales
- **Analyse** : Analyse automatisée des performances des modules et projets complets
- **Détection** : Identification des goulots d'étranglement et points faibles
- **Optimisation** : Propositions d'optimisation et de correction
- **Audit Universel** : Support de l'analyse de performance sur fichiers individuels ou projets complets

## 2. Capacités Techniques

#### Capacités d'Audit Universel (V2.0)
- **Audit de fichiers individuels** : Analyse de performance complète d'un fichier Python spécifique
- **🆕 Audit de répertoires complets** : Analyse récursive de performance de structures de projets entières
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents (.venv, __pycache__, .git, etc.)
- **Rapports consolidés** : Métriques de performance globales + détails par fichier
- **Scoring unifié** : Système de notation de performance cohérent (0-100)

#### Capacités d'Analyse de Performance
- Analyse automatisée des performances (CPU, mémoire, I/O)
- Détection des ralentissements et points faibles
- Génération de rapports d'audit de performance
- Propositions d'optimisation ou de correction
- Coordination avec les autres agents de maintenance

## 3. Architecture V2.0 (Mission Claudecode)

### 3.1 Architecture Technique
- **Orchestrateur Central** : `audit_universal_performance` coordonne tous les types d'audit
- **Audit Fichier Unique** : `_audit_single_python_file` pour l'analyse détaillée de performance
- **Filtrage Intelligent** : `_should_skip_path` pour ignorer les répertoires non pertinents
- **Mapping Performance** : `_map_score_to_performance_level` pour la notation uniforme
- **Gestion Consolidée** : Centralisation des métriques et scoring dans l'orchestrateur

### 3.2 Métriques de Performance
```python
performance_metrics = {
    'cpu_usage': {'weight': 0.3, 'threshold': {'warning': 70, 'critical': 90}},
    'memory_usage': {'weight': 0.3, 'threshold': {'warning': 75, 'critical': 95}},
    'io_operations': {'weight': 0.2, 'threshold': {'warning': 1000, 'critical': 5000}},
    'response_time': {'weight': 0.2, 'threshold': {'warning': 500, 'critical': 2000}}
}
```

## 4. Guide d'Utilisation

### 4.1 Initialisation
```python
from agents.agent_MAINTENANCE_08_analyseur_performance import AgentMaintenance08AnalyseurPerformance
agent = AgentMaintenance08AnalyseurPerformance()
```

### 4.2 Audit d'un Fichier Individuel
```python
# Audit de performance d'un fichier Python spécifique
task_details = {
    "action": "audit_universal_performance",
    "params": {
        "target_path": "chemin/vers/votre/fichier.py"
    }
}
result = agent.execute_task(task_details)
print(f"Score performance : {result['data']['score_global']}/100")
print(f"Niveau performance : {result['data']['niveau_performance']}")
```

### 4.3 🆕 Audit d'un Projet Complet (V2.0)
```python
# Audit de performance d'un répertoire complet
task_details = {
    "action": "audit_universal_performance",
    "params": {
        "target_path": "chemin/vers/votre/projet/"
    }
}
result = agent.execute_task(task_details)

# Résultats consolidés
print(f"Nombre de fichiers analysés : {result['data']['nb_fichiers_analyses']}")
print(f"Score global de performance : {result['data']['score_global']}/100")
print(f"Niveau performance global : {result['data']['niveau_performance']}")

# Détails par fichier
for fichier_result in result['data']['resultats_fichiers']:
    print(f"- {fichier_result['fichier']} :")
    print(f"  Score : {fichier_result['score']}/100")
    print(f"  Goulots d'étranglement : {len(fichier_result['bottlenecks'])}")
```

## 5. Spécifications Techniques V2.0

### 5.1 Méthodes Principales
- **`audit_universal_performance(target_path)`** : Orchestrateur principal (fichier ou répertoire)
- **`_audit_single_python_file(file_path)`** : Audit détaillé de performance d'un fichier
- **`_should_skip_path(path)`** : Filtrage intelligent des chemins à ignorer
- **`_map_score_to_performance_level(score)`** : Mapping score → niveau de performance

### 5.2 Filtrage Intelligent
Répertoires automatiquement ignorés :
- `.venv/`, `venv/`, `env/` (environnements virtuels)
- `__pycache__/`, `.pyc` (cache Python)
- `.git/`, `.svn/` (contrôle de version)
- `node_modules/`, `.npm/` (dépendances JS)
- `build/`, `dist/`, `.egg-info/` (artefacts de build)

### 5.3 Métriques de Performance
- **Score global** : Note consolidée 0-100
- **Nombre de fichiers** : Fichiers Python analysés
- **Goulots d'étranglement** : Points critiques identifiés
- **Utilisation CPU** : Patterns d'utilisation intensive
- **Utilisation mémoire** : Fuites et pics de consommation
- **Opérations I/O** : Patterns d'accès aux ressources

## 6. Guide d'Extension

- **Ajout de nouvelles métriques** : Étendre `_audit_single_python_file`
- **Personnalisation du filtrage** : Modifier `_should_skip_path`
- **Nouveaux formats de rapport** : Surcharger les méthodes de reporting
- **Intégration avec d'autres agents** : Workflow collaboratif maintenance

## 7. Journal des Améliorations

### Version 2.0 (2025-06-26) - Mission Claudecode
- **🚀 AMÉLIORATION MAJEURE** : Support de l'audit de répertoires complets
- **Refactorisation architecture** : `audit_universal_performance` devient orchestrateur central
- **Nouvelles méthodes** : `_audit_single_python_file`, `_should_skip_path`, `_map_score_to_performance_level`
- **Rapports consolidés** : Métriques de performance globales + détails par fichier
- **Filtrage intelligent** : Exclusion automatique des répertoires non pertinents
- **Compatibilité ascendante** : Anciens workflows préservés

### Version 1.0.0
- Version initiale avec analyse de performance basique
- Passage à l'analyse automatisée (Sprint 4)
- Ajout de la détection proactive des ralentissements
- Intégration avec le reporting détaillé

## 8. Recommandations d'Amélioration

### Court Terme
- Ajouter l'analyse prédictive des performances (machine learning)
- Intégrer un dashboard de suivi des performances
- Automatiser la gestion des optimisations critiques

### Moyen Terme
- Analyse de performance distribuée pour grands projets
- Intégration avec des outils de profiling avancés
- Support des autres langages (JavaScript, TypeScript, etc.)
- Analyse dynamique de performance en temps réel

---

**Statut :** ✅ Production Ready V2.0 – Audit universel de performance avec support répertoires complets opérationnel (Mission Claudecode)

---

*Document mis à jour automatiquement suite à la Mission Claudecode - Version 2.0 avec capacités d'audit universel étendues.*

# Agent Analyseur de Performance

## Objectif
Analyser et optimiser les performances du système en se concentrant sur les métriques clés :
- Temps de réponse
- Utilisation mémoire
- Hit rate du cache
- Taux de succès des opérations

## Responsabilités
1. Monitoring continu des performances
2. Optimisation du cache et des ressources
3. Analyse des goulots d'étranglement
4. Recommandations d'amélioration

## Métriques de Performance Validées
- ✅ Temps moyen : 0.209s
- ✅ Utilisation mémoire : 0.8 MB
- ✅ Taux de succès : 100%
- ⚠️ Cache hit rate : 33.3% (objectif 80%)

## Infrastructure Monitoring
### Métriques Prometheus
- Temps de réponse (histogramme)
- Taux de succès/erreurs
- Utilisation mémoire
- Performance du cache

### Seuils d'Alerte
- Taux d'erreur >10%
- Cache hit rate <80%
- Mémoire >1GB
- Latence P95 >500ms

### Optimisations Implémentées
1. Cache Intelligent
   - Stratégie LRU (Least Recently Used)
   - Détection de patterns
   - Préchargement adaptatif
   - Métriques en temps réel

2. Pipeline de Transformation
   - Cache multi-niveaux
   - Traitement parallèle
   - Compression automatique

3. Monitoring Production
   - Dashboard Grafana
   - Alerting configuré
   - Métriques temps réel
   - Historique des performances

## Prochaines Étapes
1. Optimisation de la stratégie de cache pour atteindre >80% hit rate
2. Ajustement des paramètres de mise en cache
3. Analyse continue des patterns d'utilisation
4. Calibration des seuils d'alerte

## Intégration
- Collaboration avec l'agent Chef d'Équipe pour la coordination
- Support de l'agent Adaptateur pour les optimisations
- Interface avec le système de monitoring Prometheus/Grafana

## Documentation
- Rapports de performance
- Métriques et KPIs
- Configurations monitoring
- Procédures d'optimisation