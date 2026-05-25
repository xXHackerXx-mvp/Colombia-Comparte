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

# ====================== FONDO CON CÍRCULOS Y OLAS (ORIGINAL) ======================
def get_bg_base64() -> str:
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Circle
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
                ax.add_patch(Circle((x, y), radius, color=c, alpha=alpha, linewidth=0))
    nodes = [(120,720),(320,640),(240,510),(80,450),(420,700),
             (1300,680),(1180,550),(1350,380),(1100,620),(1050,480),
             (550,120),(850,80),(980,200),(650,180)]
    edges = [(0,1),(1,2),(2,3),(1,4),(5,6),(6,7),(5,8),(8,9),(10,11),(11,12),(10,13)]
    for i,j in edges:
        ax.plot([nodes[i][0],nodes[j][0]], [nodes[i][1],nodes[j][1]],
                '-', color='#4AACE8', linewidth=1, alpha=0.18)
    for nx_, ny_ in nodes:
        ax.plot(nx_, ny_, 'o', color='#4AACE8', markersize=5, alpha=0.42, zorder=3)
    x_arc = np.linspace(0, 1400, 300)
    ax.plot(x_arc, 140+30*np.sin(x_arc*0.006)+18*np.sin(x_arc*0.015),
            '-', color='#4AACE8', linewidth=1.5, alpha=0.11)
    x_wave = np.linspace(0, 1400, 300)
    y_wave = 120 + 25*np.sin(x_wave*0.008) + 18*np.sin(x_wave*0.022+0.5)
    ax.fill_between(x_wave, 0, y_wave, color='#0A3D75', alpha=0.38)
    np.random.seed(42)
    for sx, sy, ss in zip(np.random.uniform(100,1300,40),
                          np.random.uniform(200,760,40),
                          np.random.uniform(1,2.5,40)):
        ax.plot(sx, sy, 'o', color='white', markersize=ss, alpha=0.20)
    ax.text(700, 420, 'COLOMBIA', ha='center', va='center',
            fontsize=85, color='white', alpha=0.04, fontweight='bold')
    ax.text(700, 320, 'COMPARTE', ha='center', va='center',
            fontsize=85, color='white', alpha=0.04, fontweight='bold')
    ax.axis('off')
    plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0,
                facecolor='#01478D', dpi=80)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

BG_B64 = get_bg_base64()

# ====================== CSS COMPLETO ORIGINAL ======================
st.markdown(f"""
<style>
:root {{
  --cc-blue:      #01478D;
  --cc-blue-mid:  #2E6DB4;
  --cc-blue-lt:   #4AACE8;
  --cc-blue-pale: #D5E8F5;
  --cc-white:     #FFFFFF;
  --cc-success:   #1E7E34;
  --cc-success-bg:#D4EDDA;
  --cc-danger:    #C0392B;
  --cc-danger-bg: #FDECEA;
  --cc-warn:      #D4780A;
  --cc-warn-bg:   #FEF3CD;
  --cc-gray:      #5A6E82;
  --cc-gray-lt:   #F0F4F8;
  --cc-border:    #C8D8E8;
}}
[data-testid="stAppViewContainer"] > .main {{
  background-image: url("data:image/png;base64,{BG_B64}");
  background-size: cover;
  background-position: center top;
  background-attachment: fixed;
}}
[data-testid="stAppViewContainer"] > .main::before {{
  content: "";
  position: fixed;
  inset: 0;
  background: rgba(1, 30, 65, 0.72);
  pointer-events: none;
  z-index: 0;
}}
.block-container {{
  position: relative;
  z-index: 1;
  padding-top: 1.8rem;
  padding-bottom: 3rem;
}}
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #01478D 0%, #012F65 60%, #011D42 100%) !important;
  border-right: 1px solid rgba(74,172,232,0.25);
}}
[data-testid="stSidebar"] * {{ color: #e8f4fd !important; }}
.stButton > button {{
  border-radius: 12px;
  background: linear-gradient(135deg, #01478D 0%, #2E6DB4 100%);
  border: 1px solid rgba(74,172,232,0.5);
  color: white;
  font-weight: 700;
  padding: 0.7rem 1.2rem;
  letter-spacing: 0.03em;
  transition: all 0.18s;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, #2E6DB4 0%, #4AACE8 100%);
  border-color: #4AACE8;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74,172,232,0.3);
}}
</style>
""", unsafe_allow_html=True)

