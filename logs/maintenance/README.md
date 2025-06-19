# 📁 LOGS DE MAINTENANCE - STRUCTURE ORGANISÉE

## 🎯 Vue d'ensemble

Cette structure organisée centralise tous les logs de maintenance des agents NextGeneration pour une meilleure traçabilité et maintenance.

## 📋 Structure des répertoires

```
logs/maintenance/
├── orchestrateur/     # Logs du Chef Équipe Maintenance Orchestrateur
├── analyseur/        # Logs de l'Agent Analyseur Structure
├── evaluateur/       # Logs de l'Agent Évaluateur Utilité
├── testeur/          # Logs de l'Agent Testeur Agents
├── docteur/          # Logs de l'Agent Docteur Réparation
└── README.md         # Ce fichier
```

## 🎖️ Orchestrateur (`orchestrateur/`)

**Rapports consolidés** de maintenance d'équipes complètes :
- `rapport_maintenance_complete_orchestrateur_YYYYMMDD_HHMMSS.json`
- `rapport_analyse_equipe_orchestrateur_YYYYMMDD_HHMMSS.json`

**Contenu typique** :
- Résumé exécution workflows
- Statistiques agents traités
- Recommandations consolidées
- Actions suivantes

## 🔍 Analyseur (`analyseur/`)

**Analyses de structure** d'équipes d'agents :
- `rapport_analyse_analyseur_YYYYMMDD_HHMMSS.json`
- `cache_analyse_structure.json`

**Contenu typique** :
- Inventaire agents détectés
- Analyse complexité et structure
- Métriques de code
- Imports et dépendances

## 🎯 Évaluateur (`evaluateur/`)

**Évaluations d'utilité** et pertinence :
- `rapport_evaluation_evaluateur_YYYYMMDD_HHMMSS.json`
- `selection_outils_YYYYMMDD_HHMMSS.json`

**Contenu typique** :
- Scores d'utilité pondérés
- Agents sélectionnés/rejetés
- Critères d'évaluation
- Recommandations d'intégration

## 🧪 Testeur (`testeur/`)

**Tests de conformité** Pattern Factory :
- `rapport_testeur_YYYYMMDD_HHMMSS.json`
- `rapport_agents_dev_testeur_agents_YYYYMMDD_HHMMSS.json`
- `cache_testeur_agents.json`

**Contenu typique** :
- Scores conformité Pattern Factory
- Tests obligatoires/recommandés
- Distribution niveaux conformité
- Recommandations corrections

## 🩺 Docteur (`docteur/`)

**Interventions de réparation** automatique :
- `rapport_interventions_docteur_YYYYMMDD_HHMMSS.json`
- `rapport_reparations_dev_docteur_reparation_YYYYMMDD_HHMMSS.json`
- `historique_reparations_docteur.json`

**Contenu typique** :
- Agents réparés avec succès
- Corrections appliquées
- Backups créés
- Taux de réussite interventions

## 🔧 Configuration

La structure est gérée par `config/logs_maintenance_config.py` :

```python
from config.logs_maintenance_config import LogsMaintenanceConfig

# Assurer structure existe
LogsMaintenanceConfig.ensure_logs_structure()

# Obtenir chemin rapport
rapport_path = LogsMaintenanceConfig.get_rapport_path("orchestrateur", "maintenance_complete")
```

## 📊 Avantages de cette organisation

### ✅ **Avant** (logs en vrac à la racine)
- ❌ Difficile de retrouver les logs
- ❌ Pollution répertoire racine
- ❌ Pas de classification
- ❌ Maintenance complexe

### ✅ **Après** (structure organisée)
- ✅ **Classification claire** par type d'agent
- ✅ **Répertoire racine propre**
- ✅ **Traçabilité améliorée**
- ✅ **Maintenance simplifiée**
- ✅ **Archivage organisé**

## 🚀 Usage recommandé

### Consultation logs récents
```bash
# Derniers rapports orchestrateur
ls -la logs/maintenance/orchestrateur/ | tail -5

# Derniers tests conformité
ls -la logs/maintenance/testeur/ | tail -5

# Dernières réparations
ls -la logs/maintenance/docteur/ | tail -5
```

### Nettoyage périodique
```bash
# Archiver logs > 30 jours
find logs/maintenance/ -name "*.json" -mtime +30 -exec mv {} archive/ \;
```

### Monitoring
```bash
# Surveiller taille répertoire
du -sh logs/maintenance/

# Compter rapports par type
find logs/maintenance/ -name "*.json" | wc -l
```

## 📈 Métriques de maintenance

Cette structure permet de suivre facilement :
- **Fréquence maintenance** par équipe
- **Évolution scores conformité** dans le temps
- **Efficacité réparations** automatiques
- **Tendances qualité** agents

## 🔄 Migration automatique

Les anciens logs à la racine ont été automatiquement déplacés vers cette structure organisée lors de la mise à jour.

---

*Structure organisée v2.0.0 - Chef Équipe Maintenance Orchestrateur NextGeneration* 