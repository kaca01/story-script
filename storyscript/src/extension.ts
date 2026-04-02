import * as path from 'path';
import { ExtensionContext, workspace } from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    const rootPath = path.join(context.extensionPath, '..');

    const serverModule = path.join(rootPath, 'back', 'src', 'lsp', 'server.py');
    const pythonPath = path.join(rootPath, 'back', 'venv', 'Scripts', 'python.exe');

    let serverOptions: ServerOptions = {
        command: pythonPath, 
        args: [serverModule]
    };

    let clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'storyscript' }],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/.story')
        }
    };

    client = new LanguageClient('storyServer', 'Story Language Server', serverOptions, clientOptions);
    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}