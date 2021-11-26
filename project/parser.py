import ply.yacc as yacc
import argparse
from node import Node
from lexer import *
from tac import TAC

def setParentOfChildren(node):
    for child in node.children:
        if isinstance(child, Node):
            child.parent = node

def parse_args():
    parser = argparse.ArgumentParser(description= "YACC parcer")
    parser.add_argument("-f", "--file", nargs="?", help="Program file input")
    var_args = vars(parser.parse_args())
    return var_args


def p_block(p):
    '''block : stmt block 
                | stmt 
                | empty
    '''
    if (len(p)) == 3:
        p[0] = Node('block', p[1], p[2])
    else:
        p[0] = p[1]

def p_empty(p):
    '''empty :
    '''
    pass

def p_stmt(p):
    '''stmt : decl
                    | assign
                    | cond
                    | while
    '''
    p[0] = p[1]

def p_type(p):
    '''type : BOOLEAN
                    | INT
                    | FLOAT
                    | STRING
    '''
    p[0] = p[1]

def p_decl(p):
    '''decl : type ID ';' 
            | type ID '=' expr ';'
    '''
    if len(p) == 4:
        p[0] = Node('decl', [p[1], p[2]])
    else:
        p[0] = Node('declassign', [p[1], p[2], p[4]])

def p_expr(p):
    '''expr : boolexpr
        | numexpr
        | strexpr
    '''
    p[0] = p[1]


def p_boolexpr_bool(p):
    '''boolexpr : '(' boolexpr ')'
        | boolconst
        | ID
        | boolexpr boolop boolexpr
        | ID boolop boolexpr
    '''
    if p[1] == '(':
        p[0] = Node('bool', [p[2]])
    elif len(p) == 2:
        p[0] = Node('bool', [p[1]])
    else:
        p[0] = Node('boolop', [p[1], p[2], p[3]])


def p_boolexpr_num(p):
    '''boolexpr : numexpr comp numexpr
    '''
    p[0] = Node('numcomp', [p[1], p[2], p[3]])

def p_boolconst(p):
    '''boolconst : TRUE
        | FALSE
    '''
    p[0] = p[1]

def p_comp(p):
    '''comp : SML
        | SMLEQ
        | GRT
        | GRTEQ
        | EQ
        | NOTEQ
    '''
    p[0] = p[1]


def p_boolop(p):
    '''boolop : AND
        | OR
    '''
    p[0] = p[1]


def p_numexpr(p):
    '''numexpr : '(' numexpr ')'
        | INTVAL
        | FLOATVAL
        | ID
        | numexpr numop numexpr
        | ID numop numexpr 
    '''
    if p[1] == '(':
        p[0] = Node('num', p[2])
    if len(p) == 2:
        p[0] = Node('num', p[1])
    else:
        p[0] = Node('numop', [p[1], p[2], p[3]])


def p_numop(p):
    '''numop : '+'
                     | '-'
                     | '*'
                     | '/'
                     | '^'
    '''
    p[0] = p[1]


def p_strexpr(p):
    '''strexpr : STRINGVAL
                       | STRING '(' numexpr ')'
                       | ID
                       | strexpr '+' strexpr
                       | ID '+' strexpr
    '''
    if len(p) == 4:
        p[0] = Node('concat', [p[1], p[3]])
    elif len(p) == 5:
        p[0] = Node('strcast', [p[3]])
    else:
        p[0] = Node('str', [p[1]])


def p_assign(p):
    '''assign : ID '=' expr ';'
    '''
    p[0] = Node('assign', [p[1], p[3]])


def p_cond(p):
    '''cond : IF '(' boolexpr ')' '{' block '}' elifs else
    '''
    p[0] = Node('if', [p[3], p[6]])
    if p[8]:
        p[0].children.append(p[8])
    if p[9]:
        p[0].children.append(p[9])


def p_elifs(p):
    '''elifs : ELIF '(' boolexpr ')' '{' block '}' elifs
                     | empty
    '''
    if len(p) > 2:
        p[0] = Node('elif', [p[3], p[6]])
        if p[8]:
            p[0].children.append(p[8])


def p_else(p):
    '''else : ELSE '{' block '}'
                    | empty
    '''
    if len(p) > 2:
        p[0] = Node('else', [p[3]])


def p_while(p):
    '''while : WHILE '(' boolexpr ')' '{' block '}'
    '''
    p[0] = Node('while', [p[3], p[6]])


def p_error(p):
    raise(Exception(p))

parser = yacc.yacc()

abstractTree = parser.parse(lexer=lexer, input=open("input.txt").read(), debug=True)

print("The code has been succesfully compiled.")

add_gen = TAC()
add_gen.gen_address(abstractTree)

f = open('output.txt', 'w')
f.write(add_gen.str)
f.close()

print("Output code saved on output.txt")