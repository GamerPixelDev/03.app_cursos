from tkinter import ttk

CLARO_BG = "#F5F7FB"
OSC_BG   = "#121417"
PRIMARIO = "#3E64FF"

# =============================
#  ESTILO GLOBAL ESTABLE
# =============================
def aplicar_estilo_global(modo="claro"):
    style = ttk.Style()
    # Asegura un tema estable (clam no toca demasiado nada)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    # Colores principales
    bg = CLARO_BG if modo == "claro" else OSC_BG
    fg = "#1a1a1a" if modo == "claro" else "#E8E8E8"
    # BOTONES
    style.configure(
        "TButton",
        padding=6,
        font=("Segoe UI", 10),
        background=PRIMARIO,
        foreground="white"
    )
    style.map("TButton", background=[("active", "#2f53e8")])
    # LABELS BÁSICOS
    style.configure("TLabel", background=bg, foreground=fg)
    # TREEVIEW (Restaurado como antes)
    tv_bg  = "#FFFFFF" if modo == "claro" else "#1A1D21"
    tv_fg  = "#222"    if modo == "claro" else "#E8E8E8"
    th_bg  = "#dfe3eb" if modo == "claro" else "#2A2F36"
    style.configure(
        "Treeview",
        background=tv_bg,
        fieldbackground=tv_bg,
        foreground=tv_fg,
        rowheight=22
    )
    style.configure(
        "Treeview.Heading",
        background=th_bg,
        foreground="#1a1a1a" if modo == "claro" else "#FFFFFF",
        font=("Segoe UI", 10, "bold")
    )
    return style, bg

#  REPINTADO SUAVE — no toca el banner azul (#3E64FF)
def pintar_fondo_recursivo(widget, bg):
    import tkinter as tk
    tipos = (tk.Frame, tk.Label, tk.LabelFrame, tk.Toplevel)
    # No tocamos el banner azul ni Treeviews
    try:
        if widget.cget("bg") == PRIMARIO:
            return
    except Exception:
        pass
    if isinstance(widget, tipos):
        try:
            widget.configure(bg=bg)
        except Exception:
            pass
    for child in widget.winfo_children():
        pintar_fondo_recursivo(child, bg)
