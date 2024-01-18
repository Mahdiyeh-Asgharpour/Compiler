import ply.yacc as yacc
import AST
# Get the token map from the lexer.  This is required.
from phase1 import tokens

def p_prog(p):
    """prog : empty 
    | func prog"""
    if len(p)==3:
        p[0]=AST.Program(func=p[1], prog=p[2], pos=p.lineno(1)-len(data))
def p_func(p):
    """func : DEFWORD type WORD LPAREN flist RPAREN CROR body CROL 
    | DEFWORD  type WORD LPAREN flist RPAREN RETURNWORD expr SEMICOULOMN"""
    if isinstance(p[8], Body) or p[8] is None:
            p[0] = AST.FunctionDef(rettype=p[2], name=p[3], fmlparams=p[5], body=p[8], pos=p.lineno(1)-len(data))
    else:
            p[0] = AST.BodyLessFunctionDef(rettype=p[2], name=p[3], fmlparams=p[5], expr=p[8],pos=p.lineno(1)-len(data))

def p_body(p):
    """body : empty 
    | stmt body"""
    if len(p) == 3:
        p[0] = Body(statement=p[1], body=p[2])
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
    if len(p)==3 or len(p)==1:
        p[0]=p[1]
    elif len(p)==6:
        if p[1]=="if":
            p[0]=AST.IfOrIfElseInstruction(cond=p[3], if_statement=p[5], \
                                     else_statement=None, pos=p.lineno(1)-len(data))
        elif p[1]=="while":
            p[0]=AST.WhileInstruction(cond=p[3], while_statement=p[5],pos=p.lineno(1)-len(data))
    elif len(p)==8:
        p[0] = AST.IfOrIfElseInstruction(cond=p[3], if_statement=p[5], \
                                     else_statement=p[7], pos=p.lineno(1)-len(data))
    elif len(p)==10:
        p[0] = AST.ForInstruction(id=p[3], start_expr=p[5], end_expr=p[7], \
                              for_statement=p[9], pos=p.lineno(1)-len(data))
    elif len(p)==4:
        if p[1]=="return":
            p[0] = AST.ReturnInstruction(expr=p[2], pos=p.lineno(1)-len(data))
        elif p[1]=="{":
            p[0] = AST.Block(body=p[2])

def p_defvar(p):
    """defvar : VARWORD type WORD 
    | VARWORD type WORD EQUAL expr"""
    if len(p) == 4:
            p[0] = AST.VariableDecl(type=p[2], id=p[3], expr=None,pos=p.lineno(1)-len(data))
    elif len(p) == 6:
            p[0] = AST.VariableDecl(type=p[2], id=p[3], expr=p[5],pos=p.lineno(1)-len(data))

def p_flist(p):
    """flist : empty 
    | type WORD 
    | type WORD COMMA flist"""
    if len(p) == 3:
        p[0] = AST.ParametersList(parameters=[Parameter(type=p[1], id=p[2])])
    elif len(p) == 5:
        p[0] = AST.ParametersList(parameters=p[4].parameters + [Parameter(type=p[1], id=p[2])])
def p_clist(p):
    """clist : empty 
    | expr 
    | expr COMMA clist"""
    if len(p) == 2:
        exprs = [] if p[1] == [] else [p[1]]
        p[0] = AST.ExprList(exprs=exprs)
    elif len(p) == 4:
        p[0] = AST.ExprList(exprs=p[3].exprs + [p[1]])
def p_type(p):
    """type : INTWORD 
    | VECTORWORD 
    | STRWORD 
    | NULLWORD"""
    
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
    | NUMBER
    | STRING
    | builtin_methods"""
    if len(p) == 4 or len(p) == 3:
            if p[1] == '-':
                p[2].value = -p[2].value
                p[0] = p[2]
            elif p[1] == '!':
                p[2].value = 0 if p[2].value else 1
                p[0] = p[2]
            else:
                p[0] = AST.BinExpr(left=p[1], op=p[2], right=p[3], pos=p.lineno(1)-len(data))
            
    elif len(p)==2:
            if p.slice[1].type in ('NUMBER', 'STRING', 'ID'):
                p[0] = p.slice[1]
            else:
                p[0] = p[1]
    elif len(p)==5:
        if p[2]=="(":
            p[0] = AST.FunctionCall(id=p[1], args=p[3],pos=p.lineno(1)-len(data))
        else:
            p[0] = AST.OperationOnList(expr=p[1], index_expr=p[3], pos=p.lineno(1)-len(data))
    else:
            p[0] = AST.TernaryExpr(cond=p[1], first_expr=p[3], second_expr=p[5],  pos=p.lineno(1)-len(data))
def p_empty(p):
    """empty : """
    p[0] = []
def p_builtin_methods(p):
    """builtin_methods : LENGTHWORD LPAREN expr RPAREN
    | SCANWORD LPAREN RPAREN 
    | PRINTWORD LPAREN expr RPAREN
    | LISTWORD LPAREN expr RPAREN
    | EXITWORD LPAREN expr RPAREN"""
# Error rule for syntax errors
def p_error(p):
    # print("Syntax error in input!")
    pass
def p_func1_error(p):
    """func : DEFWORD type WORD LPAREN error RPAREN CROR body CROL """
    print("error :"+p[5]+ " in "+str(p.lineno(5)-len(data)))
def p_func2_error(p):
    """func : DEFWORD  type WORD LPAREN error RPAREN RETURNWORD expr SEMICOULOMN"""
    print("error :"+p[5]+ " in "+str(p.lineno(5)-len(data)))
def p_stmt1_error(p):
    """stmt : FORWORD LPAREN WORD  EQUAL error TOWORD expr RPAREN stmt"""
    print("error :"+p[4]+ " in "+str(p.lineno(4)-len(data)))
def p_defvar1_error(p):
    """defvar : VARWORD error WORD"""
    print("error :"+p[1]+ " in "+str(p.lineno(1)-len(data)))
def p_defvar2_error(p):
    """defvar : VARWORD error WORD EQUAL expr"""
    print("error :"+p[2].value+ " in "+str(p.lineno(2)-len(data)))
def p_flist1_error(p):
    """flist : error WORD COMMA flist"""
    print("error :"+p[1]+ " in "+str(p.lineno(1)-len(data)))

def p_flist2_error(p):
    """flist : type WORD COMMA error"""
    print("error :"+p[3]+ " in "+str(p.lineno(3)-len(data)))

def p_expr1_error(p):
    """expr : WORD LPAREN error RPAREN"""
    print("error :"+p[2]+ " in "+str(p.lineno(2)-len(data)))


# Build the parser
parser = yacc.yacc()
string =""
inputFile=open(input("Enter file name :"), "r")
data= inputFile.readlines()
for i in range (0,int(len(data))):
    string =string+ data[i]

inputFile.close()
result = parser.parse(string)
print(result)
print (string)