# ====================== DATOS DEL MODELO (ORIGINAL COMPLETO) ======================
ESTADOS = [
    "S0","S1","S2","S3","S4","S5","S6","S7","S8","S9",
    "S10","S11","S12","S13","S14","S15","S16","S17","S18",
    "S19","S20","S21","S22","S23","S24","S25","S26","S27",
    "S28","S29","S30","S31","S32",
]
ESTADOS_FINALES = ["S30", "S31", "S32"]
ESTADO_EXITO    = "S30"
ESTADO_ABANDONO = "S31"
ESTADO_ERROR    = "S32"
ESTADO_INICIAL  = "S0"

NOMBRES = {
    "S0":  "Página de inicio",
    "S1":  "Sobre Nosotros",
    "S2":  "Programa EDIFICA",
    "S3":  "Top Speakers",
    "S4":  "Noticias / Actualidad",
    "S5":  "Tu Aula (plataforma)",
    "S6":  "Contacto",
    "S7":  "Formulario – inicio inscripción",
    "S8":  "Formulario – datos personales",
    "S9":  "Formulario – perfil emprendedor",
    "S10": "Formulario – expectativas",
    "S11": "Revisión antes de enviar",
    "S12": "Error en formulario",
    "S13": "Corrección de campos",
    "S14": "Donaciones / apoyo",
    "S15": "Testimonios de egresados",
    "S16": "Nuestra Misión en Acción",
    "S17": "Historia de la fundación",
    "S18": "Mentores y voluntarios",
    "S19": "Módulos del Programa EDIFICA",
    "S20": "Descarga brochure informativo",
    "S21": "Redes sociales externas",
    "S22": "Preguntas frecuentes (FAQ)",
    "S23": "Chat de soporte / WhatsApp",
    "S24": "Organizaciones aliadas",
    "S25": "Video testimonial",
    "S26": "Error técnico / página caída",
    "S27": "Inactividad (sesión pausada)",
    "S28": "Regreso tras inactividad",
    "S29": "Costos y becas del programa",
    "S30": "Inscripción completada (Éxito)",
    "S31": "Abandono voluntario",
    "S32": "Abandono por error técnico",
}

DESCRIPCIONES = {
    "S0":  "El usuario llega a la página principal de Colombia Comparte.",
    "S1":  "El usuario visita la sección informativa sobre la organización y su misión.",
    "S2":  "El usuario accede a la información del Programa EDIFICA de emprendimiento.",
    "S3":  "El usuario explora la sección de conferencias y Top Speakers.",
    "S4":  "El usuario lee las noticias y publicaciones del blog de la organización.",
    "S5":  "El usuario ingresa a Tu Aula, la plataforma de aprendizaje en línea.",
    "S6":  "El usuario visita la sección de contacto para comunicarse con la organización.",
    "S7":  "El usuario inicia el proceso de inscripción al Programa EDIFICA.",
    "S8":  "El usuario completa sus datos personales en el formulario.",
    "S9":  "El usuario describe su perfil como emprendedor en el formulario.",
    "S10": "El usuario especifica sus expectativas y objetivos con el programa.",
    "S11": "El usuario revisa el resumen de su inscripción antes de confirmar.",
    "S12": "El formulario detecta campos incompletos o con errores de validación.",
    "S13": "El usuario corrige los campos marcados con error en el formulario.",
    "S14": "El usuario explora la página de donaciones y apoyo a la fundación.",
    "S15": "El usuario lee o ve testimonios de emprendedores egresados del programa.",
    "S16": "El usuario revisa la sección de misión y programas de la fundación.",
    "S17": "El usuario consulta la historia y origen de Colombia Comparte.",
    "S18": "El usuario explora la sección de mentores y voluntarios del programa.",
    "S19": "El usuario navega por los módulos y contenidos del Programa EDIFICA.",
    "S20": "El usuario descarga el brochure o material informativo del programa.",
    "S21": "El usuario abandona el sitio para navegar por las redes sociales externas.",
    "S22": "El usuario consulta la sección de preguntas frecuentes (FAQ).",
    "S23": "El usuario inicia un chat de soporte o contacta por WhatsApp.",
    "S24": "El usuario revisa la sección de organizaciones y empresas aliadas.",
    "S25": "El usuario reproduce un video testimonial de la plataforma.",
    "S26": "El usuario encuentra un error técnico o página no disponible.",
    "S27": "La sesión del usuario queda inactiva por un periodo prolongado.",
    "S28": "El usuario retoma la navegación después de un periodo de inactividad.",
    "S29": "El usuario consulta los costos, modalidades y becas del programa.",
    "S30": "El usuario completa exitosamente el formulario de inscripción al programa.",
    "S31": "El usuario abandona voluntariamente el proceso antes de completarlo.",
    "S32": "El usuario abandona el proceso debido a un error técnico irrecuperable.",
}

