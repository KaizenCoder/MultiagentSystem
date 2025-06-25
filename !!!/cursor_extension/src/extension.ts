// Extension Cursor pour l'environnement multi-agent
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