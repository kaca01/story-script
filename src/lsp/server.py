import sys
import os
from pygls.server import LanguageServer
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, 
                              CompletionItem, CompletionList, CompletionItemKind,
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

# definition
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
    word = re.findall(r'\w+', line)
    target_word = ""
    for w in word:
        start = line.find(w)
        if start <= col_num <= start + len(w):
            target_word = w
            break

    if not target_word: return None

    try:
        model = metamodel.model_from_str(source)
        for room in model.rooms:
            if room.name == target_word:
                for idx, l in enumerate(lines):
                    if f"room {target_word}" in l:
                        return Location(
                            uri=params.text_document.uri,
                            range=Range(
                                start=Position(line=idx, character=0),
                                end=Position(line=idx, character=len(l))
                            )
                        )
    except:
        pass
    return None

# autocomplete
@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams = None):
    items = []

    # basic keywords
    keywords = [
        "adventure", "room", "rule", "define", "strength", "gold", "luck", "boss_strength", 
        "weapon", "treasure", "option", "goto", "value", "hit_points","take", "buy", "set", 
        "fight", "win", "lose", "restart", "random"
    ]
    for words in keywords:
        items.append(CompletionItem(label=words, kind=CompletionItemKind.Keyword))

    # dynamic proposal from textX
    if metamodel:
        try:
            doc = server.workspace.get_document(params.text_document.uri)
            model = metamodel.model_from_str(doc.source)

            # proposal for rooms ('goto', 'win', 'lose')
            if hasattr(model, 'rooms'):
                for room in model.rooms:
                    items.append(CompletionItem(label=room.name))

            # proposal for weapons ('buy')
            if hasattr(model, 'weapons'):
                for weapon in model.weapons:
                    items.append(CompletionItem(label=weapon.name))

            # proposal for treasures ('take')
            if hasattr(model, 'treasures'):
                for t in model.treasures:
                    items.append(CompletionItem(label=t.name))

            # proposal for variables ('set' and conditions)
            if hasattr(model, 'variables'):
                for v in model.variables:
                    items.append(CompletionItem(label=v.name))

            # proposal for hitRanges
            if hasattr(model, 'hitRanges'):
                for hr in model.hitRanges:
                    items.append(CompletionItem(label=hr.name))

            # proposal for rules
            if hasattr(model, 'globalRules'):
                for rule in model.globalRules:
                    items.append(CompletionItem(label=rule.name))
                    
        # if the model is syntactically invalid
        except Exception as e:
            import re
            content = doc.source
            
            patterns = {
                'room': r'room\s+(\w+)',
                'weapon': r'weapon\s+(\w+)',
                'treasure': r'treasure\s+(\w+)',
                'var': r'(strength|gold|luck|boss_strength)\s+(\w+)',
                'hitrange': r'define\s+(\w+)\s*=',
                'rule': r'rule\s+(\w+)'
            }
            
            for kind, pattern in patterns.items():
                found = re.findall(pattern, content)
                for item in set(found):
                    name = item[1] if isinstance(item, tuple) else item
                    items.append(CompletionItem(label=name))

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