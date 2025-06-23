# TaskMaster Next‑Gen — Livrables V1

> **Version :** 0.1  |  **Date :** 23 juin 2025  |  **Auteur :** ChatGPT (o3)

---

## 1. Rapport d’analyse détaillé

### 1.1 Contexte et héritage

L’architecture actuelle (« prototype actuel ») gère déjà la découverte dynamique d’agents et la délégation par *capability*, mais n’intègre ni parsing NLP poussé ni découpage hiérarchique des tâches. Toutes les fonctionnalités marquées comme *abandonnées* dans la précédente mouture doivent donc être **ré‑intégrées** et **étendues** fileciteturn2file0. Le cahier des charges exige en outre la priorisation, l’estimation de complexité et l’export structuré fileciteturn2file1.

### 1.2 Analyse d’écart (gap analysis)

| Domaine                       | Prototype actuel                | Exigence cible                               | Écart        |
| ----------------------------- | ------------------------------- | -------------------------------------------- | ------------ |
| NLP & extraction d’intentions | Manual prompts + règles simples | spaCy/transformers avec modèles multilingues | **Fort**     |
| Découpage WBS + dépendances   | Non automatisé                  | Automatisé + justifié                        | **Critique** |
| Estimation complexité         | N/A                             | Score + justification                        | **Critique** |
| Priorisation intelligente     | N/A                             | Calcul priorité dynamique                    | **Moyen**    |
| Export/Import structuré       | Logs textuels                   | JSON + Markdown + Graph                      | **Moyen**    |
| Observabilité métriques       | Logs bruts                      | KPI agrégés + alertes                        | **Moyen**    |

### 1.3 Choix techniques majeurs

- **Langage :** Python 3.12 (compatibilité avec librairies NLP récentes).
- **NLP :** spaCy v3 + modèle *fr\_core\_news\_lg* pour parsing francophone, complété par Transformers (HF) pour embeddings sémantiques.
- **Graph dependency :** *networkx* pour construire et manipuler le graphe des tâches.
- **Persistance & export :** schéma JSONSchema + Markdown auto‑généré.
- **Tests :** pytest + fixtures markdown/PRD.
- **CI :** GitHub Actions avec matrix Python {3.12, 3.11}.

---

## 2. Architecture fonctionnelle & logique

```
                    ┌───────────────┐           ┌───────────────┐
                    │  InputParser  │           │ DocumentStore │
                    └──────┬────────┘           └────────┬──────┘
                           │                             │
                           ▼                             ▼
┌─────────────┐   Context  ┌───────────────┐   Graph   ┌──────────────┐
│ Capability  │──────────▶│ TaskAnalyzer   │─────────▶│ Dependency   │
│  Router     │           └──────┬─────────┘           │  Resolver    │
└─────────────┘                  │                     └────┬─────────┘
                           Plan  ▼                          │
                     ┌───────────────┐  Updates             │
                     │   Scheduler   │──────────────────────┘
                     └──────┬────────┘
                            ▼
                     ┌───────────────┐
                     │   Reporter    │
                     └───────────────┘
```

**Description rapide** :

- **InputParser** : détecte le type de document (PRD, Markdown, prompt brut), l’encode en structure interne.
- **TaskAnalyzer** : NLP + heuristiques → génère WBS initiale, complexité, dépendances.
- **DependencyResolver** : transforme les liens en graphe orienté ; détecte cycles, blocs critiques.
- **Scheduler** : assigne statuts, priorités, propose la « next actionable task ».
- **Reporter** : export JSON/Markdown + rendu graphique (mermaid ou .svg).

---

## 3. Plan d’implémentation détaillé

| Sprint (5 jours)             | Modules / Jalons                                            | Points de validation                                |
| ---------------------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| S1 — Boot & Parser           | Repo scaffold, InputParser, unit tests                      | Parse un PRD de 2 000 tokens sans erreur            |
| S2 — TaskAnalyzer v1         | spaCy pipeline, extraction intents‑constraints‑deliverables | WBS correcte (±10 % vs référence)                   |
| S3 — Complexity + Dependency | Algorithme scoring, graph build (networkx)                  | Graphe sans cycle, complexité > 0 pour chaque tâche |
| S4 — Scheduler + Reporter    | Priorisation heuristics, export Markdown/JSON               | Fonction `getNextTask` retourne tâche cohérente     |
| S5 — Hardening + CLI/API     | Coverage 90 %, packaging, docs                              | `pip install taskmaster-ng` OK                      |

