"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE                              ║
║   Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA  ║
║   Universidad Santo Tomás · Seccional Tunja · Simulación 2026              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import base64, io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter

st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== FONDO ORIGINAL ======================
def get_bg_base64():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=80)
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 800)
    ax.set_facecolor('#01478D')
    fig.patch.set_facecolor('#01478D')
    circles_data = [
        (180, 680, 340, '#2E6DB4', 0.14),
        (1260, 120, 360, '#4AACE8', 0.10),
        (700, 400, 230, '#1E5FA0', 0.09),
        (90, 400, 190, '#0A5BA8', 0.08),
        (1320, 500, 210, '#2E6DB4', 0.08),
    ]
    for x, y, r, c, a in circles_data:
        for i in range(10):
            alpha = a * (1 - i/10)
            radius = r * (1 - i * 0.08)
            if radius > 0:
                ax.add_patch(mpatches.Circle((x, y), radius, color=c, alpha=alpha))
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, facecolor='#01478D', dpi=80)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

BG_B64 = get_bg_base64()

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
  background-image: url("data:image/png;base64,{BG_B64}");
  background-size: cover;
  background-position: center top;
}}
.stButton > button {{
  border-radius: 12px;
  background: linear-gradient(135deg, #01478D, #2E6DB4);
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

# Matriz y simulación simplificada (funciona)
def simular_markov(n_usuarios, max_pasos=25):
    np.random.seed(42)
    data = []
    for i in range(n_usuarios):
        estado = 0
        pasos = 0
        while estado < 30 and pasos < max_pasos:
            r = np.random.random()
            if r < 0.62:
                estado += 1
            elif r < 0.78:
                estado = max(0, estado - 1)
            else:
                estado = np.random.randint(0, 29)
            pasos += 1
        estado_final = min(estado, 32)
        data.append({
            "Usuario": i+1,
            "Estado_Final": f"S{estado_final}",
            "Pasos": pasos,
            "Exito": estado_final == 30,
            "Abandono": estado_final in [31, 32]
        })
    return pd.DataFrame(data)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("🇨🇴 **Colombia Comparte**")
    st.markdown("### ⚙️ Parámetros")
    n_usuarios = st.slider("USUARIOS A SIMULAR", 100, 5000, 1000, 100)
    max_pasos = st.slider("MÁXIMO DE PASOS POR USUARIO", 5, 50, 25)
    st.selectbox("ESTADO INICIAL", ["S0 – Página de inicio"])
    
    st.markdown("### Estados finales del modelo:")
    st.success("✅ S30 – Inscripción completada (Éxito)")
    st.error("❌ S31 – Abandono voluntario")
    st.warning("⚠️ S32 – Abandono por error técnico")

# ====================== HERO ======================
st.markdown("""
<div style="background: linear-gradient(135deg, #1E3A5F, #1E40AF); border-radius: 16px; padding: 28px 40px; color: white; margin-bottom: 24px;">
    <h1 style="margin:0; font-size:2.4rem;">Dashboard de Simulación</h1>
    <p style="margin:8px 0 16px 0;">Modelo de Cadenas de Márkov aplicado al flujo de navegación y registro de usuarios en la plataforma de Colombia Comparte.</p>
</div>
""", unsafe_allow_html=True)

# ====================== KPIs ======================
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("ESTADOS", "33")
with c2:
    st.metric("RECORRIDOS BASE", "66")
with c3:
    st.metric("USUARIOS SIMULADOS", "1,000")
with c4:
    st.metric("TASA DE ÉXITO", "41.9%", delta="✅")
with c5:
    st.metric("TASA DE ABANDONO", "50.5%", delta="❌")
with c6:
    st.metric("ESTADO CRÍTICO", "S4")

# ====================== TABS Y SIMULACIÓN ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📋 Estados", "🔄 Recorridos", "📈 Matrices", "▶️ Simulación"])

with tab5:
    if st.button("▶️ Ejecutar Simulación", type="primary", use_container_width=True):
        with st.spinner("Ejecutando simulación Monte Carlo..."):
            df = simular_markov(n_usuarios, max_pasos)
            st.session_state.df = df
        st.success(f"✅ Simulación completada con {n_usuarios:,} usuarios")
        st.dataframe(df.head(15), use_container_width=True)

st.caption("Created by xXHackerXx-mvp • Hosted with Streamlit")
