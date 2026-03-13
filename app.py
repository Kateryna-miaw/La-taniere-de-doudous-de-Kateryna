import streamlit as st
import pandas as pd
import random
import base64
import os

# --- Configuration de la page ---
st.set_page_config(page_title="La Tanière des Doudous de Kateryna 🧸", layout="wide", initial_sidebar_state="expanded")

# --- Gestion du fond d'écran animé ou statique ---
_gif_path = "images/background.gif"
_gif_b64  = ""
if os.path.exists(_gif_path):
    with open(_gif_path, "rb") as _f:
        _gif_b64 = base64.b64encode(_f.read()).decode()
_bg_css = (
    f"background-image: url('data:image/gif;base64,{_gif_b64}') !important;"
    if _gif_b64 else
    "background: linear-gradient(135deg,#f7b8d0,#f0d0e8) !important;"
)

# ── Audio system ──
def _load_audio_b64(path):
    # retourne "" si fichier manquant, streamlit plante pas
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def _audio_mime(path):
    ext = path.rsplit(".", 1)[-1].lower()
    return {"mp3": "audio/mpeg", "ogg": "audio/ogg", "wav": "audio/wav"}.get(ext, "audio/mpeg")

# charger les fichiers audio (on fait ça une fois au démarrage)
_bgm_path       = next((p for p in ["audio/bgm.mp3","audio/bgm.ogg","audio/bgm.wav"] if os.path.exists(p)), "")
_sfx_btn_hover  = next((p for p in ["audio/btn_hover.mp3","audio/btn_hover.ogg","audio/btn_hover.wav"] if os.path.exists(p)), "")
_sfx_btn_click  = next((p for p in ["audio/btn_click.mp3","audio/btn_click.ogg","audio/btn_click.wav"] if os.path.exists(p)), "")
_sfx_plush_hover= next((p for p in ["audio/plush_hover.mp3","audio/plush_hover.MP3","audio/plush_hover.ogg","audio/plush_hover.wav"] if os.path.exists(p)), "")
_sfx_unlock_path= next((p for p in ["audio/unlock.mp3","audio/unlock.MP3","audio/unlock.ogg","audio/unlock.wav"] if os.path.exists(p)), "")
_sfx_calamar_path=next((p for p in ["audio/calamar.mp3","audio/calamar.MP3","audio/calamar.ogg","audio/calamar.wav"] if os.path.exists(p)), "")

_bgm_b64         = _load_audio_b64(_bgm_path)        if _bgm_path         else ""
_sfx_hover_b64   = _load_audio_b64(_sfx_btn_hover)   if _sfx_btn_hover    else ""
_sfx_click_b64   = _load_audio_b64(_sfx_btn_click)   if _sfx_btn_click    else ""
_sfx_plush_b64   = _load_audio_b64(_sfx_plush_hover) if _sfx_plush_hover  else ""
_sfx_unlock_b64  = _load_audio_b64(_sfx_unlock_path) if _sfx_unlock_path  else ""
_sfx_calamar_b64 = _load_audio_b64(_sfx_calamar_path)if _sfx_calamar_path else ""

_bgm_mime     = _audio_mime(_bgm_path)        if _bgm_path         else "audio/mpeg"
_hover_mime   = _audio_mime(_sfx_btn_hover)   if _sfx_btn_hover    else "audio/mpeg"
_click_mime   = _audio_mime(_sfx_btn_click)   if _sfx_btn_click    else "audio/mpeg"
_plush_mime   = _audio_mime(_sfx_plush_hover) if _sfx_plush_hover  else "audio/mpeg"
_unlock_mime  = _audio_mime(_sfx_unlock_path) if _sfx_unlock_path  else "audio/mpeg"
_calamar_mime = _audio_mime(_sfx_calamar_path)if _sfx_calamar_path else "audio/mpeg"

# gif calamar pour l'overlay
_calamar_gif_b64 = ""
if os.path.exists("images/calamar.gif"):
    with open("images/calamar.gif", "rb") as _f:
        _calamar_gif_b64 = base64.b64encode(_f.read()).decode()
_dim_overlay = """
<style>
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(255,220,235,0.52);
    z-index: 0;
    pointer-events: none;
}
</style>
"""

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;500;600;700&family=Nunito:ital,wght@0,400;0,700;0,800;1,400&display=swap');

:root {{
    --glass:       rgba(255,255,255,0.72);
    --glass-card:  rgba(255,252,245,0.88);
    --glass-dark:  rgba(80,30,50,0.55);
    --glass-yellow:rgba(255,240,160,0.92);
    --glass-mint:  rgba(180,235,180,0.88);
    --surface:     rgba(255,255,255,0.92);
    --mint:        #a8d8a8;
    --mint-d:      #5fa85f;
    --peach:       #FFAF9C;
    --peach-d:     #ff8c73;
    --yellow:      #ffeaa0;
    --pink:        #ffb3c6;
    --pink-d:      #e05080;
    --lavender:    #e8d4f0;
    --sky:         #b8e0ff;
    --text:        #1a0810;
    --text-soft:   #5a1030;
    --text-light:  #ffffff;
    --border:      #1a0810;
    --shadow:      4px 4px 0px rgba(26,8,16,0.6);
    --shadow-sm:   2px 2px 0px rgba(26,8,16,0.5);
    --radius:      12px;
    --blur:        blur(10px);
}}

html, body {{
    font-family: 'Nunito', sans-serif !important;
    color: var(--text) !important;
}}
.stApp {{
    {_bg_css}
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-attachment: scroll !important;
    min-height: 100vh !important;
}}
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(255, 210, 230, 0.65);
    z-index: 0;
    pointer-events: none;
}}
/* Calamar GIF is z-index:1 ; main content must be above it */
.stApp > div, .stMainBlockContainer, .stMain, .main {{
    position: relative;
    z-index: 2;
}}
[class*="css"] {{
    background: transparent !important;
}}

.main .block-container {{
    background: rgba(255,240,248,0.72) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    border-radius: 24px !important;
    border: 2px solid rgba(255,255,255,0.5) !important;
    padding: 1.5rem 2rem !important;
    max-width: 1300px !important;
    box-shadow: 0 8px 32px rgba(180,60,100,0.2) !important;
    position: relative;
    z-index: 1;
}}

h1, h2, h3 {{ font-family: 'Pixelify Sans', monospace !important; }}
h1 {{
    font-size: 2.8rem !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    text-shadow: 2px 2px 0px rgba(255,255,255,0.7) !important;
    margin-bottom: 0.2rem !important;
}}
h2 {{ color: #7b1040 !important; -webkit-text-fill-color: #7b1040 !important; }}
h3 {{ color: #5a1030 !important; -webkit-text-fill-color: #5a1030 !important; }}

p, span, label, li, td, th {{ color: var(--text) !important; }}
div {{ color: var(--text); }}
.stMarkdown, .stMarkdown p,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong {{ color: var(--text) !important; }}
.stCaption, [data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color: var(--text-soft) !important;
    -webkit-text-fill-color: var(--text-soft) !important;
    font-weight: 700 !important;
}}

[data-testid="stSidebar"] {{
    background: rgba(255,220,235,0.82) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    border-right: 3px solid var(--border) !important;
    box-shadow: 3px 0 0 rgba(42,16,32,0.3) !important;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}}
[data-testid="stSidebar"] [data-testid="stMetric"] {{
    background: rgba(255,255,255,0.75);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
    padding: 0.6rem 1rem;
    margin-bottom: 0.5rem;
}}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
    font-family: 'Pixelify Sans', monospace !important;
    font-size: 1.8rem !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
    color: var(--text-soft) !important;
    -webkit-text-fill-color: var(--text-soft) !important;
}}

/* ── Audio control pill (mute/unmute) ── */
#audio-control-btn {{
    position: fixed;
    bottom: 1.2rem;
    right: 1.2rem;
    z-index: 10001;
    background: rgba(255,220,235,0.95);
    border: 2.5px solid var(--border);
    border-radius: 50px;
    padding: 0.4rem 0.9rem;
    font-family: 'Pixelify Sans', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    backdrop-filter: blur(8px);
    transition: transform 0.08s, box-shadow 0.08s;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    user-select: none;
}}
#audio-control-btn:hover {{
    transform: translate(-1px,-1px);
    box-shadow: var(--shadow);
}}
#audio-control-btn:active {{
    transform: translate(1px,1px);
    box-shadow: none;
}}

.stButton > button {{
    font-family: 'Pixelify Sans', monospace !important;
    background: rgba(255,200,215,0.9) !important;
    color: var(--text) !important;
    border: 2.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    padding: 0.4rem 1rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
    backdrop-filter: blur(4px) !important;
}}
.stButton > button:hover {{
    transform: translate(-1px, -1px) !important;
    box-shadow: 3px 3px 0px var(--border) !important;
    background: var(--peach-d) !important;
    color: #fff !important;
}}
.stButton > button:active {{
    transform: translate(2px, 2px) !important;
    box-shadow: 0px 0px 0px var(--border) !important;
}}
.stButton > button[kind="primary"] {{
    background: var(--glass-mint) !important;
    border-color: var(--border) !important;
    font-size: 1rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: var(--shadow) !important;
    color: #0e3b0e !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: var(--mint-d) !important;
    color: #fff !important;
    box-shadow: 5px 5px 0px var(--border) !important;
    transform: translate(-2px, -2px) !important;
}}

.stat-bar-wrap {{
    width: 100%;
    margin-bottom: 0.55rem;
}}
.stat-bar-label {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3px;
}}
.stat-bar-label span {{
    font-family: 'Pixelify Sans', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}}
