import ply.lex as lex
from datetime import datetime
import os

reserved = {
    # Tipos de datos primitivos
    "String": "STRING",
    "double": "DOUBLE",
    "int": "INT",
    "bool": "BOOL",
    "num": "NUM",
    "Object": "OBJECT",
    "Null": "NULL",
    
    # Tipos de datos estructurados
    "List": "LIST",
    "Map": "MAP",
    "Set": "SET",
    "Iterable": "ITERABLE",
    
    # Control de flujo
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "while": "WHILE",
    "do": "DO",
    "switch": "SWITCH",
    "case": "CASE",
    "default": "DEFAULT",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    
    # Valores booleanos
    "true": "TRUE",
    "false": "FALSE",
    
    # Declaración de variables
    "var": "VAR",
    "final": "FINAL",
    "const": "CONST",
    "late": "LATE",
    "required": "REQUIRED",
    
    # Funciones
    "Function": "FUNCTION",
    "void": "VOID",
    "async": "ASYNC",
    "await": "AWAIT",
    "sync": "SYNC",
    "yield": "YIELD",
    
    # Programación orientada a objetos
    "class": "CLASS",
    "extends": "EXTENDS",
    "implements": "IMPLEMENTS",
    "with": "WITH",
    "abstract": "ABSTRACT",
    "interface": "INTERFACE",
    "mixin": "MIXIN",
    "super": "SUPER",
    "this": "THIS",
    "new": "NEW",
    "factory": "FACTORY",
    "get": "GET",
    "set": "SETTER",
    "static": "STATIC",
    "operator": "OPERATOR",
    
    # Manejo de excepciones
    "try": "TRY",
    "catch": "CATCH",
    "finally": "FINALLY",
    "throw": "THROW",
    "rethrow": "RETHROW",
    "on": "ON",
    
    # Aserciones y debugging
    "assert": "ASSERT",
    "debugPrint": "DEBUGPRINT",
    
    # Imports y exports
    "import": "IMPORT",
    "export": "EXPORT",
    "library": "LIBRARY",
    "part": "PART",
    "part of": "PART_OF",
    "show": "SHOW",
    "hide": "HIDE",
    "as": "AS",
    "deferred": "DEFERRED",
    
    # Operadores y palabras clave adicionales
    "in": "IN",
    "is": "IS",
    "is!": "IS_NOT",
    "as": "AS",
    "of": "OF",
    "external": "EXTERNAL",
    "typedef": "TYPEDEF",
    "enum": "ENUM",
    "sealed": "SEALED",
    "base": "BASE",
    "interface": "INTERFACE",
    "mixin": "MIXIN_CLASS",
    
    # Funciones de entrada/salida
    "print": "PRINT",
    "stdin": "STDIN",
    "readLineSync": "READLINESYNC",
    "stdout": "STDOUT",
    "stderr": "STDERR",
    
    # Propiedades y métodos comunes
    "length": "LENGTH",
    "isEmpty": "ISEMPTY",
    "isNotEmpty": "ISNOTEMPTY",
    "add": "ADD",
    "remove": "REMOVE",
    "clear": "CLEAR",
    "contains": "CONTAINS",
    "forEach": "FOREACH",
    "map": "MAP_FUNC",
    "where": "WHERE",
    "first": "FIRST",
    "last": "LAST",
    
    # Tipos dinámicos
    "dynamic": "DYNAMIC",
    "Never": "NEVER",
}

# Lista de tokens
tokens = (
    # Identificadores
    'ID',
    
    # Operadores aritméticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE',
    'INT_DIVIDE',
    'POWER',
    
    # Operadores de asignación
    'ASSIGN',
    'PLUS_EQUAL',
    'MINUS_EQUAL',
    'TIMES_EQUAL',
    'DIVIDE_EQUAL',
    'MODULE_EQUAL',
    'INT_DIVIDE_EQUAL',
    'POWER_EQUAL',
    'AND_EQUAL',
    'OR_EQUAL',
    'XOR_EQUAL',
    'LEFT_SHIFT_EQUAL',
    'RIGHT_SHIFT_EQUAL',
    
    # Operadores de comparación
    'EQUALS',
    'NOT_EQUALS',
    'LESS',
    'LESS_EQUAL',
    'GREATER',
    'GREATER_EQUAL',
    'IDENTICAL',
    'NOT_IDENTICAL',
    
    # Operadores lógicos
    'AND',
    'OR',
    'NOT',
    
    # Operadores de bits
    'BITAND',
    'BITOR',
    'BITXOR',
    'BITNOT',
    'LEFT_SHIFT',
    'RIGHT_SHIFT',
    'UNSIGNED_RIGHT_SHIFT',
    
    # Operadores de incremento/decremento
    'INCREMENT',
    'DECREMENT',
    
    # Operadores de acceso
    'DOT',
    'DOUBLE_DOT',
    'TRIPLE_DOT',
    'ARROW',
    'FAT_ARROW',
    'QUESTION_DOT',
    'DOUBLE_COLON',
    
    # Delimitadores
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COMMA',
    'COLON',
    'QUESTION',
    'EXCLAMATION',
    
    # Literales
    'INT_LITERAL',
    'DOUBLE_LITERAL',
    'STRING_LITERAL',
    'CHAR_LITERAL',
    'RAW_STRING_LITERAL',
    'MULTILINE_STRING_LITERAL',
    'BOOLEAN_LITERAL',
    'NULL_LITERAL',
    
    # Símbolos especiales
    'DOLLAR_SIGN',
    'QUOTATION_MARK',
    'SINGLE_QUOTE',
    'CIRCUMFLEX',
    'BACKSLASH',
    'UNDERSCORE',
    'AT_SIGN',
    'HASH',
    'BACKTICK',
    
    # Comentarios (no se incluyen en tokens pero se manejan)
    'COMMENT_SINGLE',
    'COMMENT_MULTI',
    'COMMENT_DOC',
    
) + tuple(reserved.values())

