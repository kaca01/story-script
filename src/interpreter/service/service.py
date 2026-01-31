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
        for option in self.engine.available_options:
            options.append(parse_option_to_dict(option, self.engine.variables))
        return {
            "header": self.engine.current_room.header,
            "body": self.engine.current_room.body,
            "imagePath": self.engine.current_room.imagePath,
            "options": options,
        }
    
    def select_option(self, index: int):
        self.engine.select_option(index)
        return self.get_view_state()