.stat-bar-label .stat-val {{
    font-size: 0.7rem !important;
    font-weight: 900 !important;
    opacity: 0.8;
}}
.stat-bar-track {{
    width: 100%;
    height: 13px;
    background: rgba(26,8,16,0.12);
    border: 2px solid var(--border);
    border-radius: 4px;
    box-shadow: inset 1px 1px 0px rgba(26,8,16,0.1), 2px 2px 0px rgba(26,8,16,0.45);
    overflow: hidden;
    position: relative;
}}
.stat-bar-fill {{
    height: 100%;
    border-radius: 2px;
    transition: width 0.45s cubic-bezier(0.4,0,0.2,1);
    position: relative;
}}
.stat-bar-fill::after {{
    content: '';
    position: absolute;
    top: 1px; left: 4px; right: 4px;
    height: 3px;
    background: rgba(255,255,255,0.35);
    border-radius: 2px;
}}
.bar-energy  {{ background: linear-gradient(90deg, #7dd87d, #3aa83a); }}
.bar-stress  {{ background: linear-gradient(90deg, #ffb347, #e05020); }}
.bar-love    {{ background: linear-gradient(90deg, #ff8fb0, #d0206a); }}

[data-testid="column"] > div > div {{
    background: var(--glass-card) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 2.5px solid rgba(42,16,32,0.7) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin: 0.3rem !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.1s, box-shadow 0.1s !important;
}}
[data-testid="column"] > div > div:hover {{
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px rgba(42,16,32,0.55) !important;
}}

[data-testid="stAlert"] {{
    background: rgba(255,255,255,0.82) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 12px !important;
    border: 2px solid var(--border) !important;
    font-family: 'Nunito', sans-serif !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text) !important;
}}
[data-testid="stAlert"] p, [data-testid="stAlert"] div {{
    color: var(--text) !important;
}}

[data-testid="stSelectbox"] > div, [data-baseweb="select"] {{
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    box-shadow: var(--shadow-sm) !important;
}}

.stRadio > div {{ gap: 0.3rem; }}
.stRadio label {{
    background: rgba(255,240,160,0.88) !important;
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.3rem 0.8rem !important;
    transition: background 0.1s, transform 0.1s;
    cursor: pointer;
    font-size: 0.85rem !important;
    color: var(--text) !important;
    box-shadow: var(--shadow-sm) !important;
}}
.stRadio label:hover {{
    background: var(--peach) !important;
    transform: translate(-1px,-1px);
}}

[data-testid="stExpander"] {{
    background: rgba(255,255,255,0.78) !important;
    backdrop-filter: blur(8px) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow-sm) !important;
}}
[data-testid="stExpander"] summary {{
    font-family: 'Pixelify Sans', monospace !important;
    font-size: 1rem !important;
    color: var(--text) !important;
}}

.card-divider {{
    border: none !important;
    background: transparent !important;
    margin: 0.6rem 0 0.5rem 0 !important;
}}
hr {{
    border: none !important;
    background: transparent !important;
    margin: 1.2rem 0 !important;
}}

[data-testid="stTab"] {{ font-family: 'Pixelify Sans', monospace !important; color: var(--text-soft) !important; }}
[data-testid="stTab"][aria-selected="true"] {{ color: var(--text) !important; border-bottom: 3px solid var(--border) !important; }}
[data-testid="stTabContent"] {{ background: rgba(255,255,255,0.7) !important; border-radius: 0 0 12px 12px !important; }}
[data-testid="stMetricValue"] {{ font-family: 'Pixelify Sans', monospace !important; color: var(--text) !important; }}
[data-testid="stToast"] {{
    background: rgba(255,240,160,0.95) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
    color: var(--text) !important;
}}

::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: rgba(255,200,220,0.3); }}
::-webkit-scrollbar-thumb {{ background: var(--pink-d); border: 2px solid var(--border); border-radius: 4px; }}

/* --- animations peluches --- */
@keyframes plushie-bounce {{
    0%, 100% {{ transform: translateY(0) scale(1); }}
    20%       {{ transform: translateY(-14px) scale(1.05, 0.95); }}
    40%       {{ transform: translateY(-20px) scale(0.95, 1.05); }}
    60%       {{ transform: translateY(-8px) scale(1.02, 0.98); }}
    80%       {{ transform: translateY(-4px) scale(1, 1); }}
}}
@keyframes plushie-wiggle {{
    0%, 100% {{ transform: rotate(0deg) scale(1); }}
    15%       {{ transform: rotate(-6deg) scale(1.04); }}
    30%       {{ transform: rotate(6deg) scale(0.97); }}
    45%       {{ transform: rotate(-5deg) scale(1.03); }}
    60%       {{ transform: rotate(5deg) scale(0.98); }}
    75%       {{ transform: rotate(-3deg) scale(1.01); }}
    90%       {{ transform: rotate(2deg) scale(1); }}
}}
@keyframes plushie-heartbeat {{
    0%, 100% {{ transform: scale(1);    filter: drop-shadow(0 0 0px rgba(255,80,130,0)); }}
    14%       {{ transform: scale(1.12); filter: drop-shadow(0 0 12px rgba(255,80,130,0.85)); }}
    28%       {{ transform: scale(1);    filter: drop-shadow(0 0 4px rgba(255,80,130,0.4)); }}
    42%       {{ transform: scale(1.08); filter: drop-shadow(0 0 10px rgba(255,80,130,0.7)); }}
    70%       {{ transform: scale(1);    filter: drop-shadow(0 0 0px rgba(255,80,130,0)); }}
}}
@keyframes plushie-scared {{
    0%, 100% {{ transform: translateX(0) rotate(0deg); }}
    10%       {{ transform: translateX(-6px) rotate(-3deg); }}
    20%       {{ transform: translateX(6px) rotate(3deg); }}
    30%       {{ transform: translateX(-5px) rotate(-2deg); }}
    40%       {{ transform: translateX(5px) rotate(2deg); }}
    50%       {{ transform: translateX(-4px) rotate(-1deg); }}
    60%       {{ transform: translateX(4px) rotate(1deg); }}
    80%       {{ transform: translateX(-2px); }}
}}
@keyframes plushie-sad-pulse {{
    0%, 100% {{ transform: scale(1);    opacity: 1; }}
    50%       {{ transform: scale(0.94); opacity: 0.7; }}
}}
@keyframes plushie-hover-float {{
    0%, 100% {{ transform: translateY(0); }}
    50%       {{ transform: translateY(-6px); }}
}}

.plushie-anim-wrap {{
    display: inline-block;
    position: relative;
    cursor: pointer;
    transition: filter 0.2s;
}}
.plushie-anim-wrap:hover img,
.plushie-anim-wrap:hover .art-placeholder {{
    animation: plushie-hover-float 0.7s ease-in-out infinite !important;
}}
.plushie-anim-wrap[data-mood="happy"] img,
.plushie-anim-wrap[data-mood="happy"] .art-placeholder {{
    animation: plushie-bounce 0.9s cubic-bezier(0.36,0.07,0.19,0.97) infinite;
}}
.plushie-anim-wrap[data-mood="happy"]:hover img,
.plushie-anim-wrap[data-mood="happy"]:hover .art-placeholder {{
    animation: plushie-bounce 0.6s cubic-bezier(0.36,0.07,0.19,0.97) infinite !important;
}}
.plushie-anim-wrap[data-mood="sad"] img,
.plushie-anim-wrap[data-mood="sad"] .art-placeholder,
.plushie-anim-wrap[data-mood="burnout"] img,
.plushie-anim-wrap[data-mood="burnout"] .art-placeholder {{
    animation: plushie-sad-pulse 2s ease-in-out infinite;
}}
.plushie-anim-wrap[data-mood="sad"]:hover img,
.plushie-anim-wrap[data-mood="sad"]:hover .art-placeholder,
.plushie-anim-wrap[data-mood="burnout"]:hover img,
.plushie-anim-wrap[data-mood="burnout"]:hover .art-placeholder {{
    animation: plushie-wiggle 0.6s ease-in-out infinite !important;
}}
.plushie-anim-wrap[data-mood="scared"] img,
.plushie-anim-wrap[data-mood="scared"] .art-placeholder {{
    animation: plushie-scared 0.4s ease-in-out infinite;
}}
.plushie-anim-wrap[data-mood="winner"] img,
.plushie-anim-wrap[data-mood="winner"] .art-placeholder {{
    animation: plushie-heartbeat 1.4s ease-in-out infinite;
}}
.plushie-anim-wrap[data-mood="winner"]:hover img,
.plushie-anim-wrap[data-mood="winner"]:hover .art-placeholder {{
    animation: plushie-heartbeat 0.8s ease-in-out infinite !important;
}}
.plushie-anim-wrap[data-mood="winner-big"] img,
.plushie-anim-wrap[data-mood="winner-big"] .art-placeholder {{
    animation: plushie-heartbeat 1.2s ease-in-out infinite;
    filter: drop-shadow(0 0 16px rgba(255,80,130,0.6));
}}
.plushie-anim-wrap[data-mood="idle"] img,
.plushie-anim-wrap[data-mood="idle"] .art-placeholder {{
    animation: plushie-bounce 2.5s ease-in-out infinite;
}}
.plushie-anim-wrap[data-mood="idle"]:nth-child(2) img {{ animation-delay: 0.3s; }}
.plushie-anim-wrap[data-mood="idle"]:nth-child(3) img {{ animation-delay: 0.6s; }}

/* --- composants custom --- */
.hero-banner {{
    background: rgba(255,220,235,0.80);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 3px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{ content:'🌸'; position:absolute; top:12px; right:20px; font-size:2.5rem; opacity:0.45; }}
.hero-banner::after  {{ content:'⭐'; position:absolute; bottom:12px; right:60px; font-size:1.8rem; opacity:0.35; }}
.hero-title {{
    font-family: 'Pixelify Sans', monospace;
    font-size: 3rem;
    color: var(--text);
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
    text-shadow: 2px 2px 0px rgba(255,255,255,0.5);
}}
.hero-sub {{
    font-family: 'Nunito', sans-serif;
    color: var(--text-soft);
    font-size: 1rem;
    margin: 0;
    font-weight: 700;
}}
.rule-card {{
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(8px);
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.1s;
}}
.rule-card:hover {{ transform: translate(-1px,-1px); box-shadow: 3px 3px 0px var(--border); }}
.rule-icon  {{ font-size: 1.4rem; flex-shrink: 0; }}
.rule-title {{ font-family: 'Pixelify Sans', monospace; font-size: 0.95rem; color: var(--text); margin: 0 0 0.1rem 0; word-break: keep-all; overflow-wrap: break-word; hyphens: none; }}
.rule-desc  {{ font-size: 0.84rem; color: var(--text-soft); margin: 0; line-height: 1.5; word-break: keep-all; overflow-wrap: break-word; hyphens: none; }}

.plushie-name {{
    font-family: 'Pixelify Sans', monospace;
    font-size: 1.15rem;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    margin-bottom: 0.05rem;
    font-weight: 700;
    text-shadow: 1px 1px 0px rgba(255,255,255,0.6);
    word-break: keep-all; overflow-wrap: break-word; hyphens: none; white-space: nowrap;
}}
.plushie-name.danger {{ color: #900010 !important; -webkit-text-fill-color: #900010 !important; }}
.plushie-name.winner {{ color: #0d500d !important; -webkit-text-fill-color: #0d500d !important; }}

.stat-label {{
    font-size: 0.70rem;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.08rem;
    margin-top: 0.4rem;
    font-weight: 900;
}}
.mood-pill {{
    display: inline-block;
    padding: 0.15rem 0.65rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 800;
    margin-top: 0.35rem;
    margin-bottom: 0.4rem;
    font-family: 'Pixelify Sans', monospace;
    border: 2px solid var(--border);
    box-shadow: 2px 2px 0px var(--border);
}}
.mood-happy {{ background: #c8f5b0; color: #0e3b0e !important; -webkit-text-fill-color: #0e3b0e !important; }}
.mood-sad   {{ background: #bde0ff; color: #082050 !important; -webkit-text-fill-color: #082050 !important; }}
.mood-burn  {{ background: #ffb3b3; color: #600000 !important; -webkit-text-fill-color: #600000 !important; }}
.mood-neut  {{ background: rgba(255,240,160,0.97); color: #3d2800 !important; -webkit-text-fill-color: #3d2800 !important; }}

.day-badge {{
    display: inline-block;
    background: rgba(255,240,160,0.95);
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    font-family: 'Pixelify Sans', monospace;
    font-size: 1rem;
    padding: 0.25rem 1.1rem;
    border-radius: 8px;
    border: 2px solid var(--border);
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    backdrop-filter: blur(4px);
}}
@keyframes shake {{
    0%, 100% {{ transform: translateX(0); }}
    20%       {{ transform: translateX(-4px) rotate(-1deg); }}
    40%       {{ transform: translateX(4px) rotate(1deg); }}
    60%       {{ transform: translateX(-3px); }}
    80%       {{ transform: translateX(3px); }}
}}
.calamar-alert {{ animation: shake 0.5s ease infinite; border-radius: 12px; }}
@keyframes calamar-vignette {{
    0%, 100% {{ box-shadow: inset 0 0 60px rgba(220, 20, 60, 0.3); background: rgba(220, 20, 60, 0.05); }}
    50%       {{ box-shadow: inset 0 0 160px rgba(255, 0, 0, 0.5); background: rgba(255, 0, 0, 0.12); }}
}}
.calamar-screen-overlay {{
    position: fixed; inset: 0; z-index: 9998;
    pointer-events: none;
    animation: calamar-vignette 1.5s ease-in-out infinite;
}}
.action-label {{
    font-family: 'Pixelify Sans', monospace;
    font-size: 0.72rem;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0.3rem 0 0.2rem 0;
    font-weight: 900;
}}
.dialogue-box {{
    background: rgba(255,240,160,0.90);
    backdrop-filter: blur(6px);
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 0.7rem 0.9rem;
    margin-top: 0.5rem;
    box-shadow: var(--shadow-sm);
    position: relative;
}}
.dialogue-box::before {{
    content: ''; position: absolute; top:-10px; left:18px;
    width:0; height:0;
    border-left:8px solid transparent; border-right:8px solid transparent;
    border-bottom:10px solid var(--border);
}}
.dialogue-box::after {{
    content: ''; position: absolute; top:-7px; left:20px;
    width:0; height:0;
    border-left:6px solid transparent; border-right:6px solid transparent;
    border-bottom:8px solid rgba(255,240,160,0.90);
}}
.validate-wrapper {{
    background: var(--glass-mint);
    backdrop-filter: blur(8px);
    border: 3px solid var(--border);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
}}
.waiting-text {{
    font-family: 'Pixelify Sans', monospace;
    font-size: 0.95rem;
    color: var(--text-soft);
    background: rgba(255,240,160,0.88);
    border: 2px dashed var(--border);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    display: inline-block;
}}
.planned-action {{
    background: rgba(180,245,160,0.88);
    border: 2px solid var(--border);
    border-radius: 8px;
    padding: 0.35rem 0.7rem;
    font-family: 'Pixelify Sans', monospace;
    font-size: 0.82rem;
    color: #1a4d1a;
    box-shadow: var(--shadow-sm);
    margin-top: 0.3rem;
}}
@keyframes twinkle {{
    0%, 100% {{ opacity:1; transform:scale(1); }}
    50%       {{ opacity:0.5; transform:scale(0.85); }}
}}
.star-deco {{ animation: twinkle 2s ease-in-out infinite; display:inline-block; }}
.art-placeholder {{
    background: rgba(232,212,240,0.80);
    backdrop-filter: blur(6px);
    border: 2px dashed var(--border);
    border-radius: 12px;
    text-align: center;
    padding: 1rem 0.5rem 0.6rem;
    margin-bottom: 0.4rem;
    min-height: 100px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}}
.modal-overlay {{
    position: fixed; inset: 0;
    background: rgba(80,10,40,0.45);
    z-index: 9999;
    display: flex; align-items: center; justify-content: center;
    backdrop-filter: blur(6px);
}}
.modal-card {{
    background: rgba(255,245,200,0.97);
    backdrop-filter: blur(16px);
    border: 4px solid var(--border);
    border-radius: 24px;
    box-shadow: 8px 8px 0px rgba(42,16,32,0.5);
    padding: 2rem 2.5rem;
    text-align: center;
    max-width: 380px; width: 90%;
    position: relative;
    animation: popIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
}}
@keyframes popIn {{
    0%   {{ opacity:0; transform:scale(0.5) rotate(-4deg); }}
    70%  {{ transform:scale(1.06) rotate(1deg); }}
    100% {{ opacity:1; transform:scale(1) rotate(0deg); }}
}}
.modal-card h2 {{ font-family:'Pixelify Sans',monospace; font-size:1.5rem; color:var(--text) !important; -webkit-text-fill-color:var(--text) !important; margin:0.5rem 0 0.3rem; }}
.modal-card p  {{ font-size:0.9rem; color:var(--text-soft) !important; -webkit-text-fill-color:var(--text-soft) !important; margin:0 0 0.6rem; }}
.modal-stars {{ font-size:1.6rem; letter-spacing:4px; margin-bottom:0.5rem; }}
@keyframes floatStar {{
    0%,100% {{ transform:translateY(0) rotate(0deg); }}
    33%      {{ transform:translateY(-8px) rotate(10deg); }}
    66%      {{ transform:translateY(-4px) rotate(-6deg); }}
}}
.float-star {{ display:inline-block; animation:floatStar 2s ease-in-out infinite; }}
.float-star:nth-child(2) {{ animation-delay:0.3s; }}
.float-star:nth-child(3) {{ animation-delay:0.6s; }}
.winner-shelf {{
    background: linear-gradient(135deg, rgba(200,245,176,0.92), rgba(255,240,160,0.88));
    backdrop-filter: blur(10px);
    border: 3px solid var(--border);
    border-radius: 20px;
    padding: 1rem 1.4rem;
    box-shadow: var(--shadow);
    display: flex; align-items: center; gap: 1rem;
    margin-bottom: 0.6rem;
    animation: bounceIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
}}
.winner-shelf-name {{ word-break: keep-all; overflow-wrap: break-word; hyphens: none; white-space: nowrap;
    font-family: 'Pixelify Sans', monospace;
    font-size: 1.05rem;
    color: #0d500d !important; -webkit-text-fill-color: #0d500d !important;
    font-weight: 700; margin: 0 0 0.15rem 0;
}}
.winner-shelf-sub {{
    font-size: 0.78rem;
    color: #2d6e2d !important; -webkit-text-fill-color: #2d6e2d !important;
    margin: 0; font-weight: 700;
}}
@keyframes bounceIn {{
    0%   {{ opacity:0; transform:scale(0.85) translateY(8px); }}
    70%  {{ transform:scale(1.03) translateY(-2px); }}
    100% {{ opacity:1; transform:scale(1) translateY(0); }}
}}
.validate-wrapper p {{
    color: #0e3b0e !important; -webkit-text-fill-color: #0e3b0e !important;
}}
.waiting-text {{
    font-family: 'Pixelify Sans', monospace;
    font-size: 0.95rem;
    color: var(--text) !important; -webkit-text-fill-color: var(--text) !important;
    background: rgba(255,240,160,0.92);
    border: 2px dashed var(--border);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    display: inline-block; font-weight: 800;
}}
</style>
""", unsafe_allow_html=True)
st.markdown(_dim_overlay, unsafe_allow_html=True)

# moteur audio — injecté dans window.parent pour contourner l'isolation iframe
# (j'ai galéré pas mal sur ça, voir commentaires dans _inject_audio_engine)
def _inject_audio_engine():
    """Inject audio engine into window.parent so it can reach all Streamlit DOM elements."""
    bgm_src     = f"data:{_bgm_mime};base64,{_bgm_b64}"             if _bgm_b64          else ""
    hover_src   = f"data:{_hover_mime};base64,{_sfx_hover_b64}"     if _sfx_hover_b64    else ""
    click_src   = f"data:{_click_mime};base64,{_sfx_click_b64}"     if _sfx_click_b64    else ""
    plush_src   = f"data:{_plush_mime};base64,{_sfx_plush_b64}"     if _sfx_plush_b64    else ""
    unlock_src  = f"data:{_unlock_mime};base64,{_sfx_unlock_b64}"   if _sfx_unlock_b64   else ""
    calamar_src = f"data:{_calamar_mime};base64,{_sfx_calamar_b64}" if _sfx_calamar_b64  else ""
    calamar_gif = f"data:image/gif;base64,{_calamar_gif_b64}"       if _calamar_gif_b64  else ""

    # We use st.components.v1.html so the <script> actually executes.
    # All audio objects + DOM elements are created on window.parent (the real Streamlit page),
    # not inside this sandboxed iframe - that's the key to reaching all buttons/plushies.
    html = f"""<!DOCTYPE html><html><body style="margin:0;padding:0;overflow:hidden">
<script>
(function() {{
  // P = the real Streamlit page window
  var P = (window.parent && window.parent !== window) ? window.parent : window;

  // ---- One-time engine init ----
  if (!P._aud) {{
    var bgmSrc     = {repr(bgm_src)};
    var hoverSrc   = {repr(hover_src)};
    var clickSrc   = {repr(click_src)};
    var plushSrc   = {repr(plush_src)};
    var unlockSrc  = {repr(unlock_src)};
    var calamarSrc = {repr(calamar_src)};
    var calamarGif = {repr(calamar_gif)};

    function mk(src, loop, vol) {{
      if (!src) return null;
      var a = new P.Audio(src);
      a.loop = !!loop; a.volume = vol || 0.5; return a;
    }}
    var bgm        = mk(bgmSrc,     true,  0.3);
    var sfxHover   = mk(hoverSrc,  false, 0.55);
    var sfxClick   = mk(clickSrc,  false, 0.7);
    var sfxPlush   = mk(plushSrc,  false, 0.6);
    var sfxUnlock  = mk(unlockSrc,  false, 0.85);
    var sfxCalamar = mk(calamarSrc, true,  0.75);  // loop=true : musique calamar en boucle
    var muted = false, unlocked = false, calamarActive = false;

    function play(sfx) {{
      if (!sfx || muted) return;
      try {{ sfx.currentTime = 0; sfx.play().catch(function(){{}}); }} catch(e) {{}}
    }}

    // Unlock BGM on first user gesture (browser autoplay policy)
    function doUnlock() {{
      if (unlocked) return;
      unlocked = true;
      if (bgm && !muted && !calamarActive) bgm.play().catch(function(){{}});
    }}
    P.document.addEventListener('click',   doUnlock);
    P.document.addEventListener('keydown', doUnlock);

    // Inject CSS into parent DOM
    if (!P.document.getElementById('_aud_style')) {{
      var s = P.document.createElement('style');
      s.id = '_aud_style';
      s.textContent =
        '#aud-btn{{position:fixed;bottom:1.2rem;right:1.2rem;z-index:9999;'
        +'display:flex;align-items:center;gap:.4rem;'
        +'background:rgba(255,220,235,.92);border:2px solid #1a0810;'
        +'border-radius:2rem;padding:.45rem 1rem;cursor:pointer;'
        +'font-family:"Pixelify Sans",monospace;font-size:.85rem;'
        +'color:#1a0810;box-shadow:3px 3px 0 rgba(26,8,16,.5);'
        +'transition:transform .15s;user-select:none;}}'
        +'#aud-btn:hover{{transform:scale(1.06)}}'
        +'#calamar-gif-layer{{display:none;position:fixed;top:0;right:0;bottom:0;width:35vw;z-index:1;pointer-events:none;opacity:0.38;background-size:auto 100%!important;background-position:right center!important;background-repeat:no-repeat!important;}}'
        +'@keyframes calamarIn{{from{{opacity:0;transform:translateX(40px)}}to{{opacity:0.38;transform:translateX(0)}}}}';      P.document.head.appendChild(s);
    }}

    // Inject mute button into parent DOM
    if (!P.document.getElementById('aud-btn')) {{
      var btn = P.document.createElement('div');
      btn.id = 'aud-btn';
      btn.innerHTML = '<span id="aud-icon">\U0001F50A</span><span id="aud-label">Musique</span>';
      btn.onclick = function() {{ if (P._aud) P._aud.toggleMute(); }};
      P.document.body.appendChild(btn);
    }}

    // Inject calamar GIF div into parent DOM
    if (calamarGif && !P.document.getElementById('calamar-gif-layer')) {{
      var gifDiv = P.document.createElement('div');
      gifDiv.id = 'calamar-gif-layer';
      gifDiv.style.background = 'url("' + calamarGif + '") center center/contain no-repeat';
      P.document.body.appendChild(gifDiv);
    }}

    // Attach SFX listeners to buttons and plushies (in parent DOM)
    function attach() {{
      P.document.querySelectorAll('.stButton > button:not([data-ab])').forEach(function(b) {{
        b.setAttribute('data-ab','1');
        b.addEventListener('mouseenter', function(){{ play(sfxHover); }});
        b.addEventListener('click',      function(){{ play(sfxClick); }});
      }});
      P.document.querySelectorAll('.plushie-anim-wrap:not([data-ab])').forEach(function(w) {{
        w.setAttribute('data-ab','1');
        w.addEventListener('mouseenter', function(){{ play(sfxPlush); }});
      }});
    }}
    attach();
    new MutationObserver(attach).observe(P.document.body, {{childList:true, subtree:true}});

    P._aud = {{
      attach: attach,
      toggleMute: function() {{
        muted = !muted;
        var icon  = P.document.getElementById('aud-icon');
        var label = P.document.getElementById('aud-label');
        if (icon)  icon.textContent  = muted ? '\U0001F507' : '\U0001F50A';
        if (label) label.textContent = muted ? 'Muet' : 'Musique';
        if (muted) {{ if (bgm) bgm.pause(); }}
        else if (unlocked && !calamarActive) {{ if (bgm) bgm.play().catch(function(){{}}); }}
      }},
      calamarOn: function() {{
        if (calamarActive) return; calamarActive = true;
        if (bgm) bgm.pause();
        // Démarre la musique calamar en boucle
        if (sfxCalamar && !muted) {{
          sfxCalamar.currentTime = 0;
          sfxCalamar.play().catch(function(){{}});
        }}
        var l = P.document.getElementById('calamar-gif-layer');
        if (l) {{
          l.style.animation = 'none'; l.style.display = 'block';
          void l.offsetWidth; l.style.animation = 'calamarIn 0.7s ease-out forwards';
        }}
      }},
      calamarOff: function() {{
        if (!calamarActive) return; calamarActive = false;
        // Arrête la musique calamar
        if (sfxCalamar) {{ sfxCalamar.pause(); sfxCalamar.currentTime = 0; }}
        var l = P.document.getElementById('calamar-gif-layer');
        if (l) l.style.display = 'none';
        if (bgm && !muted && unlocked) bgm.play().catch(function(){{}});
      }},
      playUnlock: function() {{ play(sfxUnlock); }}
    }};
  }} else {{
    // Engine exists: just re-attach listeners after Streamlit rerun
    P._aud.attach();
  }}
}})();
</script>
</body></html>"""
    st.components.v1.html(html, height=0, scrolling=False)

_inject_audio_engine()

# --- état de la session ---
# tout ici parce que streamlit rerun à chaque interaction
defaults = {
    'current_page': "home", 'day': 1, 'max_days': 10,
    'history': [], 'last_events': [], 'morning_event': "",
    'calamar_active': False, 'active_card': None, 'active_action': None,
    'pending_actions': {},
    'popup_plushie': None,
    'popup_queue': [],
    'last_reactions': {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if 'unlocked_art' not in st.session_state:
    st.session_state.unlocked_art = {"Zaïtchyk 🐰": False, "Jean-Jacques 🐻": False, "Frédéric 🐷": False}

if 'plushies' not in st.session_state:
    st.session_state.plushies = {
        "Zaïtchyk 🐰":      {"energy": 70, "stress": 20, "affection": 0, "trait": "Extraverti",  "langage_ideal": "Enthousiaste"},
        "Jean-Jacques 🐻": {"energy": 70, "stress": 20, "affection": 0, "trait": "Introverti",  "langage_ideal": "Empathique"},
        "Frédéric 🐷":     {"energy": 70, "stress": 20, "affection": 0, "trait": "Équilibré",   "langage_ideal": "Factuel"}
    }

dialogues_db = {
    "Zaïtchyk 🐰": {
        "dodo":        ["Zzz... (il bouge dans son sommeil)", "C'était ennuyeux mais nécessaire...", "Je rêvais de courir partout !"],
        "jouer_cool":  ["C'était TROP BIEN !", "Je suis survolté !", "Meilleure partie de ma vie ! On recommence ?"],
        "refus":       ["Laisse-moi... j'ai pas la force de sauter aujourd'hui.", "Je suis trop triste pour m'amuser..."],
        "comm_succes": ["Ouais ! T'as tout à fait raison !", "C'est exactement ça ! Trop cool !", "Tu me motives à fond !"],
        "comm_echec":  ["Euh... t'es sûr de toi ?", "C'est un peu bizarre ce que tu dis.", "Mouais, bof. Je m'ennuie."]
    },
    "Jean-Jacques 🐻": {
        "dodo":        ["Merci... le silence fait du bien.", "Zzz... (il serre Kateryna très fort)", "C'était une sieste très réparatrice."],
        "jouer_stress":["Il y avait trop de bruit...", "Je suis fatigué maintenant...", "On peut faire un truc plus calme ?"],
        "refus":       ["Je veux juste rester dans ma grotte...", "S'il te plaît, pas aujourd'hui..."],
        "comm_succes": ["Merci pour ta douceur...", "Tu me comprends vraiment bien.", "Ça me touche beaucoup."],
        "comm_echec":  ["Tu parles trop fort pour moi...", "Je ne me sens pas compris.", "C'est un peu agressif..."]
    },
    "Frédéric 🐷": {
        "dodo":        ["Temps de repos optimisé.", "Mes batteries sont rechargées à 100%.", "Zzz... (ronflements réguliers)"],
        "jouer_cool":  ["Activité ludique validée.", "C'était une bonne stimulation cognitive.", "Mes paramètres de joie augmentent."],
        "refus":       ["Niveau d'énergie critique. Activité annulée.", "Paramètres émotionnels instables. Je refuse."],
        "comm_succes": ["Analyse correcte. Je valide.", "C'est très logique, merci.", "Communication efficace et pertinente."],
        "comm_echec":  ["C'est illogique.", "Je ne vois pas le rapport.", "Données non pertinentes. Rejeté."]
    }
}

def clamp(v): return max(0, min(100, v))
def get_mood(e, s):
    if s >= 80:              return "Burnout 💥"
    elif e <= 25 or s >= 65: return "Triste 😢"
    elif e > 60 and s < 40:  return "Heureux 😊"
    else:                    return "Neutre 😐"
def mood_class(m):
    if "Heureux" in m: return "mood-happy"
    if "Triste"  in m: return "mood-sad"
    if "Burnout" in m: return "mood-burn"
    return "mood-neut"

def mood_to_anim(mood, calamar=False, winner=False, idle=False):
    if winner:  return "winner"
    if idle:    return "idle"
    if calamar: return "scared"
    if "Heureux" in mood: return "happy"
    if "Triste"  in mood: return "sad"
    if "Burnout" in mood: return "burnout"
    return "happy"

PLUSHIE_KEYS = {
    "Zaïtchyk 🐰":      "zaïtchyk",
    "Jean-Jacques 🐻": "jean_jacques",
    "Frédéric 🐷":     "frederic",
}
MOOD_TO_EMOTION = {
    "Heureux 😊": "happy",
    "Neutre 😐":  "happy",
    "Triste 😢":  "sad",
    "Burnout 💥": "tired",
}

def get_plushie_image(name, emotion):
    key  = PLUSHIE_KEYS.get(name, "unknown")
    path = f"images/{emotion}_{key}.png"
    return path if os.path.exists(path) else None

def show_plushie_image(name, emotion, caption=None, width=180, anim_mood="happy"):
    path = get_plushie_image(name, emotion)
    if path:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = path.split(".")[-1]
        img_tag = f'<img src="data:image/{ext};base64,{b64}" style="width:{width}px;height:{width}px;object-fit:contain;image-rendering:pixelated;display:block;" />'
    else:
        emotion_emoji = {"happy":"😊","sad":"😢","tired":"😴","scared":"😱","super_happy":"🤩"}.get(emotion,"🧸")
        key = PLUSHIE_KEYS.get(name,"?")
        img_tag = (
            f'<div class="art-placeholder" style="width:{width}px;min-height:{width}px;">'
            f'<span style="font-size:{int(width*0.35)}px;display:block;margin-bottom:0.3rem">{emotion_emoji}</span>'
            f'<span style="font-size:0.7rem;opacity:0.5">images/{emotion}_{key}.png</span>'
            f'</div>'
        )
    caption_html = f'<div style="font-size:0.72rem;text-align:center;color:var(--text-soft);font-weight:700;margin-top:0.2rem;">{caption}</div>' if caption else ""
    st.markdown(
        f'<div class="plushie-anim-wrap" data-mood="{anim_mood}">'
        f'{img_tag}{caption_html}'
        f'</div>',
        unsafe_allow_html=True
    )

def stat_bar(label, icon, value, bar_class):
    pct = int(clamp(value))
    st.markdown(f"""
    <div class="stat-bar-wrap">
        <div class="stat-bar-label">
            <span>{icon} {label}</span>
            <span class="stat-val">{pct}</span>
        </div>
        <div class="stat-bar-track">
            <div class="stat-bar-fill {bar_class}" style="width:{pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def resolve_action(action_target, action_type, dialogue_choice=None, partner=None):
    p        = st.session_state.plushies
    t        = p[action_target]
    r        = dialogues_db[action_target]
    trait    = t["trait"]; lang = t["langage_ideal"]
    mood     = get_mood(t["energy"], t["stress"])
    msg      = ""
    reaction = "neutral"

    if st.session_state.calamar_active:
        if action_type in ["Jouer 🕹️", "Discussion 💬"]:
            t["stress"] += 15
            msg = f"❌ **{action_target}** claque des dents : *« T'es fou ?! Calamar rôde ! »*"
            reaction = "sad"
        elif action_type == "Dormir 💤":
            t["stress"] -= 10; t["energy"] += 15
            msg = f"✨ **{action_target}** se cache sous la couette : *« J'espère qu'il sera parti à mon réveil... »*"
            reaction = "neutral"
        elif action_type == "Communiquer 🗣️":
            CALAMAR_SUCCES = {
                "Zaïtchyk 🐰": [
                    "« T'INQUIÈTE PAS, on va l'atomiser ce calamar ! Reste avec moi ! »",
                    "« Regarde-moi dans les yeux ✦ il va PAS entrer ici, je te le promets ! »",
                ],
                "Jean-Jacques 🐻": [
                    "« Tu es en sécurité ici. Je suis là, tout près de toi. Respire. »",
                    "« Je comprends ta peur, elle est tout à fait normale. On traverse ça ensemble. »",
                ],
                "Frédéric 🐷": [
                    "« Statistiquement, Calamar ne peut pas franchir notre périmètre de sécurité. »",
                    "« Analyse de la menace : neutralisable. Protocole de protection activé. Calme-toi. »",
                ],
            }
            CALAMAR_ECHEC = {
                "Zaïtchyk 🐰": [
                    "*« C'EST PAS LE MOMENT DE FAIRE LA FÊTE ?! T'as vu ce qu'il y a dehors ?! »*",
                    "*« Arrête de sauter partout, tu vas attirer son attention !! »*",
                ],
                "Jean-Jacques 🐻": [
                    "*« Tes mots sonnent creux... tu ne réalises pas à quel point j'ai peur. »*",
                    "*« S'il te plaît... parle-moi doucement, là j'y arrive plus. »*",
                ],
                "Frédéric 🐷": [
                    "*« Ce discours n'est pas logique dans le contexte actuel. Calamar est RÉEL. »*",
                    "*« Tes données sont incorrectes. La menace n'est pas neutralisée. »*",
                ],
            }
            if dialogue_choice and lang in dialogue_choice:
                t["stress"] -= 50; t["affection"] += 35
                repl = random.choice(CALAMAR_SUCCES.get(action_target, ["« Tu m'as rassuré·e ! »"]))
                msg = f"🛡️ **{action_target}** : *{repl}* **(Affection +35, Stress -50)**"
                reaction = "happy"
            else:
                t["stress"] += 20
                repl = random.choice(CALAMAR_ECHEC.get(action_target, ["« Tu ne comprends rien ! »"]))
                msg = f"❌ **{action_target}** panique : {repl}"
                reaction = "sad"
    else:
        if mood in ["Triste 😢","Burnout 💥"] and action_type in ["Jouer 🕹️","Discussion 💬"]:
            t["stress"] += 15
            msg = f"❌ **{action_target}** : *« {random.choice(r['refus'])} »*"
            reaction = "sad"
        else:
            if action_type == "Dormir 💤":
                t["stress"] -= 20
                t["energy"] += 40 if trait == "Introverti" else 20
                if t["energy"] < 40: t["affection"] += 15
                msg = f"✨ **{action_target}** : *« {random.choice(r['dodo'])} »*"
                reaction = "neutral"
            elif action_type == "Jouer 🕹️":
                if trait in ["Extraverti","Équilibré"]:
                    t["energy"] += 20 if trait == "Extraverti" else -10
                    t["stress"] -= 30; t["affection"] += 20
                    msg = f"✨ **{action_target}** : *« {random.choice(r['jouer_cool'])} »* **(Affection +20)**"
                    reaction = "happy"
                else:
                    t["energy"] -= 15; t["stress"] += 10
                    msg = f"⚠️ **{action_target}** : *« {random.choice(r['jouer_stress'])} »*"
                    reaction = "sad"
            elif action_type == "Communiquer 🗣️":
                if dialogue_choice and lang in dialogue_choice:
                    t["stress"] -= 40; t["energy"] += 10; t["affection"] += 25
                    msg = f"💬 **{action_target}** : *« {random.choice(r['comm_succes'])} »* **(Affection +25)**"
                    reaction = "happy"
                else:
                    t["stress"] += 10
                    msg = f"❌ **{action_target}** : *« {random.choice(r['comm_echec'])} »*"
                    reaction = "sad"
            elif action_type == "Discussion 💬" and partner:
                pm = get_mood(p[partner]["energy"], p[partner]["stress"])
                pt = p[partner]["trait"]
                if pm in ["Triste 😢","Burnout 💥"]:
                    t["stress"] += 15
                    msg = f"❌ **{partner}** était trop déprimé pour parler avec **{action_target}**."
                    reaction = "sad"
                else:
                    t["affection"] += 10; p[partner]["affection"] += 10
                    reaction = "happy"
                    if pt == "Extraverti":
                        t["energy"] += 25
                        if trait == "Introverti": t["stress"] += 15; msg = f"🗣️ **{partner}** a raconté une histoire passionnante, ça a fatigué **{action_target}** nerveusement."; reaction = "sad"
                        else:                     t["stress"] -= 15; msg = f"🤣 **{partner}** et **{action_target}** ont eu un gros fou rire ensemble !"
                    elif pt == "Introverti":
                        t["stress"] -= 25
                        if trait == "Extraverti": t["energy"] -= 15; msg = f"☕ **{partner}** a offert un thé calmant, mais **{action_target}** s'est un peu ennuyé."
                        else:                     t["energy"] += 10;  msg = f"🤫 **{partner}** et **{action_target}** ont partagé un silence apaisant."
                    else:
                        t["stress"] -= 15; t["energy"] += 10
                        msg = f"🤝 **{partner}** a donné de bons conseils à **{action_target}**. Discussion constructive !"
    return msg, reaction


def end_of_day():
    messages  = []
    reactions = {}
    for name, action in st.session_state.pending_actions.items():
        msg, reaction = resolve_action(
            name, action["type"],
            dialogue_choice=action.get("dialogue"),
            partner=action.get("partner")
        )
        messages.append(msg)
        reactions[name] = reaction

    for name in st.session_state.plushies:
        act = st.session_state.pending_actions.get(name, {})
        # extraire le registre depuis la fin de la string du dialogue
        dial_raw = act.get("dialogue") or ""
        import re as _re
        reg_match = _re.search(r"\((\w+)\)\s*$", dial_raw)
        registre = reg_match.group(1) if reg_match else ""
        st.session_state.history.append({
            "Jour":       st.session_state.day,
            "Personnage": name,
            "Énergie":    st.session_state.plushies[name]["energy"],
            "Stress":     st.session_state.plushies[name]["stress"],
            "Affection":  st.session_state.plushies[name]["affection"],
            "Action":     act.get("type", ""),
            "Registre":   registre,
            "Calamar":    int(st.session_state.calamar_active),
            "Partenaire": act.get("partner") or "",
        })
        st.session_state.plushies[name]["energy"] -= 10
        st.session_state.plushies[name]["stress"]  += 5

    # reset état nuit
    # TODO: peut-être garder un historique des events nuit aussi ?
    st.session_state.calamar_active = False
    st.session_state.morning_event  = ""
    rc = random.random()
    if rc < 0.15:
        st.session_state.calamar_active = True
        st.session_state.morning_event  = "ALERTE ROUGE : Calamar a été aperçu cette nuit ! Les peluches sont pétrifiées. Utilise 'Parler' avec le bon registre pour les rassurer !"
        for p in st.session_state.plushies:
            st.session_state.plushies[p]["stress"] += 40
            st.session_state.plushies[p]["energy"] -= 10
    elif rc < 0.40:
        ev = random.choice(["cauchemar","sucre","cadeau"])
        c  = random.choice(list(st.session_state.plushies.keys()))
        if ev == "cauchemar":
            st.session_state.plushies[c]["stress"] += 30
            st.session_state.morning_event = f"🌩️ **{c}** a fait un mauvais rêve *(Stress en hausse)*."
        elif ev == "sucre":
            st.session_state.plushies[c]["energy"] += 40
            st.session_state.morning_event = f"🍬 **{c}** a trouvé des friandises. Énergie au top !"
        else:
            st.session_state.plushies[c]["affection"] += 15
            st.session_state.morning_event = f"🎁 **{c}** a trouvé un petit mot gentil *(Affection +15)* !"

    for name in st.session_state.plushies:
        for k in ["energy","stress","affection"]:
            st.session_state.plushies[name][k] = clamp(st.session_state.plushies[name][k])

    st.session_state.last_events     = messages
    st.session_state.last_reactions  = reactions
    st.session_state.pending_actions = {}
    st.session_state.active_card     = None
    st.session_state.active_action   = None
    st.session_state.day += 1
    if st.session_state.day > st.session_state.max_days:
        st.session_state.current_page = "results"
    st.rerun()


# ==========================================
# HOME
# ==========================================
if st.session_state.current_page == "home":
    st.markdown("""
    <div class="hero-banner">
        <p class="hero-title">La Tanière des Doudous de Kateryna 🧸</p>
        <p class="hero-sub">Une simulation comportementale</p>
    </div>""", unsafe_allow_html=True)

    col_rules, col_launch = st.columns([3,2], gap="large")
    with col_rules:
        st.markdown("### 🎯 Ta Mission")
        st.markdown(f"Atteins **100% d'Affection ❤️** avec tes 3 peluches en moins de **{st.session_state.max_days} jours**. Gère leurs ressources, choisis les bons mots, et méfie-toi de Calamar…")
        st.markdown("<br>", unsafe_allow_html=True)
        for icon, title, desc in [
            ("⚡","Énergie & Stress","Équilibre les ressources de chaque peluche pour éviter le Burnout total."),
            ("🗣️","Pragmatique Linguistique","Chaque peluche a un langage idéal. Trouve le bon registre pour gagner de l'affection."),
            ("🤝","Dynamiques de Groupe","Les discussions entre amis créent des synergies, ou des tensions."),
            ("🦑","DANGER ✦ Calamar","Calamar peut surgir la nuit. Seul le bon langage peut rassurer les peluches terrorisées."),
        ]:
            st.markdown(f'<div class="rule-card"><div class="rule-icon">{icon}</div><div><p class="rule-title">{title}</p><p class="rule-desc">{desc}</p></div></div>', unsafe_allow_html=True)

    with col_launch:
        st.markdown("### 🧪 Les Peluches")
        home_cols = st.columns(3)
        plushie_info = [
            ("Zaïtchyk 🐰",      "Extraverti",  "Enthousiaste", "#ff6b9d"),
            ("Jean-Jacques 🐻", "Introverti",  "Empathique",   "#5b9bd5"),
            ("Frédéric 🐷",     "Équilibré",   "Factuel",      "#4caf50"),
        ]
        for idx, (name, trait, lang, color) in enumerate(plushie_info):
            with home_cols[idx]:
                show_plushie_image(name, "happy", width=90, anim_mood="idle")
        for name, trait, lang, color in plushie_info:
            st.markdown(f'<div class="rule-card" style="border-left:3px solid {color}; margin-bottom:0.6rem"><div><p class="rule-title" style="color:{color}">{name}</p><p class="rule-desc">Profil : <b>{trait}</b> · Langage : <b>{lang}</b></p></div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Lancer la Simulation", use_container_width=True, type="primary"):
            st.session_state.current_page = "game"; st.rerun()


# ==========================================
# RESULTS
# ==========================================
elif st.session_state.current_page == "results":
    st.markdown('<p class="hero-title" style="font-size:2.5rem">🎓 Évaluation Finale</p>', unsafe_allow_html=True)
    st.markdown("##### Rapport de Simulation Comportementale")
    st.markdown("<br>", unsafe_allow_html=True)

    maxed = sum(1 for a in st.session_state.unlocked_art.values() if a)
    if maxed == 3:
        st.success("### 🌟 MENTION TRÈS BIEN ✦ ADMISSION DIRECTE !")
        st.markdown("Impressionnant ! Tu as maîtrisé la gestion du stress, la pragmatique linguistique et même survécu à Calamar.")
        st.balloons()
    elif maxed > 0:
        st.warning(f"### 👍 MENTION ASSEZ BIEN ✦ {maxed}/3 Peluches sauvées")
        st.markdown("Bon travail analytique, mais la gestion de crise laisse quelques lacunes.")
    else:
        st.error("### ❌ ÉCHEC DE LA SIMULATION ✦ 0/3 Peluches")
        st.markdown("Les peluches sont épuisées. Retente ta chance !")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 Galerie des Best Friends")
    art_cols = st.columns(3)
    for i, (name, is_unlocked) in enumerate(st.session_state.unlocked_art.items()):
        with art_cols[i]:
            if is_unlocked:
                st.success(f"✅ {name}")
                show_plushie_image(name, "super_happy", caption="Merci d'être mon ami(e) !", width=220, anim_mood="winner-big")
            else:
                st.error(f"🔒 {name}")
                show_plushie_image(name, "sad", caption="Affection requise : 100%", width=220, anim_mood="sad")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Analyse des Données ✦ Rapport Final")

    if st.session_state.history:
        import math
        df = pd.DataFrame(st.session_state.history)

        # ── Tab layout ──
        tab_charts, tab_export, tab_pearson, tab_equity = st.tabs([
            "📈 Graphiques", "💾 Export CSV", "🔢 Corrélation de Pearson", "⚖️ Analyse des Biais"
        ])

        # ── GRAPHIQUES ──
        with tab_charts:
            t1,t2,t3 = st.tabs(["📉 Énergie","📈 Stress","❤️ Affection"])
            def safe_pivot(col):
                try: return df.pivot(index="Jour", columns="Personnage", values=col)
                except: return None
            with t1:
                piv = safe_pivot("Énergie")
                if piv is not None: st.line_chart(piv)
            with t2:
                piv = safe_pivot("Stress")
                if piv is not None: st.line_chart(piv)
            with t3:
                piv = safe_pivot("Affection")
                if piv is not None: st.line_chart(piv)

        # ── EXPORT CSV ──
        with tab_export:
            st.markdown("""
<div class="rule-card">
<div class="rule-icon">💾</div>
<div><p class="rule-title">Data Engineering ✦ Export du Dataset</p>
<p class="rule-desc">Télécharge le dataset complet généré par ta partie. Chaque ligne = une peluche × un jour.
Colonnes : Jour, Personnage, Énergie, Stress, Affection, Action, Registre linguistique, Calamar actif, Partenaire.</p></div>
</div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            # Preview
            st.dataframe(df, use_container_width=True, height=280)
            st.markdown("<br>", unsafe_allow_html=True)
            csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="⬇️ Télécharger dataset.csv",
                data=csv_bytes,
                file_name="kateryna_doudous_dataset.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
            st.caption(f"📦 {len(df)} lignes · {len(df.columns)} colonnes · {len(df.to_csv(index=False))//1024 + 1} Ko")

        # ── CORRÉLATION DE PEARSON ──
        with tab_pearson:
            st.markdown("""
<div class="rule-card">
<div class="rule-icon">🔢</div>
<div><p class="rule-title">Mathématiques ✦ Coefficient de corrélation de Pearson</p>
<p class="rule-desc">Mesure la relation linéaire entre le Stress et l'Affection pour chaque peluche.
<b>r ∈ [-1, 1]</b> : proche de -1 = forte corrélation négative (plus de stress = moins d'affection), 0 = aucune, +1 = forte positive.</p></div>
</div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # formule de pearson faite à la main (numpy pas dispo sans install)
            def pearson(x_vals, y_vals):
                n = len(x_vals)
                if n < 2: return None
                mx = sum(x_vals)/n; my = sum(y_vals)/n
                num   = sum((x-mx)*(y-my) for x,y in zip(x_vals,y_vals))
                denom = math.sqrt(sum((x-mx)**2 for x in x_vals) * sum((y-my)**2 for y in y_vals))
                return round(num/denom, 4) if denom != 0 else None

            def interpret_r(r):
                if r is None: return "—", "mood-neut"
                a = abs(r)
                if a >= 0.7:   strength = "forte"
                elif a >= 0.4: strength = "modérée"
                else:          strength = "faible"
                direction = "négative 📉" if r < 0 else "positive 📈"
                if a < 0.1: return "Quasi-nulle 😶 (pas de relation linéaire)", "mood-neut"
                return f"Corrélation {strength} {direction} (r = {r})", "mood-happy" if r < -0.3 else "mood-sad"

            plushie_names_r = df["Personnage"].unique()
            cols_p = st.columns(len(plushie_names_r))
            for i, plush in enumerate(plushie_names_r):
                sub = df[df["Personnage"] == plush]
                r   = pearson(sub["Stress"].tolist(), sub["Affection"].tolist())
                label, css = interpret_r(r)
                with cols_p[i]:
                    st.markdown(f"""
<div class="rule-card" style="text-align:center">
  <p class="plushie-name">{plush}</p>
  <p style="font-size:2.2rem;margin:0.3rem 0">{("💙" if r is not None and r < -0.4 else "💛" if r is not None and abs(r) < 0.4 else "❤️")}</p>
  <p style="font-size:1.5rem;font-weight:800;font-family:'Pixelify Sans',monospace">{r if r is not None else "N/A"}</p>
  <p class="rule-desc">{label}</p>
</div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            # Global scatter data
            st.markdown("**📌 Dispersion Stress vs Affection ✦ toutes peluches**")
            try:
                scatter_df = df[["Stress","Affection","Personnage"]].copy()
                st.scatter_chart(scatter_df, x="Stress", y="Affection", color="Personnage", use_container_width=True)
            except Exception:
                st.info("Données insuffisantes pour le scatter plot.")

            st.markdown("<br>", unsafe_allow_html=True)
            r_global = pearson(df["Stress"].tolist(), df["Affection"].tolist())
            label_g, _ = interpret_r(r_global)
            st.markdown(f"""
<div class="rule-card" style="border-left:4px solid #ff6b9d">
<div class="rule-icon">🌐</div>
<div><p class="rule-title">Corrélation globale (toutes peluches)</p>
<p class="rule-desc">{label_g}</p></div>
</div>""", unsafe_allow_html=True)

        # ── ANALYSE DES BIAIS ──
        with tab_equity:
            st.markdown("""
<div class="rule-card">
<div class="rule-icon">⚖️</div>
<div><p class="rule-title">Sciences Humaines ✦ Analyse des Biais du Joueur</p>
<p class="rule-desc">As-tu traité toutes les peluches de manière équitable ? Cette section mesure tes biais comportementaux :
favoritisme, négligence, et cohérence dans le choix du registre linguistique.</p></div>
</div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            plushies_list = df["Personnage"].unique().tolist()

            # qui a eu le plus d'actions Communiquer = favoritisme potentiel
            comm_df = df[df["Action"] == "Communiquer 🗣️"]
            comm_counts = comm_df["Personnage"].value_counts()

            # précision du registre — combien de fois le joueur a tapé juste
            IDEAL_REGISTER = {
                "Zaïtchyk 🐰":      "Enthousiaste",
                "Jean-Jacques 🐻": "Empathique",
                "Frédéric 🐷":     "Factuel",
            }
            register_rows = comm_df[comm_df["Registre"] != ""]
            accuracy = {}
            for plush in plushies_list:
                sub = register_rows[register_rows["Personnage"] == plush]
                if len(sub) == 0: accuracy[plush] = None; continue
                ideal = IDEAL_REGISTER.get(plush, "")
                correct = sub[sub["Registre"] == ideal].shape[0]
                accuracy[plush] = round(correct / len(sub) * 100, 1)

            # nb d'actions par peluche
            action_counts = df[df["Action"] != ""]["Personnage"].value_counts()
            avg_actions   = action_counts.mean() if len(action_counts) > 0 else 1

            # écart-type affection finale -> plus c'est bas, plus c'est équitable
            final_affection = {}
            for plush in plushies_list:
                sub = df[df["Personnage"] == plush]
                if len(sub): final_affection[plush] = sub.iloc[-1]["Affection"]
            aff_vals = list(final_affection.values())
            std_aff  = round(math.sqrt(sum((v - sum(aff_vals)/len(aff_vals))**2 for v in aff_vals)/len(aff_vals)), 1) if aff_vals else 0
            equity_score = max(0, round(100 - std_aff, 1))

            # taux de réussite calamar — nb de fois bon registre / nb tentatives totales
            rows_cal = df[(df["Calamar"] == 1) & (df["Action"] == "Communiquer 🗣️") & (df["Registre"] != "")]
            nb_tentatives = len(rows_cal)
            nb_succes = sum(
                1 for _, row in rows_cal.iterrows()
                if row["Registre"] == IDEAL_REGISTER.get(row["Personnage"], "")
            )
            taux_calamar = round(nb_succes / nb_tentatives * 100, 1) if nb_tentatives > 0 else None

            st.markdown("#### 🎯 Attention portée à chaque peluche")

            # Build all cards as a single flex row — avoids Streamlit column width constraints
            cards_html = '<div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-bottom:0.6rem;">'
            for plush in plushies_list:
                actions_n  = int(action_counts.get(plush, 0))
                aff_final  = final_affection.get(plush, 0)
                acc        = accuracy.get(plush)
                comm_n     = int(comm_counts.get(plush, 0))
                delta_act  = actions_n - avg_actions
                label_biais = "🟢 Équitable" if abs(delta_act) <= 2 else ("🔴 Favori·te" if delta_act > 0 else "🔵 Négligé·e")
                acc_str    = f"{acc}%" if acc is not None else "—"
                cards_html += f"""
<div style="flex:1;min-width:180px;background:rgba(255,255,255,0.82);
  backdrop-filter:blur(8px);border:2px solid #1a0810;border-radius:12px;
  padding:0.9rem 1rem;box-shadow:2px 2px 0px rgba(26,8,16,0.5);">
  <p style="font-family:'Pixelify Sans',monospace;font-size:1rem;font-weight:700;
     color:#1a0810;margin:0 0 0.5rem 0;">{plush}</p>
  <p style="font-size:0.84rem;color:#5a1030;margin:0.2rem 0;line-height:1.6;">
    🎮 <b>{actions_n}</b> actions totales &nbsp;{label_biais}</p>
  <p style="font-size:0.84rem;color:#5a1030;margin:0.2rem 0;line-height:1.6;">
    🗣️ <b>{comm_n}</b> fois Communiquer</p>
  <p style="font-size:0.84rem;color:#5a1030;margin:0.2rem 0;line-height:1.6;">
    🎯 Bon registre : <b>{acc_str}</b></p>
  <p style="font-size:0.84rem;color:#5a1030;margin:0.2rem 0;line-height:1.6;">
    ❤️ Affection finale : <b>{aff_final}</b>/100</p>
</div>"""
            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_eq1, col_eq2 = st.columns(2)
            with col_eq1:
                eq_color = "#4caf50" if equity_score >= 75 else ("#ff9800" if equity_score >= 50 else "#e53935")
                eq_emoji = "🟢" if equity_score >= 75 else ("🟡" if equity_score >= 50 else "🔴")
                st.markdown(f"""
<div class="rule-card" style="border-left:4px solid {eq_color};text-align:center">
  <p class="rule-title">⚖️ Score d'équité global</p>
  <p style="font-size:2.5rem;font-family:'Pixelify Sans',monospace;font-weight:800;color:{eq_color}">{equity_score} / 100</p>
  <p class="rule-desc">{eq_emoji} {"Très équitable ✦ tu as pris soin de tout le monde uniformément." if equity_score >= 75 else ("Quelques disparités notables entre les peluches." if equity_score >= 50 else "Fort favoritisme détecté ✦ certaines peluches ont été négligées.")}</p>
</div>""", unsafe_allow_html=True)
            with col_eq2:
                if taux_calamar is not None:
                    cal_color = "#4caf50" if taux_calamar >= 70 else ("#ff9800" if taux_calamar >= 40 else "#e53935")
                    st.markdown(f"""
<div class="rule-card" style="border-left:4px solid {cal_color};text-align:center">
  <p class="rule-title">🦑 Gestion de crise Calamar</p>
  <p style="font-size:2.5rem;font-family:'Pixelify Sans',monospace;font-weight:800;color:{cal_color}">{taux_calamar}%</p>
  <p class="rule-desc">Taux de succès du bon registre lors des apparitions de Calamar ({nb_tentatives} tentative{"s" if nb_tentatives > 1 else ""}).</p>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
<div class="rule-card" style="text-align:center">
  <p class="rule-title">🦑 Gestion de crise Calamar</p>
  <p class="rule-desc">Aucune crise Calamar rencontrée durant cette partie.</p>
</div>""", unsafe_allow_html=True)

            # Register usage heatmap (table)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Registres linguistiques utilisés par peluche")
            if len(register_rows) > 0:
                reg_pivot = register_rows.groupby(["Personnage","Registre"]).size().unstack(fill_value=0)
                st.dataframe(reg_pivot, use_container_width=True)
                st.caption("Chaque cellule = nombre de fois où tu as utilisé ce registre avec cette peluche.")
            else:
                st.info("Aucune donnée de registre disponible.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Recommencer la Simulation", type="primary"):
        st.session_state.clear(); st.rerun()


# ==========================================
# GAME
# ==========================================
elif st.session_state.current_page == "game":

    pending = st.session_state.pending_actions
    plushie_names = list(st.session_state.plushies.keys())

    with st.sidebar:
        st.markdown("### ⚙️ Laboratoire")
        st.metric("⏳ Jours restants", st.session_state.max_days - st.session_state.day + 1)
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("💖 Peluches sauvées", f"{sum(1 for v in st.session_state.unlocked_art.values() if v)} / 3")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Actions planifiées :**")
        active_for_sidebar = [n for n in plushie_names if not st.session_state.unlocked_art[n]]
        if active_for_sidebar:
            for n in active_for_sidebar:
                if n in pending:
                    label = pending[n]["type"].split()[0]
                    st.markdown(f"✅ {n.split()[0]} ׂ╰┈➤ {label}")
                else:
                    st.markdown(f"⬜ {n.split()[0]} ✦ *pas encore*")
        else:
            st.markdown("🎉 *Toutes conquises !*")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Accueil",     use_container_width=True): st.session_state.current_page="home"; st.rerun()
        if st.button("🔄 Recommencer", use_container_width=True): st.session_state.clear();              st.rerun()

    st.markdown('<p class="hero-title" style="font-size:2.2rem">🧸 La Tanière des Doudous de Kateryna</p>', unsafe_allow_html=True)
    st.markdown(f'<span class="day-badge">📅 Jour {st.session_state.day} / {st.session_state.max_days}</span>', unsafe_allow_html=True)

    newly_unlocked = []
    for name, stats in st.session_state.plushies.items():
        if stats["affection"] >= 100 and not st.session_state.unlocked_art[name]:
            st.session_state.unlocked_art[name] = True
            newly_unlocked.append(name)
    # Queue ALL newly unlocked plushies — don't overwrite with one
    if newly_unlocked:
        st.session_state.popup_queue = st.session_state.popup_queue + newly_unlocked
    # Move first from queue into active popup slot if nothing showing
    if not st.session_state.popup_plushie and st.session_state.popup_queue:
        st.session_state.popup_plushie = st.session_state.popup_queue[0]
        st.session_state.popup_queue   = st.session_state.popup_queue[1:]
    # Early game over if all 3 are unlocked and no popups pending
    if all(st.session_state.unlocked_art.values()) and not st.session_state.popup_plushie:
        st.session_state.current_page = "results"
        st.rerun()

    # ── Celebration Banner (1, 2, or 3 simultaneous unlocks) ──
    if st.session_state.popup_plushie:
        # Gather ALL plushies to celebrate at once
        winners_now = [st.session_state.popup_plushie] + list(st.session_state.popup_queue)

        # Unlock SFX
        st.components.v1.html("""<script>
(function t(){var P=(window.parent&&window.parent!==window)?window.parent:window;
if(P._aud&&P._aud.playUnlock){P._aud.playUnlock();}else{setTimeout(t,120);}})();
</script>""", height=0)

        # Build plushie image cards
        cards_html = ""
        for cel_name in winners_now:
            cel_img = get_plushie_image(cel_name, "super_happy")
            if cel_img:
                with open(cel_img, "rb") as _cf:
                    _b64 = base64.b64encode(_cf.read()).decode()
                _ext = cel_img.split(".")[-1]
                _img_tag = f'<img src="data:image/{_ext};base64,{_b64}" style="width:100px;height:100px;object-fit:contain;image-rendering:pixelated;display:block;margin:0 auto;" />'
            else:
                _img_tag = '<div style="font-size:4rem;text-align:center">🤩</div>'
            cards_html += f"""<div style="display:flex;flex-direction:column;align-items:center;gap:0.3rem;flex:1;min-width:110px;max-width:160px;">
              <div class="plushie-anim-wrap" data-mood="winner-big" style="width:100px;">{_img_tag}</div>
              <p style="font-family:'Pixelify Sans',monospace;font-size:0.88rem;font-weight:800;color:#0d500d;text-align:center;margin:0;white-space:nowrap;">💖 {cel_name}</p>
            </div>"""

        n_cel = len(winners_now)
        title_txt = "🌟 TOUT LE MONDE AU MAX !" if n_cel == 3 else ("💖 DOUBLE VICTOIRE !" if n_cel == 2 else "💖 MAX AFFECTION !")
        desc_txt  = ("Ces peluches ont" if n_cel > 1 else "Cette peluche a") + " atteint 100% d'affection !<br>Tu as trouvé les mots parfaits !"
        st.markdown(f"""
        <div class="modal-overlay">
          <div class="modal-card" style="max-width:min(90vw,560px);padding:2rem 2rem 1.4rem;">
            <div class="modal-stars"><span class="float-star">⭐</span><span class="float-star">✨</span><span class="float-star">⭐</span></div>
            <h2 style="font-size:1.3rem;margin-bottom:0.6rem">{title_txt}</h2>
            <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:1.2rem;margin:0.4rem 0 1rem;">{cards_html}</div>
            <p style="font-size:0.9rem;margin:0 0 1.4rem 0">{desc_txt}</p>
          </div>
        </div>""", unsafe_allow_html=True)

        with st.form("popup_close_form", clear_on_submit=True, border=False):
            st.markdown("""<style>
            [data-testid="stForm"] {
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, 148px) !important;
                z-index: 10001 !important;
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                width: 230px !important;
            }
            [data-testid="stForm"] .stButton > button {
                background: linear-gradient(135deg, rgba(180,245,160,0.97), rgba(140,220,120,0.97)) !important;
                color: #0e3b0e !important;
                font-family: 'Pixelify Sans', monospace !important;
                font-size: 1rem !important;
                font-weight: 800 !important;
                padding: 0.65rem 1.5rem !important;
                border: 2.5px solid #1a0810 !important;
                border-radius: 10px !important;
                box-shadow: 4px 4px 0px rgba(26,8,16,0.6) !important;
                width: 100% !important;
                cursor: pointer !important;
            }
            [data-testid="stForm"] .stButton > button:hover {
                transform: translate(-2px,-2px) !important;
                box-shadow: 6px 6px 0px rgba(26,8,16,0.5) !important;
            }
            </style>""", unsafe_allow_html=True)
            submitted = st.form_submit_button("✨ Super, on continue !", use_container_width=True)
            if submitted:
                st.session_state.popup_plushie = None
                st.session_state.popup_queue   = []
                if all(st.session_state.unlocked_art.values()):
                    st.session_state.current_page = "results"
                st.rerun()

    # ── Night alerts ──
    if st.session_state.calamar_active:
        st.components.v1.html("""<script>
(function t(){var P=(window.parent&&window.parent!==window)?window.parent:window;
if(P._aud&&P._aud.calamarOn){P._aud.calamarOn();}else{setTimeout(t,120);}})();
</script>""", height=0)
        st.markdown('<div class="calamar-screen-overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="calamar-alert">', unsafe_allow_html=True)
        st.error(f"🦑 {st.session_state.morning_event}", icon="🦑")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.components.v1.html("""<script>
(function(){var P=(window.parent&&window.parent!==window)?window.parent:window;
if(P._aud&&P._aud.calamarOff)P._aud.calamarOff();})();
</script>""", height=0)
        if st.session_state.morning_event:
            st.info(st.session_state.morning_event)

    if st.session_state.last_events:
        with st.expander("📜 Résultats du jour précédent", expanded=True):
            for ev in st.session_state.last_events:
                if "❌" in ev:   st.error(ev)
                elif "⚠️" in ev: st.warning(ev)
                elif "🛡️" in ev: st.success(ev)
                else:             st.success(ev)

    winners      = [n for n in plushie_names if st.session_state.unlocked_art[n]]
    active_names = [n for n in plushie_names if not st.session_state.unlocked_art[n]]

    if winners:
        st.markdown("#### 💖 Peluches conquises")
        w_cols = st.columns(len(winners))
        for wi, wname in enumerate(winners):
            with w_cols[wi]:
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    show_plushie_image(wname, "super_happy", width=80, anim_mood="winner")
                with col_txt:
                    st.markdown(f'<p class="winner-shelf-name">💖 {wname}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="winner-shelf-sub">❤️ Affection : 100%<br>✨ Amitié éternelle !</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if active_names:
        n_active = len(active_names)
        cols = st.columns(n_active)
        for i, name in enumerate(active_names):
            stats = st.session_state.plushies[name]
            with cols[i]:
                mood      = get_mood(stats['energy'], stats['stress'])
                nc        = "danger" if mood in ["Triste 😢","Burnout 💥"] else ""
                planned   = pending.get(name)
                last_react = st.session_state.last_reactions.get(name)

                if st.session_state.calamar_active:
                    emotion = "scared"; anim_mood = "scared"
                elif last_react == "sad":
                    emotion = "sad";   anim_mood = "sad"
                elif last_react == "happy":
                    emotion = "happy"; anim_mood = "happy"
                else:
                    emotion   = MOOD_TO_EMOTION.get(mood, "happy")
                    anim_mood = mood_to_anim(mood, calamar=st.session_state.calamar_active)

                show_plushie_image(name, emotion, width=160, anim_mood=anim_mood)

                planned_badge = " ✅" if planned else ""
                st.markdown(f'<p class="plushie-name {nc}">{name}{planned_badge}</p>', unsafe_allow_html=True)
                st.caption(f"{stats['trait']}  ·  {stats['langage_ideal']}")

                stat_bar("Énergie",   "⚡", stats['energy'],   "bar-energy")
                stat_bar("Stress",    "😰", stats['stress'],   "bar-stress")
                stat_bar("Affection", "❤️", stats['affection'],"bar-love")
                st.markdown(f'<span class="mood-pill {mood_class(mood)}">{mood}</span>', unsafe_allow_html=True)
                st.markdown('<hr class="card-divider">', unsafe_allow_html=True)

                if planned:
                    st.markdown('<p class="action-label">✅ Action planifiée</p>', unsafe_allow_html=True)
                    action_summary = planned["type"]
                    if planned.get("partner"):  action_summary += f" avec {planned['partner'].split()[0]}"
                    if planned.get("dialogue"): action_summary += " *(langage choisi)*"
                    st.markdown(f'<div class="planned-action">✅ {action_summary}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("✏️ Changer", key=f"chg_{name}", use_container_width=True):
                        del st.session_state.pending_actions[name]
                        st.session_state.active_card   = None
                        st.session_state.active_action = None
                        st.rerun()
                else:
                    st.markdown('<p class="action-label">🎮 Choisir une action</p>', unsafe_allow_html=True)

                    if st.session_state.active_card == name:
                        st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
                        if st.session_state.active_action == "Communiquer 🗣️":
                            # Calamar special dialogues override normal ones
                            if st.session_state.calamar_active:
                                # Special calamar reassurance dialogues
                                CALAMAR_DIALOGUES = {
                                    "theme": "🦑 URGENCE ✦ Calamar rôde !",
                                    "options": [
                                        "« ALLEZ COURAGE ! On va le chasser ce monstre, t'as rien à craindre avec moi ! » (Enthousiaste)",
                                        "« Je suis là, tout près de toi. Respire... tu es en sécurité, je te le promets. » (Empathique)",
                                        "« Analyse de la menace : risque faible. Tu es protégé·e dans ce périmètre. » (Factuel)",
                                    ]
                                }
                                st.markdown(f"**🦑 {CALAMAR_DIALOGUES['theme']} ✦ Comment rassures-tu {name.split()[0]} ?**")
                                dc = st.radio("langue_cal", CALAMAR_DIALOGUES["options"],
                                              label_visibility="collapsed", key=f"dc_{name}")
                            else:
                                # Normal daily dialogues (1 set per day)
                                DIALOGUES_PAR_JOUR = [
                                    {"theme": "🌅 Première rencontre", "options": [
                                        "« Hey toi ! T'es prêt pour une super aventure ensemble ?! » (Enthousiaste)",
                                        "« Salut... je suis là si tu as besoin de parler, sans pression. » (Empathique)",
                                        "« Bonjour. Je viens établir un premier bilan de ta situation. » (Factuel)"]},
                                    {"theme": "🔍 Découverte", "options": [
                                        "« Dis-moi tout ! C'est quoi ton truc préféré dans la vie ?! » (Enthousiaste)",
                                        "« J'aimerais vraiment comprendre ce qui te rend heureux... » (Empathique)",
                                        "« Quelles sont tes préférences ? Je compile les données. » (Factuel)"]},
                                    {"theme": "😤 Tension du jour", "options": [
                                        "« Lâche tout ça ! On va s'éclater et oublier les soucis ! » (Enthousiaste)",
                                        "« Je vois que tu portes quelque chose de lourd... tu peux tout me dire. » (Empathique)",
                                        "« Niveau de stress élevé détecté. Appliquons un protocole de décompression. » (Factuel)"]},
                                    {"theme": "💪 Motivation", "options": [
                                        "« T'es INCROYABLE et tu vas tout déchirer aujourd'hui ! » (Enthousiaste)",
                                        "« Je crois vraiment en toi, même dans les moments difficiles. » (Empathique)",
                                        "« Tes performances sont en hausse de 12%. Continuez ainsi. » (Factuel)"]},
                                    {"theme": "📊 Mi-parcours", "options": [
                                        "« On est à la moitié ! La deuxième partie va être ENCORE meilleure ! » (Enthousiaste)",
                                        "« Comment tu te sens depuis le début ? Tu as évolué, je le sens. » (Empathique)",
                                        "« Bilan intermédiaire : indicateurs globalement positifs, ajustements mineurs requis. » (Factuel)"]},
                                    {"theme": "⚡ Désaccord", "options": [
                                        "« On va pas se laisser abattre par ça ! On est une équipe ! » (Enthousiaste)",
                                        "« Je comprends que tu sois blessé·e. Tes émotions sont valides. » (Empathique)",
                                        "« Analysons objectivement les points de friction pour trouver une solution. » (Factuel)"]},
                                    {"theme": "😴 Coup de mou", "options": [
                                        "« Allez, un petit coup de boost et ça repart en flèche ! » (Enthousiaste)",
                                        "« C'est normal d'être épuisé·e. Tu n'as pas à tout porter seul·e. » (Empathique)",
                                        "« Fatigue cumulée diagnostiquée. Réduction de charge recommandée. » (Factuel)"]},
                                    {"theme": "🌈 Rêves & projets", "options": [
                                        "« Imagine tout ce qu'on va faire après ! Les possibilités sont INFINIES ! » (Enthousiaste)",
                                        "« C'est quoi ton plus grand rêve ? J'adorerais l'entendre. » (Empathique)",
                                        "« Définissons ensemble des objectifs réalistes et mesurables pour la suite. » (Factuel)"]},
                                    {"theme": "🕯️ Avant la fin", "options": [
                                        "« On est presque au bout ! Je suis tellement fier·e de nous deux ! » (Enthousiaste)",
                                        "« Ces moments avec toi ont vraiment compté. Je veux que tu le saches. » (Empathique)",
                                        "« Dernière phase initiée. Optimisation finale des paramètres relationnels. » (Factuel)"]},
                                    {"theme": "🌟 Dernier jour", "options": [
                                        "« C'est le GRAND FINAL ! On donne TOUT ce qu'on a ! » (Enthousiaste)",
                                        "« Quoi qu'il arrive, je suis content·e d'avoir été là pour toi. » (Empathique)",
                                        "« Journée de clôture. Synthèse de toutes les données relationnelles collectées. » (Factuel)"]},
                                ]
                                jour_idx = min(st.session_state.day - 1, 9)
                                set_jour = DIALOGUES_PAR_JOUR[jour_idx]
                                st.markdown(f"**💬 {set_jour['theme']} ✦ Que lui dis-tu ?**")
                                dc = st.radio("langue", set_jour["options"],
                                              label_visibility="collapsed", key=f"dc_{name}")
                            # Confirm / cancel — shared by calamar and normal branches
                            ca, cb = st.columns(2)
                            with ca:
                                if st.button("✅ Confirmer", key=f"snd_{name}", use_container_width=True):
                                    st.session_state.pending_actions[name] = {"type": "Communiquer 🗣️", "dialogue": dc, "partner": None}
                                    st.session_state.active_card = None; st.session_state.active_action = None
                                    st.rerun()
                            with cb:
                                if st.button("✖ Annuler", key=f"cnc_{name}", use_container_width=True):
                                    st.session_state.active_card = None; st.session_state.active_action = None
                                    st.rerun()
                        elif st.session_state.active_action == "Discussion 💬":
                            partners = [p for p in plushie_names if p != name]
                            st.markdown("**🤝 Avec qui discuter ?**")
                            partner = st.radio("partenaire", partners, label_visibility="collapsed", key=f"dp_{name}")
                            ca, cb  = st.columns(2)
                            with ca:
                                if st.button("✅ Confirmer", key=f"snd2_{name}", use_container_width=True):
                                    st.session_state.pending_actions[name] = {"type": "Discussion 💬", "dialogue": None, "partner": partner}
                                    st.session_state.active_card = None; st.session_state.active_action = None
                                    st.rerun()
                            with cb:
                                if st.button("✖ Annuler", key=f"cnc2_{name}", use_container_width=True):
                                    st.session_state.active_card = None; st.session_state.active_action = None
                                    st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("💤 Dormir",   key=f"slp_{name}", use_container_width=True):
                                st.session_state.pending_actions[name] = {"type": "Dormir 💤", "dialogue": None, "partner": None}
                                st.rerun()
                            if st.button("🗣️ Parler",   key=f"cmm_{name}", use_container_width=True):
                                st.session_state.active_card   = name
                                st.session_state.active_action = "Communiquer 🗣️"
                                st.rerun()
                        with c2:
                            if st.button("🕹️ Jouer",    key=f"ply_{name}", use_container_width=True):
                                st.session_state.pending_actions[name] = {"type": "Jouer 🕹️", "dialogue": None, "partner": None}
                                st.rerun()
                            if st.button("💬 Discuter",  key=f"dsc_{name}", use_container_width=True):
                                st.session_state.active_card   = name
                                st.session_state.active_action = "Discussion 💬"
                                st.rerun()

    elif not winners:
        st.info("Aucune peluche active.")

    st.markdown("<br>", unsafe_allow_html=True)
    needed        = len(active_names)
    actions_count = sum(1 for n in active_names if n in pending)
    all_ready     = (needed == 0) or (actions_count == needed)

    bcol1, bcol2, bcol3 = st.columns([1, 2, 1])
    with bcol2:
        if needed == 0:
            st.markdown('<div class="validate-wrapper"><p style="text-align:center;font-family:\'Pixelify Sans\',monospace;font-weight:800;">🎉 Toutes les peluches sont heureuses !</p></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🌙 Passer la Nuit", use_container_width=True, type="primary"):
                end_of_day()
        elif all_ready:
            st.markdown('<div class="validate-wrapper">', unsafe_allow_html=True)
            st.markdown('<p style="font-family:\'Pixelify Sans\',monospace;font-size:0.85rem;font-weight:800;text-align:center;margin:0 0 0.5rem;">✨ Actions prêtes ✦ bonne nuit !</p>', unsafe_allow_html=True)
            if st.button("🌙 Valider la Journée & Passer à la Nuit", use_container_width=True, type="primary"):
                end_of_day()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            remaining = needed - actions_count
            stars = "⭐" * actions_count + "☆" * remaining
            st.markdown(
                f'<div style="text-align:center;">'
                f'<span class="waiting-text">{stars} Encore {remaining} peluche{"s" if remaining > 1 else ""} à planifier…</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 Tableau de Bord des Données (Temps réel)"):
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            t1,t2,t3 = st.tabs(["📉 Énergie","📈 Stress","❤️ Affection"])
            with t1: st.line_chart(df.pivot(index='Jour',columns='Personnage',values='Énergie'))
            with t2: st.line_chart(df.pivot(index='Jour',columns='Personnage',values='Stress'))
            with t3: st.line_chart(df.pivot(index='Jour',columns='Personnage',values='Affection'))
        else:
            st.info("Les données apparaîtront après le premier jour joué.")