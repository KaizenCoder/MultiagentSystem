# 🧪 AGENT 05 – MAÎTRE TESTS & VALIDATION (Auto-Évaluation)

## 1. Identification

- **Nom :** Agent Maître Tests & Validation (Auto-Évaluation)
- **Identifiant :** `agent_05_maitre_tests_validation`
- **Version :** (Chargée dynamiquement depuis `config/maintenance_config.json`, voir section Configuration)
- **Responsable Principal :** IA Équipe de Développement et Maintenance Stratégique
- **Contact Technique :** `#canal-agents-validation`

## 2. Description Générale

L'Agent 05 est spécialisé dans l'**auto-évaluation** rigoureuse de ses propres composants internes et de ses fonctionnalités. Il exécute des diagnostics sur son `TemplateManager` (issu du `code_expert`), réalise des "smoke tests" internes pour vérifier son intégrité opérationnelle, et génère des rapports détaillés (formats JSON et Markdown) sur son état de santé interne. Ces rapports couvrent les aspects de tests, validation, performance perçue et qualité de ses propres opérations.

Il ne teste PAS d'autres agents mais se concentre sur sa propre robustesse et fiabilité.

## 3. Objectifs et Missions

- **Auto-Diagnostic Continu :** Surveiller l'état de santé et la performance de ses composants critiques internes.
- **Validation Interne :** S'assurer que son `TemplateManager` et les mécanismes associés sont opérationnels.
- **Exécution de "Smoke Tests" Internes :** Vérifier régulièrement le bon fonctionnement de ses fonctionnalités de base.
- **Reporting d'Auto-Évaluation :** Produire des rapports clairs et concis (JSON & Markdown) sur :
    - Résultats des tests internes.
    - Statut de validation des composants.
    - Indicateurs de performance internes.
    - Évaluation de la qualité de ses propres processus.
- **Support à la Fiabilité :** Fournir des données objectives sur son propre état pour garantir sa fiabilité au sein de l'écosystème d'agents.

## 4. Fonctionnalités Clés (Conformité Pattern Factory)

L'agent respecte le Pattern Factory de base et expose les méthodes suivantes pour son auto-évaluation :

- **`startup()`** : Initialise l'agent, charge sa configuration (y compris les chemins vers `code_expert_dir` et `templates_subdir`), et tente d'initialiser son `TemplateManager`.
- **`health_check()`** : Retourne l'état de santé de l'agent, incluant la disponibilité du `TemplateManager`.
- **`execute_task(task: Task)`** : Point d'entrée principal. Actions supportées pour l'auto-évaluation :
    - `generer_rapport_strategique`: Pour générer un rapport d'auto-évaluation en JSON.
    - `generer_rapport_markdown`: Pour générer un rapport d'auto-évaluation en Markdown (nécessite un rapport JSON en entrée).
- **`generer_rapport_strategique(context: Dict, type_rapport: str)`** :
    - `context`: Actuellement peu utilisé car l'évaluation est interne.
    - `type_rapport`: Type de rapport d'auto-évaluation (`tests`, `validation`, `performance`, `qualite`).
    - Retourne un dictionnaire JSON du rapport.
- **`generer_rapport_markdown(rapport_json: Dict, type_rapport: str, context: Dict)`**:
    - `rapport_json`: Le rapport JSON précédemment généré.
    - `type_rapport`, `context`: Similaires à `generer_rapport_strategique`.
    - Retourne une chaîne Markdown du rapport.
- **`run_smoke_tests()`** : Exécute des tests internes pour vérifier le `TemplateManager` et d'autres aspects. Ne prend pas d'arguments externes.
- **`_collecter_metriques_tests()`**: Méthode interne pour rassembler les données des `run_smoke_tests()` et l'état du `TemplateManager`.
- **`get_capabilities()`** : Retourne une liste des capacités de l'agent, focalisée sur la génération de rapports d'auto-évaluation et l'exécution de tests internes (voir section 5 pour exemples).
- **`shutdown()`** : Arrête l'agent proprement.

