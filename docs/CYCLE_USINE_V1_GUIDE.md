# 🏭 Cycle-Usine v1 - Guide Complet
================================

## Vue d'Ensemble

Le **Cycle-Usine v1** est un système de développement automatisé qui orchestre intelligemment le cycle complet de création d'agents NextGeneration :

**Spec → Code → Test → Doc → Deploy**

### Architecture du Système

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  📋 SPEC        │───▶│  ⚡ CODE        │───▶│  🧪 TEST        │
│  Requirements  │    │  Generation     │    │  Validation     │
│  Analysis       │    │  with LLM       │    │  & Coverage     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  🚀 DEPLOY      │◀───│  📚 DOC         │◀───│  Quality Gates  │
│  Automated      │    │  Auto Generated │    │  Validation     │
│  with Rollback  │    │  Technical Docs │    │  (90-95%)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Fonctionnalités Principales

### ✨ Capacités Automatisées
- **Analyse Intelligente** : Conversion des requirements en spécifications techniques
- **Génération de Code** : Code Python avec validation syntaxique
- **Tests Automatiques** : Suite complète avec couverture de code
- **Documentation** : README et API docs générés automatiquement
- **Déploiement** : Pipeline avec validation et rollback

### 🛡️ Quality Gates
- **Spec Completeness** : 95% de complétude
- **Code Coverage** : 85% de couverture minimum
- **Test Success Rate** : 90% de réussite
- **Doc Coverage** : 90% de documentation
- **Deploy Success Rate** : 95% de succès

### 🔄 Parallélisme
- Jusqu'à **4 tâches concurrent**
- Tests parallélisés
- Déploiement séquentiel pour sécurité

## Installation et Configuration

### 1. Structure des Fichiers

```bash
/mnt/c/Dev/nextgeneration/
├── systems/
│   └── cycle_usine_v1.py          # Système principal
├── scripts/
│   └── demo_cycle_usine_v1.py     # Démonstration
├── configs/
│   └── cycle_usine_config.json    # Configuration
└── cycles/                        # Cycles générés
    └── [cycle_id]/
        ├── specifications.json
        ├── generated_code/
        ├── documentation/
        ├── cycle_state.json
        └── cycle_results.json
```

### 2. Configuration

```json
{
  "workspace": "/mnt/c/Dev/nextgeneration",
  "llm_gateway": "http://localhost:11434",
  "models": {
    "spec": "deepseek-coder:33b",
    "code": "deepseek-coder:33b",
    "test": "deepseek-coder:33b",
    "doc": "deepseek-coder:7b"
  },
  "quality_gates": {
    "spec_completeness": 0.95,
    "code_coverage": 0.85,
    "test_success_rate": 0.90,
    "doc_coverage": 0.90,
    "deploy_success_rate": 0.95
  }
}
```

## Utilisation

### 1. Lancement d'un Cycle

```python
from cycle_usine_v1 import CycleUsineV1

# Initialiser le système
usine = CycleUsineV1()

# Définir les requirements
requirements = {
    'name': 'Mon Agent',
    'description': 'Agent de maintenance intelligent',
    'architecture': 'nextgeneration',
    'features': [
        'llm_integration',
        'async_processing',
        'monitoring_integration',
        'auto_healing'
    ],
    'capabilities': {
        'input_formats': ['json', 'yaml'],
        'output_formats': ['json', 'markdown'],
        'processing_modes': ['batch', 'stream']
    }
}

# Démarrer le cycle
cycle_id = await usine.start_cycle('mon_agent', requirements)

# Exécuter le cycle complet
results = await usine.execute_cycle()
```

### 2. Monitoring d'un Cycle

```python
# Vérifier le statut
status = usine.get_cycle_status(cycle_id)
print(f"Succès: {status['success_rate']:.1%}")

# Lister tous les cycles
cycles = usine.list_cycles()
for cycle in cycles:
    print(f"{cycle['cycle_id']}: {cycle['success_rate']:.1%}")
```

### 3. Démonstration Complète

```bash
# Lancer la démonstration
python3 scripts/demo_cycle_usine_v1.py
```

## Étapes du Cycle

### 📋 1. SPECIFICATION
**Objectif** : Analyser les requirements et générer un cahier des charges détaillé

**Processus** :
- Analyse LLM des requirements d'entrée
- Génération des spécifications techniques
- Identification des livrables
- Définition des critères de validation

**Outputs** :
- `specifications.json` : Spécifications structurées
- Cahier des charges markdown
- Liste des livrables

### ⚡ 2. CODE GENERATION
**Objectif** : Générer automatiquement le code Python avec validation

**Processus** :
- Génération de code avec modèle LLM
- Validation syntaxique Python
- Création de la structure de fichiers
- Vérification des patterns

**Outputs** :
- `main.py` : Code principal de l'agent
- `tests.py` : Tests unitaires
- Rapport de validation syntaxique

### 🧪 3. TESTING
**Objectif** : Exécuter une suite complète de tests automatisés

**Processus** :
- Génération de tests automatiques
- Exécution de la suite de tests
- Calcul de la couverture de code
- Validation des performances

