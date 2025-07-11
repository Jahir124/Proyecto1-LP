import ply.yacc as yacc
from analizador_lexico import tokens
from datetime import datetime
import os

# ============================================================================
# VARIABLES GLOBALES Y TABLAS DE SÍMBOLOS
# ============================================================================

symbol_table = {}          # Tabla de símbolos para variables
function_table = set()     # Tabla de funciones declaradas
semantic_errors = []       # Lista de errores semánticos
function_return_stack = [] # Pila para tipos de retorno de funciones
sintactic_results = []     # Resultados del análisis sintáctico

# ============================================================================
# REGLAS GRAMATICALES PRINCIPALES
# ============================================================================

def p_compiler(p):
    '''compiler : statement_composed'''
    p[0] = p[1]

def p_statement_composed(p):
    '''statement_composed : statement
                          | statement_composed statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

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
                 | break_stmt
                 | expression SEMICOLON'''
    p[0] = p[1]

def p_empty_statement(p):
    '''statement : '''
    p[0] = None

# ============================================================================
# DECLARACIÓN DE VARIABLES
# ============================================================================

def p_variable_only_def(p):
    '''variable_only_def : type ID SEMICOLON
                         | DYNAMIC ID SEMICOLON
                         | VAR ID SEMICOLON
                         | STATIC type ID SEMICOLON
                         | STATIC VAR ID SEMICOLON
                         | STATIC DYNAMIC ID SEMICOLON'''
    
    # Determinar el tipo declarado
    declared_type = p[1] if p[1] in ['int', 'double', 'String', 'bool'] else None
    var_name = p[3] if p[1] == 'static' else p[2]
    
    # Verificar si la variable ya fue declarada
    if var_name in symbol_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: La variable '{var_name}' ya fue declarada"
        semantic_errors.append(mensaje)
        print(mensaje)
    else:
        symbol_table[var_name] = declared_type if declared_type else 'unknown'
    
    p[0] = 'variable_declaration'

def p_variable_def(p):
    '''variable_def : type ID ASSIGN expression SEMICOLON
                    | DYNAMIC ID ASSIGN expression SEMICOLON
                    | VAR ID ASSIGN expression SEMICOLON
                    | STATIC type ID ASSIGN expression SEMICOLON
                    | STATIC VAR ID ASSIGN expression SEMICOLON
                    | STATIC DYNAMIC ID ASSIGN expression SEMICOLON'''
    # Determinar el tipo declarado y el nombre de la variable
    declared_type = p[1] if p[1] in ['int', 'double', 'String', 'bool', 'Set'] else None
    if p[1] == 'static':
        declared_type = p[2] if p[2] in ['int', 'double', 'String', 'bool', 'Set'] else None
    
    var_name = p[3] if p[1] == 'static' else p[2]
    expr_type = p[5] if p[1] == 'static' else p[4]
    # Verificar que la expresión tenga un tipo válido
    if expr_type in [None, 'unknown']:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: No se puede asignar una variable no declarada a '{var_name}'. No se añade a la tabla de símbolos."
        print(mensaje)
        semantic_errors.append(mensaje)
        return
    # Agregar a la tabla de símbolos
    symbol_table[var_name] = expr_type
    # Verificar compatibilidad de tipos
    if declared_type is not None:
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
    p[0] = 'variable_assignment'

# ============================================================================
# EXPRESIONES
# ============================================================================

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
    p[0] = p[2]

def p_expression_value(p):
    '''expression : value'''
    p[0] = p[1]

def p_expression_incdec(p):
    '''expression : ID INCREMENT
                  | ID DECREMENT'''
    p[0] = 'increment_decrement'

def p_expression_property_access(p):
    '''expression : expression DOT ID
                  | expression DOT function_call'''
    p[0] = 'property_access'

def p_expression_method_call(p):
    '''expression : expression DOT ID LPAREN argument_list_opt RPAREN'''
    p[0] = 'method_call'

def p_expression_compound_assign(p):
    '''expression : ID PLUS_EQUAL expression
                  | ID MINUS_EQUAL expression
                  | ID TIMES_EQUAL expression
                  | ID DIVIDE_EQUAL expression
                  | ID MODULE_EQUAL expression'''
    p[0] = 'compound_assign'

def p_expression_unary(p):
    '''expression : INCREMENT ID
                  | DECREMENT ID
                  | PLUS ID
                  | MINUS ID'''
    p[0] = 'unary_op'

def p_expression_ternary(p):
    '''expression : expression QUESTION expression COLON expression'''
    p[0] = 'ternary'

def p_expression_cascade(p):
    '''expression : expression DOUBLE_DOT expression'''
    p[0] = 'cascade'

