import ply.lex as lex
from datetime import datetime
import os
reserved = {
    "String": "STRING",
    "double": "DOUBLE",
    "int": "INT",
    "bool": "BOOL",
    "List": "LIST",
    "Map": "MAP",
    "if": "IF",
    "else": "ELSE",
    "true": "TRUE",
    "false": "FALSE",
    "in": "IN",
    "var": "VAR",
    "void": "VOID",
    "final": "FINAL",
    "const": "CONST",
    "Function": "FUNCTION",
    "for": "FOR",
    "while": "WHILE",
    "required": "REQUIRED",
    "return": "RETURN",
    "set": "SET",
    "this": "THIS",
    "print": "PRINT",
    "length": "LENGTH",
    "dynamic": "DYNAMIC",
    "stdin": "STDIN",
    "readLineSync": "READLINESYNC",
    "class": "CLASS",
    "extends": "EXTENDS",
    "implements": "IMPLEMENTS",
    "with": "WITH",
    "static": "STATIC",
    "abstract": "ABSTRACT",
    "enum": "ENUM",
    "super": "SUPER",
    "try": "TRY",
    "catch": "CATCH",
    "finally": "FINALLY",
    "throw": "THROW",
    "assert": "ASSERT",
    "break": "BREAK",
    "continue": "CONTINUE",
    "switch": "SWITCH",
    "case": "CASE",
    "default": "DEFAULT",
    "do": "DO",
    "import": "IMPORT",
    "export": "EXPORT",
    "library": "LIBRARY",
    "part": "PART",
    "of": "OF",
    "as": "AS",
    "is": "IS",
    "new" : "NEW"
}

# Lista de tokens
tokens = (
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE',
    'EQUALS',
    'NOT_EQUALS',
    'LESS',
    'LESS_EQUAL',
    'GREATER',
    'GREATER_EQUAL',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'DOUBLE_COLON',
    'QUESTION',
    'COMMA',
    'AND',
    'OR',
    'NOT',
    'BITNOT',
    'DOT',
    'INCREMENT',
    'DECREMENT',
    'ARROW',
    'INT_DIVIDE',
    'COLON',
    'PLUS_EQUAL',
    'MINUS_EQUAL',
    'TIMES_EQUAL',
    'DIVIDE_EQUAL',
    'MODULE_EQUAL',
    'DOLLAR_SIGN',
    'QUOTATION_MARK',
    'SINGLE_QUOTE',
    'CIRCUMFLEX',
) + tuple(reserved.values())


# Reglas de expresiones regulares
t_PLUS            = r'\+'
t_MINUS           = r'-'
t_TIMES           = r'\*'
t_INT_DIVIDE      = r'~/'
t_DIVIDE          = r'/'
t_MODULE          = r'%'
t_EQUALS          = r'=='
t_NOT_EQUALS      = r'!='
t_LESS            = r'<'
t_LESS_EQUAL      = r'<='
t_GREATER         = r'>'
t_GREATER_EQUAL   = r'>='
t_ASSIGN          = r'='
t_PLUS_EQUAL      = r'\+='
t_MINUS_EQUAL     = r'-='
t_TIMES_EQUAL     = r'\*='
t_DIVIDE_EQUAL    = r'/='
t_MODULE_EQUAL    = r'%='
t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_LBRACE          = r'\{'
t_RBRACE          = r'\}'
t_LBRACKET        = r'\['
t_RBRACKET        = r'\]'
t_SEMICOLON       = r';'
t_COMMA           = r','
t_AND             = r'&&'
t_OR              = r'\|\|'
t_NOT             = r'!'
t_BITNOT          = r'~'
t_DOT             = r'\.'
t_INCREMENT       = r'\+\+'
t_DECREMENT       = r'--'
t_ARROW           = r'=>'
t_COLON           = r':'
t_DOUBLE_COLON    = r'::'
t_QUESTION        = r'\?'
t_DOLLAR_SIGN     = r'\$'
t_QUOTATION_MARK  = r'\"'
t_SINGLE_QUOTE    = r'\''
t_CIRCUMFLEX      = r'\^'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Comentarios
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    pass  # Ignora comentarios multilínea

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

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

#Construcción del lexer
lexer = lex.lex()


# while(True):
#     try:
#         s= input('lex > ')
#     except EOFError:
#         break
#     lexer.input(s)
#     for tok in lexer:
#         print(tok)



# lexic_results = []
# def analyze_tokens(data):
#     global results
#     lexic_results.clear()
#     lexer.input(data)

#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         lexic_results.append(str(tok))
#         print(tok)

#     return lexic_results

# algorithm = """

# """

# result = analyze_tokens(algorithm)

# username = "drac2606" #Cambien su username
# file_test = r"C:\Users\Dario_Anchundia\Documents\GitHub\Proyecto1-LP\algoritmos_dart\algoritmo_dario.dart" #Cambien su local path

# os.makedirs("logs", exist_ok=True)

# with open(file_test, "r", encoding="utf-8") as f:
#     data = f.read()

# ahora = datetime.now()
# fecha_hora = ahora.strftime("%d-%m-%Y-%Hh%M")
# log_filename = f"logs/lexico-{username}-{fecha_hora}.txt"

# with open(log_filename, "w", encoding="utf-8") as log_file:
#     lexer.input(data)
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         print(tok)
#         log_file.write(str(tok) + '\n')

# print(f"\nTokens de {username} guardados en: {log_filename}")


