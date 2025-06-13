from radon.complexity import cc_visit

def get_cyclomatic_complexity(code):
    return [obj.__dict__ for obj in cc_visit(code)]