# Reglas de expresiones regulares para operadores
t_PLUS            = r'\+'
t_MINUS           = r'-'
t_TIMES           = r'\*'
t_INT_DIVIDE      = r'~/'
t_DIVIDE          = r'/'
t_MODULE          = r'%'
t_POWER           = r'\*\*'

# Operadores de asignación
t_ASSIGN          = r'='
t_PLUS_EQUAL      = r'\+='
t_MINUS_EQUAL     = r'-='
t_TIMES_EQUAL     = r'\*='
t_DIVIDE_EQUAL    = r'/='
t_MODULE_EQUAL    = r'%='
t_INT_DIVIDE_EQUAL = r'~/='
t_POWER_EQUAL     = r'\*\*='
t_AND_EQUAL       = r'&='
t_OR_EQUAL        = r'\|='
t_XOR_EQUAL       = r'\^='
t_LEFT_SHIFT_EQUAL = r'<<='
t_RIGHT_SHIFT_EQUAL = r'>>='

# Operadores de comparación
t_EQUALS          = r'=='
t_NOT_EQUALS      = r'!='
t_LESS            = r'<'
t_LESS_EQUAL      = r'<='
t_GREATER         = r'>'
t_GREATER_EQUAL   = r'>='
t_IDENTICAL       = r'==='
t_NOT_IDENTICAL   = r'!=='

# Operadores lógicos
t_AND             = r'&&'
t_OR              = r'\|\|'
t_NOT             = r'!'

# Operadores de bits
t_BITAND          = r'&'
t_BITOR           = r'\|'
t_BITXOR          = r'\^'
t_BITNOT          = r'~'
t_LEFT_SHIFT      = r'<<'
t_RIGHT_SHIFT     = r'>>'
t_UNSIGNED_RIGHT_SHIFT = r'>>>'

# Operadores de incremento/decremento
t_INCREMENT       = r'\+\+'
t_DECREMENT       = r'--'

# Operadores de acceso
t_DOT             = r'\.'
t_DOUBLE_DOT      = r'\.\.'
t_TRIPLE_DOT      = r'\.\.\.'
t_ARROW           = r'->'
t_FAT_ARROW       = r'=>'
t_QUESTION_DOT    = r'\?\.'
t_DOUBLE_COLON    = r'::'

# Delimitadores
t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_LBRACE          = r'\{'
t_RBRACE          = r'\}'
t_LBRACKET        = r'\['
t_RBRACKET        = r'\]'
t_SEMICOLON       = r';'
t_COMMA           = r','
t_COLON           = r':'
t_QUESTION        = r'\?'
t_EXCLAMATION     = r'!'

# Símbolos especiales
t_DOLLAR_SIGN     = r'\$'
t_QUOTATION_MARK  = r'\"'
t_SINGLE_QUOTE    = r'\''
t_CIRCUMFLEX      = r'\^'
t_BACKSLASH       = r'\\'
t_UNDERSCORE      = r'_'
t_AT_SIGN         = r'@'
t_HASH            = r'\#'
t_BACKTICK        = r'`'

# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = ' \t\r'

# Comentarios
def t_COMMENT_SINGLE(t):
    r'//.*'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT_DOC(t):
    r'///.*'
    t.lexer.lineno += t.value.count('\n')
    pass

# Literales numéricos
def t_DOUBLE_LITERAL(t):
    r'\d+\.\d+([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Literales de cadena
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover comillas
    return t

def t_RAW_STRING_LITERAL(t):
    r'r\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[2:-1]  # Remover 'r' y comillas
    return t

def t_MULTILINE_STRING_LITERAL(t):
    r'\"\"\"[\s\S]*?\"\"\"'
    t.value = t.value[3:-3]  # Remover comillas triples
    return t

def t_CHAR_LITERAL(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]  # Remover comillas simples
    return t

# Literales booleanos y null
def t_BOOLEAN_LITERAL(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

def t_NULL_LITERAL(t):
    r'null'
    t.value = None
    return t

# Identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Seguimiento de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores léxicos
def t_error(t):
    print(f"[Error Léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()
__all__ = ['tokens', 'lexer']


# while(True):
#     try:
#         s= input('lex > ')
#     except EOFError:
#         break
#     lexer.input(s)
#     for tok in lexer:
#         print(tok)


