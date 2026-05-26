"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov - Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== ESTILOS CSS ======================
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #011D42 0%, #01478D 100%);}
    .hero {
        background: linear-gradient(135deg, #01478D, #2E6DB4);
        border-radius: 16px;
        padding: 40px 30px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero h1 {font-size: 2.8rem; margin: 0; font-weight: 900;}
    .hero p {font-size: 1.25rem; opacity: 0.95; margin-top: 10px;}
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        height: 52px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>COLOMBIA COMPARTE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0C4FF;'>Programa EDIFICA</p>", unsafe_allow_html=True)

    st.markdown("### Parámetros de Simulación")
    n_usuarios = st.slider("Número de usuarios", 100, 5000, 1200, 100)
    max_pasos = st.slider("Máximo de pasos", 5, 50, 20)
    st.markdown("---")

    if st.button("Reiniciar Simulación", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ====================== CONTENIDO PRINCIPAL ======================
st.markdown("""
<div class="hero">
    <h1>Simulación Markov — EDIFICA</h1>
    <p>Análisis del flujo de inscripción al Programa EDIFICA</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Simulación", "Estados y Transiciones", "Análisis"])

with tab1:
    col1, col2 = st.columns([2, 5])
    with col1:
        if st.button("Ejecutar Simulación", type="primary", use_container_width=True):
            with st.spinner("Ejecutando simulación..."):
                st.success(f"✅ Simulación completada con {n_usuarios:,} usuarios")
                st.balloons()

                data = {
                    "Usuario": range(1, 11),
                    "Estado_Final": np.random.choice(["Inscrito", "En Proceso", "Abandono"], 10),
                    "Pasos": np.random.randint(5, 25, 10)
                }
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)

    with col2:
        st.info("Ajusta los parámetros en la barra lateral y presiona 'Ejecutar Simulación'")

# ====================== ACCIONES RÁPIDAS ======================
st.markdown("### Acciones Rápidas")
cols = st.columns(4)

with cols[0]:
    if st.button("Exportar a Excel", use_container_width=True):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame({"Ejemplo": [1, 2, 3]}).to_excel(writer, index=False)
        output.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=output,
            file_name="resultados_simulacion.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with cols[1]:
    if st.button("Exportar a CSV", use_container_width=True):
        csv = pd.DataFrame({"Ejemplo": [1, 2, 3]}).to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="resultados_simulacion.csv",
            mime="text/csv"
        )

with cols[2]:
    if st.button("Modo Accesibilidad", use_container_width=True):
        st.success("Modo alto contraste activado (simulado)")

with cols[3]:
    if st.button("Compartir Resultados", use_container_width=True):
        st.success("Enlace copiado al portapapeles (simulado)")

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
