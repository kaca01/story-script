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


def evaluate_expression(obj, context_vars):
    if hasattr(obj, 'op') and len(obj.op) > 0:
        result = evaluate_expression(obj.left, context_vars)

        for op, right in zip(obj.op, obj.right):
            if op == '+':
                result += evaluate_expression(right, context_vars)
            elif op == '-':
                result -= evaluate_expression(right, context_vars)
            elif op == '*':
                result *= evaluate_expression(right, context_vars)
            elif op == '/':
                result /= evaluate_expression(right, context_vars)
        return result

    if hasattr(obj, 'left'):
        return evaluate_expression(obj.left, context_vars)

    if isinstance(obj, int):
        return obj

    if hasattr(obj, 'var') and obj.var:
        var_name = obj.var.name
        return context_vars.get(var_name, 0)

    if hasattr(obj, 'value'):
        return obj.value

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


def parse_option_to_dict(option):
        return {
            'text': option.text,
            'room': option.target.name,
            'action': action_to_dict(option.action)
        }


def action_to_dict(action):
    if action is None:
        return None

    return {
        "take": action.item.name if getattr(action, "item", None) else None,
        "assignments": [
            {
                "varName": a.varName.name,
                "exp": assignment_to_string(a)  # optional, make expression readable
            }
            for a in getattr(action, "assignments", [])
        ],
        "rules": [
            {
                "name": r.name,
                "assignments": [
                    {
                        "varName": ra.varName.name,
                        "exp": assignment_to_string(ra)
                    }
                    for ra in getattr(r, "assignments", [])
                ]
            }
            for r in getattr(action, "rules", [])
        ]
    }


def assignment_to_string(assignment):
    res = assignment.varName.name + " = "
    # TODO: finish this
    return res

# def term_to_string(term):
#     res = ""
#     match(term.left) :
#         case(isinstance(term.left, int)):
#             res += str(term.left)
#         case(isinstance(term.left, int)): # TODO...
#     return res


