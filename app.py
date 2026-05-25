import streamlit as st
from src.generator import ask
from datetime import datetime


def render_source_pills(sources):
    lib_config = {
        "huggingface.co":   {"label": "HuggingFace",  "color": "#92520A", "bg": "#FFF7ED", "border": "#FDDCB5"},
        "pytorch.org":      {"label": "PyTorch",       "color": "#9B1C0E", "bg": "#FFF2F0", "border": "#FDCDC8"},
        "scikit-learn.org": {"label": "Scikit-learn",  "color": "#0A5490", "bg": "#EFF6FF", "border": "#BFDBFE"},
    }
    skip = {"https:", "http:", "docs", "stable", "www", "en", "latest", ""}
    pills = []
    for url in sources:
        cfg = {"label": "Docs", "color": "#5B3FA6", "bg": "#F5F3FF", "border": "#DDD6FE"}
        for domain, c in lib_config.items():
            if domain in url:
                cfg = c
                break
        parts = [p for p in url.rstrip("/").split("/")
                 if p not in skip and not p.startswith(("huggingface", "pytorch", "scikit"))]
        page = parts[-1].replace("-", " ").replace("_", " ").replace(".html", "").title() if parts else "Docs"
        pills.append(
            f'<a href="{url}" target="_blank" class="src-pill" '
            f'style="color:{cfg["color"]};background:{cfg["bg"]};border-color:{cfg["border"]};">'
            f'<span class="src-dot" style="background:{cfg["color"]};"></span>'
            f'<span class="src-lib">{cfg["label"]}</span>'
            f'<span class="src-sep"> · </span>'
            f'<span class="src-page">{page}</span>'
            f'<span style="font-size:9px;opacity:.3;margin-left:3px;">↗</span>'
            f'</a>'
        )
    return (
        '<div class="src-wrap"><p class="src-label">Sources</p>'
        + "".join(pills) + "</div>"
    )


st.set_page_config(
    page_title="DocPilot",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Playfair+Display:ital,wght@0,600;1,500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:           #EEEAF7;
    --surface:      #FFFFFF;
    --border:       #DDD8EE;
    --accent:       #7C3AED;
    --accent-2:     #6D28D9;
    --accent-pale:  #EDE9FE;
    --text-1:       #1A1228;
    --text-2:       #5B4B7B;
    --text-3:       #9888BE;
    --sb-bg:        #130C22;
    --shadow-sm:    0 1px 4px rgba(40,10,100,.06), 0 2px 12px rgba(40,10,100,.05);
    --shadow-md:    0 4px 20px rgba(40,10,100,.09);
}

*, *::before, *::after { box-sizing: border-box; }
body, * { font-family: 'Inter', sans-serif; }

/* ── Shell ── */
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"]       { display: none !important; }
[data-testid="collapsedControl"]{ display: none !important; }

/* Kill stray white bars */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div { background: var(--bg) !important; }

/* ── Columns layout: target sidebar column via :has() ── */
div[data-testid="stColumn"]:has(> div > .sb-anchor) {
    background: var(--sb-bg) !important;
    border-right: 1px solid rgba(255,255,255,.06) !important;
    padding: 0 !important;
    min-height: 100vh !important;
}
div[data-testid="stColumn"]:has(> div > .sb-anchor) > div {
    background: var(--sb-bg) !important;
    min-height: 100vh !important;
    padding: 0 !important;
}

/* ── Sidebar buttons ── */
div[data-testid="stColumn"]:has(> div > .sb-anchor) .stButton button {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 9px !important;
    color: #B8A8D8 !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    padding: 7px 12px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all .15s !important;
    line-height: 1.45 !important;
}
div[data-testid="stColumn"]:has(> div > .sb-anchor) .stButton button:hover {
    background: rgba(124,58,237,.2) !important;
    border-color: rgba(124,58,237,.4) !important;
    color: #E2D4FF !important;
}
div[data-testid="stColumn"]:has(> div > .sb-anchor) hr {
    border-color: rgba(255,255,255,.07) !important;
    margin: 6px 0 !important;
}

