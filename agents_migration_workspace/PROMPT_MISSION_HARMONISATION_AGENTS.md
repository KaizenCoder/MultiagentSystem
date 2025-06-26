PROMPT DE MISSION : Protocole d'Harmonisation des Agents v2.0
📌 Synthèse de Mission
Ce document établit le protocole obligatoire pour la mission d'harmonisation et de mise à niveau des agents. Votre exécution doit être guidée par trois éléments fondamentaux :

Objectif : Aligner tous les agents sur les standards de qualité, de performance et de documentation du projet.

Document Clé : Le fichier agents_migration_workspace/SUIVI_MIGRATION_AGENTS.md est votre source de vérité unique. Sa consultation est un prérequis à toute action, et sa mise à jour est une obligation post-action.

Méthode Incontournable : Chaque agent doit être traité en suivant rigoureusement le Protocole Standard de Traitement en 9 Étapes détaillé ci-dessous. Aucune déviation n'est autorisée.

🎯 1. Objectif Final
Harmoniser, mettre à niveau et assurer la qualité de l'ensemble des agents et scripts du répertoire agents/.

Livrables attendus en fin de mission :

Agents conformes : Code respectant les standards, testé unitairement et fonctionnellement, et pleinement opérationnel.

Documentation synchronisée : Docstrings et fichiers .md dans docs/3_Agents_et_Modeles_IA/agents/ parfaitement à jour.

Journal des Opérations (SUIVI_MIGRATION_AGENTS.md) : Complété de manière exhaustive, traçant la totalité des interventions.

Optionnel (Phase A) : Une nouvelle équipe d'agents "cartographes" pour assister le processus, développée selon ce même protocole.

⚙️ 2. Les 3 Principes Directeurs (Règles d'Or)
Discipline du Journal de Suivi : Le SUIVI_MIGRATION_AGENTS.md est le cerveau de la mission.

LIRE AVANT : Consultez systématiquement la cartographie (Section 3) et le journal des opérations (Section 4) avant de commencer le traitement d'un nouvel agent.

ÉCRIRE APRÈS : Mettez à jour le journal des opérations (Section 4) immédiatement après chaque action significative (sauvegarde, test, validation, commit, rollback). La traçabilité en temps réel est non négociable.

Intégrité du Processus : Le "Protocole Standard de Traitement" (voir section 3) est immuable. Il doit être appliqué dans son intégralité et dans l'ordre pour chaque agent.

Sécurité et Qualité :

Sauvegardes : Aucune modification n'est entreprise sans une sauvegarde préalable (<nom_fichier>.backup_YYYYMMDD_HHMMSS).

Tests : Des tests CLI sont obligatoires après chaque modification.

Rollback : En cas d'échec de test, un retour à la version de sauvegarde est immédiat et obligatoire. L'incident doit être consigné dans le journal.

Validation Humaine : Aucun commit ne peut être effectué sans la validation explicite du "metasuperviseur".

Standards : Le respect du Pattern Factory, du Logging Manager, la non-régression et la synchronisation code/doc sont impératifs.

🗂️ 3. Le Protocole Standard de Traitement (Cycle en 9 Étapes)
Ceci est la seule méthodologie autorisée pour la modification d'un agent ou d'un script.

Étape 1 : Sauvegarde et Initialisation du Suivi
    - Créer une copie de sauvegarde dans `agents/backups/<nom_agent_ou_script>.py.backup_YYYYMMDD_HHMMSS`.
    - Initialiser/Mettre à jour l'entrée de l'agent dans `SUIVI_MIGRATION_AGENTS.md` (Section 4), marquant le début du traitement.

Étape 2 : Analyse Préliminaire et Planification
    - Lire la documentation existante (.md), le code source, et les informations du `WORKFLOW_SUIVI_AGENTS.md`.
    - Identifier les écarts (documentation, PF, fonctionnalités).
    - Définir un plan d'action précis pour l'agent.
    - Consigner l'analyse et le plan dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).

Étape 3 : Modification / Développement / Synchronisation
    - Implémenter les modifications (code, docstrings).
    - Mettre à jour/créer la documentation .md associée dans `docs/3_Agents_et_Modeles_IA/agents/`.
    - Documenter les choix techniques importants dans `SUIVI_MIGRATION_AGENTS.md` (Section 4) et/ou le journal de l'agent si existant (`logs/agents/`).

Étape 4 : Tests CLI (et autres tests pertinents)
    - Définir et exécuter des tests CLI couvrant les fonctionnalités modifiées/clés.
    - Exécuter tests unitaires/intégration si disponibles.
    - Consigner commandes de test et résultats bruts dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).

