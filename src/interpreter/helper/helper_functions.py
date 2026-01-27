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