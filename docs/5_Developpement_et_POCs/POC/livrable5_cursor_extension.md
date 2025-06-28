# Livrable 5 : Extension Cursor pour VS Code

| Élément | Description |
|---------|-------------|
| **package.json** | Déclare la commande `multiAgent.orchestrateTask`, raccourci clavier et paramètres utilisateur (URL, timeout). |
| **extension.ts** | 1. Récupère la sélection et la description de tâche<br>2. Envoie `POST /invoke` à l’orchestrateur<br>3. Gère le streaming SSE, agrège les réponses et remplace la sélection<br>4. Affiche une barre de statut et un channel de log. |

```plaintext
User flow : Sélectionnez du code → Cmd/Ctrl+Shift+P → Multi‑Agent : Orchestrate  
Décrivez la tâche → Suivez la barre de statut → Le code/documentation généré
remplace la sélection.
```

> L’extension offre une intégration directe de l’orchestrateur multi‑agent
dans l’éditeur, améliorant la productivité sans quitter VS Code.
Cette version est complète, commentée et prête à l'emploi. Elle transforme l'extension d'un simple outil de remplacement de texte en une véritable interface de développement interactive et professionnelle pour votre système multi-agents.

Livrable 5 : Intégration Cursor (Extension VS Code) - Version Complète et Optimisée
Ce livrable contient les trois fichiers nécessaires pour l'extension.

1. Fichier : cursor_extension/package.json
Ce fichier définit les métadonnées, les commandes, les raccourcis, les configurations et les dépendances de l'extension. Il est enrichi pour offrir une expérience utilisateur complète.

JSON

