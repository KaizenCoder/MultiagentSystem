# 🛠️ Wiki des Outils Spécialisés de NextGeneration

## 1. 🚀 Vue d'ensemble et Philosophie

Ce wiki sert de catalogue et de guide pour la suite d'outils spécialisés développés pour l'écosystème NextGeneration. Contrairement aux composants de l'infrastructure de base, ces outils sont des applications autonomes conçues pour résoudre des problèmes spécifiques liés à la performance, au déploiement, à la gestion de projet et à l'intégration avec des systèmes tiers.

Chaque outil est conçu pour être modulaire, avec sa propre configuration, sa documentation et ses tests, tout en s'intégrant au système de monitoring et de logging centralisé du projet.

## 2. 🎤 Outils de Synthèse Vocale (TTS)

Un pôle d'expertise a été développé autour de la technologie Text-to-Speech (TTS) pour des besoins d'interaction vocale.

### `tts_dependencies_installer`
- **Rôle** : Installateur et configurateur.
- **Description** : Cet outil est le point d'entrée pour quiconque souhaite utiliser les capacités TTS du projet. Il automatise l'installation complexe de toutes les dépendances nécessaires, y compris le moteur de synthèse vocale **Piper TTS**, les librairies audio, et surtout, les composants pour l'accélération GPU via la **RTX 3090** (CUDA, PyTorch).
- **Usage typique** : Exécuté une seule fois pour préparer un environnement de développement.

### `tts_performance_monitor`
- **Rôle** : Outil de surveillance et d'optimisation.
- **Description** : Une fois le système TTS installé, ce moniteur permet de suivre en temps réel ses performances. Il ne se contente pas de surveiller l'usage des ressources (GPU, CPU), mais analyse aussi la qualité de la voix générée (clarté, naturalité). Il peut même ajuster les paramètres à la volée et dispose d'un dashboard web pour la visualisation.
- **Usage typique** : Lancé en arrière-plan pendant l'utilisation des fonctionnalités TTS.

## 3. 💼 Outils d'Intégration et de Gestion

Ce sont les outils qui connectent NextGeneration à d'autres écosystèmes ou qui gèrent le cycle de vie du projet.

### `excel_vba_tools_launcher`
- **Rôle** : Pont avec le monde Microsoft Office.
- **Description** : Cet outil sert de lanceur universel pour les scripts et macros VBA/Excel, notamment ceux provenant d'un framework tiers nommé Apex. Il permet de générer des rapports Excel automatisés et de lancer des traitements de données, offrant une interface web pour la gestion des tâches.
- **Usage typique** : Planifié pour générer des rapports périodiques ou lancé manuellement pour des traitements de données spécifiques.

### `project_backup_system`
- **Rôle** : Assurance vie du projet.
- **Description** : Un système de sauvegarde de niveau "entreprise", entièrement configurable. Il crée des archives ZIP optimisées en excluant intelligemment les fichiers inutiles (`.git`, caches...). Il peut être configuré pour s'exécuter automatiquement via le planificateur de tâches Windows et intègre des mécanismes de sécurité pour valider l'intégrité des sauvegardes.
- **Usage typique** : Configuré une fois, il tourne en arrière-plan pour assurer la sécurité des données du projet.

### `generate_pitch_document`
- **Rôle** : Générateur de documentation projet.
- **Description** : Cet outil analyse le code source du projet pour en extraire les fonctionnalités, les métriques et les graphiques pertinents, et les assemble automatiquement dans un document de présentation ("pitch") professionnel.
- **Usage typique** : Utilisé pour générer des rapports d'avancement ou des présentations pour des parties prenantes.

## 4. 🗑️ Outils Dépréciés

### `legacy_imported_tools`
- **Rôle** : Archive historique.
- **Description** : Ce répertoire contient une ancienne version des outils importés. Il ne doit plus être utilisé et est conservé uniquement pour des raisons historiques. Les fonctionnalités sont maintenant couvertes par les outils spécialisés ci-dessus. 