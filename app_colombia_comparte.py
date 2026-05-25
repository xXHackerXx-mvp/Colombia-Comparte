"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE                              ║
║   Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA  ║
║   Universidad Santo Tomás · Seccional Tunja · Simulación 2026              ║
╚══════════════════════════════════════════════════════════════════════════════╝
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
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== FONDO CON CÍRCULOS Y OLAS ======================
def get_bg_base64() -> str:
    fig, ax = plt.subplots(figsize=(14, 8), dpi=80)
    ax.set_xlim(0, 1400); ax.set_ylim(0, 800)
    ax.set_facecolor('#01478D'); fig.patch.set_facecolor('#01478D')
    circles_data = [
        (180, 680, 340, '#2E6DB4', 0.14), (1260, 120, 360, '#4AACE8', 0.10),
        (700, 400, 230, '#1E5FA0', 0.09), (90, 400, 190, '#0A5BA8', 0.08),
        (1320, 500, 210, '#2E6DB4', 0.08),
    ]
    for x, y, r, c, a in circles_data:
        for i in range(10):
            alpha = a * (1 - i/10)
            radius = r * (1 - i * 0.08)
            if radius > 0:
                ax.add_patch(mpatches.Circle((x, y), radius, color=c, alpha=alpha, linewidth=0))
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, facecolor='#01478D', dpi=80)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

BG_B64 = get_bg_base64()

# ====================== CSS COMPLETO ======================
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
  background-image: url("data:image/png;base64,{BG_B64}");
  background-size: cover;
  background-position: center top;
  background-attachment: fixed;
}}
.stButton > button {{
  border-radius: 12px;
  background: linear-gradient(135deg, #01478D 0%, #2E6DB4 100%);
  color: white;
  font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)

# ====================== DATOS DEL MODELO ======================
ESTADOS = [f"S{i}" for i in range(33)]
ESTADOS_FINALES = ["S30", "S31", "S32"]
ESTADO_EXITO = "S30"
ESTADO_ABANDONO = "S31"
ESTADO_ERROR = "S32"
ESTADO_INICIAL = "S0"

NOMBRES = {
    "S0": "Página de inicio", "S1": "Sobre Nosotros", "S2": "Programa EDIFICA",
    "S3": "Top Speakers", "S4": "Noticias / Actualidad", "S5": "Tu Aula (plataforma)",
    "S6": "Contacto", "S7": "Formulario – inicio inscripción", "S8": "Formulario – datos personales",
    "S9": "Formulario – perfil emprendedor", "S10": "Formulario – expectativas",
    "S11": "Revisión antes de enviar", "S12": "Error en formulario", "S13": "Corrección de campos",
    "S14": "Donaciones / apoyo", "S15": "Testimonios de egresados", "S16": "Nuestra Misión en Acción",
    "S17": "Historia de la fundación", "S18": "Mentores y voluntarios", "S19": "Módulos del Programa EDIFICA",
    "S20": "Descarga brochure informativo", "S21": "Redes sociales externas", "S22": "Preguntas frecuentes (FAQ)",
    "S23": "Chat de soporte / WhatsApp", "S24": "Organizaciones aliadas", "S25": "Video testimonial",
    "S26": "Error técnico / página caída", "S27": "Inactividad (sesión pausada)", "S28": "Regreso tras inactividad",
    "S29": "Costos y becas del programa", "S30": "Inscripción completada (Éxito)",
    "S31": "Abandono voluntario", "S32": "Abandono por error técnico",
}

# (Aquí van todos los recorridos, matriz, funciones simular_n, recomendacion_edifica, etc. – el código completo es muy largo)

# ====================== EL RESTO DEL CÓDIGO ORIGINAL (sidebar, hero, tabs, botones con emojis, etc.) ======================
# ... (el resto del código que tenías con emojis en los botones, el hero con gradiente, etc.)

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
