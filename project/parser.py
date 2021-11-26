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
    '''block : stmt block | 
               stmt | 
               empty
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
    '''stmt : dcl
                    | assign
                    | cond
                    | while
    '''
    p[0] = p[1]

def p_decl(p):
    '''decl : type ID | 
              type ID "=" expr ";"
    '''

parser = yacc.yacc()
resNode = parser.parse(lexer=lexer, input=open("test.txt").read())
print("Compiled succesfully")

generator = TacGenerator()
generator.gen_tac(resNode)
f = open('out.txt', 'w')
f.write(generator.tac_str)
f.close()
print("Output saved on out.txt")