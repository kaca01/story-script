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