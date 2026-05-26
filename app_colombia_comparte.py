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

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDIFICA · Simulación Markov",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Palette — used in matplotlib & inline HTML
C = dict(
    bg="#FAFAF7", surf="#FFFFFF", surf2="#F4F3EE",
    fg="#14120C", fg_m="#5C594F", fg_d="#9A968B",
    acc="#3D4FE0", good="#1F8A5B", bad="#C84B3B",
    warn="#E0A23D", bord="#E3E1DA",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS  — plain string (no f-string) to prevent Streamlit stripping <style>
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --bg:    #FAFAF7; --surf:  #FFFFFF; --surf2: #F4F3EE;
  --fg:    #14120C; --fg-m:  #5C594F; --fg-d:  #9A968B;
  --acc:   #3D4FE0; --good:  #1F8A5B; --bad:   #C84B3B;
  --warn:  #E0A23D; --bord:  #E3E1DA;
}

/* ── reset ── */
html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
  background: var(--bg) !important;
  color: var(--fg) !important;
}
.main .block-container {
  background: var(--bg) !important;
  padding: 2rem 2.5rem 4rem !important;
  max-width: 1380px;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── background grid ── */
.main::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(61,79,224,.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(61,79,224,.035) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none; z-index: 0;
}

/* ── header bar ── */
.app-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--surf); border: 1px solid var(--bord);
  border-radius: 14px; margin-bottom: 1.5rem;
  box-shadow: 0 1px 6px rgba(20,18,12,.06);
}
.app-header-left { display: flex; align-items: center; gap: 1rem; }
.app-header-logo {
  width: 40px; height: 40px; border-radius: 10px;
  background: var(--acc); display: flex; align-items: center;
  justify-content: center; font-size: 1.2rem; flex-shrink: 0;
}
.app-header-title { font-size: 1rem; font-weight: 700; color: var(--fg); line-height: 1.2; }
.app-header-sub   { font-size: .72rem; color: var(--fg-d); margin-top: 1px; }
.app-header-right { font-size: .7rem; color: var(--fg-d); text-align: right; }

/* ── KPI row ── */
.kpi-row {
  display: grid; grid-template-columns: repeat(6,1fr);
  gap: .8rem; margin-bottom: 1.4rem;
}
.kpi {
  background: var(--surf); border: 1px solid var(--bord);
  border-radius: 12px; padding: .9rem 1.1rem;
  box-shadow: 0 1px 4px rgba(20,18,12,.05);
  position: relative; overflow: hidden;
}
.kpi::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  border-radius: 12px 12px 0 0;
  background: var(--acc);
}
.kpi.good::after { background: var(--good); }
.kpi.bad::after  { background: var(--bad);  }
.kpi.warn::after { background: var(--warn); }
.kpi-label {
  font-size: .62rem; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; color: var(--fg-d); margin-bottom: .3rem;
}
.kpi-value {
  font-size: 1.55rem; font-weight: 700; line-height: 1;
  color: var(--fg); font-family: 'IBM Plex Mono', monospace;
}
.kpi-detail { font-size: .68rem; color: var(--fg-d); margin-top: .22rem; }
.kpi-delta  { font-size: .7rem;  margin-top: .22rem; color: var(--fg-m); }
.kpi-delta.up   { color: var(--good); }
.kpi-delta.down { color: var(--bad);  }

/* ── card ── */
.card {
  background: var(--surf); border: 1px solid var(--bord);
  border-radius: 14px; padding: 1.15rem 1.35rem 1.25rem;
  box-shadow: 0 1px 5px rgba(20,18,12,.05); margin-bottom: 1rem;
}
.card-title {
  font-size: .7rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .08em; color: var(--fg-d); margin: 0 0 .8rem;
}
.card-body { font-size: .84rem; color: var(--fg-m); line-height: 1.65; }

/* ── section heading inside tab ── */
.sec-h { font-size: 1rem; font-weight: 700; color: var(--fg); margin: .2rem 0 1rem; }
.sec-p { font-size: .84rem; color: var(--fg-m); line-height: 1.6; margin: -.6rem 0 1rem; }

