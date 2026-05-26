"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov aplicadas al flujo de inscripción al Programa EDIFICA
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
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS  (diseño Simulacion Desing)
# ══════════════════════════════════════════════════════════════════════════════
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
    .hero p  {font-size: 1.1rem; opacity: 0.92; margin-top: 8px;}
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        height: 52px;
    }
    .kpi-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(74,172,232,0.35);
        border-radius: 14px;
        padding: 18px 14px;
        text-align: center;
    }
    .kpi-label {font-size: 0.72rem; text-transform: uppercase;
                letter-spacing: 0.08em; color: #9fc8e8; font-weight: 700;}
    .kpi-value {font-size: 1.9rem; font-weight: 900; color: #FFFFFF; line-height: 1.1;}
    .kpi-detail{font-size: 0.73rem; color: #7bb8d8; margin-top: 3px;}
    .diag-box {
        background: rgba(1,47,101,0.65);
        border-left: 5px solid #4AACE8;
        border-radius: 12px;
        padding: 18px 20px;
        color: #daeef9;
        margin: 12px 0 18px 0;
        line-height: 1.65;
    }
    .rec-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(74,172,232,0.28);
        border-radius: 14px;
        padding: 20px;
        color: #e8f4fd;
        margin-top: 14px;
        line-height: 1.65;
    }
    .rec-box h4 {color:#FFFFFF; margin-top:0; font-size:1rem;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATOS DEL MODELO
# ══════════════════════════════════════════════════════════════════════════════
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

NOMBRES = {
    "S0":"Página de inicio","S1":"Sobre Nosotros","S2":"Programa EDIFICA",
    "S3":"Top Speakers","S4":"Noticias / Actualidad","S5":"Tu Aula (plataforma)",
    "S6":"Contacto","S7":"Formulario – inicio inscripción",
    "S8":"Formulario – datos personales","S9":"Formulario – perfil emprendedor",
    "S10":"Formulario – expectativas","S11":"Revisión antes de enviar",
    "S12":"Error en formulario","S13":"Corrección de campos",
    "S14":"Donaciones / apoyo","S15":"Testimonios de egresados",
    "S16":"Nuestra Misión en Acción","S17":"Historia de la fundación",
    "S18":"Mentores y voluntarios","S19":"Módulos del Programa EDIFICA",
    "S20":"Descarga brochure informativo","S21":"Redes sociales externas",
    "S22":"Preguntas frecuentes (FAQ)","S23":"Chat de soporte / WhatsApp",
    "S24":"Organizaciones aliadas","S25":"Video testimonial",
    "S26":"Error técnico / página caída","S27":"Inactividad (sesión pausada)",
    "S28":"Regreso tras inactividad","S29":"Costos y becas del programa",
    "S30":"Inscripción completada (Éxito)","S31":"Abandono voluntario",
    "S32":"Abandono por error técnico",
}

DESCRIPCIONES = {
    "S0":"El usuario llega a la página principal de Colombia Comparte.",
    "S1":"El usuario visita la sección informativa sobre la organización y su misión.",
    "S2":"El usuario accede a la información del Programa EDIFICA de emprendimiento.",
    "S3":"El usuario explora la sección de conferencias y Top Speakers.",
    "S4":"El usuario lee las noticias y publicaciones del blog de la organización.",
    "S5":"El usuario ingresa a Tu Aula, la plataforma de aprendizaje en línea.",
    "S6":"El usuario visita la sección de contacto para comunicarse con la organización.",
    "S7":"El usuario inicia el proceso de inscripción al Programa EDIFICA.",
    "S8":"El usuario completa sus datos personales en el formulario.",
    "S9":"El usuario describe su perfil como emprendedor en el formulario.",
    "S10":"El usuario especifica sus expectativas y objetivos con el programa.",
    "S11":"El usuario revisa el resumen de su inscripción antes de confirmar.",
    "S12":"El formulario detecta campos incompletos o con errores de validación.",
    "S13":"El usuario corrige los campos marcados con error en el formulario.",
    "S14":"El usuario explora la página de donaciones y apoyo a la fundación.",
    "S15":"El usuario lee o ve testimonios de emprendedores egresados del programa.",
    "S16":"El usuario revisa la sección de misión y programas de la fundación.",
    "S17":"El usuario consulta la historia y origen de Colombia Comparte.",
    "S18":"El usuario explora la sección de mentores y voluntarios del programa.",
    "S19":"El usuario navega por los módulos y contenidos del Programa EDIFICA.",
    "S20":"El usuario descarga el brochure o material informativo del programa.",
    "S21":"El usuario abandona el sitio para navegar por las redes sociales externas.",
    "S22":"El usuario consulta la sección de preguntas frecuentes (FAQ).",
    "S23":"El usuario inicia un chat de soporte o contacta por WhatsApp.",
    "S24":"El usuario revisa la sección de organizaciones y empresas aliadas.",
    "S25":"El usuario reproduce un video testimonial de la plataforma.",
    "S26":"El usuario encuentra un error técnico o página no disponible.",
    "S27":"La sesión del usuario queda inactiva por un periodo prolongado.",
    "S28":"El usuario retoma la navegación después de un periodo de inactividad.",
    "S29":"El usuario consulta los costos, modalidades y becas del programa.",
    "S30":"El usuario completa exitosamente el formulario de inscripción al programa.",
    "S31":"El usuario abandona voluntariamente el proceso antes de completarlo.",
    "S32":"El usuario abandona el proceso debido a un error técnico irrecuperable.",
}

TIPOS = {"S0":"Inicial","S30":"Final exitoso","S31":"Final negativo","S32":"Error técnico"}
for s in ESTADOS:
    if s not in TIPOS:
        TIPOS[s] = "Intermedio"

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
    ["S0","S2","S23","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S1","S4","S31"],
    ["S0","S4","S21","S31"],
    ["S0","S3","S25","S21","S31"],
    ["S0","S1","S17","S31"],
    ["S0","S4","S31"],
    ["S0","S3","S31"],
    ["S0","S1","S16","S4","S31"],
    ["S0","S14","S31"],
    ["S0","S21","S31"],
    ["S0","S5","S31"],
    ["S0","S3","S25","S31"],
    ["S0","S4","S3","S31"],
    ["S0","S1","S18","S31"],
    ["S0","S1","S4","S3","S31"],
    ["S0","S16","S4","S31"],
    ["S0","S2","S31"],
    ["S0","S2","S15","S31"],
    ["S0","S2","S19","S31"],
    ["S0","S2","S29","S31"],
    ["S0","S2","S19","S22","S31"],
    ["S0","S2","S7","S31"],
    ["S0","S2","S7","S8","S31"],
    ["S0","S2","S7","S8","S9","S31"],
    ["S0","S2","S7","S8","S9","S10","S31"],
    ["S0","S2","S29","S7","S8","S31"],
    ["S0","S26","S32"],
    ["S0","S2","S7","S26","S32"],
    ["S0","S2","S7","S8","S26","S32"],
    ["S0","S5","S26","S32"],
    ["S0","S2","S7","S8","S9","S26","S32"],
    ["S0","S26","S28","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S7","S26","S28","S8","S9","S10","S11","S30"],
    ["S0","S27","S28","S2","S7","S8","S31"],
    ["S0","S27","S28","S2","S7","S8","S9","S10","S11","S30"],
    ["S0","S2","S12","S13","S12","S32"],
    ["S0","S1","S24","S18","S6","S30"],
    ["S0","S24","S6","S30"],
    ["S0","S1","S18","S6","S30"],
    ["S0","S24","S18","S6","S31"],
    ["S0","S6","S30"],
    ["S0","S1","S24","S6","S31"],
    ["S0","S24","S21","S31"],
    ["S0","S18","S6","S30"],
    ["S0","S2","S19","S4","S15","S2","S29","S7","S8","S9","S10","S11","S30"],
    ["S0","S1","S17","S2","S19","S29","S7","S8","S12","S13","S9","S10","S11","S30"],
    ["S0","S2","S19","S22","S2","S7","S8","S9","S10","S27","S28","S11","S30"],
    ["S0","S4","S15","S2","S29","S7","S31"],
    ["S0","S1","S2","S19","S4","S25","S2","S7","S8","S9","S10","S11","S31"],
    ["S0","S15","S17","S2","S7","S8","S9","S10","S27","S28","S11","S30"],
    ["S0","S22","S2","S29","S7","S8","S9","S10","S12","S13","S11","S30"],
    ["S0","S2","S20","S7","S8","S9","S10","S11","S30"],
]

PERFILES = {
    tuple(r): (
        "A – Emprendedor motivado"  if r[-1]=="S30" and "S21" not in r and len(r)>=8
        else "D – Mentor / Aliado"  if "S24" in r or ("S6" in r and "S7" not in r)
        else "C – Usuario con errores" if "S26" in r or "S27" in r or ("S12" in r and r[-1]!="S30")
        else "E – Usuario indeciso"  if len(r)>=10
        else "B – Visitante curioso"
    )
    for r in [tuple(x) for x in RECORRIDOS]
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DEL MODELO
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def construir_matrices(recorridos, estados, estados_finales):
    idx = {s: i for i, s in enumerate(estados)}
    conteos = pd.DataFrame(0, index=estados, columns=estados)
    for r in recorridos:
        for i in range(len(r) - 1):
            o, d = r[i], r[i+1]
            if o not in estados_finales and o in idx and d in idx:
                conteos.loc[o, d] += 1
    probs = conteos.div(conteos.sum(axis=1).replace(0, np.nan), axis=0).fillna(0)
    for ef in estados_finales:
        if ef in probs.index:
            probs.loc[ef] = 0.0
            if ef in probs.columns:
                probs.loc[ef, ef] = 1.0
    return conteos, probs

def simular_usuario(matriz_prob, estado_inicial, estados_finales, max_pasos):
    estado = estado_inicial
    historial = [estado]
    for _ in range(max_pasos):
        if estado in estados_finales:
            break
        if estado not in matriz_prob.index:
            break
        probs = matriz_prob.loc[estado]
        if probs.sum() == 0:
            break
        estado = np.random.choice(matriz_prob.columns.tolist(), p=probs.values)
        historial.append(estado)
    return historial

def simular_n(n, matriz_prob, estado_inicial, estados_finales, max_pasos):
    rows = []
    for i in range(n):
        h = simular_usuario(matriz_prob, estado_inicial, estados_finales, max_pasos)
        ef = h[-1]
        resultado = (
            "Éxito ✅"   if ef == ESTADO_EXITO   else
            "Error ⚠️"   if ef == ESTADO_ERROR   else
            "Abandono ❌"
        )
        rows.append({
            "Usuario":             f"Usuario {i+1:04d}",
            "Recorrido":           " → ".join(h),
            "Recorrido (nombres)": " → ".join(NOMBRES.get(e, e) for e in h),
            "Estado final":        ef,
            "Resultado":           resultado,
            "Pasos":               len(h) - 1,
        })
    return pd.DataFrame(rows)

def estado_critico(df_sim):
    abnd = df_sim[df_sim["Estado final"] == ESTADO_ABANDONO]["Recorrido"]
    previos = []
    for r in abnd:
        pasos = [p.strip() for p in r.split("→")]
        if len(pasos) >= 2:
            previos.append(pasos[-2])
    if not previos:
        return None, 0
    c = Counter(previos)
    ec, n = c.most_common(1)[0]
    return ec, n

def matriz_mejorada_fn(matriz_prob, ec, reduccion=0.20):
    m = matriz_prob.copy()
    if ec not in m.index or ESTADO_ABANDONO not in m.columns:
        return m
    prob_actual = m.loc[ec, ESTADO_ABANDONO]
    red_real = min(reduccion, prob_actual)
    if red_real <= 0:
        return m
    m.loc[ec, ESTADO_ABANDONO] -= red_real
    otros  = m.loc[ec].drop(ESTADO_ABANDONO)
    validos = otros[otros > 0].index.tolist()
    if not validos:
        if ESTADO_EXITO in m.columns:
            m.loc[ec, ESTADO_EXITO] += red_real
    else:
        suma = m.loc[ec, validos].sum()
        for d in validos:
            m.loc[ec, d] += red_real * (m.loc[ec, d] / suma)
    s = m.loc[ec].sum()
    if s > 0:
        m.loc[ec] /= s
    return m

def recomendacion_edifica(ec, matriz_prob):
    nombre  = NOMBRES.get(ec, ec)
    desc    = DESCRIPCIONES.get(ec, "")
    prob_ab = matriz_prob.loc[ec, ESTADO_ABANDONO] if ec in matriz_prob.index else 0
    texto   = f"{nombre} {desc}".lower()
    if "red" in texto or "social" in texto:
        causa  = "Los enlaces a redes sociales redirigen al usuario fuera del sitio sin posibilidad de retorno."
        mejora = "Modificar los enlaces para que abran en nueva pestaña, manteniendo al usuario dentro del flujo."
        accion = "Reducir P(S21→S31) de 1.0 a ~0.3 e introducir transiciones de retorno hacia S0 y S2."
        kpi    = "Tasa de retorno desde redes sociales al flujo principal."
    elif "formulario" in texto or "datos" in texto or "campo" in texto:
        causa  = "Los formularios largos o poco claros generan fricción y aumentan la probabilidad de abandono."
        mejora = "Simplificar el formulario reduciendo campos obligatorios y añadir guardado automático."
        accion = "Reducir P(S8→S31) aumentando P(S8→S9) en la matriz de transición."
        kpi    = "Tasa de completitud del formulario de inscripción."
    elif "noticia" in texto or "actualidad" in texto:
        causa  = "Los usuarios que consumen contenido editorial no encuentran un camino claro hacia la inscripción."
        mejora = "Agregar llamadas a la acción visibles ('Inscríbete a EDIFICA') en las páginas de noticias."
        accion = "Reducir P(S4→S31) e incrementar P(S4→S2) y P(S4→S7)."
        kpi    = "Tasa de navegación de Noticias hacia el Programa EDIFICA."
    elif "speaker" in texto or "confer" in texto or "video" in texto:
        causa  = "El contenido de conferencias no conecta directamente con el proceso de inscripción."
        mejora = "Incluir un botón de inscripción prominente debajo de cada video o sección de speakers."
        accion = "Reducir P(S3→S31) e incrementar P(S3→S2)."
        kpi    = "Conversión desde sección de conferencias hacia inscripción."
    else:
        causa  = "El usuario encuentra fricción o falta de claridad en este punto del recorrido."
        mejora = "Revisar el contenido del estado, mejorar la jerarquía visual y agregar una llamada a la acción clara."
        accion = f"Reducir la probabilidad de abandono desde {ec} y redistribuirla hacia estados del flujo."
        kpi    = f"Tasa de avance desde {ec} hacia estados del formulario."
    return {"estado": ec, "nombre": nombre, "descripcion": desc,
            "prob_abandono": prob_ab,
            "causa": causa, "mejora": mejora, "accion": accion, "kpi": kpi}

# ══════════════════════════════════════════════════════════════════════════════
# DATAFRAMES BASE
# ══════════════════════════════════════════════════════════════════════════════
matriz_conteos, matriz_prob = construir_matrices(RECORRIDOS, ESTADOS, ESTADOS_FINALES)

df_estados = pd.DataFrame({
    "Código":      ESTADOS,
    "Nombre":      [NOMBRES[e] for e in ESTADOS],
    "Descripción": [DESCRIPCIONES[e] for e in ESTADOS],
    "Tipo":        [TIPOS[e] for e in ESTADOS],
})

df_recorridos_base = pd.DataFrame({
    "ID":                  [f"R{i+1:02d}" for i in range(len(RECORRIDOS))],
    "Perfil":              [PERFILES.get(tuple(r), "—") for r in RECORRIDOS],
    "Recorrido":           [" → ".join(r) for r in RECORRIDOS],
    "Recorrido (nombres)": [" → ".join(NOMBRES.get(e, e) for e in r) for r in RECORRIDOS],
    "Estado final":        [r[-1] for r in RECORRIDOS],
    "Resultado":           [
        "Éxito ✅" if r[-1]==ESTADO_EXITO else
        "Error ⚠️" if r[-1]==ESTADO_ERROR else "Abandono ❌"
        for r in RECORRIDOS
    ],
    "Pasos": [len(r)-1 for r in RECORRIDOS],
})

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h2 style='text-align:center;color:white;'>🤝 COLOMBIA COMPARTE</h2>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#A0C4FF;'>Programa EDIFICA</p>",
                unsafe_allow_html=True)
    st.markdown("### ⚙️ Parámetros de Simulación")

    n_usuarios = st.slider("Número de usuarios", 100, 5000, 1000, 100,
                           help="Usuarios que la cadena de Márkov simulará.")
    max_pasos  = st.slider("Máximo de pasos",    5,   60,   25,  5,
                           help="Límite de transiciones por recorrido.")
    estado_inicial_sel = st.selectbox(
        "Estado inicial", options=ESTADOS, index=0,
        format_func=lambda x: f"{x} – {NOMBRES.get(x, x)}"
    )
    st.markdown("---")
    st.success(f"✅ {ESTADO_EXITO} – {NOMBRES[ESTADO_EXITO]}")
    st.error(f"❌ {ESTADO_ABANDONO} – {NOMBRES[ESTADO_ABANDONO]}")
    st.warning(f"⚠️ {ESTADO_ERROR} – {NOMBRES[ESTADO_ERROR]}")
    st.markdown("---")

    if st.button("🔄 Reiniciar Simulación", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown(
        "<div style='font-size:0.74rem;color:#7bb8d8;line-height:1.6;'>"
        "📚 <b>Universidad Santo Tomás</b><br>Seccional Tunja · 2026</div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>Simulación Markov — EDIFICA</h1>
  <p>Análisis del flujo de inscripción al Programa EDIFICA · 33 estados · 66 recorridos base · Cadenas de Márkov</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIMULACIÓN INICIAL (session state)
# ══════════════════════════════════════════════════════════════════════════════
if "df_sim" not in st.session_state:
    st.session_state["df_sim"] = simular_n(
        n_usuarios, matriz_prob, estado_inicial_sel, ESTADOS_FINALES, max_pasos
    )

df_sim      = st.session_state["df_sim"]
ec_actual, ec_n = estado_critico(df_sim)
pct_exito   = (df_sim["Estado final"] == ESTADO_EXITO).mean()   * 100
pct_abnd    = (df_sim["Estado final"] == ESTADO_ABANDONO).mean()* 100
pct_err     = (df_sim["Estado final"] == ESTADO_ERROR).mean()   * 100
prom_pasos  = df_sim["Pasos"].mean()

# ══════════════════════════════════════════════════════════════════════════════
# PESTAÑAS  (estructura Simulacion Desing)
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["▶️ Simulación", "🗂️ Estados y Transiciones", "📊 Análisis"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · SIMULACIÓN
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("▶️ Ejecutar Simulación", type="primary", use_container_width=True):
            with st.spinner("Ejecutando simulación con cadenas de Márkov..."):
                st.session_state["df_sim"] = simular_n(
                    n_usuarios, matriz_prob, estado_inicial_sel, ESTADOS_FINALES, max_pasos
                )
                for k in ["df_sim_mejor", "rec_obj", "matriz_mejor"]:
                    st.session_state.pop(k, None)
            st.success(f"✅ Simulación completada: {n_usuarios:,} usuarios generados.")
            st.balloons()
            df_sim     = st.session_state["df_sim"]
            ec_actual, ec_n = estado_critico(df_sim)
            pct_exito  = (df_sim["Estado final"]==ESTADO_EXITO).mean()*100
            pct_abnd   = (df_sim["Estado final"]==ESTADO_ABANDONO).mean()*100
            pct_err    = (df_sim["Estado final"]==ESTADO_ERROR).mean()*100
            prom_pasos = df_sim["Pasos"].mean()

        st.markdown("<br>", unsafe_allow_html=True)

        # KPIs
        for icon, label, val, detail in [
            ("✅","Tasa de éxito",    f"{pct_exito:.1f}%",  f"{int(pct_exito*len(df_sim)/100)} usuarios"),
            ("❌","Tasa de abandono", f"{pct_abnd:.1f}%",   f"{int(pct_abnd*len(df_sim)/100)} usuarios"),
            ("⚠️","Error técnico",   f"{pct_err:.1f}%",    f"{int(pct_err*len(df_sim)/100)} usuarios"),
            ("📏","Promedio pasos",  f"{prom_pasos:.1f}",  "por usuario simulado"),
            ("🚨","Estado crítico",  ec_actual or "—",
             NOMBRES.get(ec_actual,"Sin datos")[:30] if ec_actual else "Sin datos"),
        ]:
            st.markdown(f"""
            <div class="kpi-box">
              <div class="kpi-label">{icon} {label}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-detail">{detail}</div>
            </div><br>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 👁️ Vista previa — primeros 20 usuarios simulados")
        df_prev = st.session_state["df_sim"].head(20)[["Usuario","Resultado","Pasos","Recorrido"]]
        st.dataframe(df_prev, use_container_width=True, hide_index=True,
                     column_config={"Recorrido": st.column_config.TextColumn("Recorrido", width=380)})

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · ESTADOS Y TRANSICIONES
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🗂️ Estados del modelo")
    st.caption("33 pantallas y acciones posibles dentro de la plataforma Colombia Comparte.")

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        busqueda = st.text_input("🔍 Buscar estado", placeholder="Ej: S7 o formulario")
    with col_f2:
        filtro_tipo = st.multiselect("Tipo", options=df_estados["Tipo"].unique().tolist(),
                                     default=df_estados["Tipo"].unique().tolist())

    df_ef = df_estados[df_estados["Tipo"].isin(filtro_tipo)]
    if busqueda:
        mask = (df_ef["Código"].str.contains(busqueda, case=False) |
                df_ef["Nombre"].str.contains(busqueda, case=False) |
                df_ef["Descripción"].str.contains(busqueda, case=False))
        df_ef = df_ef[mask]

    st.dataframe(df_ef, use_container_width=True, hide_index=True,
                 column_config={
                     "Código":      st.column_config.TextColumn("Código",  width=80),
                     "Nombre":      st.column_config.TextColumn("Nombre",  width=220),
                     "Descripción": st.column_config.TextColumn("Descripción", width=400),
                     "Tipo":        st.column_config.TextColumn("Tipo",    width=130),
                 })
    st.caption(f"Mostrando {len(df_ef)} de {len(df_estados)} estados.")

    st.markdown("---")
    st.markdown("### 🔀 Recorridos base")
    st.caption("66 caminos realistas construidos a partir de 5 perfiles de usuario.")

    fc1, fc2 = st.columns(2)
    with fc1:
        f_res = st.multiselect("Resultado", options=df_recorridos_base["Resultado"].unique().tolist(),
                               default=df_recorridos_base["Resultado"].unique().tolist())
    with fc2:
        f_prf = st.multiselect("Perfil",    options=df_recorridos_base["Perfil"].unique().tolist(),
                               default=df_recorridos_base["Perfil"].unique().tolist())

    df_rf = df_recorridos_base[
        df_recorridos_base["Resultado"].isin(f_res) &
        df_recorridos_base["Perfil"].isin(f_prf)
    ]
    st.dataframe(df_rf[["ID","Perfil","Recorrido","Resultado","Pasos"]],
                 use_container_width=True, hide_index=True)
    st.caption(f"Mostrando {len(df_rf)} de {len(RECORRIDOS)} recorridos.")

    st.markdown("---")
    st.markdown("### 📐 Matrices de transición")
    tipo_mat = st.radio("Ver", ["📊 Conteos", "🎯 Probabilidades"], horizontal=True)
    activos  = [s for s in ESTADOS if matriz_conteos.loc[s].sum()>0 or matriz_conteos[s].sum()>0]

    if tipo_mat == "📊 Conteos":
        st.dataframe(matriz_conteos.loc[activos, activos], use_container_width=True)
    else:
        st.dataframe(matriz_prob.loc[activos, activos].round(4), use_container_width=True)

    st.markdown("#### 🌡️ Mapa de calor (estados principales)")
    core = ["S0","S2","S7","S8","S9","S10","S11","S15","S19","S21","S22","S29","S30","S31","S32"]
    sub  = matriz_prob.loc[core, core]
    fig_hm, ax_hm = plt.subplots(figsize=(10, 5))
    fig_hm.patch.set_facecolor('#01182E'); ax_hm.set_facecolor('#01182E')
    im = ax_hm.imshow(sub.values, cmap='Blues', aspect='auto', vmin=0, vmax=1)
    ax_hm.set_xticks(range(len(core))); ax_hm.set_yticks(range(len(core)))
    ax_hm.set_xticklabels(core, rotation=45, ha='right', color='white', fontsize=8)
    ax_hm.set_yticklabels(core, color='white', fontsize=8)
    for i in range(len(core)):
        for j in range(len(core)):
            v = sub.values[i, j]
            if v > 0.05:
                ax_hm.text(j, i, f"{v:.2f}", ha='center', va='center',
                           fontsize=7, color='white' if v > 0.5 else '#001A3A', fontweight='bold')
    cbar = fig_hm.colorbar(im, ax=ax_hm)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white', fontsize=8)
    ax_hm.set_title("Matriz de probabilidades", color='white', fontsize=10, pad=8)
    plt.tight_layout()
    st.pyplot(fig_hm)
    plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · ANÁLISIS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    df_sim = st.session_state["df_sim"]
    pct_e  = (df_sim["Estado final"]==ESTADO_EXITO).mean()*100
    pct_a  = (df_sim["Estado final"]==ESTADO_ABANDONO).mean()*100
    pct_er = (df_sim["Estado final"]==ESTADO_ERROR).mean()*100
    prom   = df_sim["Pasos"].mean()
    prom_e = df_sim[df_sim["Estado final"]==ESTADO_EXITO]["Pasos"].mean()
    prom_a = df_sim[df_sim["Estado final"]==ESTADO_ABANDONO]["Pasos"].mean()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("✅ Éxito",          f"{pct_e:.1f}%",  f"{int(pct_e*len(df_sim)/100)} usuarios")
    m2.metric("❌ Abandono",       f"{pct_a:.1f}%",  f"{int(pct_a*len(df_sim)/100)} usuarios")
    m3.metric("⚠️ Error técnico",  f"{pct_er:.1f}%", f"{int(pct_er*len(df_sim)/100)} usuarios")
    m4.metric("📏 Promedio pasos", f"{prom:.2f}",    f"Éxito:{prom_e:.1f} | Abandono:{prom_a:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)
    gr1, gr2 = st.columns(2)

    with gr1:
        st.markdown("#### 📊 Distribución de resultados")
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        fig1.patch.set_facecolor('#01182E'); ax1.set_facecolor('#01182E')
        vals = [int(pct_e*len(df_sim)/100), int(pct_a*len(df_sim)/100), int(pct_er*len(df_sim)/100)]
        etiq = [f"Éxito\n{pct_e:.1f}%", f"Abandono\n{pct_a:.1f}%", f"Error\n{pct_er:.1f}%"]
        ax1.pie(vals, labels=etiq, colors=["#1E7E34","#C0392B","#D4780A"],
                startangle=140,
                wedgeprops=dict(edgecolor='#01182E', linewidth=2),
                textprops=dict(color='white', fontsize=10, fontweight='bold'))
        ax1.set_title(f"{len(df_sim):,} usuarios simulados", color='white', fontsize=10)
        plt.tight_layout(); st.pyplot(fig1); plt.close()

    with gr2:
        st.markdown("#### 📏 Pasos promedio por resultado")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        fig2.patch.set_facecolor('#01182E'); ax2.set_facecolor('#01182E')
        grupos = df_sim.groupby("Estado final")["Pasos"].mean()
        etiq2, vals2, cols2 = [], [], []
        for ef, col, lab in [(ESTADO_EXITO,"#1E7E34","Éxito"),
                             (ESTADO_ABANDONO,"#C0392B","Abandono"),
                             (ESTADO_ERROR,"#D4780A","Error")]:
            if ef in grupos:
                etiq2.append(lab); vals2.append(grupos[ef]); cols2.append(col)
        bars2 = ax2.bar(etiq2, vals2, color=cols2, edgecolor='#01182E', width=0.5)
        for b, v in zip(bars2, vals2):
            ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.1,
                     f"{v:.1f}", ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')
        ax2.set_ylabel("Pasos promedio", color='white')
        ax2.set_title("Profundidad del recorrido", color='white', fontsize=10)
        ax2.tick_params(colors='white'); ax2.spines[:].set_visible(False)
        ax2.set_ylim(0, max(vals2)*1.3 if vals2 else 10)
        plt.tight_layout(); st.pyplot(fig2); plt.close()

    # Top estados de abandono
    st.markdown("#### 🚨 Top estados previos al abandono")
    df_abn = df_sim[df_sim["Estado final"]==ESTADO_ABANDONO]["Recorrido"]
    previos_all = []
    for r in df_abn:
        pasos_ = [p.strip() for p in r.split("→")]
        if len(pasos_) >= 2:
            previos_all.append(pasos_[-2])
    if previos_all:
        top8    = Counter(previos_all).most_common(8)
        top_lbl = [f"{k} – {NOMBRES.get(k,'')[:20]}" for k,_ in top8]
        top_val = [v for _,v in top8]
        fig3, ax3 = plt.subplots(figsize=(9, 3.5))
        fig3.patch.set_facecolor('#01182E'); ax3.set_facecolor('#01182E')
        cols3 = ["#C0392B" if i==0 else "#2E6DB4" for i in range(len(top8))]
        bars3 = ax3.barh(top_lbl[::-1], top_val[::-1], color=cols3[::-1], height=0.6)
        for b, v in zip(bars3, top_val[::-1]):
            ax3.text(b.get_width()+0.3, b.get_y()+b.get_height()/2,
                     str(v), va='center', color='white', fontsize=9, fontweight='bold')
        ax3.set_xlabel("Abandonos", color='white')
        ax3.tick_params(colors='white', labelsize=8); ax3.spines[:].set_visible(False)
        ax3.set_title("Estado previo al abandono (top 8)", color='white', fontsize=10)
        plt.tight_layout(); st.pyplot(fig3); plt.close()
    else:
        st.info("No se registraron abandonos en esta simulación.")

    # Rutas más frecuentes
    st.markdown("#### 🔁 Recorridos más frecuentes")
    rf = df_sim["Recorrido"].value_counts().head(8).reset_index()
    rf.columns = ["Recorrido","Frecuencia"]
    st.dataframe(rf, use_container_width=True, hide_index=True)

    # ── Diagnóstico ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔧 Diagnóstico y mejora del abandono")
    ec_d, ec_n_d = estado_critico(df_sim)

    if ec_d is None:
        st.success("No se detectaron abandonos en la simulación actual.")
    else:
        total_abnd     = (df_sim["Estado final"]==ESTADO_ABANDONO).sum()
        pct_s_abnd     = ec_n_d/total_abnd*100 if total_abnd>0 else 0
        pct_s_total    = ec_n_d/len(df_sim)*100

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("🚨 Estado crítico",        ec_d)
        d2.metric("📌 Nombre",                NOMBRES.get(ec_d,"—"))
        d3.metric("❌ Abandonos asociados",    ec_n_d)
        d4.metric("% sobre abandonos totales", f"{pct_s_abnd:.1f}%")

        st.markdown(f"""
        <div class="diag-box">
          <b>🔎 Diagnóstico principal</b><br><br>
          El estado más crítico es <b>{ec_d} – {NOMBRES.get(ec_d,'')}</b>.<br>
          <b>Descripción:</b> {DESCRIPCIONES.get(ec_d,'')}<br><br>
          De los <b>{total_abnd}</b> usuarios que abandonaron, el <b>{pct_s_abnd:.1f}%</b>
          ({ec_n_d} usuarios) lo hizo inmediatamente después de pasar por este estado.
          Representa el <b>{pct_s_total:.1f}%</b> del total simulado.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔧 Generar recomendación ejecutiva", use_container_width=True):
            st.session_state["rec_obj"] = recomendacion_edifica(ec_d, matriz_prob)

        if "rec_obj" in st.session_state:
            rec = st.session_state["rec_obj"]
            st.markdown(f"""
            <div class="rec-box">
              <h4>📋 Propuesta de intervención — {rec['estado']} · {rec['nombre']}</h4>
              <b>Probabilidad directa de abandono:</b> {rec['prob_abandono']:.2%}<br><br>
              <b>🔍 Causa:</b> {rec['causa']}<br><br>
              <b>🛠️ Mejora recomendada:</b> {rec['mejora']}<br><br>
              <b>📐 Ajuste en la matriz:</b> {rec['accion']}<br><br>
              <b>📈 KPI de validación:</b> {rec['kpi']}
            </div>
            """, unsafe_allow_html=True)

        # Escenario mejorado
        st.markdown("---")
        st.markdown("#### 📈 Escenario mejorado")
        reduccion = st.slider("Reducción de P(abandono) desde el estado crítico",
                              0.05, 0.60, 0.20, 0.05, format="%.2f")

        if st.button("🚀 Simular escenario mejorado", use_container_width=True):
            with st.spinner("Construyendo escenario mejorado..."):
                mat_m = matriz_mejorada_fn(matriz_prob, ec_d, reduccion)
                df_m  = simular_n(n_usuarios, mat_m, estado_inicial_sel, ESTADOS_FINALES, max_pasos)
                st.session_state["df_sim_mejor"] = df_m
            st.success("✅ Escenario mejorado generado correctamente.")

        if "df_sim_mejor" in st.session_state:
            st.markdown("#### ⚖️ Comparación: inicial vs mejorado")
            df_m    = st.session_state["df_sim_mejor"]
            pct_ini = df_sim["Resultado"].value_counts(normalize=True)*100
            pct_mej = df_m["Resultado"].value_counts(normalize=True)*100
            todos   = sorted(set(pct_ini.index)|set(pct_mej.index))
            df_comp = pd.DataFrame({
                "Resultado":    todos,
                "Inicial (%)":  [round(pct_ini.get(r,0),2) for r in todos],
                "Mejorado (%)": [round(pct_mej.get(r,0),2) for r in todos],
                "Δ (pp)":       [round(pct_mej.get(r,0)-pct_ini.get(r,0),2) for r in todos],
            })
            st.dataframe(df_comp, use_container_width=True, hide_index=True)

            fig_c, ax_c = plt.subplots(figsize=(8, 3.5))
            fig_c.patch.set_facecolor('#01182E'); ax_c.set_facecolor('#01182E')
            x = np.arange(len(todos)); w = 0.35
            b1 = ax_c.bar(x-w/2, df_comp["Inicial (%)"],  w, label="Inicial",  color="#2E6DB4")
            b2 = ax_c.bar(x+w/2, df_comp["Mejorado (%)"], w, label="Mejorado", color="#4AACE8")
            for b in list(b1)+list(b2):
                ax_c.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
                          f"{b.get_height():.1f}%", ha='center', va='bottom',
                          color='white', fontsize=8, fontweight='bold')
            ax_c.set_xticks(x); ax_c.set_xticklabels(todos, color='white', fontsize=9)
            ax_c.set_ylabel("Porcentaje (%)", color='white')
            ax_c.tick_params(colors='white'); ax_c.spines[:].set_visible(False)
            ax_c.legend(facecolor='#01182E', labelcolor='white', fontsize=8)
            ax_c.set_title("Escenario inicial vs mejorado", color='white', fontsize=10)
            plt.tight_layout(); st.pyplot(fig_c); plt.close()
            st.info("Esta comparación permite validar si la mejora propuesta reduce el abandono e incrementa el éxito.")

# ══════════════════════════════════════════════════════════════════════════════
# ACCIONES RÁPIDAS  (diseño Simulacion Desing — datos reales)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### ⚡ Acciones Rápidas")
ac1, ac2, ac3, ac4 = st.columns(4)

with ac1:
    if st.button("📥 Exportar a Excel", use_container_width=True):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state["df_sim"].to_excel(writer, index=False, sheet_name="Simulación")
            df_estados.to_excel(writer, index=False, sheet_name="Estados")
            df_recorridos_base.to_excel(writer, index=False, sheet_name="Recorridos")
        output.seek(0)
        st.download_button("⬇️ Descargar Excel", data=output,
                           file_name="simulacion_colombia_comparte.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with ac2:
    if st.button("📄 Exportar a CSV", use_container_width=True):
        csv = st.session_state["df_sim"].to_csv(index=False)
        st.download_button("⬇️ Descargar CSV", data=csv,
                           file_name="simulacion_colombia_comparte.csv",
                           mime="text/csv")

with ac3:
    if st.button("♿ Modo Accesibilidad", use_container_width=True):
        st.success("Modo alto contraste activado.")

with ac4:
    if st.button("🔗 Compartir Resultados", use_container_width=True):
        st.success("Enlace copiado al portapapeles (simulado).")

st.caption("Dashboard Colombia Comparte · Universidad Santo Tomás · Seccional Tunja · 2026")
