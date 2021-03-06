from parsec import *
from Exceptions import FormulaException
from Functions import functions
import math

def parse_formula(text):

    try:
        deps = dependancies().parse(text)
        func = add().parse(text)
    except ParseError as e:
        raise FormulaException(str(e))

    return (deps, func)

def dependancies():
    return many( \
        many(none_of("~")).compose(string("~")) \
                .compose(joint(letter(), digit())) \
                .parsecmap(lambda x: "".join(x).upper())
                ).parsecmap(set)

def identifier():
    return spaced(regex("[A-Z][\-A-Z]*[A-Z]")).parsecmap(functions.__getitem__)

def number():
    return spaced(regex("[0-9]+(\.[0-9]+)?")).parsecmap(float)

def text_string():
    return string("\"").compose(many(none_of("\""))).skip(string("\"")).parsecmap("".join)

def args():
    return sepBy(add(), string(","))

def func():
    def f(data):
        def g(sheet):
            function = data[0]
            args = (d(sheet) for d in data[1])
            return function(sheet, *args)
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
    return spaced(choice(number(),text_string())).parsecmap(f)

def atom():
    return spaced(choice(bracketed(lazy(add)), choice(link(), choice(func(), const()))))\
           .desc("either bracketed expresion, reference to another cell, function call or constant")

def mul():
    def f(atoms):
        def g(sheet):
            vals = [atom(sheet) for atom in atoms]
            if len(vals) == 1:
                return vals[0]
            elif all((type(v) == float or type(v) == int for v in vals)):
                res = 1
                for val in vals:
                    res = res * val
                return res
            else:
                raise FormulaException("cannot multiply non numeric values")
        return g
    return spaced(sepBy1(atom(), string("*"))).parsecmap(f)

def add():
    def f(atoms):
        def g(sheet):
            vals = [atom(sheet) for atom in atoms]
            if len(vals) == 1:
                return vals[0]
            elif all((type(v) == float or type(v) == int for v in vals)):
                res = 0
                for val in vals:
                    res = res + val
                return res
            else:
                raise FormulaException("cannot add non numeric values")
        return g
    return spaced(sepBy1(mul(), string("+"))).parsecmap(f)

def lazy(f):
    return lambda a,b: f()(a,b)

def spaced(p):
    return spaces().compose(p).skip(spaces())

def bracketed(p):
    return string("(").compose(p).skip(string(")"))
