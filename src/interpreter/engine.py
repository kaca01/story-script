from src.core.model import load_model
from src.interpreter.helper.helper_functions import parse_operator, evaluate_expression
import os

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
    
    def __str__(self):
        return f"StoryEngine(variables={self.variables}, collected_items={self.collected_items}, current_room={self.current_room})"
    
    def interpret(self, model):
        self.populate_variables(model.variables)
        self.populate_items(model.items)
        self.current_room = model.rooms[0]
        while True:
            if self.has_game_ended(self.current_room.options):
                print("Game over!")
                break
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
        for option in available_options:
            i += 1
            print(str(i) + " - " + option.text + " go to " + option.target.header)
        inp = int(input("Select an option: "))
        selected_option = available_options[inp - 1]
        self.take_action(selected_option.action)
        self.current_room = selected_option.target
    

    def take_action(self, action):
        if action is None:
            print("No actions here")
            return
        
        # 1. check items
        if action.item is not None:
            self.collected_items.append(action.item.name)
            print(f"Picked up item: {action.item.name}")

        # 2. check actions
        for element in action.elements:
            # if is the variable
            if hasattr(element, 'varName'): 
                res = evaluate_expression(element.exp, self.variables)
                self.variables[element.varName.name] = res
                print(f"Variable updated: {element.varName.name} = {res}")
            
            # if is the rule
            elif hasattr(element, 'rule'):
                print(f"Executing rule: {element.rule.name}")
                for rule_assignment in element.rule.assignments:
                    res = evaluate_expression(rule_assignment.exp, self.variables)
                    self.variables[rule_assignment.varName.name] = res
                    print(f"Rule update: {rule_assignment.varName.name} = {res}")
        
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
        if (len(options) == 1 and self.current_room.name == options[0].target.name):
            return True
        return False


