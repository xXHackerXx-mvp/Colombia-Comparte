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
    initial_sidebar_state="collapsed",
)

# ── COLOURS ────────────────────────────────────────────────────────────────────
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

# ── CSS ────────────────────────────────────────────────────────────────────────
# NOTE: use plain string (no f-string) to avoid Streamlit stripping <style> blocks.
# Colours are declared as CSS custom properties in :root.
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
  max-width: 1300px;
}
#MainMenu, footer, header { visibility: hidden; }

/* background dot-grid */
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

/* header */
.edifica-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 1.5rem;
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 12px;
  margin-bottom: 1.2rem;
  box-shadow: 0 1px 4px rgba(20,18,12,.06);
}
.edifica-header h1 {
  font-size: 1.1rem; font-weight: 700; color: var(--fg); margin: 0;
  letter-spacing: -0.01em;
}
.edifica-header h1 span {
  font-size: .8rem; font-weight: 400; color: var(--fg-d); margin-left: .5rem;
}

/* KPI row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: .7rem;
  margin-bottom: 1.2rem;
}
.kpi {
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 10px;
  padding: .8rem 1rem;
  box-shadow: 0 1px 3px rgba(20,18,12,.05);
}
.kpi-label {
  font-size: .65rem; font-weight: 600; letter-spacing: .06em;
  text-transform: uppercase; color: var(--fg-d); margin-bottom: .3rem;
}
.kpi-value {
  font-size: 1.5rem; font-weight: 700; line-height: 1; color: var(--fg);
  font-family: 'IBM Plex Mono', monospace;
}
.kpi-delta { font-size: .7rem; margin-top: .25rem; color: var(--fg-m); }
.kpi-delta.pos { color: var(--good); }
.kpi-delta.neg { color: var(--bad);  }

/* cards */
.card {
  background: var(--surf);
  border: 1px solid var(--bord);
  border-radius: 12px;
  padding: 1rem 1.2rem 1.1rem;
  box-shadow: 0 1px 4px rgba(20,18,12,.05);
  margin-bottom: .9rem;
}
.card h3 {
  font-size: .75rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .07em; color: var(--fg-d); margin: 0 0 .7rem 0;
}

/* diagnosis */
.diag-row { display: flex; align-items: baseline; gap: .5rem; margin-bottom: .45rem; }
.diag-label { font-size: .82rem; color: var(--fg-m); }
.diag-val {
  font-size: 1rem; font-weight: 700; color: var(--fg);
  font-family: 'IBM Plex Mono', monospace;
}
.diag-badge {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: .68rem; font-weight: 600; background: #FEF3E2; color: var(--warn);
}

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
  gap: 2px; padding: 3px;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 6px !important; font-weight: 600 !important;
  font-size: .8rem !important; color: var(--fg-m) !important;
  padding: .35rem .85rem !important;
}
.stTabs [aria-selected="true"] {
  background: var(--surf) !important; color: var(--acc) !important;
  box-shadow: 0 1px 3px rgba(20,18,12,.1) !important;
}

