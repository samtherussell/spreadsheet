from FormulaParser import parse_formula
from Exceptions import *

class Formula:

    def __init__(self, formula, func):
        self.formula = formula
        self.func = func
        self.cached = None

    def calculate(self, sheet):
        self.cached = self.func(sheet)

    def __repr__(self):
        return self.formula + "[=" + str(self.cached) + "]"

EMPTY_TYPE = "EMPTY"
TEXT_TYPE = "TEXT"
NUMBER_TYPE = "NUMBER"
FORMULA_TYPE = "FORMULA"

class Cell:

    def __init__(self, identifier):

        self.dependancies = set()
        self.subscribers = set()
        self.clear_definition()
        self.identifier = identifier

    def clear_definition(self):
        self.value = None
        self.type = EMPTY_TYPE

    def set_definition(self, definition, sheet):

            if definition.startswith("="):
                (deps, func) = parse_formula(definition[1:])
                self.change_deps(deps, sheet)

                self.value = Formula(definition, func)
                self.type = FORMULA_TYPE

                self.value.calculate(sheet)
            else:
                try:
                    if "." in definition:
                        self.value = float(definition)
                    else:
                        self.value = int(definition)
                    self.type = NUMBER_TYPE
                except ValueError:
                    self.value = definition
                    self.type = TEXT_TYPE

            self.update_subs(sheet)

    def add_sub(self, sub):
        self.subscribers.add(sub)

    def remove_sub(self, sub):
        self.subscribers.remove(sub)

    def change_deps(self, new_deps, sheet):
        for dep in self.dependancies:
            sheet[dep].remove_sub(self.identifier)

        self.dependancies = new_deps

        for dep in self.dependancies:
            if dep not in sheet:
                sheet[dep] = Cell(dep)
            sheet[dep].add_sub(self.identifier)

    def update_value(self, sheet):
        if self.type == FORMULA_TYPE:
            self.value.calculate(sheet)
            self.update_subs(sheet)
        else:
            raise Exception(self.identifier + " does not have type:FORMULA_TYPE")

    def update_subs(self, sheet):
        for sub in self.subscribers:
            sheet[sub].update_value(sheet)

    def get_value(self):
        if self.type == EMPTY_TYPE:
            raise FormulaException("referenced cell is empty")
        elif self.type == TEXT_TYPE:
            return self.value
        elif self.type == NUMBER_TYPE:
            return self.value
        elif self.type == FORMULA_TYPE:
            return self.value.cached
        else:
            raise Exception("invalid cell type:" + self.type)

    def __repr__(self):
        return "[%s] <%s> deps=%s subs=%s"%(self.type, self.value, list(self.dependancies), list(self.subscribers))
