# Procédure Opérationnelle Standard : Équipe de Maintenance d'Agents

**Version :** 1.0
**Date :** 2025-06-23
**Auteur :** Gemini Pro

## 1. Principes et Architecture

L'équipe de maintenance est un système multi-agents conçu pour analyser, évaluer, réparer et améliorer de manière autonome d'autres agents.

### 1.1. Composants Clés
- **Coordinateur (`agent_MAINTENANCE_00_...`) :** Le chef d'orchestre. Il initialise l'équipe, distribue les tâches et gère le cycle de vie de la mission.
- **Agent Factory (`core/agent_factory_architecture.py`) :** Le "service de recrutement". Elle lit le fichier `config/maintenance_config.json` pour savoir comment construire chaque agent spécialisé.
- **Agents Spécialisés (`agent_MAINTENANCE_XX_...`) :** Les membres de l'équipe, chacun avec une compétence unique (analyse, adaptation, test, etc.).

### 1.2. Le Workflow en Action
Pour chaque agent cible, le coordinateur exécute la séquence suivante :
1.  **Analyse de Structure (Agent 01) :** Une première passe pour détecter les erreurs de syntaxe fatales.
2.  **Évaluation d'Utilité (Agent 02) :** Attribution d'un score. Si le score est bas ou si une erreur de syntaxe a été trouvée, la boucle de réparation est déclenchée.
3.  **Boucle de Réparation (si nécessaire) :**
    -   `Adaptateur de Code (03)` : Tente de corriger la structure et la syntaxe.
    -   `Testeur (04)` : Tente d'instancier le code réparé pour valider la correction.
    -   *D'autres agents comme le correcteur logique (06) ou le gestionnaire de dépendances (07) peuvent intervenir ici.*
4.  **Harmonisation de Style (Agent 11) :** Une fois le code jugé fonctionnel, l'outil `black` l'uniformise.
5.  **Analyses Finales (Agents 08, 09) :** Des analyses de performance et de sécurité sont menées sur le code final.
6.  **Génération du Rapport (Agent 05) :** L'agent documenteur compile toutes les informations recueillies dans un rapport de mission détaillé.

---

## 2. Procédure d'Intégration d'un Nouvel Agent (Checklist)

Suivez cette procédure **scrupuleusement** pour éviter toute régression.

### ✅ Phase 1 : Préparation du Fichier de l'Agent
-   [ ] **1.1. Nom du Fichier :** Le nom DOIT suivre la convention `agent_MAINTENANCE_XX_nom_descriptif.py`.
-   [ ] **1.2. Nom de la Classe :** Le nom DOIT suivre la convention `AgentMAINTENANCEXXNomDescriptif`.
-   [ ] **1.3. Héritage :** La classe DOIT hériter de `Agent` (depuis `core.agent_factory_architecture`).
-   [ ] **1.4. Constructeur `__init__` :**
    -   [ ] La **première ligne** doit être `super().__init__(agent_type="mon_role", **kwargs)`.
    -   [ ] La **deuxième ligne** doit être `self.logger = logging.getLogger(self.__class__.__name__)`.
-   [ ] **1.5. Méthodes Abstraites :** La classe DOIT implémenter `startup`, `shutdown`, `health_check`, et `get_capabilities`. Des implémentations vides ou basiques suffisent au début.
-   [ ] **1.6. Fonction Factory :** Un fonction `create_agent_MAINTENANCE_XX_...(**kwargs)` DOIT exister au niveau du module et retourner une instance de votre agent.

### ✅ Phase 2 : Configuration
-   [ ] **2.1. Mettre à jour `config/maintenance_config.json` :**
    -   [ ] Ajoutez un nouvel objet à la section `"agents"`.
    -   [ ] Le nom de la clé (ex: `"mon_nouvel_agent"`) doit correspondre à l'`agent_type` défini dans le `super().__init__`.
    -   [ ] Renseignez précisément les clés `"module"`, `"class"`, et `"factory_function"`. Toute incohérence ici mènera à un échec.

### ✅ Phase 3 : Intégration dans l'Équipe
-   [ ] **3.1. Recruter l'Agent :**
    -   [ ] Ouvrez `agents/agent_MAINTENANCE_00_chef_equipe_coordinateur.py`.
    -   [ ] Dans la méthode `_recruter_equipe`, ajoutez votre `agent_type` à la liste `roles`.
