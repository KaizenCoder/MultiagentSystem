# 🚀 PROMPT MISSION : FINALISATION DE LA TRANSPOSITION SUPERWHISPER_V6

## 🎯 **CONTEXTE**

Suite à l'implémentation réussie de l'agent `generate_bundle_nextgeneration.py`, cette mission vise à accomplir les trois objectifs restants de la transposition des meilleures pratiques de SuperWhisper_V6, comme défini dans le document de mission original.

L'objectif est de capitaliser sur l'infrastructure existante pour produire rapidement une documentation et des workflows de haute qualité.

## ✅ **AXES DE TRAVAIL & LIVRABLES**

### **Axe 1 : Procédures de Transmission Standardisées**

**Objectif :** Formaliser les processus clés du projet pour améliorer la qualité et la transmission des connaissances.
**Répertoire cible :** `docs/procedures/`

**Livrables :**
1.  **`TRANSMISSION_COORDINATEUR.md`** : Créer une procédure standardisée avec une checklist complète pour la transmission des missions entre les coordinateurs et les agents.
2.  **`ON_BOARDING_IA_NEXTGENERATION.md`** : Rédiger un guide d'onboarding pour les futures IA, décrivant l'architecture, les outils disponibles, et les conventions à respecter.
3.  **`CHECKLIST_QUALITE.md`** : Définir les critères d'acceptation techniques et fonctionnels pour les nouvelles fonctionnalités, les nouveaux agents et les rapports.

*Base de travail : S'inspirer du style et de la structure des guides existants (`GUIDE_*.md`).*

### **Axe 2 : Workflow de Validation et de Documentation Automatisé**

**Objectif :** Créer un script unique pour fiabiliser et accélérer le processus de validation et de documentation du projet.
**Répertoire cible :** `scripts/`

**Livrable :**
1.  **`validate_and_document.ps1`** : Créer un script PowerShell qui orchestre les actions suivantes :
    *   **Étape 1 :** Lancer les tests unitaires et d'intégration du projet.
    *   **Étape 2 (en cas de succès des tests) :** Exécuter l'agent `agent_synthese_auto_update.py` pour mettre à jour `SYNTHESE_EXECUTIVE.md` et `CHANGELOG.md`.
    *   **Étape 3 :** Exécuter l'agent `generate_bundle_nextgeneration.py` pour régénérer le `CODE-SOURCE.md`.

### **Axe 3 : Standards GPU Formalisés**

**Objectif :** Centraliser la connaissance sur la configuration matérielle pour garantir la performance et la reproductibilité.
**Répertoire cible :** `docs/RTX3090/`

**Livrables :**
1.  **`STANDARDS_GPU_NEXTGENERATION.md`** : Documenter les standards techniques, les versions de drivers, et les bibliothèques recommandées (CUDA, cuDNN) pour le matériel RTX 3090 dans le contexte de NextGeneration.
2.  **`CONFIGURATION_OPTIMALE.md`** : Fournir un guide pratique pour la configuration optimale du matériel et du système d'exploitation pour maximiser les performances des agents et de l'orchestrateur.

## 🏆 **CRITÈRES DE SUCCÈS**

- L'ensemble des 6 fichiers (`.md` et `.ps1`) sont créés, peuplés avec un contenu pertinent et de haute qualité.
- Le script `validate_and_document.ps1` est fonctionnel et exécute la chaîne de validation et de documentation comme décrit.
- La nouvelle documentation est cohérente avec le style et la terminologie du projet NextGeneration. 