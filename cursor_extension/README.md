# Multi-Agent Orchestrator - Extension Cursor/VS Code

## Vue d'ensemble

Cette extension transforme Cursor/VS Code en une interface de développement IA avancée, permettant d'orchestrer des tâches multi-agents directement depuis l'éditeur.

## ✨ Fonctionnalités

- **🚀 Orchestration intelligente** : Sélectionnez du code et décrivez une tâche
- **👀 Vue de comparaison** : Visualisez les modifications avant de les appliquer
- **⚡ Streaming temps réel** : Suivez le progrès des agents
- **🎯 Intégration native** : Menu contextuel et raccourcis clavier
- **⚙️ Configuration flexible** : URL, timeout et paramètres personnalisables

## 🚀 Installation rapide

### Méthode 1 : Installation en développement

```bash
# Cloner le projet et aller dans le dossier extension
cd cursor_extension

# Installer les dépendances
npm install

# Compiler le code TypeScript
npm run compile

# Optionnel : Créer un package VSIX
npm run package
```

### Méthode 2 : Installation via VS Code

1. Ouvrir VS Code/Cursor
2. `Ctrl+Shift+P` → "Developer: Install Extension from Location"
3. Sélectionner le dossier `cursor_extension`

## 📋 Utilisation

### Workflow principal

1. **Sélectionner du code** dans votre éditeur
2. **Déclencher l'orchestration** :
   - Raccourci : `Ctrl+Shift+M` (Win/Linux) ou `Cmd+Shift+M` (Mac)
   - Menu contextuel : Clic droit → "Orchestrate with Multi-Agent"
   - Palette : `Ctrl+Shift+P` → "Multi-Agent: Orchestrate with Multi-Agent"

3. **Décrire la tâche** dans la boîte de dialogue :
   ```
   Exemples :
   - "Ajouter des tests unitaires pour cette fonction"
   - "Améliorer la documentation avec des exemples"
   - "Optimiser les performances de ce code"
   - "Ajouter la gestion d'erreurs"
   ```

4. **Suivre le progrès** via la barre de progression

5. **Examiner les modifications** dans la vue de comparaison

6. **Accepter ou rejeter** les changements :
   - ✅ **Accepter** : `Ctrl+Shift+P` → "Multi-Agent: Accept Agent Changes"
   - ❌ **Rejeter** : `Ctrl+Shift+P` → "Multi-Agent: Reject Agent Changes"

## ⚙️ Configuration

### Paramètres disponibles

```json
{
  "multiAgent.orchestratorUrl": "http://localhost:8002/invoke",
  "multiAgent.showDiff": true,
  "multiAgent.timeout": 90000
}
```

### Description des paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `orchestratorUrl` | string | `http://localhost:8002/invoke` | URL de l'endpoint d'orchestration |
| `showDiff` | boolean | `true` | Afficher la vue de comparaison |
| `timeout` | number | `90000` | Timeout en millisecondes (90s) |

### Modifier la configuration

1. **Via VS Code** : `File` → `Preferences` → `Settings`
2. **Rechercher** : "Multi-Agent"
3. **Modifier** les valeurs selon vos besoins

## 🛠️ Développement

### Structure du projet

```
cursor_extension/
├── package.json          # Configuration de l'extension
├── tsconfig.json         # Configuration TypeScript
├── src/
│   └── extension.ts      # Code principal de l'extension
├── out/                  # Code compilé
└── README.md            # Cette documentation
```

### Scripts disponibles

```bash
# Compiler le TypeScript
npm run compile

# Compiler en mode watch (développement)
npm run watch

# Linter le code
npm run lint

# Créer un package VSIX
npm run package
```

### API de l'orchestrateur

L'extension communique avec l'orchestrateur via l'endpoint `/invoke` :

```typescript
// Payload envoyé
{
  "task_description": "Description de la tâche",
  "code_context": "Code sélectionné"
}

// Réponse attendue (streaming)
{
  "session_id": "uuid",
  "results": {
    "code_generation": "Code généré",
    "documentation": "Documentation ajoutée"
  },
  "errors": []
}
```

## 🐛 Dépannage

### L'extension ne se charge pas

1. Vérifiez que les dépendances sont installées : `npm install`
2. Compilez le code : `npm run compile`
3. Redémarrez VS Code/Cursor

### Erreur de connexion à l'orchestrateur

1. Vérifiez que les services Docker sont démarrés : `docker-compose ps`
2. Testez l'endpoint : `curl http://localhost:8002/status`
3. Vérifiez l'URL dans les paramètres de l'extension

### La vue de comparaison ne s'affiche pas

1. Vérifiez le paramètre `multiAgent.showDiff` dans les settings
2. Assurez-vous qu'il y a du contenu sélectionné
3. Consultez la console de développement : `Help` → `Toggle Developer Tools`

### Timeout des requêtes

1. Augmentez la valeur de `multiAgent.timeout` dans les settings
2. Vérifiez la performance de votre système
3. Consultez les logs de l'orchestrateur : `docker-compose logs orchestrator`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature : `git checkout -b feature/nouvelle-fonctionnalite`
3. Commit les changements : `git commit -am 'Ajouter nouvelle fonctionnalité'`
4. Push vers la branche : `git push origin feature/nouvelle-fonctionnalite`
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🔗 Liens utiles

- [Documentation VS Code Extension API](https://code.visualstudio.com/api)
- [Guide de publication d'extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Marketplace VS Code](https://marketplace.visualstudio.com/vscode) 