import ply.yacc as yacc
from analizador_lexico import tokens
from datetime import datetime
import os

#Inicio Aporte Jahir Cajas
def p_compiler(p):
    '''compiler : statement_composed'''

def p_statement_composed(p):
    '''statement_composed : statement
                          | statement_composed statement'''

def p_statement(p):
    '''statement : print_stmt
                 | input_stmt
                 | control_structures
                 | function
                 | lambda_function
                 | list_def
                 | map_def
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

# Input
def p_input_stmt(p):
    '''input_stmt : STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON
                  | VAR ID ASSIGN STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON
                  | type ID ASSIGN STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON'''

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


# Conditionals
def p_control_structures(p):
    '''control_structures : if_block
                          | if_block else_block
                          | while_loop
                          | for_loop'''

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
    
# APORTE JAVIER RODRIGUEZ    
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

def p_class_body(p):
    '''class_body : class_member
                  | class_body class_member'''

def p_class_def(p):
    '''class_def : CLASS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID LBRACE class_body RBRACE
                 | CLASS ID IMPLEMENTS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID IMPLEMENTS ID LBRACE class_body RBRACE'''
#FIN APORTE


# For loop (Estructura de control)
def p_for_loop(p):
    '''for_loop : FOR LPAREN for_init SEMICOLON conditions SEMICOLON for_update RPAREN LBRACE statement_composed RBRACE
                | FOR LPAREN type ID IN ID RPAREN LBRACE statement_composed RBRACE'''


def p_for_init(p):
    '''for_init : variable_def
                | empty'''

def p_for_update(p):
    '''for_update : incdec_statement
                  | ID ASSIGN expression
                  | empty'''


def p_class_member(p):
    '''class_member : class_property
                    | class_method
                    | constructor'''

def p_class_property(p):
    '''class_property : type ID SEMICOLON
                      | VAR ID SEMICOLON
                      | FINAL type ID SEMICOLON
                      | CONST type ID SEMICOLON
                      | STATIC type ID SEMICOLON
                      | type ID ASSIGN expression SEMICOLON
                      | VAR ID ASSIGN expression SEMICOLON
                      | FINAL type ID ASSIGN expression SEMICOLON
                      | CONST type ID ASSIGN expression SEMICOLON
                      | STATIC type ID ASSIGN expression SEMICOLON'''

def p_class_method(p):
    '''class_method : type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | type ID LPAREN RPAREN LBRACE statement_composed RBRACE
                    | VOID ID LPAREN RPAREN LBRACE statement_composed RBRACE
                    | STATIC type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | STATIC VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE'''

def p_constructor(p):
    '''constructor : ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                   | ID LPAREN RPAREN LBRACE statement_composed RBRACE'''


#Data Types
def p_type(p):
    '''type : STRING
            | INT
            | DOUBLE
            | BOOL'''

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

# Maps (Estructura de datos)
def p_map_def(p):
    '''map_def : MAP LESS type COMMA type GREATER ID ASSIGN LBRACE map_entries RBRACE SEMICOLON
               | MAP ID ASSIGN LBRACE map_entries RBRACE SEMICOLON'''

def p_map_entries(p):
    '''map_entries : map_entry
                   | map_entries COMMA map_entry'''

def p_map_entry(p):
    '''map_entry : value COLON value'''

# Values
def p_value(p):
    '''value : INT
             | FLOAT
             | STRING
             | ID
             | TRUE
             | FALSE'''

# Lambda functions (Tipo de función)
def p_lambda_function(p):
    '''lambda_function : type ID ASSIGN LPAREN parameters RPAREN ARROW expression SEMICOLON
                       | VAR ID ASSIGN LPAREN parameters RPAREN ARROW expression SEMICOLON
                       | type ID ASSIGN LPAREN RPAREN ARROW expression SEMICOLON
                       | VAR ID ASSIGN LPAREN RPAREN ARROW expression SEMICOLON'''

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

def analyze_syntax(data):
    sintactic_results.clear()
    result = parser.parse(data)
    sintactic_results.append(f"Parsing result : {result}")
    print(f"Parsing result : {result}")
    return sintactic_results

import os
from datetime import datetime

# Variables que usas para nombre usuario y archivo de prueba
username = "drac2606"  # Cambia por tu usuario
file_test = r"C:\Users\Dario_Anchundia\Documents\GitHub\Proyecto1-LP\algoritmos_dart\algoritmo_dario.dart"  # Cambia por tu ruta local

os.makedirs("logs", exist_ok=True)  # Crea carpeta logs si no existe

# Leer archivo de entrada
with open(file_test, "r", encoding="utf-8") as f:
    data = f.read()

# Limpiar resultados anteriores
sintactic_results.clear()

# Parsear el código fuente
parser.parse(data)

# Crear nombre del archivo log con fecha y hora
ahora = datetime.now()
fecha_hora = ahora.strftime("%d-%m-%Y-%Hh%M")
log_filename = f"logs/sintactico-{username}-{fecha_hora}.txt"

# Guardar resultados en el archivo de log
with open(log_filename, "w", encoding="utf-8") as log_file:
    for line in sintactic_results:
        print(line)             # Opcional: imprimir en consola
        log_file.write(line + "\n")

print(f"\nTokens sintácticos de {username} guardados en: {log_filename}")

#fin Aporte Jahir