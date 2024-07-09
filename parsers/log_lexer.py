'''
Propositional logic lexer
'''

import ply.lex as lex

# List of tokens (terminals)
tokens = (
   # PARENS
   'TVALUE',
   'LPAREN',
   'RPAREN',
   # Prop Logic Symbols
   'LETTER',
   # Prop Logic OPERATORS
   'CONJUNCT',
   'DISJUNCT',
   'BICONDITIONAL',
   'CONDITIONAL',   
   'NEGATION',
   # Pred Logic Operators
    #'QUANTIFIER',
)

# Regular expression rules for simple tokens
t_TVALUE = r'[0-1]'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
# Prop Logic Symbols
t_LETTER = r'[A-Z]'
# Prop Logic OPERATORS
t_CONJUNCT = r'\^|\&|and'
t_DISJUNCT =  r'v|or'
t_BICONDITIONAL =  r'<->|iff'
t_CONDITIONAL =  r'->'
t_NEGATION = r'~|not'
# Pred Logic Operators
#t_QUANTIFIER = r'AE[x-z]'

# Ignore spaces, tabs
t_ignore  = r' \t'

# Defines number token, but makes sure it is in an INTs.

#def t_NUMBER(t):
#    r'\d+'
#    t.value = int(t.value)
#    return t

#def t_FLOAT(t):
#    r'\d+\.\d+'
#    t.value = float(t.value)
#    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_QUANTIFIER(t):
    r'[AE][x-z]{1}'
    t.type = "QUANTIFIER"
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Gives input to the lexer, outputs a list of the lexer data: tok.type, tok.value, tok.lineno, tok.lexpos. To get the lexer object, output tok
def lexer_wff_data(s:str): 
    #print(f"Processing input: {s}")
    lexer.input(s)
    tok_list = []
    while True:
        tok = lexer.token() # returns next token
        if not tok:
            break 
        tok_data = (tok.type, tok.value, tok.lineno, tok.lexpos)
        tok_list.append(tok_data)
    #print(f"Returning: {tok_list}")
    return tok_list