## 5. Formats d'Entrée et de Sortie Clés

- **Entrée pour `execute_task` (action `generer_rapport_strategique` - auto-évaluation type "validation" en JSON) :**
  ```json
  {
    "id": "task_auto_eval_1",
    "method": "generer_rapport_strategique", 
    "params": {
      "type_rapport": "validation",
      "context": {} 
    }
  }
  ```
- **Sortie de `execute_task` (exemple succès, rapport JSON d'auto-évaluation) :**
  ```json
  {
    "status": "success",
    "data": {
      "agent_id": "agent_05_maitre_tests_validation",
      "type_rapport": "validation",
      "timestamp": "YYYY-MM-DDTHH:MM:SS.ffffff",
      "specialisation": "maitre_tests_validation_interne",
      "metriques_validation": {
        "score_validation_global": 85,
        // ... autres métriques de validation interne ...
        "statut_validation_template_manager": "OPTIMAL"
      },
      "recommandations_validation": [
        // ... recommandations basées sur l'auto-validation ...
      ],
      "details_techniques_validation": {
        // ... détails techniques de l'auto-validation ...
        "template_manager_operational": true,
        "smoke_tests_passed": true
      }
    },
    "message": "Rapport stratégique 'validation' généré avec succès."
  }
  ```
- **Capacités retournées par `get_capabilities()` (extrait) :**
  ```json
  [
    "generate_self_assessment_report:json:tests",
    "generate_self_assessment_report:markdown:tests",
    "generate_self_assessment_report:json:validation",
    "generate_self_assessment_report:markdown:validation",
    // ... autres types et formats ...
    "run_smoke_tests:internal",
    "get_internal_metrics"
  ]
  ```

## 6. Dépendances et Prérequis

- **Internes au projet :**
    - `core.agent_factory_architecture` (pour `Agent`, `Task`, `Result`)
    - `core.logging_manager`
    - Modules situés dans le `code_expert_dir` (configuré via `maintenance_config.json`), typiquement :
        - `enhanced_agent_templates` (pour `AgentTemplate`, `TemplateValidationError`)
        - `optimized_template_manager` (pour `TemplateManager`)
- **Python Standard :** `sys`, `pathlib`, `os`, `json`, `time`, `asyncio`, `datetime`, `typing`, `pydantic`.

## 7. Configuration

L'agent charge sa configuration depuis `config/maintenance_config.json` sous la clé correspondant à son `agent_id` (`agent_05_maitre_tests_validation`). Les paramètres spécifiques importants pour son auto-évaluation incluent :
- `version`: La version de l'agent.
- `config.code_expert_dir`: Chemin relatif vers le répertoire contenant le code expert (ex: `code_expert/`).
- `config.templates_subdir`: Sous-répertoire pour les templates utilisés par le `TemplateManager` (ex: `templates/`).
- `config.cache_size`, `config.ttl_seconds`, `config.enable_hot_reload`, `config.num_workers`: Paramètres pour le `TemplateManager`.

Ces configurations sont cruciales pour l'initialisation et le fonctionnement du `TemplateManager`, qui est un point central de son auto-évaluation.

## 8. Journal des Modifications de cette Documentation (.md)

- **v1.0 (Date de création initiale) :** Description d'un agent orchestrateur de tests externes. *Obsolète par rapport au code actuel.*
- **v2.0 (2025-06-26) :** Refonte complète pour aligner la documentation avec le rôle réel de l'agent : auto-évaluation de ses composants internes (TemplateManager, smoke tests) et génération de rapports associés. Clarification des fonctionnalités, entrées/sorties, et configuration liées à ce rôle.

---

**Statut Actuel de l'Agent :** En cours de validation pour son rôle d'auto-évaluation.

---

*Document généré automatiquement par l’IA de maintenance NextGeneration.*