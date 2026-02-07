from src.interpreter.helper.helper_functions import parse_option_to_dict
from src.interpreter.engine import StoryEngine
from src.core.model import load_model

class StoryService:
    def __init__(self, story_path):
        self.model = load_model(story_path, False)
        self.engine = StoryEngine()
        self.engine.interpret(self.model)

    def get_view_state(self):
        options = []
        print("Gold:", self.engine.variables)
        print("Available options:", self.engine.available_options)
        for option in self.engine.available_options:
            options.append(parse_option_to_dict(option, self.engine.variables))
        return {
            "header": self.engine.current_room.header,
            "body": self.engine.current_room.body,
            "imagePath": self.engine.current_room.imagePath,
            "options": options,
            "player" : {
                "stats": {k: v for k, v in self.engine.variables.items() if k != "boss_hp"},
                "inventory": self.engine.inventory
            }
        }
    
    def select_option(self, index: int):
        print("-" * 30)
        self.engine.select_option(index)
        print("Selected option index:", index)
        return self.get_view_state()