-   [ ] **3.2. Intégrer au Workflow :**
    -   [ ] C'est l'étape la plus délicate. Toujours dans le coordinateur, trouvez le bon endroit logique dans la méthode `_run_remediation_cycle` pour appeler votre agent.
    -   [ ] Utilisez `await self._run_sub_task("votre_agent_type", "la_tache_a_executer", params_dict)` pour l'invoquer.

---

## 3. Tester et Valider les Modifications

Ne jamais commiter sans tester.

### 3.1. Lancement du Test
La commande de base pour un test ciblé est :
```bash
python run_maintenance.py --agents <chemin_vers_un_agent_cible>
```

### 3.2. Stratégie de Test Recommandée
1.  **Test 1 (Intégration) :** Lancez le workflow sur un agent cible **connu pour être fonctionnel** (ex: `agents/agent_16_peer_reviewer_senior.py`). Le but est de vérifier que votre nouvel agent est correctement recruté et s'insère dans la chaîne sans la casser.
2.  **Test 2 (Non-Régression) :** Lancez le workflow sur un agent cible **connu pour être défectueux** (ex: `agents/agent_18_auditeur_securite.py`). Le but est de s'assurer que votre nouvel agent n'empêche pas les autres agents (comme l'Adaptateur) de faire leur travail.

### 3.3. Analyse des Logs
Pendant l'exécution, cherchez ces lignes :
-   `INFO - Type d'agent 'mon_role' enregistré...` : Prouve que la configuration est lue.
-   `INFO - Agent mon_role créé avec ID:...` : Prouve que le recrutement a réussi.
-   `INFO - Délégation de la tâche 'ma_tache' à l'agent 'mon_role'` : Prouve que l'intégration au workflow est fonctionnelle.
-   **Absence d'erreurs** de type `AttributeError: ... has no attribute 'logger'` ou `Agent type ... not registered`.

---

## 4. Capitalisation : Pièges à Éviter & Bonnes Pratiques

Cette section est le résumé de toutes les erreurs que nous avons corrigées ensemble.

-   **PIÈGE n°1 : L'Ordre d'Initialisation du Logger.**
    -   **Symptôme :** `AttributeError: ... object has no attribute 'logger'`
    -   **Cause :** Dans le `__init__`, `self.logger` est utilisé avant d'être défini.
    -   **RÈGLE D'OR :** L'ordre dans le `__init__` est **NON NÉGOCIABLE** : 1. `super().__init__(...)`, 2. `self.logger = ...`, 3. Le reste.

-   **PIÈGE n°2 : Les Noms Incohérents.**
    -   **Symptôme :** `ModuleNotFoundError`, `AttributeError`, ou `Agent type '...' not registered.`
    -   **Cause :** Une faute de frappe ou une incohérence entre le nom de la classe/fonction dans le fichier Python et ce qui est déclaré dans `config/maintenance_config.json`.
    -   **RÈGLE D'OR :** Copiez-collez les noms (classe, fonction, module) depuis votre code vers le fichier JSON. Ne les retapez jamais.

-   **BONNE PRATIQUE : L'Intégration "à blanc".**
    -   Pour un agent qui modifie profondément le code, envisagez de l'intégrer une première fois avec sa logique de transformation désactivée (il se contente de recevoir et renvoyer le code).
    -   Si le workflow passe, l'intégration est validée. Vous pouvez ensuite activer sa logique en toute confiance.

-   **BONNE PRATIQUE : La Journalisation.**
    -   Après chaque intégration réussie et validée par un test, mettez à jour le `JOURNAL_EVOLUTION_EQUIPE.md`.
    -   Ceci crée une trace immuable des décisions et des résultats, essentielle pour la maintenance à long terme.

-   **POINT D'ATTENTION : La Limite d'Arguments du Terminal.**
    -   Lors du lancement sur un grand nombre d'agents (> 7-8 sur Windows), le terminal peut atteindre sa limite de longueur d'arguments.
    -   Dans ce cas, la solution est de coder temporairement la liste des agents cibles directement dans `run_maintenance.py` ou d'implémenter une lecture depuis un fichier.