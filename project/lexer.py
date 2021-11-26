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
          'PLUSI',
          'MINUSI'
          'ID'] + list(reserved.values())

t_EQ = r'=='
t_NOTEQ = r'!='
t_GRTEQ = r'>='
t_SMLEQ = r'<='
t_PLUSI = r'\+\+'
t_MINUSI = r'\-\-'
t_INTVAL = r'\d+'
t_FLOATVAL = r'\d+\.\d+'
t_ignore = " \t"

# Token

def t_INT(t):
    r'int'
    t.value = str(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = str(t.value)
    return t

def t_STRING(t):
    r'".*"'
    t.value = t.value.replace("\"", "")
    t.type = reserved.get(t.value,'STRINGVAL') # Check for reserved words

def t_BOOLEAN(t):
    r'boolean'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_PRINT(t):
    r'print'
    t.value = str(t.value)

def t_AND(t):
    r'and'
    t.value = str(t.value)
    return t

def t_OR(t):
    r'or'
    t.value = str(t.value)
    return t

def t_WHILE(t):
    r'while'
    t.value = str(t.value)
    return t

def t_FOR(t):
    r'for'
    t.value = str(t.value)
    return t

def t_IF(t):
    r'if'
    t.value = str(t.value)
    return t

def t_ELIF(t):
    r'elif'
    t.value = str(t.value)
    return t

def t_ELSE(t):
    r'else'
    t.value = str(t.value)
    return t

def t_TRUE(t):
    r'true'
    t.value = str(t.value)
    return t

def t_FALSE(t):
    r'false'
    t.value = str(t.value)
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")



def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()