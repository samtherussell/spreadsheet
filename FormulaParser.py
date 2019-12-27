def parse_formula(text):

    deps = [text]
    func = lambda sheet: sheet[text].get_value()
    
    return (deps, func)
