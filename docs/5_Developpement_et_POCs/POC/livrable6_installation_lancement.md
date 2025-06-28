# Livrable 6 : Procédure d’installation et de lancement

## Prérequis
- Docker Desktop  
- Node.js ≥ 18  
- Python 3.11+

## Étapes

1. **Cloner** le dépôt :  
   ```bash
   git clone <repo-url>
   cd <repo>
   ```
2. **Configurer** les secrets :  
   ```bash
   cp .env.example .env
   # éditer .env pour ajouter les clés OpenAI/Anthropic
   ```
3. **Démarrer** l’environnement Docker :  
   ```bash
   docker-compose up --build -d
   ```
4. **Installer** l’extension Cursor :  
   ```bash
   cd cursor_extension
   npm install
   npm run compile
   code --install-extension cursor-extension-0.0.1.vsix
   ```
5. **Exemple de workflow** :  
   - Sélectionner un bloc de code  
   - Exécuter la commande **Multi‑Agent : Orchestrate Task**  
   - Décrire la tâche (ex. “optimise cette fonction et ajoute la docstring”)  

> En quelques commandes, l’ensemble du stack (API mémoire, orchestrateur,
vector store et extension VS Code) est opérationnel sur votre machine locale.