{
  "name": "multi-agent-orchestrator",
  "displayName": "Multi-Agent Orchestrator",
  "description": "Extension professionnelle pour orchestrer des tâches multi-agents depuis Cursor/VS Code",
  "version": "1.0.1",
  "publisher": "votre-nom-editeur",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": [
    "Other",
    "Programming Languages"
  ],
  "keywords": ["AI", "multi-agent", "langgraph", "code generation", "automation"],
  "icon": "images/icon.png",
  "activationEvents": [
    "onCommand:multiAgent.orchestrateTask",
    "onCommand:multiAgent.acceptChanges",
    "onCommand:multiAgent.rejectChanges"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "multiAgent.orchestrateTask",
        "title": "Orchestrate with Multi-Agent",
        "category": "Multi-Agent",
        "icon": "$(rocket)"
      },
      {
        "command": "multiAgent.acceptChanges",
        "title": "Accept Agent Changes",
        "category": "Multi-Agent",
        "icon": "$(check)"
      },
      {
        "command": "multiAgent.rejectChanges",
        "title": "Reject Agent Changes",
        "category": "Multi-Agent",
        "icon": "$(close)"
      }
    ],
    "keybindings": [
      {
        "command": "multiAgent.orchestrateTask",
        "key": "ctrl+shift+m",
        "mac": "cmd+shift+m",
        "when": "editorTextFocus && editorHasSelection"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "command": "multiAgent.orchestrateTask",
          "when": "editorHasSelection",
          "group": "1_modification"
        }
      ]
    },
    "configuration": {
      "title": "Multi-Agent Orchestrator",
      "properties": {
        "multiAgent.orchestratorUrl": {
          "type": "string",
          "default": "http://localhost:8002/invoke",
          "description": "URL de l'endpoint /invoke du service d'orchestration."
        },
        "multiAgent.showDiff": {
          "type": "boolean",
          "default": true,
          "description": "Afficher une vue de comparaison (diff) au lieu de remplacer directement le code."
        },
        "multiAgent.timeout": {
          "type": "number",
          "default": 90000,
          "description": "Timeout en millisecondes pour les requêtes API vers le service d'orchestration."
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "lint": "eslint src --ext ts",
    "package": "vsce package"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "20.x",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0",
    "eslint": "^8.56.0",
    "typescript": "^5.3.3",
    "vsce": "^2.15.0"
  },
  "dependencies": {
    "node-fetch": "^3.3.2"
  }
}
2. Fichier : cursor_extension/tsconfig.json
Fichier de configuration TypeScript standard pour compiler le code de l'extension.

JSON

{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2022",
    "outDir": "out",
    "lib": ["ES2022"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
3. Fichier : cursor_extension/src/extension.ts
C'est le cœur de l'extension. Ce code contient toute la logique pour interagir avec l'utilisateur et le backend, y compris la gestion de la vue diff, le suivi de la progression et l'application des modifications.

TypeScript

import * as vscode from 'vscode';
import fetch, { Response } from 'node-fetch';

// Interface pour stocker les résultats de l'agent
interface TaskResult {
    session_id: string;
    results: {
        code_generation?: string;
        documentation?: string;
    };
    errors: string[];
}

// Classe pour fournir le contenu des documents virtuels pour la vue de comparaison
class DiffContentProvider implements vscode.TextDocumentContentProvider {
    private originalContent: string = '';
    private modifiedContent: string = '';

    // Met à jour le contenu à afficher dans la vue de comparaison
    public setContents(original: string, modified: string) {
        this.originalContent = original;
        this.modifiedContent = modified;
    }

    // Fournit le contenu en fonction de l'URI demandé (original ou modifié)
    provideTextDocumentContent(uri: vscode.Uri): string {
        if (uri.path.startsWith('/original')) {
            return this.originalContent;
        }
        if (uri.path.startsWith('/modified')) {
            return this.modifiedContent;
        }
        return `Contenu non trouvé pour ${uri.toString()}`;
    }
}

// Fonction principale d'activation de l'extension
export function activate(context: vscode.ExtensionContext) {
    console.log('Multi-Agent Orchestrator extension is now active!');

    const provider = new DiffContentProvider();

    // Enregistrement du fournisseur de contenu pour notre schéma d'URI personnalisé
    context.subscriptions.push(
        vscode.workspace.registerTextDocumentContentProvider('multi-agent', provider)
    );

    // Enregistrement de la commande principale pour orchestrer une tâche
    const orchestrateCommand = vscode.commands.registerCommand(
        'multiAgent.orchestrateTask',
        () => orchestrateTaskWithDiff(context, provider)
    );

    // Commande pour accepter les changements de la vue de comparaison
    const acceptCommand = vscode.commands.registerCommand(
        'multiAgent.acceptChanges',
        () => acceptChanges(context)
    );

    // Commande pour rejeter les changements
    const rejectCommand = vscode.commands.registerCommand(
        'multiAgent.rejectChanges',
        rejectChanges
    );

    context.subscriptions.push(orchestrateCommand, acceptCommand, rejectCommand);
}

// Fonction principale du workflow utilisateur
async function orchestrateTaskWithDiff(context: vscode.ExtensionContext, provider: DiffContentProvider) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('Aucun éditeur de texte actif.');
        return;
    }

    const selection = editor.selection;
    const selectedText = editor.document.getText(selection);
    if (selection.isEmpty) {
        vscode.window.showWarningMessage('Veuillez sélectionner du code à modifier.');
        return;
    }

    const taskDescription = await vscode.window.showInputBox({
        prompt: 'Décrivez la tâche à accomplir par les agents',
        placeHolder: 'Ex: "Ajoute des tests unitaires et améliore la documentation."',
        ignoreFocusOut: true,
    });

    if (!taskDescription) {
        return; // L'utilisateur a annulé
    }

    // Sauvegarder le contexte original pour pouvoir l'utiliser plus tard
    context.workspaceState.update('originalUri', editor.document.uri.toString());
    context.workspaceState.update('originalSelection', selection);

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Orchestration Multi-Agents",
        cancellable: true
    }, async (progress, token) => {
        try {
            progress.report({ increment: 10, message: "Envoi de la tâche aux agents..." });

            const config = vscode.workspace.getConfiguration('multiAgent');
            const orchestratorUrl = config.get<string>('orchestratorUrl', 'http://localhost:8002/invoke');
            const timeout = config.get<number>('timeout', 90000);

            // Appel API
            const response = await callOrchestratorAPI(orchestratorUrl, taskDescription, selectedText, timeout, token);
            if (token.isCancellationRequested) return;

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status} ${response.statusText}`);
            }

            // Traitement de la réponse en streaming
            progress.report({ increment: 30, message: "Les agents travaillent..." });
            const result = await processStreamingResponse(response, progress);
            if (!result || !result.results) {
                throw new Error('Aucun résultat valide reçu des agents.');
            }

            // Combinaison des résultats
            const modifiedCode = result.results.code_generation || selectedText;
            const documentation = result.results.documentation ? `\n\n"""\n${result.results.documentation}\n"""` : '';
            const finalContent = modifiedCode + documentation;

            // Mettre à jour le contenu pour la vue de comparaison et l'état de l'extension
            provider.setContents(selectedText, finalContent);
            context.workspaceState.update('modifiedContent', finalContent);

            progress.report({ increment: 100, message: "Affichage des modifications." });

            // Afficher la vue de comparaison
            await showDiffView(editor.document, taskDescription);

        } catch (error: any) {
            if (!token.isCancellationRequested) {
                vscode.window.showErrorMessage(`Erreur d'orchestration: ${error.message}`);
            }
        }
    });
}