hr.edifica { border: none; border-top: 1px solid var(--bord); margin: .5rem 0 1rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DATA MODEL
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
    ("S17","Plan de negocio",         "Proyecto",    "upload"),   # CRITICAL STATE
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
    """Return terminal kind ('success','abandon','reject','error') or None."""
    kind = STATES[i][3]
    return kind.split(":")[1] if kind.startswith("terminal:") else None

# Transition table: {from_id: [(to_id, p_base, p_improved|None), …]}
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
    # S17 = CRITICAL: abandono baja de 42% → 16% en escenario mejorado
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
        row_sum = M[i].sum()
        if row_sum > 0:
            M[i] /= row_sum
    return M


@st.cache_data
def simulate(n: int, max_steps: int, scenario: str, seed: int) -> dict:
    M = build_matrix(scenario)
    rng = np.random.default_rng(seed)

    weights = np.array([p[3] for p in PROFILES], dtype=float)
    weights /= weights.sum()
    cum_w = np.cumsum(weights)

    finals    = np.zeros(N_STATES, dtype=int)
    visits    = np.zeros(N_STATES, dtype=int)
    step_dist = np.zeros((max_steps + 1, N_STATES), dtype=int)
    counts    = np.zeros((N_STATES, N_STATES), dtype=int)
    steps_to_outcome = {"success": [], "abandon": [], "reject": [], "error": []}
    profile_outcomes = [
        {"success": 0, "abandon": 0, "reject": 0, "error": 0, "inprocess": 0}
        for _ in PROFILES
    ]

    M_cs = np.cumsum(M, axis=1)   # precomputed cumsum rows

    for _ in range(n):
        r0    = rng.random()
        p_idx = int(np.searchsorted(cum_w, r0))
        p_idx = min(p_idx, len(PROFILES) - 1)
        s     = STATE_IDX[PROFILES[p_idx][2]]

        visits[s]       += 1
        step_dist[0][s] += 1
        terminal = terminal_of(s)
        step = 0

        while terminal is None and step < max_steps:
            nxt = int(np.searchsorted(M_cs[s], rng.random()))
            nxt = min(nxt, N_STATES - 1)
            counts[s, nxt] += 1
            s = nxt
            step += 1
            visits[s] += 1
            if step <= max_steps:
                step_dist[step][s] += 1
            terminal = terminal_of(s)

        finals[s] += 1
        if terminal:
            steps_to_outcome[terminal].append(step)
            profile_outcomes[p_idx][terminal] += 1
        else:
            profile_outcomes[p_idx]["inprocess"] += 1

    outcome = {"success": 0, "abandon": 0, "reject": 0, "error": 0, "inprocess": 0}
    for i in range(N_STATES):
        t = terminal_of(i)
        outcome[t if t else "inprocess"] += finals[i]

    abandon_idx = STATE_IDX["S32"]
    critical = {"idx": -1, "score": 0, "abandon_flow": 0, "abandon_rate": 0.0, "outflow": 0}
    for i in range(N_STATES):
        if terminal_of(i) is not None:
            continue
        outflow = int(counts[i].sum())
        if outflow < 5:
            continue
        ab_flow = int(counts[i, abandon_idx])
        if ab_flow > critical["score"]:
            critical = {
                "idx": i, "score": ab_flow, "abandon_flow": ab_flow,
                "abandon_rate": ab_flow / outflow, "outflow": outflow,
            }

    avg_steps = {
        k: float(np.mean(v)) if v else 0.0
        for k, v in steps_to_outcome.items()
    }

    return {
        "n": n, "max_steps": max_steps, "scenario": scenario, "seed": seed,
        "finals": finals, "visits": visits, "step_dist": step_dist, "counts": counts,
        "outcome": outcome, "steps_to_outcome": steps_to_outcome,
        "avg_steps": avg_steps, "profile_outcomes": profile_outcomes,
        "critical": critical, "M": M,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=SURF, transparent=False)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def render_img(fig, caption=""):
    b64 = fig_to_b64(fig)
    html = f'<img src="data:image/png;base64,{b64}" style="width:100%;border-radius:6px;"/>'
    if caption:
        html += f'<p style="font-size:.67rem;color:{FG_D};margin-top:3px;">{caption}</p>'
    st.markdown(html, unsafe_allow_html=True)

def chart_funnel(res_b, res_i=None):
    labels = [STATE_NAMES[STATE_IDX[s]] for s in FUNNEL_PATH]
    bvis   = [res_b["visits"][STATE_IDX[s]] for s in FUNNEL_PATH]
    x      = np.arange(len(FUNNEL_PATH))

    fig, ax = plt.subplots(figsize=(7, 3.9))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

    bw = 0.37 if res_i else 0.6
    ax.bar(x - (bw/2 if res_i else 0), bvis, width=bw,
           color=ACC, alpha=0.85, zorder=3, label="Base")
    if res_i:
        ivis = [res_i["visits"][STATE_IDX[s]] for s in FUNNEL_PATH]
        ax.bar(x + bw/2, ivis, width=bw,
               color=GOOD, alpha=0.85, zorder=3, label="Mejorado")
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

    cmap = LinearSegmentedColormap.from_list("edifica",
        [SURF, "#C7CBF7", ACC], N=256)
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    short = [f"S{i+1:02d}" for i in range(N_STATES)]
    ax.set_xticks(range(N_STATES))
    ax.set_xticklabels(short, fontsize=5, rotation=90, color=FG_M)
    ax.set_yticks(range(N_STATES))
    ax.set_yticklabels(short, fontsize=5, color=FG_M)
    ax.set_xlabel("Estado destino", fontsize=7, color=FG_D)
    ax.set_ylabel("Estado origen",  fontsize=7, color=FG_D)
    cb = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cb.ax.tick_params(labelsize=7)
    fig.tight_layout(pad=0.5)
    return fig

def chart_stepchart(res_b, res_i=None):
    sd_b   = res_b["step_dist"]
    t_mask = np.array([terminal_of(i) is not None for i in range(N_STATES)])
    steps  = range(sd_b.shape[0])
    act_b  = np.array([sd_b[t, ~t_mask].sum() for t in steps])

    fig, ax = plt.subplots(figsize=(7, 3.2))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

    ax.plot(steps, act_b, color=ACC, linewidth=2, label="Base", zorder=3)
    ax.fill_between(steps, act_b, alpha=0.07, color=ACC)
    if res_i:
        sd_i  = res_i["step_dist"]
        act_i = np.array([sd_i[t, ~t_mask].sum() for t in steps])
        ax.plot(steps, act_i, color=GOOD, linewidth=2, label="Mejorado", zorder=3)
        ax.fill_between(steps, act_i, alpha=0.07, color=GOOD)
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
    labels_cat = ["Aceptado","Abandono","Rechazado","Error"]
    x = np.arange(len(PROFILES))

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

    bottom = np.zeros(len(PROFILES))
    for cat, col, lbl in zip(cats, colors, labels_cat):
        vals = np.array([res_b["profile_outcomes"][i][cat] for i in range(len(PROFILES))], float)
        ax.bar(x, vals, bottom=bottom, color=col, alpha=0.85, label=lbl, zorder=3)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels([p[1] for p in PROFILES], rotation=20, ha="right",
                       fontsize=7, color=FG_M)
    ax.set_ylabel("Usuarios", fontsize=7.5, color=FG_D)
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["bottom","left"]].set_color(BORD)
    ax.grid(axis="y", color=BORD, linewidth=0.5, zorder=0)
    ax.tick_params(labelsize=7, colors=FG_D)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{int(v):,}"))
    fig.tight_layout(pad=0.6)
    return fig

