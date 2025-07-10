import tkinter as tk
from tkinter import ttk, scrolledtext
from analizador_lexico import lexer
from analizador_sintactico import parser, semantic_errors, sintactic_results, symbol_table, function_table

# Captura de errores léxicos para visualización
lexical_errors = []

# Redefinición del manejador de errores léxicos
def custom_lex_error(t):
    error_msg = f"[Error Léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'"
    lexical_errors.append(error_msg)
    lexer.skip(1)

lexer.errorfunc = custom_lex_error

def analizar_codigo():
    # Limpiar salidas anteriores
    for i in tree_tokens.get_children():
        tree_tokens.delete(i)
    text_errores.delete("1.0", tk.END)
    text_arbol.delete("1.0", tk.END)
    for i in tree_vars.get_children():
        tree_vars.delete(i)

    codigo = entrada_codigo.get("1.0", tk.END)

    # Resetear estado
    lexer.lineno = 1
    lexical_errors.clear()
    semantic_errors.clear()
    sintactic_results.clear()
    symbol_table.clear()
    function_table.clear()

    # Análisis léxico
    lexer.input(codigo)
    while True:
        tok = lexer.token()
        if not tok:
            break
        tree_tokens.insert("", "end", values=(tok.type, tok.value, tok.lineno))

    # Análisis sintáctico y semántico
    parser.parse(codigo)

    # Mostrar errores
    if lexical_errors or sintactic_results or semantic_errors:
        for err in lexical_errors + sintactic_results + semantic_errors:
            text_errores.insert(tk.END, err + "\n")
    else:
        text_errores.insert(tk.END, "✅ Análisis exitoso. No se encontraron errores.")

    # Resultado árbol sintáctico (texto por ahora)
    text_arbol.insert(tk.END, "🌳 Árbol de sintaxis generado exitosamente (modo textual).\n")
    text_arbol.insert(tk.END, "⚠️ Visualización gráfica no implementada (opcional).\n")
    actualizar_variables()
    print(symbol_table)

# --- GUI Principal ---
ventana = tk.Tk()
ventana.title("MiniDart Analyzer")
ventana.geometry("1000x720")
ventana.configure(bg="#1e1e1e")

# Título
tk.Label(ventana, text="MiniDart Analyzer", font=("Helvetica", 20, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)
tk.Label(ventana, text="Herramienta interactiva para el análisis léxico, sintáctico y semántico del lenguaje Dart", bg="#1e1e1e", fg="white").pack()

# Área de código
tk.Label(ventana, text="Ingresa abajo tu código en Dart:", bg="#1e1e1e", fg="white").pack(anchor="w", padx=10, pady=(15, 5))
entrada_codigo = scrolledtext.ScrolledText(ventana, height=10, bg="#2b2b2b", fg="white", insertbackground="white")
entrada_codigo.pack(fill="x", padx=10)

# Botón analizar
tk.Button(ventana, text="Analizar Código", command=analizar_codigo, bg="#3c3c3c", fg="white").pack(pady=10)

# Panel de resultados con pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- Pestaña: Tokens ---
frame_tokens = ttk.Frame(notebook)
notebook.add(frame_tokens, text="Tokens Generados")

tree_tokens = ttk.Treeview(frame_tokens, columns=("Tipo", "Valor", "Línea"), show="headings")
tree_tokens.heading("Tipo", text="Tipo de Token")
tree_tokens.heading("Valor", text="Valor")
tree_tokens.heading("Línea", text="Línea")
tree_tokens.column("Tipo", width=200)
tree_tokens.column("Valor", width=400)
tree_tokens.column("Línea", width=100)
tree_tokens.pack(fill="both", expand=True)

# Cambiar color de fondo y letras para tokens
style = ttk.Style()
style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
style.map("Treeview", background=[("selected", "#444444")], foreground=[("selected", "white")])

# --- Pestaña: Errores ---
frame_errores = ttk.Frame(notebook)
notebook.add(frame_errores, text="Errores")

text_errores = scrolledtext.ScrolledText(frame_errores, bg="#2b2b2b", fg="white")
text_errores.pack(fill="both", expand=True)

# --- Pestaña: Árbol de Sintaxis ---
frame_arbol = ttk.Frame(notebook)
notebook.add(frame_arbol, text="Árbol de Sintaxis")

text_arbol = scrolledtext.ScrolledText(frame_arbol, bg="#2b2b2b", fg="white")
text_arbol.pack(fill="both", expand=True)

# --- Pestaña: Variables ---
frame_vars = ttk.Frame(notebook)
notebook.add(frame_vars, text="Variables")

tree_vars = ttk.Treeview(frame_vars, columns=("Nombre", "Tipo"), show="headings")
tree_vars.heading("Nombre", text="Nombre")
tree_vars.heading("Tipo", text="Tipo")
tree_vars.column("Nombre", width=200)
tree_vars.column("Tipo", width=200)
tree_vars.pack(fill="both", expand=True)

# Cambiar color de fondo y letras para variables
style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
style.map("Treeview", background=[("selected", "#444444")], foreground=[("selected", "white")])

def actualizar_variables():
    # Limpiar tabla
    for i in tree_vars.get_children():
        tree_vars.delete(i)
    # Insertar variables actuales
    for nombre, tipo in symbol_table.items():
        tree_vars.insert("", "end", values=(nombre, tipo))

ventana.mainloop()
