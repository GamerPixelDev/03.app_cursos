from tkinter import ttk

CLARO_BG = "#F5F7FB"
OSC_BG   = "#121417"
PRIMARIO = "#3E64FF"

#--- Aplica un estilo visual coherente a toda la app (modo claro u oscuro) ---
def aplicar_estilo_global(modo="claro"):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    bg = CLARO_BG if modo == "claro" else OSC_BG
    fg = "#1a1a1a" if modo == "claro" else "#E8E8E8"
    card = "#FFFFFF" if modo == "claro" else "#1b1f24"
    # Botón básico
    style.configure(
        "TButton",
        padding=6,
        font=("Segoe UI", 10),
        background=PRIMARIO,
        foreground="white"
    )
    style.map("TButton", background=[("active", "#2f53e8")])
    # Label y Frame “card”
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("Card.TFrame", background=card)
    # Treeview
    tv_bg  = "#FFFFFF" if modo == "claro" else "#101318"
    tv_fg  = "#222"    if modo == "claro" else "#E8E8E8"
    th_bg  = "#e6e9f2" if modo == "claro" else "#20242b"
    style.configure("Treeview", background=tv_bg, foreground=tv_fg, fieldbackground=tv_bg)
    style.configure("Treeview.Heading", background=th_bg, foreground=tv_fg)
    return style, bg

def pintar_fondo_recursivo(widget, bg):
    #Aplica bg a frames/labels descendientes y fuerza redraw
    import tkinter as tk
    tipos = (tk.Frame, tk.Label, tk.LabelFrame, tk.Toplevel, tk.Canvas)
    if isinstance(widget, tipos):
        try:
            widget.configure(bg=bg)
        except Exception:
            pass
    for child in widget.winfo_children():
        pintar_fondo_recursivo(child, bg)