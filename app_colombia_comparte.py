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

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Colombia Comparte · Simulación EDIFICA",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# IMAGEN DE FONDO (incrustada en base64)
# ══════════════════════════════════════════════════════════════════════════════
def get_bg_base64() -> str:
    """Generate background image on-the-fly and return as base64."""
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

@st.cache_data
def get_bg():
    return get_bg_base64()

BG_B64 = get_bg()

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Paleta Colombia Comparte ── */
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

/* ── Fondo principal ── */
[data-testid="stAppViewContainer"] > .main {{
  background-image: url("data:image/png;base64,{BG_B64}");
  background-size: cover;
  background-position: center top;
  background-attachment: fixed;
}}

/* ── Overlay semitransparente sobre el fondo ── */
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

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #01478D 0%, #012F65 60%, #011D42 100%) !important;
  border-right: 1px solid rgba(74,172,232,0.25);
}}
[data-testid="stSidebar"] * {{ color: #e8f4fd !important; }}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {{
  color: #a8d4f0 !important;
  font-weight: 600;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
[data-testid="stSidebar"] hr {{ border-color: rgba(74,172,232,0.3) !important; }}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {{
  background-color: #4AACE8 !important;
}}

/* ── Hero banner ── */
.hero {{
  background: linear-gradient(135deg,
    rgba(1,71,141,0.95) 0%,
    rgba(46,109,180,0.90) 50%,
    rgba(74,172,232,0.85) 100%);
  border: 1px solid rgba(74,172,232,0.45);
  border-radius: 22px;
  padding: 32px 40px 28px 40px;
  margin-bottom: 22px;
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.12);
}}
.hero-title {{
  font-size: 2.5rem;
  font-weight: 900;
  color: #FFFFFF;
  letter-spacing: -0.03em;
  margin: 0 0 4px 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
.hero-sub {{
  font-size: 1rem;
  color: #a8d4f0;
  margin: 0 0 10px 0;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}
.hero-desc {{
  font-size: 0.97rem;
  color: #daeef9;
  line-height: 1.6;
  max-width: 860px;
  margin: 0;
}}
.hero-badges {{
  display: flex;
  gap: 10px;
  margin-top: 16px;
  flex-wrap: wrap;
}}
.badge {{
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.22);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 0.78rem;
  color: #daeef9;
  font-weight: 600;
  letter-spacing: 0.04em;
}}

/* ── Tarjetas de métricas ── */
.kpi-card {{
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(74,172,232,0.35);
  border-radius: 18px;
  padding: 20px 18px 16px 18px;
  backdrop-filter: blur(10px);
  min-height: 118px;
  transition: transform 0.18s, box-shadow 0.18s;
}}
.kpi-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.28);
}}
.kpi-label {{
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #9fc8e8;
  font-weight: 700;
  margin-bottom: 8px;
}}
.kpi-value {{
  font-size: 2rem;
  font-weight: 900;
  color: #FFFFFF;
  line-height: 1.1;
  margin-bottom: 4px;
}}
.kpi-detail {{
  font-size: 0.75rem;
  color: #7bb8d8;
  line-height: 1.4;
}}
.kpi-icon {{ font-size: 1.3rem; margin-bottom: 6px; }}

/* ── Panel de contenido ── */
.cc-panel {{
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(74,172,232,0.28);
  border-radius: 18px;
  padding: 24px 26px;
  backdrop-filter: blur(10px);
  margin-bottom: 18px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.20);
}}
.cc-panel-dark {{
  background: linear-gradient(135deg,
    rgba(1,47,101,0.92) 0%,
    rgba(1,30,66,0.90) 100%);
  border: 1px solid rgba(74,172,232,0.32);
  border-radius: 18px;
  padding: 24px 26px;
  backdrop-filter: blur(12px);
  margin-bottom: 18px;
}}

/* ── Section titles ── */
.sec-title {{
  font-size: 1.45rem;
  font-weight: 800;
  color: #FFFFFF;
  margin-bottom: 4px;
  letter-spacing: -0.02em;
}}
.sec-sub {{
  font-size: 0.87rem;
  color: #8bbbd8;
  margin-bottom: 18px;
  line-height: 1.55;
}}

/* ── Status cards ── */
.status-success {{
  background: rgba(30,126,52,0.18);
  border: 1px solid rgba(30,126,52,0.45);
  border-radius: 14px;
  padding: 16px;
  color: #90EBA8;
  min-height: 100px;
}}
.status-warning {{
  background: rgba(212,120,10,0.18);
  border: 1px solid rgba(212,120,10,0.45);
  border-radius: 14px;
  padding: 16px;
  color: #FBBF72;
  min-height: 100px;
}}
.status-danger {{
  background: rgba(192,57,43,0.18);
  border: 1px solid rgba(192,57,43,0.45);
  border-radius: 14px;
  padding: 16px;
  color: #F4937A;
  min-height: 100px;
}}

