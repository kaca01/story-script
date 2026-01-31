from src.interpreter.helper.helper_functions import parse_operator, evaluate_expression, parse_option_to_dict

# TODO: rules and go back are not implemented
# for go back add ID (int) for each item
# when user enters room if items are already taken,
# user can release them and move on
class StoryEngine:
    def __init__(self):
        self.variables = {}
        self.items = {}  # values are weights
        self.collected_items = []
        self.current_room = None
        self.available_options = []
    
    
    def __str__(self):
        return f"StoryEngine(variables={self.variables}, collected_items={self.collected_items}, current_room={self.current_room})"
    
    def interpret(self, model):
        self.populate_variables(model.variables)
        self.populate_items(model.items)
        self.current_room = model.rooms[0]
        self.available_options = self.filter_available_options(self.current_room.options)
        print("-" * 50)
        print(f"Interpreting room: {self.current_room.name}")
    
    def populate_variables(self, variables):
        for var in variables:
            self.variables[var.name] = var.value
            print(f"Initialized variable: {var.name} = {var.value}")
    
    def populate_items(self, items):
        for item in items:
            self.items[item.name] = item.weight
            print(f"Initialized item: {item.name} weight {item.weight}")
            
    def select_option(self, inp):
        selected_option = self.available_options[inp]
        self.take_action(selected_option.action)
        self.current_room = selected_option.target
        self.available_options = self.filter_available_options(self.current_room.options)
    
    def take_action(self, action):
        if action is None:
            print("No actions here")
            return
        if action.item is not None:
            self.collected_items.append(action.item.name)
        for assignment in action.assignments:
            res = evaluate_expression(assignment.exp, self.variables)
            self.variables[assignment.varName.name] = res
            print(self.variables)
            
    def filter_available_options(self, options):
        available_options = []
        for option in options:
            if option.condition != None:
                variable = option.condition.varName.name
                value = option.condition.val
                if (parse_operator(option.condition.op)(self.variables[variable], value)):
                    available_options.append(option)
            else:
                available_options.append(option)
        return available_options
    
    def has_game_ended(self, options):
        if len(options) == 1 and self.current_room.name == options[0].target.name:
            return True
        return False
