_Exported on 6/23/2025 at 01:15:00 GMT+2 from Cursor (1.1.3)_

---

**User**

Prends connaissance des documents suivants sans rien implémenter. La mission a déjà commencé.

Attends ma validation pour implémenter quoi que ce soit.
Le prompt de lancement est le suivant, ne l'exécute pas :

---

# PROMPT DE LANCEMENT — Implémentation TaskMaster V3

## 0. ⚠️ ACTION IMMÉDIATE
1.  Créer le fichier **`JOURNAL_MIGRATION_TASKMASTER_V2_V3.md`** à la racine du répertoire d'implémentation (`IMPLEMENTATION_DIR`). Y coller **strictement** le contenu fourni en § 8.
2.  Créer le fichier **`SUIVI_AVANCEMENT_TASKMASTER_V3.md`** dans `IMPLEMENTATION_DIR`. Y coller **strictement** le contenu fourni en § 9.

_Aucune autre action n'est autorisée tant que ces deux fichiers n'existent pas._

---

## 1. Contexte et Mission
1.1 **Rôle de l'IA** : assistant expert en architecture logicielle et implémentation de systèmes IA.
1.2 **Objectif** : **Adapter et fusionner les implémentations expertes (Claude, Gemini, ChatGPT) pour créer concrètement l'architecture unifiée de TaskMaster V3.** On ne réinvente pas l'implémentation, on l'adapte en prenant le meilleur de chaque proposition.
1.3 **Point de départ** : Le document `ARCHITECTURE_UNIFIEE_TASKMASTER.md` qui a été validé.
1.4 **Code Source Expert (à adapter)** :
    -   **Claude :** `C:\Dev\nextgeneration\agents\taskmaster_nextgen.py`
    -   **Gemini :** Script Python contenu dans `C:\Dev\nextgeneration\20250620_projet_taskmanager\05_taskmaster_V2\1_retour_expert_taskmaster_v2\3_gemini\taskmaster_V2_gemini.txt`
    -   **ChatGPT :** Archive `C:\Dev\nextgeneration\20250620_projet_taskmanager\05_taskmaster_V2\1_retour_expert_taskmaster_v2\1_chatgpt\taskmaster_ng_reponse_chatgpt.zip`

---

## 2. Répertoires (noms sans espaces)
| Variable | Chemin absolu |
|----------|---------------|
| `PROJECT_ROOT` | `C:\Dev\nextgeneration` |
| `REFERENCE_ARCH_DIR` | `C:\Dev\nextgeneration\20250620_projet_taskmanager\05_taskmaster_V2\2_implementation_locale_taskmaster_v2` |
| `IMPLEMENTATION_DIR` | `C:\Dev\nextgeneration\taskmaster_v3` |

*Toute sortie (logs, rapports, journaux, suivi) doit aller dans `IMPLEMENTATION_DIR` pour centraliser le travail.*

---

## 3. Sauvegarde Pré-Travail
Avant **chaque** sprint de développement :
- Créer un tag Git `sprint-X-start-YYYYMMDD-HHMM`.
- Reporter le nom du tag dans `JOURNAL_MIGRATION_TASKMASTER_V2_V3.md`.

---

## 4. Cycle de Développement par Sprint (7 étapes impératives)
| # | Étape | Détail |
|---|-------|--------|
| 1 | **Analyser** | Examiner les objectifs du sprint et les sections de code expert correspondantes. |
| 2 | **Proposer** | Détailler la stratégie de fusion/adaptation et les fichiers/classes à créer/modifier. |
| 3 | **Journaliser** | Ajouter l'analyse + proposition dans le journal de migration. |
| 4 | **Valider** | Attendre le feu vert explicite de l'utilisateur pour commencer le développement. |
| 5 | **Appliquer** | Implémenter le code dans `IMPLEMENTATION_DIR` en respectant la structure cible. |
| 6 | **Tester** | Créer et lancer les tests `pytest` correspondants (0 échec requis, couverture > 85%). |
| 7 | **Clôturer & Valider** | **Tester le workflow complet :** Reporter résultat/couverture dans le journal, mettre à jour le suivi, et décider **GO/NO-GO**. |

Commit message standard :
`feat(sprint-X): <résumé clair des fonctionnalités implémentées>`

**Workflow de clôture de sprint :**
- **Si succès des tests :** Effectuer un `commit` et `push`. Journaliser le succès.
- **Si échec des tests :** Effectuer un `rollback` sur le tag Git du début de sprint. Journaliser l'échec et la cause.

---

## 5. Phases du Projet (Sprints)
Correspondent au plan défini dans le document d'architecture :
1.  **Phase 1 – Sprint 1** : Socle et Modèles de données.
2.  **Phase 2 – Sprint 2** : Parsing et Analyse de Base.
3.  **Phase 3 – Sprint 3** : Dépendances et Orchestration.
4.  **Phase 4 – Sprint 4** : API et Finalisation.

---

## 6. Limites de Périmètre
- Ne jamais modifier de fichiers hors `IMPLEMENTATION_DIR` (sauf autorisation explicite).
- Le code doit être autonome et ne pas avoir de dépendances cachées avec le reste du `PROJECT_ROOT`.

---

## 7. Gestion des Dates & Heures
- Horodatage obligatoire au format `YYYY-MM-DD HH:MM CET` dans le journal et les commits.

---

## 8. Contenu initial du journal de migration (à copier tel quel)

```markdown
# Journal de Migration — TaskMaster V2 -> V3

* **Date de début :** 2025-06-23
* **Objectif :** Implémenter l'architecture unifiée de TaskMaster V3 en fusionnant les meilleures approches des codes experts (Claude, Gemini, ChatGPT).

---

## Phase 1 : Sprint 1 - Socle et Modèles

* **Date :**
* **Analyse des Objectifs du Sprint :**
* **Proposition de Fusion/Adaptation :**
* **Décision avant développement :**
* **Résultat des Tests :**
* **Observations post-développement :**
* **Décision Finale (GO/NO-GO pour Sprint 2) :**

---
```

## 9. Contenu initial du fichier de suivi (à copier tel quel)

```markdown
# Suivi d'Avancement — TaskMaster V3

## Sprints

- [ ] **Sprint 1 : Socle et Modèles**
- [ ] **Sprint 2 : Parsing et Analyse de Base**
- [ ] **Sprint 3 : Dépendances et Orchestration**
- [ ] **Sprint 4 : API et Finalisation**

## Livrables Majeurs

- [ ] Architecture de projet créée
- [ ] Modèles de données implémentés
- [ ] Moteur de parsing fonctionnel
- [ ] Moteur de dépendances fonctionnel
- [ ] API REST disponible
- [ ] Documentation finale livrée
```
