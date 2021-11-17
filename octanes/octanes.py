from os import name
import ply.yacc as yacc
import ply.lex as lex
import sys

literals = ['=', '+', '-', '*', '/', '(', ')']
reserved = {
    'dec': 'DECNUM',
    'ct': 'OCTNUM',
    'print': 'PRINT'
}

tokens = [
        'DNUM', 'ONUM', 'NAME'
         ] + list(reserved.values())

# Tokens
def t_NAME(t):
    r'[a-np-zA-Z_][a-np-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t

def t_DNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ONUM(t):
    r'o\d+'
    t.value = float(t.value.lstrip('o'))
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
abstractTree = []

def p_statement_declare_ct(p):
    'statement : OCTNUM NAME is_assing'
    names[p[2]] = { "type": "OCT", "value": p[3]}
def p_statement_declare_dec(p):
    'statement : DECNUM NAME is_assing'
    names[p[2]] = { "type": "DEC", "value": p[3]}

def p_is_assing(p):
    '''is_assing : "=" expression
                | '''
    p[0] = 0
    if len(p) > 2:
        p[0] = p[2]

def p_statement_print(p):
    '''statement : PRINT '(' expression ')' '''
    print(p[3])

def p_statement_assign(p):
    'statement : NAME "=" expression'
    if p[1] not in names:
        print ( "You must declare a variable before using it")

    elif names[p[1]]["type"] == "DEC" and not str(p[3]).startswith('o'):
        print(p[3])
        names[p[1]]["value"] = p[3]

    elif names[p[1]]["type"] == "OCT":
        names[p[1]]["value"] = p[3]
    else:
        print("Invalid assignation between number notations.")

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if names[p[1]]["type"] == names[p[3]]["type"]:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[1] == '/':
            p[0] = p[1] - p[3]
    else:
        print("Mismatch in number notations\nCan't operate between an OCT and a DEC.")

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_ONUM(p):
    "expression : ONUM"
    p[0] = p[1]

def p_expression_DNUM(p):
    "expression : DNUM"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]["value"]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

if len(sys.argv) == 3 and (sys.argv[1] == '--input' or sys.argv[1] == '-i'):
    # Read from input
    filePath = sys.argv[2]
    print("Reading code input from '" + filePath + "'")
else:
    filePath = 'input.txt'


lines = []
with open(filePath) as file:
    lines = file.readlines()

for line in lines:
    yacc.parse(line)