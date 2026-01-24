from src.core.model import load_model
import os


class StoryEngine:
    def __init__(self):
        self.variables = {}
        self.items = {}
        self.collected_items = []
        self.current_room = None
    
    def __str__(self):
        return f"StoryEngine(variables={self.variables}, collected_items={self.collected_items}, current_room={self.current_room})"
    
    def interpret(self, model):
        for room in model.rooms:
            print("-" * 50)
            print(f"Interpreting room: {room.name}")
            self.select_option(room)
            
    def select_option(self, room):
        print("Your options are: ")
        i = 0
        for option in room.options:
            i += 1
            print(str(i) + " - " + option.text + " go to " + option.target.header)
            
    
def run_engine(debug=False):
    # TODO: implement debug
    path = os.path.join(os.path.dirname(__file__), '../../examples/lostTemple.story')
    story_model = load_model(path)
    story_engine = StoryEngine()
    story_engine.interpret(story_model)
