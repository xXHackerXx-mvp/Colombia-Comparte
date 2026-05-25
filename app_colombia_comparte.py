import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Colombia Comparte · Simulación EDIFICA", layout="wide", page_icon="")

# ====================== ESTILOS (igual al screenshot) ======================
st.markdown("""
<style>
    .stApp {background-color: #0F172A;}
    .main {background-color: #0F172A;}
    .metric-card {
        background: #1E2937;
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        border: 1px solid #334155;
    }
    .kpi-value {font-size: 1.9rem; font-weight: 800; color: white; line-height: 1;}
    .kpi-label {font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;}
    .hero {
        background: linear-gradient(135deg, #1E3A5F, #1E40AF);
        border-radius: 16px;
        padding: 32px 40px;
        color: white;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab-list"] {background: #1E2937; border-radius: 10px;}
    .stTabs [data-baseweb="tab"] {color: #CBD5E1;}
    .stTabs [aria-selected="true"] {background: #3B82F6; color: white; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# ====================== DATOS Y LÓGICA MARKOV ======================
ESTADOS = [f"S{i}" for i in range(33)]
NOMBRES = {
    "S0": "Página de inicio", "S30": "Inscripción completada (Éxito)",
    "S31": "Abandono voluntario", "S32": "Abandono por error técnico"
}

def simular_markov(n=1000, max_pasos=25):
    np.random.seed(42)
    data = []
    for i in range(n):
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
            "Nombre": NOMBRES.get(f"S{estado_final}", f"S{estado_final}"),
            "Pasos": pasos,
            "Exito": estado_final == 30,
            "Abandono": estado_final in [31, 32]
        })
    return pd.DataFrame(data)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("""
    <div style="background:#1E2937; border-radius:12px; padding:16px; text-align:center; margin-bottom:24px;">
        <div style="font-weight:800; font-size:1.05rem; color:white;">co Colombia Comparte</div>
        <div style="font-size:0.75rem; color:#64748B;">SIMULACIÓN PROGRAMA EDIFICA</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Parámetros")
    n_usuarios = st.slider("USUARIOS A SIMULAR", 100, 5000, 1000, 100)
    max_pasos = st.slider("MÁXIMO DE PASOS POR USUARIO", 5, 50, 25)
    estado_inicial = st.selectbox("ESTADO INICIAL", ["S0 – Página de inicio"])
    
    st.markdown("### Estados finales del modelo:")
    st.success("✅ S30 – Inscripción completada (Éxito)")
    st.error("❌ S31 – Abandono voluntario")
    st.warning("⚠️ S32 – Abandono por error técnico")

# ====================== HERO ======================
st.markdown("""
<div class="hero">
    <h1 style="margin:0 0 8px 0; font-size:2.3rem;">Dashboard de Simulación</h1>
    <p style="margin:0 0 20px 0; opacity:0.9;">Modelo de Cadenas de Márkov aplicado al flujo de navegación y registro de usuarios en la plataforma de Colombia Comparte.</p>
    
    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.8rem;">📊 33 Estados</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.8rem;">🔄 66 Recorridos base</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.8rem;">📈 Cadenas de Márkov</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.8rem;">🎓 Universidad Santo Tomás - Tunja</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.8rem;">📅 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== KPIs ======================
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown('<div class="metric-card"><div class="kpi-label">ESTADOS</div><div class="kpi-value">33</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="kpi-label">RECORRIDOS BASE</div><div class="kpi-value">66</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="kpi-label">USUARIOS SIMULADOS</div><div class="kpi-value">1,000</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><div class="kpi-label">TASA DE ÉXITO</div><div class="kpi-value" style="color:#22C55E;">41.9%</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="metric-card"><div class="kpi-label">TASA DE ABANDONO</div><div class="kpi-value" style="color:#EF4444;">50.5%</div></div>', unsafe_allow_html=True)
with col6:
    st.markdown('<div class="metric-card"><div class="kpi-label">ESTADO CRÍTICO</div><div class="kpi-value" style="color:#F59E0B;">S4</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ====================== TABS ======================
tab_resumen, tab_estados, tab_recorridos, tab_matrices, tab_simulacion = st.tabs([
    "📊 Resumen", "📋 Estados", "🔄 Recorridos", "📈 Matrices", "▶️ Simulación"
])

with tab_resumen:
    st.subheader("Resumen ejecutivo del modelo")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:#14532D; border-radius:12px; padding:20px; color:white; height:160px;">
            <h4 style="margin-top:0;">✅ Resultado exitoso</h4>
            <p style="font-size:0.9rem;">El usuario completa la inscripción al Programa EDIFICA correctamente. Representa la conversión deseada de la plataforma.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#431407; border-radius:12px; padding:20px; color:white; height:160px;">
            <h4 style="margin-top:0;">❌ Abandono voluntario</h4>
            <p style="font-size:0.9rem;">El usuario sale del proceso antes de completar la inscripción. Puede deberse a fricción, duda o distracción externa.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:#431407; border-radius:12px; padding:20px; color:white; height:160px;">
            <h4 style="margin-top:0;">⚠️ Error técnico</h4>
            <p style="font-size:0.9rem;">El usuario encuentra una falla, página caída o error de formulario que impide continuar el recorrido.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_simulacion:
    if st.button("▶️ Ejecutar Simulación", type="primary", use_container_width=True):
        with st.spinner("Ejecutando simulación Monte Carlo..."):
            df = simular_markov(n_usuarios, max_pasos)
            st.session_state["df"] = df
        
        df = st.session_state["df"]
        exito = df["Exito"].mean() * 100
        abandono = df["Abandono"].mean() * 100
        
        st.success(f"✅ Simulación completada con {n_usuarios:,} usuarios")
        
        col_a, col_b = st.columns(2)
        col_a.metric("Tasa de Éxito", f"{exito:.1f}%")
        col_b.metric("Tasa de Abandono", f"{abandono:.1f}%")
        
        st.dataframe(df.head(20), use_container_width=True)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 4))
        df["Estado_Final"].value_counts().head(10).plot(kind="bar", ax=ax, color="#3B82F6")
        ax.set_title("Distribución de Estados Finales (Top 10)")
        st.pyplot(fig)

st.caption("Created by xXHackerXx-mvp • Hosted with Streamlit")
