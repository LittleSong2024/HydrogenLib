
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMMENT DEDENT DYNAMIC_PLACEHOLDER EQUALS IDENTIFIER INDENT LBRACE LBRACKET MULTILINE_COMMENT NUMBER RBRACE RBRACKET STRINGconfig : config statement\n| statementstatement : table\n| key_value_pair\n| INDENT\n| DEDENTtable : LBRACKET IDENTIFIER RBRACKET\n| LBRACKET IDENTIFIER RBRACKET INDENT statements DEDENTkey_value_pair : IDENTIFIER EQUALS valuevalue : STRING\n| NUMBER\n| DYNAMIC_PLACEHOLDERstatements : statements statement\n| statementindent_statement : INDENTdedent_statement : DEDENT'
    
_lr_action_items = {'INDENT':([0,1,2,3,4,5,6,9,12,13,14,15,16,17,18,19,20,21,],[5,5,-2,-3,-4,-5,-6,-1,17,-9,-10,-11,-12,5,5,-14,-6,-13,]),'DEDENT':([0,1,2,3,4,5,6,9,12,13,14,15,16,17,18,19,20,21,],[6,6,-2,-3,-4,-5,-6,-1,-7,-9,-10,-11,-12,6,20,-14,-6,-13,]),'LBRACKET':([0,1,2,3,4,5,6,9,12,13,14,15,16,17,18,19,20,21,],[7,7,-2,-3,-4,-5,-6,-1,-7,-9,-10,-11,-12,7,7,-14,-6,-13,]),'IDENTIFIER':([0,1,2,3,4,5,6,7,9,12,13,14,15,16,17,18,19,20,21,],[8,8,-2,-3,-4,-5,-6,10,-1,-7,-9,-10,-11,-12,8,8,-14,-6,-13,]),'$end':([1,2,3,4,5,6,9,12,13,14,15,16,20,],[0,-2,-3,-4,-5,-6,-1,-7,-9,-10,-11,-12,-8,]),'EQUALS':([8,],[11,]),'RBRACKET':([10,],[12,]),'STRING':([11,],[14,]),'NUMBER':([11,],[15,]),'DYNAMIC_PLACEHOLDER':([11,],[16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'config':([0,],[1,]),'statement':([0,1,17,18,],[2,9,19,21,]),'table':([0,1,17,18,],[3,3,3,3,]),'key_value_pair':([0,1,17,18,],[4,4,4,4,]),'value':([11,],[13,]),'statements':([17,],[18,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> config","S'",1,None,None,None),
  ('config -> config statement','config',2,'p_config','_parser.py',98),
  ('config -> statement','config',1,'p_config','_parser.py',99),
  ('statement -> table','statement',1,'p_statement','_parser.py',107),
  ('statement -> key_value_pair','statement',1,'p_statement','_parser.py',108),
  ('statement -> INDENT','statement',1,'p_statement','_parser.py',109),
  ('statement -> DEDENT','statement',1,'p_statement','_parser.py',110),
  ('table -> LBRACKET IDENTIFIER RBRACKET','table',3,'p_table','_parser.py',115),
  ('table -> LBRACKET IDENTIFIER RBRACKET INDENT statements DEDENT','table',6,'p_table','_parser.py',116),
  ('key_value_pair -> IDENTIFIER EQUALS value','key_value_pair',3,'p_key_value_pair','_parser.py',124),
  ('value -> STRING','value',1,'p_value','_parser.py',129),
  ('value -> NUMBER','value',1,'p_value','_parser.py',130),
  ('value -> DYNAMIC_PLACEHOLDER','value',1,'p_value','_parser.py',131),
  ('statements -> statements statement','statements',2,'p_statements','_parser.py',136),
  ('statements -> statement','statements',1,'p_statements','_parser.py',137),
  ('indent_statement -> INDENT','indent_statement',1,'p_indent_statement','_parser.py',146),
  ('dedent_statement -> DEDENT','dedent_statement',1,'p_dedent_statement','_parser.py',151),
]