/* ── Main column padding ── */
div[data-testid="stColumn"]:not(:has(> div > .sb-anchor)) {
    padding: 0 28px 0 24px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text-1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 13px 18px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: border-color .2s, box-shadow .2s !important;
    resize: none !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(124,58,237,.45) !important;
    box-shadow: var(--shadow-sm), 0 0 0 3px rgba(124,58,237,.08) !important;
    outline: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-3) !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-1) !important;
    margin-bottom: 14px !important;
    padding: 14px 18px !important;
    animation: msgIn .3s cubic-bezier(.16,1,.3,1) both;
}
@keyframes msgIn {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0);   }
}

/* User bubble — purple, right-side */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
    background: linear-gradient(135deg, #7C3AED 0%, #6625CC 100%) !important;
    border-color: transparent !important;
    box-shadow: 0 4px 22px rgba(109,40,217,.30) !important;
    margin-left: 14% !important;
    margin-right: 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) > div:nth-child(2) {
    margin-right: 12px !important;
    margin-left: 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) li,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span {
    color: rgba(255,255,255,.93) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .msg-time {
    color: rgba(255,255,255,.38) !important;
}

/* Assistant bubble — white, left-side */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    margin-right: 10% !important;
}

/* ── Code blocks: LIGHT background so syntax highlighting is readable ── */
[data-testid="stChatMessage"] pre {
    background: #F5F2FF !important;
    border: 1px solid #DBD4F5 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin: 10px 0 4px !important;
    overflow-x: auto !important;
}
/* Let Streamlit's pygments syntax colors show through — only set font */
[data-testid="stChatMessage"] pre code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
    line-height: 1.65 !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    /* NO color override — syntax highlighting stays visible */
}
/* Inline code */
[data-testid="stChatMessage"] code:not(pre > code) {
    background: rgba(124,58,237,.08) !important;
    border: 1px solid rgba(124,58,237,.15) !important;
    border-radius: 5px !important;
    padding: 1px 5px !important;
    font-size: 88% !important;
    color: #5028A8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
/* Code inside user bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) pre {
    background: rgba(255,255,255,.14) !important;
    border-color: rgba(255,255,255,.22) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) pre code {
    color: #F0E8FF !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) code:not(pre > code) {
    background: rgba(255,255,255,.18) !important;
    border-color: rgba(255,255,255,.28) !important;
    color: #fff !important;
}

/* ── Timestamp ── */
.msg-time {
    font-size: 10px;
    color: var(--text-3);
    margin-top: 6px;
    display: block;
}

/* ── Source pills ── */
.src-wrap {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 6px; margin-top: 12px; padding-top: 10px;
    border-top: 1px solid var(--border);
}
.src-label {
    width: 100%;
    font-size: 9px !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 1.3px !important;
    color: var(--text-3) !important; margin: 0 0 2px !important;
}
.src-pill {
    display: inline-flex; align-items: center; gap: 5px;
    border: 1px solid; border-radius: 99px;
    padding: 4px 10px;
    font-family: 'Inter', sans-serif; font-size: 11.5px; font-weight: 500;
    text-decoration: none; white-space: nowrap;
    transition: all .15s ease;
}
.src-pill:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,.10); }
.src-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; opacity: .7; }
.src-lib { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .7px; opacity: .65; }
.src-sep { opacity: .3; }

/* ── Thinking dots ── */
.thinking {
    display: flex; align-items: center; gap: 9px;
    color: var(--text-3); font-size: 13px; padding: 4px 0;
}
.dots { display: flex; gap: 4px; }
.dots span {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent); opacity: .35;
    animation: dp 1.2s ease-in-out infinite;
}
.dots span:nth-child(2) { animation-delay: .14s; }
.dots span:nth-child(3) { animation-delay: .28s; }
@keyframes dp {
    0%,80%,100% { transform: scale(.6); opacity: .3; }
    40%          { transform: scale(1);  opacity: .9; }
}

