#-----------
# Parser for Valuation
# ----------

from parsers.log_lexer import lexer, tokens
import ply.yacc as yacc

precedence = (    
    ('left', 'CONJUNCT', 'DISJUNCT', 'CONDITIONAL', 'BICONDITIONAL'),
    ('left', 'NEGATION'),
)

def p_term_factor(p):
    'wff : subwff'
    p[0] = p[1]

def p_factor_expr(p):
    'subwff : LPAREN subwff RPAREN'
    p[0] = p[2]

def p_wff_biconditional(p):
    'subwff : subwff BICONDITIONAL subwff'
    #p[0] = f"({p[1]}<->{p[3]})"
    if p[1] == p[3]:
        p[0] = 1 
    else:
        p[0] = 0

def p_wff_disjunction(p):
    'subwff : subwff DISJUNCT subwff'
    #p[0] = f"({p[1]}v{p[3]})"
    p[0] = max(p[1], p[3])

def p_wff_conjunction(p):
    'subwff : subwff CONJUNCT subwff'
    #p[0] = f"({p[1]}^{p[3]})"
    p[0] = min(p[1], p[3])

def p_wff_conditional(p):
    'subwff : subwff CONDITIONAL subwff'
    #p[0] = f"({p[1]}->{p[3]})"
    p[0] = max(1-p[1], p[3])

def p_sub_wff_negation(p):
    'subwff : NEGATION subwff'
    #p[0] = f"~({p[2]})"    
    if p[2] == 1: 
        p[0] = 0
    elif p[2] == 0:
        p[0] = 1
    else: 
        p[0] = p[0]

def p_factor_letter(p):
    'subwff : LETTER'
    p[0] = p[1]

def p_factor_tvalue(p):
    'subwff : TVALUE'
    p[0] = int(p[1])

#def p_empty(p):
#    'empty :'

def p_error(p):    
    print("Syntax error in input!")

truth_value_parser = yacc.yacc() #debug=True

# Testing
#tv_parser = truth_value_parser.parse("1^1^0")
#print(tv_parser)