# ── KPI card HTML ──────────────────────────────────────────────────────────────
def kpi(label, value, delta=None, pos=True):
    d = ""
    if delta is not None:
        cls   = "pos" if pos else "neg"
        arrow = "▲" if pos else "▼"
        d = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    return (f'<div class="kpi">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{d}</div>')

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="edifica-header">
  <h1>EDIFICA · Simulación Markov <span>Programa Colombia Comparte</span></h1>
  <div style="font-size:.72rem;color:#9A968B;">
    Universidad Santo Tomás · Seccional Tunja · 2026
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls ───────────────────────────────────────────────────────────────────
cc = st.columns([1.6, 1.6, 1, 1.8, 1], gap="small")
with cc[0]: n_usuarios = st.slider("Usuarios", 200, 5000, 1500, 100)
with cc[1]: max_pasos  = st.slider("Pasos máximos", 5, 50, 25)
with cc[2]: seed_val   = st.number_input("Semilla", value=42, min_value=0,
                                          max_value=9999, step=1)
with cc[3]: scenario   = st.selectbox(
    "Escenario", ["base","improved"],
    format_func=lambda x: "📊 Base (sin mejoras)" if x=="base"
                          else "✅ Mejorado (S17 optimizado)"
)
with cc[4]: run_btn = st.button("▶ Ejecutar", type="primary", use_container_width=True)

st.markdown('<hr class="edifica"/>', unsafe_allow_html=True)

# ── Run simulation ─────────────────────────────────────────────────────────────
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

if res_b is None:
    st.info("Presiona **▶ Ejecutar** para iniciar la simulación.")
    st.stop()

# ── Derived metrics ────────────────────────────────────────────────────────────
n      = res_b["n"]
oc_b   = res_b["outcome"]
oc_i   = res_i["outcome"]
conv_b = oc_b["success"] / n * 100
conv_i = oc_i["success"] / n * 100
Δconv  = conv_i - conv_b
abd_b  = oc_b["abandon"] / n * 100
abd_i  = oc_i["abandon"] / n * 100
Δabd   = abd_b - abd_i
avg_s_b = res_b["avg_steps"].get("success", 0)
crit    = res_b["critical"]
crit_name = STATE_NAMES[crit["idx"]] if crit["idx"] >= 0 else "—"
crit_id   = STATE_IDS[crit["idx"]]   if crit["idx"] >= 0 else "—"
crit_rate = crit["abandon_rate"] * 100

