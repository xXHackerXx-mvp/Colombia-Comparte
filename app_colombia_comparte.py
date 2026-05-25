"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · 2026
"""

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

# ====================== ESTILOS CSS (Diseño profesional) ======================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #011D42 0%, #01478D 100%);
    }
    .hero {
        background: linear-gradient(135deg, #01478D, #2E6DB4);
        border-radius: 16px;
        padding: 40px 30px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 900;
    }
    .hero p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-top: 10px;
    }
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        height: 52px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(74,172,232,0.4);
    }
    .sidebar .css-1d391kg {
        background-color: #012A5E;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: white; margin: 0;">COLOMBIA COMPARTE</h2>
            <p style="color: #A0C4FF; font-size: 0.95rem;">Programa EDIFICA</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Parámetros de Simulación")
    
    n_usuarios = st.slider("Número de usuarios", 100, 5000, 1200, 100)
    max_pasos = st.slider("Máximo de pasos", 5, 50, 20)
    
    estado_inicial = st.selectbox("Estado inicial", ["S0"])
    
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Simulación", 
    "Estados y Transiciones", 
    "Análisis", 
    "Herramientas Avanzadas"
])

with tab1:
    col1, col2 = st.columns([2, 5])
    with col1:
        if st.button("🚀 Ejecutar Simulación", type="primary", use_container_width=True):
            st.success(f"Simulación completada con {n_usuarios:,} usuarios")
            # ← Aquí pega tu lógica completa de simulación Markov

    with col2:
        st.info("Ajusta los parámetros desde la barra lateral izquierda")

# Acciones rápidas
st.markdown("### Acciones Rápidas")
cols = st.columns(4)

with cols[0]:
    st.button("Exportar a Excel", use_container_width=True)

with cols[1]:
    st.button("Exportar a CSV", use_container_width=True)

with cols[2]:
    st.button("Modo Accesibilidad", use_container_width=True)

with cols[3]:
    st.button("Compartir Resultados", use_container_width=True)

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
