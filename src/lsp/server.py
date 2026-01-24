import sys
import os
from pygls.server import LanguageServer
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, 
                              CompletionItem, CompletionList, 
                              CompletionParams)
from lsprotocol.types import (TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_OPEN,
                              Diagnostic, Position, Range)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.model import get_metamodel

server = LanguageServer("story-script-server", "v0.1")

try:
    metamodel = get_metamodel()
except Exception as e:
    metamodel = None

# autocomplete
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

# error checking
def validate(ls, params):
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    source = text_doc.source
    lines = source.splitlines()
    diagnostics = []

    try:
        metamodel.model_from_str(source)
    except Exception as e:
       if hasattr(e, 'line') and hasattr(e, 'col'):
            line_idx = e.line - 1
            col_idx = e.col - 1
            
            current_line = lines[line_idx] if line_idx < len(lines) else ""
            
            import re
            rest_of_line = current_line[col_idx:]
            word_match = re.match(r'^\S+', rest_of_line)
            
            word_length = len(word_match.group(0)) if word_match else 1

            d = Diagnostic(
                range=Range(
                    start=Position(line=line_idx, character=col_idx),
                    end=Position(line=line_idx, character=col_idx + word_length),
                ),
                message=str(e),
                source="StoryScript"
            )
            diagnostics.append(d)

    ls.publish_diagnostics(text_doc.uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params):
    validate(ls, params)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params):
    validate(ls, params)

if __name__ == "__main__":
    server.start_io()