Étape 5 : Analyse des Résultats des Tests et Décision
    - Si Échec :
        - Rollback immédiat à la version de sauvegarde (Étape 1).
        - Consigner l'échec, cause, et rollback dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).
        - Retour à Étape 2 (Analyse et Planification de la correction).
    - Si Succès :
        - Consigner le succès dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).
        - Passer à Étape 6.

Étape 6 : Demande de Validation Utilisateur (Metasuperviseur)
    - Préparer un résumé des modifications (diff ou description).
    - Fournir preuves des tests CLI réussis.
    - Soumettre pour validation via le canal de communication défini, en référençant l'entrée dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).

Étape 7 : Traitement du Retour Utilisateur
    - Si Refus / Demandes de Modifications :
        - Consigner le retour dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).
        - Retour à Étape 2 (Analyse et Planification des ajustements).
    - Si Validation Utilisateur (✅) :
        - Consigner la validation explicite (✅) dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).
        - Passer à Étape 8.

Étape 8 : Commit & Push des Modifications Validées
    - `git add [fichiers pertinents]` (agent.py, doc.md, SUIVI_MIGRATION_AGENTS.md, etc.)
    - `git commit -m "feat(AgentX): Description modif - Validé @Metasuperviseur"` ou `fix(...)`
        - Format du message de commit : `type(scope): Sujet bref - Validé @Metasuperviseur`
            - `type` : feat, fix, docs, style, refactor, test, chore
            - `scope` (optionnel) : Nom de l'agent (ex: Agent02, ACP) ou module impacté.
    - `git push`
    - Consigner l'action de commit/push dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).

Étape 9 : Clôture de l'Intervention et Mise à Jour Finale des Suivis
    - Mettre à jour le statut de l'agent dans `WORKFLOW_SUIVI_AGENTS.md`.
    - Mettre à jour/confirmer la cartographie (Section 3) dans `SUIVI_MIGRATION_AGENTS.md`.
    - Marquer l'intervention comme terminée dans `SUIVI_MIGRATION_AGENTS.md` (Section 4).
    - Annoncer la clôture et la disponibilité de l'agent sur le canal de communication.

📞 4. Communication et Validation
Canal Principal : Ce chat.
Validation Explicite : Le mot-clé "VALIDÉ" ou "APPROUVÉ" du metasuperviseur est requis pour passer de l'Étape 7 à l'Étape 8.
Rapports d'Avancement : Des synthèses régulières basées sur SUIVI_MIGRATION_AGENTS.md pourront être demandées.

Date de création du prompt : YYYY-MM-DD
Version du prompt : 2.0
Ce prompt est la seule source de vérité pour la conduite de la mission. Toute déviation doit être explicitement validée. 





### Règle : Protocole de Modification de Fichier Sécurisée

Pour pallier les instabilités de l'outil d'édition et éviter la corruption de fichiers, suivre impérativement ce processus :

1.  **Sauvegarde :** Avant toute modification, créer une copie de sauvegarde du fichier (ex: `fichier.ext.bak`).
2.  **Remplacement Intégral :** Générer la totalité du nouveau contenu et écraser le fichier cible en une seule fois. Ne pas éditer de manière incrémentielle.
3.  **Vérification :** Confirmer que l'opération d'écriture a réussi et que le fichier n'est pas vide.
4.  **Tests :** Exécuter tous les tests pertinents (syntaxe, fonctionnels, et CLI).
5.  **Finalisation :**
    * **Si les tests réussissent :** Supprimer le fichier de sauvegarde.
    * **Si les tests échouent :** Restaurer immédiatement le fichier depuis la sauvegarde et analyser l'échec.