/* ── Welcome chip buttons (nested columns inside main col) ── */
div[data-testid="stColumn"]:not(:has(> div > .sb-anchor)) div[data-testid="stColumn"] .stButton button {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-2) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all .16s !important;
    width: 100% !important;
}
div[data-testid="stColumn"]:not(:has(> div > .sb-anchor)) div[data-testid="stColumn"] .stButton button:hover {
    background: var(--accent-pale) !important;
    border-color: rgba(124,58,237,.35) !important;
    color: var(--accent) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Back button ── */
.stButton button[kind="secondary"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,.18); border-radius: 4px; }

/* ── Sidebar HTML components ── */
.sb-anchor { display: none; }

.sb-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 22px 18px 14px;
    border-bottom: 1px solid rgba(255,255,255,.06);
}
.sb-logo-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #7C3AED, #A78BFA);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; color: #fff;
    box-shadow: 0 4px 14px rgba(124,58,237,.4);
    flex-shrink: 0;
}
.sb-name { font-size: 14px; font-weight: 600; color: #EDE9FE; letter-spacing: -.2px; }
.sb-sub  { font-size: 10px; color: #6B5B8A; font-weight: 400; margin-top: 1px; }

.sb-online {
    display: flex; align-items: center; gap: 7px;
    padding: 7px 18px; font-size: 11px; color: #4ADE80; font-weight: 500;
    background: rgba(74,222,128,.07);
    border-bottom: 1px solid rgba(255,255,255,.06);
}
.sb-online-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #4ADE80; flex-shrink: 0;
    animation: pulse 2s ease infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.4; transform:scale(.7); }
}

.sb-section {
    font-size: 9px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.7px; color: #4B3A72;
    padding: 14px 18px 5px;
}
.sb-item {
    display: flex; align-items: center; gap: 8px;
    padding: 5px 18px; font-size: 12px; color: #9880C8;
}
.sb-item-dot {
    width: 3px; height: 3px; border-radius: 50%;
    background: #7C3AED; flex-shrink: 0; opacity: .7;
}
.sb-footer {
    padding: 10px 18px;
    border-top: 1px solid rgba(255,255,255,.06);
    font-size: 10.5px; color: #4B3A72; line-height: 1.7;
}

/* ── Top nav ── */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 0 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 6px;
}
.topnav-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 99px; padding: 4px 12px;
    font-size: 11px; color: var(--accent); font-weight: 500;
    box-shadow: var(--shadow-sm);
}
.topnav-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--accent); animation: pulse 2s ease infinite; }
.topnav-links { display: flex; gap: 18px; }
.topnav-link  { font-size: 12px; color: var(--text-3); font-weight: 400; }

/* ── Hero ── */
.hero { padding: 48px 0 28px; text-align: center; }
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 7px;
    background: var(--accent-pale);
    border: 1px solid rgba(124,58,237,.18);
    border-radius: 99px; padding: 5px 14px;
    font-size: 11px; color: var(--accent); font-weight: 500;
    margin-bottom: 18px;
}
.hero-heading {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.9rem, 3.5vw, 2.6rem);
    font-weight: 600; color: var(--text-1);
    line-height: 1.2; letter-spacing: -.4px;
    margin-bottom: 12px;
}
.hero-heading em { font-style: italic; color: var(--accent); }
.hero-body {
    font-size: 14.5px; color: var(--text-2); font-weight: 400;
    line-height: 1.65; max-width: 430px; margin: 0 auto 28px;
}
.chips-label {
    font-size: 9px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 2px; color: var(--text-3); margin-bottom: 10px;
}

