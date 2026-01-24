import sys
import os
from pygls.server import LanguageServer
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, 
                              CompletionItem, CompletionList, 
                              CompletionParams)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.model import get_metamodel

server = LanguageServer("story-script-server", "v0.1")

try:
    metamodel = get_metamodel()
except Exception as e:
    metamodel = None

@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams = None):
    items = []

    # basic keywords
    keywords = ["room", "item", "var", "option", "goto", "take"]
    for k in keywords:
        items.append(CompletionItem(label=k))

    # dynamic proposal from textX
    if metamodel:
        try:
            doc = server.workspace.get_document(params.text_document.uri)
            model = metamodel.model_from_str(doc.source)

            if hasattr(model, 'rooms'):
                    for room in model.rooms:
                        if room.name:
                            items.append(CompletionItem(label=room.name))
        except Exception as e:
            import re
            rooms = re.findall(r'room\s+(\w+)', doc.source)
            for r in set(rooms):
                items.append(CompletionItem(label=r))

    return CompletionList(is_incomplete=False, items=items)

if __name__ == "__main__":
    server.start_io()