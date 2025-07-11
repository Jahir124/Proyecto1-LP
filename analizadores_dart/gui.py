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
    text_errores.config(state="normal")
    text_errores.delete("1.0", tk.END)

    codigo = entrada_codigo.get("1.0", tk.END)

    # Resetear estado
    lexer.lineno = 1
    lexical_errors.clear()
    semantic_errors.clear()
    sintactic_results.clear()

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
    text_errores.config(state="disabled")

# --- GUI Principal ---
ventana = tk.Tk()
ventana.title("MiniDart Analyzer")
ventana.geometry("1100x700")
ventana.configure(bg="#181818")
ventana.minsize(900, 600)

# Estilo general
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#232323", borderwidth=0)
style.configure("TNotebook.Tab", background="#232323", foreground="#cccccc", font=("Segoe UI", 11, "bold"), padding=10)
# Pestaña activa: fondo azul, texto blanco, borde inferior
style.map("TNotebook.Tab",
    background=[("selected", "#2563eb"), ("!selected", "#232323")],
    foreground=[("selected", "white"), ("!selected", "#cccccc")],
)
# Simula borde inferior con padding extra y color
style.configure("TNotebook.Tab", borderwidth=0, focusthickness=0, padding=(10, 10, 10, 16))
style.layout("TNotebook.Tab", [
    ("Notebook.tab", {
        "sticky": "nswe",
        "children": [
            ("Notebook.padding", {
                "side": "top",
                "sticky": "nswe",
                "children": [
                    ("Notebook.label", {"side": "top", "sticky": ""})
                ]
            })
        ]
    })
])

# Título con icono unicode
icono = "\U0001F4BB"  # 💻
tk.Label(
    ventana, text=f"{icono} MiniDart Analyzer", font=("Segoe UI", 28, "bold"), bg="#181818", fg="white"
).pack(pady=(30, 5))
tk.Label(
    ventana,
    text="Herramienta interactiva para el análisis léxico, sintáctico y semántico del lenguaje Dart",
    bg="#181818", fg="#cccccc", font=("Segoe UI", 12)
).pack(pady=(0, 25))

# Área de entrada de código en "tarjeta"
frame_input_card = tk.Frame(ventana, bg="#232323", bd=0, highlightthickness=0)
frame_input_card.pack(fill="x", padx=40, pady=(0, 18))
frame_input_card.grid_propagate(False)
frame_input_card.configure(highlightbackground="#333", highlightcolor="#333", highlightthickness=1)

label_input = tk.Label(
    frame_input_card, text="Ingresa abajo tu código en Dart:", bg="#232323", fg="#cccccc", font=("Segoe UI", 11, "bold")
)
label_input.pack(anchor="w", pady=(10, 6), padx=16)
entrada_codigo = scrolledtext.ScrolledText(
    frame_input_card, height=10, bg="#181818", fg="white", insertbackground="white", font=("Consolas", 12), borderwidth=0, relief="flat"
)
entrada_codigo.pack(fill="x", padx=16, pady=(0, 16))

# Botón analizar con efecto hover
def on_enter(e):
    analizar_btn["bg"] = "#2563eb"
def on_leave(e):
    analizar_btn["bg"] = "#3c82f6"

boton_frame = tk.Frame(ventana, bg="#181818")
boton_frame.pack(fill="x", padx=40, pady=(0, 18))
analizar_btn = tk.Button(
    boton_frame, text="Analizar código", command=analizar_codigo,
    bg="#3c82f6", fg="white", font=("Segoe UI", 14, "bold"),
    activebackground="#2563eb", activeforeground="white",
    relief="flat", bd=0, padx=28, pady=12, cursor="hand2"
)
analizar_btn.pack(anchor="w")
analizar_btn.bind("<Enter>", on_enter)
analizar_btn.bind("<Leave>", on_leave)

# Panel de resultados en "tarjeta"
panel_resultados_card = tk.Frame(ventana, bg="#232323", bd=0, highlightthickness=0)
panel_resultados_card.pack(fill="both", expand=True, padx=40, pady=(0, 30))
panel_resultados_card.grid_propagate(False)
panel_resultados_card.configure(highlightbackground="#333", highlightcolor="#333", highlightthickness=1)

notebook = ttk.Notebook(panel_resultados_card)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- Pestaña: Tokens ---
frame_tokens = ttk.Frame(notebook)
notebook.add(frame_tokens, text="Tokens generados")
tree_tokens = ttk.Treeview(frame_tokens, columns=("Tipo", "Valor", "Línea"), show="headings", height=12)
tree_tokens.heading("Tipo", text="Tipo de Token")
tree_tokens.heading("Valor", text="Valor")
tree_tokens.heading("Línea", text="Línea")
tree_tokens.column("Tipo", width=180, anchor="center")
tree_tokens.column("Valor", width=500, anchor="w")
tree_tokens.column("Línea", width=80, anchor="center")
tree_tokens.pack(fill="both", expand=True, pady=16, padx=16)

# --- Pestaña: Errores ---
frame_errores = ttk.Frame(notebook)
notebook.add(frame_errores, text="Errores encontrados")
text_errores = scrolledtext.ScrolledText(
    frame_errores, bg="#181818", fg="#ff6b6b", font=("Consolas", 12), borderwidth=0, relief="flat", state="disabled"
)
text_errores.pack(fill="both", expand=True, pady=16, padx=16)

# --- Pestañas con emoji dinámico ---
def update_tab_icons():
    current = notebook.index(notebook.select())
    notebook.tab(0, text=("🔎 Tokens generados" if current == 0 else "Tokens generados"))
    notebook.tab(1, text=("⚠️ Errores encontrados" if current == 1 else "Errores encontrados"))
notebook.bind("<<NotebookTabChanged>>", lambda e: update_tab_icons())
ventana.after(100, update_tab_icons)

ventana.mainloop()
