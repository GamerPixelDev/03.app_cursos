from tkinter import ttk

def aplicar_estilo():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Treeview",
                    background="#fdfdfd",
                    foreground="#222",
                    rowheight=24,
                    fieldbackground="#fdfdfd",
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
                    background="#3E64FF",
                    foreground="white",
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", "#4A90E2")])
    style.configure("TButton",
                    font=("Segoe UI", 10),
                    padding=6)
    style.map("TButton", relief=[("pressed", "sunken")])
