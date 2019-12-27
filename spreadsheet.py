import pickle
from Exceptions import *
from Cell import Cell

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


if __name__ == "__main__":
    main()
