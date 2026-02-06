import random
from src.interpreter.helper.helper_functions import parse_operator, evaluate_expression

class StoryEngine:
    def __init__(self):
        self.variables = {}  # Stores: snaga, zlato, sreca, boss_hp...
        self.weapons = []    # List of weapon objects
        self.inventory = []  # List of treasure objects
        self.hit_ranges = {} # Maps name -> (from, to)
        self.current_room = None
        self.available_options = []

    def interpret(self, model):
        self.model = model

        self.hit_ranges = {}  
        for hr in model.hitRanges:
            start = getattr(hr, 'from_', getattr(hr, 'from', 0))
            self.hit_ranges[hr.name] = (start, hr.to)

        self.reset_game_state()

    def reset_game_state(self):
        """Vraća igru na nulti trenutak: početna soba, početni statsi, prazan ranac."""
        if not self.model:
            return

        adventure_name = getattr(self.model, 'name', 'Nepoznata Avantura')
        print("\n" + "*" * (len(adventure_name) + 20))
        print(f"*** WELCOME TO: {adventure_name} ***")
        print("*" * (len(adventure_name) + 20))

        # 1. Resetuj globalne varijable na vrednosti iz .story fajla
        self.variables = {}
        for var in self.model.variables:
            self.variables[var.name] = var.value
            
        # 2. Isprazni inventar i oružja
        self.weapons = []
        self.inventory = []
        
        # 3. Vrati igru u prvu sobu
        self.current_room = self.model.rooms[0]
        self.refresh_room_state()

    def refresh_room_state(self):
        """Updates available options based on current conditions."""
        if hasattr(self.current_room, 'options') and self.current_room.options:
            self.available_options = self.filter_available_options(self.current_room.options)
        else:
            self.available_options = []

    def filter_available_options(self, options):
        available = []
        for opt in options:
            if opt.condition:
                # evaluate_expression now handles variables like 'zlato' or 'snaga'
                left = evaluate_expression(opt.condition.left, self.variables)
                right = evaluate_expression(opt.condition.right, self.variables)
                operator_func = parse_operator(opt.condition.op)
                
                if operator_func(left, right):
                    available.append(opt)
            else:
                available.append(opt)
        return available

    def select_option(self, index):
        """Glavna metoda za navigaciju kroz konzolu ili API."""
        if 0 <= index < len(self.available_options):
            selected = self.available_options[index]
            
            if selected.action:
                self.execute_action(selected.action)
            
            # Ako akcija nije bila restart, idemo u ciljnu sobu
            # (restart nas sam prebacuje u prvu sobu)
            if selected.action != "restart":
                self.current_room = selected.target
                self.refresh_room_state()
        else:
            print("Nevalidan indeks opcije!")

    def execute_action(self, action):
        """Izvršava logiku kupovine, sakupljanja ili restarta."""
        if action == "restart":
            self.reset_game_state()
            return

        # Case 1: BUY WEAPON
        if hasattr(action, 'item') and action.__class__.__name__ == "Buy":
            weapon = action.item
            gold_var = next((k for k in self.variables.keys() if "zlato" in k.lower()), None)
            
            if gold_var and self.variables[gold_var] >= weapon.value:
                self.variables[gold_var] -= weapon.value
                self.weapons.append(weapon)
                print(f"Kupljeno: {weapon.name}. Preostalo zlata: {self.variables[gold_var]}")
            else:
                print("Nemaš dovoljno zlata!")

        # Case 2: TAKE TREASURE
        elif hasattr(action, 'item') and action.__class__.__name__ == "Take":
            treasure = action.item
            
            # Sprečavamo duplo uzimanje istog blaga ako je već u inventory-ju
            if treasure.name not in [t.name for t in self.inventory]:
                self.inventory.append(treasure)
                
                # Automatsko oduzimanje snage na osnovu težine
                strength_var = next((k for k in self.variables.keys() if "snaga" in k.lower()), None)
                if strength_var:
                    self.variables[strength_var] -= treasure.weight
                    print(f"Uzeto: {treasure.name}. Snaga opala za {treasure.weight}.")

            # Izvršavanje set komandi (npr. set zlato = zlato + 200)
            if hasattr(action, 'assignments'):
                for asn in action.assignments:
                    res = evaluate_expression(asn.exp, self.variables)
                    self.variables[asn.varName.name] = res

            # Primena globalnih pravila (ako postoje)
            if hasattr(action, 'rules'):
                for rule in action.rules:
                    for asn in rule.assignments:
                        res = evaluate_expression(asn.exp, self.variables)
                        self.variables[asn.varName.name] = res

    def resolve_fight(self, fight):
        """Interaktivna borba gde igrač bira oružje."""
        boss_hp_key = next(k for k in self.variables.keys() if "hp" in k.lower())
        player_hp_key = next(k for k in self.variables.keys() if "snaga" in k.lower())
        
        # Opseg za boss-a (ostaje slučajan)
        b_min, b_max = (1, 5) 

        print(f"\n--- BORBA POČINJE: {fight.hr.name} ---")
        
        while self.variables[boss_hp_key] > 0 and self.variables[player_hp_key] > 0:
            print(f"\nTvoj HP (Snaga): {self.variables[player_hp_key]} | Boss HP: {self.variables[boss_hp_key]}")
            print("Izaberi napad:")
            print("0. Udari rukama (Slučajan dmg iz tvog hit_range)")
            
            # Prikaz dostupnih oružja
            for i, w in enumerate(self.weapons, 1):
                print(f"{i}. Koristi {w.name} (+{w.hp} dmg, jednokratno)")
            
            try:
                choice = int(input("Tvoj izbor: "))
                
                # 1. Obračun štete koju nanosi igrač
                damage_to_boss = 0
                if choice == 0:
                    # Napad bez oružja (random)
                    p_min, p_max = self.hit_ranges.get(fight.hr.name, (1, 10))
                    damage_to_boss = random.randint(p_min, p_max)
                    print(f"Udario si boss-a pesnicama za {damage_to_boss} dmg!")
                elif 0 < choice <= len(self.weapons):
                    # Napad oružjem (fiksni hit_points)
                    used_weapon = self.weapons.pop(choice - 1) # Skida oružje iz liste (iskorišćeno)
                    damage_to_boss = used_weapon.hp
                    print(f"Zamahnuo si {used_weapon.name} i naneo {damage_to_boss} dmg! Oružje se slomilo.")
                else:
                    print("Promašio si jer si uneo pogrešan broj!")

                self.variables[boss_hp_key] -= damage_to_boss

                # Provera da li je boss mrtav pre nego što uzvrati
                if self.variables[boss_hp_key] <= 0:
                    print("Boss je poražen!")
                    break

                # 2. Boss uzvraća udarac
                damage_from_boss = random.randint(b_min, b_max)
                self.variables[player_hp_key] -= damage_from_boss
                print(f"Boss te je udario za {damage_from_boss} dmg!")

            except ValueError:
                print("Unesi validan broj!")

        # Kraj borbe - usmeravanje u sobu
        if self.variables[player_hp_key] > 0:
            self.current_room = fight.winRoom
        else:
            self.current_room = fight.loseRoom
        
        self.refresh_room_state()
