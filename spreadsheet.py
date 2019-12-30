import pickle
from Exceptions import *
from Cell import Cell
from Functions import function_help_text

spreadsheet = {}

def main():
    while True:
        input_string = input("spreadsheet > ")
        try:
            (command, arguments) = parse_input(input_string)
            perform_command(command, arguments)
        except InputException as e:
            print(e)
        except ExitException as e:
            break

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
        print(read_command(arguments))
    elif command in ["write", "w"]:
        write_command(arguments)
    elif command in ["print", "p"]:
        print(spreadsheet)
    elif command in ["save", "s"]:
        save_sheet(arguments)
    elif command in ["open", "o"]:
        open_sheet(arguments)
    elif command in ["help", "h", "?"]:
        print_help(arguments)
    elif command in ["quit", "q"]:
        raise ExitException()
    else:
        raise InputException("command not supported")

def read_command(arguments):
    arguments = arguments.strip()
    
    if len(arguments) != 2:
        raise InputException("read command needs a single argument: location as column letter and row number eg. B4")

    arguments = arguments.upper()

    if arguments not in spreadsheet:
        return "<empty>"
    else:
        try:
            return spreadsheet[arguments].get_value()
        except FormulaException:
            return "<empty>"
    
def write_command(arguments):
    arguments = arguments.split(" ", 1)
    
    if len(arguments) < 2:
        raise InputException("write command needs a two arguments: location and value")

    arguments[0] = arguments[0].upper()
    
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

help_text = {
    "help": "(h,?) to show help, can specify command eg. help read",
    "read": "(r) to read the value of a cell eg. read A1",
    "write": """(w) to write a value to a cell eg. write A1 42
    Values can be numeric or text constants or formulas.

    Formulas
    Are prefixed with '='
    Cell references in formulas must be prefixed with ~ eg. =~B4
    Number constants in formulas do not need a prefix.
    Text constants need to be surrounded by double quotes eg. ="hi"
    The following functions are supported with the syntax: FUNC-NAME(ARG1,ARG2...)
    """+function_help_text,
    "print": "(p) to print the spreadsheet internal representation",
    "save": "(s) to save the spreadsheet. specify the filename eg. save file.sheet",
    "open": "(o) to open a saved spreadsheet. specify the filename eg. open file.sheet",
    "quit": "(q) to quit program",
}

def print_help(argument):
    if argument == "":
        for c in help_text:
            print(c, ":", help_text[c], "\n")
    elif argument not in help_text:
        print("no command with name")
    else:
        print(argument, ":", help_text[argument])


if __name__ == "__main__":
    main()
