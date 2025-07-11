import ply.yacc as yacc
from analizador_lexico import tokens
from datetime import datetime
import os

symbol_table = {}
function_table = set()
semantic_errors = []
function_return_stack = []

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
                | variable_only_def
                 | SEMICOLON
                 | function_call
                 | return_statement
                 | incdec_statement
                 | class_def
                 | object_instantiation
                 '''

def p_empty_statement(p):
    '''statement : 
    '''

def p_variable_only_def(p):
    '''variable_only_def : type ID SEMICOLON
                         | DYNAMIC ID SEMICOLON
                         | VAR ID SEMICOLON
                         | STATIC type ID SEMICOLON
                         | STATIC VAR ID SEMICOLON
                         | STATIC DYNAMIC ID SEMICOLON'''

    # Detecta tipo declarado, incluyendo Set y Set<int>
    declared_type = p[1] if p[1] not in ['var', 'dynamic', 'static'] else None
    var_name = p[3] if p[1] == 'static' else p[2]

    # Si ya existe, error
    if var_name in symbol_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: La variable '{var_name}' ya fue declarada"
        semantic_errors.append(mensaje)
        print(mensaje)
    else:
        # Si es Set o Set<int> se guarda correctamente
        if declared_type and (declared_type.startswith('Set') or declared_type == 'Set'):
            symbol_table[var_name] = declared_type
        elif declared_type:
            symbol_table[var_name] = declared_type
        else:
            symbol_table[var_name] = 'unknown'
            

def p_variable_def(p):
    '''variable_def : type ID ASSIGN expression SEMICOLON
                    | DYNAMIC ID ASSIGN expression SEMICOLON
                    | VAR ID ASSIGN expression SEMICOLON
                    | STATIC type ID ASSIGN expression SEMICOLON
                    | STATIC VAR ID ASSIGN expression SEMICOLON
                    | STATIC DYNAMIC ID ASSIGN expression SEMICOLON
                    | type ID ASSIGN set_value SEMICOLON
                    | VAR ID ASSIGN set_value SEMICOLON
                    | DYNAMIC ID ASSIGN set_value SEMICOLON
                    | STATIC type ID ASSIGN set_value SEMICOLON
                    | STATIC VAR ID ASSIGN set_value SEMICOLON
                    | STATIC DYNAMIC ID ASSIGN set_value SEMICOLON'''

    # Determina el tipo declarado y el nombre de la variable
    declared_type = p[1] if p[1] not in ['var', 'dynamic', 'static'] else None
    var_name = p[3] if p[1] == 'static' else p[2]
    expr_type = p[5] if p[1] == 'static' else p[4]

    # --- SET: Verificación de tipo ---
    # Si la asignación es un set_value, el tipo es 'Set' o 'Set<tipo>'
    if (p.slice[4].type == 'set_value') or (len(p) > 5 and p.slice[5].type == 'set_value'):
        # Si el tipo declarado es Set<algo>, expr_type debe ser Set<algo>
        if declared_type and declared_type.startswith('Set<'):
            # Extrae el tipo esperado, por ejemplo 'int' de 'Set<int>'
            tipo_esperado = declared_type[4:-1].strip()
            # p[4] o p[5] debe ser una lista de tipos de los elementos del set
            tipos_elementos = getattr(p, 'set_element_types', None)
            if tipos_elementos is None and isinstance(expr_type, list):
                tipos_elementos = set(expr_type)
            elif hasattr(p, 'set_element_types'):
                tipos_elementos = set(p.set_element_types)
            else:
                tipos_elementos = set()
            # Si el set está vacío, se permite
            if tipos_elementos and (len(tipos_elementos) > 1 or tipo_esperado not in tipos_elementos):
                mensaje = f"[Error Semántico] Línea {p.lineno(2)}: Todos los elementos de un {declared_type} deben ser de tipo '{tipo_esperado}'. Encontrados: {tipos_elementos}"
                semantic_errors.append(mensaje)
                print(mensaje)
                return
            expr_type = declared_type
        else:
            expr_type = 'Set'

    # --- SET: Error si se asigna un valor que no es set_value ---
    if declared_type and declared_type.startswith('Set'):
        # Si el valor asignado no es un set
        if not (p.slice[4].type == 'set_value' or (len(p) > 5 and p.slice[5].type == 'set_value')):
            mensaje = f"[Error Semántico] Línea {p.lineno(2)}: Solo se puede asignar un conjunto (Set) a una variable de tipo {declared_type}"
            semantic_errors.append(mensaje)
            print(mensaje)
            return

    if expr_type in [None, 'unknown']:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: No se puede asignar una variable no declarada a '{var_name}'. No se añade a la tabla de símbolos."
        print(mensaje)
        semantic_errors.append(mensaje)
        return  

    # --- SET: Guardar el tipo correcto en symbol_table ---
    if declared_type is None or declared_type in ['var', 'dynamic']:
        symbol_table[var_name] = expr_type
    else:
        if declared_type == 'int' and expr_type == 'double':
            del symbol_table[var_name]
            mensaje = f"[Error Semántico] Línea {p.lineno(2)}: Dart no convierte automáticamente de double a int"
            print(mensaje)
            semantic_errors.append(mensaje)
        elif declared_type != expr_type:
            del symbol_table[var_name]
            mensaje = f"[Error semántico] Línea {p.lineno(2)}: Asignación de tipo '{expr_type}' a variable '{var_name}' de tipo '{declared_type}'"
            print(mensaje)
            semantic_errors.append(mensaje)
        else:
            symbol_table[var_name] = declared_type

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

    left_type = p[1]
    right_type = p[3]
    operador = p[2]

    # Reglas para operaciones numéricas
    tipos_validos = ['int', 'double']

    if left_type != right_type:
        mensaje = f"[Advertencia Semántica] Línea {p.lineno(2)}: Operación entre tipos distintos: '{left_type}' y '{right_type}'"
        print(mensaje)
        semantic_errors.append(mensaje)

    if left_type not in tipos_validos or right_type not in tipos_validos:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: Operación inválida entre '{left_type}' y '{right_type}' con operador '{operador}'"
        print(mensaje)
        semantic_errors.append(mensaje)

    p[0] = left_type if left_type == right_type else 'unknown'

def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''

def p_expression_value(p):
    '''expression : value'''
    p[0] = p[1] 



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
                 | NOT value
                 | TRUE
                 | FALSE
                 | ID comparison_operator value
                 | ID comparison_operator ID'''

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
    function_name = p[2]
    return_type = p[1] if p[1] != "VOID" else 'void'

    if function_name in function_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: La función '{function_name}' ya fue declarada"
        semantic_errors.append(mensaje)
        print(mensaje)
    else:
        function_table.add(function_name)

    function_return_stack.append(return_type)  # Guardamos tipo de retorno
    # El statement_composed ya se procesó como parte del parser
    function_return_stack.pop()


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

    function_name = p[1]
    if function_name not in function_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(1)}: La función '{function_name}' no está declarada"
        semantic_errors.append(mensaje)
        print(mensaje)


