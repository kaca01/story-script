import random
from src.interpreter.helper.helper_functions import parse_operator, evaluate_expression

class StoryEngine:
    def __init__(self):
        self.variables = {}
        self.weapons = []
        self.inventory = []
        self.hit_ranges = {}
        self.current_room = None
        self.available_options = []
        self.model = None


    def interpret(self, model):
        self.model = model
        self.hit_ranges = {}  
        for hr in model.hitRanges:
            start = getattr(hr, 'from_', getattr(hr, 'from', 0))
            self.hit_ranges[hr.name] = (start, hr.to)

        self.reset_game_state()


    def reset_game_state(self):
        if not self.model:
            return

        adventure_name = getattr(self.model, 'name', 'Unknown Adventure')
        print("\n" + "*" * (len(adventure_name) + 20))
        print(f"*** WELCOME TO: {adventure_name} ***")
        print("*" * (len(adventure_name) + 20))

        # 1. Reset global variables to values from the .story file
        self.variables = {}
        for var in self.model.variables:
            self.variables[var.name] = var.value
            
        # 2. Clear inventory and weapons
        self.weapons = []
        self.inventory = []
        
        # 3. Return to the first room
        self.current_room = self.model.rooms[0]
        self.refresh_room_state()


    def refresh_room_state(self):
        if hasattr(self.current_room, 'options') and self.current_room.options:
            self.available_options = self.filter_available_options(self.current_room.options)
        else:
            self.available_options = []


    def filter_available_options(self, options):
        available = []
        for opt in options:
            # check standard condition (e.g., [gold >= 15])
            condition_passed = True
            if opt.condition:
                left = evaluate_expression(opt.condition.left, self.variables)
                right = evaluate_expression(opt.condition.right, self.variables)
                operator_func = parse_operator(opt.condition.op)
                if not operator_func(left, right):
                    condition_passed = False

            # check does action kill the player?
            if condition_passed and self.is_option_safe(opt):
                available.append(opt)
                
        return available


    def is_option_safe(self, option):
        if not option.action:
            return True

        temp_vars = self.variables.copy()
        strength_key = next((k for k in temp_vars.keys() if "snaga" in k.lower() or "strength" in k.lower()), None)
        
        if not strength_key:
            return True

        if hasattr(option.action, 'item') and option.action.__class__.__name__ == "Take":
            temp_vars[strength_key] -= option.action.item.weight

        if hasattr(option.action, 'assignments'):
            for asn in option.action.assignments:
                res = evaluate_expression(asn.exp, temp_vars)
                temp_vars[asn.varName.name] = max(0, res)

        if hasattr(option.action, 'rules'):
            for rule in option.action.rules:
                for asn in rule.assignments:
                    res = evaluate_expression(asn.exp, temp_vars)
                    temp_vars[asn.varName.name] = max(0, res)

        return temp_vars[strength_key] > 0


    def select_option(self, index):
        if 0 <= index < len(self.available_options):
            selected = self.available_options[index]
            
            if selected.action:
                self.execute_action(selected.action)
            
            if selected.action != "restart":
                self.current_room = selected.target
                self.refresh_room_state()
        else:
            print("Invalid option index!")


    def execute_action(self, action):
        if action == "restart":
            self.reset_game_state()
            return

        # BUY WEAPON
        if hasattr(action, 'item') and action.__class__.__name__ == "Buy":
            weapon = action.item
            gold_var = next((k for k in self.variables.keys() if "zlato" in k.lower() or "gold" in k.lower()), None)
            
            if gold_var and self.variables[gold_var] >= weapon.value:
                self.variables[gold_var] -= weapon.value
                self.weapons.append(weapon)
                print(f"Purchased: {weapon.name}. Remaining gold: {self.variables[gold_var]}")
            else:
                print("Not enough gold!")

        # TAKE TREASURE
        elif hasattr(action, 'item') and action.__class__.__name__ == "Take":
            treasure = action.item
            if treasure.name not in [t.name for t in self.inventory]:
                self.inventory.append(treasure)
                
                # auto decrease strength based on weight
                strength_var = next((k for k in self.variables.keys() if "snaga" in k.lower() or "strength" in k.lower()), None)
                if strength_var:
                    self.variables[strength_var] = max(0, self.variables[strength_var] - treasure.weight)
                    print(f"Taken: {treasure.name}. Strength decreased by {treasure.weight}.")

            # for 'set' commands
            if hasattr(action, 'assignments'):
                for asn in action.assignments:
                    res = evaluate_expression(asn.exp, self.variables)
                    self.variables[asn.varName.name] = max(0, res)

            # for global rules
            if hasattr(action, 'rules'):
                for rule in action.rules:
                    for asn in rule.assignments:
                        res = evaluate_expression(asn.exp, self.variables)
                        self.variables[asn.varName.name] = max(0, res)


    def resolve_fight(self, fight):
        boss_hp_key = next(k for k in self.variables.keys() if "hp" in k.lower())
        player_hp_key = next(k for k in self.variables.keys() if "snaga" in k.lower() or "strength" in k.lower())
        
        b_min, b_max = (1, 5) 

        print(f"\n--- COMBAT BEGINS: {fight.hr.name} ---")
        
        while self.variables[boss_hp_key] > 0 and self.variables[player_hp_key] > 0:
            print(f"\nYour HP: {self.variables[player_hp_key]} | Boss HP: {self.variables[boss_hp_key]}")
            print("Choose your attack:")
            print("0. Punch (Random dmg based on hit_range)")
            
            for i, w in enumerate(self.weapons, 1):
                print(f"{i}. Use {w.name} (+{w.hp} dmg, one-time use)")
            
            try:
                choice = int(input("Your choice: "))
                damage_to_boss = 0
                if choice == 0:
                    p_min, p_max = self.hit_ranges.get(fight.hr.name, (1, 10))
                    damage_to_boss = random.randint(p_min, p_max)
                    print(f"You punched the boss for {damage_to_boss} dmg!")
                elif 0 < choice <= len(self.weapons):
                    used_weapon = self.weapons.pop(choice - 1)
                    damage_to_boss = used_weapon.hp
                    print(f"You swung your {used_weapon.name} for {damage_to_boss} dmg! The weapon broke.")
                else:
                    print("You missed due to an invalid choice!")

                self.variables[boss_hp_key] = max(0, self.variables[boss_hp_key] - damage_to_boss)

                if self.variables[boss_hp_key] <= 0:
                    print("The boss has been defeated!")
                    break

                damage_from_boss = random.randint(b_min, b_max)
                self.variables[player_hp_key] = max(0, self.variables[player_hp_key] - damage_from_boss)
                print(f"The boss hit you for {damage_from_boss} dmg!")

            except ValueError:
                print("Please enter a valid number!")

        if self.variables[player_hp_key] > 0:
            self.current_room = fight.winRoom
        else:
            self.current_room = fight.loseRoom
        
        self.refresh_room_state()