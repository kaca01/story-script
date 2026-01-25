from src.core.model import load_model
from src.interpreter.helper.helper_functions import parse_operator
import os


class StoryEngine:
    def __init__(self):
        self.variables = {}
        self.items = {}  # values are weights
        self.collected_items = []
        self.current_room = None
    
    def __str__(self):
        return f"StoryEngine(variables={self.variables}, collected_items={self.collected_items}, current_room={self.current_room})"
    
    def interpret(self, model):
        self.populate_variables(model.variables)
        self.populate_items(model.items)
        self.current_room = model.rooms[0]
        while True:
            print("-" * 50)
            print(f"Interpreting room: {self.current_room.name}")
            self.select_option(self.current_room.options)
    
    def populate_variables(self, variables):
        for var in variables:
            self.variables[var.name] = var.value
            print(f"Initialized variable: {var.name} = {var.value}")
    
    def populate_items(self, items):
        for item in items:
            self.items[item.name] = item.weight
            print(f"Initialized item: {item.name} weight {item.weight}")
            
    def select_option(self, options):
        available_options = self.filter_available_options(options)
        print("Your options are: ")
        i = 0
        for option in options:
            i += 1
            print(str(i) + " - " + option.text + " go to " + option.target.header)
        inp = int(input("Select an option: "))
        selected_option = options[inp - 1]
        self.current_room = selected_option.target
        
    def filter_available_options(self, options):
        available_options = []
        for option in options:
            if option.condition != None:
                variable = option.condition.varName.name
                value = option.condition.val
                print(variable + option.condition.op + str(value))
                if (parse_operator(option.condition.op)(self.variables[variable], value)):
                    print("passed")
    

def run_engine(debug=False):
    # TODO: implement debug
    path = os.path.join(os.path.dirname(__file__), '../../examples/lostTemple.story')
    story_model = load_model(path)
    story_engine = StoryEngine()
    story_engine.interpret(story_model)
