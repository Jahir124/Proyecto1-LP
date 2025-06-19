import ply.yacc as yacc
from analizador_lexico import tokens

#Inicio Aporte Jahir Cajas
def p_compiler(p):
    '''compiler : statement_composed'''

def p_statement_composed(p):
    '''statement_composed : statement
                      | statement_composed statement'''

def p_statement(p):
    '''statement : print
                 | control_structures
                 | function
                 | list_def
                 | variable_def
                 | SEMICOLON'''

def p_variable_def(p):
    '''variable_def : type ID ASSIGN expression SEMICOLON
                           | DYNAMIC ID ASSIGN expression SEMICOLON
                           | VAR ID ASSIGN expression SEMICOLON
                           | STATIC type ID ASSIGN expression SEMICOLON
                           | STATIC VAR ID ASSIGN expression SEMICOLON
                           | STATIC DYNAMIC ID ASSIGN expression SEMICOLON'''

# Print
def p_print(p):
    '''print : PRINT LPAREN RPAREN SEMICOLON
             | PRINT LPAREN value RPAREN SEMICOLON
             | PRINT LPAREN expression RPAREN SEMICOLON'''

# Expressions
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

def p_expression_simplified(p):
    '''expression : value PLUS value'''


def p_expression_value(p):
    '''expression : value'''


# Conditionals
def p_control_structures(p):
    '''control_structures : if_block
                          | if_block else_block'''

def p_if_block(p):
    '''if_block : IF LPAREN conditions RPAREN LBRACKET statement_composed RBRACKET'''


def p_else_block(p):
    '''else_block : ELSE LBRACKET statement_composed RBRACKET'''


def p_conditions(p):
    '''conditions : condition
                  | conditions AND condition
                  | conditions OR condition'''

def p_condition(p):
    '''condition : value comparison_operator value
                 | NOT value'''

def p_comparison_operator(p):
    '''comparison_operator : GREATER
                  | LESS
                  | GREATER_EQUAL
                  | LESS_EQUAL
                  | EQUALS'''

# Functions
def p_function(p):
    '''function : type ID LPAREN parameters RPAREN LBRACKET statement_composed RBRACKET
                | VOID ID LPAREN parameters RPAREN LBRACKET statement_composed RBRACKET
                | type ID LPAREN RPAREN LBRACKET statement_composed RBRACKET
                | VOID ID LPAREN RPAREN LBRACKET statement_composed RBRACKET'''

def p_parameters(p):
    '''parameters : parameter
                      | parameters COMMA parameter'''

def p_parameter(p):
    '''parameter : type ID
                 | REQUIRED type ID'''

#Data Types
def p_type(p):
    '''type : STRING
            | INT
            | DOUBLE
            | BOOL'''

# Lists
def p_list_def(p):
    '''list_def : LIST LBRACKET value_list RBRACKET SEMICOLON
                       | LIST LESS type GREATER ID ASSIGN LBRACKET value_list RBRACKET SEMICOLON'''

def p_value_list(p):
    '''value_list : value
                  | value_list COMMA value'''

# Values
def p_value(p):
    '''value : INT
             | FLOAT
             | STRING
             | ID'''

def p_value_bool(p):
    '''value : TRUE
             | FALSE'''

sintactic_results = []

#Error Handling
def p_error(p):
    if p:
        err_msg = f"Syntax error at token '{p.type}' (value: '{p.value}') on line {p.lineno}"
    else:
        err_msg = "Syntax error at EOF"
    sintactic_results.append(err_msg)
    print(err_msg)

parser = yacc.yacc()


def test_parser(input_code):
    result = parser.parse(input_code)
    msg = f"Parsing result : {result}"
    sintactic_results.append(msg)
    print(msg)

test_parser("""
    int v = 10;
""")

#fin Aporte Jahir Cajas