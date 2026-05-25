"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · 2026
"""

import base64
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== ESTILOS CSS ======================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #011D42 0%, #01478D 100%);
    }
    .hero {
        background: linear-gradient(135deg, rgba(1,71,141,0.95), rgba(46,109,180,0.90));
        border-radius: 20px;
        padding: 35px 40px;
        margin-bottom: 25px;
        text-align: center;
        color: white;
    }
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>COLOMBIA COMPARTE</h2>", unsafe_allow_html=True)
    
    st.markdown("### Parametros de Simulacion")
    
    n_usuarios = st.slider("Numero de usuarios", 100, 5000, 1000, 100)
    max_pasos = st.slider("Maximo de pasos", 5, 50, 25)
    
    estado_inicial = st.selectbox("Estado inicial", ["S0"], index=0)
    
    st.markdown("---")
    if st.button("Reiniciar Simulacion", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ====================== CONTENIDO PRINCIPAL ======================
st.markdown("""
<div class="hero">
    <h1 style="margin:0; font-size:2.8rem;">Simulacion Markov — EDIFICA</h1>
    <p style="margin:8px 0 0 0; opacity:0.9; font-size:1.1rem;">
        Analisis del flujo de inscripcion al Programa EDIFICA
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Simulacion", 
    "Estados y Transiciones", 
    "Analisis", 
    "Herramientas Avanzadas"
])

with tab1:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Ejecutar Simulacion", type="primary", use_container_width=True):
            st.success(f"Simulacion de {n_usuarios:,} usuarios completada")
            # Aquí va tu lógica original de simulación

    with col2:
        st.info("Ajusta los parametros en la barra lateral")

st.markdown("### Acciones Rapidas")
cols = st.columns(4)

with cols[0]:
    st.button("Exportar a Excel", use_container_width=True)

with cols[1]:
    st.button("Exportar a CSV", use_container_width=True)

with cols[2]:
    st.button("Modo Accesibilidad", use_container_width=True)

with cols[3]:
    st.button("Compartir Resultados", use_container_width=True)

st.caption("Dashboard Colombia Comparte • 2026")
