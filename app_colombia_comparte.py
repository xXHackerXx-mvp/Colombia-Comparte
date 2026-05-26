"""
DASHBOARD DE SIMULACIÓN — COLOMBIA COMPARTE
Cadenas de Márkov — Programa EDIFICA
Universidad Santo Tomás · Seccional Tunja · 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDIFICA · Simulación Markov",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PYTHON COLOUR CONSTANTS (for inline HTML / matplotlib) ─────────────────────
BG   = "#FAFAF7"
SURF = "#FFFFFF"
SURF2= "#F4F3EE"
FG   = "#14120C"
FG_M = "#5C594F"
FG_D = "#9A968B"
ACC  = "#3D4FE0"
GOOD = "#1F8A5B"
BAD  = "#C84B3B"
WARN = "#E0A23D"
BORD = "#E3E1DA"

# ── CSS  (plain string — no f-string — to prevent Streamlit stripping <style>) ─
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --bg:    #FAFAF7;
  --surf:  #FFFFFF;
  --surf2: #F4F3EE;
  --fg:    #14120C;
  --fg-m:  #5C594F;
  --fg-d:  #9A968B;
  --acc:   #3D4FE0;
  --good:  #1F8A5B;
  --bad:   #C84B3B;
  --warn:  #E0A23D;
  --bord:  #E3E1DA;
}

html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
  background: var(--bg) !important;
  color: var(--fg) !important;
}
.main .block-container {
  background: var(--bg) !important;
  padding: 1.5rem 2rem 3rem !important;
  max-width: 1340px;
}
#MainMenu, footer, header { visibility: hidden; }

/* background grid */
.main::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(61,79,224,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(61,79,224,.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

/* sidebar */
[data-testid="stSidebar"] {
  background: var(--surf) !important;
  border-right: 1px solid var(--bord) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
  color: var(--fg-m) !important;
  font-size: .82rem !important;
}

/* header */
.edifica-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.4rem;
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 12px;
  margin-bottom: 1.1rem;
  box-shadow: 0 1px 4px rgba(20,18,12,.06);
}
.edifica-header h1 {
  font-size: 1.05rem; font-weight: 700; color: var(--fg); margin: 0;
  letter-spacing: -0.01em;
}
.edifica-header h1 span {
  font-size: .78rem; font-weight: 400; color: var(--fg-d); margin-left: .45rem;
}

/* hero */
.hero {
  background: linear-gradient(135deg, #2138c8 0%, #3D4FE0 50%, #5b6ef5 100%);
  border-radius: 14px;
  padding: 2rem 2rem 1.8rem;
  margin-bottom: 1.1rem;
  color: #fff;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px);
  background-size: 32px 32px;
}
.hero-eyebrow {
  font-size: .7rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; opacity: .75; margin-bottom: .6rem;
}
.hero h2 {
  font-size: 2rem; font-weight: 800; margin: 0 0 .5rem; line-height: 1.15;
}
.hero p { font-size: .9rem; opacity: .85; margin: 0 0 1rem; max-width: 620px; }
.hero-tags { display: flex; flex-wrap: wrap; gap: .4rem; }
.hero-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 99px;
  font-size: .7rem;
  font-weight: 600;
  background: rgba(255,255,255,.18);
  border: 1px solid rgba(255,255,255,.3);
}

/* KPI row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: .65rem;
  margin-bottom: 1.1rem;
}
.kpi {
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 10px;
  padding: .75rem .95rem;
  box-shadow: 0 1px 3px rgba(20,18,12,.05);
}
.kpi-icon { font-size: 1.1rem; margin-bottom: .2rem; }
.kpi-label {
  font-size: .6rem; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; color: var(--fg-d); margin-bottom: .25rem;
}
.kpi-value {
  font-size: 1.45rem; font-weight: 700; line-height: 1; color: var(--fg);
  font-family: 'IBM Plex Mono', monospace;
}
.kpi-detail { font-size: .68rem; color: var(--fg-d); margin-top: .2rem; }
.kpi-delta  { font-size: .68rem; margin-top: .2rem; color: var(--fg-m); }
.kpi-delta.pos { color: var(--good); }
.kpi-delta.neg { color: var(--bad);  }

/* cards */
.card {
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 12px;
  padding: 1rem 1.2rem 1.1rem;
  box-shadow: 0 1px 4px rgba(20,18,12,.05);
  margin-bottom: .85rem;
}
.card h3 {
  font-size: .72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .07em; color: var(--fg-d); margin: 0 0 .65rem 0;
}
.card h4 {
  font-size: .9rem; font-weight: 700; color: var(--fg); margin: 0 0 .5rem;
}

/* outcome cards */
.outcome-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: .7rem; margin-bottom: .8rem; }
.outcome-card { border-radius: 10px; padding: .9rem 1rem; }
.outcome-card.success { background: #E8F5EE; border: 1px solid #A8D9BC; }
.outcome-card.abandon { background: #FDECEA; border: 1px solid #F0B8B2; }
.outcome-card.error   { background: #FEF8E7; border: 1px solid #F0D98A; }
.outcome-card h4 { font-size: .78rem; font-weight: 700; margin: 0 0 .3rem; }
.outcome-card.success h4 { color: var(--good); }
.outcome-card.abandon h4 { color: var(--bad);  }
.outcome-card.error   h4 { color: var(--warn); }
.outcome-card p { font-size: .8rem; color: var(--fg-m); margin: 0; line-height: 1.55; }

/* diagnosis */
.diag-row { display: flex; align-items: baseline; gap: .5rem; margin-bottom: .4rem; }
.diag-label { font-size: .8rem; color: var(--fg-m); }
.diag-val {
  font-size: .95rem; font-weight: 700; color: var(--fg);
  font-family: 'IBM Plex Mono', monospace;
}
.diag-badge {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: .66rem; font-weight: 700; background: #FEF3E2; color: var(--warn);
  letter-spacing: .04em; text-transform: uppercase;
}

/* state pill */
.pill {
  display: inline-block; padding: 2px 8px; border-radius: 99px;
  font-size: .67rem; font-weight: 600;
}
.pill-acceso     { background: #EEF0FD; color: var(--acc); }
.pill-registro   { background: #E6F0FA; color: #1B6BB0; }
.pill-perfil     { background: #F0EBF8; color: #7B3FA6; }
.pill-proyecto   { background: #FFF3E0; color: #B05E00; }
.pill-envio      { background: #E8F5EE; color: var(--good); }
.pill-evaluacion { background: #FDECEA; color: var(--bad); }
.pill-resultado  { background: #F4F3EE; color: var(--fg-m); }
.pill-soporte    { background: #F4F3EE; color: var(--fg-m); }

/* buttons */
.stButton > button {
  background: var(--acc) !important; color: #fff !important;
  border: none !important; border-radius: 8px !important;
  font-weight: 600 !important;
  font-family: 'IBM Plex Sans', sans-serif !important;
  padding: .5rem 1.1rem !important;
}
.stButton > button:hover { background: #2d3ecc !important; }

/* form labels */
.stSlider label, .stNumberInput label, .stSelectbox label {
  color: var(--fg-m) !important; font-size: .8rem !important;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surf2) !important; border-radius: 8px !important;
  gap: 2px; padding: 3px; flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 6px !important; font-weight: 600 !important;
  font-size: .78rem !important; color: var(--fg-m) !important;
  padding: .32rem .8rem !important;
}
.stTabs [aria-selected="true"] {
  background: var(--surf) !important; color: var(--acc) !important;
  box-shadow: 0 1px 3px rgba(20,18,12,.1) !important;
}

/* divider */
hr.edifica { border: none; border-top: 1px solid var(--bord); margin: .5rem 0 1rem; }

/* comparison table */
.cmp-table { width:100%; font-size:.82rem; border-collapse:collapse; }
.cmp-table th { text-align:left; padding:5px 0; font-size:.68rem; text-transform:uppercase;
                letter-spacing:.05em; color:var(--fg-d); font-weight:700; }
.cmp-table th.r { text-align:right; padding:5px 8px; }
.cmp-table td { padding:5px 0; color:var(--fg-m); border-top:1px solid var(--bord); }
.cmp-table td.r { text-align:right; font-family:monospace; padding:5px 8px; }
.cmp-table td.pos { text-align:right; color:var(--good); font-weight:700; }
.cmp-table td.neg { text-align:right; color:var(--bad);  font-weight:700; }
.cmp-table td.neu { text-align:right; color:var(--fg-m); }
.cmp-table tr.total td { border-top:2px solid var(--bord); font-weight:700; color:var(--fg); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DATA MODEL  (from handoff data.js)
# ══════════════════════════════════════════════════════════════════════════════
STATES = [
    ("S01","Landing",                 "Acceso",      "page"),
    ("S02","Catálogo de programas",   "Acceso",      "page"),
    ("S03","EDIFICA · Detalle",       "Acceso",      "page"),
    ("S04","Quiz de elegibilidad",    "Acceso",      "page"),
    ("S05","Registro · Inicio",       "Registro",    "page"),
    ("S06","Formulario datos básicos","Registro",    "form"),
    ("S07","Verificación correo",     "Registro",    "verify"),
    ("S08","OTP móvil",               "Registro",    "verify"),
    ("S09","Aceptación T&C",          "Registro",    "form"),
    ("S10","Login",                   "Registro",    "form"),
    ("S11","Perfil personal",         "Perfil",      "form"),
    ("S12","Documento de identidad",  "Perfil",      "upload"),
    ("S13","Comprobante domicilio",   "Perfil",      "upload"),
    ("S14","Información educativa",   "Perfil",      "form"),
    ("S15","Experiencia laboral",     "Perfil",      "form"),
    ("S16","Idea de negocio",         "Proyecto",    "form"),
    ("S17","Plan de negocio",         "Proyecto",    "upload"),
    ("S18","Modelo financiero",       "Proyecto",    "upload"),
    ("S19","Fotos del proyecto",      "Proyecto",    "upload"),
    ("S20","Pitch en video",          "Proyecto",    "upload"),
    ("S21","Referencias",             "Proyecto",    "form"),
    ("S22","Revisión del resumen",    "Envío",       "page"),
    ("S23","Envío de solicitud",      "Envío",       "action"),
    ("S24","Confirmación",            "Envío",       "page"),
    ("S25","Programar entrevista",    "Evaluación",  "form"),
    ("S26","Entrevista realizada",    "Evaluación",  "action"),
    ("S27","Decisión",                "Evaluación",  "action"),
    ("S28","Aceptado",                "Resultado",   "terminal:success"),
    ("S29","Lista de espera",         "Resultado",   "page"),
    ("S30","Rechazado",               "Resultado",   "terminal:reject"),
    ("S31","Reintento de sesión",     "Soporte",     "action"),
    ("S32","Abandono",                "Resultado",   "terminal:abandon"),
    ("S33","Error técnico",           "Resultado",   "terminal:error"),
]
N_STATES    = len(STATES)
STATE_IDS   = [s[0] for s in STATES]
STATE_NAMES = [s[1] for s in STATES]
STATE_IDX   = {s[0]: i for i, s in enumerate(STATES)}

def terminal_of(i: int):
    kind = STATES[i][3]
    return kind.split(":")[1] if kind.startswith("terminal:") else None

T_RAW = {
    "S01": [("S02",0.55,None),("S03",0.20,None),("S04",0.10,None),("S32",0.15,None)],
    "S02": [("S03",0.65,None),("S01",0.10,None),("S32",0.20,None),("S33",0.05,None)],
    "S03": [("S04",0.45,None),("S05",0.30,None),("S02",0.10,None),("S32",0.15,None)],
    "S04": [("S05",0.60,None),("S03",0.15,None),("S32",0.22,None),("S33",0.03,None)],
    "S05": [("S06",0.78,None),("S10",0.10,None),("S32",0.10,None),("S33",0.02,None)],
    "S06": [("S07",0.70,None),("S33",0.08,None),("S32",0.22,None)],
    "S07": [("S08",0.74,None),("S31",0.10,None),("S32",0.13,None),("S33",0.03,None)],
    "S08": [("S09",0.86,None),("S31",0.05,None),("S32",0.07,None),("S33",0.02,None)],
    "S09": [("S11",0.90,None),("S32",0.08,None),("S33",0.02,None)],
    "S10": [("S11",0.82,None),("S31",0.10,None),("S32",0.06,None),("S33",0.02,None)],
    "S11": [("S12",0.80,None),("S32",0.18,None),("S33",0.02,None)],
    "S12": [("S13",0.74,None),("S32",0.22,None),("S33",0.04,None)],
    "S13": [("S14",0.78,None),("S32",0.18,None),("S33",0.04,None)],
    "S14": [("S15",0.86,None),("S32",0.12,None),("S33",0.02,None)],
    "S15": [("S16",0.84,None),("S32",0.14,None),("S33",0.02,None)],
    "S16": [("S17",0.75,None),("S32",0.22,None),("S33",0.03,None)],
    "S17": [("S18",0.50,0.78),("S32",0.42,0.16),("S33",0.08,0.06)],
    "S18": [("S19",0.78,None),("S32",0.18,None),("S33",0.04,None)],
    "S19": [("S20",0.72,None),("S32",0.24,None),("S33",0.04,None)],
    "S20": [("S21",0.70,None),("S32",0.26,None),("S33",0.04,None)],
    "S21": [("S22",0.88,None),("S32",0.10,None),("S33",0.02,None)],
    "S22": [("S23",0.92,None),("S32",0.06,None),("S33",0.02,None)],
    "S23": [("S24",0.96,None),("S33",0.04,None)],
    "S24": [("S25",0.94,None),("S32",0.04,None),("S33",0.02,None)],
    "S25": [("S26",0.90,None),("S32",0.08,None),("S33",0.02,None)],
    "S26": [("S27",0.98,None),("S33",0.02,None)],
    "S27": [("S28",0.42,None),("S29",0.18,None),("S30",0.40,None)],
    "S28": [("S28",1.0,None)],
    "S29": [("S28",0.30,None),("S30",0.40,None),("S32",0.30,None)],
    "S30": [("S30",1.0,None)],
    "S31": [("S10",0.80,None),("S32",0.15,None),("S33",0.05,None)],
    "S32": [("S32",1.0,None)],
    "S33": [("S31",0.55,None),("S32",0.45,None)],
}

PROFILES = [
    ("P1","Explorador casual",    "S01", 0.35),
    ("P2","Referido directo",     "S03", 0.22),
    ("P3","Candidato motivado",   "S04", 0.20),
    ("P4","Usuario recurrente",   "S10", 0.15),
    ("P5","Reintento post-error", "S31", 0.08),
]

FUNNEL_PATH = ["S01","S05","S09","S11","S16","S17","S18","S21","S22","S23","S27","S28"]

GROUP_COLORS = {
    "Acceso":     "#EEF0FD",
    "Registro":   "#E6F0FA",
    "Perfil":     "#F0EBF8",
    "Proyecto":   "#FFF3E0",
    "Envío":      "#E8F5EE",
    "Evaluación": "#FDECEA",
    "Resultado":  "#F4F3EE",
    "Soporte":    "#F4F3EE",
}

# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def build_matrix(scenario: str) -> np.ndarray:
    M = np.zeros((N_STATES, N_STATES))
    for from_id, edges in T_RAW.items():
        i = STATE_IDX[from_id]
        for (to_id, p1, p2) in edges:
            p = p2 if (scenario == "improved" and p2 is not None) else p1
            M[i, STATE_IDX[to_id]] = p
        s = M[i].sum()
        if s > 0:
            M[i] /= s
    return M

@st.cache_data
def simulate(n: int, max_steps: int, scenario: str, seed: int) -> dict:
    M   = build_matrix(scenario)
    rng = np.random.default_rng(seed)

    w   = np.array([p[3] for p in PROFILES], dtype=float)
    w  /= w.sum()
    cw  = np.cumsum(w)
    Mcs = np.cumsum(M, axis=1)

    finals    = np.zeros(N_STATES, dtype=int)
    visits    = np.zeros(N_STATES, dtype=int)
    step_dist = np.zeros((max_steps + 1, N_STATES), dtype=int)
    counts    = np.zeros((N_STATES, N_STATES), dtype=int)
    steps_to  = {"success": [], "abandon": [], "reject": [], "error": []}
    prof_out  = [{"success":0,"abandon":0,"reject":0,"error":0,"inprocess":0}
                 for _ in PROFILES]

    for _ in range(n):
        pi = min(int(np.searchsorted(cw, rng.random())), len(PROFILES)-1)
        s  = STATE_IDX[PROFILES[pi][2]]
        visits[s] += 1
        step_dist[0][s] += 1
        term = terminal_of(s)
        step = 0
        while term is None and step < max_steps:
            nxt = min(int(np.searchsorted(Mcs[s], rng.random())), N_STATES-1)
            counts[s, nxt] += 1
            s = nxt
            step += 1
            visits[s] += 1
            if step <= max_steps:
                step_dist[step][s] += 1
            term = terminal_of(s)
        finals[s] += 1
        if term:
            steps_to[term].append(step)
            prof_out[pi][term] += 1
        else:
            prof_out[pi]["inprocess"] += 1

    outcome = {"success":0,"abandon":0,"reject":0,"error":0,"inprocess":0}
    for i in range(N_STATES):
        t = terminal_of(i)
        outcome[t if t else "inprocess"] += finals[i]

    ab_idx   = STATE_IDX["S32"]
    critical = {"idx":-1,"score":0,"abandon_flow":0,"abandon_rate":0.0,"outflow":0}
    for i in range(N_STATES):
        if terminal_of(i) is not None:
            continue
        outflow = int(counts[i].sum())
        if outflow < 5:
            continue
        ab = int(counts[i, ab_idx])
        if ab > critical["score"]:
            critical = {"idx":i,"score":ab,"abandon_flow":ab,
                        "abandon_rate":ab/outflow,"outflow":outflow}

    avg_steps = {k: float(np.mean(v)) if v else 0.0 for k, v in steps_to.items()}

    return dict(n=n, max_steps=max_steps, scenario=scenario, seed=seed,
                finals=finals, visits=visits, step_dist=step_dist, counts=counts,
                outcome=outcome, steps_to=steps_to, avg_steps=avg_steps,
                prof_out=prof_out, critical=critical, M=M)

# ══════════════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fig_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=SURF, transparent=False)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def img_html(fig, caption="") -> str:
    b64 = fig_b64(fig)
    h = f'<img src="data:image/png;base64,{b64}" style="width:100%;border-radius:6px;"/>'
    if caption:
        h += f'<p style="font-size:.67rem;color:{FG_D};margin-top:3px;">{caption}</p>'
    return h

def show_img(fig, caption=""):
    st.markdown(img_html(fig, caption), unsafe_allow_html=True)

def chart_funnel(res_b, res_i=None):
    labels = [STATE_NAMES[STATE_IDX[s]] for s in FUNNEL_PATH]
    bv = [res_b["visits"][STATE_IDX[s]] for s in FUNNEL_PATH]
    x  = np.arange(len(FUNNEL_PATH))
    fig, ax = plt.subplots(figsize=(7.5, 4))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    bw = 0.37 if res_i else 0.62
    ax.bar(x-(bw/2 if res_i else 0), bv, width=bw, color=ACC, alpha=0.85, zorder=3, label="Base")
    if res_i:
        iv = [res_i["visits"][STATE_IDX[s]] for s in FUNNEL_PATH]
        ax.bar(x+bw/2, iv, width=bw, color=GOOD, alpha=0.85, zorder=3, label="Mejorado")
        ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=38, ha="right", fontsize=6.3, color=FG_M)
    ax.set_ylabel("Visitas", fontsize=7.5, color=FG_D)
    ax.tick_params(axis="y", labelsize=7, colors=FG_D)
    ax.tick_params(axis="x", colors=FG_M)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(BORD)
    ax.grid(axis="y", color=BORD, linewidth=0.5, zorder=0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{int(v):,}"))
    fig.tight_layout(pad=0.6)
    return fig

def chart_heatmap(res):
    M = res["M"]
    fig, ax = plt.subplots(figsize=(8, 7.5))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    cmap = LinearSegmentedColormap.from_list("edifica",[SURF,"#C7CBF7",ACC], N=256)
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    short = [f"S{i+1:02d}" for i in range(N_STATES)]
    ax.set_xticks(range(N_STATES)); ax.set_xticklabels(short, fontsize=5, rotation=90, color=FG_M)
    ax.set_yticks(range(N_STATES)); ax.set_yticklabels(short, fontsize=5, color=FG_M)
    ax.set_xlabel("Estado destino", fontsize=7, color=FG_D)
    ax.set_ylabel("Estado origen",  fontsize=7, color=FG_D)
    plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02).ax.tick_params(labelsize=7)
    fig.tight_layout(pad=0.5)
    return fig

def chart_stepchart(res_b, res_i=None):
    sd   = res_b["step_dist"]
    tmask= np.array([terminal_of(i) is not None for i in range(N_STATES)])
    steps= range(sd.shape[0])
    ab   = np.array([sd[t,~tmask].sum() for t in steps])
    fig, ax = plt.subplots(figsize=(7, 3.2))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    ax.plot(steps, ab, color=ACC, linewidth=2, label="Base", zorder=3)
    ax.fill_between(steps, ab, alpha=0.07, color=ACC)
    if res_i:
        sd2 = res_i["step_dist"]
        ab2 = np.array([sd2[t,~tmask].sum() for t in steps])
        ax.plot(steps, ab2, color=GOOD, linewidth=2, label="Mejorado", zorder=3)
        ax.fill_between(steps, ab2, alpha=0.07, color=GOOD)
        ax.legend(fontsize=7, frameon=False)
    ax.set_xlabel("Paso", fontsize=7.5, color=FG_D)
    ax.set_ylabel("Usuarios activos", fontsize=7.5, color=FG_D)
    ax.tick_params(labelsize=7, colors=FG_D)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["bottom","left"]].set_color(BORD)
    ax.grid(color=BORD, linewidth=0.5, zorder=0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{int(v):,}"))
    fig.tight_layout(pad=0.6)
    return fig

def chart_profiles(res_b):
    cats   = ["success","abandon","reject","error"]
    colors = [GOOD, BAD, WARN, FG_D]
    lbls   = ["Aceptado","Abandono","Rechazado","Error"]
    x = np.arange(len(PROFILES))
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    bot = np.zeros(len(PROFILES))
    for cat, col, lbl in zip(cats, colors, lbls):
        vals = np.array([res_b["prof_out"][i][cat] for i in range(len(PROFILES))], float)
        ax.bar(x, vals, bottom=bot, color=col, alpha=0.85, label=lbl, zorder=3)
        bot += vals
    ax.set_xticks(x)
    ax.set_xticklabels([p[1] for p in PROFILES], rotation=20, ha="right", fontsize=7, color=FG_M)
    ax.set_ylabel("Usuarios", fontsize=7.5, color=FG_D)
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["bottom","left"]].set_color(BORD)
    ax.grid(axis="y", color=BORD, linewidth=0.5, zorder=0)
    ax.tick_params(labelsize=7, colors=FG_D)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{int(v):,}"))
    fig.tight_layout(pad=0.6)
    return fig

def chart_outcomes_pie(res):
    oc = res["outcome"]
    vals  = [oc["success"], oc["abandon"], oc["reject"], oc["error"]]
    labs  = ["Aceptado","Abandono","Rechazado","Error"]
    cols  = [GOOD, BAD, WARN, FG_D]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    wedges, texts, autotexts = ax.pie(
        vals, labels=labs, colors=cols, autopct="%1.1f%%",
        startangle=140, wedgeprops=dict(edgecolor=SURF, linewidth=2),
        textprops=dict(color=FG_M, fontsize=8))
    for at in autotexts:
        at.set_fontsize(7.5); at.set_color(SURF); at.set_fontweight("bold")
    ax.set_title(f"n = {res['n']:,} usuarios", fontsize=8, color=FG_D)
    fig.tight_layout(pad=0.3)
    return fig

def chart_top_abandon(res):
    ab_idx = STATE_IDX["S32"]
    flows  = [(i, int(res["counts"][i, ab_idx])) for i in range(N_STATES)
              if terminal_of(i) is None and res["counts"][i, ab_idx] > 0]
    flows.sort(key=lambda x: x[1], reverse=True)
    top = flows[:8]
    if not top:
        return None
    lbls = [f"{STATE_IDS[i]} {STATE_NAMES[i][:18]}" for i,_ in top]
    vals = [v for _,v in top]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    cols = [BAD if j==0 else ACC for j in range(len(top))]
    ax.barh(lbls[::-1], vals[::-1], color=cols[::-1], height=0.6, zorder=3)
    for i, v in enumerate(vals[::-1]):
        ax.text(v+0.3, i, str(v), va="center", fontsize=8, color=FG_M, fontweight="600")
    ax.set_xlabel("Usuarios perdidos", fontsize=7.5, color=FG_D)
    ax.tick_params(labelsize=7.5, colors=FG_M)
    ax.spines[["top","right","bottom"]].set_visible(False)
    ax.spines["left"].set_color(BORD)
    ax.grid(axis="x", color=BORD, linewidth=0.5, zorder=0)
    fig.tight_layout(pad=0.6)
    return fig

# ── KPI card HTML ──────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, detail="", delta=None, pos=True):
    d = ""
    if delta is not None:
        cls   = "pos" if pos else "neg"
        arrow = "▲" if pos else "▼"
        d = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    det = f'<div class="kpi-detail">{detail}</div>' if detail else ""
    return (f'<div class="kpi">'
            f'<div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'{det}{d}</div>')

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:.8rem 0 .4rem;">
      <div style="font-size:1.6rem;">🏗️</div>
      <div style="font-weight:800;font-size:1rem;color:#14120C;">Colombia Comparte</div>
      <div style="font-size:.72rem;color:#9A968B;margin-top:2px;">Simulación Programa EDIFICA</div>
    </div>
    <hr style="border:none;border-top:1px solid #E3E1DA;margin:.6rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("**⚙️ Parámetros de Simulación**")
    n_usuarios = st.slider("Usuarios a simular", 100, 5000, 1500, 100,
                           help="Número de trayectorias Monte Carlo")
    max_pasos  = st.slider("Máximo de pasos por usuario", 5, 60, 25,
                           help="Límite de transiciones por recorrido")
    seed_val   = st.number_input("Semilla aleatoria", value=42, min_value=0,
                                  max_value=9999, step=1)
    scenario   = st.selectbox("Escenario", ["base","improved"],
                               format_func=lambda x: "📊 Base" if x=="base" else "✅ Mejorado")

    st.markdown('<hr style="border:none;border-top:1px solid #E3E1DA;margin:.6rem 0;">',
                unsafe_allow_html=True)

    run_btn = st.button("▶ Ejecutar Simulación", type="primary", use_container_width=True)

    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown('<hr style="border:none;border-top:1px solid #E3E1DA;margin:.6rem 0;">',
                unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:.72rem;color:#9A968B;line-height:1.7;">
      <b style="color:#5C594F;">Estados terminales</b><br>
      ✅ S28 – Aceptado<br>
      ❌ S30 – Rechazado<br>
      🚫 S32 – Abandono<br>
      ⚠️ S33 – Error técnico<br><br>
      <b style="color:#5C594F;">5 perfiles de usuario</b><br>
      P1 Explorador casual (35%)<br>
      P2 Referido directo (22%)<br>
      P3 Candidato motivado (20%)<br>
      P4 Usuario recurrente (15%)<br>
      P5 Reintento post-error (8%)
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:.67rem;color:#9A968B;margin-top:1rem;">
      Universidad Santo Tomás<br>Seccional Tunja · 2026
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION TRIGGER
# ══════════════════════════════════════════════════════════════════════════════
if "res_base" not in st.session_state:
    st.session_state.res_base = None
    st.session_state.res_imp  = None

if run_btn or st.session_state.res_base is None:
    with st.spinner("Ejecutando simulación Markov…"):
        st.session_state.res_base = simulate(n_usuarios, max_pasos, "base",     int(seed_val))
        st.session_state.res_imp  = simulate(n_usuarios, max_pasos, "improved", int(seed_val))
    st.balloons()

res_b = st.session_state.res_base
res_i = st.session_state.res_imp

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="edifica-header">
  <h1>EDIFICA · Simulación Markov <span>Programa Colombia Comparte</span></h1>
  <div style="font-size:.7rem;color:#9A968B;">
    Universidad Santo Tomás · Seccional Tunja · 2026
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">🏗️ Colombia Comparte · Programa EDIFICA</div>
  <h2>Dashboard de Simulación</h2>
  <p>Modelo de Cadenas de Márkov aplicado al flujo de inscripción al Programa EDIFICA.
     Visualiza estados, matrices, recorridos, resultados y recomendaciones de mejora en tiempo real.</p>
  <div class="hero-tags">
    <span class="hero-tag">📋 33 Estados</span>
    <span class="hero-tag">🔀 Cadenas de Márkov</span>
    <span class="hero-tag">👤 5 Perfiles</span>
    <span class="hero-tag">🎲 Monte Carlo</span>
    <span class="hero-tag">🏛️ Universidad Santo Tomás · Tunja</span>
    <span class="hero-tag">📅 2026</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stop here if no simulation yet ─────────────────────────────────────────────
if res_b is None:
    st.info("Presiona **▶ Ejecutar Simulación** en la barra lateral para iniciar.")
    st.stop()

# ── DERIVED METRICS ────────────────────────────────────────────────────────────
n      = res_b["n"]
oc_b   = res_b["outcome"]
oc_i   = res_i["outcome"]
conv_b = oc_b["success"] / n * 100
conv_i = oc_i["success"] / n * 100
Δconv  = conv_i - conv_b
abd_b  = oc_b["abandon"] / n * 100
abd_i  = oc_i["abandon"] / n * 100
Δabd   = abd_b - abd_i
avg_sb = res_b["avg_steps"].get("success", 0)
crit   = res_b["critical"]
crit_name = STATE_NAMES[crit["idx"]] if crit["idx"] >= 0 else "—"
crit_id   = STATE_IDS[crit["idx"]]   if crit["idx"] >= 0 else "—"
crit_rate = crit["abandon_rate"] * 100

# ── KPI ROW ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="kpi-row">'
    + kpi_card("📋","Estados del modelo","33","Nodos de la cadena")
    + kpi_card("👥","Usuarios simulados", f"{n:,}", "Muestra generada")
    + kpi_card("✅","Tasa de éxito (base)", f"{conv_b:.1f}%",
               f"{oc_b['success']:,} usuarios")
    + kpi_card("✅","Tasa de éxito (mejor.)", f"{conv_i:.1f}%",
               delta=f"+{Δconv:.1f}pp", pos=True)
    + kpi_card("❌","Tasa de abandono", f"{abd_b:.1f}%",
               f"{oc_b['abandon']:,} usuarios")
    + kpi_card("🚨","Estado crítico",
               crit_name[:12]+("…" if len(crit_name)>12 else ""),
               f"{crit_rate:.0f}% abandono", delta=crit_id, pos=False)
    + '</div>',
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
(tab_resumen, tab_estados, tab_recorridos,
 tab_matrices, tab_sim, tab_resultados, tab_diag) = st.tabs([
    "📋 Resumen",
    "🗂️ Estados",
    "🔀 Recorridos",
    "📐 Matrices",
    "📈 Simulación",
    "📊 Resultados",
    "🔧 Diagnóstico",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — RESUMEN
# ══════════════════════════════════════════════════════════════════════════════
with tab_resumen:
    st.markdown("""
    <div class="card">
      <h3>Resumen ejecutivo del modelo</h3>
      <p style="font-size:.85rem;color:#5C594F;margin:0 0 .8rem;">
        Visión general de la metodología, flujo analítico y tipos de resultado del simulador.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="outcome-row">
      <div class="outcome-card success">
        <h4>✅ Resultado exitoso</h4>
        <p>El usuario completa todo el flujo de inscripción al Programa EDIFICA y llega al estado
        <b>S28 – Aceptado</b>. Se mide la tasa de conversión y los pasos promedio hasta el éxito.</p>
      </div>
      <div class="outcome-card abandon">
        <h4>🚫 Abandono voluntario</h4>
        <p>El usuario abandona el proceso en algún punto del flujo llegando al estado
        <b>S32 – Abandono</b>. El diagnóstico identifica el estado previo más frecuente.</p>
      </div>
      <div class="outcome-card error">
        <h4>⚠️ Error técnico</h4>
        <p>El usuario llega al estado <b>S33 – Error técnico</b>. Puede reintentar via
        <b>S31</b> o terminar en abandono. El escenario mejorado reduce esta tasa.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns([1.1, 1], gap="medium")
    with r1:
        st.markdown('<div class="card"><h3>Distribución de resultados (base)</h3>',
                    unsafe_allow_html=True)
        show_img(chart_outcomes_pie(res_b))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Embudo de conversión</h3>',
                    unsafe_allow_html=True)
        show_img(chart_funnel(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="card">
          <h3>Resumen de simulación</h3>
          <div class="diag-row">
            <span class="diag-label">Usuarios simulados:</span>
            <span class="diag-val">{n:,}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Pasos máximos:</span>
            <span class="diag-val">{res_b['max_steps']}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Semilla aleatoria:</span>
            <span class="diag-val">{res_b['seed']}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Pasos prom. éxito:</span>
            <span class="diag-val">{avg_sb:.1f}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Pasos prom. abandono:</span>
            <span class="diag-val">{res_b['avg_steps'].get('abandon',0):.1f}</span>
          </div>
          <hr style="border:none;border-top:1px solid {BORD};margin:.6rem 0;">
          <table class="cmp-table">
            <thead>
              <tr>
                <th>Resultado</th>
                <th class="r">Base</th>
                <th class="r">Mejorado</th>
                <th class="r">Δ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>✅ Aceptados</td>
                <td class="r">{oc_b['success']:,}</td>
                <td class="r">{oc_i['success']:,}</td>
                <td class="pos">+{oc_i['success']-oc_b['success']:,}</td>
              </tr>
              <tr>
                <td>🚫 Abandonos</td>
                <td class="r">{oc_b['abandon']:,}</td>
                <td class="r">{oc_i['abandon']:,}</td>
                <td class="pos">−{oc_b['abandon']-oc_i['abandon']:,}</td>
              </tr>
              <tr>
                <td>❌ Rechazados</td>
                <td class="r">{oc_b['reject']:,}</td>
                <td class="r">{oc_i['reject']:,}</td>
                <td class="neu">{oc_i['reject']-oc_b['reject']:+,}</td>
              </tr>
              <tr>
                <td>⚠️ Errores</td>
                <td class="r">{oc_b['error']:,}</td>
                <td class="r">{oc_i['error']:,}</td>
                <td class="neu">{oc_i['error']-oc_b['error']:+,}</td>
              </tr>
              <tr class="total">
                <td>Tasa de éxito</td>
                <td class="r">{conv_b:.2f}%</td>
                <td class="r">{conv_i:.2f}%</td>
                <td class="pos">+{Δconv:.2f}pp</td>
              </tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Metodología</h3>', unsafe_allow_html=True)
        st.markdown("""
        <ul style="font-size:.83rem;color:#5C594F;line-height:1.7;padding-left:1.2rem;margin:0;">
          <li><b>Modelo:</b> Cadena de Márkov de Tiempo Discreto (DTMC)</li>
          <li><b>Estados:</b> 33 nodos que representan pantallas y acciones</li>
          <li><b>Terminales:</b> S28 (éxito), S30 (rechazo), S32 (abandono), S33 (error)</li>
          <li><b>Perfiles:</b> 5 arquetipos con peso y estado inicial diferenciado</li>
          <li><b>Simulación:</b> Monte Carlo con semilla determinista</li>
          <li><b>Escenario mejorado:</b> S17 abandono 42% → 16%</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — ESTADOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_estados:
    st.markdown('<div class="card"><h3>33 Estados del modelo</h3>', unsafe_allow_html=True)
    st.caption("Todas las pantallas y acciones posibles dentro de la plataforma.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Filters
    cf1, cf2, cf3 = st.columns([2, 1.5, 1])
    with cf1:
        busq = st.text_input("🔍 Buscar estado", placeholder="Ej: S17 o formulario")
    with cf2:
        grupos_uniq = list(dict.fromkeys(s[2] for s in STATES))
        sel_grupos  = st.multiselect("Grupo", grupos_uniq, default=grupos_uniq)
    with cf3:
        tipos_uniq  = list(dict.fromkeys(
            ("Terminal" if s[3].startswith("terminal:") else s[3]) for s in STATES))
        sel_tipos   = st.multiselect("Tipo", tipos_uniq, default=tipos_uniq)

    rows = []
    for s in STATES:
        grp  = s[2]
        kind = "Terminal" if s[3].startswith("terminal:") else s[3]
        term = s[3].split(":")[1].upper() if s[3].startswith("terminal:") else ""
        if grp not in sel_grupos: continue
        if kind not in sel_tipos: continue
        if busq and busq.lower() not in (s[0]+s[1]+grp+kind).lower(): continue
        rows.append({"Código": s[0], "Nombre": s[1], "Grupo": grp,
                     "Tipo": kind, "Terminal": term})
    df_estados = pd.DataFrame(rows)
    st.dataframe(df_estados, use_container_width=True, hide_index=True,
                 column_config={
                     "Código":   st.column_config.TextColumn("Código",   width=80),
                     "Nombre":   st.column_config.TextColumn("Nombre",   width=230),
                     "Grupo":    st.column_config.TextColumn("Grupo",    width=120),
                     "Tipo":     st.column_config.TextColumn("Tipo",     width=90),
                     "Terminal": st.column_config.TextColumn("Terminal", width=90),
                 })
    st.caption(f"Mostrando {len(df_estados)} de {N_STATES} estados.")

    # Transition probabilities per state
    st.markdown('<hr class="edifica">', unsafe_allow_html=True)
    st.markdown("**Transiciones desde un estado**")
    sel_state = st.selectbox("Seleccionar estado", STATE_IDS,
                             format_func=lambda x: f"{x} – {STATE_NAMES[STATE_IDX[x]]}")
    si = STATE_IDX[sel_state]
    M  = res_b["M"]
    tr_rows = [(STATE_IDS[j], STATE_NAMES[j], round(float(M[si,j]),4))
               for j in range(N_STATES) if M[si,j] > 0.001]
    tr_rows.sort(key=lambda x: x[2], reverse=True)
    st.dataframe(
        pd.DataFrame(tr_rows, columns=["Destino","Nombre","Probabilidad"]),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — RECORRIDOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_recorridos:
    rc1, rc2 = st.columns([1, 1], gap="medium")
    with rc1:
        st.markdown('<div class="card"><h3>Ruta principal (funnel path)</h3>',
                    unsafe_allow_html=True)
        for idx_f, sid in enumerate(FUNNEL_PATH):
            i    = STATE_IDX[sid]
            grp  = STATES[i][2]
            name = STATE_NAMES[i]
            color= GROUP_COLORS.get(grp,"#F4F3EE")
            arrow = "↓" if idx_f < len(FUNNEL_PATH)-1 else "🏁"
            vis  = res_b["visits"][i]
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:.6rem;'
                f'margin-bottom:.3rem;">'
                f'<div style="width:32px;height:32px;border-radius:8px;'
                f'background:{color};display:flex;align-items:center;'
                f'justify-content:center;font-size:.68rem;font-weight:700;'
                f'color:{FG_M};">{sid}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-size:.82rem;font-weight:600;color:{FG};">{name}</div>'
                f'<div style="font-size:.68rem;color:{FG_D};">{grp} · {vis:,} visitas</div>'
                f'</div>'
                f'<div style="font-size:.9rem;color:{FG_D};">{arrow}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with rc2:
        st.markdown('<div class="card"><h3>Visitas por estado (top 15)</h3>',
                    unsafe_allow_html=True)
        top_vis = sorted(range(N_STATES), key=lambda i: res_b["visits"][i], reverse=True)[:15]
        vis_df  = pd.DataFrame({
            "Estado": [f"{STATE_IDS[i]} · {STATE_NAMES[i]}" for i in top_vis],
            "Grupo":  [STATES[i][2] for i in top_vis],
            "Visitas": [res_b["visits"][i] for i in top_vis],
        })
        st.dataframe(vis_df, use_container_width=True, hide_index=True, height=360)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Top estados previos al abandono</h3>',
                    unsafe_allow_html=True)
        fig_ab = chart_top_abandon(res_b)
        if fig_ab:
            show_img(fig_ab, "Estados no terminales con mayor flujo hacia S32 (Abandono)")
        else:
            st.info("Sin datos de abandono en esta simulación.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Profiles
    st.markdown('<div class="card"><h3>Perfiles de usuario — pesos de inicio</h3>',
                unsafe_allow_html=True)
    p1, p2, p3, p4, p5 = st.columns(5)
    for col, p in zip([p1,p2,p3,p4,p5], PROFILES):
        with col:
            po = res_b["prof_out"][PROFILES.index(p)]
            tot= sum(po.values())
            pct= po["success"]/tot*100 if tot else 0
            st.markdown(
                f'<div style="background:{SURF};border:1px solid {BORD};border-radius:10px;'
                f'padding:.8rem;text-align:center;">'
                f'<div style="font-size:.65rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.06em;color:{FG_D};">{p[0]}</div>'
                f'<div style="font-size:.85rem;font-weight:700;color:{FG};margin:.25rem 0;">{p[1]}</div>'
                f'<div style="font-size:.72rem;color:{FG_M};">Inicio: {p[2]}</div>'
                f'<div style="font-size:.72rem;color:{FG_M};">Peso: {p[3]*100:.0f}%</div>'
                f'<div style="font-size:.9rem;font-weight:700;color:{GOOD};margin-top:.3rem;">'
                f'{pct:.1f}% éxito</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — MATRICES
# ══════════════════════════════════════════════════════════════════════════════
with tab_matrices:
    m1, m2 = st.columns([1, 1.1], gap="medium")
    with m1:
        st.markdown('<div class="card"><h3>Mapa de calor — Matriz de transición</h3>',
                    unsafe_allow_html=True)
        show_img(chart_heatmap(res_b),
                 "Probabilidades de transición (escenario base). Filas = origen · Columnas = destino.")
        st.markdown("</div>", unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="card"><h3>Matriz interactiva (escenario base)</h3>',
                    unsafe_allow_html=True)
        M_df = pd.DataFrame(
            res_b["M"],
            index  =[f"{s[0]} · {s[1]}" for s in STATES],
            columns=[s[0] for s in STATES],
        )
        st.dataframe(
            M_df.style.background_gradient(cmap="Blues", vmin=0, vmax=1).format("{:.3f}"),
            use_container_width=True, height=500,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Scenario diff
    st.markdown('<div class="card"><h3>Diferencia entre escenarios (Mejorado − Base)</h3>',
                unsafe_allow_html=True)
    Mb = build_matrix("base")
    Mi = build_matrix("improved")
    diff = Mi - Mb
    diff_df = pd.DataFrame(diff,
                           index  =[f"{s[0]} · {s[1]}" for s in STATES],
                           columns=[s[0] for s in STATES])
    st.dataframe(
        diff_df.style.background_gradient(cmap="RdYlGn", vmin=-0.3, vmax=0.3).format("{:.3f}"),
        use_container_width=True, height=350,
    )
    st.caption("Verde = probabilidad aumentó en escenario mejorado · Rojo = probabilidad disminuyó")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — SIMULACIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tab_sim:
    s1, s2 = st.columns([1.1, 1.4], gap="medium")
    with s1:
        st.markdown('<div class="card"><h3>Embudo de conversión (base vs mejorado)</h3>',
                    unsafe_allow_html=True)
        show_img(chart_funnel(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Usuarios activos por paso</h3>',
                    unsafe_allow_html=True)
        show_img(chart_stepchart(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="card">
          <h3>⚠️ Estado crítico detectado</h3>
          <div class="diag-row">
            <span class="diag-label">Estado:</span>
            <span class="diag-val">{crit_id} · {crit_name}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Tasa de abandono:</span>
            <span class="diag-val" style="color:{BAD};">{crit_rate:.1f}%</span>
            <span class="diag-badge">CRÍTICO</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Usuarios perdidos:</span>
            <span class="diag-val">{crit['abandon_flow']:,}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Flujo total saliente:</span>
            <span class="diag-val">{crit['outflow']:,}</span>
          </div>
          <p style="font-size:.79rem;color:{FG_M};margin-top:.65rem;line-height:1.6;">
            En el escenario <b>mejorado</b>, la probabilidad de abandono en
            <b>S17 (Plan de negocio)</b> baja de
            <b style="color:{BAD};">42%</b> a <b style="color:{GOOD};">16%</b>,
            aumentando la conversión en
            <b style="color:{GOOD};">+{Δconv:.1f} pp</b>.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Distribución de resultados</h3>',
                    unsafe_allow_html=True)
        show_img(chart_outcomes_pie(res_b))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Resultados por perfil</h3>',
                    unsafe_allow_html=True)
        show_img(chart_profiles(res_b))
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_resultados:
    res1, res2 = st.columns(2, gap="medium")

    with res1:
        st.markdown('<div class="card"><h3>Detalle de visitas por estado</h3>',
                    unsafe_allow_html=True)
        vis_full = pd.DataFrame({
            "Estado": [f"{STATE_IDS[i]} · {STATE_NAMES[i]}" for i in range(N_STATES)],
            "Grupo":  [STATES[i][2] for i in range(N_STATES)],
            "Visitas base":     res_b["visits"].tolist(),
            "Visitas mejorado": res_i["visits"].tolist(),
            "Δ visitas":        (res_i["visits"] - res_b["visits"]).tolist(),
        }).sort_values("Visitas base", ascending=False).reset_index(drop=True)
        st.dataframe(vis_full, use_container_width=True, height=420)
        st.markdown("</div>", unsafe_allow_html=True)

    with res2:
        st.markdown('<div class="card"><h3>Resultados por perfil — Detalle</h3>',
                    unsafe_allow_html=True)
        prof_rows = []
        for pi, p in enumerate(PROFILES):
            po    = res_b["prof_out"][pi]
            total = sum(po.values())
            prof_rows.append({
                "Perfil":     p[1],
                "Aceptado":   po["success"],
                "Abandono":   po["abandon"],
                "Rechazado":  po["reject"],
                "Error":      po["error"],
                "En proceso": po["inprocess"],
                "% Éxito":    f'{po["success"]/total*100:.1f}%' if total else "0%",
            })
        prof_df = pd.DataFrame(prof_rows)
        st.dataframe(prof_df, use_container_width=True, height=230)
        st.markdown("</div>", unsafe_allow_html=True)

        # Export
        st.markdown('<div class="card"><h3>Exportar resultados</h3>',
                    unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        with e1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                vis_full.to_excel(writer, sheet_name="Visitas",    index=False)
                prof_df.to_excel( writer, sheet_name="Perfiles",   index=False)
                M_df.to_excel(    writer, sheet_name="Matriz")
                pd.DataFrame([
                    {"Escenario":"Base",
                     **{k.capitalize():v for k,v in oc_b.items()},
                     "Tasa_exito_%":f"{conv_b:.2f}"},
                    {"Escenario":"Mejorado",
                     **{k.capitalize():v for k,v in oc_i.items()},
                     "Tasa_exito_%":f"{conv_i:.2f}"},
                ]).to_excel(writer, sheet_name="Comparativa", index=False)
            buf.seek(0)
            st.download_button("⬇ Excel", buf, "edifica_simulacion.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        with e2:
            st.download_button("⬇ CSV", vis_full.to_csv(index=False),
                               "edifica_visitas.csv", "text/csv",
                               use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — DIAGNÓSTICO
# ══════════════════════════════════════════════════════════════════════════════
with tab_diag:
    d1, d2 = st.columns([1, 1.1], gap="medium")

    with d1:
        st.markdown(f"""
        <div class="card">
          <h3>🔍 Diagnóstico — Estado crítico</h3>
          <div class="diag-row">
            <span class="diag-label">Estado identificado:</span>
            <span class="diag-val">{crit_id}</span>
            <span class="diag-badge">CRÍTICO</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Nombre:</span>
            <span class="diag-val">{crit_name}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Usuarios perdidos:</span>
            <span class="diag-val" style="color:{BAD};">{crit['abandon_flow']:,}</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Tasa de abandono:</span>
            <span class="diag-val" style="color:{BAD};">{crit_rate:.1f}%</span>
          </div>
          <div class="diag-row">
            <span class="diag-label">Flujo saliente total:</span>
            <span class="diag-val">{crit['outflow']:,}</span>
          </div>
          <hr style="border:none;border-top:1px solid {BORD};margin:.7rem 0;">
          <h4 style="font-size:.88rem;color:{FG};margin:0 0 .4rem;">
            🔎 Análisis del problema
          </h4>
          <p style="font-size:.82rem;color:{FG_M};line-height:1.65;margin:0;">
            El estado <b>{crit_id} – {crit_name}</b> es el punto con mayor pérdida de usuarios
            en la cadena. Con una tasa de abandono del <b style="color:{BAD};">{crit_rate:.1f}%</b>,
            representa el cuello de botella principal del proceso de inscripción.<br><br>
            <b>Causa probable:</b> La carga de documentos complejos (plan de negocio)
            genera alta fricción y deserción antes de completar el requisito.<br><br>
            <b>Acción recomendada:</b> Simplificar el proceso de carga, añadir
            plantillas guía, guardar avance automático y notificaciones de recordatorio.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Top estados con mayor pérdida</h3>',
                    unsafe_allow_html=True)
        fig_ab2 = chart_top_abandon(res_b)
        if fig_ab2:
            show_img(fig_ab2)
        st.markdown("</div>", unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="card">
          <h3>📈 Escenario mejorado — Impacto de la intervención</h3>
          <p style="font-size:.82rem;color:{FG_M};margin:0 0 .8rem;line-height:1.6;">
            Al reducir la probabilidad de abandono en
            <b>S17 (Plan de negocio)</b> de <b style="color:{BAD};">42%</b>
            a <b style="color:{GOOD};">16%</b> (mejora del <b>26 pp</b>),
            el impacto en la conversión global es:
          </p>
          <table class="cmp-table">
            <thead>
              <tr>
                <th>Métrica</th>
                <th class="r">Base</th>
                <th class="r">Mejorado</th>
                <th class="r">Δ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>✅ Aceptados</td>
                <td class="r">{oc_b['success']:,}</td>
                <td class="r">{oc_i['success']:,}</td>
                <td class="pos">+{oc_i['success']-oc_b['success']:,}</td>
              </tr>
              <tr>
                <td>🚫 Abandonos</td>
                <td class="r">{oc_b['abandon']:,}</td>
                <td class="r">{oc_i['abandon']:,}</td>
                <td class="pos">−{oc_b['abandon']-oc_i['abandon']:,}</td>
              </tr>
              <tr>
                <td>❌ Rechazados</td>
                <td class="r">{oc_b['reject']:,}</td>
                <td class="r">{oc_i['reject']:,}</td>
                <td class="neu">{oc_i['reject']-oc_b['reject']:+,}</td>
              </tr>
              <tr>
                <td>⚠️ Errores</td>
                <td class="r">{oc_b['error']:,}</td>
                <td class="r">{oc_i['error']:,}</td>
                <td class="neu">{oc_i['error']-oc_b['error']:+,}</td>
              </tr>
              <tr class="total">
                <td>Tasa de éxito</td>
                <td class="r">{conv_b:.2f}%</td>
                <td class="r">{conv_i:.2f}%</td>
                <td class="pos">+{Δconv:.2f} pp</td>
              </tr>
              <tr class="total">
                <td>Tasa abandono</td>
                <td class="r">{abd_b:.2f}%</td>
                <td class="r">{abd_i:.2f}%</td>
                <td class="pos">−{Δabd:.2f} pp</td>
              </tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Embudo comparativo (Base vs Mejorado)</h3>',
                    unsafe_allow_html=True)
        show_img(chart_funnel(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Usuarios activos por paso (ambos escenarios)</h3>',
                    unsafe_allow_html=True)
        show_img(chart_stepchart(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:2rem;padding-top:1rem;
     border-top:1px solid {BORD};font-size:.7rem;color:{FG_D};">
  Dashboard Colombia Comparte · Programa EDIFICA ·
  Universidad Santo Tomás · Seccional Tunja · 2026
</div>
""", unsafe_allow_html=True)