// Ouvre la vue de comparaison native de VS Code
async function showDiffView(originalDoc: vscode.TextDocument, taskDescription: string) {
    const originalUri = vscode.Uri.parse(`multi-agent:/original/${originalDoc.fileName}?task=${encodeURIComponent(taskDescription)}`);
    const modifiedUri = vscode.Uri.parse(`multi-agent:/modified/${originalDoc.fileName}?task=${encodeURIComponent(taskDescription)}`);

    const title = `🤖 Agent: ${taskDescription.slice(0, 30)}...`;

    await vscode.commands.executeCommand('vscode.diff', originalUri, modifiedUri, title, {
        preview: true,
        viewColumn: vscode.ViewColumn.Beside,
    });
}

// Applique les modifications proposées
async function acceptChanges(context: vscode.ExtensionContext) {
    const originalUriString = context.workspaceState.get<string>('originalUri');
    const originalSelection = context.workspaceState.get<vscode.Selection>('originalSelection');
    const modifiedContent = context.workspaceState.get<string>('modifiedContent');

    if (!originalUriString || !originalSelection || modifiedContent === undefined) {
        vscode.window.showErrorMessage('Impossible d\'appliquer les changements : contexte original non trouvé.');
        return;
    }

    const originalUri = vscode.Uri.parse(originalUriString);
    const targetEditor = vscode.window.visibleTextEditors.find(e => e.document.uri.toString() === originalUri.toString());

    if (targetEditor) {
        await targetEditor.edit(editBuilder => {
            editBuilder.replace(originalSelection, modifiedContent);
        });
        vscode.window.showInformationMessage('✅ Changements appliqués avec succès !');

        // Fermer la vue de comparaison
        await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    } else {
        vscode.window.showWarningMessage('Le document original n\'est pas ouvert. Veuillez l\'ouvrir pour appliquer les changements.');
    }
}

// Rejette les modifications et ferme la vue de comparaison
async function rejectChanges() {
    await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    vscode.window.showInformationMessage('❌ Changements rejetés.');
}

// Fonction pour appeler l'API de l'orchestrateur
async function callOrchestratorAPI(url: string, taskDescription: string, codeContext: string, timeout: number, token: vscode.CancellationToken): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    token.onCancellationRequested(() => {
        controller.abort();
    });

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task_description: taskDescription,
                code_context: codeContext
            }),
            signal: controller.signal as any,
        });
        return response;
    } finally {
        clearTimeout(timeoutId);
    }
}

// Traite la réponse en streaming (Server-Sent Events)
async function processStreamingResponse(response: Response, progress: vscode.Progress<{ message?: string, increment?: number }>): Promise<TaskResult | null> {
    const reader = response.body;
    if (!reader) {
        throw new Error('Impossible de lire la réponse du service.');
    }
    
    const decoder = new TextDecoder();
    let finalResult: TaskResult | null = null;
    let buffer = '';

    for await (const chunk of reader) {
        buffer += decoder.decode(chunk as Buffer, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
            if (line.startsWith('event:')) {
                const eventName = line.substring(6).trim();
                progress.report({ increment: 15, message: `Étape : ${eventName}...` });
            } else if (line.startsWith('data:')) {
                try {
                    const data = JSON.parse(line.substring(5));
                    // Chercher le dernier état complet dans le stream
                    if (data.supervisor?.task_status === 'completed' || data.supervisor?.task_status === 'failed') {
                        finalResult = data.supervisor;
                    }
                } catch (e) {
                    // Ignorer les erreurs de parsing JSON, cela peut arriver avec des streams partiels
                }
            }
        }
    }
    return finalResult;
}

// Fonction de désactivation de l'extension
export function deactivate() {
    console.log('Multi-Agent Orchestrator extension is now deactivated.');
}