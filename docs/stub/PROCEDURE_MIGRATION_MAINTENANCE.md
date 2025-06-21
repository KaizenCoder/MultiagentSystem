# Procédure de Migration et de Validation de l'Équipe de Maintenance

Ce document détaille les étapes suivies pour migrer l'équipe d'agents de maintenance vers une structure centralisée, corriger les dépendances du projet et valider son bon fonctionnement à travers une mission de développement concrète.

## 1. Migration des Agents de Maintenance

*   **Objectif :** Déplacer les agents du dossier `agent_equipe_maintenance/` vers le dossier centralisé `agent_factory_implementation/agents/`.
*   **Contrainte :** Conserver la nomenclature métier originale des agents (ex: `agent_MAINTENANCE_00_...`).
*   **Action :**
    1.  Tentative initiale d'utiliser un script de backup personnalisé (`/tools/project_backup_system/backup.py`). L'opération a échoué en raison de chemins incorrects et de dépendances manquantes dans le script.
    2.  Utilisation de la commande `xcopy` pour effectuer une copie directe des 7 agents vers le répertoire de destination, assurant un transfert rapide et fiable.

## 2. Correction des Chemins d'Importation

*   **Problème :** Après le déplacement, 27 fichiers du projet contenaient encore des importations pointant vers l'ancien emplacement des agents.
*   **Solution :**
    1.  Création d'un script Python ad-hoc (`update_imports_maintenance.py`).
    2.  Ce script a parcouru l'ensemble du projet pour identifier les fichiers concernés et remplacer automatiquement les anciens chemins d'importation (`from agent_equipe_maintenance...`) par les nouveaux (`from agent_factory_implementation.agents...`).
    3.  Le script a été exécuté avec succès, corrigeant toutes les dépendances en une seule opération.

## 3. Validation par une Mission de Développement (Agents PostgreSQL)

*   **Objectif :** Tester l'intégration et l'opérationnalité de l'équipe de maintenance fraîchement migrée.
*   **Mission :** Développer le code des agents situés dans `docs/agents_postgresql_resolution/`, qui étaient initialement des fichiers vides.

### 3.1. Phase de Test et Débogage

*   **Script de test :** Création du script `test_equipe_maintenance_postgresql.py` pour simuler la mission et isoler les problèmes potentiels.
*   **Itérations de débogage :**
    1.  **`ModuleNotFoundError` :** Le module `logging_manager_optimized` était introuvable. Corrigé en copiant la version de production du module à la racine du projet.
    2.  **`ImportError` :** Le script de test utilisait des noms de fonctions de création d'agent incorrects. Les bons noms ont été identifiés avec `grep` et corrigés.
    3.  **Erreur de logique :** Le script ne détectait pas les fichiers agents PostgreSQL à cause d'un préfixe de nommage inattendu (`agent_POSTGRESQL_...`). La logique de détection a été ajustée.
    4.  **Erreur `NoneType` :** L'agent chef d'équipe n'était pas initialisé correctement. Corrigé en passant les bons chemins en argument à son constructeur.

### 3.2. Exécution de la Mission

*   **Script d'orchestration :** Création du script `lancer_equipe_maintenance_postgresql.py` pour lancer la mission de développement sur les 3 agents PostgreSQL jugés les plus critiques.
*   **Débogage mineur :** Correction d'une erreur de syntaxe dans une chaîne de caractères multiligne au sein du script.
*   **Résultat :** Le script s'est exécuté avec succès, générant le code pour les 3 agents ciblés et produisant un rapport de mission.

## 4. Finalisation et Rapport

*   **Complétion manuelle :** L'utilisateur a restauré manuellement les 6 agents PostgreSQL restants.
*   **Vérification :** Confirmation que les 9 agents dans `docs/agents_postgresql_resolution/` étaient désormais complets et fonctionnels.
*   **Actions finales :**
    1.  Mise à jour du fichier `docs/agents_postgresql_resolution/README.md` pour marquer la mission comme "100% ACCOMPLIE" et documenter le statut de chaque agent.
    2.  Création d'un rapport de mission final (`rapport_mission_postgresql_finalise.json`) pour archiver officiellement la réussite de l'opération. 