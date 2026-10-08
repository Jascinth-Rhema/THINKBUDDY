import time
import streamlit as st
from llm import ask_llm, DETAIL_LEVELS
from prompt_templates import TECHNIQUES, build_prompt

st.set_page_config(page_title="ThinkBuddy", page_icon="🧠", layout="wide")

BADGES = {
    "Zero-Shot": ("ZS", "#6366f1"),
    "One-Shot": ("1S", "#0ea5e9"),
    "Few-Shot": ("FS", "#14b8a6"),
    "Chain of Thought (CoT)": ("CoT", "#f59e0b"),
    "Tree of Thought (ToT)": ("ToT", "#ec4899"),
}

# ====================== STYLES ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"], button, input, textarea, select {
    font-family: 'Inter', sans-serif !important;
}

/* ---------- force light + readable text ---------- */
.stApp {background:#f8fafc; color:#0f172a;}
.stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp div[data-testid="stMarkdownContainer"] {color:#0f172a;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {position:relative; z-index:1; padding-top:2rem; max-width:1200px;}

/* ---------- animated background blobs ---------- */
.blob {position:fixed; border-radius:50%; filter:blur(80px); opacity:.45;
       z-index:0; pointer-events:none; animation: drift 18s ease-in-out infinite;}
.b1 {width:420px; height:420px; background:#c7d2fe; top:-100px; left:-80px;}
.b2 {width:380px; height:380px; background:#fbcfe8; top:35%; right:-100px; animation-delay:-6s;}
.b3 {width:340px; height:340px; background:#a5f3fc; bottom:-120px; left:30%; animation-delay:-12s;}
@keyframes drift {
    0%,100% {transform:translate(0,0) scale(1)}
    33% {transform:translate(60px,40px) scale(1.12)}
    66% {transform:translate(-40px,70px) scale(.92)}
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {background:#ffffff; border-right:1px solid #e2e8f0;}
section[data-testid="stSidebar"] * {color:#0f172a;}
.side-title {font-size:.75rem; letter-spacing:.12em; font-weight:700; color:#64748b !important;
             text-transform:uppercase; margin:1rem 0 .6rem;}
.tech-item {display:flex; gap:.75rem; align-items:flex-start; padding:.65rem .7rem; border-radius:12px;
            border:1px solid #e2e8f0; margin-bottom:.5rem; background:#fff;
            transition: all .25s ease; animation: fadeUp .6s ease both;}
.tech-item:hover {transform:translateX(6px); box-shadow:0 6px 18px rgba(79,70,229,.12); border-color:#c7d2fe;}
.tech-badge {min-width:38px; height:28px; border-radius:8px; color:#fff !important; font-weight:700;
             font-size:.72rem; display:flex; align-items:center; justify-content:center;}
.tech-name {font-weight:600; font-size:.85rem; line-height:1.2;}
.tech-desc {font-size:.75rem; color:#64748b !important; line-height:1.3;}

/* ---------- hero ---------- */
.hero {display:flex; align-items:center; gap:2rem; padding:1rem 0 1.5rem; animation: fadeUp .7s ease both;}
.hero h1 {font-size:3.2rem; font-weight:800; margin:0; letter-spacing:-.03em;
          background:linear-gradient(90deg,#4f46e5,#0ea5e9,#ec4899,#4f46e5);
          background-size:300% 100%; -webkit-background-clip:text;
          -webkit-text-fill-color:transparent !important; animation: shine 6s linear infinite;}
.hero p {margin:.3rem 0 0; color:#475569 !important; font-size:1.05rem;}
.pill {display:inline-flex; align-items:center; gap:.45rem; padding:.3rem .8rem; border-radius:999px;
       background:#eef2ff; color:#4338ca !important; font-size:.78rem; font-weight:600; margin-bottom:.7rem;}
.pill i {width:8px; height:8px; border-radius:50%; background:#22c55e; display:inline-block;
         animation: ping 1.6s infinite;}
@keyframes ping {0%{box-shadow:0 0 0 0 rgba(34,197,94,.6)}100%{box-shadow:0 0 0 10px rgba(34,197,94,0)}}
@keyframes shine {to {background-position:300% 0}}
@keyframes fadeUp {from{opacity:0; transform:translateY(18px)} to{opacity:1; transform:translateY(0)}}

/* neural network svg */
.net line {stroke:#a5b4fc; stroke-width:1.5; stroke-dasharray:5 5; animation: flow 1.4s linear infinite;}
@keyframes flow {to {stroke-dashoffset:-20}}
.net circle {animation: glow 2.4s ease-in-out infinite; transform-box:fill-box; transform-origin:center;}
.net circle:nth-child(2n) {animation-delay:.4s}
.net circle:nth-child(3n) {animation-delay:.9s}
@keyframes glow {0%,100%{transform:scale(1); opacity:.85}50%{transform:scale(1.35); opacity:1}}

/* ---------- inputs ---------- */
.stTextArea textarea {background:#fff !important; color:#0f172a !important; border:1.5px solid #cbd5e1 !important;
                      border-radius:14px !important; font-size:1rem; transition:all .25s ease;}
.stTextArea textarea:focus {border-color:#4f46e5 !important; box-shadow:0 0 0 4px rgba(79,70,229,.15) !important;}
.stTextArea textarea::placeholder {color:#94a3b8 !important;}
div[data-baseweb="select"] > div {background:#fff !important; border:1.5px solid #cbd5e1 !important;
                                  border-radius:12px !important; color:#0f172a !important;}
div[data-baseweb="select"] * {color:#0f172a !important;}
div[data-baseweb="popover"] * {color:#0f172a !important; background-color:#fff;}
div[data-baseweb="tag"] {background:#eef2ff !important;}
div[data-baseweb="tag"] * {color:#4338ca !important;}
div[role="radiogroup"] label p {color:#0f172a !important; font-weight:500;}

/* ---------- button ---------- */
.stButton>button {width:100%; border:none; border-radius:14px; padding:.85rem; font-size:1rem;
    font-weight:700; color:#fff !important;
    background:linear-gradient(90deg,#4f46e5,#7c3aed,#0ea5e9,#4f46e5); background-size:300% 100%;
    box-shadow:0 10px 24px rgba(79,70,229,.3); animation: btnflow 5s linear infinite;
    transition:transform .2s ease, box-shadow .2s ease;}
.stButton>button p {color:#fff !important;}
.stButton>button:hover {transform:translateY(-3px); box-shadow:0 16px 32px rgba(79,70,229,.4); color:#fff;}
.stButton>button:active {transform:translateY(0);}
@keyframes btnflow {to {background-position:300% 0}}

/* ---------- result cards ---------- */
.res-head {display:flex; align-items:center; gap:.7rem; margin:1rem 0 .6rem; animation: fadeUp .5s ease both;}
.res-head .tech-badge {height:32px; min-width:46px; font-size:.8rem;}
.res-head b {font-size:1.1rem;}
div[data-testid="stVerticalBlockBorderWrapper"] {background:#fff; border:1px solid #e2e8f0 !important;
    border-radius:18px !important; box-shadow:0 10px 30px rgba(15,23,42,.06);
    animation: fadeUp .6s ease both; transition:box-shadow .3s ease;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {box-shadow:0 14px 40px rgba(79,70,229,.14);}
.chips {display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.6rem;}
.chip {padding:.25rem .7rem; border-radius:999px; background:#f1f5f9; color:#475569 !important;
       font-size:.75rem; font-weight:600;}

/* ---------- loader ---------- */
.loader {background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:1.3rem; margin:.5rem 0;}
.dots {display:flex; gap:6px; align-items:center; margin-bottom:1rem;}
.dots span {width:10px; height:10px; border-radius:50%; background:#4f46e5; animation: bounce 1s infinite;}
.dots span:nth-child(2){animation-delay:.15s; background:#0ea5e9}
.dots span:nth-child(3){animation-delay:.3s; background:#ec4899}
.dots small {margin-left:.6rem; color:#64748b !important; font-weight:600;}
@keyframes bounce {0%,80%,100%{transform:translateY(0); opacity:.5}40%{transform:translateY(-9px); opacity:1}}
.sk {height:12px; border-radius:6px; margin:.55rem 0;
     background:linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);
     background-size:200% 100%; animation: skel 1.4s infinite;}
@keyframes skel {to {background-position:-200% 0}}

/* ---------- temperature indicator ---------- */
.temp-box {padding:.7rem .9rem; border-radius:12px; background:#f8fafc; border:1px solid #e2e8f0; margin-top:.4rem;}
.temp-bar {height:6px; border-radius:6px; background:linear-gradient(90deg,#38bdf8,#facc15,#ef4444); position:relative; margin-top:.5rem;}
.temp-dot {position:absolute; top:-5px; width:16px; height:16px; border-radius:50%; background:#fff;
           border:3px solid #4f46e5; transform:translateX(-50%); transition:left .4s ease;}
</style>

<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
""", unsafe_allow_html=True)

# ====================== HERO ======================
st.markdown("""
<div class="hero">
<svg class="net" width="230" height="120" viewBox="0 0 230 120">
<line x1="30" y1="25" x2="115" y2="15"/><line x1="30" y1="25" x2="115" y2="60"/><line x1="30" y1="25" x2="115" y2="105"/>
<line x1="30" y1="60" x2="115" y2="15"/><line x1="30" y1="60" x2="115" y2="60"/><line x1="30" y1="60" x2="115" y2="105"/>
<line x1="30" y1="95" x2="115" y2="15"/><line x1="30" y1="95" x2="115" y2="60"/><line x1="30" y1="95" x2="115" y2="105"/>
<line x1="115" y1="15" x2="200" y2="40"/><line x1="115" y1="60" x2="200" y2="40"/><line x1="115" y1="105" x2="200" y2="40"/>
<line x1="115" y1="15" x2="200" y2="80"/><line x1="115" y1="60" x2="200" y2="80"/><line x1="115" y1="105" x2="200" y2="80"/>
<circle cx="30" cy="25" r="8" fill="#6366f1"/><circle cx="30" cy="60" r="8" fill="#6366f1"/><circle cx="30" cy="95" r="8" fill="#6366f1"/>
<circle cx="115" cy="15" r="8" fill="#0ea5e9"/><circle cx="115" cy="60" r="8" fill="#0ea5e9"/><circle cx="115" cy="105" r="8" fill="#0ea5e9"/>
<circle cx="200" cy="40" r="9" fill="#ec4899"/><circle cx="200" cy="80" r="9" fill="#ec4899"/>
</svg>
<div>
<div class="pill"><i></i>Prompt Engineering Workspace</div>
<h1>ThinkBuddy</h1>
<p>Compare Zero-Shot, One-Shot, Few-Shot, Chain of Thought and Tree of Thought side by side.</p>
</div>
</div>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown('<div class="side-title">Model Settings</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Low = precise and focused. High = creative and varied.")
    if temperature <= 0.3:
        label = "Precise"
    elif temperature <= 0.7:
        label = "Balanced"
    else:
        label = "Creative"
    st.markdown(
        f'<div class="temp-box"><b>{label}</b><span style="float:right;color:#64748b">{temperature:.2f}</span>'
        f'<div class="temp-bar"><div class="temp-dot" style="left:{temperature*100}%"></div></div></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    detail = st.select_slider("Answer length", options=list(DETAIL_LEVELS.keys()), value="Detailed")
    show_prompt = st.checkbox("Show generated prompt", value=False)

    st.markdown('<div class="side-title">Techniques</div>', unsafe_allow_html=True)
    for i, (name, info) in enumerate(TECHNIQUES.items()):
        b, c = BADGES[name]
        st.markdown(
            f'<div class="tech-item" style="animation-delay:{i*0.1}s">'
            f'<div class="tech-badge" style="background:{c}">{b}</div>'
            f'<div><div class="tech-name">{name}</div><div class="tech-desc">{info["desc"]}</div></div></div>',
            unsafe_allow_html=True,
        )

# ====================== INPUT ======================
task = st.text_area(
    "Your question or task",
    height=130,
    placeholder="e.g. A farmer has 17 sheep. All but 9 run away. How many are left?",
)

mode = st.radio("Mode", ["Single technique", "Compare techniques"], horizontal=True)

if mode == "Single technique":
    selected = [st.selectbox("Technique", list(TECHNIQUES.keys()))]
else:
    selected = st.multiselect(
        "Choose techniques to compare",
        list(TECHNIQUES.keys()),
        default=["Zero-Shot", "Chain of Thought (CoT)"],
    )

st.write("")
run = st.button("Generate Response")


# ====================== RUN ======================
def render(tech: str):
    badge, color = BADGES[tech]
    prompt = build_prompt(tech, task)

    st.markdown(
        f'<div class="res-head"><div class="tech-badge" style="background:{color}">{badge}</div>'
        f'<b>{tech}</b></div>',
        unsafe_allow_html=True,
    )
    if show_prompt:
        with st.expander("Prompt sent to the model"):
            st.code(prompt, language="text")

    loader = st.empty()
    loader.markdown(
        '<div class="loader"><div class="dots"><span></span><span></span><span></span>'
        '<small>Generating response...</small></div>'
        '<div class="sk" style="width:95%"></div><div class="sk" style="width:80%"></div>'
        '<div class="sk" style="width:88%"></div><div class="sk" style="width:60%"></div></div>',
        unsafe_allow_html=True,
    )
    try:
        start = time.time()
        answer = ask_llm(prompt, detail=detail, temperature=temperature)  # <-- the missing API call
        elapsed = time.time() - start
        loader.empty()
        with st.container(border=True):
            st.markdown(answer)  # <-- shows the model's answer
            st.markdown(
                f'<div class="chips"><span class="chip">{elapsed:.1f}s</span>'
                f'<span class="chip">Temp {temperature:.2f}</span>'
                f'<span class="chip">{detail}</span></div>',
                unsafe_allow_html=True,
            )
    except Exception as e:
        loader.empty()
        st.error(f"Something went wrong: {e}")


if run:
    if not task.strip():
        st.warning("Please enter a question first.")
    elif not selected:
        st.warning("Select at least one technique.")
    elif len(selected) == 1:
        render(selected[0])
    else:
        cols = st.columns(len(selected))
        for col, tech in zip(cols, selected):
            with col:
                render(tech)