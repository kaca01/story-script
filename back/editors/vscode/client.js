const { LanguageClient } = require('vscode-languageclient/node');
const path = require('path');

let client;

function activate(context) {
    // path to python server
    let serverModule = path.join(__dirname, '..', '..', 'src', 'lsp', 'server.py');
    
    // path to python venv
    let pythonPath = path.join(__dirname, '..', '..', 'venv', 'Scripts', 'python.exe');

    let serverOptions = {
        run: { command: pythonPath, args: [serverModule] },
        debug: { command: pythonPath, args: [serverModule] }
    };

    let clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'story' }],
    };

    client = new LanguageClient('storyLanguageServer', 'StoryScript LSP', serverOptions, clientOptions);
    client.start();
}

function deactivate() {
    if (!client) { return undefined; }
    return client.stop();
}

module.exports = { activate, deactivate };