import os
from textx import metamodel_from_file
from src.core.validator import validate_model 

def get_metamodel(debug=False):
    current_dir = os.path.dirname(__file__)
    grammar_path = os.path.join(current_dir, '../grammar/story.tx')
    return metamodel_from_file(grammar_path, debug=debug)

def load_model(file_path, debug=False):
    mm = get_metamodel(debug)    
    model = mm.model_from_file(file_path, debug=debug)
    validate_model(model)
    
    return model