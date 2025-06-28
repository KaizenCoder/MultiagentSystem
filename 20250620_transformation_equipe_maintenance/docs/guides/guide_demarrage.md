# 🚀 Guide de Démarrage - Équipe Agents NextGeneration

## 🎯 Introduction

Bienvenue dans l'équipe d'agents NextGeneration ! Ce guide vous aide à démarrer rapidement.

## 📋 Prérequis

- Python 3.8+
- pip installé
- Accès au répertoire du projet

## ⚡ Démarrage Rapide

### 1. Installation
```bash
cd equipe_agents_tools_migration
pip install -r requirements.txt
```

### 2. Lancement du Chef d'Équipe
```bash
python agent_0_chef_equipe_coordinateur.py
```

### 3. Lancement d'un Agent Individuel
```bash
python agent_1_analyseur_structure.py
python agent_2_evaluateur_utilite.py
```

## 🛠️ Configuration

### Variables d'Environnement
- `NEXTGEN_DEBUG=true` : Mode debug
- `NEXTGEN_LOG_LEVEL=INFO` : Niveau de logging

### Chemins Importants
- **Agents source**: `../agent_factory_implementation/agents`
- **Workspace**: `./`
- **Rapports**: `./reports`

## 📊 Commandes Utiles

```bash
# Vérifier l'état de l'équipe
python agent_0_chef_equipe_coordinateur.py --help

# Analyser la structure
python agent_1_analyseur_structure.py --analyze

# Évaluer l'utilité
python agent_2_evaluateur_utilite.py --evaluate
```

---
*Créé par Agent 5 Documenteur - 2025-06-20*