# ── KPI Row ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="kpi-row">'
    + kpi("Tasa de éxito (base)",     f"{conv_b:.1f}%")
    + kpi("Tasa de éxito (mejor.)",   f"{conv_i:.1f}%",   f"+{Δconv:.1f}pp",   True)
    + kpi("Abandono (base)",          f"{abd_b:.1f}%")
    + kpi("Reducción abandono",       f"{Δabd:.1f}pp",    f"−{Δabd:.1f}pp",    True)
    + kpi("Pasos prom. éxito",        f"{avg_s_b:.1f}")
    + kpi("Estado crítico",
          (crit_name[:14]+"…" if len(crit_name) > 14 else crit_name),
          f"{crit_rate:.0f}% ab.", False)
    + '</div>',
    unsafe_allow_html=True,
)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📈 Simulación",
    "🔥 Matriz de transición",
    "📊 Análisis detallado",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — SIMULACIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([1.1, 1.4], gap="medium")

    # ── Left column ────────────────────────────────────────────────────────────
    with left:
        # Funnel
        st.markdown('<div class="card"><h3>Embudo de conversión</h3>',
                    unsafe_allow_html=True)
        render_img(chart_funnel(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

        # Step chart
        st.markdown('<div class="card"><h3>Usuarios activos por paso</h3>',
                    unsafe_allow_html=True)
        render_img(chart_stepchart(res_b, res_i))
        st.markdown("</div>", unsafe_allow_html=True)

        # Diagnosis
        st.markdown(f"""
        <div class="card">
          <h3>⚠️ Diagnóstico — Estado crítico</h3>
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
          <p style="font-size:.78rem;color:{FG_M};margin-top:.65rem;line-height:1.55;">
            En el escenario <b>mejorado</b>, la probabilidad de abandono en
            <b>S17 (Plan de negocio)</b> baja de
            <b style="color:{BAD};">42 %</b> a <b style="color:{GOOD};">16 %</b>,
            aumentando la conversión global en
            <b style="color:{GOOD};">+{Δconv:.1f} puntos porcentuales</b>.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Right column ──────────────────────────────────────────────────────────
    with right:
        # Heatmap
        st.markdown(
            '<div class="card"><h3>Mapa de calor — Matriz de transición (33 × 33)</h3>',
            unsafe_allow_html=True,
        )
        render_img(
            chart_heatmap(res_b),
            "Probabilidades de transición (escenario base). "
            "Filas = estado origen · Columnas = estado destino.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Profiles
        st.markdown('<div class="card"><h3>Resultados por perfil de usuario</h3>',
                    unsafe_allow_html=True)
        render_img(chart_profiles(res_b))
        st.markdown("</div>", unsafe_allow_html=True)

        # Comparison table
        st.markdown(f"""
        <div class="card">
          <h3>Comparativa de escenarios</h3>
          <table style="width:100%;font-size:.81rem;border-collapse:collapse;">
            <thead>
              <tr style="color:{FG_D};font-size:.7rem;text-transform:uppercase;
                         letter-spacing:.05em;">
                <th style="text-align:left;padding:4px 0;">Métrica</th>
                <th style="text-align:right;padding:4px 8px;">Base</th>
                <th style="text-align:right;padding:4px 8px;">Mejorado</th>
                <th style="text-align:right;padding:4px 0;">Δ</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-top:1px solid {BORD};">
                <td style="padding:5px 0;color:{FG_M};">Aceptados</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_b["success"]:,}</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_i["success"]:,}</td>
                <td style="text-align:right;color:{GOOD};font-weight:600;">+{oc_i["success"]-oc_b["success"]:,}</td>
              </tr>
              <tr style="border-top:1px solid {BORD};">
                <td style="padding:5px 0;color:{FG_M};">Abandonos</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_b["abandon"]:,}</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_i["abandon"]:,}</td>
                <td style="text-align:right;color:{GOOD};font-weight:600;">−{oc_b["abandon"]-oc_i["abandon"]:,}</td>
              </tr>
              <tr style="border-top:1px solid {BORD};">
                <td style="padding:5px 0;color:{FG_M};">Rechazados</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_b["reject"]:,}</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_i["reject"]:,}</td>
                <td style="text-align:right;color:{FG_M};">{oc_i["reject"]-oc_b["reject"]:+,}</td>
              </tr>
              <tr style="border-top:1px solid {BORD};">
                <td style="padding:5px 0;color:{FG_M};">Errores técn.</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_b["error"]:,}</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_i["error"]:,}</td>
                <td style="text-align:right;color:{FG_M};">{oc_i["error"]-oc_b["error"]:+,}</td>
              </tr>
              <tr style="border-top:1px solid {BORD};">
                <td style="padding:5px 0;color:{FG_M};">En proceso</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_b["inprocess"]:,}</td>
                <td style="text-align:right;font-family:monospace;padding:5px 8px;">{oc_i["inprocess"]:,}</td>
                <td style="text-align:right;color:{FG_M};">{oc_i["inprocess"]-oc_b["inprocess"]:+,}</td>
              </tr>
              <tr style="border-top:2px solid {BORD};font-weight:700;">
                <td style="padding:6px 0;">Tasa de éxito</td>
                <td style="text-align:right;font-family:monospace;padding:6px 8px;">{conv_b:.2f}%</td>
                <td style="text-align:right;font-family:monospace;padding:6px 8px;">{conv_i:.2f}%</td>
                <td style="text-align:right;color:{GOOD};font-weight:700;">+{Δconv:.2f}pp</td>
              </tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — MATRIZ
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<div class="card"><h3>Matriz de transición estocástica — 33 × 33 estados</h3>',
        unsafe_allow_html=True,
    )
    M_df = pd.DataFrame(
        res_b["M"],
        index  =[f"{s[0]} · {s[1]}" for s in STATES],
        columns=[s[0] for s in STATES],
    )
    st.dataframe(
        M_df.style
            .background_gradient(cmap="Blues", vmin=0, vmax=1)
            .format("{:.3f}"),
        use_container_width=True, height=640,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — ANÁLISIS DETALLADO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    a1, a2 = st.columns(2, gap="medium")

    with a1:
        st.markdown('<div class="card"><h3>Visitas por estado (top 20)</h3>',
                    unsafe_allow_html=True)
        vis_df = (
            pd.DataFrame({
                "Estado":           [f"{STATE_IDS[i]} · {STATE_NAMES[i]}"
                                     for i in range(N_STATES)],
                "Grupo":            [STATES[i][2] for i in range(N_STATES)],
                "Visitas base":     res_b["visits"].tolist(),
                "Visitas mejorado": res_i["visits"].tolist(),
            })
            .sort_values("Visitas base", ascending=False)
            .head(20)
            .reset_index(drop=True)
        )
        st.dataframe(vis_df, use_container_width=True, height=420)
        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        # Profile detail
        st.markdown('<div class="card"><h3>Resultados por perfil — Detalle</h3>',
                    unsafe_allow_html=True)
        prof_rows = []
        for pi, p in enumerate(PROFILES):
            po    = res_b["profile_outcomes"][pi]
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
                vis_df.to_excel(writer,  sheet_name="Visitas",     index=False)
                prof_df.to_excel(writer, sheet_name="Perfiles",    index=False)
                M_df.to_excel(writer,    sheet_name="Matriz")
                pd.DataFrame([
                    {"Escenario": "Base",
                     **{k.capitalize(): v for k, v in oc_b.items()},
                     "Tasa_éxito_%": f"{conv_b:.2f}"},
                    {"Escenario": "Mejorado",
                     **{k.capitalize(): v for k, v in oc_i.items()},
                     "Tasa_éxito_%": f"{conv_i:.2f}"},
                ]).to_excel(writer, sheet_name="Comparativa", index=False)
            buf.seek(0)
            st.download_button(
                "⬇ Descargar Excel", buf, "edifica_simulacion.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with e2:
            st.download_button(
                "⬇ Descargar CSV", vis_df.to_csv(index=False),
                "edifica_visitas.csv", "text/csv",
                use_container_width=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:2rem;padding-top:1rem;
     border-top:1px solid {BORD};font-size:.7rem;color:{FG_D};">
  Dashboard Colombia Comparte · Programa EDIFICA ·
  Universidad Santo Tomás · Seccional Tunja · 2026
</div>
""", unsafe_allow_html=True)
