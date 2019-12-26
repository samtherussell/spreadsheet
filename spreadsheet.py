
spreadsheet = {}

def read_command(arguments):
    arguments = arguments.strip()
    
    if len(arguments) != 2:
        raise Exception("read command needs a single argument: location as column letter and row number eg. B4")

    if arguments in spreadsheet:
        print(spreadsheet[arguments])
    else:
        print("<empty>")
    
def write_command(arguments):
    arguments = arguments.split(" ", 1)
    
    if len(arguments) < 2:
        raise Exception("write command needs a two arguments: location and value")

    spreadsheet[arguments[0]] = arguments[1]

def parse_input(input_string):

    commands = input_string.split(" ", 1)
    
    if len(commands) < 1:
        raise Exception("please specify a command")
    else:
        command = commands[0]

    if len(commands) < 2:
        arguments = ""
    else:
        arguments = commands[1]

    return (command, arguments)

def perform_command(command, arguments):

    if command == "read":
        read_command(arguments)
    elif command == "write":
        write_command(arguments)
    elif command == "print":
        print(spreadsheet)
    else:
        raise Exception("command not supported")

while True:
    input_string = input("spreadsheet > ")
    (command, arguments) = parse_input(input_string)
    perform_command(command, arguments)
    
    
    
    