def p_expression_lambda_anywhere(p):
    '''expression : LPAREN parameters RPAREN ARROW expression
                  | LPAREN RPAREN ARROW expression'''
    p[0] = 'lambda_anywhere'

def p_expression_bool_null_literals(p):
    '''expression : TRUE
                  | FALSE
                  | NULL_LITERAL'''
    p[0] = 'bool_or_null_literal'

# ============================================================================
# ESTRUCTURAS DE CONTROL
# ============================================================================

def p_control_structures(p):
    '''control_structures : if_block
                          | if_block else_block
                          | while_loop
                          | for_loop'''
    p[0] = p[1]

def p_if_block(p):
    '''if_block : IF LPAREN conditions RPAREN LBRACE statement_composed RBRACE'''
    p[0] = 'if_statement'

def p_else_block(p):
    '''else_block : ELSE LBRACE statement_composed RBRACE'''
    p[0] = 'else_statement'

def p_conditions(p):
    '''conditions : condition
                  | conditions AND condition
                  | conditions OR condition'''
    p[0] = p[1]

def p_condition(p):
    '''condition : value comparison_operator value
                 | NOT value
                 | TRUE
                 | FALSE
                 | ID comparison_operator value
                 | ID comparison_operator ID'''
    p[0] = 'condition'

def p_comparison_operator(p):
    '''comparison_operator : GREATER
                           | LESS
                           | GREATER_EQUAL
                           | LESS_EQUAL
                           | EQUALS
                           | NOT_EQUALS'''
    p[0] = p[1]

def p_while_loop(p):
    '''while_loop : WHILE LPAREN conditions RPAREN LBRACE statement_composed RBRACE'''
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    p.parser.loop_stack.append('while')
    p[0] = 'while_loop'
    p.parser.loop_stack.pop()

def p_for_loop(p):
    '''for_loop : FOR LPAREN for_init SEMICOLON conditions SEMICOLON for_update RPAREN LBRACE statement_composed RBRACE
                | FOR LPAREN type ID IN ID RPAREN LBRACE statement_composed RBRACE'''
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    p.parser.loop_stack.append('for')
    p[0] = 'for_loop'
    p.parser.loop_stack.pop()

def p_for_init(p):
    '''for_init : variable_def
                | empty'''
    p[0] = p[1]

def p_for_update(p):
    '''for_update : incdec_statement
                  | ID ASSIGN expression
                  | empty'''
    p[0] = p[1]

def p_break_stmt(p):
    'break_stmt : BREAK SEMICOLON'
    if not hasattr(p.parser, 'loop_stack'):
        p.parser.loop_stack = []
    if not p.parser.loop_stack:
        mensaje = f"[Error Semántico] Línea {p.lineno(1)}: 'break' fuera de un bucle"
        semantic_errors.append(mensaje)
        print(mensaje)
    p[0] = 'break_statement'

def p_for_in_loop(p):
    '''for_in_loop : FOR LPAREN VAR ID IN ID RPAREN LBRACE statement_composed RBRACE
                   | FOR LPAREN type ID IN ID RPAREN LBRACE statement_composed RBRACE'''
    # Declarar la variable del loop en la tabla de símbolos
    var_name = p[4]
    var_type = p[3] if len(p) == 12 else 'dynamic'
    symbol_table[var_name] = var_type
    p[0] = 'for_in_loop'

def p_try_catch_block(p):
    '''try_catch_block : TRY LBRACE statement_composed RBRACE CATCH LPAREN ID RPAREN LBRACE statement_composed RBRACE'''
    # Declarar la variable de excepción en la tabla de símbolos
    exception_var = p[7]
    symbol_table[exception_var] = 'Exception'
    p[0] = 'try_catch_block'

# ============================================================================
# FUNCIONES
# ============================================================================

def p_function(p):
    '''function : type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                | VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                | type ID LPAREN RPAREN LBRACE statement_composed RBRACE
                | VOID ID LPAREN RPAREN LBRACE statement_composed RBRACE
                | type ID LPAREN optional_parameters RPAREN LBRACE statement_composed RBRACE
                | VOID ID LPAREN optional_parameters RPAREN LBRACE statement_composed RBRACE'''
    
    function_name = p[2]
    return_type = p[1] if p[1] != "VOID" else 'void'
    
    if function_name in function_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(2)}: La función '{function_name}' ya fue declarada"
        semantic_errors.append(mensaje)
        print(mensaje)
    else:
        function_table.add(function_name)
    
    function_return_stack.append(return_type)
    function_return_stack.pop()
    
    p[0] = 'function_declaration'

