# 📁 LOGS DE MAINTENANCE - STRUCTURE ET CONFIGURATION

## 🎯 Vue d'ensemble

Cette structure organise automatiquement tous les logs de maintenance des agents NextGeneration.

**⚠️ IMPORTANT** : Les fichiers de logs ne sont **PAS versionnés** dans Git (voir `.gitignore`)

## 📋 Structure Automatique

La structure suivante est créée automatiquement lors de l'exécution des agents :

```
logs/maintenance/
├── orchestrateur/     # 🎖️ Chef Équipe Maintenance Orchestrateur
├── analyseur/        # 🔍 Agent Analyseur Structure  
├── evaluateur/       # 🎯 Agent Évaluateur Utilité
├── testeur/          # 🧪 Agent Testeur Agents
└── docteur/          # 🩺 Agent Docteur Réparation
```

## 🔧 Configuration

### Création Automatique
```python
from config.logs_maintenance_config import LogsMaintenanceConfig

# La structure est créée automatiquement
LogsMaintenanceConfig.ensure_logs_structure()
```

### Obtenir Chemin Rapport
```python
# Rapport avec timestamp automatique
rapport_path = LogsMaintenanceConfig.get_rapport_path("orchestrateur", "maintenance_complete")
# → logs/maintenance/orchestrateur/rapport_maintenance_complete_orchestrateur_20250619_175030.json
```

## 📊 Types de Fichiers Générés

### 🎖️ Orchestrateur
- `rapport_maintenance_complete_orchestrateur_YYYYMMDD_HHMMSS.json`
- `rapport_analyse_equipe_orchestrateur_YYYYMMDD_HHMMSS.json`

### 🧪 Testeur
- `rapport_testeur_YYYYMMDD_HHMMSS.json`
- `cache_testeur_agents.json`

### 🩺 Docteur
- `rapport_interventions_docteur_YYYYMMDD_HHMMSS.json`
- `historique_reparations_docteur.json`

### 🔍 Analyseur & 🎯 Évaluateur
- `rapport_analyse_analyseur_YYYYMMDD_HHMMSS.json`
- `rapport_evaluation_evaluateur_YYYYMMDD_HHMMSS.json`

## 🚫 Fichiers Ignorés (.gitignore)

```gitignore
# Logs de maintenance (générés automatiquement)
logs/maintenance/
rapport_*.json
cache_*.json
historique_*.json
backups_docteur/
*_backup_*.json
```

## 🚀 Usage

### Consultation Logs
```bash
# Vérifier si structure existe
ls logs/maintenance/

# Derniers rapports par type
ls logs/maintenance/orchestrateur/ | tail -3
ls logs/maintenance/testeur/ | tail -3
ls logs/maintenance/docteur/ | tail -3
```

### Nettoyage Périodique
```bash
# Archiver logs > 30 jours
find logs/maintenance/ -name "*.json" -mtime +30 -exec mv {} archive/ \;

# Taille totale logs
du -sh logs/maintenance/
```

## 📈 Avantages

- ✅ **Structure organisée** par type d'agent
- ✅ **Pas de pollution** répertoire racine
- ✅ **Timestamps automatiques** pour traçabilité
- ✅ **Configuration centralisée**
- ✅ **Non versionnés** dans Git (performances)

## ⚙️ Intégration Agents

Tous les agents de maintenance utilisent automatiquement cette structure :

```python
# Dans un agent de maintenance
rapport_path = LogsMaintenanceConfig.get_rapport_path(
    agent_type="testeur", 
    rapport_type="conformite"
)

# Sauvegarde automatique dans bon répertoire
with open(rapport_path, 'w') as f:
    json.dump(rapport_data, f, indent=2)
```

---

*Configuration logs maintenance v2.0.0 - NextGeneration Team* 