# Suivi de Migration vers la "Golden Source" de Logging

**Statut Général :** EN COURS

## Phase 1 : Identification des Fichiers à Migrer

- [x] Lancer la recherche des motifs obsolètes.
- [ ] Lister les fichiers identifiés ci-dessous :
  - [ ] `template_manager.py`
  - [x] `start_meta_strategique.py`
  - [x] `test_agents_fonctionnent.py`
  - [x] `test_agents_working.py`
  - [x] `test_workflow_complet_equipe.py`
  - [x] `tests/unit/test_logging_security.py`
  - [x] `tests/advanced/load_testing_1000_users_real.py`
  - [x] `tools/documentation_generator/agent_generateur_documentation.py`
  - [x] `orchestrator/app/performance/load_balancer.py`
  - [ ] `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`

## Phase 2 : Refactoring des Fichiers

*(Répéter pour chaque fichier identifié)*

- **Fichier `template_manager.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `start_meta_strategique.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `test_agents_fonctionnent.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `test_agents_working.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `test_workflow_complet_equipe.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `tests/unit/test_logging_security.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `tests/advanced/load_testing_1000_users_real.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `tools/documentation_generator/agent_generateur_documentation.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `orchestrator/app/performance/load_balancer.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

- **Fichier `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`**
  - [x] Remplacer les anciens imports.
  - [x] Adapter les appels à la nouvelle API.
  - [x] Valider le fonctionnement (test ou exécution).
  - [x] Mettre à jour ce document.

## Phase 2b : Migration en Masse (Terminée)

- [x] Remplacer `from logging_manager_optimized import LoggingManager` dans tous les fichiers `.py`.

## Phase 3 : Validation et Nettoyage Ciblé

- [ ] Identifier les erreurs d'exécution via les tests et l'analyse statique.
- [ ] Corriger les initialisations du logger (`LoggingManager().get_logger(...)` -> `logging_manager.get_logger(...)`).
- [ ] Corriger les appels de méthode spécifiques (`get_agent_logger`, etc.).

## Phase 4 : Nettoyage Final

- [ ] Supprimer `logging_manager_optimized.py` (racine).
- [ ] Supprimer `.../core/logging_manager_optimized_DEPRECATED.py`.

---

## 🚫 Fichiers Hors Périmètre (Ne pas modifier)

- `agents/agent_MAINTENANCE_01_analyseur_structure.py`
- `agents/agent_MAINTENANCE_02_evaluateur_utilite.py`
- `agents/agent_MAINTENANCE_03_adaptateur_code.py`
- `agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py`
- `agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py`
- `agents/agent_MAINTENANCE_06_validateur_final.py`

## Phase 5 : Mission Terminée

- [ ] Confirmer le succès de la migration.

### Fichiers à Adapter

- [x] `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`
- [x] `agents/agent_MAINTENANCE_01_analyseur_structure.py`
- [x] `agents/agent_MAINTENANCE_02_evaluateur_utilite.py`
- [x] `agents/agent_MAINTENANCE_03_adaptateur_code.py`
- [x] `agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py`
- [x] `agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py`
- [x] `agents/agent_MAINTENANCE_06_validateur_final.py`

### Plan de Déploiement

1.  **Backup :** Sauvegarde complète des agents.
2.  **Adaptation :**
    - `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`
    - `agents/agent_MAINTENANCE_01_analyseur_structure.py`
    - `agents/agent_MAINTENANCE_02_evaluateur_utilite.py`
    - `agents/agent_MAINTENANCE_03_adaptateur_code.py`
    - `agents/agent_MAINTENANCE_04_testeur_anti_faux_agents.py`
    - `agents/agent_MAINTENANCE_05_documenteur_peer_reviewer.py`
    - `agents/agent_MAINTENANCE_06_validateur_final.py`
3.  **Tests :** Exécution de `test_all_agents.py`.
4.  **Validation :** Vérification manuelle des logs.

- **Fichier `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`**
  - **Ligne 23:** `self.log_manager = LoggingManager(config_path='../../config/logging_centralized.json', agent_name=self.name)` -> `self.log_manager = LoggingManager(agent_name=self.name)`
  - **Ligne 24:** `self.logger = self.log_manager.get_logger()`
  - **Statut :** ✅ Appliqué 