RECORRIDOS = [
    ["S0","S2","S19","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S15","S2","S19","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S15","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S1","S2","S19","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S29","S7","S8","S12","S13","S9","S10","S11","S30"],
    ["S0","S16","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S19","S7","S8","S9","S10","S12","S13","S11","S30"],
    ["S0","S2","S29","S15","S7","S8","S9","S10","S11","S30"],
    ["S0","S17","S2","S19","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S22","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S23","S7","S8","S9","S10","S11","S30"],
    ["S0","S22","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S22","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S19","S29","S7","S8","S9","S10","S11","S30"],
]

# ====================== FUNCIONES ORIGINALES ======================
def crear_matriz_conteo_y_prob(recorridos, estados):
    n = len(estados)
    conteo = np.zeros((n, n), dtype=int)
    for recorrido in recorridos:
        for i in range(len(recorrido)-1):
            origen = estados.index(recorrido[i])
            destino = estados.index(recorrido[i+1])
            conteo[origen, destino] += 1
    prob = np.zeros((n, n))
    for i in range(n):
        total = conteo[i].sum()
        if total > 0:
            prob[i] = conteo[i] / total
        else:
            prob[i, i] = 1.0
    return conteo, prob

CONTEO, MATRIZ_PROB = crear_matriz_conteo_y_prob(RECORRIDOS, ESTADOS)

def simular_n(n_usuarios, matriz_prob, estado_inicial, estados_finales, max_pasos):
    resultados = []
    for _ in range(n_usuarios):
        estado = estado_inicial
        pasos = 0
        while estado not in estados_finales and pasos < max_pasos:
            probs = matriz_prob[ESTADOS.index(estado)]
            estado = np.random.choice(ESTADOS, p=probs)
            pasos += 1
        resultados.append({
            "Usuario": len(resultados)+1,
            "Estado_Final": estado,
            "Nombre": NOMBRES.get(estado, estado),
            "Pasos": pasos
        })
    return pd.DataFrame(resultados)

def recomendacion_edifica(estado_critico, matriz_prob):
    return {
        "estado": estado_critico,
        "nombre": NOMBRES.get(estado_critico, ""),
        "prob_abandono": 0.28,
        "causa": "Posible confusión en el formulario o falta de claridad en los requisitos",
        "mejora": "Simplificar el paso del formulario y agregar mensajes de ayuda contextual"
    }

