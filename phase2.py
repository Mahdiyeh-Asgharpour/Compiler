import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

def p_prog(p):
    "prog :empty | func prog"
def f_func(p):
    "func : DEFWORD type WORD LPAREN flist RPAREN CROR body CROL | DEFWORD  type WORD LPAREN flist RPAREN RETURNWORD expr SEMICOULOMN"
def p_body(p):
    "body : empty | stmt body"
def p_stmt(p):
    """stmt : expr SEMICOULOMN
    | defvar SEMICOULOMN 
    | IFWORD LPAREN expr RPAREN stmt 
    | IFWORD LPAREN expr RPAREN stmt ELSEWORD stmt 
    | WHILEWORD LPAREN expr RPAREN stmt 
    | FORWORD LPAREN WORD  EQUAL expr TOWORD expr RPAREN stmt 
    | RETURNWORD stmt SEMICOULOMN 
    | CROR body CROL
    | func"""
def p_defvar(p):
    "defvar : VARWORD type WORD | VARWORD type WORD EQUAL expr"
def p_flist(p):
    "flist : empty | type WORD | type WORD COMMA flist"
def p_clist(p):
    "clist : empty | expr | expr COMMA clist"
def p_type(p):
    "type : INTWORD | VECTORWORD | STRWORD | NULLWORD"
def p_expr(p):
    """expr : expr BRL expr BRR 
    | BRL clist BRR
    | expr QUESTION expr DOUBLED expr
    | expr PLUS expr
    | expr MINUS expr
    | expr TIMES expr
    | expr DIVIDE expr
    | expr PERCENT expr
    | expr BIGGER expr
    | expr SMALLER expr
    | expr IFEQUAL expr
    | expr BEQUAL expr
    | expr SEQUAL expr
    | expr OR expr
    | expr AND expr
    | EXCLAMATION expr
    | PLUS expr
    | MINUS expr
    | WORD
    | WORD EQUAL expr
    | WORD LPAREN clist RPAREN
    | INTWORD
    | STRWORD
    | builtin_methods"""
def p_empty(p):
    "empty : "
def builtin_methods(p):
    """builtin_methods : LENGTHWORD LPAREN expr RPAREN
    | SCANWORD LPAREN RPAREN 
    | PRINTWORD LPAREN expr RPAREN
    | LISTWORD LPAREN expr RPAREN
    | EXITWORD LPAREN expr RPAREN"""
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)