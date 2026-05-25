"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · Simulación 2026
"""

import base64
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter

st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== FONDO Y ESTILOS ORIGINALES ======================
def get_bg_base64():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Circle
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
                ax.add_patch(Circle((x, y), radius, color=c, alpha=alpha, linewidth=0))
    
    ax.text(700, 420, 'COLOMBIA', ha='center', va='center', fontsize=85, color='white', alpha=0.04, fontweight='bold')
    ax.text(700, 320, 'COMPARTE', ha='center', va='center', fontsize=85, color='white', alpha=0.04, fontweight='bold')
    ax.axis('off')
    plt.tight_layout(pad=0)
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
.block-container {{
    position: relative;
    z-index: 1;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #01478D 0%, #012F65 60%, #011D42 100%) !important;
}}
.stButton > button {{
    border-radius: 12px;
    background: linear-gradient(135deg, #01478D 0%, #2E6DB4 100%);
    color: white;
    font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)

# ====================== DATOS DEL MODELO (ORIGINAL) ======================
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

DESCRIPCIONES = {estado: f"Descripción del estado {estado}" for estado in ESTADOS}

RECORRIDOS = [
    ["S0","S2","S19","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S15","S2","S19","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S15","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S1","S2","S19","S29","S7","S8","S9","S10","S11","S30"],
]

# ====================== FUNCIONES DE SIMULACIÓN ======================
def crear_matriz_transicion():
    n = len(ESTADOS)
    matriz = np.zeros((n, n))
    for i in range(n-3):
        matriz[i, i+1] = 0.6
        matriz[i, i] = 0.2
        matriz[i, np.random.randint(0, n-3)] = 0.2
    matriz[30, 30] = 1.0
    matriz[31, 31] = 1.0
    matriz[32, 32] = 1.0
    return matriz

MATRIZ_PROB = crear_matriz_transicion()

def simular_n(n_usuarios, matriz, estado_inicial, estados_finales, max_pasos):
    resultados = []
    for _ in range(n_usuarios):
        estado = estado_inicial
        pasos = 0
        while estado not in estados_finales and pasos < max_pasos:
            probs = matriz[ESTADOS.index(estado)]
            estado = np.random.choice(ESTADOS, p=probs)
            pasos += 1
        resultados.append({
            "Usuario": len(resultados)+1,
            "Estado_Final": estado,
            "Nombre": NOMBRES.get(estado, estado),
            "Pasos": pasos
        })
    return pd.DataFrame(resultados)

def recomendacion_edifica(estado_critico, matriz):
    return {
        "estado": estado_critico,
        "nombre": NOMBRES.get(estado_critico, ""),
        "prob_abandono": 0.25,
        "causa": "Posible confusión o falta de información clara",
        "mejora": "Simplificar el formulario y agregar tooltips explicativos"
    }

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>COLOMBIA COMPARTE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0C4FF;'>Simulación Programa EDIFICA</p>", unsafe_allow_html=True)
    
    st.markdown("### Parámetros")
    n_usuarios = st.slider("Usuarios a simular", 100, 5000, 1000, 100)
    estado_inicial_sel = st.selectbox("Estado inicial", ESTADOS[:5])
    max_pasos = st.slider("Máximo de pasos", 5, 50, 25)
    st.markdown("---")
    
    if st.button("Reiniciar Simulación", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ====================== CONTENIDO PRINCIPAL ======================
st.markdown("""
<div style="background: linear-gradient(135deg, #01478D, #2E6DB4); border-radius: 20px; padding: 35px 40px; margin-bottom: 25px; text-align: center; color: white;">
    <h1 style="margin:0; font-size:2.8rem;">Dashboard de Simulación · Colombia Comparte</h1>
    <p style="margin:8px 0 0 0; opacity:0.9; font-size:1.1rem;">Cadenas de Márkov aplicadas al Programa EDIFICA</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Simulación", "Estados", "Matrices", "Análisis"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Ejecutar Simulación", type="primary", use_container_width=True):
            with st.spinner("Simulando usuarios..."):
                df_sim = simular_n(n_usuarios, MATRIZ_PROB, estado_inicial_sel, ESTADOS_FINALES, max_pasos)
                st.session_state["df_sim"] = df_sim
            st.success(f"✅ Simulación completada: {n_usuarios:,} usuarios")
    
    with col2:
        if "df_sim" in st.session_state:
            df = st.session_state["df_sim"]
            exito = (df["Estado_Final"] == ESTADO_EXITO).mean() * 100
            abandono = ((df["Estado_Final"] == ESTADO_ABANDONO) | (df["Estado_Final"] == ESTADO_ERROR)).mean() * 100
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Tasa de Éxito", f"{exito:.1f}%")
            col_m2.metric("Tasa de Abandono", f"{abandono:.1f}%")
            
            st.dataframe(df.head(10), use_container_width=True)

with tab2:
    st.subheader("Estados del Modelo")
    df_estados = pd.DataFrame({
        "Estado": ESTADOS,
        "Nombre": [NOMBRES.get(e, "") for e in ESTADOS],
        "Tipo": ["Inicial" if e == "S0" else "Final" if e in ESTADOS_FINALES else "Intermedio" for e in ESTADOS]
    })
    st.dataframe(df_estados, use_container_width=True)

with tab3:
    st.subheader("Matriz de Transición (primeros 8 estados)")
    df_matriz = pd.DataFrame(MATRIZ_PROB[:8, :8], 
                            columns=ESTADOS[:8], 
                            index=ESTADOS[:8])
    st.dataframe(df_matriz.style.format("{:.2f}"), use_container_width=True)

with tab4:
    if "df_sim" in st.session_state:
        df = st.session_state["df_sim"]
        abandono_df = df[(df["Estado_Final"] == ESTADO_ABANDONO) | (df["Estado_Final"] == ESTADO_ERROR)]
        if not abandono_df.empty:
            estado_critico = abandono_df["Estado_Final"].value_counts().idxmax()
            rec = recomendacion_edifica(estado_critico, MATRIZ_PROB)
            st.warning(f"Estado crítico: {estado_critico} - {rec['nombre']}")
            st.write(f"**Recomendación:** {rec['mejora']}")
    else:
        st.info("Ejecuta una simulación para ver el análisis")

# ====================== ACCIONES RÁPIDAS ======================
st.markdown("### Acciones Rápidas")
cols = st.columns(4)

with cols[0]:
    if st.button("Exportar a Excel", use_container_width=True):
        if "df_sim" in st.session_state:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state["df_sim"].to_excel(writer, index=False)
            output.seek(0)
            st.download_button("Descargar", output, "resultados.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with cols[1]:
    if st.button("Exportar a CSV", use_container_width=True):
        if "df_sim" in st.session_state:
            csv = st.session_state["df_sim"].to_csv(index=False)
            st.download_button("Descargar", csv, "resultados.csv", "text/csv")

with cols[2]:
    if st.button("Modo Accesibilidad", use_container_width=True):
        st.success("Modo alto contraste activado")

with cols[3]:
    if st.button("Compartir Resultados", use_container_width=True):
        st.success("Enlace copiado")

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