def p_parameters(p):
    '''parameters : parameter
                  | parameters COMMA parameter'''
    p[0] = p[1]

def p_parameter(p):
    '''parameter : type ID
                 | REQUIRED type ID'''
    p[0] = 'parameter'

def p_optional_parameters(p):
    '''optional_parameters : LBRACKET parameters RBRACKET
                          | LBRACE named_parameters RBRACE'''
    p[0] = 'optional_or_named_params'

def p_named_parameters(p):
    '''named_parameters : named_parameter
                        | named_parameters COMMA named_parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_named_parameter(p):
    '''named_parameter : type ID
                       | REQUIRED type ID'''
    p[0] = 'named_param'

def p_function_call(p):
    '''function_call : ID LPAREN RPAREN SEMICOLON
                     | ID LPAREN argument_list RPAREN SEMICOLON'''
    
    function_name = p[1]
    if function_name not in function_table:
        mensaje = f"[Error Semántico] Línea {p.lineno(1)}: La función '{function_name}' no está declarada"
        semantic_errors.append(mensaje)
        print(mensaje)
    
    p[0] = 'function_call'

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''
    p[0] = p[1]

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                         | empty'''
    p[0] = p[1]

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    
    if not function_return_stack:
        return
    
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
    
    p[0] = 'return_statement'

def p_lambda_function(p):
    '''lambda_function : type ID ASSIGN LPAREN parameters RPAREN ARROW expression SEMICOLON
                       | VAR ID ASSIGN LPAREN parameters RPAREN ARROW expression SEMICOLON
                       | type ID ASSIGN LPAREN RPAREN ARROW expression SEMICOLON
                       | VAR ID ASSIGN LPAREN RPAREN ARROW expression SEMICOLON'''
    p[0] = 'lambda_function'

def p_anonymous_function(p):
    '''anonymous_function : LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                         | LPAREN RPAREN LBRACE statement_composed RBRACE'''
    p[0] = 'anonymous_function'

def p_variable_def_anonymous_func(p):
    '''variable_def : VAR ID ASSIGN anonymous_function SEMICOLON
                    | type ID ASSIGN anonymous_function SEMICOLON'''
    p[0] = 'var_anon_func'

# ============================================================================
# ESTRUCTURAS DE DATOS
# ============================================================================

def p_list_def(p):
    '''list_def : LIST LBRACKET value_list RBRACKET SEMICOLON
                | LIST LESS type GREATER ID ASSIGN LBRACKET value_list RBRACKET SEMICOLON
                | LIST LESS type GREATER ID SEMICOLON
                | LIST LESS type GREATER ID ASSIGN LBRACKET list_of_lists RBRACKET SEMICOLON'''
    p[0] = 'list_definition'

def p_value_list(p):
    '''value_list : value
                  | value_list COMMA value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_list_of_lists(p):
    '''list_of_lists : LBRACKET value_list RBRACKET
                     | list_of_lists COMMA LBRACKET value_list RBRACKET'''
    if len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = p[1] + [p[4]]

def p_map_def(p):
    '''map_def : MAP LESS type COMMA type GREATER ID ASSIGN LBRACE map_entries RBRACE SEMICOLON
               | MAP ID ASSIGN LBRACE map_entries RBRACE SEMICOLON
               | MAP LESS type COMMA type GREATER ID ASSIGN LBRACE map_of_lists RBRACE SEMICOLON'''
    p[0] = 'map_definition'

def p_map_entries(p):
    '''map_entries : map_entry
                   | map_entries COMMA map_entry'''
    p[0] = p[1]

def p_map_entry(p):
    '''map_entry : value COLON value'''
    p[0] = 'map_entry'

def p_map_of_lists(p):
    '''map_of_lists : map_list_entry
                    | map_of_lists COMMA map_list_entry'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_map_list_entry(p):
    '''map_list_entry : value COLON LBRACKET value_list RBRACKET'''
    p[0] = (p[1], p[4])

def p_set_value(p):
    '''set_value : LBRACE value_list RBRACE'''
    tipos = set(p[2]) if isinstance(p[2], list) else set()
    if len(tipos) > 1:
        mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Todos los elementos de un Set deben ser del mismo tipo. Encontrados: {tipos}"
        semantic_errors.append(mensaje)
        print(mensaje)
    p[0] = 'Set' if tipos else 'unknown'

# ============================================================================
# CLASES Y OBJETOS
# ============================================================================

def p_class_def(p):
    '''class_def : CLASS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID LBRACE class_body RBRACE
                 | CLASS ID IMPLEMENTS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID IMPLEMENTS ID LBRACE class_body RBRACE
                 | CLASS ID EXTENDS ID WITH ID IMPLEMENTS ID LBRACE class_body RBRACE'''
    p[0] = 'class_definition'

