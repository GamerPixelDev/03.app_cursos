import tkinter.font as tkfont

#--- Ajusta automáticamente el ancho de las columnas de un Treeview al texto más largo ---
def auto_ajustar_columnas(tree):
    tree.update_idletasks()
    font = tkfont.Font()
    for col in tree["columns"]:
        header_text = tree.heading(col)["text"]
        max_width = font.measure(header_text)
        for item_id in tree.get_children():
            text = str(tree.set(item_id, col))
            w = font.measure(text)
            if w > max_width:
                max_width = w
        # Añade un margen visual y desactiva stretch
        tree.column(col, width=max_width + 25, stretch=False)
    tree.update_idletasks()

#--- Ajusta el ancho de la ventana según el contenido de un Treeview ---
def ajustar_tamano_ventana(tree, ventana, margen_extra=40, alto_fijo=500):
    try:
        ventana.update_idletasks()  # asegura que las columnas están renderizadas
        total_ancho = 0
        for col in tree["columns"]:
            info = tree.column(col)
            total_ancho += info["width"]
        nuevo_ancho = total_ancho + margen_extra
        ancho_actual = ventana.winfo_width()
        # solo cambia si hay una diferencia significativa
        if abs(nuevo_ancho - ancho_actual) > 30:
            ventana.geometry(f"{nuevo_ancho}x{alto_fijo}")
    except Exception as e:
        print(f"[ajustar_tamano_ventana] Error ajustando ventana: {e}")

    #=== Funcion usada para comprobar que anchos se dibujaban al mostrar alumnos ===
    def ajustar_columnas_debug(self):
        """Versión de depuración: muestra por consola las medidas."""
        self.update_idletasks()
        font = tkfont.Font()
        print("=== Ajuste de columnas ===")
        for col in self.tree["columns"]:
            header_text = self.tree.heading(col)["text"]
            max_width = font.measure(header_text)
            print(f"Encabezado {header_text}: {max_width}px")
            for item_id in self.tree.get_children():
                text = str(self.tree.set(item_id, col))
                w = font.measure(text)
                if w > max_width:
                    max_width = w
            print(f"  -> Máx. {col}: {max_width}px")
            self.tree.column(col, width=max_width + 25)
        print("=== Fin de ajuste ===")

