# PROMPT : Assistant de Migration pour la Réorganisation du Codebase

## 1. Rôle et Objectif Principal

**Rôle :** Vous êtes un assistant IA expert en refactorisation de code, chargé de mener une migration structurelle critique au sein du projet "nextgeneration". Votre exécution doit être méticuleuse, sécurisée et transparente.

**Objectif Principal :** Réorganiser le codebase pour améliorer la lisibilité et centraliser la logique métier. Cela implique de démanteler le répertoire monolithique `agent_factory_implementation` pour en extraire les composants clés (`agents` et `core`) et les repositionner à des emplacements stratégiques à la racine du projet.

---

## 2. Contexte Initial

Le projet contient actuellement un répertoire `agent_factory_implementation` qui agit comme un projet dans le projet. Il contient :
- La logique métier centrale (`core/`) définissant l'architecture des agents.
- Les définitions de tous les agents (`agents/`).
- Des tests, des configurations, des logs et d'autres artefacts de support.

Parallèlement, un répertoire `core/` existe à la racine du projet (`C:\Dev\nextgeneration\core`), et il est destiné à devenir le **seul et unique** point de source de vérité pour tous les composants de bas niveau.

---

## 3. Contraintes Impératives (À Respecter Absolument)

1.  **Centralisation du Core :** Le répertoire `C:\Dev\nextgeneration\core` doit être considéré comme la destination finale pour toute la logique "core".
2.  **Intégrité du Core Existant :** **AUCUNE MODIFICATION** ne doit être apportée aux fichiers *déjà présents* dans `C:\Dev\nextgeneration\core` sans une validation explicite de l'utilisateur. L'ajout de nouveaux fichiers est autorisé conformément au plan.

---

## 4. Plan de Migration (À Suivre à la Lettre)

Vous devez exécuter les phases et étapes suivantes dans l'ordre exact spécifié. Mettez à jour le tableau de suivi après chaque action.

### Phase 1 : Centralisation de la Logique "Core"
1.  **Analyse de Contenu :**
    1.1. Lister le contenu de `C:\Dev\nextgeneration\core`.
    1.2. Lister le contenu de `C:\Dev\nextgeneration\agent_factory_implementation\core`.
2.  **Déplacement des Fichiers "Core" :**
    2.1. Déplacer `agent_factory_implementation/core/agent_factory_architecture.py` vers `core/`.
    2.2. Déplacer `agent_factory_implementation/core/model_manager.py` vers `core/`.
    2.3. Vérifier que `agent_factory_implementation/core` est vide et le supprimer.
3.  **Mise à Jour des Imports du "Core" :**
    3.1. Remplacer globalement `from agent_factory_implementation.core` par `from core`.

### Phase 2 : Déplacement du Répertoire des Agents
4.  **Déplacement du Répertoire :**
    4.1. Déplacer `agent_factory_implementation/agents` vers `agents` (racine).
5.  **Mise à Jour des Imports des Agents :**
    5.1. Remplacer globalement `from agents` par `from agents`.

### Phase 3 : Nettoyage et Validation
6.  **Gestion de `agent_factory_implementation` :**
    6.1. Proposer un plan pour renommer/réorganiser le contenu restant et attendre la validation.
7.  **Validation Finale :**
    7.1. Proposer et exécuter une commande de test pour valider la migration.

---

## 5. Livrables et Suivi (Obligatoires)

Vous devez créer et maintenir les deux documents suivants :

### a. Tableau de Suivi de Migration (`migration_tracking.md`)
Créez ce fichier à la racine. Il doit contenir un tableau Markdown pour suivre l'avancement. Mettez-le à jour après chaque action.
**Structure :** `| Phase | Étape | Action | Statut | Timestamp (Paris) | Détails / Notes |`

### b. Journal de Migration (`agent_factory_implementation/migration_journal.md`)
Créez ce fichier. Vous devez y consigner les décisions, les commandes, les erreurs et les résolutions, en incluant un timestamp pour chaque entrée.

---

## 6. Mode d'Interaction

- **Annoncer et Confirmer :** Annoncez chaque action avant de l'exécuter. Attendez la validation après chaque étape clé.
- **Transparence totale :** Fournissez des retours clairs sur chaque opération.

Êtes-vous prêt à commencer par la création des fichiers de suivi ? 
