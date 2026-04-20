import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# ==========================================
# CONFIGURACIÓN VISUAL ESTILO "CUSTOMTKINTER"
# ==========================================
st.set_page_config(page_title="IC360 SAC | Calculadora", layout="wide")

# Inyección de CSS para clonar su interfaz de escritorio
st.markdown("""
    <style>
    /* Fondo principal estilo Dark Mode de su App */
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    
    /* Estilo de Tarjetas (Cards) como en su código original */
    .card {
        background-color: #161b22;
        border: 2px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Títulos con color azul brillante de su App */
    .title-text { color: #58a6ff; font-family: 'Arial', sans-serif; font-weight: bold; }
    
    /* Botón verde idéntico al suyo */
    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: none !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# DATA TÉCNICA - FUENTE ICG
DATA_ICG = {
    "140 kg/cm2": {"cem": 7.01, "are": 0.51, "pie": 0.64, "agu": 0.184},
    "175 kg/cm2": {"cem": 8.43, "are": 0.54, "pie": 0.55, "agu": 0.185},
    "210 kg/cm2": {"cem": 9.73, "are": 0.52, "pie": 0.53, "agu": 0.186},
    "245 kg/cm2": {"cem": 11.50, "are": 0.50, "pie": 0.51, "agu": 0.187},
    "280 kg/cm2": {"cem": 13.34, "are": 0.45, "pie": 0.51, "agu": 0.189}
}

# INTERFAZ PRINCIPAL
st.markdown('<h1 class="title-text">Calculadora de Materiales</h1>', unsafe_allow_html=True)
st.write("Desarrollado por Ing. Frank Falla Rojas | Corporación IC360 SAC")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fc = st.selectbox("Resistencia f'c:", list(DATA_ICG.keys()), index=2)
        vol = st.number_input("Volumen Neto (m3):", min_value=0.0, format="%.2f")
    with col2:
        desp = st.number_input("Desperdicio (%):", value=5)
        adi = st.selectbox("Aditivo:", ["Ninguno", "Plastificante", "Superplastificante"])

if st.button("CALCULAR"):
    if vol > 0:
        v_final = vol * (1 + (desp / 100))
        d = DATA_ICG[fc]
        
        # Cálculos
        c_bol = v_final * d['cem']
        are_m3 = v_final * d['are']; a_bal = are_m3 * 37
        pie_m3 = v_final * d['pie']; p_bal = pie_m3 * 37
        agu_m3 = v_final * d['agu']; w_bal = agu_m3 * 37
        
        # UI DE RESULTADOS (Clonando sus Tarjetas)
        st.markdown("---")
        r1, r2 = st.columns(2)
        
        with r1:
            st.markdown(f'<div class="card"><h3 style="color:#1f6aa5">CEMENTO</h3><h1>{c_bol:.2f}</h1><p>BOLSAS</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><h3 style="color:#d35400">PIEDRA CHANCADA</h3><h1>{p_bal:.1f} Baldes</h1><p>{pie_m3:.2f} m3</p></div>', unsafe_allow_html=True)
            
        with r2:
            st.markdown(f'<div class="card"><h3 style="color:#c0392b">ARENA GRUESA</h3><h1>{a_bal:.1f} Baldes</h1><p>{are_m3:.2f} m3</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><h3 style="color:#2980b9">AGUA</h3><h1>{w_bal:.1f} Baldes</h1><p>{agu_m3:.2f} m3</p></div>', unsafe_allow_html=True)

        # Botón de PDF (Estilo Reporte)
        buffer = io.BytesIO()
        # ... (lógica de PDF igual al código anterior) ...
        st.download_button("EXPORTAR REPORTE PDF", data=buffer.getvalue(), file_name="Reporte.pdf", mime="application/pdf")