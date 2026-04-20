import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

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

# Configuración de página
st.set_page_config(page_title="IC360 SAC | Calculadora", page_icon="🏗️", layout="wide")

# Estilo personalizado (CSS)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #238636; color: white; }
    .metric-card { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ CALCULADORA DE MATERIALES | CORPORACIÓN IC360 SAC")
st.caption("Desarrollado por Ing. Frank Falla Rojas")

# Layout de entrada
col1, col2 = st.columns(2)

with col1:
    fc = st.selectbox("Resistencia f'c:", list(DATA_ICG.keys()), index=2)
    vol = st.number_input("Volumen Neto (m3):", min_value=0.0, step=0.1, format="%.2f")

with col2:
    desp = st.slider("Desperdicio (%):", 0, 15, 5)
    adi = st.selectbox("Aditivo:", ["Ninguno", "Plastificante", "Superplastificante"])

if st.button("CALCULAR MATERIALES"):
    if vol > 0:
        # Lógica de cálculo
        v_final = vol * (1 + (desp / 100))
        d = DATA_ICG[fc]
        
        c_bol = v_final * d['cem']
        are_m3 = v_final * d['are']
        pie_m3 = v_final * d['pie']
        agu_m3 = v_final * d['agu']
        
        ml_b = 500 if "Super" in adi else (250 if "Plastificante" == adi else 0)
        adi_l = (c_bol * ml_b) / 1000

        # Mostrar Resultados en Columnas
        st.subheader(f"Resultados para {v_final:.3f} m3 (Inc. {desp}%)")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cemento", f"{c_bol:.2f} bol")
        m2.metric("Arena Gruesa", f"{are_m3:.2f} m3")
        m3.metric("Piedra", f"{pie_m3:.2f} m3")
        m4.metric("Agua", f"{agu_m3:.3f} m3")

        if adi_l > 0:
            st.info(f"Aditivo Requerido: {adi_l:.2f} Litros de {adi}")

        # Generación de PDF en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph(f"REPORTE DE MATERIALES - IC360 SAC", styles['Title']))
        elements.append(Paragraph(f"Ingeniero Responsable: Frank Falla Rojas", styles['Normal']))
        elements.append(Paragraph(f"Resistencia: {fc} | Volumen Total: {v_final:.3f} m3", styles['Normal']))
        
        data = [
            ['Material', 'Cantidad', 'Unidad'],
            ['Cemento', f"{c_bol:.2f}", 'Bolsas'],
            ['Arena Gruesa', f"{are_m3:.3f}", 'm3'],
            ['Piedra Chancada', f"{pie_m3:.3f}", 'm3'],
            ['Agua', f"{agu_m3:.3f}", 'm3'],
            ['Aditivo', f"{adi_l:.2f}", 'Litros']
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.navy),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        elements.append(table)
        doc.build(elements)
        
        st.download_button(
            label="📄 Descargar Reporte PDF",
            data=buffer.getvalue(),
            file_name=f"Reporte_Materiales_{fc}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Por favor, ingrese un volumen mayor a cero.")