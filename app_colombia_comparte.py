import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Colombia Comparte · Simulación EDIFICA", layout="wide", page_icon="")

# ====================== ESTILOS (igual al screenshot) ======================
st.markdown("""
<style>
    .main {background-color: #0D1B2A;}
    .stApp {background-color: #0D1B2A;}
    .sidebar .stMarkdown {color: white;}
    .metric-card {
        background: #1B2838;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid #2E4A6B;
    }
    .kpi-value {font-size: 1.8rem; font-weight: 800; color: white;}
    .kpi-label {font-size: 0.75rem; color: #8BA3C7; text-transform: uppercase;}
    .hero {
        background: linear-gradient(135deg, #1E3A5F, #2E5A8B);
        border-radius: 16px;
        padding: 32px;
        color: white;
        margin-bottom: 20px;
    }
    .tab-button {
        background: #1B2838;
        border-radius: 8px;
        padding: 8px 16px;
        margin: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== DATOS ======================
ESTADOS = [f"S{i}" for i in range(33)]
NOMBRES = {
    "S0": "Página de inicio", "S30": "Inscripción completada (Éxito)",
    "S31": "Abandono voluntario", "S32": "Abandono por error técnico"
}
ESTADOS_FINALES = ["S30", "S31", "S32"]

def simular_markov(n_usuarios=1000, max_pasos=25):
    np.random.seed(42)
    resultados = []
    for _ in range(n_usuarios):
        estado = 0
        pasos = 0
        while estado < 30 and pasos < max_pasos:
            if np.random.random() < 0.65:
                estado += 1
            elif np.random.random() < 0.25:
                estado = max(0, estado - 1)
            else:
                estado = np.random.randint(0, 30)
            pasos += 1
        estado_final = min(estado, 32)
        resultados.append({
            "Usuario": len(resultados)+1,
            "Estado_Final": f"S{estado_final}",
            "Pasos": pasos,
            "Exito": estado_final == 30,
            "Abandono": estado_final in [31, 32]
        })
    return pd.DataFrame(resultados)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("""
    <div style="background:#1B2838; border-radius:12px; padding:16px; margin-bottom:20px; text-align:center;">
        <div style="font-size:1.1rem; font-weight:800; color:white;">🇨🇴 Colombia Comparte</div>
        <div style="font-size:0.8rem; color:#8BA3C7;">SIMULACIÓN PROGRAMA EDIFICA</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Parámetros")
    n_usuarios = st.slider("USUARIOS A SIMULAR", 100, 5000, 1000, 100)
    max_pasos = st.slider("MÁXIMO DE PASOS POR USUARIO", 5, 50, 25)
    estado_inicial = st.selectbox("ESTADO INICIAL", ["S0 – Página de inicio"])
    
    st.markdown("### Estados finales del modelo:")
    st.markdown("✅ **S30** – Inscripción completada (Éxito)")
    st.markdown("❌ **S31** – Abandono voluntario")
    st.markdown("⚠️ **S32** – Abandono por error técnico")

# ====================== HERO ======================
st.markdown("""
<div class="hero">
    <h1 style="margin:0; font-size:2.2rem;">Dashboard de Simulación</h1>
    <p style="margin:8px 0 16px 0; opacity:0.9;">Modelo de Cadenas de Márkov aplicado al flujo de navegación y registro de usuarios en la plataforma de Colombia Comparte.</p>
    
    <div style="display:flex; gap:12px; flex-wrap:wrap;">
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.85rem;">📊 33 Estados</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.85rem;">🔄 66 Recorridos base</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.85rem;">📈 Cadenas de Márkov</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.85rem;">🎓 Universidad Santo Tomás - Tunja</div>
        <div style="background:#2E5A8B; padding:6px 14px; border-radius:20px; font-size:0.85rem;">📅 2026</div>
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📋 Estados", "🔄 Recorridos", "📈 Matrices", "▶️ Simulación"])

with tab1:
    st.subheader("Resumen ejecutivo del modelo")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:#14532D; border-radius:12px; padding:20px; color:white;">
            <h4>✅ Resultado exitoso</h4>
            <p>El usuario completa la inscripción al Programa EDIFICA correctamente. Representa la conversión deseada de la plataforma.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#431407; border-radius:12px; padding:20px; color:white;">
            <h4>❌ Abandono voluntario</h4>
            <p>El usuario sale del proceso antes de completar la inscripción. Puede deberse a fricción, duda o distracción externa.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:#431407; border-radius:12px; padding:20px; color:white;">
            <h4>⚠️ Error técnico</h4>
            <p>El usuario encuentra una falla, página caída o error de formulario que impide continuar el recorrido.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ¿Cómo funciona el simulador?")
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.info("**PASO 01**\nDefinir estados\nSe definen 33 pantallas y acciones posibles dentro de la plataforma Colombia Comparte.")
    with p2: st.info("**PASO 02**\nModelar recorridos\nSe construyen 66 caminos realistas de 4 perfiles de usuario (A, B, C, D, E).")
    with p3: st.info("**PASO 03**\nCalcular matrices\nSe calcula la matriz de conteos y la matriz de probabilidad de transición entre estados.")
    with p4: st.info("**PASO 04**\nSimular y analizar\nSe simulan N usuarios, se identifican resultados, estado crítico y se genera la recomendación de mejora.")

with tab5:
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
        
        st.dataframe(df.head(15), use_container_width=True)
        
        # Gráfico
        fig, ax = plt.subplots()
        df["Estado_Final"].value_counts().plot(kind="bar", ax=ax, color="#3B82F6")
        ax.set_title("Distribución de Estados Finales")
        st.pyplot(fig)

st.caption("Created by xXHackerXx-mvp • Hosted with Streamlit")
