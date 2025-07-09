import os
from datetime import datetime
from analizador_lexico import lexer
from analizador_sintactico import parser, semantic_errors, sintactic_results, symbol_table, function_table

# --- CONFIGURACIÓN DE RUTAS ---
# COLOCAR RUTAS ABSOLUTAS CORRECTAS
# Ruta donde están los archivos .dart de los algoritmos
RUTA_ALGORITMOS = "algoritmos_dart"
# Ruta donde se guardarán los logs
RUTA_LOGS = "logs"


# Crear carpeta logs si no existe
os.makedirs(RUTA_LOGS, exist_ok=True)

# Guardar logs
def guardar_log(tipo, usuario_git, errores):
    if not errores:
        return

    now = datetime.now()
    fecha = now.strftime("%d%m%Y")
    hora = now.strftime("%Hh%M")
    nombre_log = f"{tipo}-{usuario_git}-{fecha}-{hora}.txt"
    ruta = os.path.join(RUTA_LOGS, nombre_log)

    with open(ruta, "w", encoding="utf-8") as f:
        for e in errores:
            f.write(e + "\n")
    print(f"[Log guardado] {ruta}")

# Analizar archivo
def analizar_archivo(ruta_archivo):
    # Limpiar estado global
    semantic_errors.clear()
    sintactic_results.clear()
    symbol_table.clear()
    function_table.clear()

    nombre_archivo = os.path.basename(ruta_archivo)

    # Extraer usuario desde el nombre del archivo: algoritmo_usuario.dart
    nombre_base = os.path.splitext(nombre_archivo)[0]
    partes = nombre_base.split('_')
    if len(partes) < 2:
        print(f"[Error] El archivo '{nombre_archivo}' no cumple el formato 'algoritmo_usuario.dart'")
        return
    usuario_git = partes[1]

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print(f"\n📄 Analizando: {nombre_archivo} (usuario: {usuario_git})")

    # Léxico
    lexer.input(codigo)
    lexico_resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        lexico_resultado.append(f"{tok.type} ({tok.value}) -> línea {tok.lineno}")
    guardar_log("lexico", usuario_git, lexico_resultado)

    # Sintáctico y semántico
    parser.parse(codigo)
    guardar_log("sintactico", usuario_git, sintactic_results)
    guardar_log("semantico", usuario_git, semantic_errors)

# Ejecutar análisis masivo
def ejecutar_analisis_masivo():
    archivos = [f for f in os.listdir(RUTA_ALGORITMOS) if f.endswith(".dart")]
    for archivo in archivos:
        ruta = os.path.join(RUTA_ALGORITMOS, archivo)
        analizar_archivo(ruta)

# Entrada principal
if __name__ == "__main__":
    ejecutar_analisis_masivo()
