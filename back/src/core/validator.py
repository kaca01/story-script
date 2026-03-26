from textx import get_children_of_type
from textx.exceptions import TextXSemanticError


def validate_model(model):
    check_unique_names(model)
    check_initial_values(model)
    check_variable_dependencies(model)
    check_hit_ranges_logic(model)
    check_game_flow(model)


def check_variable_dependencies(model):
    var_types = {v.__class__.__name__ for v in model.variables}
    
    has_weapons = len(model.weapons) > 0
    has_treasures = len(model.treasures) > 0
    
    if has_weapons and 'Gold' not in var_types:
        raise TextXSemanticError("Error: Story contains weapons, but no 'gold' variable is initialized.")

    if has_treasures:
        if 'Gold' not in var_types or 'Strength' not in var_types:
            raise TextXSemanticError("Error: Story contains treasures. You must initialize both 'gold' and 'strength' variables.")

    hr_names = {hr.name for hr in model.hitRanges}
    if 'boss_hit_range' in hr_names and 'BossStrength' not in var_types:
        raise TextXSemanticError("Error: 'boss_hit_range' is defined, but no 'boss_strength' variable (HP) was found.")


def check_hit_ranges_logic(model):
    hr_names = {hr.name for hr in model.hitRanges}
    fights = get_children_of_type('Fight', model)

    if 'player_hit_range' in hr_names and 'boss_hit_range' not in hr_names:
        raise TextXSemanticError("Error: You defined 'player_hit_range' but forgot 'boss_hit_range'.")

    if fights:
        if 'player_hit_range' not in hr_names or 'boss_hit_range' not in hr_names:
            raise TextXSemanticError("Error: Fight detected! Both 'player_hit_range' and 'boss_hit_range' must be defined.")


def check_initial_values(model):
    for var in model.variables:
        if var.value < 0:
            raise TextXSemanticError(f"Variable '{var.name}' cannot be negative!")
        

def check_unique_names(model):
    names = set()
    all_entities = model.rooms + model.weapons + model.treasures + model.variables + model.hitRanges
    for ent in all_entities:
        if ent.name in names:
            raise TextXSemanticError(f"Duplicate name found: '{ent.name}'. All IDs must be unique.", obj=ent)
        names.add(ent.name)


def check_game_flow(model):
    if not model.rooms:
        return

    start_room = model.rooms[0]
    visited = set()
    reached_end = False

    stack = [(start_room, [start_room.name])]

    while stack:
        current_room, path = stack.pop()

        if current_room.name in visited:
            continue
        
        visited.add(current_room.name)
        next_rooms = get_next_rooms(current_room)

        if not next_rooms or has_restart(current_room):
            reached_end = True

        for neighbor in next_rooms:
            if neighbor.name in path:
                continue
            
            stack.append((neighbor, path + [neighbor.name]))

    if not reached_end:
        raise TextXSemanticError("Infinite loop detected: The story has no reachable end state or restart.")


def get_next_rooms(room):
    next_rooms = []
    # check fight branch
    if getattr(room, 'fight', None):
        next_rooms.extend([room.fight.winRoom, room.fight.loseRoom])

    # check options branch
    for opt in getattr(room, 'options', []):
        if opt.action != "restart" and opt.target:
            next_rooms.append(opt.target)
    return next_rooms


def has_restart(room):
    return any(opt.action == "restart" for opt in getattr(room, 'options', []))