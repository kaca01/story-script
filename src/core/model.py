from textx import metamodel_from_file
import os

def get_metamodel():
    current_dir = os.path.dirname(__file__)
    # Putanja do tvoje gramatike
    grammar_path = os.path.join(current_dir, '../../grammar/story.tx')
    return metamodel_from_file(grammar_path)

def load_model(file_path):
    mm = get_metamodel()
    return mm.model_from_file(file_path)