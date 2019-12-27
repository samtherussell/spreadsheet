import pickle

class ExitException(Exception):
    pass

class InputException(Exception):
    pass

class FormulaException(InputException):
    pass

def parse_formula(text):

    deps = [text]
    func = lambda sheet: sheet[text].get_value()
    
    return (deps, func)
    
EMPTY_TYPE = "EMPTY"
TEXT_TYPE = "TEXT"
NUMBER_TYPE = "NUMBER"
FORMULA_TYPE = "FORMULA"

class Formula:

    def __init__(self, formula, func):
        self.formula = formula
        self.func = func
        self.cached = None

    def calculate(self, sheet):
        self.cached = self.func(sheet)

    def __repr__(self):
        return self.formula + "[=" + str(self.cached) + "]"

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

spreadsheet = {}

def read_command(arguments):
    arguments = arguments.strip()
    
    if len(arguments) != 2:
        raise InputException("read command needs a single argument: location as column letter and row number eg. B4")

    if arguments not in spreadsheet:
        print("<empty>")
    else:
        try:
            print(spreadsheet[arguments].get_value())
        except FormulaException:
            print("<empty>")
    
def write_command(arguments):
    arguments = arguments.split(" ", 1)
    
    if len(arguments) < 2:
        raise InputException("write command needs a two arguments: location and value")

    if arguments[0] not in spreadsheet:
        spreadsheet[arguments[0]] = Cell(arguments[0])

    spreadsheet[arguments[0]].set_definition(arguments[1], spreadsheet)

def save_sheet(arguments):
    with open(arguments, "wb") as f:
        pickle.dump(spreadsheet, f)

def open_sheet(arguments):
    with open(arguments, "rb") as f:
        global spreadsheet
        spreadsheet = pickle.load(f)

def parse_input(input_string):

    if len(input_string) < 1:
        raise InputException("please specify a command")

    commands = input_string.split(" ", 1)

    command = commands[0]

    if len(commands) < 2:
        arguments = ""
    else:
        arguments = commands[1]

    return (command, arguments)

def perform_command(command, arguments):

    if command in ["read", "r"]:
        read_command(arguments)
    elif command in ["write", "w"]:
        write_command(arguments)
    elif command in ["print", "p"]:
        print(spreadsheet)
    elif command in ["save", "s"]:
        save_sheet(arguments)
    elif command in ["open", "o"]:
        open_sheet(arguments)
    elif command in ["quit", "q"]:
        raise ExitException()
    else:
        raise InputException("command not supported")

while True:
    input_string = input("spreadsheet > ")
    try:
        (command, arguments) = parse_input(input_string)
        perform_command(command, arguments)
    except InputException as e:
        print(e)
    except ExitException as e:
        break
    
    
    
    
