import random


# * Christopher Ismael Ortega Gonzalez
# * A01634500 

functional = ["f", "i", "p"]
operations = ["+", "-"]
assignation = "="
ids = {}
tids = []

# ! A very important note to take in mind for my compiler is that spaces are very important 
# ! for it to be capable to easily detect distintc characters without further computation 

def is_number(num):
    if num.rstrip("\n").isdigit():
        return True
    else:
        num_split = num.rstrip("\n").split(".")
        return len(num_split) == 2 and num_split[0].isdigit() and num_split[1].isdigit()
    
def gen_tid(type):
    name = "t" + str(len(tids))
    tids.append(name)
    ids[name] = {
        "type": type,
        "value": None
    }
    return name

def parse_expression(expression, var, expression_prep):
    if var == None:
        # * Return the value of the calculation
        for j, elem in enumerate(expression):
            if is_number(elem) and j == 0 and len(expression) == 1:
                return str(elem)
            elif is_number(elem) and expression[j+1] in operations:
                return str(float(elem) + (float(parse_expression(float(expression[j+2]), None, [])) if expression[j+1] == "+" else -float(parse_expression(float(expression[j+2]), None, []))))
            elif elem in list(ids.keys()):
                return ids[elem]["value"]
    else:
        # * this will return the new lines that correspond to the calculation of the right side
        #if "+" not in expression and "-" not in expression and len(expression) == 1:
        #    return expression[0]
        for j, elem in enumerate(expression):
            # * just a number and that's all
            if is_number(elem) and j == 0 and len(expression) == 1:
                return var + " := " + elem
            elif elem in operations:
                if elem == "+":
                    h0 = expression[:j]
                    h1 = expression[j+1:]
                    if h0.__contains__("+") or h0.__contains__("-"):
                        t0 = parse_expression(h0, gen_tid("f"), expression_prep)
                    else:
                        t0 = h0[0]

                    if h1.__contains__("+") or h1.__contains__("-"):
                        t1 = parse_expression(h1, gen_tid("f"), expression_prep)
                    else:
                        t1 = h1[0]
                    
                    last_exp = ""
                    # todo: Guardar las instrucciones previas y poner la ultima
                    if t0 in list(ids.keys()) or is_number(t0):
                        # * Es un id que solo se coloca en la literal final
                        last_exp += var + " := " + str(t0) + " " + elem
                    if t1 in list(ids.keys()) or is_number(t1):
                        last_exp += " " + str(t1)
                    
                    expression_prep.append(last_exp)

                    return expression_prep
               
            elif elem.strip("\n") in ids and len(expression) == 1:
                return elem.strip("\n")
            elif is_number(elem) and expression[j-1] in operations:
                continue
        

        return "[Error] Expresion invalida"

def parse_line(line):
    to_write = []
    words = line.split(" ")
    for idx, word in enumerate(words):
        
        # * check if its reserved word
        # * also needs to be the first character in line
        if word in functional and idx == 0:
            # * check if its declaration
            if word == "f" or word == "i":
                # * next character needs to be a new and fresh ID
                if words[idx+1].rstrip("\n") not in list(ids.keys()):
                    # * save character into ids with its respective type
                    ids[words[idx+1].rstrip("\n")] = {
                        "type": word,
                        "value": None
                    }
                
                    to_write.append("DeclareFloat(" + words[idx+1].rstrip("\n") + ")\n")
                    return to_write
                else:
                    # * send error for a redeclaration
                    return "[Error]: Redeclaration for var" + words[idx+1] + "\n"

            elif word == "p":
                # * check for id or expression
                if words[idx+1].rstrip("\n") in ids:
                    # * is id
                    to_write.append("Print(" + str(words[idx+1].rstrip("\n")) + ")\n")
                else:
                    # * check for valid expression
                    #/ TODO: Parse expression
                    to_write.append("Print(" + str(parse_expression(words[idx+1::], None), []) + ")\n")
                return to_write

        # * check if it's id
        elif word.rstrip("\n") in list(ids.keys()):
            # * check if it's assignation
            if len(words) > idx + 1 and words[idx+1] == "=":
                # * parse right side of the equation and prepare it
                #/ TODO: Parse epxression
                to_write.append(parse_expression(words[idx+2::], word, []))
                return to_write


        # * send an error
        #/ TODO: Send error for undeclared variable
        elif str(word) not in ids:
            to_write.append("[Error]: Undeclared variable -> " + str(word) + "\n")
            return to_write




def simple_compiler(filepath):

    ast = {}

    file = open(filepath, "r")
    lines = file.readlines()
    file.close()

    output = open("output.txt", "w+")
    output.write("// Compiled language\n")
    mid_code = []

    # * Reading line by line
    for line in lines:
        result = parse_line(line)
        mid_code.append(result)

    for code in mid_code:
        for l_code in code:
            if str(type(l_code) == "<class list>"):
                for l2_code in l_code:
                    output.write(l2_code)
            else:
                output.write(l_code)

    output.close()

simple_compiler("D:\9th\Compiladores\Lex\SimpleCompiler\input.txt")