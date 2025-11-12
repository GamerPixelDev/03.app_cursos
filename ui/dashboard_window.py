import tkinter as tk
from tkinter import ttk
from datetime import datetime
from models import alumnos, cursos, matriculas
from ui.utils_style import aplicar_estilo_global
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class DashboardWindow(tk.Frame):
    def __init__(self, parent, modo="claro"):
        super().__init__(parent)
        self.modo = modo
        self.style, self.bg_color = aplicar_estilo_global(modo)
        self.configure(bg=self.bg_color)
        self.pack(fill="both", expand=True)
        # === Título principal ===
        lbl_titulo = tk.Label(
            self,
            text="📊 Panel de Control - Gestor de Cursos",
            font=("Segoe UI", 16, "bold"),
            fg="#3E64FF",
            bg=self.bg_color
        )
        lbl_titulo.pack(pady=15)
        # === Frame superior: resumen ===
        frame_resumen = tk.Frame(self, bg=self.bg_color)
        frame_resumen.pack(fill="x", pady=10)
        self.cards = {}
        metrics = [
            ("🧑‍🎓 Alumnos", alumnos.obtener_alumnos, "#4CAF50"),
            ("📚 Cursos", cursos.obtener_cursos, "#2196F3"),
            ("📝 Matrículas", matriculas.obtener_matriculas, "#FF9800"),
            ("⚡ Cursos activos", self.obtener_cursos_activos, "#9C27B0")
        ]
        for i, (titulo, funcion, color) in enumerate(metrics):
            frame = tk.Frame(frame_resumen, bg=color, bd=2, relief="ridge")
            frame.grid(row=0, column=i, padx=10, ipadx=20, ipady=15, sticky="nsew")
            label_titulo = tk.Label(frame, text=titulo, font=("Segoe UI", 11, "bold"), bg=color, fg="white")
            label_titulo.pack()
            valor = tk.Label(frame, text="0", font=("Segoe UI", 18, "bold"), bg=color, fg="white")
            valor.pack(pady=5)
            self.cards[titulo] = (valor, funcion)
        frame_resumen.grid_columnconfigure(tuple(range(4)), weight=1)
        # === Frame medio: gráficos ===
        frame_graficos = tk.Frame(self, bg=self.bg_color)
        frame_graficos.pack(fill="both", expand=True, padx=20, pady=10)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(9, 3))
        self.fig.patch.set_facecolor(self.bg_color)
        self.ax1.set_facecolor(self.bg_color)
        self.ax2.set_facecolor(self.bg_color)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graficos)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        # === Frame inferior: accesos rápidos ===
        frame_botones = tk.Frame(self, bg=self.bg_color)
        frame_botones.pack(pady=10)
        botones = [
            ("👤 Gestión de Alumnos", lambda: parent.abrir_ventana("alumnos")),
            ("📘 Gestión de Cursos", lambda: parent.abrir_ventana("cursos")),
            ("🗂️ Gestión de Matrículas", lambda: parent.abrir_ventana("matriculas"))
        ]
        for i, (texto, comando) in enumerate(botones):
            ttk.Button(frame_botones, text=texto, command=comando).grid(row=0, column=i, padx=10)
        # === Cargar datos al iniciar ===
        self.actualizar_datos()

    # === Función auxiliar para contar cursos activos ===
    def obtener_cursos_activos(self):
        hoy = datetime.now().date()
        cursos_lista = cursos.obtener_cursos()
        activos = [c for c in cursos_lista if c[2] <= str(hoy) <= c[3]]
        return activos

    # === Actualizar datos y gráficos ===
    def actualizar_datos(self):
        # Actualizar tarjetas
        for titulo, (label, funcion) in self.cards.items():
            try:
                datos = funcion()
                if isinstance(datos, list):
                    valor = len(datos)
                else:
                    valor = len(datos.fetchall())
                label.config(text=str(valor))
            except Exception:
                label.config(text="-")
        # Actualizar gráfico 1: Matrículas por mes
        datos = matriculas.obtener_matriculas()
        conteo_meses = {}
        for m in datos:
            try:
                fecha = datetime.strptime(m[4], "%Y-%m-%d")
                mes = fecha.strftime("%b")
                conteo_meses[mes] = conteo_meses.get(mes, 0) + 1
            except Exception:
                pass
        self.ax1.clear()
        self.ax1.bar(conteo_meses.keys(), conteo_meses.values(), color="#3E64FF")
        self.ax1.set_title("Matrículas por mes")
        self.ax1.tick_params(axis='x', rotation=45)
        # Actualizar gráfico 2: Modalidad de cursos
        datos_cursos = cursos.obtener_cursos()
        modalidades = {}
        for c in datos_cursos:
            modalidad = c[5] if len(c) > 5 else "Desconocida"
            modalidades[modalidad] = modalidades.get(modalidad, 0) + 1
        self.ax2.clear()
        if modalidades:
            self.ax2.pie(modalidades.values(), labels=modalidades.keys(), autopct="%1.0f%%", startangle=90)
        self.ax2.set_title("Modalidad de cursos")
        self.canvas.draw_idle()
