from tkinter import ttk

#--- Aplica un estilo visual coherente a toda la app (modo claro u oscuro) ---
def aplicar_estilo_global(modo="claro"):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    # --- Paleta de colores según modo ---
    if modo.lower() == "oscuro":
        fondo = "#1E1E1E"          # fondo general
        fondo_widget = "#2A2A2A"   # fondo de campos/frames
        texto = "#FFFFFF"          # texto principal
        texto_invertido = "#000000"
        principal = "#4A90E2"      # azul acento
        seleccion = "#4A90E2"
    else:  # modo claro (por defecto)
        fondo = "#F5F6FA"
        fondo_widget = "#FFFFFF"
        texto = "#222222"
        texto_invertido = "#FFFFFF"
        principal = "#3E64FF"
        seleccion = "#4A90E2"
    # --- Estilo de Treeview (tablas) ---
    style.configure(
        "Treeview",
        background=fondo_widget,
        fieldbackground=fondo_widget,
        foreground=texto,
        rowheight=24,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Treeview.Heading",
        background=principal,
        foreground=texto_invertido,
        font=("Segoe UI", 10, "bold")
    )
    style.map(
        "Treeview",
        background=[("selected", seleccion)]
    )
    # --- Botones ---
    style.configure(
        "TButton",
        font=("Segoe UI", 10),
        padding=6,
        background=principal,
        foreground=texto_invertido
    )
    style.map(
        "TButton",
        background=[("active", seleccion)]
    )
    # --- Labels (sin fondo marrón) ---
    style.configure("TLabel", font=("Segoe UI", 10), foreground=texto, background=fondo)
    # --- Frames y fondo general ---
    style.configure("TFrame", background=fondo)
    return style, fondo
