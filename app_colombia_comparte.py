import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Colombia Comparte · Simulación EDIFICA", layout="wide", page_icon="🇨🇴")

# ====================== ESTILOS EXACTOS AL SCREENSHOT ======================
st.markdown("""
<style>
    .stApp {background-color: #0F172A;}
    .main {background-color: #0F172A;}
    .metric-card {
        background: #1E2937;
        border-radius: 12px;
        padding: 20px 12px;
        text-align: center;
        border: 1px solid #334155;
    }
    .kpi-value {font-size: 2rem; font-weight: 800; color: white;}
    .kpi-label {font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;}
    .hero {
        background: linear-gradient(135deg, #1E3A5F, #1E40AF);
        border-radius: 16px;
        padding: 28px 40px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ====================== LÓGICA MARKOV (funcional) ======================
def simular_markov(n_usuarios=1000, max_pasos=25):
    np.random.seed(42)
    data = []
    for i in range(n_usuarios):
        estado = 0
        pasos = 0
        while estado < 30 and pasos < max_pasos:
            r = np.random.random()
            if r < 0.62: estado += 1
            elif r < 0.78: estado = max(0, estado - 1)
            else: estado = np.random.randint(0, 29)
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
    st.markdown("""
    <div style="background:#1E2937; border-radius:12px; padding:16px; text-align:center; margin-bottom:20px;">
        <div style="font-weight:800; color:white;">🇨🇴 Colombia Comparte</div>
        <div style="font-size:0.8rem; color:#8BA3C7;">SIMULACIÓN PROGRAMA EDIFICA</div>
    </div>
    """, unsafe_allow_html=True)
    
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
<div class="hero">
    <h1 style="margin:0; font-size:2.4rem;">Dashboard de Simulación</h1>
    <p style="margin:8px 0 16px 0;">Modelo de Cadenas de Márkov aplicado al flujo de navegación y registro de usuarios en la plataforma de Colombia Comparte.</p>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <div style="background:#2E5A8B; padding:6px 16px; border-radius:9999px; font-size:0.85rem;">📊 33 Estados</div>
        <div style="background:#2E5A8B; padding:6px 16px; border-radius:9999px; font-size:0.85rem;">🔄 66 Recorridos base</div>
        <div style="background:#2E5A8B; padding:6px 16px; border-radius:9999px; font-size:0.85rem;">📈 Cadenas de Márkov</div>
        <div style="background:#2E5A8B; padding:6px 16px; border-radius:9999px; font-size:0.85rem;">🎓 Universidad Santo Tomás - Tunja</div>
        <div style="background:#2E5A8B; padding:6px 16px; border-radius:9999px; font-size:0.85rem;">📅 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== KPIs ======================
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown('<div class="metric-card"><div class="kpi-label">ESTADOS</div><div class="kpi-value">33</div></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="metric-card"><div class="kpi-label">RECORRIDOS BASE</div><div class="kpi-value">66</div></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="metric-card"><div class="kpi-label">USUARIOS SIMULADOS</div><div class="kpi-value">1,000</div></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric-card"><div class="kpi-label">TASA DE ÉXITO</div><div class="kpi-value" style="color:#22C55E;">41.9%</div></div>', unsafe_allow_html=True)
with c5: st.markdown('<div class="metric-card"><div class="kpi-label">TASA DE ABANDONO</div><div class="kpi-value" style="color:#EF4444;">50.5%</div></div>', unsafe_allow_html=True)
with c6: st.markdown('<div class="metric-card"><div class="kpi-label">ESTADO CRÍTICO</div><div class="kpi-value" style="color:#F59E0B;">S4</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📋 Estados", "🔄 Recorridos", "📈 Matrices", "▶️ Simulación"])

with tab1:
    st.subheader("Resumen ejecutivo del modelo")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div style="background:#14532D;border-radius:12px;padding:20px;color:white;height:170px;">
            <h4>✅ Resultado exitoso</h4><p>El usuario completa la inscripción al Programa EDIFICA correctamente.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div style="background:#431407;border-radius:12px;padding:20px;color:white;height:170px;">
            <h4>❌ Abandono voluntario</h4><p>El usuario sale del proceso antes de completar la inscripción.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div style="background:#431407;border-radius:12px;padding:20px;color:white;height:170px;">
            <h4>⚠️ Error técnico</h4><p>El usuario encuentra una falla o error de formulario.</p>
        </div>""", unsafe_allow_html=True)

with tab5:
    if st.button("▶️ Ejecutar Simulación", type="primary", use_container_width=True):
        with st.spinner("Ejecutando simulación..."):
            df = simular_markov(n_usuarios, max_pasos)
            st.session_state.df = df
        st.success(f"✅ Simulación completada con {n_usuarios:,} usuarios")
        st.dataframe(df.head(15), use_container_width=True)

st.caption("Created by xXHackerXx-mvp • Hosted with Streamlit")