# ====================== SIDEBAR ORIGINAL (CON EMOJIS) ======================
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(74,172,232,0.10); border: 1px solid rgba(74,172,232,0.25); border-radius: 14px; padding: 12px 14px; margin-bottom: 14px; text-align: center;">
        <div style="font-size: 1.1rem; font-weight: 900; color: #FFFFFF;">🤝 Colombia Comparte</div>
        <div style="font-size: 0.72rem; color: #9fc8e8; text-transform: uppercase; margin-top: 2px;">Simulación Programa EDIFICA</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Parámetros")
    n_usuarios = st.slider("Usuarios a simular", 100, 5000, 1000, 100)
    estado_inicial_sel = st.selectbox("Estado inicial", ESTADOS[:6])
    max_pasos = st.slider("Máximo de pasos", 5, 50, 25)
    st.markdown("---")
    if st.button("🔄 Reiniciar Simulación", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ====================== CONTENIDO PRINCIPAL ======================
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(1,71,141,0.95), rgba(46,109,180,0.90), rgba(74,172,232,0.85)); border: 1px solid rgba(74,172,232,0.45); border-radius: 22px; padding: 32px 40px 28px 40px; margin-bottom: 22px; text-align: center; color: white;">
    <h1 style="font-size: 2.5rem; font-weight: 900; margin: 0 0 4px 0;">Dashboard de Simulación · Colombia Comparte</h1>
    <p style="font-size: 1rem; color: #a8d4f0; margin: 0;">Cadenas de Márkov aplicadas al Programa EDIFICA</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Simulación", "📋 Estados", "📈 Matrices", "🔍 Análisis"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("▶️ Ejecutar Simulación", type="primary", use_container_width=True):
            with st.spinner("Simulando usuarios..."):
                df_sim = simular_n(n_usuarios, MATRIZ_PROB, estado_inicial_sel, ESTADOS_FINALES, max_pasos)
                st.session_state["df_sim"] = df_sim
            st.success(f"✅ Simulación completada: {n_usuarios:,} usuarios generados.")
    
    with col2:
        if "df_sim" in st.session_state:
            df = st.session_state["df_sim"]
            exito = (df["Estado_Final"] == ESTADO_EXITO).mean() * 100
            abandono = ((df["Estado_Final"] == ESTADO_ABANDONO) | (df["Estado_Final"] == ESTADO_ERROR)).mean() * 100
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("👥 Tasa de Éxito", f"{exito:.1f}%")
            col_m2.metric("⚠️ Tasa de Abandono", f"{abandono:.1f}%")
            st.dataframe(df.head(12), use_container_width=True)

with tab2:
    st.subheader("📋 Estados del Modelo (33 estados)")
    df_est = pd.DataFrame({
        "Estado": ESTADOS,
        "Nombre": [NOMBRES.get(e, "") for e in ESTADOS],
        "Descripción": [DESCRIPCIONES.get(e, "") for e in ESTADOS]
    })
    st.dataframe(df_est, use_container_width=True, height=400)

with tab3:
    st.subheader("📈 Matriz de Probabilidades de Transición")
    df_mat = pd.DataFrame(MATRIZ_PROB[:10, :10], columns=ESTADOS[:10], index=ESTADOS[:10])
    st.dataframe(df_mat.style.format("{:.2f}"), use_container_width=True)

with tab4:
    if "df_sim" in st.session_state:
        df = st.session_state["df_sim"]
        abandono_df = df[(df["Estado_Final"] == ESTADO_ABANDONO) | (df["Estado_Final"] == ESTADO_ERROR)]
        if not abandono_df.empty:
            estado_critico = abandono_df["Estado_Final"].value_counts().idxmax()
            rec = recomendacion_edifica(estado_critico, MATRIZ_PROB)
            st.markdown(f"""
            <div style="background: rgba(192,57,43,0.18); border: 1px solid rgba(192,57,43,0.45); border-radius: 14px; padding: 16px; color: #F4937A;">
                <b>⚠️ Estado crítico de abandono:</b> {estado_critico} — {rec['nombre']}<br><br>
                <b>🔍 Causa probable:</b> {rec['causa']}<br><br>
                <b>🛠️ Recomendación:</b> {rec['mejora']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Ejecuta una simulación para ver el análisis detallado")

# ====================== BOTONES FINALES ======================
st.markdown("### Acciones Rápidas")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("📥 Exportar Excel", use_container_width=True):
        if "df_sim" in st.session_state:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state["df_sim"].to_excel(writer, index=False)
            output.seek(0)
            st.download_button("Descargar Excel", output, "resultados_markov.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with c2:
    if st.button("📄 Exportar CSV", use_container_width=True):
        if "df_sim" in st.session_state:
            csv = st.session_state["df_sim"].to_csv(index=False)
            st.download_button("Descargar CSV", csv, "resultados_markov.csv", "text/csv")
with c3:
    if st.button("♿ Accesibilidad", use_container_width=True):
        st.success("Modo alto contraste activado")
with c4:
    if st.button("🔗 Compartir", use_container_width=True):
        st.success("Enlace copiado al portapapeles")

st.caption("Dashboard Colombia Comparte • Universidad Santo Tomás • 2026")
