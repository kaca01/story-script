import copy
import random
import operator


def parse_operator(op):
    match(op):
        case "==":
            return operator.eq
        case "<":
            return operator.lt
        case ">":
            return operator.gt
        case "<=":
            return operator.le
        case ">=":
            return operator.ge


def evaluate_expression(exp, context_vars):
    if hasattr(exp, 'op') and len(exp.op) > 0:
        result = evaluate_expression(exp.left, context_vars)

        for op, right in zip(exp.op, exp.right):
            if op == '+':
                result += evaluate_expression(right, context_vars)
            elif op == '-':
                result -= evaluate_expression(right, context_vars)
            elif op == '*':
                result *= evaluate_expression(right, context_vars)
            elif op == '/':
                result /= evaluate_expression(right, context_vars)
        return result
    
    if hasattr(exp, 'random') and exp.random:
        start = getattr(exp.random, 'from_', getattr(exp.random, 'from', 0))
        end = exp.random.to
        return random.randint(start, end)

    if hasattr(exp, 'left'):
        return evaluate_expression(exp.left, context_vars)

    if isinstance(exp, int):
        return exp

    if hasattr(exp, 'var') and exp.var:
        var_name = exp.var.name
        return context_vars.get(var_name, 0)

    if hasattr(exp, 'value'):
        return exp.value

    return 0


def parse_object_to_dict(obj, seen=None):
    if seen is None:
        seen = set()

    # Base types
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    # Avoid circular references
    obj_id = id(obj)
    if obj_id in seen:
        # Just return a reference (name or id)
        if hasattr(obj, 'name'):
            return f"<ref:{obj.name}>"
        return "<circular_ref>"
    seen.add(obj_id)

    # Lists / tuples
    if isinstance(obj, (list, tuple)):
        return [parse_object_to_dict(item, seen) for item in obj]

    # Dictionaries
    if isinstance(obj, dict):
        return {key: parse_object_to_dict(value, seen) for key, value in obj.items()}

    # Objects
    result = {}
    for attr in dir(obj):
        if attr.startswith("_"):
            continue
        value = getattr(obj, attr)
        if callable(value):
            continue
        result[attr] = parse_object_to_dict(value, seen)

    return result


def parse_option_to_dict(option, context_vars):
    return {
        'text': option.text,
        'action': action_to_dict(option.action, context_vars)
    }


def get_exp_effects(assignment, context_vars):
    difference = {}
    copy_vars = copy.copy(context_vars)
    res = evaluate_expression(assignment.exp, copy_vars)
    copy_vars[assignment.varName.name] = res
    for k, v in copy_vars.items():
        if context_vars[k] != v:
            difference[k] = v - context_vars[k]
    return difference


def action_to_dict(action, context_vars):
    if action is None:
        return None

    return {
        "take": action.item.name if getattr(action, "item", None) else None,
        "assignments": [
            {
                "varName": assignment.varName.name,
                "exp": get_exp_effects(assignment, context_vars)
            }
            for assignment in getattr(action, "assignments", [])
        ],
        "rules": [
            {
                "name": r.name,
                "assignments": [
                    {
                        "varName": assignment.varName.name,
                        "exp": get_exp_effects(assignment, context_vars)
                    }
                    for assignment in getattr(action, "assignments", [])
                ],
            }
            for r in getattr(action, "rules", [])
        ]
    }

def inventory_to_dict(inventory_item):
    return {
        "name": inventory_item.name,
        "hp": inventory_item.hp
    }
