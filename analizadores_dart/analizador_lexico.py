import ply.lex as lex

# Lista de tokens
tokens = [
    'ID', 'FLOAT', 'INT', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMI', 'COMMA', 'AND', 'OR', 'NOT', 'BITNOT', 'DOT', 'INCREMENT', 'DECREMENT', 'ARROW', 'IDIV', 'COLON',
    'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ'
]

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
    "function": "FUNCTION",
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
    "readLineSync": "READLINESYNC"
}

tokens += list(reserved.values())


# Reglas de expresiones regulares
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_MOD      = r'%'
t_EQ       = r'=='
t_NEQ      = r'!='
t_LT       = r'<'
t_LE       = r'<='
t_GT       = r'>'
t_GE       = r'>='
t_ASSIGN   = r'='
t_PLUSEQ   = r'\+='
t_MINUSEQ  = r'-='
t_TIMESEQ  = r'\*='
t_DIVEQ    = r'/='
t_MODEQ    = r'%='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI     = r';'
t_COMMA    = r','
t_AND      = r'&&'
t_OR       = r'\|\|'
t_NOT      = r'!'
t_BITNOT = r'~'
t_DOT = r'\.'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_ARROW    = r'=>'
t_IDIV     = r'~/'
t_COLON = r':'


# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Comentarios
def t_COMMENT(t):
    r'//.*'
    pass 

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    pass  # Ignora comentarios multilínea

def t_FLOAT(t):
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

lexer = lex.lex()

# Prueba rápida
if __name__ == "__main__":
    data = '''
        // Algoritmo de búsqueda con estadísticas básicas 
        class Analizador { 
        List<int> datos; 
        Map<String, dynamic> resumen; 
        Analizador(this.datos) { 
        resumen = {"min": 0, "max": 0, "promedio": 0.0, "existe": 
        false}; 
        } 
        int busquedaBinaria(int objetivo) { 
        int ini = 0, fin = datos.length - 1; 
        while (ini <= fin) { 
        int mid = (ini + fin) ~/ 2; 
        if (datos[mid] == objetivo) { 
        resumen["existe"] = true; 
        return mid; 
        } else if (datos[mid] < objetivo) { 
        ini = mid + 1; 
        } else { 
        fin = mid - 1; 
        } 
        } 
        return -1; 
        } 
        void calcularResumen() { 
        int suma = 0, min = datos[0], max = datos[0]; 
        for (int val in datos) { 
        suma += val; 
        if (val < min) min = val; 
        if (val > max) max = val; 
        } 
        resumen["min"] = min; 
        resumen["max"] = max; 
        resumen["promedio"] = suma / datos.length; 
        } 
        void mostrarResumen() { 
        print("Resumen:"); 
        print("Min: ${resumen["min"]}, Max: ${resumen["max"]}, 
        Promedio: ${resumen["promedio"]}"); 
        print("Elemento buscado existe: ${resumen["existe"]}"); 
        } 
        } 
        void main() { 
        List<int> lista = [3, 6, 8, 12, 15, 20]; 
        int objetivo = 12; 
        var analizador = Analizador(lista); 
        int pos = analizador.busquedaBinaria(objetivo); 
        analizador.calcularResumen(); 
        if (pos != -1) { 
        print("Elemento encontrado en posición $pos"); 
        } else { 
        print("Elemento no encontrado"); 
        } 
        analizador.mostrarResumen(); 
        var entrada = 2.34;
        }

    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)