import ply.yacc as yacc
import ply.lex as lex

literals = ['=', '+', '-', '*', '/', '^', '(', ')', '{', '}', '<', '>', ';']

reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'do': 'DO',
    'while': 'WHILE',
    'for': 'FOR',
    'and': 'AND',
    'or': 'OR',
    'print': 'PRINT'
}

tokens = ['INTVAL',
          'FLOATVAL',
          'STRINGVAL',
          'EQ',
          'NOTEQ',
          'SMLEQ',
          'GRTEQ',
          'ID'] + list(reserved.values())

# Token

def t_INTVAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOATVAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_STRING(t):
    r'".*"'
    t.value = t.value.replace("\"", "")
    t.type = reserved.get(t.value,'STRINGVAL') # Check for reserved words


def t_VARBOOL(t):
    r'true|false'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules

precedence = (
    ('right', '='),
    ('left', 'EQ', 'NOTEQ'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('left', 'AND', 'OR'),
    ('nonassoc', '<', '>', 'BIGEQ', 'SMALLEQ'),
    ('right', 'UMINUS')
)

# dictionary of names
names = {}
abstractTree = {}


def p_init(p):
    ''''''

def p_statement_declare_int(p):
    '''statement : INTVAL NAME is_assing'''
    if type(p[3]) == int:
        names[p[2]] = { "type": "INT", "value": p[3]}
    else:
        print('No puedes asignar flotantes a enteros')

def p_is_assing(p):
    '''is_assing : "=" expression 
                | '''
    p[0] = 0
    if len(p) > 2:
        p[0] = p[2]

def p_statement_declare_float(p):
    'statement : FLOATDEC NAME'
    names[p[2]] = { "type": "FLOAT", "value":0}

def p_statement_declare_bool(p):
    'statement : VBOOL NAME'
    names[p[2]] = { "type": "BOOL", "value":0}

def p_statement_print(p):
    '''statement : PRINT '(' expression ')' '''
    print(p[3])

def p_statement_assign(p):
    'statement : NAME "=" expression'
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]


def p_statement_expr(p):
    'statement : expression'
    # print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_inumber(p):
    "expression : INUMBER"
    p[0] = p[1]

def p_expression_fnumber(p):
    "expression : FNUMBER"
    p[0] = p[1]

def p_expression_varbool(p):
    "expression : VARBOOL"
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
        print("Syntax error at line '%s' character '%s'" % (p.lexpos, p.lineno) )
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Console 
#while True:
#    try:
#        s = input('calc > ')
#    except EOFError:
#        break
#    if not s:
#        continue
#    yacc.parse(s)

#File
inputData = []
with open('data.txt') as file:
    inputData = file.readlines()

for data in inputData:
    yacc.parse(data)