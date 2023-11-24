import ply.lex as lex
inputFileName = input("Enter name of input file: ")
inputFile = open(inputFileName, "r") 
# List of token names.   This is always required
tokens = (
       'NUMBER',
       'PLUS',
       'MINUS',
       'TIMES',
       'DIVIDE',
       'LPAREN',
       'RPAREN',
       'SEMICOULOMN',
       'EQUAL',
       'CROR',
       'CROL',
       'BIGGER',
       'SMALLER',
       'BRL',
       'BRR',
       'HASHTAG',
       'DOUBLEQ',
       'QUESTION',
       'PERCENT',
       'IFEQUAL',
       'BEQUAL',
       'SEQUAL',
       'NEQUAL',
       'OR',
       'AND',
       'EXCLAMATION',
       'DOUBLED',
       #Words=Idens
       'WORD',
       'DEFWORD',
       'INTWORD',
       'VECTORWORD',
       'STRWORD',
       'VARWORD',
       'FORWORD',
       'LENGTHWORD',
       'RETURNWORD',
       'IFWORD',
       'ELSEWORD',
       'WHILEWORD',
       'SCANWORD',
       'PRINTWORD',
       'LISTWORD',
       'EXITWORD',
       'NULLWORD',
        )
x={
    'def':'DEFWORD',
    'int':'INTWORD',
    'vector':'VECTORWORD',
    'str':'STRWORD',
    'var':'VARWORD',
    'for':'FORWORD',
    'length':'LENGTHWORD',
    'return':'RETURNWORD',
    'if':'IFWORD',
    'else':'ELSEWORD',
    'while':'WHILEWORD',
    'scan':'SCANWORD',
    'print':'PRINTWORD',
    'list':'LISTWORD',
    'exit':'EXITWORD',
    'null':'NULLWORD',
}

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOULOMN = r'\;'
t_EQUAL=r'\='
t_CROR=r'\{'
t_CROL=r'\}'
t_BIGGER=r'\>'
t_SMALLER=r'\<'
t_BRL=r'\['
t_BRR=r'\]'
t_HASHTAG=r'\#'
t_DOUBLEQ=r'\"'
t_QUESTION=r'\?'
t_PERCENT=r'%'
t_IFEQUAL=r'=='
t_BEQUAL=r'>='
t_SEQUAL=r'<='
t_NEQUAL=r'!='
t_OR=r'\|\|'
t_AND=r'&&'
t_EXCLAMATION=r'!'
t_DOUBLED=r':'
#For words
def t_WORD(t):
    r'[A-Za-z]([a-z]|[A-Z]|[0-9]|\_)*'
    t.type=x.get(t.value,'WORD')
    return t
# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
#Comment
def t_comment(t):
    r'\#.*'
    pass
# Error handling rule
def t_error(t):
    y=t.value[0]
    i=1
    while True:
        if(t.value[i]==';' or t.value[i]==' '):
            print("Illegal character '"+y+"'")
            t.lexer.skip(1)
            break
        else:
            y+=t.value[i]
            i=i+1
            t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
data=inputFile.readlines()
for i in range (0,int(len(data))):
    lexer.input(data[i])
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok.value)
inputFile.close()
