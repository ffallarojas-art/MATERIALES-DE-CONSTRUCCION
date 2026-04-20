import customtkinter as ctk
from tkinter import messagebox, filedialog
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ==========================================
# DATA TÉCNICA - FUENTE ICG
# ==========================================
DATA_ICG = {
    "140 kg/cm2": {"cem": 7.01, "are": 0.51, "pie": 0.64, "agu": 0.184},
    "175 kg/cm2": {"cem": 8.43, "are": 0.54, "pie": 0.55, "agu": 0.185},
    "210 kg/cm2": {"cem": 9.73, "are": 0.52, "pie": 0.53, "agu": 0.186},
    "245 kg/cm2": {"cem": 11.50, "are": 0.50, "pie": 0.51, "agu": 0.187},
    "280 kg/cm2": {"cem": 13.34, "are": 0.45, "pie": 0.51, "agu": 0.189}
}

class ConcreteAppV8(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CALCULADORA DE MATERIALES | CORPORACIÓN IC360 SAC")
        self.geometry("1100x850")
        ctk.set_appearance_mode("Dark")
        
        self.main_container = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.show_home()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_container()
        home_frame = ctk.CTkFrame(self.main_container, fg_color="#161b22", corner_radius=15, border_width=2, border_color="#30363d")
        home_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)

        ctk.CTkLabel(home_frame, text="Calculadora de Materiales", font=("Orbitron", 28, "bold"), text_color="#58a6ff").pack(pady=(40, 10))
        ctk.CTkLabel(home_frame, text="Desarrollado por Ing. Frank Falla Rojas", font=("Arial", 14), text_color="#8b949e").pack(pady=(0, 30))

        grid_f = ctk.CTkFrame(home_frame, fg_color="transparent")
        grid_f.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(grid_f, text="Resistencia f'c:", font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_fc = ctk.CTkComboBox(grid_f, values=list(DATA_ICG.keys()), width=250, height=40)
        self.combo_fc.grid(row=1, column=0, padx=(0, 20), pady=(0, 20))
        self.combo_fc.set("210 kg/cm2")

        ctk.CTkLabel(grid_f, text="Volumen Neto (m3):", font=("Arial", 13, "bold")).grid(row=0, column=1, sticky="w", pady=5)
        self.ent_vol = ctk.CTkEntry(grid_f, placeholder_text="Ej: 15.00", width=250, height=40)
        self.ent_vol.grid(row=1, column=1, pady=(0, 20))

        ctk.CTkLabel(grid_f, text="Desperdicio (%):", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.ent_desp = ctk.CTkEntry(grid_f, width=250, height=40)
        self.ent_desp.insert(0, "5")
        self.ent_desp.grid(row=3, column=0, padx=(0, 20), pady=(0, 20))

        ctk.CTkLabel(grid_f, text="Aditivo:", font=("Arial", 13, "bold")).grid(row=2, column=1, sticky="w", pady=5)
        self.combo_adi = ctk.CTkComboBox(grid_f, values=["Ninguno", "Plastificante", "Superplastificante"], width=250, height=40)
        self.combo_adi.grid(row=3, column=1, pady=(0, 20))

        ctk.CTkButton(home_frame, text="CALCULAR", fg_color="#238636", hover_color="#2ea043", 
                      height=55, font=("Arial", 16, "bold"), command=self.procesar_y_mostrar).pack(pady=40, padx=60, fill="x")

    def procesar_y_mostrar(self):
        try:
            fc = self.combo_fc.get()
            vol = float(self.ent_vol.get())
            desp = float(self.ent_desp.get()) / 100
            v_final = vol * (1 + desp)
            d = DATA_ICG[fc]

            # Cálculos de materiales
            c_bol = v_final * d['cem']
            
            # Agregados y Agua: Baldes y M3
            are_m3 = v_final * d['are']
            a_bal = are_m3 * 37
            
            pie_m3 = v_final * d['pie']
            p_bal = pie_m3 * 37
            
            agu_m3 = v_final * d['agu']
            w_bal = agu_m3 * 37
            
            tipo_adi = self.combo_adi.get()
            ml_b = 500 if "Super" in tipo_adi else (250 if "Plastificante" == tipo_adi else 0)
            adi_l = (c_bol * ml_b) / 1000

            self.data_reporte = {
                "fc": fc, "vol": vol, "v_final": v_final, "desp": desp*100,
                "cem": c_bol, 
                "are_b": a_bal, "are_m3": are_m3,
                "pie_b": p_bal, "pie_m3": pie_m3,
                "agu_b": w_bal, "agu_m3": agu_m3,
                "adi": adi_l, "adi_t": tipo_adi
            }

            self.clear_container()
            self.build_results_ui()

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

    def build_results_ui(self):
        header = ctk.CTkFrame(self.main_container, fg_color="#161b22", height=100, corner_radius=0)
        header.pack(fill="x", side="top")
        
        ctk.CTkLabel(header, text=f"RESULTADOS: f'c {self.data_reporte['fc']}", font=("Arial", 24, "bold"), text_color="#00d4ff").pack(side="left", padx=40, pady=20)
        
        btn_home = ctk.CTkButton(header, text="NUEVO CÁLCULO", fg_color="#30363d", width=150, command=self.show_home)
        btn_home.pack(side="right", padx=40, pady=20)

        # Contenedor inferior para botones de acción (Movido hacia arriba del fondo)
        footer = ctk.CTkFrame(self.main_container, fg_color="#161b22", height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")

        ctk.CTkButton(footer, text="EXPORTAR REPORTE PDF", fg_color="#d73a49", height=40, width=250, 
                      font=("Arial", 13, "bold"), command=self.exportar_pdf).pack(pady=15)

        scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=10)

        cards_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        cards_container.pack(fill="x")
        cards_container.columnconfigure((0, 1), weight=1)

        # Renderizado de Tarjetas con unidades duales
        self.create_card(cards_container, "CEMENTO", f"{self.data_reporte['cem']:.2f}", "BOLSAS", "#1f6aa5", 0, 0)
        
        # Arena con m3
        self.create_card(cards_container, "ARENA GRUESA", 
                         f"{self.data_reporte['are_b']:.1f} Baldes\n{self.data_reporte['are_m3']:.2f} m3", 
                         "CANTIDAD TOTAL", "#c0392b", 0, 1)
        
        # Piedra con m3
        self.create_card(cards_container, "PIEDRA CHANCADA", 
                         f"{self.data_reporte['pie_b']:.1f} Baldes\n{self.data_reporte['pie_m3']:.2f} m3", 
                         "CANTIDAD TOTAL", "#d35400", 1, 0)
        
        # Agua con m3
        self.create_card(cards_container, "AGUA", 
                         f"{self.data_reporte['agu_b']:.1f} Baldes\n{self.data_reporte['agu_m3']:.2f} m3", 
                         "CANTIDAD TOTAL", "#2980b9", 1, 1)
        
        if self.data_reporte['adi'] > 0:
            self.create_card(cards_container, f"ADITIVO ({self.data_reporte['adi_t']})", f"{self.data_reporte['adi']:.2f}", "LITROS", "#27ae60", 2, 0, columnspan=2)

    def create_card(self, master, title, value, unit, color, row, col, columnspan=1):
        card = ctk.CTkFrame(master, fg_color="#1c2128", border_width=2, border_color=color, corner_radius=12)
        card.grid(row=row, column=col, columnspan=columnspan, padx=15, pady=15, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=("Arial", 13, "bold"), text_color=color).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=value, font=("Orbitron", 28, "bold"), text_color="#f0f6fc", justify="center").pack()
        ctk.CTkLabel(card, text=unit, font=("Arial", 11), text_color="#8b949e").pack(pady=(5, 15))

    def exportar_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not path: return
        
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        header_style = ParagraphStyle(name='H', fontSize=18, textColor=colors.HexColor("#1a1c2e"), alignment=1, spaceAfter=20)
        content.append(Paragraph("REPORTE DE CANTIDAD DE MATERIALES", header_style))
        content.append(Paragraph(f"<b>Responsable:</b> Ing. Frank Falla Rojas", styles['Normal']))
        content.append(Paragraph(f"<b>Resistencia:</b> {self.data_reporte['fc']} | <b>Volumen:</b> {self.data_reporte['v_final']:.3f} m3", styles['Normal']))
        content.append(Spacer(1, 20))

        data = [
            ['MATERIAL', 'BALDES', 'M3 / UNID.'],
            ['Cemento', '-', f"{self.data_reporte['cem']:.2f} Bolsas"],
            ['Arena Gruesa', f"{self.data_reporte['are_b']:.2f}", f"{self.data_reporte['are_m3']:.3f} m3"],
            ['Piedra Chancada', f"{self.data_reporte['pie_b']:.2f}", f"{self.data_reporte['pie_m3']:.3f} m3"],
            ['Agua', f"{self.data_reporte['agu_b']:.2f}", f"{self.data_reporte['agu_m3']:.3f} m3"],
            ['Aditivo', '-', f"{self.data_reporte['adi']:.2f} Litros"]
        ]

        t = Table(data, colWidths=[150, 150, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a1c2e")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        content.append(t)
        doc.build(content)
        messagebox.showinfo("Éxito", "Reporte generado correctamente.")

if __name__ == "__main__":
    app = ConcreteAppV8()
    app.mainloop()