/* ── Feature cards ── */
.cards {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 12px; margin: 24px 0 28px;
}
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 18px 16px;
    box-shadow: var(--shadow-sm);
    transition: all .2s;
}
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); border-color: rgba(124,58,237,.2); }
.card-tag   { font-size: 9px; font-weight: 700; letter-spacing: 1.3px; text-transform: uppercase; color: var(--text-3); margin-bottom: 7px; }
.card-title { font-size: 13px; font-weight: 600; color: var(--text-1); margin-bottom: 5px; }
.card-desc  { font-size: 12px; color: var(--text-2); line-height: 1.6; }

.divider { display: flex; align-items: center; gap: 12px; margin: 4px 0 18px; }
.divider-line { flex:1; height:1px; background: var(--border); }
.divider-text { font-size: 9.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: var(--text-3); white-space: nowrap; }

/* ── Conversation header ── */
.conv-header { padding: 20px 0 12px; display: flex; align-items: center; gap: 8px; }
.conv-title  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.8px; color: var(--text-3); }
.conv-count  {
    font-size: 10px; background: var(--accent-pale);
    border: 1px solid rgba(124,58,237,.15); border-radius: 99px;
    padding: 2px 8px; color: var(--accent); font-weight: 600;
}

/* ── Mobile ── */
@media (max-width: 700px) {
    .cards { grid-template-columns: 1fr; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])     { margin-left: 5% !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { margin-right: 5% !important; }
    div[data-testid="stColumn"]:not(:has(> div > .sb-anchor)) { padding: 0 12px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── STATE ────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good evening" if hour >= 18 else "Good afternoon"

# ── COLUMNS LAYOUT ───────────────────────────────────────────────────────────
sb_col, main_col = st.columns([1.55, 4], gap="small")

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with sb_col:
    # This hidden div is the CSS :has() anchor that makes the column dark
    st.markdown('<div class="sb-anchor"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-mark">D</div>
        <div>
            <div class="sb-name">DocPilot</div>
            <div class="sb-sub">AI Documentation Assistant</div>
        </div>
    </div>
    <div class="sb-online">
        <span class="sb-online-dot"></span> Groq LLaMA 3.1 · Online
    </div>
    <div class="sb-section">Knowledge Base</div>
    <div>
        <div class="sb-item"><span class="sb-item-dot"></span>HuggingFace Transformers</div>
        <div class="sb-item"><span class="sb-item-dot"></span>HuggingFace Datasets</div>
        <div class="sb-item"><span class="sb-item-dot"></span>HuggingFace Pipelines</div>
        <div class="sb-item"><span class="sb-item-dot"></span>PyTorch Tensors</div>
        <div class="sb-item"><span class="sb-item-dot"></span>PyTorch Autograd</div>
        <div class="sb-item"><span class="sb-item-dot"></span>PyTorch Model Building</div>
        <div class="sb-item"><span class="sb-item-dot"></span>Scikit-learn Basics</div>
    </div>
    <div class="sb-section">Try Asking</div>
    """, unsafe_allow_html=True)

    for q in [
        "How do I load a dataset in HuggingFace?",
        "How do I create a tensor in PyTorch?",
        "How do I train a model with HuggingFace?",
        "How do I build a neural network in PyTorch?",
        "How does autograd work in PyTorch?",
        "What is the Trainer API?",
    ]:
        if st.button(q, use_container_width=True, key=f"sb_{q}"):
            st.session_state.pending_question = q

    st.divider()
    if st.button("🗑  Clear conversation", use_container_width=True, key="clear"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sb-footer">ChromaDB · Groq LLaMA 3.1 · Streamlit<br>100% free stack</div>',
        unsafe_allow_html=True,
    )

# ─── MAIN ────────────────────────────────────────────────────────────────────
with main_col:
    st.markdown("""
    <div class="topnav">
      <div class="topnav-badge"><span class="topnav-dot"></span> AI · Docs · Live</div>
      <div class="topnav-links">
        <span class="topnav-link">HuggingFace</span>
        <span class="topnav-link">PyTorch</span>
        <span class="topnav-link">Scikit-learn</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WELCOME ──
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="hero">
          <div class="hero-eyebrow">◈ &nbsp;Navigate your docs, not your frustration</div>
          <div class="hero-heading">{greeting}.<br>What are you <em>building</em>?</div>
          <div class="hero-body">Ask anything about HuggingFace, PyTorch or Scikit-learn — precise answers drawn directly from official docs, with sources cited.</div>
        </div>
        <div class="chips-label">Try one of these</div>
        """, unsafe_allow_html=True)

        chips = [
            "How do I load a dataset?",
            "Create a tensor in PyTorch",
            "Fine-tune a HuggingFace model",
            "Build a neural network",
            "What is autograd?",
            "How does the Trainer API work?",
        ]
        c1, c2, c3 = st.columns(3, gap="small")
        for i, chip in enumerate(chips):
            with [c1, c2, c3][i % 3]:
                if st.button(chip, key=f"chip_{i}", use_container_width=True):
                    st.session_state.pending_question = chip

        st.markdown("""
        <div class="cards">
          <div class="card">
            <div class="card-tag">01 · HuggingFace</div>
            <div class="card-title">Transformers & Datasets</div>
            <div class="card-desc">Model loading, training pipelines, tokenizers and the full HF ecosystem.</div>
          </div>
          <div class="card">
            <div class="card-tag">02 · PyTorch</div>
            <div class="card-title">Tensors & Neural Nets</div>
            <div class="card-desc">Tensor ops, autograd, building models and custom training loops.</div>
          </div>
          <div class="card">
            <div class="card-tag">03 · Scikit-learn</div>
            <div class="card-title">Classical ML</div>
            <div class="card-desc">Supervised learning, preprocessing, model evaluation and pipelines.</div>
          </div>
        </div>
        <div class="divider">
          <div class="divider-line"></div>
          <div class="divider-text">or type your own question below</div>
          <div class="divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

    # ── CONVERSATION ──
    else:
        n = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"""
        <div class="conv-header">
          <span class="conv-title">Conversation</span>
          <span class="conv-count">{n} question{"s" if n != 1 else ""}</span>
        </div>
        """, unsafe_allow_html=True)

        back_col, _ = st.columns([1, 6])
        with back_col:
            if st.button("← Back", use_container_width=True, key="back_btn"):
                st.session_state.messages = []
                st.rerun()

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "time" in msg:
                    st.markdown(f'<span class="msg-time">{msg["time"]}</span>', unsafe_allow_html=True)
                if "sources" in msg:
                    st.markdown(render_source_pills(msg["sources"]), unsafe_allow_html=True)

    # ── PROCESS PROMPT (inside main_col so messages render here) ──
    active = st.session_state.pending_question or st.session_state.pending_prompt
    if active:
        st.session_state.pending_question = None
        st.session_state.pending_prompt   = None
        now = datetime.now().strftime("%H:%M")

        with st.chat_message("user"):
            st.markdown(active)
            st.markdown(f'<span class="msg-time">{now}</span>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": active, "time": now})

        with st.chat_message("assistant"):
            ph = st.empty()
            ph.markdown(
                '<div class="thinking">'
                '<div class="dots"><span></span><span></span><span></span></div>'
                'Searching documentation…'
                '</div>',
                unsafe_allow_html=True,
            )
            result   = ask(active)
            ans_time = datetime.now().strftime("%H:%M")
            ph.empty()
            st.markdown(result["answer"])
            st.markdown(f'<span class="msg-time">{ans_time}</span>', unsafe_allow_html=True)
            st.markdown(render_source_pills(result["sources"]), unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "time": ans_time,
        })
        st.rerun()

# ── CHAT INPUT (full-width, below columns) ───────────────────────────────────
raw = st.chat_input("Ask about HuggingFace, PyTorch or Scikit-learn…")
if raw:
    st.session_state.pending_prompt = raw
    st.rerun()
