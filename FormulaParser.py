from parsec import *

def parse_formula(text):

    deps = dependancies().parse(text)
    func = add().parse(text)
    
    return (deps, func)

def dependancies():
    return many( \
        many(none_of("~")).compose(string("~")) \
                .compose(joint(letter(), digit())) \
                .parsecmap(lambda x: "".join(x).upper())
                ).parsecmap(set)

def lazy(f):
    return lambda a,b: f()(a,b)

def spaced(p):
    return spaces().compose(p).skip(spaces())

def bracketed(p):
    return string("(").compose(p).skip(string(")"))

functions = {
    "MIN": lambda a,b: a if a < b else b,
    "MAX": lambda a,b: a if a > b else b
}

def identifier():
    return spaced(regex("[A-Z][\-A-Z]*[A-Z]")).parsecmap(functions.__getitem__)

def number():
    return spaced(regex("[0-9]+(\.[0-9]+)?")).parsecmap(float)

def args():
    return sepBy(add(), string(","))

def func():
    def f(data):
        def g(sheet):
            function = data[0]
            args = (d(sheet) for d in data[1])
            return function(*args)
        return g
    return joint(identifier(), bracketed(lazy(args))).parsecmap(f)

def link():
    def f(data):
        def g(sheet):
            identifier = data[0]+data[1]
            return sheet[identifier.upper()].get_value()
        return g
    return spaced(string("~").compose(joint(letter(), digit()))).parsecmap(f)

def const():
    def f(data):
        def g(sheet):
            return data
        return g
    return number().parsecmap(f)

def atom():
    return spaced(choice(bracketed(lazy(add)), choice(link(), choice(func(), const()))))

def mul():
    def f(atoms):
        def g(sheet):
            res = 1
            for atom in atoms:
                res = res * atom(sheet)
            return res
        return g
    return spaced(sepBy(atom(), string("*"))).parsecmap(f)

def add():
    def f(atoms):
        def g(sheet):
            res = 0
            for atom in atoms:
                res = res + atom(sheet)
            return res
        return g
    return spaced(sepBy(mul(), string("+"))).parsecmap(f)