**Outputs** :
- Résultats des tests (succès/échec)
- Rapport de couverture
- Métriques de performance

### 📚 4. DOCUMENTATION
**Objectif** : Générer automatiquement la documentation technique

**Processus** :
- Analyse du code pour extraction des APIs
- Génération de README avec exemples
- Création de documentation API
- Guide d'utilisation

**Outputs** :
- `README.md` : Documentation principale
- `API.md` : Documentation des APIs
- Guides d'installation

### 🚀 5. DEPLOYMENT
**Objectif** : Déploiement automatisé avec validation

**Processus** :
- Préparation du package de déploiement
- Déploiement avec validation
- Tests post-déploiement
- Configuration du monitoring

**Outputs** :
- URL de déploiement
- Résultats des tests post-deploy
- Configuration de monitoring

## Quality Gates

### Validation Progressive
Le système utilise des **quality gates** pour garantir la qualité à chaque étape :

```python
# Exemple de vérification
if test_success_rate >= 0.90:  # 90% minimum
    proceed_to_next_stage()
else:
    fail_cycle_with_rollback()
```

### Seuils Configurables
- **Développement** : Seuils assouplis (70-80%)
- **Staging** : Seuils intermédiaires (80-90%)
- **Production** : Seuils stricts (90-99%)

## Intégrations

### 🤖 LLM Gateway
- Support Ollama local et APIs distantes
- Modèles spécialisés par étape
- Fallback automatique

### 📊 Monitoring
- Métriques temps réel
- Alertes sur échecs
- Dashboard de suivi

### 🔄 MessageBus
- Communication inter-agents
- Événements de cycle
- Notifications automatiques

## Exemples d'Utilisation

### Agent de Maintenance
```python
requirements = {
    'name': 'Agent Maintenance Pro',
    'type': 'maintenance_agent',
    'features': [
        'system_health_check',
        'auto_repair',
        'predictive_maintenance',
        'alert_management'
    ],
    'quality_requirements': {
        'performance': {'response_time_ms': 200},
        'reliability': {'uptime_percentage': 99.9}
    }
}
```

### Agent API
```python
requirements = {
    'name': 'Agent API Gateway',
    'type': 'api_agent',
    'features': [
        'request_routing',
        'load_balancing',
        'rate_limiting',
        'authentication'
    ],
    'deployment': {
        'container_ready': True,
        'health_checks': True,
        'metrics_export': True
    }
}
```

## Résultats de Cycle

### Métriques de Succès
```json
{
  "cycle_id": "agent_demo_20250628_214259",
  "overall_success_rate": 1.0,
  "total_duration": 0.01,
  "stages": {
    "specification": {"success_rate": 1.0, "duration": 0.00},
    "code_generation": {"success_rate": 1.0, "duration": 0.01},
    "testing": {"success_rate": 1.0, "duration": 0.00},
    "documentation": {"success_rate": 1.0, "duration": 0.00},
    "deployment": {"success_rate": 1.0, "duration": 0.00}
  }
}
```

### Artefacts Générés
- **Code Source** : Agent prêt à l'emploi
- **Tests** : Suite complète validée
- **Documentation** : Guides utilisateur et technique
- **Configuration** : Paramètres de déploiement
- **Monitoring** : Métriques et alertes

## Troubleshooting

### Erreurs Communes

**1. Échec Quality Gate Testing**
```bash
# Vérifier la configuration des seuils
Error: Quality gate échoué pour testing (95% vs 98% requis)
Solution: Ajuster quality_gates.test_success_rate dans config
```

**2. Erreur de Génération de Code**
```bash
# Vérifier la syntaxe générée
Error: Syntax error in generated code
Solution: Améliorer les prompts LLM ou validation
```

**3. Problème de Déploiement**
```bash
# Vérifier les ressources
Error: Deployment failed - resource not available
Solution: Vérifier l'environnement de déploiement
```

### Logs et Debug
```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier les états de cycle
status = usine.get_cycle_status(cycle_id)
print(status)
```

## Évolutions Futures

### Version 1.1
- [ ] Intégration LLM temps réel
- [ ] Support multi-langages (JS, Go, Rust)
- [ ] Pipeline CI/CD intégré

### Version 1.2
- [ ] Interface graphique web
- [ ] Templates d'agents prédéfinis
- [ ] Marketplace d'agents

### Version 2.0
- [ ] Intelligence artificielle pour optimisation automatique
- [ ] Auto-scaling des cycles
- [ ] Déploiement multi-cloud

## Contribution

### Structure du Code
- `CycleUsineV1` : Classe principale
- `CycleTask` : Modèle de tâche
- `CycleStage` : Énumération des étapes
- Handlers spécialisés par étape

### Tests
```bash
# Lancer la suite de tests
python3 -m pytest tests/test_cycle_usine.py -v

# Test de performance
python3 scripts/benchmark_cycle_usine.py
```

---

**🎯 Cycle-Usine v1** - Automatisation intelligente du développement NextGeneration

*Développé par l'équipe NextGeneration - 2025*