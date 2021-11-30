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