/* ── Step boxes ── */
.step-box {{
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(74,172,232,0.28);
  border-radius: 16px;
  padding: 18px;
  min-height: 130px;
  backdrop-filter: blur(8px);
}}
.step-num {{
  font-size: 0.72rem;
  color: #4AACE8;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}}
.step-title {{ font-size: 1rem; color: #FFFFFF; font-weight: 800; margin-bottom: 6px; }}
.step-text  {{ font-size: 0.82rem; color: #8bbbd8; line-height: 1.5; }}

/* ── Diagnostic box ── */
.diag-box {{
  background: rgba(1,47,101,0.65);
  border-left: 5px solid #4AACE8;
  border-radius: 14px;
  padding: 20px 22px;
  color: #daeef9;
  margin: 14px 0 20px 0;
  line-height: 1.65;
}}
.rec-box {{
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(74,172,232,0.30);
  border-radius: 18px;
  padding: 24px;
  color: #e8f4fd;
  margin-top: 16px;
  line-height: 1.65;
  backdrop-filter: blur(8px);
}}
.rec-box h4 {{ color: #FFFFFF; margin-top: 0; font-size: 1.05rem; }}

/* ── Buttons ── */
div.stButton > button {{
  border-radius: 12px;
  background: linear-gradient(135deg, #01478D 0%, #2E6DB4 100%);
  border: 1px solid rgba(74,172,232,0.5);
  color: white;
  font-weight: 700;
  padding: 0.7rem 1.2rem;
  letter-spacing: 0.03em;
  transition: all 0.18s;
}}
div.stButton > button:hover {{
  background: linear-gradient(135deg, #2E6DB4 0%, #4AACE8 100%);
  border-color: #4AACE8;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74,172,232,0.3);
}}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
  background: rgba(1,47,101,0.55);
  border-radius: 14px;
  padding: 4px;
  gap: 2px;
  border: 1px solid rgba(74,172,232,0.2);
  backdrop-filter: blur(8px);
}}
.stTabs [data-baseweb="tab"] {{
  border-radius: 10px;
  color: #8bbbd8 !important;
  font-weight: 600;
  font-size: 0.83rem;
  padding: 8px 16px;
}}
.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, #01478D 0%, #2E6DB4 100%) !important;
  color: white !important;
}}

/* ── Metrics ── */
[data-testid="stMetric"] {{
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(74,172,232,0.28);
  padding: 14px;
  border-radius: 14px;
  backdrop-filter: blur(8px);
}}
[data-testid="stMetric"] label {{ color: #9fc8e8 !important; }}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: white !important; }}

/* ── Alerts & info boxes ── */
.stAlert {{ border-radius: 12px !important; backdrop-filter: blur(6px); }}
[data-testid="stInfo"] {{ background: rgba(74,172,232,0.12) !important; border-color: rgba(74,172,232,0.4) !important; }}
[data-testid="stSuccess"] {{ background: rgba(30,126,52,0.15) !important; border-color: rgba(30,126,52,0.4) !important; }}
[data-testid="stWarning"] {{ background: rgba(212,120,10,0.15) !important; border-color: rgba(212,120,10,0.4) !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: rgba(1,47,101,0.4); }}
::-webkit-scrollbar-thumb {{ background: rgba(74,172,232,0.5); border-radius: 3px; }}

/* ── Sidebar logo strip ── */
.sidebar-logo {{
  background: rgba(74,172,232,0.10);
  border: 1px solid rgba(74,172,232,0.25);
  border-radius: 14px;
  padding: 12px 14px;
  margin-bottom: 14px;
  text-align: center;
}}
.sidebar-logo-title {{
  font-size: 1.1rem;
  font-weight: 900;
  color: #FFFFFF !important;
  letter-spacing: 0.02em;
}}
.sidebar-logo-sub {{
  font-size: 0.72rem;
  color: #9fc8e8 !important;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 2px;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATOS DEL MODELO — COLOMBIA COMPARTE / PROGRAMA EDIFICA
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

TIPOS = {
    "S0": "Inicial",
    "S30": "Final exitoso",
    "S31": "Final negativo",
    "S32": "Error técnico",
}
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
        "A – Emprendedor motivado" if r[-1] == "S30" and "S21" not in r and len(r) >= 8
        else "D – Mentor / Aliado"  if "S24" in r or ("S6" in r and "S7" not in r)
        else "C – Usuario con errores" if "S26" in r or "S27" in r or ("S12" in r and r[-1]!="S30")
        else "E – Usuario indeciso" if len(r) >= 10
        else "B – Visitante curioso"
    )
    for r in [tuple(x) for x in RECORRIDOS]
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DEL MODELO
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def construir_matrices(recorridos, estados, estados_finales):
    n = len(estados)
    idx = {s: i for i, s in enumerate(estados)}
    conteos = pd.DataFrame(0, index=estados, columns=estados)
    for r in recorridos:
        for i in range(len(r) - 1):
            o, d = r[i], r[i+1]
            if o not in estados_finales and o in idx and d in idx:
                conteos.loc[o, d] += 1
    probs = conteos.div(conteos.sum(axis=1).replace(0, np.nan), axis=0).fillna(0)
    # estados finales: absorben con prob 1
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
            "Éxito ✅"    if ef == ESTADO_EXITO    else
            "Error ⚠️"    if ef == ESTADO_ERROR    else
            "Abandono ❌"
        )
        rows.append({
            "Usuario":            f"Usuario {i+1:04d}",
            "Recorrido":          " → ".join(h),
            "Recorrido (nombres)": " → ".join(NOMBRES.get(e, e) for e in h),
            "Estado final":       ef,
            "Resultado":          resultado,
            "Pasos":              len(h) - 1,
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
    otros = m.loc[ec].drop(ESTADO_ABANDONO)
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
    nombre = NOMBRES.get(ec, ec)
    desc   = DESCRIPCIONES.get(ec, "")
    prob_ab = matriz_prob.loc[ec, ESTADO_ABANDONO] if ec in matriz_prob.index else 0

    texto = f"{nombre} {desc}".lower()
    if "red" in texto or "social" in texto:
        causa  = "Los enlaces a redes sociales redirigen al usuario fuera del sitio sin posibilidad de retorno."
        mejora = "Modificar los enlaces a redes sociales para que abran en nueva pestaña, manteniendo al usuario dentro del flujo de inscripción."
        accion = "Reducir P(S21→S31) de 1.0 a ~0.3 e introducir transiciones de retorno hacia S0 y S2."
        kpi    = "Tasa de retorno desde redes sociales al flujo principal."
    elif "formulario" in texto or "datos" in texto or "campo" in texto:
        causa  = "Los formularios largos o poco claros generan fricción y aumentan la probabilidad de abandono."
        mejora = "Simplificar el formulario en S8 reduciendo campos obligatorios, añadir guardado automático y mensajes de ayuda contextual."
        accion = "Reducir P(S8→S31) aumentando P(S8→S9) en la matriz de transición."
        kpi    = "Tasa de completitud del formulario de inscripción."
    elif "noticia" in texto or "actualidad" in texto:
        causa  = "Los usuarios que consumen contenido editorial no encuentran un camino claro hacia la inscripción."
        mejora = "Agregar llamadas a la acción visibles ('Inscríbete a EDIFICA') en las páginas de noticias."
        accion = "Reducir P(S4→S31) e incrementar P(S4→S2) y P(S4→S7)."
        kpi    = "Tasa de navegación de Noticias hacia el Programa EDIFICA."
    elif "speaker" in texto or "confer" in texto or "video" in texto:
        causa  = "El contenido de conferencias o testimonios no conecta directamente con el proceso de inscripción."
        mejora = "Incluir un botón de inscripción prominente debajo de cada video o sección de speakers."
        accion = "Reducir P(S3→S31) e incrementar P(S3→S2)."
        kpi    = "Conversión desde sección de conferencias hacia inscripción."
    else:
        causa  = "El usuario encuentra fricción o falta de claridad en este punto del recorrido."
        mejora = "Revisar el contenido del estado, mejorar la jerarquía visual y agregar una llamada a la acción clara."
        accion = f"Reducir la probabilidad de abandono desde {ec} y redistribuirla hacia estados del flujo de inscripción."
        kpi    = f"Tasa de avance desde {ec} hacia estados del formulario."
    return {
        "estado": ec, "nombre": nombre, "descripcion": desc,
        "prob_abandono": prob_ab,
        "causa": causa, "mejora": mejora, "accion": accion, "kpi": kpi,
    }

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
        "Éxito ✅" if r[-1] == ESTADO_EXITO else
        "Error ⚠️" if r[-1] == ESTADO_ERROR else
        "Abandono ❌"
        for r in RECORRIDOS
    ],
    "Pasos": [len(r) - 1 for r in RECORRIDOS],
})

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-title">🤝 Colombia Comparte</div>
      <div class="sidebar-logo-sub">Simulación Programa EDIFICA</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Parámetros")

    n_usuarios = st.slider(
        "Usuarios a simular",
        min_value=100, max_value=5000, value=1000, step=100,
        help="Número de usuarios que la cadena de Márkov simulará."
    )

    max_pasos = st.slider(
        "Máximo de pasos por usuario",
        min_value=5, max_value=60, value=25, step=5,
        help="Límite de transiciones por recorrido simulado."
    )

    estado_inicial_sel = st.selectbox(
        "Estado inicial",
        options=ESTADOS,
        index=0,
        format_func=lambda x: f"{x} – {NOMBRES.get(x, x)}"
    )

    st.markdown("---")
    st.markdown("**Estados finales del modelo:**")
    st.success(f"✅ {ESTADO_EXITO} – {NOMBRES[ESTADO_EXITO]}")
    st.error(f"❌ {ESTADO_ABANDONO} – {NOMBRES[ESTADO_ABANDONO]}")
    st.warning(f"⚠️ {ESTADO_ERROR} – {NOMBRES[ESTADO_ERROR]}")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#7bb8d8; line-height:1.6;">
      📚 <b>Universidad Santo Tomás</b><br>
      Seccional Tunja<br>
      Simulación · 2026<br><br>
      Ajusta los parámetros y ejecuta la simulación en la pestaña <b>Simulación</b>.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-sub">🤝 Colombia Comparte · Programa EDIFICA</div>
  <div class="hero-title">Dashboard de Simulación</div>
  <div class="hero-desc">
    Modelo de Cadenas de Márkov aplicado al flujo de navegación y registro de usuarios
    en la plataforma de Colombia Comparte. Visualiza estados, matrices, recorridos,
    resultados y recomendaciones de mejora en tiempo real.
  </div>
  <div class="hero-badges">
    <span class="badge">📊 33 Estados</span>
    <span class="badge">🔀 66 Recorridos base</span>
    <span class="badge">🧮 Cadenas de Márkov</span>
    <span class="badge">🎓 Universidad Santo Tomás · Tunja</span>
    <span class="badge">🗓️ 2026</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIMULACIÓN INICIAL (session state)
# ══════════════════════════════════════════════════════════════════════════════
if "df_sim" not in st.session_state:
    st.session_state["df_sim"] = simular_n(
        n_usuarios, matriz_prob, estado_inicial_sel, ESTADOS_FINALES, max_pasos
    )

df_sim = st.session_state["df_sim"]
ec_actual, ec_n = estado_critico(df_sim)

conteo_res = df_sim["Resultado"].value_counts()
pct_exito   = (df_sim["Estado final"] == ESTADO_EXITO).mean()   * 100
pct_abnd    = (df_sim["Estado final"] == ESTADO_ABANDONO).mean()* 100
pct_err     = (df_sim["Estado final"] == ESTADO_ERROR).mean()   * 100
prom_pasos  = df_sim["Pasos"].mean()

res_frecuente = df_sim["Resultado"].value_counts().idxmax() if not df_sim.empty else "—"

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5, k6 = st.columns(6)

cards = [
    (k1, "🗂️", "Estados", f"{len(ESTADOS)}", "Nodos del modelo Márkov"),
    (k2, "🔀", "Recorridos base", f"{len(RECORRIDOS)}", "Caminos para la matriz"),
    (k3, "👥", "Usuarios simulados", f"{len(df_sim):,}", "Muestra generada"),
    (k4, "✅", "Tasa de éxito",  f"{pct_exito:.1f}%", f"{int(pct_exito*len(df_sim)/100)} usuarios"),
    (k5, "❌", "Tasa de abandono", f"{pct_abnd:.1f}%", f"{int(pct_abnd*len(df_sim)/100)} usuarios"),
    (k6, "⚠️", "Estado crítico", ec_actual or "—",
         f"{NOMBRES.get(ec_actual,'—')[:22]}…" if ec_actual else "Sin datos"),
]
for col, icon, label, val, detail in cards:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon">{icon}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{val}</div>
          <div class="kpi-detail">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PESTAÑAS
# ══════════════════════════════════════════════════════════════════════════════
tab_res, tab_est, tab_rec, tab_mat, tab_sim, tab_result, tab_diag = st.tabs([
    "📋 Resumen",
    "🗂️ Estados",
    "🔀 Recorridos",
    "📐 Matrices",
    "▶️ Simulación",
    "📊 Resultados",
    "🔧 Diagnóstico",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · RESUMEN EJECUTIVO
# ─────────────────────────────────────────────────────────────────────────────
with tab_res:
    st.markdown('<div class="sec-title">Resumen ejecutivo del modelo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Visión general de la metodología, flujo analítico y tipos de resultado del simulador.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="status-success">
          <b>✅ Resultado exitoso</b><br><br>
          El usuario completa la inscripción al Programa EDIFICA correctamente.
          Representa la conversión deseada de la plataforma.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="status-warning">
          <b>❌ Abandono voluntario</b><br><br>
          El usuario sale del proceso antes de completar la inscripción.
          Puede deberse a fricción, duda o distracción externa.
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="status-danger">
          <b>⚠️ Error técnico</b><br><br>
          El usuario encuentra una falla, página caída o error de formulario
          que impide continuar el recorrido.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cc-panel-dark">
      <div class="sec-title">¿Cómo funciona el simulador?</div>
      <div class="sec-sub">El modelo aplica teoría de cadenas de Márkov de tiempo discreto al flujo real de navegación en Colombia Comparte.</div>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    for col, num, title, text in [
        (s1,"01","Definir estados","Se identifican 33 pantallas y acciones posibles dentro de la plataforma Colombia Comparte."),
        (s2,"02","Modelar recorridos","Se construyen 66 caminos realistas de 4 perfiles de usuario (A, B, C, D, E)."),
        (s3,"03","Calcular matrices","Se calcula la matriz de conteos y la matriz de probabilidades de transición entre estados."),
        (s4,"04","Simular y analizar","Se simulan N usuarios, se identifican resultados, estado crítico y se genera la recomendación de mejora."),
    ]:
        with col:
            st.markdown(f"""
            <div class="step-box">
              <div class="step-num">Paso {num}</div>
              <div class="step-title">{title}</div>
              <div class="step-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="cc-panel">
      <div class="sec-title" style="font-size:1.1rem;">🏢 Acerca de Colombia Comparte</div>
      <div style="color:#c8e0f4; font-size:0.9rem; line-height:1.7;">
        <b>Colombia Comparte</b> es una organización social autosostenible fundada por Carolina Ruiz Herrera y Eduardo Del Castillo.
        En 10 años ha acompañado a más de <b>1.200 personas y familias</b>, trabajado con <b>70 empresas</b> y contado con
        <b>65 mentores y voluntarios</b>. Su Programa <b>EDIFICA</b> forma emprendedores en mentoría, estrategia, finanzas,
        marketing y modelo de negocio.<br><br>
        El flujo modelado en este simulador corresponde al proceso de <b>inscripción al Programa EDIFICA</b>,
        desde la llegada a la página de inicio hasta la confirmación exitosa del registro.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · ESTADOS
# ─────────────────────────────────────────────────────────────────────────────
with tab_est:
    st.markdown('<div class="sec-title">Estados del modelo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Cada estado representa una pantalla, acción o situación dentro del recorrido de navegación del usuario en Colombia Comparte.</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        busqueda = st.text_input("🔍 Buscar estado (código o nombre)", placeholder="Ej: S7 o formulario")
    with col_f2:
        filtro_tipo = st.multiselect(
            "Filtrar por tipo",
            options=df_estados["Tipo"].unique().tolist(),
            default=df_estados["Tipo"].unique().tolist()
        )

    df_est_filtrado = df_estados[df_estados["Tipo"].isin(filtro_tipo)]
    if busqueda:
        mask = (
            df_est_filtrado["Código"].str.contains(busqueda, case=False) |
            df_est_filtrado["Nombre"].str.contains(busqueda, case=False) |
            df_est_filtrado["Descripción"].str.contains(busqueda, case=False)
        )
        df_est_filtrado = df_est_filtrado[mask]

    st.dataframe(
        df_est_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Código":      st.column_config.TextColumn("Código", width=80),
            "Nombre":      st.column_config.TextColumn("Nombre del estado", width=220),
            "Descripción": st.column_config.TextColumn("Descripción", width=400),
            "Tipo":        st.column_config.TextColumn("Tipo", width=140),
        }
    )
    st.caption(f"Mostrando {len(df_est_filtrado)} de {len(df_estados)} estados.")

    st.markdown("<br>", unsafe_allow_html=True)
    ea, eb, ec_, ed = st.columns(4)
    for col, tipo, color, icon in [
        (ea, "Inicial",         "#4AACE8", "🔵"),
        (eb, "Intermedio",      "#8bbbd8", "⚪"),
        (ec_,"Final exitoso",   "#1E7E34", "✅"),
        (ed, "Final negativo",  "#C0392B", "❌"),
    ]:
        n_tipo = len(df_estados[df_estados["Tipo"] == tipo])
        with col:
            st.metric(f"{icon} {tipo}", n_tipo)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · RECORRIDOS BASE
# ─────────────────────────────────────────────────────────────────────────────
with tab_rec:
    st.markdown('<div class="sec-title">Recorridos base de usuarios</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">66 recorridos que representan el comportamiento real de cuatro perfiles de usuario en la plataforma Colombia Comparte. Son la base para construir las matrices del modelo.</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        filtro_res = st.multiselect(
            "Filtrar por resultado",
            options=df_recorridos_base["Resultado"].unique().tolist(),
            default=df_recorridos_base["Resultado"].unique().tolist()
        )
    with fc2:
        filtro_perf = st.multiselect(
            "Filtrar por perfil",
            options=df_recorridos_base["Perfil"].unique().tolist(),
            default=df_recorridos_base["Perfil"].unique().tolist()
        )

    df_rec_f = df_recorridos_base[
        df_recorridos_base["Resultado"].isin(filtro_res) &
        df_recorridos_base["Perfil"].isin(filtro_perf)
    ]

    st.dataframe(
        df_rec_f[["ID","Perfil","Recorrido","Resultado","Pasos"]],
        use_container_width=True, hide_index=True,
        column_config={
            "ID":        st.column_config.TextColumn("ID", width=55),
            "Perfil":    st.column_config.TextColumn("Perfil", width=200),
            "Recorrido": st.column_config.TextColumn("Recorrido codificado", width=320),
            "Resultado": st.column_config.TextColumn("Resultado", width=130),
            "Pasos":     st.column_config.NumberColumn("Pasos", width=70),
        }
    )
    st.caption(f"Mostrando {len(df_rec_f)} de {len(RECORRIDOS)} recorridos.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="font-size:1.1rem;">🔍 Detalle de un recorrido</div>', unsafe_allow_html=True)

    rec_elegido = st.selectbox(
        "Selecciona un recorrido para ver su detalle",
        options=df_rec_f["ID"].tolist(),
        format_func=lambda x: f"{x} · {df_rec_f[df_rec_f['ID']==x]['Perfil'].values[0]} · {df_rec_f[df_rec_f['ID']==x]['Resultado'].values[0]}"
    )
    if rec_elegido:
        fila = df_rec_f[df_rec_f["ID"] == rec_elegido].iloc[0]
        dc1, dc2 = st.columns(2)
        with dc1:
            st.info(f"**Codificado:** {fila['Recorrido']}")
        with dc2:
            st.success(f"**Nombrado:** {fila['Recorrido (nombres)']}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · MATRICES
# ─────────────────────────────────────────────────────────────────────────────
with tab_mat:
    st.markdown('<div class="sec-title">Matrices de transición</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">La matriz de conteos registra las transiciones observadas en los 66 recorridos. La matriz de probabilidades normaliza cada fila para obtener las probabilidades de la cadena de Márkov.</div>', unsafe_allow_html=True)

    tipo_mat = st.radio(
        "Matriz a visualizar",
        ["📊 Conteos", "🎯 Probabilidades"],
        horizontal=True
    )

    # filtrar solo filas/columnas activas
    activos = [s for s in ESTADOS
               if matriz_conteos.loc[s].sum() > 0 or matriz_conteos[s].sum() > 0]

    if tipo_mat == "📊 Conteos":
        st.dataframe(matriz_conteos.loc[activos, activos], use_container_width=True)
    else:
        st.dataframe(matriz_prob.loc[activos, activos].round(4), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="font-size:1.1rem;">🔑 Transiciones más relevantes</div>', unsafe_allow_html=True)

    trans_destacadas = [
        ("S0","S2"),("S2","S7"),("S7","S8"),("S8","S9"),
        ("S11","S30"),("S21","S31"),("S12","S13"),("S26","S28"),
    ]
    td_rows = []
    for o, d in trans_destacadas:
        if o in matriz_prob.index and d in matriz_prob.columns:
            td_rows.append({
                "Transición": f"{o} → {d}",
                "De": NOMBRES.get(o, o),
                "Hacia": NOMBRES.get(d, d),
                "Probabilidad": f"{matriz_prob.loc[o,d]:.4f}",
            })
    st.dataframe(pd.DataFrame(td_rows), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # Heatmap de las transiciones activas
    st.markdown('<div class="sec-title" style="font-size:1.1rem;">🌡️ Mapa de calor (probabilidades)</div>', unsafe_allow_html=True)
    estados_core = ["S0","S2","S7","S8","S9","S10","S11","S15","S19","S21","S22","S29","S30","S31","S32"]
    sub_mat = matriz_prob.loc[estados_core, estados_core]

    fig_hm, ax_hm = plt.subplots(figsize=(10, 6))
    fig_hm.patch.set_facecolor('#01182E')
    ax_hm.set_facecolor('#01182E')
    im = ax_hm.imshow(sub_mat.values, cmap='Blues', aspect='auto', vmin=0, vmax=1)
    ax_hm.set_xticks(range(len(estados_core)))
    ax_hm.set_yticks(range(len(estados_core)))
    ax_hm.set_xticklabels(estados_core, rotation=45, ha='right', color='white', fontsize=9)
    ax_hm.set_yticklabels(estados_core, color='white', fontsize=9)
    for i in range(len(estados_core)):
        for j in range(len(estados_core)):
            v = sub_mat.values[i, j]
            if v > 0.05:
                ax_hm.text(j, i, f"{v:.2f}", ha='center', va='center',
                           fontsize=7, color='white' if v > 0.5 else '#001A3A', fontweight='bold')
    cbar = fig_hm.colorbar(im, ax=ax_hm)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white', fontsize=8)
    ax_hm.set_title("Matriz de probabilidades (estados principales)", color='white', fontsize=11, pad=10)
    plt.tight_layout()
    st.pyplot(fig_hm)
    plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · SIMULACIÓN
# ─────────────────────────────────────────────────────────────────────────────
with tab_sim:
    st.markdown('<div class="sec-title">Ejecutar simulación</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Configura los parámetros en la barra lateral y presiona el botón para generar nuevos recorridos simulados con la cadena de Márkov.</div>', unsafe_allow_html=True)

    sc1, sc2 = st.columns([1, 2])

    with sc1:
        st.markdown('<div class="cc-panel">', unsafe_allow_html=True)
        st.metric("👥 Usuarios configurados", f"{n_usuarios:,}")
        st.metric("📍 Estado inicial", f"{estado_inicial_sel} – {NOMBRES.get(estado_inicial_sel, '')}")
        st.metric("🔢 Máximo de pasos", max_pasos)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("▶️ Ejecutar simulación", use_container_width=True):
            with st.spinner("Simulando usuarios..."):
                st.session_state["df_sim"] = simular_n(
                    n_usuarios, matriz_prob, estado_inicial_sel, ESTADOS_FINALES, max_pasos
                )
                for key in ["df_sim_mejor","rec_obj","matriz_mejor"]:
                    if key in st.session_state:
                        del st.session_state[key]
            st.success(f"✅ Simulación completada: {n_usuarios:,} usuarios generados.")

    with sc2:
        st.markdown('<div class="sec-title" style="font-size:1.05rem;">👁️ Vista previa (primeros 20 usuarios)</div>', unsafe_allow_html=True)
        df_preview = st.session_state["df_sim"].head(20)[["Usuario","Resultado","Pasos","Recorrido"]]
        st.dataframe(df_preview, use_container_width=True, hide_index=True,
                     column_config={
                         "Recorrido": st.column_config.TextColumn("Recorrido", width=360),
                     })

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 · RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────
with tab_result:
    st.markdown('<div class="sec-title">Resultados de la simulación</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Métricas, distribuciones y rutas más frecuentes obtenidas a partir de los recorridos simulados.</div>', unsafe_allow_html=True)

    df_sim = st.session_state["df_sim"]
    pct_e  = (df_sim["Estado final"] == ESTADO_EXITO).mean()   * 100
    pct_a  = (df_sim["Estado final"] == ESTADO_ABANDONO).mean()* 100
    pct_er = (df_sim["Estado final"] == ESTADO_ERROR).mean()   * 100
    prom   = df_sim["Pasos"].mean()
    prom_e = df_sim[df_sim["Estado final"]==ESTADO_EXITO]["Pasos"].mean()
    prom_a = df_sim[df_sim["Estado final"]==ESTADO_ABANDONO]["Pasos"].mean()

    rm1, rm2, rm3, rm4 = st.columns(4)
    rm1.metric("✅ Éxito",            f"{pct_e:.1f}%",  f"{int(pct_e*len(df_sim)/100)} usuarios")
    rm2.metric("❌ Abandono",         f"{pct_a:.1f}%",  f"{int(pct_a*len(df_sim)/100)} usuarios")
    rm3.metric("⚠️ Error técnico",    f"{pct_er:.1f}%", f"{int(pct_er*len(df_sim)/100)} usuarios")
    rm4.metric("📏 Promedio de pasos",f"{prom:.2f}",    f"Éxito:{prom_e:.1f} | Abandono:{prom_a:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)
    gr1, gr2 = st.columns([1, 1])

    # Gráfica 1: Pie chart
    with gr1:
        st.markdown('<div class="sec-title" style="font-size:1rem;">📊 Distribución de resultados</div>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        fig1.patch.set_facecolor('#01182E')
        ax1.set_facecolor('#01182E')
        valores = [int(pct_e*len(df_sim)/100), int(pct_a*len(df_sim)/100), int(pct_er*len(df_sim)/100)]
        etiquetas = [f"Éxito\n{pct_e:.1f}%", f"Abandono\n{pct_a:.1f}%", f"Error\n{pct_er:.1f}%"]
        colores = ["#1E7E34","#C0392B","#D4780A"]
        wedges, texts = ax1.pie(
            valores, labels=etiquetas, colors=colores,
            startangle=140, wedgeprops=dict(edgecolor='#01182E', linewidth=2.5),
            textprops=dict(color='white', fontsize=11, fontweight='bold')
        )
        ax1.set_title(f"1.000 usuarios simulados", color='white', fontsize=11, pad=8)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    # Gráfica 2: Barras de pasos promedio
    with gr2:
        st.markdown('<div class="sec-title" style="font-size:1rem;">📏 Pasos promedio por resultado</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        fig2.patch.set_facecolor('#01182E')
        ax2.set_facecolor('#01182E')
        grupos   = df_sim.groupby("Estado final")["Pasos"].mean()
        etiq2    = []
        vals2    = []
        cols2    = []
        for ef, col, lab in [(ESTADO_EXITO,"#1E7E34","Éxito"),(ESTADO_ABANDONO,"#C0392B","Abandono"),(ESTADO_ERROR,"#D4780A","Error")]:
            if ef in grupos:
                etiq2.append(lab)
                vals2.append(grupos[ef])
                cols2.append(col)
        bars2 = ax2.bar(etiq2, vals2, color=cols2, edgecolor='#01182E', linewidth=1.5, width=0.5)
        for b, v in zip(bars2, vals2):
            ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.1,
                     f"{v:.1f}", ha='center', va='bottom', color='white', fontsize=11, fontweight='bold')
        ax2.set_ylabel("Pasos promedio", color='white')
        ax2.set_title("Profundidad del recorrido", color='white', fontsize=11, pad=8)
        ax2.tick_params(colors='white')
        ax2.spines[:].set_visible(False)
        ax2.set_facecolor('#01182E')
        ax2.set_ylim(0, max(vals2)*1.25 if vals2 else 10)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # Gráfica 3: top estados de abandono
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="font-size:1rem;">🚨 Top estados donde más usuarios abandonan</div>', unsafe_allow_html=True)
    _, ec_n_full = estado_critico(df_sim)
    df_abn = df_sim[df_sim["Estado final"] == ESTADO_ABANDONO]["Recorrido"]
    previos_all = []
    for r in df_abn:
        pasos_ = [p.strip() for p in r.split("→")]
        if len(pasos_) >= 2:
            previos_all.append(pasos_[-2])
    if previos_all:
        top8 = Counter(previos_all).most_common(8)
        top_ec  = [f"{k}\n{NOMBRES.get(k,'')[:18]}…" if len(NOMBRES.get(k,''))>18 else f"{k}\n{NOMBRES.get(k,'')}" for k,_ in top8]
        top_val = [v for _,v in top8]
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        fig3.patch.set_facecolor('#01182E')
        ax3.set_facecolor('#01182E')
        colores3 = ["#C0392B" if i==0 else "#2E6DB4" for i in range(len(top8))]
        bars3 = ax3.barh(top_ec[::-1], top_val[::-1], color=colores3[::-1],
                         edgecolor='#01182E', linewidth=1, height=0.65)
        for b, v in zip(bars3, top_val[::-1]):
            ax3.text(b.get_width()+0.5, b.get_y()+b.get_height()/2,
                     str(v), va='center', color='white', fontsize=10, fontweight='bold')
        ax3.set_xlabel("Número de abandonos", color='white')
        ax3.tick_params(colors='white', labelsize=9)
        ax3.spines[:].set_visible(False)
        ax3.set_title("Estado previo al abandono (top 8)", color='white', fontsize=11, pad=8)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()
    else:
        st.info("No se registraron abandonos en esta simulación.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="font-size:1rem;">🔁 Recorridos más frecuentes</div>', unsafe_allow_html=True)
    rutas_frec = df_sim["Recorrido"].value_counts().head(8).reset_index()
    rutas_frec.columns = ["Recorrido", "Frecuencia"]
    st.dataframe(rutas_frec, use_container_width=True, hide_index=True)

    # Tabla resumen
    st.markdown("<br>", unsafe_allow_html=True)
    conteo_res2 = df_sim["Resultado"].value_counts().reset_index()
    conteo_res2.columns = ["Resultado", "Usuarios"]
    conteo_res2["Porcentaje (%)"] = (conteo_res2["Usuarios"] / len(df_sim) * 100).round(2)
    st.dataframe(conteo_res2, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 · DIAGNÓSTICO Y MEJORA
# ─────────────────────────────────────────────────────────────────────────────
with tab_diag:
    st.markdown('<div class="sec-title">Diagnóstico y mejora del abandono</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Identificación del estado crítico de la simulación y propuesta de intervención con escenario comparativo.</div>', unsafe_allow_html=True)

    df_sim = st.session_state["df_sim"]
    ec_d, ec_n_d = estado_critico(df_sim)

    if ec_d is None:
        st.success("No se detectaron abandonos en la simulación actual.")
    else:
        total_abnd = (df_sim["Estado final"] == ESTADO_ABANDONO).sum()
        pct_sobre_abnd = ec_n_d / total_abnd * 100 if total_abnd > 0 else 0
        pct_sobre_total = ec_n_d / len(df_sim) * 100

        dm1, dm2, dm3, dm4 = st.columns(4)
        dm1.metric("🚨 Estado crítico",       ec_d)
        dm2.metric("📌 Nombre",               NOMBRES.get(ec_d, "—"))
        dm3.metric("❌ Abandonos asociados",   ec_n_d)
        dm4.metric("% sobre abandonos totales", f"{pct_sobre_abnd:.1f}%")

        st.markdown(f"""
        <div class="diag-box">
          <b>🔎 Diagnóstico principal</b><br><br>
          El estado más crítico identificado es <b>{ec_d} – {NOMBRES.get(ec_d,'')}</b>.<br>
          <b>Descripción:</b> {DESCRIPCIONES.get(ec_d,'')}<br><br>
          De los <b>{total_abnd}</b> usuarios que abandonaron, el <b>{pct_sobre_abnd:.1f}%</b>
          ({ec_n_d} usuarios) lo hizo inmediatamente después de pasar por este estado.
          Sobre el total simulado, representa el <b>{pct_sobre_total:.1f}%</b> de los usuarios.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-title" style="font-size:1.05rem;">💡 Recomendación de mejora</div>', unsafe_allow_html=True)
        st.write("Presiona el botón para generar la recomendación ejecutiva basada en el estado crítico.")

        if st.button("🔧 Generar recomendación ejecutiva", use_container_width=True):
            st.session_state["rec_obj"] = recomendacion_edifica(ec_d, matriz_prob)

        if "rec_obj" in st.session_state:
            rec = st.session_state["rec_obj"]
            st.markdown(f"""
            <div class="rec-box">
              <h4>📋 Propuesta de intervención — {rec['estado']} · {rec['nombre']}</h4>
              <b>Probabilidad directa de abandono desde este estado:</b> {rec['prob_abandono']:.2%}<br><br>
              <b>🔍 Posible causa:</b><br>{rec['causa']}<br><br>
              <b>🛠️ Mejora recomendada:</b><br>{rec['mejora']}<br><br>
              <b>📐 Ajuste en la matriz de transición:</b><br>{rec['accion']}<br><br>
              <b>📈 Indicador de validación:</b><br>{rec['kpi']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title" style="font-size:1.05rem;">📈 Evaluación del escenario mejorado</div>', unsafe_allow_html=True)
        st.write("Ajusta la reducción de abandono desde el estado crítico y simula el escenario mejorado.")

        reduccion = st.slider(
            "Reducción de P(abandono) desde el estado crítico",
            min_value=0.05, max_value=0.60, value=0.20, step=0.05,
            format="%.2f"
        )

        if st.button("🚀 Simular escenario mejorado", use_container_width=True):
            with st.spinner("Construyendo escenario mejorado..."):
                mat_m = matriz_mejorada_fn(matriz_prob, ec_d, reduccion)
                df_m  = simular_n(n_usuarios, mat_m, estado_inicial_sel, ESTADOS_FINALES, max_pasos)
                st.session_state["df_sim_mejor"] = df_m
                st.session_state["matriz_mejor"] = mat_m
            st.success("✅ Escenario mejorado generado correctamente.")

        if "df_sim_mejor" in st.session_state:
            st.markdown('<div class="sec-title" style="font-size:1.05rem;">⚖️ Comparación de escenarios</div>', unsafe_allow_html=True)
            df_m = st.session_state["df_sim_mejor"]

            pct_ini = df_sim["Resultado"].value_counts(normalize=True)*100
            pct_mej = df_m["Resultado"].value_counts(normalize=True)*100
            todos   = sorted(set(pct_ini.index)|set(pct_mej.index))

            df_comp = pd.DataFrame({
                "Resultado":            todos,
                "Inicial (%)":          [round(pct_ini.get(r,0),2) for r in todos],
                "Mejorado (%)":         [round(pct_mej.get(r,0),2) for r in todos],
                "Δ Cambio (pp)":        [round(pct_mej.get(r,0)-pct_ini.get(r,0),2) for r in todos],
            })
            st.dataframe(df_comp, use_container_width=True, hide_index=True)

            fig_cmp, ax_cmp = plt.subplots(figsize=(9, 4))
            fig_cmp.patch.set_facecolor('#01182E')
            ax_cmp.set_facecolor('#01182E')
            x  = np.arange(len(todos))
            w  = 0.35
            b1 = ax_cmp.bar(x-w/2, df_comp["Inicial (%)"],  w, label="Escenario inicial",  color="#2E6DB4", edgecolor='#01182E')
            b2 = ax_cmp.bar(x+w/2, df_comp["Mejorado (%)"], w, label="Escenario mejorado", color="#4AACE8", edgecolor='#01182E')
            for b in list(b1)+list(b2):
                ax_cmp.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
                            f"{b.get_height():.1f}%", ha='center', va='bottom',
                            color='white', fontsize=8, fontweight='bold')
            ax_cmp.set_xticks(x)
            ax_cmp.set_xticklabels(todos, color='white', fontsize=10)
            ax_cmp.set_ylabel("Porcentaje (%)", color='white')
            ax_cmp.tick_params(colors='white')
            ax_cmp.spines[:].set_visible(False)
            ax_cmp.legend(facecolor='#01182E', labelcolor='white', fontsize=9)
            ax_cmp.set_title("Comparación: Escenario inicial vs mejorado", color='white', fontsize=11, pad=8)
            plt.tight_layout()
            st.pyplot(fig_cmp)
            plt.close()

            st.info("Esta comparación permite justificar si la mejora propuesta reduce el abandono o incrementa el éxito en el modelo simulado.")