---

## 4. Code source — Structure proposée

```
/ taskmaster_ng
│
├── __init__.py
├── main.py              # Point d’entrée CLI
├── core/
│   ├── models.py        # dataclasses Task, Project, Doc
│   ├── parser.py        # InputParser
│   ├── analyzer.py      # TaskAnalyzer
│   ├── complexity.py    # Scoring logic
│   ├── dependency.py    # DependencyResolver
│   ├── scheduler.py     # Scheduler
│   └── reporter.py      # Reporter/export
├── utils/
│   ├── nlp.py           # spaCy helpers
│   └── io.py            # read/write docs
├── tests/
│   ├── test_parser.py
│   ├── test_analyzer.py
│   ├── test_dependency.py
│   └── fixtures/
│       ├── prd_sample.md
│       └── plan_sample.md
└── docs/
    ├── README.md
    ├── architecture.md
    └── api_reference.md
```

### 4.1 Exemple de code (extrait : `models.py`)

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    id: str
    title: str
    description: str
    complexity: int = 0  # 1 = easy → 5 = hard
    priority: str = "medium"  # high|medium|low
    status: str = "todo"      # todo|in‑progress|review|done
    depends_on: List[str] = field(default_factory=list)

@dataclass
class Project:
    name: str
    tasks: List[Task] = field(default_factory=list)

    def get_next_task(self) -> Optional[Task]:
        pending = [t for t in self.tasks if t.status == "todo" and not t.depends_on]
        return sorted(pending, key=lambda t: t.priority)[0] if pending else None
```

---

## 5. Jeux de tests

### 5.1 Scénarios unitaires (pytest)

- **test\_parser\_valid\_prd** : vérifie qu’un PRD complexe est converti en structure interne sans exception.
- **test\_analyzer\_wbs\_depth** : assure que chaque tâche a ≤ 3 niveaux de profondeur dans un plan de 40 tâches.
- **test\_complexity\_range** : garantit que la complexité est entre 1 et 5.
- **test\_dependency\_no\_cycles** : construit le graphe et vérifie l’absence de cycles.
- **test\_get\_next\_task\_logic** : simule tâches avec dépendances et vérifie que la suivante est cohérente.

### 5.2 Fixtures fuzzées

Un script `scripts/generate_fuzz_fixtures.py` génère 30 PRD avec fautes d’indentation, formats mixtes, sections manquantes pour tester la robustesse du parser.

---

## 6. Documentation utilisateur & technique

| Fichier               | Contenu                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **README.md**         | Présentation, installation, quick‑start (CLI)                                              |
| **architecture.md**   | Diagrammes (mermaid), description modules                                                  |
| **api\_reference.md** | Docstring autodoc via `pdoc`                                                               |
| **user\_guide.md**    | Tutoriaux pas‑à‑pas : importer un PRD, obtenir le prochain lot de tâches, exporter le plan |

---

## 7. Rapport de validation (template)

| Test suite                     | Couverture | Résultat                  |
| ------------------------------ | ---------- | ------------------------- |
| `pytest -q`                    | XX %       | ✅ / ❌                     |
| Parser large PRD (10 k tokens) | —          | Time < 2 s                |
| Export JSON/Markdown           | —          | Fichiers valides ✔︎       |
| CLI `getNextTask`              | —          | Retourne ID tâche attendu |

Un script `scripts/run_validation.sh` exécute l’ensemble et génère `reports/validation_report.md`.

---

## 8. Prochaines étapes

1. **Décider** si l’on crée un nouvel agent spécifique “TaskMaster” ou si l’on étend le `Coordinateur` actuel.
2. **Cloner** ce squelette dans votre repo monorepo.
3. **Sprint 1** (Parser) peut démarrer immédiatement ; estimation : 2 jours.

---

*Fin du document — Tous les éléments sont fournis sous licence MIT, prêts pour itérations ultérieures.*

