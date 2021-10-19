
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "left+-left*/rightUMINUSFNUMBER INUMBER NAMEstatement : 'f' NAMEstatement : 'i' NAMEstatement : NAME '=' expressionstatement : expressionstatement : 'p' expressionexpression : expression '+' expression\n                  | expression '-' expression\n                  | expression '*' expression\n                  | expression '/' expressionexpression : '-' expression %prec UMINUSexpression : '(' expression ')'expression : FNUMBERexpression : INUMBERexpression : NAME"
    
_lr_action_items = {'f':([0,],[2,]),'i':([0,],[4,]),'NAME':([0,2,4,6,7,8,12,14,15,16,17,],[3,11,13,19,19,19,19,19,19,19,19,]),'p':([0,],[6,]),'-':([0,3,5,6,7,8,9,10,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,],[7,-14,15,7,7,7,-12,-13,7,7,7,7,7,15,-14,-10,15,15,-6,-7,-8,-9,-11,]),'(':([0,6,7,8,12,14,15,16,17,],[8,8,8,8,8,8,8,8,8,]),'FNUMBER':([0,6,7,8,12,14,15,16,17,],[9,9,9,9,9,9,9,9,9,]),'INUMBER':([0,6,7,8,12,14,15,16,17,],[10,10,10,10,10,10,10,10,10,]),'$end':([1,3,5,9,10,11,13,18,19,20,22,23,24,25,26,27,],[0,-14,-4,-12,-13,-1,-2,-5,-14,-10,-3,-6,-7,-8,-9,-11,]),'=':([3,],[12,]),'+':([3,5,9,10,18,19,20,21,22,23,24,25,26,27,],[-14,14,-12,-13,14,-14,-10,14,14,-6,-7,-8,-9,-11,]),'*':([3,5,9,10,18,19,20,21,22,23,24,25,26,27,],[-14,16,-12,-13,16,-14,-10,16,16,16,16,-8,-9,-11,]),'/':([3,5,9,10,18,19,20,21,22,23,24,25,26,27,],[-14,17,-12,-13,17,-14,-10,17,17,17,17,-8,-9,-11,]),')':([9,10,19,20,21,23,24,25,26,27,],[-12,-13,-14,-10,27,-6,-7,-8,-9,-11,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,6,7,8,12,14,15,16,17,],[5,18,20,21,22,23,24,25,26,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> f NAME','statement',2,'p_statement_declare_float','calc.py',48),
  ('statement -> i NAME','statement',2,'p_statement_declare_int','calc.py',56),
  ('statement -> NAME = expression','statement',3,'p_statement_assign','calc.py',64),
  ('statement -> expression','statement',1,'p_statement_expr','calc.py',71),
  ('statement -> p expression','statement',2,'p_statement_print','calc.py',76),
  ('expression -> expression + expression','expression',3,'p_expression_binop','calc.py',81),
  ('expression -> expression - expression','expression',3,'p_expression_binop','calc.py',82),
  ('expression -> expression * expression','expression',3,'p_expression_binop','calc.py',83),
  ('expression -> expression / expression','expression',3,'p_expression_binop','calc.py',84),
  ('expression -> - expression','expression',2,'p_expression_uminus','calc.py',96),
  ('expression -> ( expression )','expression',3,'p_expression_group','calc.py',101),
  ('expression -> FNUMBER','expression',1,'p_expression_fnumber','calc.py',106),
  ('expression -> INUMBER','expression',1,'p_expression_inumber','calc.py',112),
  ('expression -> NAME','expression',1,'p_expression_name','calc.py',118),
]