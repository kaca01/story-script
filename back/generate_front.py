import json
import os
import sys
from jinja2 import Environment, FileSystemLoader
from src.core.model import load_model


def expr_to_json(expr):
    if expr is None:
        return None

    if isinstance(expr, (int, float)):
        return {"type": "value", "value": expr}

    if hasattr(expr, 'var') and expr.var:
        return {"type": "var", "name": expr.var.name}

    if hasattr(expr, 'random') and expr.random:
        return {
            "type": "random",
            "from": getattr(expr.random, 'from', 0),
            "to": getattr(expr.random, 'to', 0)
        }

    if hasattr(expr, 'left') and getattr(expr, 'left', None) is not None:
        left = expr_to_json(expr.left)
        ops = list(getattr(expr, 'op', []) or [])
        rights = getattr(expr, 'right', []) or []
        if ops and rights:
            return {
                "type": "binary",
                "left": left,
                "ops": ops,
                "rights": [expr_to_json(right) for right in rights]
            }
        return left

    if hasattr(expr, 'inner') and getattr(expr, 'inner', None) is not None:
        return expr_to_json(expr.inner)

    if hasattr(expr, 'value') and expr.value is not None:
        return {"type": "value", "value": expr.value}

    return {"type": "value", "value": 0}


def condition_to_json(condition):
    if condition is None:
        return None
    return {
        "left": expr_to_json(condition.left),
        "op": condition.op,
        "right": expr_to_json(condition.right)
    }


def action_to_json(action):
    if action is None:
        return None
    if action == 'restart':
        return {"type": "restart"}

    if hasattr(action, 'item') and action.__class__.__name__ == 'Buy':
        return {"type": "buy", "item": action.item.name}

    if hasattr(action, 'item') and action.__class__.__name__ == 'Take':
        return {
            "type": "take",
            "item": action.item.name if getattr(action.item, 'name', None) else None,
            "assignments": [
                {
                    "varName": assignment.varName.name,
                    "exp": expr_to_json(assignment.exp)
                }
                for assignment in getattr(action, 'assignments', [])
            ],
            "rules": [
                {
                    "name": rule.name,
                    "assignments": [
                        {
                            "varName": assignment.varName.name,
                            "exp": expr_to_json(assignment.exp)
                        }
                        for assignment in getattr(rule, 'assignments', [])
                    ]
                }
                for rule in getattr(action, 'rules', [])
            ],
            "randoms": [
                {
                    "name": rand.name,
                    "from": rand.from_,
                    "to": rand.to
                }
                for rand in getattr(action, 'randoms', [])
            ]
        }

    return None


def parse_option(option):
    return {
        "text": option.text,
        "condition": condition_to_json(getattr(option, 'condition', None)),
        "action": action_to_json(getattr(option, 'action', None)),
        "target": option.target.name if getattr(option, 'target', None) else None
    }


def parse_fight(fight):
    if not fight:
        return None
    return {
        "description": fight.description,
        "hr": fight.hr.name if getattr(fight, 'hr', None) else None,
        "condition": condition_to_json(getattr(fight, 'condition', None)),
        "winRoom": fight.winRoom.name if getattr(fight, 'winRoom', None) else None,
        "loseRoom": fight.loseRoom.name if getattr(fight, 'loseRoom', None) else None
    }


def parse_room(room):
    room_obj = {
        "name": room.name,
        "imagePath": getattr(room, 'imagePath', ''),
        "header": getattr(room, 'header', ''),
        "body": getattr(room, 'body', ''),
        "options": [parse_option(opt) for opt in getattr(room, 'options', [])],
        "fight": parse_fight(getattr(room, 'fight', None))
    }
    return room_obj


def parse_model(model):
    variables = {}
    var_types = {}
    boss_strength_var = None
    player_strength_var = None

    for var in getattr(model, 'variables', []):
        variables[var.name] = var.value
        var_types[var.name] = type(var).__name__.lower()
        if type(var).__name__.lower() == 'bossstrength':
            boss_strength_var = var.name
        if type(var).__name__.lower() == 'strength':
            player_strength_var = var.name

    return {
        "title": getattr(model, 'name', 'Adventure'),
        "description": 'Static HTML front-end generated from story model.',
        "hitRanges": {
            hr.name: {"from": getattr(hr, 'from_', getattr(hr, 'from', 0)), "to": hr.to}
            for hr in getattr(model, 'hitRanges', [])
        },
        "variables": variables,
        "varTypes": var_types,
        "playerStrengthVar": player_strength_var,
        "bossStrengthVar": boss_strength_var,
        "weapons": [
            {"name": weapon.name, "value": weapon.value, "hp": weapon.hp}
            for weapon in getattr(model, 'weapons', [])
        ],
        "treasures": [
            {"name": treasure.name, "weight": treasure.weight}
            for treasure in getattr(model, 'treasures', [])
        ],
        "rules": [
            {
                "name": rule.name,
                "assignments": [
                    {
                        "varName": assignment.varName.name,
                        "exp": expr_to_json(assignment.exp)
                    }
                    for assignment in getattr(rule, 'assignments', [])
                ]
            }
            for rule in getattr(model, 'globalRules', [])
        ],
        "rooms": [parse_room(room) for room in getattr(model, 'rooms', [])]
    }


def render_front(model_file, output_file):
    model = load_model(model_file, debug=False)
    data = parse_model(model)

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=False)
    template = env.get_template('story_front.html.j2')

    story_json = json.dumps(data, ensure_ascii=False, indent=2)

    output_dir = os.path.dirname(os.path.abspath(output_file)) or os.getcwd()
    default_asset_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'front', 'src', 'assets', 'images'))
    asset_base = ''
    if os.path.isdir(default_asset_dir):
        asset_base = os.path.relpath(default_asset_dir, start=output_dir).replace('\\', '/')
        if not asset_base.endswith('/'):
            asset_base += '/'

    output = template.render(
        title=data['title'],
        description=data['description'],
        story_json=story_json,
        asset_base=asset_base
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'Generated frontend at: {output_file}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python generate_front.py <story-file> <output-html>')
        sys.exit(1)
    story_path = sys.argv[1]
    output_path = sys.argv[2]
    render_front(story_path, output_path)