def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''

    if not function_return_stack:
        return  # No estamos dentro de una función (mal diseño, pero ignoramos)

    expected_type = function_return_stack[-1]

    if len(p) == 4:
        actual_type = p[2]
        if expected_type != 'void' and actual_type != expected_type:
            mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Se esperaba retorno de tipo '{expected_type}', pero se encontró '{actual_type}'"
            semantic_errors.append(mensaje)
            print(mensaje)
        elif expected_type == 'void':
            mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Función 'void' no debe retornar ningún valor"
            semantic_errors.append(mensaje)
            print(mensaje)
    else:
        if expected_type != 'void':
            mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Se esperaba retorno de tipo '{expected_type}', pero no se retornó ningún valor"
            semantic_errors.append(mensaje)
            print(mensaje)


def p_while_loop(p):
    '''while_loop : WHILE LPAREN conditions RPAREN LBRACE statement_composed RBRACE'''
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    p.parser.loop_stack.append('while')
    # Analizar el cuerpo del bucle
    # ... aquí va el análisis normal ...
    p.parser.loop_stack.pop()

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
    



# For loop (Estructura de control)
def p_for_loop(p):
    '''for_loop : FOR LPAREN for_init SEMICOLON conditions SEMICOLON for_update RPAREN LBRACE statement_composed RBRACE
                | FOR LPAREN type ID IN ID RPAREN LBRACE statement_composed RBRACE'''
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    p.parser.loop_stack.append('for')
    # Analizar el cuerpo del bucle
    # ... aquí va el análisis normal ...
    p.parser.loop_stack.pop()


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

