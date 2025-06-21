# 🧠 TaskMaster Pool Supervisor - NextGeneration

## 🎯 Objectif
Ce module permet de lancer, superviser et monitorer dynamiquement plusieurs agents TaskMaster pour exécuter des missions parallèles dans l'écosystème NextGeneration.

---

## 📦 Composants clés

| Fichier | Rôle |
|--------|------|
| `taskmaster_pool_supervisor.py` | API FastAPI pour instancier, lister, tuer des TaskMaster |
| `launch_taskmaster.py` | Script CLI de lancement manuel d'une instance avec mission |
| `dashboard_console.py` | Affichage terminal en direct des agents actifs |
| `session_validator.py` | Validation fonctionnelle simplifiée des instances en pool |
| `logging_config_template.json` | Gabarit de logger isolé pour chaque agent |
| `spawn_multiple_agents.json` | Exemple de config JSON pour instancier des agents multiples |

---

## ⚙️ Fonctionnement

1. L'agent TaskMaster est basé sur `AgentTaskMasterNextGeneration`, hérité du Coordinateur.
2. Le superviseur REST permet de lancer dynamiquement des missions.
3. Chaque instance est enregistrée dans un registre local.
4. Les logs, métriques et sessions sont centralisés.

---

## 🚀 Démarrage rapide

```bash
# Lancer l'API de supervision
python taskmaster_pool_supervisor.py

# Lancer une mission depuis CLI
python launch_taskmaster.py "Génère la documentation API"

# Visualiser les agents actifs
python dashboard_console.py
```

---

## 🔐 Sécurité & supervision

- Agents isolés par ID
- Logging centralisé
- Métriques disponibles via `/instances`
- Possibilité d'ajouter RBAC ou restrictions API

---

## 📈 Extensions futures

- Ajout d'une base locale pour le registre (SQLite/JSON)
- UI Web minimale (FastAPI + Tailwind)
- Support du kill/restart automatique
