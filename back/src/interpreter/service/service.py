from src.interpreter.helper.helper_functions import parse_option_to_dict, inventory_to_dict
from src.interpreter.engine import StoryEngine
from src.core.model import load_model

class StoryService:
    def __init__(self, story_path):
        self.model = load_model(story_path, False)
        self.engine = StoryEngine()
        self.engine.interpret(self.model)
        
    def is_fight(self, room):
        return (hasattr(room, 'fight') and room.fight) or self.engine.fight_mode

    def get_view_state(self):
        if self.is_fight(self.engine.current_room):
            options = self.engine.build_fight_options()
        else:
            options = []
            for option in self.engine.available_options:
                options.append(parse_option_to_dict(option, self.engine.variables))
        return {
            "header": self.engine.current_room.header,
            "body": self.engine.current_room.body,
            "imagePath": self.engine.current_room.imagePath,
            "options": options,
            "player" : {
                "stats": {k: v for k, v in self.engine.variables.items() if k != "boss_hp"},
                "inventory": [inventory_to_dict(t) for t in self.engine.weapons]
            }
        }
    
    def select_option(self, index: int):
        if self.engine.fight_mode:
            self.engine.choose_fight_option(index)
        else:
            self.engine.select_option(index)
        return self.get_view_state()
