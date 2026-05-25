"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · Simulación 2026
"""

import base64, os, io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# (Aquí iba el código de fondo y estilos CSS original con muchos colores y clases)

# DATOS DEL MODELO
ESTADOS = ["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9",
           "S10","S11","S12","S13","S14","S15","S16","S17","S18",
           "S19","S20","S21","S22","S23","S24","S25","S26","S27",
           "S28","S29","S30","S31","S32"]

NOMBRES = {
    "S0": "Página de inicio",
    "S1": "Sobre Nosotros",
    "S2": "Programa EDIFICA",
    # ... (todos los nombres de estados)
}

# (Aquí seguían todas las definiciones de DESCRIPCIONES, TIPOS, RECORRIDOS, 
#  funciones de simulación, matrices de transición, etc.)

# SIDEBAR ORIGINAL
with st.sidebar:
    st.markdown("COLOMBIA COMPARTE", unsafe_allow_html=True)
    st.markdown("### Parámetros")
    n_usuarios = st.slider("Usuarios a simular", 100, 5000, 1000, 100)
    # ... resto de sliders y controles originales

# CONTENIDO PRINCIPAL ORIGINAL
st.title("Dashboard de Simulación · Colombia Comparte")

# (Aquí iban las secciones con tabs, métricas, botones con emojis como ▶️ Ejecutar simulación, etc.)

# Botones originales (ahora sin emojis)
if st.button("Ejecutar simulación", use_container_width=True):
    # ... lógica original

if st.button("Generar recomendación ejecutiva", use_container_width=True):
    # ... lógica original

# (Y todo el resto del código original que tenías)
