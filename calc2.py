import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# ==========================================
# CONFIGURACIÓN TÉCNICA Y ESTILO
# ==========================================
st.set_page_config(page_title="IC360 SAC | Calculadora", layout="wide")

# Inicializar el estado de la aplicación si no existe
if 'calculado' not in st.session_state:
    st.session_state.calculado = False
if 'data_reporte' not in st.session_state:
    st.session_state.data_reporte = {}

def reset_calculo():
    st.session_state.calculado = False
    st.session_state.data_reporte = {}

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    .card {
        background-color: #161b22;
        border: 2px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .title-text { color: #58a6ff; font-weight: bold; }
    /* Botón Calcular (Verde) */
    div.stButton > button:first-child {
        background-color: #238636 !important;
        color: white !important;
        font-weight: bold !important;
        height: 3.5em !important;
        width: 100%;
    }
    /* Botón Nuevo Cálculo (Gris Estilo GitHub) */
    .btn-nuevo > div > button {
        background-color: #30363d !important;
        color: #c9d1d9 !important;
        border: 1px solid #8b949e !important;
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

# --- PANTALLA PRINCIPAL: FORMULARIO ---
if not st.session_state.calculado:
    st.markdown('<h1 class="title-text">Calculadora de Materiales</h1>', unsafe_allow_html=True)
    st.write("Ing. Frank Falla Rojas | Corporación IC360 SAC")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fc = st.selectbox("Resistencia f'c:", list(DATA_ICG.keys()), index=2)
            vol = st.number_input("Volumen Neto (m3):", min_value=0.0, step=0.1, format="%.2f")
        with col2:
            desp = st.number_input("Desperdicio (%):", value=5)
            adi = st.selectbox("Aditivo:", ["Ninguno", "Plastificante", "Superplastificante"])

    if st.button("CALCULAR"):
        if vol > 0:
            v_final = vol * (1 + (desp / 100))
            d = DATA_ICG[fc]
            c_bol = v_final * d['cem']
            are_m3 = v_final * d['are']; a_bal = are_m3 * 37
            pie_m3 = v_final * d['pie']; p_bal = pie_m3 * 37
            agu_m3 = v_final * d['agu']; w_bal = agu_m3 * 37
            
            # Guardar en estado de sesión
            st.session_state.data_reporte = {
                "fc": fc, "v_final": v_final, "cem": c_bol,
                "are_b": a_bal, "are_m": are_m3, "pie_b": p_bal, "pie_m": pie_m3,
                "agu_b": w_bal, "agu_m": agu_m3, "adi_t": adi
            }
            st.session_state.calculado = True
            st.rerun()
        else:
            st.warning("Ingrese un volumen válido.")

# --- PANTALLA DE RESULTADOS (OCULTA EL FORMULARIO) ---
else:
    # Encabezado de resultados con botón de regreso
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown(f'<h1 class="title-text">Resultados f\'c {st.session_state.data_reporte["fc"]}</h1>', unsafe_allow_html=True)
    with h_col2:
        st.markdown('<div class="btn-nuevo">', unsafe_allow_html=True)
        if st.button("NUEVO CÁLCULO"):
            reset_calculo()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"Volumen Final con desperdicio: **{st.session_state.data_reporte['v_final']:.3f} m3**")

    # Render de tarjetas
    res = st.session_state.data_reporte
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f'<div class="card"><h3 style="color:#1f6aa5">CEMENTO</h3><h1>{res["cem"]:.2f}</h1><p>BOLSAS</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><h3 style="color:#d35400">PIEDRA CHANCADA</h3><h1>{res["pie_b"]:.1f} Baldes</h1><p>{res["pie_m"]:.2f} m3</p></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="card"><h3 style="color:#c0392b">ARENA GRUESA</h3><h1>{res["are_b"]:.1f} Baldes</h1><p>{res["are_m"]:.2f} m3</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><h3 style="color:#2980b9">AGUA</h3><h1>{res["agu_b"]:.1f} Baldes</h1><p>{res["agu_m"]:.2f} m3</p></div>', unsafe_allow_html=True)

    # Lógica de Exportación PDF (Simplificada para el ejemplo)
    st.markdown("---")
    buffer = io.BytesIO()
    # (Aquí va su lógica de ReportLab que ya tenemos guardada)
    # Por brevedad, el botón de descarga se mantiene:
    st.download_button("EXPORTAR REPORTE PDF", data=b"Contenido PDF", file_name="Reporte_IC360.pdf", mime="application/pdf")
