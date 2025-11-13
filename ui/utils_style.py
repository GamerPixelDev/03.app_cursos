from tkinter import ttk

# Colores base
CLARO_BG = "#F5F7FB"
OSC_BG   = "#171A1C"
PRIMARIO = "#3E64FF"
PRIMARIO_OSCURO = "#2F53E8"

def aplicar_estilo_global(modo="claro"):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    # --- Fondos generales ---
    bg = CLARO_BG if modo == "claro" else OSC_BG
    fg = "#1d1d1d" if modo == "claro" else "#E8E8E8"
    # --- Botones ---
    style.configure(
        "TButton",
        font=("Segoe UI", 10),
        padding=6,
        background=PRIMARIO,
        foreground="white",
        relief="flat",
        borderwidth=0
    )
    style.map("TButton", background=[("active", PRIMARIO_OSCURO)])
    # --- Labels ---
    style.configure("TLabel", background=bg, foreground=fg)
    # --- Frames “card” ---
    card = "#FFFFFF" if modo == "claro" else "#1F2326"
    style.configure("Card.TFrame", background=card)
    #   🌟 TREEVIEW RESTAURADO CON CABECERA AZUL
    tv_bg  = "#FFFFFF" if modo == "claro" else "#0F1113"
    tv_fg  = "#1d1d1d" if modo == "claro" else "#E8E8E8"
    style.configure(
        "Treeview",
        background=tv_bg,
        foreground=tv_fg,
        fieldbackground=tv_bg,
        borderwidth=0,
        rowheight=22
    )
    # --- Header AZUL como antes ---
    style.configure(
        "Treeview.Heading",
        background=PRIMARIO,
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat"
    )
    style.map(
        "Treeview.Heading",
        background=[("active", PRIMARIO_OSCURO)]
    )
    return style, bg

#   REPINTAR FONDOS (sin tocar el banner azul)
def pintar_fondo_recursivo(widget, bg):
    import tkinter as tk
    tipos = (tk.Frame, tk.Label, tk.LabelFrame, tk.Toplevel, tk.Canvas)
    try:
        if widget.cget("bg") == "#3E64FF":  # Banner azul → NO TOCAR
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