/* ── outcome chips ── */
.chip-row { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.chip {
  display: inline-flex; align-items: center; gap: .3rem;
  padding: .3rem .75rem; border-radius: 99px;
  font-size: .73rem; font-weight: 600;
}
.chip-acc  { background: #EEF0FD; color: var(--acc); }
.chip-good { background: #E8F5EE; color: var(--good); }
.chip-bad  { background: #FDECEA; color: var(--bad); }
.chip-warn { background: #FEF8E7; color: var(--warn); }
.chip-grey { background: var(--surf2); color: var(--fg-m); }

/* ── outcome big cards ── */
.oc-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: .75rem; margin-bottom: 1.1rem; }
.oc { border-radius: 12px; padding: 1rem 1.1rem; border: 1px solid; }
.oc.s { background: #F0FBF5; border-color: #9BD4B6; }
.oc.a { background: #FDF2F1; border-color: #EFB8B2; }
.oc.e { background: #FEF9ED; border-color: #F0D890; }
.oc-title { font-size: .75rem; font-weight: 700; margin-bottom: .3rem; }
.oc.s .oc-title { color: var(--good); }
.oc.a .oc-title { color: var(--bad);  }
.oc.e .oc-title { color: var(--warn); }
.oc p { font-size: .8rem; color: var(--fg-m); margin: 0; line-height: 1.6; }

/* ── diagnosis row ── */
.dr { display: flex; align-items: baseline; gap: .5rem; margin-bottom: .45rem; }
.dl { font-size: .8rem; color: var(--fg-m); min-width: 9rem; }
.dv {
  font-size: .95rem; font-weight: 700; color: var(--fg);
  font-family: 'IBM Plex Mono', monospace;
}
.badge-crit {
  display: inline-block; padding: 2px 9px; border-radius: 4px;
  font-size: .64rem; font-weight: 700; letter-spacing: .05em;
  text-transform: uppercase; background: #FEF3E2; color: var(--warn);
}
.badge-good {
  display: inline-block; padding: 2px 9px; border-radius: 4px;
  font-size: .64rem; font-weight: 700; letter-spacing: .05em;
  text-transform: uppercase; background: #E8F5EE; color: var(--good);
}

/* ── comparison table ── */
.ct { width: 100%; border-collapse: collapse; font-size: .82rem; }
.ct th {
  text-align: left; font-size: .65rem; text-transform: uppercase;
  letter-spacing: .06em; color: var(--fg-d); padding: 4px 0;
  border-bottom: 1px solid var(--bord); font-weight: 700;
}
.ct th.r, .ct td.r { text-align: right; padding-right: 1rem; }
.ct td { padding: 5px 0; color: var(--fg-m); border-top: 1px solid var(--bord); }
.ct td.mono { font-family: 'IBM Plex Mono', monospace; color: var(--fg); text-align: right; padding-right: 1rem; }
.ct td.pos  { font-family: 'IBM Plex Mono', monospace; color: var(--good); font-weight: 700; text-align: right; }
.ct td.neg  { font-family: 'IBM Plex Mono', monospace; color: var(--bad);  font-weight: 700; text-align: right; }
.ct td.neu  { font-family: 'IBM Plex Mono', monospace; color: var(--fg-m); text-align: right; }
.ct tr.ft td { border-top: 2px solid var(--bord); font-weight: 700; color: var(--fg); }

/* ── funnel path row ── */
.fp-row {
  display: flex; align-items: center; gap: .4rem; margin-bottom: .35rem;
}
.fp-badge {
  flex-shrink: 0; width: 38px; height: 38px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: .62rem; font-weight: 700;
}
.fp-name  { font-size: .84rem; font-weight: 600; color: var(--fg); }
.fp-meta  { font-size: .67rem; color: var(--fg-d); }
.fp-arrow { font-size: .9rem; color: var(--fg-d); margin-left: auto; }

/* ── profile cards ── */
.profile-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: .7rem; margin-top: .5rem; }
.profile-card {
  background: var(--surf); border: 1px solid var(--bord);
  border-radius: 11px; padding: .85rem .9rem; text-align: center;
}
.profile-id   { font-size: .6rem; font-weight: 700; letter-spacing: .07em;
                text-transform: uppercase; color: var(--fg-d); margin-bottom: .2rem; }
.profile-name { font-size: .8rem; font-weight: 700; color: var(--fg); margin-bottom: .2rem; }
.profile-meta { font-size: .68rem; color: var(--fg-d); line-height: 1.5; }
.profile-pct  { font-size: 1rem; font-weight: 700; color: var(--good); margin-top: .3rem; }

/* ── buttons ── */
.stButton > button {
  background: var(--acc) !important; color: #fff !important;
  border: none !important; border-radius: 9px !important;
  font-weight: 600 !important; font-family: 'IBM Plex Sans', sans-serif !important;
  padding: .5rem 1.25rem !important; letter-spacing: .01em !important;
}
.stButton > button:hover { background: #2d3ecc !important; }

/* ── form controls ── */
.stSlider label, .stNumberInput label, .stSelectbox label {
  color: var(--fg-m) !important; font-size: .78rem !important; font-weight: 500 !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surf2) !important; border-radius: 10px !important;
  gap: 2px !important; padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 7px !important; font-weight: 600 !important;
  font-size: .78rem !important; color: var(--fg-m) !important;
  padding: .38rem .9rem !important;
}
.stTabs [aria-selected="true"] {
  background: var(--surf) !important; color: var(--acc) !important;
  box-shadow: 0 1px 4px rgba(20,18,12,.09) !important;
}

/* ── divider ── */
.divider { border: none; border-top: 1px solid var(--bord); margin: .5rem 0 1.1rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DATA MODEL  (handoff data.js)
# ══════════════════════════════════════════════════════════════════════════════
STATES = [
    ("S01","Landing",                 "Acceso",     "page"),
    ("S02","Catálogo de programas",   "Acceso",     "page"),
    ("S03","EDIFICA · Detalle",       "Acceso",     "page"),
    ("S04","Quiz de elegibilidad",    "Acceso",     "page"),
    ("S05","Registro · Inicio",       "Registro",   "page"),
    ("S06","Formulario datos básicos","Registro",   "form"),
    ("S07","Verificación correo",     "Registro",   "verify"),
    ("S08","OTP móvil",               "Registro",   "verify"),
    ("S09","Aceptación T&C",          "Registro",   "form"),
    ("S10","Login",                   "Registro",   "form"),
    ("S11","Perfil personal",         "Perfil",     "form"),
    ("S12","Documento de identidad",  "Perfil",     "upload"),
    ("S13","Comprobante domicilio",   "Perfil",     "upload"),
    ("S14","Información educativa",   "Perfil",     "form"),
    ("S15","Experiencia laboral",     "Perfil",     "form"),
    ("S16","Idea de negocio",         "Proyecto",   "form"),
    ("S17","Plan de negocio",         "Proyecto",   "upload"),   # ← CRITICAL
    ("S18","Modelo financiero",       "Proyecto",   "upload"),
    ("S19","Fotos del proyecto",      "Proyecto",   "upload"),
    ("S20","Pitch en video",          "Proyecto",   "upload"),
    ("S21","Referencias",             "Proyecto",   "form"),
    ("S22","Revisión del resumen",    "Envío",      "page"),
    ("S23","Envío de solicitud",      "Envío",      "action"),
    ("S24","Confirmación",            "Envío",      "page"),
    ("S25","Programar entrevista",    "Evaluación", "form"),
    ("S26","Entrevista realizada",    "Evaluación", "action"),
    ("S27","Decisión",                "Evaluación", "action"),
    ("S28","Aceptado",                "Resultado",  "terminal:success"),
    ("S29","Lista de espera",         "Resultado",  "page"),
    ("S30","Rechazado",               "Resultado",  "terminal:reject"),
    ("S31","Reintento de sesión",     "Soporte",    "action"),
    ("S32","Abandono",                "Resultado",  "terminal:abandon"),
    ("S33","Error técnico",           "Resultado",  "terminal:error"),
]
N        = len(STATES)
N_STATES = N          # alias used in KPI row and captions
IDS      = [s[0] for s in STATES]
NAMES    = [s[1] for s in STATES]
IDX      = {s[0]: i for i, s in enumerate(STATES)}

def term(i):
    k = STATES[i][3]
    return k.split(":")[1] if k.startswith("terminal:") else None

T_RAW = {
    "S01":[("S02",.55,None),("S03",.20,None),("S04",.10,None),("S32",.15,None)],
    "S02":[("S03",.65,None),("S01",.10,None),("S32",.20,None),("S33",.05,None)],
    "S03":[("S04",.45,None),("S05",.30,None),("S02",.10,None),("S32",.15,None)],
    "S04":[("S05",.60,None),("S03",.15,None),("S32",.22,None),("S33",.03,None)],
    "S05":[("S06",.78,None),("S10",.10,None),("S32",.10,None),("S33",.02,None)],
    "S06":[("S07",.70,None),("S33",.08,None),("S32",.22,None)],
    "S07":[("S08",.74,None),("S31",.10,None),("S32",.13,None),("S33",.03,None)],
    "S08":[("S09",.86,None),("S31",.05,None),("S32",.07,None),("S33",.02,None)],
    "S09":[("S11",.90,None),("S32",.08,None),("S33",.02,None)],
    "S10":[("S11",.82,None),("S31",.10,None),("S32",.06,None),("S33",.02,None)],
    "S11":[("S12",.80,None),("S32",.18,None),("S33",.02,None)],
    "S12":[("S13",.74,None),("S32",.22,None),("S33",.04,None)],
    "S13":[("S14",.78,None),("S32",.18,None),("S33",.04,None)],
    "S14":[("S15",.86,None),("S32",.12,None),("S33",.02,None)],
    "S15":[("S16",.84,None),("S32",.14,None),("S33",.02,None)],
    "S16":[("S17",.75,None),("S32",.22,None),("S33",.03,None)],
    "S17":[("S18",.50,.78),("S32",.42,.16),("S33",.08,.06)],   # improved scenario
    "S18":[("S19",.78,None),("S32",.18,None),("S33",.04,None)],
    "S19":[("S20",.72,None),("S32",.24,None),("S33",.04,None)],
    "S20":[("S21",.70,None),("S32",.26,None),("S33",.04,None)],
    "S21":[("S22",.88,None),("S32",.10,None),("S33",.02,None)],
    "S22":[("S23",.92,None),("S32",.06,None),("S33",.02,None)],
    "S23":[("S24",.96,None),("S33",.04,None)],
    "S24":[("S25",.94,None),("S32",.04,None),("S33",.02,None)],
    "S25":[("S26",.90,None),("S32",.08,None),("S33",.02,None)],
    "S26":[("S27",.98,None),("S33",.02,None)],
    "S27":[("S28",.42,None),("S29",.18,None),("S30",.40,None)],
    "S28":[("S28",1.0,None)],
    "S29":[("S28",.30,None),("S30",.40,None),("S32",.30,None)],
    "S30":[("S30",1.0,None)],
    "S31":[("S10",.80,None),("S32",.15,None),("S33",.05,None)],
    "S32":[("S32",1.0,None)],
    "S33":[("S31",.55,None),("S32",.45,None)],
}

PROFILES = [
    ("P1","Explorador casual",    "S01",.35),
    ("P2","Referido directo",     "S03",.22),
    ("P3","Candidato motivado",   "S04",.20),
    ("P4","Usuario recurrente",   "S10",.15),
    ("P5","Reintento post-error", "S31",.08),
]

FUNNEL = ["S01","S05","S09","S11","S16","S17","S18","S21","S22","S23","S27","S28"]

GRP_COLOR = {
    "Acceso":"#EEF0FD","Registro":"#E6F0FA","Perfil":"#F0EBF8",
    "Proyecto":"#FFF3E0","Envío":"#E8F5EE","Evaluación":"#FDECEA",
    "Resultado":"#F4F3EE","Soporte":"#F4F3EE",
}
GRP_TEXT = {
    "Acceso":"#3D4FE0","Registro":"#1B6BB0","Perfil":"#7B3FA6",
    "Proyecto":"#B05E00","Envío":"#1F8A5B","Evaluación":"#C84B3B",
    "Resultado":"#5C594F","Soporte":"#5C594F",
}

# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def build_M(scenario: str) -> np.ndarray:
    M = np.zeros((N, N))
    for fid, edges in T_RAW.items():
        i = IDX[fid]
        for (tid, p1, p2) in edges:
            M[i, IDX[tid]] = p2 if (scenario == "improved" and p2 is not None) else p1
        s = M[i].sum()
        if s > 0: M[i] /= s
    return M

@st.cache_data
def simulate(n: int, max_steps: int, scenario: str, seed: int) -> dict:
    M   = build_M(scenario)
    Mcs = np.cumsum(M, axis=1)
    rng = np.random.default_rng(seed)
    w   = np.array([p[3] for p in PROFILES]); w /= w.sum()
    cw  = np.cumsum(w)

    finals    = np.zeros(N, dtype=int)
    visits    = np.zeros(N, dtype=int)
    step_dist = np.zeros((max_steps+1, N), dtype=int)
    counts    = np.zeros((N, N), dtype=int)
    sto       = {"success":[],"abandon":[],"reject":[],"error":[]}
    prof_out  = [{"success":0,"abandon":0,"reject":0,"error":0,"inprocess":0}
                 for _ in PROFILES]

    for _ in range(n):
        pi = min(int(np.searchsorted(cw, rng.random())), len(PROFILES)-1)
        s  = IDX[PROFILES[pi][2]]
        visits[s]+=1; step_dist[0][s]+=1
        t = term(s); step = 0
        while t is None and step < max_steps:
            nxt = min(int(np.searchsorted(Mcs[s], rng.random())), N-1)
            counts[s,nxt]+=1; s=nxt; step+=1
            visits[s]+=1
            if step<=max_steps: step_dist[step][s]+=1
            t = term(s)
        finals[s]+=1
        if t: sto[t].append(step); prof_out[pi][t]+=1
        else: prof_out[pi]["inprocess"]+=1

    oc = {"success":0,"abandon":0,"reject":0,"error":0,"inprocess":0}
    for i in range(N):
        k = term(i); oc[k if k else "inprocess"]+=finals[i]

    ab_i = IDX["S32"]
    crit = {"idx":-1,"score":0,"flow":0,"rate":0.,"outflow":0}
    for i in range(N):
        if term(i) is not None: continue
        out = int(counts[i].sum())
        if out < 5: continue
        fl  = int(counts[i,ab_i])
        if fl > crit["score"]:
            crit = {"idx":i,"score":fl,"flow":fl,"rate":fl/out,"outflow":out}

    avgs = {k: float(np.mean(v)) if v else 0. for k,v in sto.items()}
    return dict(n=n,ms=max_steps,sc=scenario,seed=seed,
                finals=finals,visits=visits,step_dist=step_dist,
                counts=counts,oc=oc,sto=sto,avgs=avgs,
                prof_out=prof_out,crit=crit,M=M)

# ══════════════════════════════════════════════════════════════════════════════
#  CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight",
                facecolor=C["surf"], transparent=False)
    plt.close(fig); buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def show(fig, cap=""):
    h = f'<img src="data:image/png;base64,{_b64(fig)}" style="width:100%;border-radius:8px;"/>'
    if cap: h += f'<p style="font-size:.66rem;color:{C["fg_d"]};margin-top:4px;">{cap}</p>'
    st.markdown(h, unsafe_allow_html=True)

def _ax_style(ax):
    ax.set_facecolor(C["surf"])
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["bottom","left"]].set_color(C["bord"])
    ax.tick_params(colors=C["fg_d"], labelsize=7)
    ax.grid(axis="y", color=C["bord"], linewidth=.5, zorder=0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{int(v):,}"))

def chart_funnel(rb, ri=None):
    lbl = [NAMES[IDX[s]] for s in FUNNEL]
    bv  = [rb["visits"][IDX[s]] for s in FUNNEL]
    x   = np.arange(len(FUNNEL))
    fig, ax = plt.subplots(figsize=(7.5,4))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    bw = .37 if ri else .62
    ax.bar(x-(bw/2 if ri else 0), bv, width=bw,
           color=C["acc"], alpha=.88, zorder=3, label="Base")
    if ri:
        iv = [ri["visits"][IDX[s]] for s in FUNNEL]
        ax.bar(x+bw/2, iv, width=bw, color=C["good"], alpha=.88, zorder=3, label="Mejorado")
        ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_xticks(x)
    ax.set_xticklabels(lbl, rotation=38, ha="right", fontsize=6.3, color=C["fg_m"])
    ax.set_ylabel("Visitas", fontsize=7.5, color=C["fg_d"])
    _ax_style(ax); ax.spines["left"].set_visible(False)
    fig.tight_layout(pad=.7); return fig

def chart_heatmap(rb):
    M = rb["M"]
    fig, ax = plt.subplots(figsize=(8, 7.8))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    cmap = LinearSegmentedColormap.from_list("e",[C["surf"],"#C7CBF7",C["acc"]],N=256)
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    short = [f"S{i+1:02d}" for i in range(N)]
    ax.set_xticks(range(N)); ax.set_xticklabels(short, fontsize=4.8, rotation=90, color=C["fg_m"])
    ax.set_yticks(range(N)); ax.set_yticklabels(short, fontsize=4.8, color=C["fg_m"])
    ax.set_xlabel("Estado destino", fontsize=7, color=C["fg_d"])
    ax.set_ylabel("Estado origen",  fontsize=7, color=C["fg_d"])
    cb = plt.colorbar(im, ax=ax, fraction=.025, pad=.02)
    cb.ax.tick_params(labelsize=7); cb.outline.set_visible(False)
    fig.tight_layout(pad=.5); return fig

def chart_stepchart(rb, ri=None):
    sd = rb["step_dist"]
    tm = np.array([term(i) is not None for i in range(N)])
    st_ = range(sd.shape[0])
    ab  = np.array([sd[t,~tm].sum() for t in st_])
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    ax.plot(st_, ab, color=C["acc"], lw=2, label="Base", zorder=3)
    ax.fill_between(st_, ab, alpha=.07, color=C["acc"])
    if ri:
        sd2 = ri["step_dist"]
        ab2 = np.array([sd2[t,~tm].sum() for t in st_])
        ax.plot(st_, ab2, color=C["good"], lw=2, label="Mejorado", zorder=3)
        ax.fill_between(st_, ab2, alpha=.07, color=C["good"])
        ax.legend(fontsize=7, frameon=False)
    ax.set_xlabel("Paso", fontsize=7.5, color=C["fg_d"])
    ax.set_ylabel("Usuarios activos", fontsize=7.5, color=C["fg_d"])
    _ax_style(ax); fig.tight_layout(pad=.7); return fig

def chart_profiles(rb):
    cats   = ["success","abandon","reject","error"]
    colors = [C["good"],C["bad"],C["warn"],C["fg_d"]]
    lbls   = ["Aceptado","Abandono","Rechazado","Error"]
    x = np.arange(len(PROFILES))
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    bot = np.zeros(len(PROFILES))
    for cat,col,lbl in zip(cats,colors,lbls):
        v = np.array([rb["prof_out"][i][cat] for i in range(len(PROFILES))],float)
        ax.bar(x, v, bottom=bot, color=col, alpha=.87, label=lbl, zorder=3)
        bot += v
    ax.set_xticks(x)
    ax.set_xticklabels([p[1] for p in PROFILES], rotation=18, ha="right",
                       fontsize=7, color=C["fg_m"])
    ax.set_ylabel("Usuarios", fontsize=7.5, color=C["fg_d"])
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    _ax_style(ax); ax.spines["left"].set_visible(False)
    fig.tight_layout(pad=.7); return fig

def chart_pie(rb):
    oc = rb["oc"]
    vals = [oc["success"],oc["abandon"],oc["reject"],oc["error"]]
    lbls = ["Aceptado","Abandono","Rechazado","Error"]
    cols = [C["good"],C["bad"],C["warn"],C["fg_d"]]
    fig, ax = plt.subplots(figsize=(4.5, 4))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    wedges, _, autotexts = ax.pie(
        vals, labels=lbls, colors=cols, autopct="%1.1f%%",
        startangle=140, wedgeprops=dict(edgecolor=C["surf"], linewidth=2.5),
        textprops=dict(color=C["fg_m"], fontsize=8))
    for at in autotexts:
        at.set_fontsize(7.5); at.set_color("#fff"); at.set_fontweight("bold")
    ax.set_title(f"n = {rb['n']:,} usuarios", fontsize=8, color=C["fg_d"], pad=6)
    fig.tight_layout(pad=.4); return fig

def chart_top_abandon(rb):
    ab_i  = IDX["S32"]
    flows = [(i, int(rb["counts"][i, ab_i])) for i in range(N)
             if term(i) is None and rb["counts"][i, ab_i] > 0]
    flows.sort(key=lambda x: x[1], reverse=True)
    top = flows[:8]
    if not top: return None
    lbls = [f"{IDS[i]}  {NAMES[i][:20]}" for i,_ in top]
    vals = [v for _,v in top]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    cols = [C["bad"] if j==0 else C["acc"] for j in range(len(top))]
    bars = ax.barh(lbls[::-1], vals[::-1], color=cols[::-1], height=.58, zorder=3)
    for bar, v in zip(bars, vals[::-1]):
        ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
                f"{v:,}", va="center", fontsize=8, color=C["fg_m"], fontweight="600")
    ax.set_xlabel("Usuarios perdidos a S32", fontsize=7.5, color=C["fg_d"])
    ax.tick_params(colors=C["fg_m"], labelsize=8)
    ax.spines[["top","right","bottom"]].set_visible(False)
    ax.spines["left"].set_color(C["bord"])
    ax.grid(axis="x", color=C["bord"], linewidth=.5, zorder=0)
    fig.tight_layout(pad=.7); return fig

def chart_diff(Mb, Mi):
    diff = Mi - Mb
    fig, ax = plt.subplots(figsize=(8.5, 7.8))
    fig.patch.set_facecolor(C["surf"]); ax.set_facecolor(C["surf"])
    cmap = LinearSegmentedColormap.from_list("d",[C["bad"],"#F4F3EE",C["good"]],N=256)
    im = ax.imshow(diff, cmap=cmap, vmin=-.4, vmax=.4, aspect="auto")
    short = [f"S{i+1:02d}" for i in range(N)]
    ax.set_xticks(range(N)); ax.set_xticklabels(short, fontsize=4.8, rotation=90, color=C["fg_m"])
    ax.set_yticks(range(N)); ax.set_yticklabels(short, fontsize=4.8, color=C["fg_m"])
    ax.set_xlabel("Estado destino", fontsize=7, color=C["fg_d"])
    ax.set_ylabel("Estado origen",  fontsize=7, color=C["fg_d"])
    cb = plt.colorbar(im, ax=ax, fraction=.025, pad=.02)
    cb.ax.tick_params(labelsize=7); cb.outline.set_visible(False)
    ax.set_title("Δ probabilidades (Mejorado − Base)",
                 fontsize=8, color=C["fg_d"], pad=6)
    fig.tight_layout(pad=.5); return fig

# ── tiny HTML helpers ──────────────────────────────────────────────────────────
def kpi(label, value, detail="", delta=None, pos=True, cls=""):
    dt = ""
    if delta is not None:
        dc = "up" if pos else "down"
        ar = "▲" if pos else "▼"
        dt = f'<div class="kpi-delta {dc}">{ar} {delta}</div>'
    de = f'<div class="kpi-detail">{detail}</div>' if detail else ""
    return (f'<div class="kpi {cls}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{de}{dt}</div>')

def row(*cards):
    return '<div class="kpi-row">' + "".join(cards) + '</div>'

def card(title, body, extra=""):
    return (f'<div class="card"><div class="card-title">{title}</div>'
            f'<div class="card-body">{body}</div>{extra}</div>')

def ct_row(label, b, i, delta, pos=True):
    dc = "pos" if pos else ("neg" if not pos else "neu")
    sign = "+" if pos else "−"
    return (f'<tr><td>{label}</td>'
            f'<td class="mono">{b:,}</td>'
            f'<td class="mono">{i:,}</td>'
            f'<td class="{dc}">{sign}{abs(delta):,}</td></tr>')

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
  <div class="app-header-left">
    <div class="app-header-logo">🏗️</div>
    <div>
      <div class="app-header-title">EDIFICA · Simulación Markov</div>
      <div class="app-header-sub">Programa Colombia Comparte</div>
    </div>
  </div>
  <div class="app-header-right">
    Universidad Santo Tomás · Seccional Tunja<br>
    Cadenas de Márkov · 2026
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PARAMS BAR  (Streamlit native container — HTML wrappers don't work around widgets)
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    pc = st.columns([1.8, 1.8, 1, 2, 1.2], gap="medium")
    with pc[0]: n_u  = st.slider("Usuarios a simular", 100, 5000, 1500, 100)
    with pc[1]: m_p  = st.slider("Máximo de pasos", 5, 60, 25)
    with pc[2]: seed = st.number_input("Semilla", 0, 9999, 42, 1)
    with pc[3]: scen = st.selectbox("Escenario", ["base","improved"],
                                    format_func=lambda x: "📊 Base (sin mejoras)"
                                                if x=="base" else "✅ Mejorado (S17 optimizado)")
    with pc[4]: run  = st.button("▶ Ejecutar", type="primary", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════════════════════
if "rb" not in st.session_state:
    st.session_state.rb = None; st.session_state.ri = None

if run or st.session_state.rb is None:
    with st.spinner("Ejecutando simulación…"):
        st.session_state.rb = simulate(n_u, m_p, "base",     int(seed))
        st.session_state.ri = simulate(n_u, m_p, "improved", int(seed))
    st.balloons()

rb = st.session_state.rb
ri = st.session_state.ri

if rb is None:
    st.info("Presiona **▶ Ejecutar** para iniciar la simulación.")
    st.stop()

# ── Derived ───────────────────────────────────────────────────────────────────
n_sim  = rb["n"]
oc_b   = rb["oc"];  oc_i = ri["oc"]
cb     = oc_b["success"]/n_sim*100;  ci = oc_i["success"]/n_sim*100; Δc = ci-cb
ab     = oc_b["abandon"]/n_sim*100;  ai = oc_i["abandon"]/n_sim*100; Δa = ab-ai
avs    = rb["avgs"].get("success",0)
crit   = rb["crit"]
cn     = NAMES[crit["idx"]] if crit["idx"]>=0 else "—"
cid    = IDS[crit["idx"]]   if crit["idx"]>=0 else "—"
crate  = crit["rate"]*100

# Precompute M_df once (used in Matrices + Resultados tabs)
Mb_arr = build_M("base")
Mi_arr = build_M("improved")
M_df   = pd.DataFrame(Mb_arr,
                      index  =[f"{s[0]} · {s[1]}" for s in STATES],
                      columns=[s[0] for s in STATES])

# ══════════════════════════════════════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    row(
        kpi("Estados del modelo",  "33",        f"{N_STATES} nodos DTMC"),
        kpi("Usuarios simulados",  f"{n_sim:,}", "Muestra generada"),
        kpi("Tasa de éxito · Base", f"{cb:.1f}%", f"{oc_b['success']:,} aceptados",   cls="good"),
        kpi("Tasa de éxito · Mejor.",f"{ci:.1f}%", delta=f"+{Δc:.1f}pp",pos=True,    cls="good"),
        kpi("Tasa de abandono",    f"{ab:.1f}%",  f"{oc_b['abandon']:,} usuarios",   cls="bad"),
        kpi("Estado crítico",
            cid,
            f"{cn[:18]}{'…' if len(cn)>18 else ''}",
            delta=f"{crate:.0f}% abandono", pos=False, cls="warn"),
    ),
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📋 Resumen", "🗂️ Estados", "🔀 Recorridos",
    "📐 Matrices", "📈 Simulación", "📊 Resultados", "🔧 Diagnóstico"
])

# ══════════════════ TAB 1 — RESUMEN ══════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="sec-h">Resumen ejecutivo del modelo</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Visión general de la metodología, resultados de la simulación y comparativa de escenarios.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="oc-grid">
      <div class="oc s">
        <div class="oc-title">✅ Resultado exitoso — S28 Aceptado</div>
        <p>El usuario completa el flujo completo de inscripción al Programa EDIFICA.
           Se mide la tasa de conversión global y los pasos promedio hasta alcanzar este estado.</p>
      </div>
      <div class="oc a">
        <div class="oc-title">🚫 Abandono voluntario — S32 Abandono</div>
        <p>El usuario deserta en algún punto del proceso. El diagnóstico identifica el estado
           previo con mayor flujo hacia el abandono para proponer intervenciones.</p>
      </div>
      <div class="oc e">
        <div class="oc-title">⚠️ Error técnico — S33 Error técnico</div>
        <p>Fallo de plataforma. El usuario puede reintentar vía S31 o terminar en abandono.
           El escenario mejorado optimiza el estado S17 para reducir deserción.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.1], gap="large")
    with c1:
        st.markdown('<div class="card"><div class="card-title">Distribución de resultados (base)</div>', unsafe_allow_html=True)
        show(chart_pie(rb))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Metodología del modelo</div><div class="card-body">', unsafe_allow_html=True)
        st.markdown("""
- **Modelo:** Cadena de Márkov de Tiempo Discreto (DTMC)
- **Estados:** 33 nodos (pantallas y acciones de la plataforma)
- **Terminales:** S28 éxito · S30 rechazo · S32 abandono · S33 error
- **Perfiles:** 5 arquetipos con peso y estado inicial diferenciado
- **Motor:** Monte Carlo con semilla determinista (numpy RNG)
- **Escenario mejorado:** S17 abandono 42 % → 16 %
        """)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">Comparativa de escenarios</div>
          <table class="ct">
            <thead>
              <tr><th>Resultado</th><th class="r">Base</th><th class="r">Mejorado</th><th class="r">Δ</th></tr>
            </thead>
            <tbody>
              {ct_row("✅ Aceptados", oc_b["success"], oc_i["success"], oc_i["success"]-oc_b["success"], True)}
              {ct_row("🚫 Abandonos", oc_b["abandon"], oc_i["abandon"], oc_b["abandon"]-oc_i["abandon"], True)}
              <tr><td>❌ Rechazados</td><td class="mono">{oc_b["reject"]:,}</td><td class="mono">{oc_i["reject"]:,}</td><td class="neu">{oc_i["reject"]-oc_b["reject"]:+,}</td></tr>
              <tr><td>⚠️ Errores téc.</td><td class="mono">{oc_b["error"]:,}</td><td class="mono">{oc_i["error"]:,}</td><td class="neu">{oc_i["error"]-oc_b["error"]:+,}</td></tr>
              <tr><td>⏳ En proceso</td><td class="mono">{oc_b["inprocess"]:,}</td><td class="mono">{oc_i["inprocess"]:,}</td><td class="neu">{oc_i["inprocess"]-oc_b["inprocess"]:+,}</td></tr>
              <tr class="ft"><td>Tasa de éxito</td><td class="mono">{cb:.2f}%</td><td class="mono">{ci:.2f}%</td><td class="pos">+{Δc:.2f}pp</td></tr>
              <tr class="ft"><td>Tasa de abandono</td><td class="mono">{ab:.2f}%</td><td class="mono">{ai:.2f}%</td><td class="pos">−{Δa:.2f}pp</td></tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
          <div class="card-title">Métricas de velocidad</div>
          <div class="dr"><span class="dl">Pasos prom. éxito:</span><span class="dv">{avs:.1f}</span></div>
          <div class="dr"><span class="dl">Pasos prom. abandono:</span><span class="dv">{rb["avgs"].get("abandon",0):.1f}</span></div>
          <div class="dr"><span class="dl">Pasos prom. error:</span><span class="dv">{rb["avgs"].get("error",0):.1f}</span></div>
          <div class="dr"><span class="dl">Pasos máximos:</span><span class="dv">{rb["ms"]}</span></div>
          <div class="dr"><span class="dl">Semilla:</span><span class="dv">{rb["seed"]}</span></div>
          <div class="dr"><span class="dl">Escenario activo:</span>
            <span class="badge-good">{"MEJORADO" if rb["sc"]=="improved" else "BASE"}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════ TAB 2 — ESTADOS ══════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="sec-h">Estados del modelo</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Los 33 nodos que componen la Cadena de Márkov del flujo de inscripción EDIFICA.</p>', unsafe_allow_html=True)

    fa, fb, fc = st.columns([2.5, 1.5, 1.5], gap="small")
    with fa: busq = st.text_input("🔍 Buscar estado", placeholder="Ej: S17  o  formulario  o  Proyecto")
    with fb:
        grps = list(dict.fromkeys(s[2] for s in STATES))
        sel_g = st.multiselect("Grupo", grps, default=grps)
    with fc:
        tip_all = ["page","form","upload","verify","action","terminal"]
        sel_t   = st.multiselect("Tipo", tip_all, default=tip_all)

    rows_e = []
    for s in STATES:
        kind = "terminal" if s[3].startswith("terminal:") else s[3]
        tout = s[3].split(":")[1].upper() if s[3].startswith("terminal:") else ""
        if s[2] not in sel_g: continue
        if kind not in sel_t: continue
        if busq and busq.lower() not in (s[0]+s[1]+s[2]+kind).lower(): continue
        rows_e.append({"Código":s[0],"Nombre":s[1],"Grupo":s[2],
                       "Tipo":kind,"Terminal":tout,
                       "Visitas (base)":int(rb["visits"][IDX[s[0]]])})
    df_e = pd.DataFrame(rows_e)
    st.dataframe(df_e, use_container_width=True, hide_index=True,
                 column_config={
                     "Código":        st.column_config.TextColumn("Código",  width=80),
                     "Nombre":        st.column_config.TextColumn("Nombre",  width=220),
                     "Grupo":         st.column_config.TextColumn("Grupo",   width=115),
                     "Tipo":          st.column_config.TextColumn("Tipo",    width=85),
                     "Terminal":      st.column_config.TextColumn("Terminal",width=90),
                     "Visitas (base)":st.column_config.NumberColumn("Visitas",format="%d",width=90),
                 })
    st.caption(f"Mostrando {len(df_e)} de {N_STATES} estados.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**Inspector de transiciones por estado**")
    sel_s = st.selectbox("Estado origen", IDS,
                         format_func=lambda x: f"{x} – {NAMES[IDX[x]]}")
    si  = IDX[sel_s]
    trn = [(IDS[j], NAMES[j], round(float(Mb_arr[si,j]),4), round(float(Mi_arr[si,j]),4))
           for j in range(N) if Mb_arr[si,j]>0.001 or Mi_arr[si,j]>0.001]
    trn.sort(key=lambda x: x[2], reverse=True)
    st.dataframe(
        pd.DataFrame(trn, columns=["Destino","Nombre","P (base)","P (mejorado)"]),
        use_container_width=True, hide_index=True,
    )

# ══════════════════ TAB 3 — RECORRIDOS ═══════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="sec-h">Recorridos y flujos</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Ruta principal del proceso, volumen de visitas y flujo hacia abandono por estado.</p>', unsafe_allow_html=True)

    r1, r2 = st.columns([1, 1.2], gap="large")
    with r1:
        st.markdown('<div class="card"><div class="card-title">Ruta principal de conversión</div>', unsafe_allow_html=True)
        for fi, sid in enumerate(FUNNEL):
            i   = IDX[sid]
            grp = STATES[i][2]
            vis = rb["visits"][i]
            bg  = GRP_COLOR.get(grp,"#F4F3EE")
            tx  = GRP_TEXT.get(grp,C["fg_m"])
            arrow = "↓" if fi < len(FUNNEL)-1 else "🏁"
            st.markdown(
                f'<div class="fp-row">'
                f'<div class="fp-badge" style="background:{bg};color:{tx};">{sid}</div>'
                f'<div>'
                f'<div class="fp-name">{NAMES[i]}</div>'
                f'<div class="fp-meta">{grp} · {vis:,} visitas</div>'
                f'</div>'
                f'<div class="fp-arrow">{arrow}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="card"><div class="card-title">Top 12 estados por visitas</div>', unsafe_allow_html=True)
        top_i = sorted(range(N), key=lambda i: rb["visits"][i], reverse=True)[:12]
        vis_df = pd.DataFrame({
            "Estado": [f"{IDS[i]} · {NAMES[i]}" for i in top_i],
            "Grupo":  [STATES[i][2] for i in top_i],
            "Visitas Base":     [int(rb["visits"][i]) for i in top_i],
            "Visitas Mejorado": [int(ri["visits"][i]) for i in top_i],
        })
        st.dataframe(vis_df, use_container_width=True, hide_index=True, height=380)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Top estados previos al abandono (S32)</div>', unsafe_allow_html=True)
        fig_ab = chart_top_abandon(rb)
        if fig_ab:
            show(fig_ab, "Estados no terminales con mayor flujo directo hacia S32 (Abandono)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Perfiles de usuario — características y resultados</div>', unsafe_allow_html=True)
    st.markdown('<div class="profile-grid">', unsafe_allow_html=True)
    for pi, p in enumerate(PROFILES):
        po  = rb["prof_out"][pi]
        tot = sum(po.values())
        pct = po["success"]/tot*100 if tot else 0
        st.markdown(
            f'<div class="profile-card">'
            f'<div class="profile-id">{p[0]}</div>'
            f'<div class="profile-name">{p[1]}</div>'
            f'<div class="profile-meta">Inicio: {p[2]}<br>Peso: {p[3]*100:.0f}%</div>'
            f'<div class="profile-pct">{pct:.1f}% éxito</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════ TAB 4 — MATRICES ═════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="sec-h">Matrices de transición</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Mapa de calor y tabla interactiva de las probabilidades de transición entre los 33 estados.</p>', unsafe_allow_html=True)

    m1, m2 = st.columns([1.05, 1], gap="large")
    with m1:
        st.markdown('<div class="card"><div class="card-title">Mapa de calor — 33 × 33 (escenario base)</div>', unsafe_allow_html=True)
        show(chart_heatmap(rb),
             "Filas = estado origen · Columnas = estado destino · Color = probabilidad de transición")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Diferencia entre escenarios (Mejorado − Base)</div>', unsafe_allow_html=True)
        show(chart_diff(Mb_arr, Mi_arr),
             "Verde = probabilidad aumentó · Rojo = probabilidad disminuyó · Solo S17 cambia")
        st.markdown('</div>', unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="card"><div class="card-title">Tabla interactiva — Escenario base</div>', unsafe_allow_html=True)
        # Display as plain rounded DataFrame — avoids Styler issues on 33x33
        st.dataframe(
            M_df.round(3),
            use_container_width=True,
            height=530,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # State-filtered view
        st.markdown('<div class="card"><div class="card-title">Vista filtrada por estado origen</div>', unsafe_allow_html=True)
        sel_m = st.selectbox("Estado", IDS, key="mat_sel",
                             format_func=lambda x: f"{x} – {NAMES[IDX[x]]}")
        mi = IDX[sel_m]
        row_df = pd.DataFrame({
            "Destino": [f"{IDS[j]} · {NAMES[j]}" for j in range(N) if Mb_arr[mi,j]>0.001],
            "P (base)":    [round(float(Mb_arr[mi,j]),4) for j in range(N) if Mb_arr[mi,j]>0.001],
            "P (mejorado)":[round(float(Mi_arr[mi,j]),4) for j in range(N) if Mb_arr[mi,j]>0.001],
        }).sort_values("P (base)", ascending=False).reset_index(drop=True)
        st.dataframe(row_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════ TAB 5 — SIMULACIÓN ═══════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="sec-h">Simulación Markov · Monte Carlo</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Embudo de conversión, evolución temporal de usuarios activos y resultados por perfil.</p>', unsafe_allow_html=True)

    s1, s2 = st.columns([1.1, 1], gap="large")
    with s1:
        st.markdown('<div class="card"><div class="card-title">Embudo de conversión — Base vs Mejorado</div>', unsafe_allow_html=True)
        show(chart_funnel(rb, ri))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Usuarios activos por paso</div>', unsafe_allow_html=True)
        show(chart_stepchart(rb, ri))
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">⚠️ Estado crítico detectado</div>
          <div class="dr">
            <span class="dl">Estado:</span>
            <span class="dv">{cid}</span>
            <span class="badge-crit">CRÍTICO</span>
          </div>
          <div class="dr">
            <span class="dl">Nombre:</span>
            <span class="dv" style="font-size:.82rem;">{cn}</span>
          </div>
          <div class="dr">
            <span class="dl">Tasa de abandono:</span>
            <span class="dv" style="color:{C["bad"]};">{crate:.1f}%</span>
          </div>
          <div class="dr">
            <span class="dl">Usuarios perdidos:</span>
            <span class="dv">{crit["flow"]:,}</span>
          </div>
          <div class="dr">
            <span class="dl">Flujo saliente:</span>
            <span class="dv">{crit["outflow"]:,}</span>
          </div>
          <hr style="border:none;border-top:1px solid {C["bord"]};margin:.7rem 0;">
          <p style="font-size:.81rem;color:{C["fg_m"]};line-height:1.65;margin:0;">
            En el escenario <b>mejorado</b>, la probabilidad de abandono en
            <b>S17 (Plan de negocio)</b> baja de
            <b style="color:{C["bad"]};">42%</b>
            a <b style="color:{C["good"]};">16%</b>,
            incrementando la conversión global en
            <b style="color:{C["good"]};">+{Δc:.1f} puntos porcentuales</b>.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Distribución de resultados</div>', unsafe_allow_html=True)
        show(chart_pie(rb))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Resultados por perfil de usuario</div>', unsafe_allow_html=True)
        show(chart_profiles(rb))
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════ TAB 6 — RESULTADOS ═══════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="sec-h">Resultados detallados</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Visitas por estado, detalle por perfil de usuario y exportación de datos.</p>', unsafe_allow_html=True)

    re1, re2 = st.columns([1.1, 1], gap="large")
    with re1:
        st.markdown('<div class="card"><div class="card-title">Visitas por estado — todos los estados</div>', unsafe_allow_html=True)
        vis_full = pd.DataFrame({
            "Estado":           [f"{IDS[i]} · {NAMES[i]}" for i in range(N)],
            "Grupo":            [STATES[i][2] for i in range(N)],
            "Visitas Base":     rb["visits"].tolist(),
            "Visitas Mejorado": ri["visits"].tolist(),
            "Δ Visitas":        (ri["visits"]-rb["visits"]).tolist(),
        }).sort_values("Visitas Base", ascending=False).reset_index(drop=True)
        st.dataframe(vis_full, use_container_width=True, height=420)
        st.markdown('</div>', unsafe_allow_html=True)

    with re2:
        st.markdown('<div class="card"><div class="card-title">Resultados por perfil de usuario</div>', unsafe_allow_html=True)
        prows = []
        for pi, p in enumerate(PROFILES):
            po  = rb["prof_out"][pi]
            tot = sum(po.values())
            prows.append({"Perfil":p[1],
                          "✅ Aceptado":po["success"],"🚫 Abandono":po["abandon"],
                          "❌ Rechazado":po["reject"],"⚠️ Error":po["error"],
                          "⏳ En proceso":po["inprocess"],
                          "% Éxito":f'{po["success"]/tot*100:.1f}%' if tot else "0%"})
        prof_df = pd.DataFrame(prows)
        st.dataframe(prof_df, use_container_width=True, hide_index=True, height=230)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Exportar resultados</div>', unsafe_allow_html=True)
        ex1, ex2 = st.columns(2)
        with ex1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                vis_full.to_excel(w, sheet_name="Visitas",     index=False)
                prof_df.to_excel( w, sheet_name="Perfiles",    index=False)
                M_df.to_excel(    w, sheet_name="Matriz Base")
                pd.DataFrame([
                    {"Escenario":"Base",    **{k.capitalize():v for k,v in oc_b.items()}, "Tasa_%":f"{cb:.2f}"},
                    {"Escenario":"Mejorado",**{k.capitalize():v for k,v in oc_i.items()}, "Tasa_%":f"{ci:.2f}"},
                ]).to_excel(w, sheet_name="Comparativa", index=False)
            buf.seek(0)
            st.download_button("⬇ Excel (.xlsx)", buf, "edifica_simulacion.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        with ex2:
            st.download_button("⬇ CSV", vis_full.to_csv(index=False),
                               "edifica_visitas.csv", "text/csv",
                               use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Top estados por abandono generado</div>', unsafe_allow_html=True)
        fig_ab = chart_top_abandon(rb)
        if fig_ab:
            show(fig_ab)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════ TAB 7 — DIAGNÓSTICO ══════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="sec-h">Diagnóstico y recomendaciones</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-p">Identificación del estado crítico, análisis de causa y comparativa del impacto del escenario mejorado.</p>', unsafe_allow_html=True)

    d1, d2 = st.columns([1, 1.1], gap="large")
    with d1:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">🔍 Estado crítico identificado</div>
          <div class="dr">
            <span class="dl">Código:</span>
            <span class="dv">{cid}</span>
            <span class="badge-crit">CRÍTICO</span>
          </div>
          <div class="dr">
            <span class="dl">Nombre:</span>
            <span class="dv" style="font-size:.84rem;">{cn}</span>
          </div>
          <div class="dr">
            <span class="dl">Grupo:</span>
            <span class="dv" style="font-size:.84rem;">
              {STATES[crit["idx"]][2] if crit["idx"]>=0 else "—"}
            </span>
          </div>
          <div class="dr">
            <span class="dl">Tasa de abandono:</span>
            <span class="dv" style="color:{C["bad"]};">{crate:.1f}%</span>
          </div>
          <div class="dr">
            <span class="dl">Usuarios perdidos:</span>
            <span class="dv">{crit["flow"]:,}</span>
          </div>
          <div class="dr">
            <span class="dl">Flujo total saliente:</span>
            <span class="dv">{crit["outflow"]:,}</span>
          </div>
          <hr style="border:none;border-top:1px solid {C["bord"]};margin:.75rem 0;">
          <p style="font-size:.82rem;color:{C["fg_m"]};line-height:1.68;margin:0;">
            <b>Causa probable:</b> La carga obligatoria de un plan de negocio completo
            en <b>S17</b> genera alta fricción. Muchos usuarios no tienen el documento
            listo o desconocen los requisitos exactos del formato.<br><br>
            <b>Acción recomendada:</b> Introducir plantillas descargables, guardar avance
            automático, enviar recordatorios por correo y permitir carga parcial con
            plazo de gracia.<br><br>
            <b>Efecto esperado:</b> Reducir la tasa de abandono en S17 del
            <b style="color:{C["bad"]};">42%</b> al <b style="color:{C["good"]};">16%</b>,
            aumentando la conversión global en
            <b style="color:{C["good"]};">+{Δc:.1f} pp</b>.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Top estados con mayor pérdida de usuarios</div>', unsafe_allow_html=True)
        fig_ab2 = chart_top_abandon(rb)
        if fig_ab2:
            show(fig_ab2, "El estado marcado en rojo es el crítico detectado automáticamente")
        st.markdown('</div>', unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">📈 Impacto del escenario mejorado</div>
          <p style="font-size:.82rem;color:{C["fg_m"]};margin:0 0 .9rem;line-height:1.65;">
            Intervención en <b>S17 (Plan de negocio)</b>: reducción de probabilidad de
            abandono de <b style="color:{C["bad"]};">42%</b>
            a <b style="color:{C["good"]};">16%</b>.
          </p>
          <table class="ct">
            <thead>
              <tr><th>Métrica</th><th class="r">Base</th><th class="r">Mejorado</th><th class="r">Δ</th></tr>
            </thead>
            <tbody>
              {ct_row("✅ Aceptados",  oc_b["success"], oc_i["success"], oc_i["success"]-oc_b["success"], True)}
              {ct_row("🚫 Abandonos",  oc_b["abandon"],  oc_i["abandon"],  oc_b["abandon"]-oc_i["abandon"],  True)}
              <tr><td>❌ Rechazados</td><td class="mono">{oc_b["reject"]:,}</td><td class="mono">{oc_i["reject"]:,}</td><td class="neu">{oc_i["reject"]-oc_b["reject"]:+,}</td></tr>
              <tr><td>⚠️ Errores</td><td class="mono">{oc_b["error"]:,}</td><td class="mono">{oc_i["error"]:,}</td><td class="neu">{oc_i["error"]-oc_b["error"]:+,}</td></tr>
              <tr class="ft"><td>Tasa de éxito</td><td class="mono">{cb:.2f}%</td><td class="mono">{ci:.2f}%</td><td class="pos">+{Δc:.2f}pp</td></tr>
              <tr class="ft"><td>Tasa de abandono</td><td class="mono">{ab:.2f}%</td><td class="mono">{ai:.2f}%</td><td class="pos">−{Δa:.2f}pp</td></tr>
            </tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Embudo — Base vs Mejorado</div>', unsafe_allow_html=True)
        show(chart_funnel(rb, ri))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Curva de usuarios activos por paso</div>', unsafe_allow_html=True)
        show(chart_stepchart(rb, ri))
        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr class="divider">
<div style="text-align:center;font-size:.7rem;color:{C["fg_d"]};">
  Dashboard Colombia Comparte · Programa EDIFICA ·
  Universidad Santo Tomás · Seccional Tunja · 2026
</div>
""", unsafe_allow_html=True)
