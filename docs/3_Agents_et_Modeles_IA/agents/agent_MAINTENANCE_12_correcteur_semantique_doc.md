# 🧠 AGENT 12 – CORRECTEUR SÉMANTIQUE (Intelligence Contextuelle)

**Auteur**    : Équipe de Maintenance NextGeneration  
**Version**   : 1.1.0 – Production Ready  
**Mission**   : Dépasser la syntaxe pour assurer la cohérence fonctionnelle du code.

---

## 1. Présentation Générale

L'Agent 12, **Correcteur Sémantique**, est un outil d'analyse statique avancé conçu pour aller au-delà de la simple validation syntaxique. Sa mission est de détecter et corriger les incohérences sémantiques et fonctionnelles dans le code Python.

Il opère de manière itérative : à chaque passe, il analyse le code, identifie un ensemble de problèmes potentiels, propose des corrections, et applique les changements. Ce processus se répète jusqu'à ce qu'aucun nouveau problème ne soit détecté (atteinte d'un "point fixe") ou qu'un nombre maximal de passes soit atteint.

Cette approche garantit une amélioration progressive et robuste du code source, en se basant sur un ensemble de "correcteurs" spécialisés et extensibles.

## 2. Caractéristiques Principales

Cette version `1.1.0` est considérée comme "Production Ready" grâce à l'implémentation des fonctionnalités suivantes :

- **Correction itérative jusqu'au point fixe** : Garantit une correction complète en ré-analysant le code après chaque modification.
- **Correcteurs injectables** : L'architecture repose sur des classes de correcteurs spécialisées qui peuvent être injectées à l'instanciation, offrant une extensibilité maximale (Pattern "Strategy").
- **Configuration externe** : Les paramètres clés (seuils de similarité, imports communs, etc.) sont gérés via un fichier `pyproject.toml`, permettant une adaptation fine sans modifier le code de l'agent.
- **Tri des imports (style `isort`)** : Les imports sont automatiquement regroupés et triés (bibliothèque standard, dépendances tierces, code local).
- **Typage statique complet** : Utilisation généralisée des annotations de type (PEP 484) et des `TypedDict` pour une meilleure robustesse.
- **Suppression des "chaînes magiques"** : Utilisation d'`Enum` pour les types d'erreurs, les actions et les niveaux de sévérité, ce qui clarifie le code.
- **Scoring de confiance pondéré** : Le résultat inclut un score de confiance calculé en fonction de la sévérité des problèmes corrigés.
- **Tests unitaires embarqués** : Un bloc `if __name__ == "__main__":` fournit un exemple d'exécution rapide et une démonstration des capacités de l'agent.

## 3. Architecture et Concepts Clés

### a. Moteur de Correction Itératif

Le cœur de l'agent réside dans la méthode `execute_task`. Elle orchestre le processus en boucle :

1.  **Analyse (`CorrectionContext`)** : Le code source est parsé en un Arbre Syntaxique Abstrait (AST) et ses symboles (imports, variables, fonctions) sont répertoriés.
2.  **Détection (`detect`)** : Chaque correcteur parcourt le contexte d'analyse pour identifier les problèmes relevant de sa spécialité.
3.  **Proposition (`propose`)** : Chaque correcteur génère des propositions de correction pour les problèmes détectés.
4.  **Application (`_apply`)** : L'agent applique les corrections au code.
5.  **Convergence** : Si le code a été modifié, une nouvelle passe est lancée. Sinon, le processus s'arrête.

### b. `CorrectionContext` : Le Cerveau de l'Analyse

La classe `CorrectionContext` est instanciée à chaque passe. Elle encapsule l'état du code à un instant `t` :
- Le code source et ses lignes.
- L'AST (si le code est syntaxiquement valide).
- Les tables de symboles : imports, variables, fonctions, classes.
- La liste des problèmes (`issues`) et des corrections (`corrections`) identifiés durant la passe.

Elle fournit une vision unifiée et statique que les correcteurs peuvent interroger sans avoir à parser le code eux-mêmes.

### c. `IssueCorrector` : Le Pattern "Strategy"

Pour découpler la logique de détection et de correction, l'agent utilise le pattern *Strategy*.
- `IssueCorrector` est une classe de base abstraite définissant l'interface (`detect`, `propose`).
- Des correcteurs concrets héritent de cette base pour implémenter une logique spécifique :
    - `CoreImportCorrector` : Vérifie la présence des imports fondamentaux (`Agent`, `Task`, `Result`).
    - `MissingImportCorrector` : Ajoute les imports manquants pour des symboles connus.
    - `NamingErrorCorrector` : Corrige les fautes de frappe dans les noms de variables/fonctions par similarité (`difflib`).
    - `DocstringCorrector` : Ajoute des docstrings de base aux fonctions publiques.

### d. Configuration Externe via `AgentConfig`

La classe `AgentConfig` charge la configuration depuis la section `[tool.semantic_corrector]` d'un fichier `pyproject.toml` s'il existe. Cela permet de centraliser et d'ajuster le comportement de l'agent pour un projet donné.

**Exemple de configuration `pyproject.toml`:**
```toml
[tool.semantic_corrector]
similarity_threshold = 0.85
max_passes = 3
common_imports = { "pd" = "import pandas as pd\n" }
```

## 4. Guide d'Utilisation

### a. Instanciation de l'Agent
```python
from agent_MAINTENANCE_10_correcteur_semantique import create_agent_MAINTENANCE_10_correcteur_semantique

# Instanciation simple avec les correcteurs par défaut
semantic_corrector_agent = create_agent_MAINTENANCE_10_correcteur_semantique(
    agent_id="corrector-01",
    version="1.1.0"
)
```

### b. Exécution d'une Tâche
```python
import asyncio
from core.agent_factory_architecture import Task

code_a_corriger = """
class MyClass:
    def my_method(self):
        # Faute de frappe : 'lst' au lieu de 'list'
        my_lst = [1, 2, 3] 
        return my_lst
"""

async def run_correction():
    task = Task(
        task_id="correction_01",
        type="semantic_correction",
        params={"code": code_a_corriger}
    )
    result = await semantic_corrector_agent.execute_task(task)

    if result.success:
        print("Code corrigé :")
        print(result.data.get("corrected_code"))
        print("\nProblèmes détectés :", result.data.get("issues"))
        print("\nConfiance :", result.data.get("confidence"), "%")
    else:
        print("Échec de la correction :", result.error)

asyncio.run(run_correction())
```

### c. Format du Résultat (`Result.data`)
- `corrected_code` (str): Le code source après application des corrections.
- `issues` (List[Issue]): La liste des problèmes détectés lors de la dernière passe.
- `corrections` (List[Correction]): La liste des corrections proposées.
- `confidence` (float): Le score de confiance (0-100) représentant le pourcentage de la "sévérité" des problèmes qui ont été résolus.
- `warning` (str, optionnel): Un avertissement, par exemple si le nombre maximal de passes a été atteint.

## 5. Guide d'Extension

### a. Créer un Nouveau Correcteur

1.  **Hériter de `IssueCorrector`** : Créez une nouvelle classe qui hérite de `IssueCorrector`.
2.  **Implémenter `detect`** : Analysez le `CorrectionContext` pour trouver des problèmes. Si un problème est trouvé, ajoutez un `Issue` à `ctx.issues`.
3.  **Implémenter `propose`** : Parcourez les `issues` que votre correcteur peut gérer et ajoutez une `Correction` à `ctx.corrections`.
4.  **Injecter le correcteur** : Passez votre nouvelle classe de correcteur lors de l'instanciation de l'agent.

**Exemple de squelette :**
```python
class MyCustomCorrector(IssueCorrector):
    def detect(self, ctx: CorrectionContext) -> None:
        # Logique de détection...
        if problem_found:
            ctx.issues.append(Issue(...))

    def propose(self, ctx: CorrectionContext) -> None:
        # Logique de proposition de correction...
        if issue_can_be_fixed:
            ctx.corrections.append(Correction(...))

# Injection
agent = AgentMaintenance10(
    correctors=[MyCustomCorrector, NamingErrorCorrector]
)
```

## 6. Journal des Améliorations (v1.1.0)

1.  **Patrons docstring** : Remplacement du dictionnaire `patterns` invalide par une liste de tuples `(regex, callable)`.
2.  **Similarité** : Utilisation de `difflib.SequenceMatcher.ratio()` pour le *fuzzy-matching*.
3.  **Validation imports** : Clé `missing` toujours présente pour éviter les `KeyError` dans le calcul de score.
4.  **Robustesse `_calculate_confidence_score`** : Accès sécurisé via `dict.get()` et composantes pondérées ajustables.
5.  **Nettoyage imports** : Suppression des dépendances inutilisées et normalisation du typage pour compatibilité.
6.  **Logging** : Unification sur `self.logger` avec ajout de niveaux DEBUG.
7.  **Type-hints** : Annotations PEP 484 généralisées.
8.  **PEP 8/PEP 257** : Longueurs de ligne ≤ 100 caractères, docstrings normalisées.
9.  **Tests rapides** : Bloc `__main__` épuré pour une exécution en < 5s.
