from node import Node

class TAC:
    def __init__(self):
        self.var = -1
        self.label = -1
        self.tac_str = ""
        self.line = 0
        self.label_stack = []

    def write_line(self, *argv):
        for arg in argv:
            self.tac_str += (arg + ' ')
        self.tac_str = self.tac_str[:-1]
        self.tac_str += '\n'
        self.line += 1

    def get_var(self):
        self.var += 1
        return 'r' + str(self.var)

    def get_label(self):
        self.label += 1
        return 'L' + str(self.label)

    def add_line_num(self, str_to_add):
        arr = str_to_add.split('\n')
        for i in range(len(arr)):
            arr[i] = str(i) + '. ' + arr[i]
        return '\n'.join(arr)

    def gen_address_code(self, node):
        if not isinstance(node, Node):
            return node
        c = node.children

        if node.type == 'block':
            self.gen_address_code(c[0])
            if len(c) == 2:
                self.gen_address_code(c[1])
        if node.type == 'dcl':
            pass
        if node.type == 'dclassign':
            self.write_line(c[1], '=', self.gen_address_code(c[2]))
        if node.type == 'bool':
            return self.gen_address_code(c[0])
        if node.type == 'boolop':
            v = self.get_var()
            self.write_line(v, '=', self.gen_address_code(
                c[0]), c[1], self.gen_address_code(c[2]))
            return v
        if node.type == 'numcomp':
            v = self.get_var()
            self.write_line(v, '=', self.gen_address_code(
                c[0]), c[1], self.gen_address_code(c[2]))
            return v
        if node.type == 'strcomp':
            v = self.get_var()
            self.write_line(v, '=', self.gen_address_code(
                c[0]), c[1], self.gen_address_code(c[2]))
            return v
        if node.type == 'num':
            return self.gen_address_code(c)
        if node.type == 'numop':
            v = self.get_var()
            self.write_line(v, '=', self.gen_address_code(
                c[0]), c[1], self.gen_address_code(c[2]))
            return v
        if node.type == 'concat':
            v = self.get_var()
            self.write_line(v, '=', self.gen_address_code(
                c[0]), '+', self.gen_address_code(c[1]))
            return v
        if node.type == 'strcast':
            v = self.get_var()
            self.write_line(v, '=', 'num2str(', self.gen_address_code(c[0]), ')')
            return v
        if node.type == 'str':
            return self.gen_address_code(c[0])
        if node.type == 'assign':
            self.write_line(c[0], '=', self.gen_address_code(c[1]))
        if node.type == 'if':
            if len(c) == 4:
                label1 = self.get_label()
                label2 = self.get_label()
                self.label_stack.append(label2)

                self.write_line(
                    'if', 'false', self.gen_address_code(c[0]), 'goto', label1)
                self.gen_address_code(c[1])
                self.write_line('goto', label2)
                self.write_line(label1)
                self.gen_address_code(c[2])
                self.gen_address_code(c[3])
                self.write_line(self.label_stack.pop())
            elif len(c) == 3:
                label1 = self.get_label()
                label2 = self.get_label()
                self.label_stack.append(label2)

                self.write_line(
                    'if', 'false', self.gen_address_code(c[0]), 'goto', label1)
                self.gen_address_code(c[1])
                self.write_line('goto', label2)
                self.write_line(label1)
                self.gen_address_code(c[2])
                self.write_line(self.label_stack.pop())
            else:
                label = self.get_label()
                self.write_line(
                    'if', 'false', self.gen_address_code(c[0]), 'goto', label)
                self.gen_address_code(c[1])
                self.write_line(label)
        if node.type == 'elif':
            if len(c) == 3:
                label = self.get_label()
                self.write_line(
                    'if', 'false', self.gen_address_code(c[0]), 'goto', label)
                self.gen_address_code(c[1])
                self.write_line('goto', self.label_stack[-1])
                self.write_line(label)
                self.gen_address_code(c[2])
            else:
                label = self.get_label()
                self.write_line(
                    'if', 'false', self.gen_address_code(c[0]), 'goto', label)
                self.gen_address_code(c[1])
                self.write_line('goto', self.label_stack[-1])
                self.write_line(self.label)
        if node.type == 'else':
            self.gen_address_code(c[0])
        if node.type == 'while':
            label1 = self.get_label()
            label2 = self.get_label()

            self.write_line(label1)
            self.write_line('if', 'false', self.gen_address_code(c[0]), 'goto', label2)
            self.gen_address_code(c[1])
            self.write_line('goto', label1)
            self.write_line(label2)