def p_set_type(p):
    '''set_type : SET
                | SET LESS type GREATER'''
    # SET o SET<int> como tipo de dato
    if len(p) == 2:
        p[0] = 'Set'
    else:
        p[0] = f'Set<{p[3]}>'

#Data Types
def p_type(p):
    '''type : STRING
            | INT
            | DOUBLE
            | BOOL
            | set_type'''
    if isinstance(p[1], str) and p.slice[1].type == "STRING":
        p[0] = 'String'
    elif isinstance(p[1], str) and p.slice[1].type == "INT":
        p[0] = 'int'
    elif isinstance(p[1], str) and p.slice[1].type == "DOUBLE":
        p[0] = 'double'
    elif isinstance(p[1], str) and p.slice[1].type == "BOOL":
        p[0] = 'bool'
    elif isinstance(p[1], str) and (p.slice[1].type == "set_type" or p[1].startswith('Set')):
        p[0] = p[1]
    else:
        p[0] = 'unknown'

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                         | empty'''

def p_empty(p):
    'empty :'
    pass


# Lists
def p_list_def(p):
    '''list_def : LIST LBRACKET value_list RBRACKET SEMICOLON
                | LIST LESS type GREATER ID ASSIGN LBRACKET value_list RBRACKET SEMICOLON
                | LIST LESS type GREATER ID SEMICOLON'''

def p_value_list(p):
    '''value_list : value
                  | value_list COMMA value'''
    if len(p) == 2:
        # Devuelve una lista con el tipo del valor
        p[0] = [p[1]]
    else:
        # Acumula los tipos de los valores
        p[0] = p[1] + [p[3]]

# Maps (Estructura de datos)
def p_map_def(p):
    '''map_def : MAP LESS type COMMA type GREATER ID ASSIGN LBRACE map_entries RBRACE SEMICOLON
               | MAP ID ASSIGN LBRACE map_entries RBRACE SEMICOLON'''

def p_map_entries(p):
    '''map_entries : map_entry
                   | map_entries COMMA map_entry'''

def p_map_entry(p):
    '''map_entry : value COLON value'''


def p_set_value(p):
    '''set_value : LBRACE value_list RBRACE'''
    # Recoge los tipos de los elementos del set
    tipos = set(p[2]) if isinstance(p[2], list) else set()
    p.set_element_types = tipos
    p[0] = list(tipos) if tipos else 'Set'

# Values
def p_value(p):
    '''value : INT
             | DOUBLE
             | STRING
             | ID
             | TRUE
             | FALSE
             | set_value'''

    if isinstance(p[1], int):
        p[0] = 'int'
    elif isinstance(p[1], float):
        p[0] = 'double'
    elif isinstance(p[1], str) and p.slice[1].type == 'STRING':
        p[0] = 'String'
    elif p[1] == 'true' or p[1] == 'false':
        p[0] = 'bool'
    elif p.slice[1].type == 'set_value':
        # Si el set está vacío, devuelve 'Set'
        if p[1] == 'Set':
            p[0] = 'Set'
        elif isinstance(p[1], list) and len(p[1]) == 1:
            # Si solo hay un tipo, devuelve ese tipo
            p[0] = p[1][0]
        elif isinstance(p[1], list) and len(set(p[1])) == 1:
            p[0] = p[1][0]
        else:
            p[0] = 'Set'
    else:  # ID
        nombre = p[1]
        if nombre in symbol_table:
            p[0] = symbol_table[nombre]
        else:
            mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Variable '{nombre}' no declarada"
            semantic_errors.append(mensaje)
            print(mensaje)

def p_statement_expression(p):
    '''statement : expression SEMICOLON'''


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


# Exportar cosas que usará main.py
__all__ = [
    'parser',
    'semantic_errors',
    'sintactic_results',
    'symbol_table',
    'function_table'
]

# while True:
#     try:
#         s = input('sintax > ')  # Use raw_input() in Python 2
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser.parse(s)
#     print(result)  # Imprime el resultado del análisis sintáctico
#     print(symbol_table)

def p_break_stmt(p):
    'statement : BREAK SEMICOLON'
    # Verificar si estamos dentro de un bucle
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    if not p.parser.loop_stack:
        mensaje = f"[Error Semántico] Línea {p.lineno(1)}: 'break' fuera de un bucle"
        semantic_errors.append(mensaje)
        print(mensaje)