def p_class_body(p):
    '''class_body : class_member
                  | class_body class_member'''
    p[0] = p[1]

def p_class_member(p):
    '''class_member : class_property
                    | class_method
                    | constructor'''
    p[0] = p[1]

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
    p[0] = 'class_property'

def p_class_method(p):
    '''class_method : type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | type ID LPAREN RPAREN LBRACE statement_composed RBRACE
                    | VOID ID LPAREN RPAREN LBRACE statement_composed RBRACE
                    | STATIC type ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                    | STATIC VOID ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE'''
    p[0] = 'class_method'

def p_constructor(p):
    '''constructor : ID LPAREN parameters RPAREN LBRACE statement_composed RBRACE
                   | ID LPAREN RPAREN LBRACE statement_composed RBRACE'''
    p[0] = 'constructor'

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
                            | type ID ASSIGN ID LPAREN RPAREN SEMICOLON'''
    p[0] = 'object_instantiation'

# ============================================================================
# ENTRADA/SALIDA
# ============================================================================

def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN RPAREN SEMICOLON
                  | PRINT LPAREN value RPAREN SEMICOLON
                  | PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = 'print_statement'

def p_input_stmt(p):
    '''input_stmt : STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON
                  | VAR ID ASSIGN STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON
                  | type ID ASSIGN STDIN DOT READLINESYNC LPAREN RPAREN SEMICOLON'''
    p[0] = 'input_statement'

# ============================================================================
# TIPOS DE DATOS
# ============================================================================

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

def p_set_type(p):
    '''set_type : SET
                | SET LESS type GREATER'''
    if len(p) == 2:
        p[0] = 'Set'
    else:
        p[0] = f'Set<{p[3]}>'

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
        p[0] = 'Set'
    else:  # ID
        nombre = p[1]
        if nombre in symbol_table:
            p[0] = symbol_table[nombre]
        else:
            mensaje = f"[Error Semántico] Línea {p.lineno(1)}: Variable '{nombre}' no declarada"
            semantic_errors.append(mensaje)
            print(mensaje)

# ============================================================================
# UTILIDADES
# ============================================================================

def p_incdec_statement(p):
    '''incdec_statement : ID INCREMENT SEMICOLON
                        | ID DECREMENT SEMICOLON
                        | INCREMENT ID SEMICOLON
                        | DECREMENT ID SEMICOLON'''
    p[0] = 'incdec_statement'

def p_empty(p):
    'empty :'
    pass

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

def p_error(p):
    if p:
        err_msg = f"Syntax error at token '{p.type}' (value: '{p.value}') on line {p.lineno}"
    else:
        err_msg = "Syntax error at EOF"
    sintactic_results.append(err_msg)
    print(err_msg)

# ============================================================================
# CONSTRUCCIÓN DEL PARSER
# ============================================================================

parser = yacc.yacc()

# ============================================================================
# FUNCIÓN DE PRUEBA
# ============================================================================

def test_parser():
    test_code = '''
    // Declaración de variables
    int x = 5;
    var nombre = "Juan";
    bool aprobado = true;
    
    // Expresiones aritméticas
    x = x + 10;
    y = (x - 2) / 3;
    x += 10;
    
    // Estructuras de control
    if (x > 0) {
        print("Positivo");
    } else {
        print("Negativo");
    }
    
    // Funciones
    int sumar(int a, int b) {
        return a + b;
    }
    
    void saludar() {
        print("Hola");
    }
    
    // Clases
    class Persona {
        String nombre;
        int edad;
        
        Persona(this.nombre, this.edad);
        
        void hablar() {
            print("Hola, soy $nombre");
        }
    }
    
    // Instanciación
    var p = Persona("Luis", 25);
    p.hablar();
    '''
    
    try:
        result = parser.parse(test_code)
        print("✅ Análisis sintáctico completado exitosamente")
        print(f"📊 Tabla de símbolos: {symbol_table}")
        print(f"🔧 Funciones declaradas: {function_table}")
        print(f"❌ Errores semánticos: {len(semantic_errors)}")
        print(f"⚠️  Errores sintácticos: {len(sintactic_results)}")
        return result
    except Exception as e:
        print(f"❌ Error en el análisis: {e}")
        return None

# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'parser',
    'semantic_errors',
    'sintactic_results',
    'symbol_table',
    'function_table',
    'test_parser'
]

# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    print("🧪 Probando analizador sintáctico...")
    test_parser()

