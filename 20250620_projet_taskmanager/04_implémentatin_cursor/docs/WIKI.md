#  wiki:
# 🎯 Wiki du Projet : TaskMaster NextGeneration (Implémentation Cursor)

Ce wiki centralise la connaissance du projet TaskMaster NextGeneration, une solution complète pour l'orchestration de tâches IA en environnement local haute performance.

## 1. 🚀 Mission et Objectifs

Le projet vise à déployer un système **TaskMaster 100% opérationnel** sur une infrastructure Windows, en exploitant la puissance de calcul d'un GPU NVIDIA (RTX 3090) pour des modèles de langage locaux (via Ollama) et en garantissant une robustesse à toute épreuve des services de données.

Un objectif majeur et désormais atteint était de **résoudre définitivement le bug d'encodage PostgreSQL UTF-8** qui empêchait le fonctionnement sur des systèmes Windows configurés en français.

## 2. 🏗️ Architecture du Système

L'architecture de TaskMaster NextGeneration est conçue pour la performance, la résilience et la modularité.

| Catégorie | Composant | Rôle | Statut |
| :--- | :--- | :--- | :--- |
| 🗄️ **Bases de Données** | **PostgreSQL 17.5** | Base de données relationnelle principale. | ✅ **Opérationnel** (après fix UTF-8) |
| | **SQLite** | Base de données de fallback pour la résilience et le développement. | ✅ **Opérationnel** |
| | **ChromaDB** | Base de données vectorielle pour la recherche sémantique et la mémoire des agents. | ✅ **Opérationnel** |
| 🤖 **Intelligence Artificielle**| **NVIDIA RTX 3090** | GPU assurant la puissance de calcul pour les modèles locaux. | ✅ **Opérationnel** |
| | **Ollama** | Runtime pour servir les modèles de langage et d'embedding en local. | ✅ **Opérationnel** |
| | **LM Studio** | (Optionnel) Interface graphique pour gérer et interagir avec les modèles. | ✅ **Opérationnel** |
| 🌐 **Services & API** | **Memory API** | API FastAPI (port 8001) qui unifie l'accès à la mémoire du système (PostgreSQL/ChromaDB). | ✅ **Opérationnel** |

## 3. 🔧 Le Défi PostgreSQL UTF-8 : Problème et Résolution

Cette section est cruciale pour comprendre l'historique et la stabilité actuelle du projet.

### Le Problème (`UnicodeDecodeError`)
- **Symptôme**: Une erreur `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9...` se produisait lors des connexions à PostgreSQL.
- **Cause Racine**: Sur un système Windows en français, PostgreSQL génère des messages d'erreur (ex: "échec de l'authentification") encodés en `Windows-1252`. Le driver Python (`psycopg2`) s'attendait à de l'UTF-8, provoquant un conflit fatal. Le byte `0xe9` correspond au caractère `é`.
- **Impact**: Blocage complet de l'utilisation de PostgreSQL, qui est la base de données principale.

### La Solution Définitive
La solution, à la fois simple et robuste, consiste à forcer PostgreSQL à envoyer ses messages système dans un format universel compatible UTF-8.
- **Action**: Modifier le fichier `postgresql.conf`.
- **Configuration**: Ajouter ou modifier la ligne `lc_messages = 'C'`.
- **Résultat**: Les messages d'erreur sont désormais en anglais et encodés en ASCII/UTF-8, ce qui élimine totalement le conflit.

## 4. 🛠️ Scripts et Composants Clés

Le répertoire `04_implémentatin_cursor` contient des scripts essentiels pour gérer, tester et utiliser le système.

### Scripts de Correction et Validation
- **`fix_postgresql_utf8_cursor.py`**: **À exécuter une seule fois (en admin)**. Ce script sauvegarde `postgresql.conf`, applique le patch `lc_messages = 'C'`, et vous guide pour redémarrer le service.
- **`test_postgresql_utf8_cursor.py`**: Valide que la correction a bien été appliquée et que la connexion à PostgreSQL est 100% fonctionnelle.
- **`test_taskmaster_final_cursor.py`**: Le script de **test ultime**. Il passe en revue tous les composants de l'architecture (70 points) et génère un rapport de conformité complet. Lancez-le pour avoir un bilan de santé global.

### Composants Applicatifs
- **`cli_taskmaster_cursor.py`**: L'interface en ligne de commande pour interagir avec TaskMaster.
  ```bash
  # Lancer une tâche
  python cli_taskmaster_cursor.py launch "Ma nouvelle tâche"
  # Valider l'infra
  python cli_taskmaster_cursor.py validate
  ```
- **`dashboard_taskmaster_cursor.py`**: Un tableau de bord en temps réel dans votre console pour monitorer l'état de tous les services (DB, GPU, API...).
  ```bash
  # Lancer le dashboard
  python dashboard_taskmaster_cursor.py
  ```
- **`validator_sessions_cursor.py`**: Un outil pour vérifier les sessions PostgreSQL actives, détecter les tâches orphelines et nettoyer les processus expirés.

## 5. 🚀 Guide d'Installation et d'Utilisation

Suivez ces étapes pour un déploiement complet :

1.  **Prérequis**:
    *   Windows 10/11
    *   PostgreSQL 17.5 installé.
    *   Python 3.11+
    *   Droits Administrateur pour la première étape.

2.  **Étape 1 : Correction de PostgreSQL (Admin)**
    Ouvrez un terminal **en tant qu'administrateur** et exécutez :
    ```bash
    cd 20250620_projet_taskmaster/04_implémentatin_cursor
    python fix_postgresql_utf8_cursor.py
    ```
    Suivez les instructions pour redémarrer le service PostgreSQL.

3.  **Étape 2 : Validation du système**
    Dans un terminal normal :
    ```bash
    # Valider juste la BDD
    python test_postgresql_utf8_cursor.py

    # Lancer le test complet pour tout vérifier
    python test_taskmaster_final_cursor.py
    ```

4.  **Étape 3 : Lancer une tâche**
    ```bash
    python cli_taskmaster_cursor.py launch "Analyser les logs du système"
    ```

5.  **Étape 4 : Monitoring**
    Dans un autre terminal, lancez le tableau de bord pour garder un oeil sur le système pendant qu'il travaille.
    ```bash
    python dashboard_taskmaster_cursor.py
    ```

## 6. 🔍 Dépannage (Troubleshooting)

- **Erreur `UnicodeDecodeError` persiste**:
  - **Cause probable**: Le fix n'a pas été appliqué ou le service PostgreSQL n'a pas été correctement redémarré.
  - **Solution**: Relancez `fix_postgresql_utf8_cursor.py` en mode admin et assurez-vous de bien redémarrer le service. Vérifiez manuellement que `lc_messages = 'C'` est présent dans `postgresql.conf`.

- **Erreur de connexion à `localhost:8001` (Memory API)**:
  - **Cause probable**: Le service de l'API mémoire n'est pas démarré.
  - **Solution**: Assurez-vous que le serveur Uvicorn pour la Memory API est en cours d'exécution.

- **Erreur de connexion à `localhost:11434` (Ollama)**:
  - **Cause probable**: Le service Ollama n'est pas démarré.
  - **Solution**: Lancez `ollama serve` dans un terminal.

- **Erreur `No module named 'memory_api'`**:
  - **Cause probable**: Le chemin vers le projet `memory_api` n'est pas dans le `PYTHONPATH`.
  - **Solution**: Les scripts dans `04_implémentatin_cursor` sont conçus pour ajouter dynamiquement les chemins nécessaires. Exécutez les scripts depuis ce répertoire. 