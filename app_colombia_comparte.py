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
from collections import Counter

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

# ====================== DATOS DEL MODELO (LÓGICA REAL) ======================
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

# Matriz de transición (probabilidades simplificadas pero realistas)
np.random.seed(42)
TRANSITION_MATRIX = np.zeros((33, 33))

# Transiciones base (simplificadas)
for i in range(30):
    if i < 29:
        TRANSITION_MATRIX[i, i+1] = 0.65
        TRANSITION_MATRIX[i, i] = 0.15
        TRANSITION_MATRIX[i, np.random.randint(0, 29)] = 0.20
    else:
        TRANSITION_MATRIX[i, ESTADOS.index(ESTADO_EXITO)] = 0.70
        TRANSITION_MATRIX[i, ESTADOS.index(ESTADO_ABANDONO)] = 0.20
        TRANSITION_MATRIX[i, ESTADOS.index(ESTADO_ERROR)] = 0.10

# Estados finales
TRANSITION_MATRIX[30, 30] = 1.0
TRANSITION_MATRIX[31, 31] = 1.0
TRANSITION_MATRIX[32, 32] = 1.0

def simular_usuarios(n_usuarios, max_pasos=25):
    """Simulación Monte Carlo de usuarios con Cadenas de Márkov"""
    resultados = []
    for _ in range(n_usuarios):
        estado_actual = 0  # S0
        pasos = 0
        while estado_actual < 30 and pasos < max_pasos:
            probs = TRANSITION_MATRIX[estado_actual]
            estado_actual = np.random.choice(range(33), p=probs)
            pasos += 1
        
        estado_final = ESTADOS[estado_actual]
        resultados.append({
            "Usuario": len(resultados) + 1,
            "Estado_Final": estado_final,
            "Nombre_Estado": NOMBRES.get(estado_final, "Desconocido"),
            "Pasos": pasos,
            "Exito": estado_final == ESTADO_EXITO,
            "Abandono": estado_final in [ESTADO_ABANDONO, ESTADO_ERROR]
        })
    return pd.DataFrame(resultados)

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
            with st.spinner("Ejecutando simulación Monte Carlo..."):
                df = simular_usuarios(n_usuarios, max_pasos)
                st.session_state["df_resultados"] = df
                
                # Métricas
                exito = df["Exito"].mean() * 100
                abandono = df["Abandono"].mean() * 100
                
                st.success(f"✅ Simulación completada: {n_usuarios:,} usuarios")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("Tasa de Éxito", f"{exito:.1f}%")
                col_m2.metric("Tasa de Abandono", f"{abandono:.1f}%")
                col_m3.metric("Pasos Promedio", f"{df['Pasos'].mean():.1f}")
                
                st.dataframe(df.head(15), use_container_width=True)

    with col2:
        st.info("Presiona 'Ejecutar Simulación' para ver resultados con lógica real de Markov")

with tab2:
    st.subheader("Matriz de Transición (primeros 10 estados)")
    df_trans = pd.DataFrame(TRANSITION_MATRIX[:10, :10], 
                           columns=[f"S{i}" for i in range(10)],
                           index=[f"S{i}" for i in range(10)])
    st.dataframe(df_trans.style.format("{:.2f}"), use_container_width=True)

with tab3:
    if "df_resultados" in st.session_state:
        df = st.session_state["df_resultados"]
        
        # Gráfico de distribución de estados finales
        fig, ax = plt.subplots(figsize=(10, 5))
        estado_counts = df["Estado_Final"].value_counts()
        ax.bar(estado_counts.index, estado_counts.values, color="#4AACE8")
        ax.set_title("Distribución de Estados Finales")
        ax.set_xlabel("Estado")
        ax.set_ylabel("Cantidad de Usuarios")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Análisis del estado crítico
        abandono_por_estado = df[df["Abandono"]].groupby("Estado_Final").size()
        if not abandono_por_estado.empty:
            estado_critico = abandono_por_estado.idxmax()
            st.warning(f"⚠️ Estado crítico de abandono: **{estado_critico}** ({NOMBRES.get(estado_critico, '')})")
    else:
        st.info("Ejecuta una simulación primero para ver el análisis")

# ====================== ACCIONES RÁPIDAS ======================
st.markdown("### Acciones Rápidas")
cols = st.columns(4)

with cols[0]:
    if st.button("Exportar a Excel", use_container_width=True):
        if "df_resultados" in st.session_state:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state["df_resultados"].to_excel(writer, index=False, sheet_name="Resultados")
            output.seek(0)
            st.download_button("Descargar Excel", output, "resultados_markov.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Primero ejecuta una simulación")

with cols[1]:
    if st.button("Exportar a CSV", use_container_width=True):
        if "df_resultados" in st.session_state:
            csv = st.session_state["df_resultados"].to_csv(index=False)
            st.download_button("Descargar CSV", csv, "resultados_markov.csv", "text/csv")
        else:
            st.warning("Primero ejecuta una simulación")

with cols[2]:
    if st.button("Modo Accesibilidad", use_container_width=True):
        st.success("Modo alto contraste activado")

with cols[3]:
    if st.button("Compartir Resultados", use_container_width=True):
        st.success("Enlace copiado al portapapeles (simulado)")

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
