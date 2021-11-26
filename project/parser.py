import argparse


class Node:
    def __init__(self, type, children=None, parent=None, ptype=None):
        
        self.type = type
        
        if parent:
            self.parent = parent
        else:
            self.parent = None
        
        if children:
            self.children = children
        else:
            self.children = []
        
        if ptype:
            self.ptype = ptype
        else:
            self.ptype = None

def setParentOfChildren(node):
    for child in node.children:
        if isinstance(child, Node):
            child.parent = node

def parse_args():
    parser = argparse.ArgumentParser(description= "YACC parcer")
    parser.add_argument("-f", "--file", nargs="?", help="Program file input")
    var_args = vars(parser.parse_args())
    return var_args