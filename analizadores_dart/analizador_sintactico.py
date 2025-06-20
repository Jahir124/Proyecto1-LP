import ply.yacc as yacc
from analizador_lexico import tokens

#Inicio Aporte Jahir Cajas
def p_compiler(p):
    '''compiler : statement_composed'''

def p_statement_composed(p):
    '''statement_composed : statement
                          | statement_composed statement'''

def p_statement(p):
    '''statement : print_stmt
                 | control_structures
                 | function
                 | list_def
                 | variable_def
                 | SEMICOLON
                 | function_call
                 | return_statement
                 | incdec_statement
                 | class_def
                 | object_instantiation'''

def p_variable_def(p):
    '''variable_def : type ID ASSIGN expression SEMICOLON
                    | DYNAMIC ID ASSIGN expression SEMICOLON
                    | VAR ID ASSIGN expression SEMICOLON
                    | STATIC type ID ASSIGN expression SEMICOLON
                    | STATIC VAR ID ASSIGN expression SEMICOLON
                    | STATIC DYNAMIC ID ASSIGN expression SEMICOLON'''

# Print
def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN RPAREN SEMICOLON
                  | PRINT LPAREN value RPAREN SEMICOLON
                  | PRINT LPAREN expression RPAREN SEMICOLON'''

# Expressions
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression INT_DIVIDE expression
                  | expression MODULE expression'''

def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''

def p_expression_value(p):
    '''expression : value'''

def p_expression_incdec(p):
    '''expression : ID INCREMENT
                  | ID DECREMENT
                  | INCREMENT ID
                  | DECREMENT ID'''

def p_incdec_statement(p):
    '''incdec_statement : ID INCREMENT SEMICOLON
                        | ID DECREMENT SEMICOLON
                        | INCREMENT ID SEMICOLON
                        | DECREMENT ID SEMICOLON'''

# Conditionals
def p_control_structures(p):
    '''control_structures : if_block
                          | if_block else_block
                          | while_loop'''

def p_if_block(p):
    '''if_block : IF LPAREN conditions RPAREN LBRACE statement_composed RBRACE'''

def p_else_block(p):
    '''else_block : ELSE LBRACE statement_composed RBRACE'''

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
                           | EQUALS
                           | NOT_EQUALS'''

# Functions
def p_function(p):
    '''function : type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                | VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                | type ID LPAREN RPAREN LBRACE statement_composed RBRACE
                | VOID ID LPAREN RPAREN LBRACE statement_composed RBRACE'''

def p_parameters(p):
    '''parameters : parameter
                  | parameters COMMA parameter'''

def p_parameter(p):
    '''parameter : type ID
                 | REQUIRED type ID'''

def p_function_call(p):
    '''function_call : ID LPAREN RPAREN SEMICOLON
                     | ID LPAREN argument_list RPAREN SEMICOLON'''

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                       | RETURN SEMICOLON'''

def p_while_loop(p):
    '''while_loop : WHILE LPAREN conditions RPAREN LBRACE statement_composed RBRACE'''

def p_class_body(p):
    '''class_body : statement_composed'''

def p_class_def(p):
    '''class_def : CLASS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID LBRACE class_body RBRACE
                 | CLASS ID IMPLEMENTS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID IMPLEMENTS ID LBRACE class_body RBRACE'''

#Data Types
def p_type(p):
    '''type : STRING
            | INT
            | DOUBLE
            | BOOL'''
def p_object_instantiation(p):
    '''object_instantiation : VAR ID ASSIGN NEW ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | type ID ASSIGN NEW ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | VAR ID ASSIGN ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | type ID ASSIGN ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | ID ID ASSIGN NEW ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | ID ID ASSIGN ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | ID ASSIGN NEW ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | ID ASSIGN ID LPAREN argument_list_opt RPAREN SEMICOLON
                            | ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON
                            | ID ASSIGN ID LPAREN RPAREN SEMICOLON
                            | VAR ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON
                            | VAR ID ASSIGN ID LPAREN RPAREN SEMICOLON
                            | type ID ASSIGN NEW ID LPAREN RPAREN SEMICOLON
                            | type ID ASSIGN ID LPAREN RPAREN SEMICOLON
    '''

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                         | empty'''

def p_empty(p):
    'empty :'
    pass


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
             | ID
             | TRUE
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
    v++;
    ++v;
    v--;
    --v;
""")

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)

#fin Aporte Jahir