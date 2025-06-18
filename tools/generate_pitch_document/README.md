# Outil : Générateur de Document de Présentation

Cet outil automatise la création d'un document Markdown complet (`PITCH`) pour le projet NextGeneration. Il fusionne un modèle de base avec l'arborescence actuelle du projet et le contenu intégral de tous les fichiers pertinents.

## 🎯 Objectif

Produire un document "single source of truth" à destination d'experts externes, de nouveaux membres de l'équipe, ou pour des revues d'architecture.

## ⚙️ Utilisation

Le script est conçu pour être lancé depuis la racine du projet NextGeneration.

### Prérequis

- Python 3

### Commande

```bash
python tools/generate_pitch_document/generate_pitch_document.py [options]
```

### Options

-   `--template <fichier>` : Spécifie le chemin vers le fichier modèle Markdown.
    -   **Défaut :** `PITCH_NEXTGENERATION.md`
-   `--output <fichier>` : Spécifie le chemin vers le fichier de sortie final.
    -   **Défaut :** `PITCH_NEXTGENERATION_FINAL.md`

### Exemple

Pour exécuter avec les paramètres par défaut :

```bash
python tools/generate_pitch_document/generate_pitch_document.py
```

## 🛠️ Fonctionnement Interne

1.  **Lecture du Modèle** : Le script charge le contenu du fichier `--template`.
2.  **Génération de l'Arborescence** : Il analyse la structure du projet (en excluant les dossiers comme `.git`, `node_modules`, etc.) et génère une arborescence textuelle.
3.  **Intégration du Codebase** : Il parcourt tous les fichiers non exclus, lit leur contenu, et l'encapsule dans des blocs de code Markdown repliables (`<details>`).
4.  **Assemblage Final** : Il remplace les placeholders dans le modèle par l'arborescence et le codebase, puis écrit le résultat dans le fichier `--output`. 