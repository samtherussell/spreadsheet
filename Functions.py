def get_table(sheet,table):
    refs = table.split(":")
    first_col,first_row = refs[0]
    last_col,last_row = refs[1]
    rows = (str(x) for x in range(int(first_row), int(last_row)+1))
    cols = [chr(x) for x in range(ord(first_col.upper()), ord(last_col.upper())+1)]
    return ([sheet[c+r].get_value() for c in cols] for r in rows)

def lookup(sheet, table, query, column):
    table = get_table(sheet,table)
    for row in table:
        if row[0] == query:
            return row[int(column)]
    return 0

def sum_up(sheet,table):
    table = get_table(sheet,table)
    res = 0
    for row in table:
        for cell in row:
            res = res + cell
    return res

def mean(sheet,table):
    table = get_table(sheet,table)
    res = 0
    count = 0
    for row in table:
        for cell in row:
            res = res + cell
            count = count + 1
    return float(res)/count

functions = {
    "MIN": lambda s,a,b: a if a < b else b,
    "MAX": lambda s,a,b: a if a > b else b,
    "POW": lambda s,a,b: a**b,
    "SIN": lambda s,x: math.sin(x),
    "COS": lambda s,x: math.cos(x),
    "TAN": lambda s,x: math.tan(x),
    "EQ": lambda s,a,b: 1 if a == b else 0,
    "LT": lambda s,a,b: 1 if a < b else 0,
    "GT": lambda s,a,b: 1 if a > b else 0,
    "LTE": lambda s,a,b: 1 if a <= b else 0,
    "GTE": lambda s,a,b: 1 if a >= b else 0,
    "IF": lambda s,a,b,c: b if a == 1 else c,
    "CONCAT": lambda s,a,b: str(a)+str(b),
    "LOOKUP": lookup,
    "SUM": sum_up,
    "MEAN": mean,
}

function_help_text = """    MIN: return the minimum of 2 numbers eg. =MIN(42,~A2)
        MAX: return the maximum of 2 numbers eg. =MAX(42,~A2)
        POW: returns first argument to the power of the second eg. =POW(11,4)
        SIN: return sine of the input eg. =SIN(0.5)
        COS: return cossine of the input eg. =COS(0.5)
        TAN: return tangential of the input eg. =TAN(0.5)
        EQ: returns 1 if the first argument is equal to the second else 0
        eg. =EQ(1,2)
        LT: returns 1 if the first argument is less than to the second else 0
        eg. =LT(1,2)
        GT: returns 1 if the first argument is greater than to the second else 0
        eg. =GT(1,2)
        LTE: returns 1 if the first argument is less than or equal to the second else 0
        eg. =LTE(1,2)
        GTE: returns 1 if the first argument is greater than or equal to the second else 0
        eg. =GTE(1,2)
        IF: if the first argument is 1 return the second else return the third
        eg. =IF(EQ(0,~A1),~B1,42)
        CONCAT: concatinate two strings together eg. =CONCAT("hi",~A1)
        LOOKUP: In the table described by the first argument, look up the row matching
        the second argument and return the third argument column's value
        eg. =LOOKUP("A1:C10","London", 3),
        SUM: returns the sum of all values in the table described by the argument
        eg =SUM("A1:A100"),
        MEAN: returns the mean of all values in the table described by the argument
        eg =MEAN("A1:A100"),"""

