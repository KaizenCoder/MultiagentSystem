# 📝 Prompt de Réparation Structurée d'Agents Python sous Contraintes

## Contexte
Vous êtes chargé de rendre fonctionnels des agents Python dans un projet d'orchestration IA.

**Contraintes majeures :**
- **Il est strictement interdit de modifier le dossier `C:\Dev\core`** (source de vérité, intouchable).
- **Les agents ne doivent pas utiliser de références à `C:\Dev\nextgeneration\code_expert`** (ni import, ni accès direct, ni dépendance).
- **Toute la logique métier, les modèles, les utilitaires doivent provenir exclusivement de `C:\Dev\core`** ou de bibliothèques standards/externes.
- **Si une fonctionnalité n'existe que dans `code_expert`, l'agent doit être adapté pour fonctionner sans, ou être marqué comme bloqué.**

---

## Démarche de Travail à Suivre

### 1. Audit Initial
- Pour chaque agent à réparer :
    - **Lister tous les imports** et dépendances.
    - **Identifier toute référence** (import, chemin, appel de fonction, etc.) à `code_expert` ou à tout autre module hors `core`.
    - **Repérer les accès directs à des chemins absolus ou relatifs interdits**.

### 2. Cartographie des Fonctions Utilisées
- Pour chaque dépendance à `code_expert` :
    - **Déterminer la fonctionnalité exacte utilisée** (classe, fonction, constante, etc.).
    - **Chercher une équivalence dans `core`** (même nom, même signature, ou fonctionnalité approchante).
    - **Documenter les cas où aucune équivalence n'existe**.

### 3. Refactoring
- **Supprimer ou remplacer** toute référence à `code_expert` :
    - Si une équivalence existe dans `core` : **remplacer l'import/l'appel**.
    - Sinon : **adapter la logique de l'agent** pour fonctionner sans cette dépendance (mode dégradé, contournement, etc.).
    - Si l'agent ne peut pas fonctionner sans cette dépendance et qu'aucune solution n'est possible sans toucher à `core` : **marquer l'agent comme bloqué**.

### 4. Validation
- **Vérifier que l'agent ne dépend plus que de `core` et des bibliothèques standards/externes**.
- **Exécuter les tests unitaires ou d'intégration** pour valider le fonctionnement.
- **Documenter précisément** :
    - Les modifications apportées.
    - Les limitations éventuelles.
    - Les agents bloqués et la raison.

### 5. Documentation et Traçabilité
- **Mettre à jour le journal de réparation** (ex : `REPAIR_MISSION_JOURNAL.md`).
- **Mettre à jour le tableau de statut des agents** (ex : `AGENTS_FUNCTIONAL_STATUS.md`).
- **Après chaque modification d'agent, la mise à jour de `AGENTS_FUNCTIONAL_STATUS.md` est OBLIGATOIRE.**
- **Après chaque cycle Mission / Tâche / Documentation (M T D), un commit Git doit être réalisé pour garantir la traçabilité.**
- **Lister pour chaque agent** :
    - Statut (Réparé, Partiellement fonctionnel, Bloqué)
    - Dépendances restantes
    - Points de vigilance

---

## Exemple de Formulation pour l'IA ou l'Opérateur

> « Pour chaque agent Python du dossier `/agents` :
> - Liste tous les imports et dépendances.
> - Pour chaque dépendance à `code_expert`, indique la fonctionnalité utilisée et cherche une équivalence dans `core`.
> - Remplace toute référence à `code_expert` par un appel à `core` si possible, sinon adapte la logique pour fonctionner sans.
> - Si l'agent ne peut pas fonctionner sans une fonctionnalité absente de `core`, marque-le comme bloqué.
> - Vérifie que l'agent ne dépend plus que de `core` et des bibliothèques standards/externes.
> - Documente chaque étape, chaque choix, et mets à jour le journal de réparation et le tableau de statut. »

---

## Conseils pour la session
- **Procéder agent par agent** pour garantir la traçabilité.
- **Ne jamais modifier ni proposer de modification dans `core`**.
- **Être explicite sur les limitations et les choix de contournement**.
- **Conserver une trace claire de chaque décision** (pour audit ou passation). 