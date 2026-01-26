import sys
import os
from pygls.server import LanguageServer
from textx import get_children_of_type
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, 
                              CompletionItemKind,
                              CompletionItem, CompletionList, 
                              CompletionParams)
from lsprotocol.types import (TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_OPEN,
                              Diagnostic, Position, Range)
from lsprotocol.types import (TEXT_DOCUMENT_DEFINITION, Location)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.model import get_metamodel

server = LanguageServer("story-script-server", "v0.1")

try:
    metamodel = get_metamodel()
except Exception as e:
    metamodel = None

# go to definition
@server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(ls, params):
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    source = text_doc.source
    
    line_num = params.position.line
    col_num = params.position.character
    lines = source.splitlines()
    if line_num >= len(lines): return None
    
    import re
    line = lines[line_num]
    words = re.finditer(r'\b\w+\b', line)
    target_word = ""
    for m in words:
        if m.start() <= col_num <= m.end():
            target_word = m.group()
            break

    if not target_word: return None

    try:
        model = metamodel.model_from_str(source)
        
        search_configs = [
            (metamodel['Room'], 'room'),
            (metamodel['Variable'], 'var'),
            (metamodel['Item'], 'item'),
            (metamodel['GlobalRule'], 'rule')
        ]

        for cls, keyword in search_configs:
            entities = get_children_of_type(cls, model)
            for ent in entities:
                if ent.name == target_word:
                    for idx, l in enumerate(lines):
                        if re.search(rf'\b{keyword}\s+{target_word}\b', l):
                            return Location(
                                uri=params.text_document.uri,
                                range=Range(
                                    start=Position(line=idx, character=0),
                                    end=Position(line=idx, character=len(l))
                                )
                            )
    except:
        patterns = [r'\broom\s+', r'\bvar\s+', r'\bitem\s+', r'\brule\s+']
        for p in patterns:
            for idx, l in enumerate(lines):
                if re.search(p + target_word + r'\b', l):
                    return Location(
                        uri=params.text_document.uri,
                        range=Range(
                            start=Position(line=idx, character=0),
                            end=Position(line=idx, character=len(l))
                        )
                    )
    return None

# autocomplete
@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams = None):
    items = []
    doc = server.workspace.get_document(params.text_document.uri)

    # basic keywords
    keywords = ["room", "item", "var", "option", "goto", "take", "rule", "set", "weight"]
    for k in keywords:
        items.append(CompletionItem(label=k))

    # dynamic proposal
    if metamodel:
        try:
            model = metamodel.model_from_str(doc.source)

            if hasattr(model, 'variables'):
                for v in model.variables:
                    items.append(CompletionItem(label=v.name, kind=CompletionItemKind.Variable))
            
            if hasattr(model, 'items'):
                for i in model.items:
                    items.append(CompletionItem(label=i.name, kind=CompletionItemKind.Struct))
            
            if hasattr(model, 'globalRules'):
                for r in model.globalRules:
                    items.append(CompletionItem(label=r.name, kind=CompletionItemKind.Function))
            
            if hasattr(model, 'rooms'):
                for room in model.rooms:
                    items.append(CompletionItem(label=room.name, kind=CompletionItemKind.Class))

        except Exception as e:
            import re
            
            patterns = {
                'var': (r'var\s+(\w+)', CompletionItemKind.Variable),
                'item': (r'item\s+(\w+)', CompletionItemKind.Struct),
                'rule': (r'rule\s+(\w+)', CompletionItemKind.Function),
                'room': (r'room\s+(\w+)', CompletionItemKind.Class)
            }
            
            for key, (pattern, kind) in patterns.items():
                found = re.findall(pattern, doc.source)
                for name in set(found):
                    items.append(CompletionItem(label=name, kind=kind))

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