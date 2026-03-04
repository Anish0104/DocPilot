import streamlit as st
from src.generator import ask
from datetime import datetime

st.set_page_config(
    page_title="DocPilot — AI Documentation Assistant",
    page_icon="◈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,500&display=swap');

:root {
    --glass-bg: rgba(255,255,255,0.55);
    --glass-border: rgba(255,255,255,0.80);
    --glass-shadow: 0 8px 32px rgba(124,58,237,0.10), 0 2px 8px rgba(124,58,237,0.06);
    --accent: #7C3AED;
    --accent-soft: #C9A8E8;
    --accent-pale: #E8D5F5;
    --text-primary: #1e1328;
    --text-secondary: #6b5b8a;
    --text-muted: #a898c0;
}

* { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(167,139,250,0.45) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 5%,   rgba(139,92,246,0.30) 0%, transparent 50%),
        radial-gradient(ellipse 70% 55% at 50% 100%,  rgba(196,167,243,0.40) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 80% 60%,  rgba(167,139,250,0.20) 0%, transparent 50%),
        radial-gradient(ellipse 40% 30% at 20% 70%,  rgba(124,58,237,0.12)  0%, transparent 50%),
        linear-gradient(160deg, #f3ecfd 0%, #e8d9f8 20%, #dccef4 45%, #cfc2ef 70%, #c5b5eb 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Kill white bottom bar ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottom"] > div > div > div {
    background: transparent !important;
    background-color: transparent !important;
}
.stApp > div { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.65) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid var(--glass-border) !important;
    box-shadow: 4px 0 24px rgba(124,58,237,0.07) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    border-radius: 14px !important;
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 12.5px !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 9px 14px !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(124,58,237,0.07) !important;
    color: var(--accent) !important;
}

/* ── Fix chat input — remove all borders and pointed corners ── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] > div > div > div,
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
    border-radius: 20px !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.80) !important;
    backdrop-filter: blur(20px) !important;
    border: 1.5px solid rgba(201,168,232,0.4) !important;
    border-radius: 20px !important;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14.5px !important;
    font-weight: 400 !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08), 0 1px 4px rgba(124,58,237,0.04) !important;
    padding: 16px 20px !important;
    resize: none !important;
    outline: none !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(124,58,237,0.4) !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.12), 0 0 0 3px rgba(124,58,237,0.07) !important;
    outline: none !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
    font-weight: 300 !important;
}
[data-testid="stChatInput"] textarea::-webkit-resizer { display: none; }

/* ── Nuke every border/radius on ALL chat input wrappers ── */
[data-testid="stChatInput"] *,
[data-testid="stChatInputContainer"] * {
    border-radius: 20px !important;
    border-top-left-radius: 20px !important;
    border-top-right-radius: 20px !important;
    border-bottom-left-radius: 20px !important;
    border-bottom-right-radius: 20px !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    overflow: hidden !important;
    border-radius: 20px !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.78) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 20px !important;
    margin-bottom: 12px !important;
    box-shadow: var(--glass-shadow) !important;
    color: var(--text-primary) !important;
}

/* ── Expander ── */
details summary {
    background: rgba(255,255,255,0.5) !important;
    border-radius: 14px !important;
    color: var(--text-secondary) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    font-size: 12.5px !important;
}

hr { border-color: rgba(124,58,237,0.1) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.18); border-radius: 4px; }

/* ── Chip buttons — purple-tinted glass ── */
div[data-testid="column"] .stButton > button,
div[data-testid="column"] .stButton > button:focus,
div[data-testid="column"] .stButton > button:active,
[data-testid="stHorizontalBlock"] div[data-testid="column"] button {
    background: rgba(124,58,237,0.12) !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    border-radius: 16px !important;
    padding: 11px 16px !important;
    font-size: 12.5px !important;
    color: #5b3fa6 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.5), 0 2px 8px rgba(124,58,237,0.08) !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
    text-align: center !important;
}
div[data-testid="column"] .stButton > button:hover,
[data-testid="stHorizontalBlock"] div[data-testid="column"] button:hover {
    background: rgba(124,58,237,0.20) !important;
    border-color: rgba(124,58,237,0.50) !important;
    color: #4c1d95 !important;
    transform: translateY(-2px) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.5), 0 6px 20px rgba(124,58,237,0.18) !important;
}

/* ── Sidebar components ── */
.sb-brand {
    display: flex; align-items: center; gap: 11px;
    padding: 26px 18px 18px;
    border-bottom: 1px solid rgba(124,58,237,0.08);
    margin-bottom: 4px;
}
.sb-brand-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #7C3AED, #C9A8E8);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(124,58,237,0.28);
    color: white; font-weight: 700; font-size: 15px;
}
.sb-brand-name { font-size: 15px; font-weight: 600; color: var(--text-primary); letter-spacing: -0.3px; }
.sb-brand-sub { font-size: 10.5px; color: var(--text-muted); font-weight: 300; margin-top: 1px; }

/* ── NEW: Online status badge ── */
.sb-status {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 18px; font-size: 11.5px;
    color: #16a34a; font-weight: 500;
    border-bottom: 1px solid rgba(124,58,237,0.08);
    background: rgba(240,253,244,0.5);
}
.sb-status-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #16a34a; flex-shrink: 0;
    animation: pulse 2s ease infinite;
}

.sb-label {
    font-size: 9.5px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.8px; color: var(--text-muted);
    margin: 18px 0 6px 18px;
}
.sb-source {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 18px; border-radius: 9px;
    font-size: 12.5px; color: var(--text-secondary);
    margin: 0 6px 2px; transition: all 0.15s; cursor: default;
}
.sb-source:hover { background: rgba(124,58,237,0.06); color: var(--accent); }
.sb-dot { width: 5px; height: 5px; border-radius: 50%; background: linear-gradient(135deg, #7C3AED, #C9A8E8); flex-shrink: 0; }
.sb-footer {
    padding: 14px 18px; border-top: 1px solid rgba(124,58,237,0.08);
    font-size: 10.5px; color: var(--text-muted); line-height: 1.7;
}

/* ── Main layout ── */
.main-wrap { max-width: 800px; margin: 0 auto; padding: 0 40px; }

.top-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 0 18px;
    border-bottom: 1px solid rgba(124,58,237,0.08);
    margin-bottom: 4px;
}
.nav-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 24px; padding: 5px 14px;
    font-size: 11.5px; color: var(--accent); font-weight: 500;
    backdrop-filter: blur(12px);
    box-shadow: 0 2px 8px rgba(124,58,237,0.08);
}
.nav-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--accent); animation: pulse 2s ease infinite; }
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.75); }
}
.nav-links { display: flex; gap: 24px; }
.nav-link { font-size: 12.5px; color: var(--text-muted); font-weight: 400; }

/* Welcome */
.welcome-wrap { padding: 52px 0 32px; text-align: center; }
.welcome-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(201,168,232,0.5);
    border-radius: 24px; padding: 6px 16px;
    font-size: 11.5px; color: var(--accent); font-weight: 500;
    margin-bottom: 22px;
    backdrop-filter: blur(12px);
    box-shadow: 0 2px 12px rgba(124,58,237,0.08);
}
.welcome-heading {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem; font-weight: 600;
    color: var(--text-primary);
    line-height: 1.18; letter-spacing: -0.5px;
    margin-bottom: 14px;
}
.welcome-heading em { font-style: italic; color: var(--accent); }
.welcome-body {
    font-size: 15px; color: var(--text-secondary);
    font-weight: 300; line-height: 1.65;
    max-width: 460px; margin: 0 auto 36px;
}

.chips-label {
    font-size: 9.5px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 2px; color: var(--text-muted);
    margin-bottom: 10px; text-align: center;
}

/* Cards */
.cards-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-bottom: 36px; }
.glass-card {
    background: var(--glass-bg); backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 22px; padding: 22px 20px;
    box-shadow: var(--glass-shadow);
    transition: all 0.22s ease; text-align: left;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 48px rgba(124,58,237,0.14);
    border-color: rgba(201,168,232,0.8);
}
.card-num { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; color: var(--accent-soft); text-transform: uppercase; margin-bottom: 10px; }
.card-title { font-size: 13.5px; font-weight: 600; color: var(--text-primary); margin-bottom: 7px; }
.card-body { font-size: 12px; color: var(--text-secondary); line-height: 1.6; font-weight: 300; }

.section-rule { display:flex; align-items:center; gap:12px; margin-bottom: 20px; }
.rule-line { flex:1; height:1px; background:rgba(124,58,237,0.1); }
.rule-label { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:1.8px; color:var(--text-muted); }

/* ── NEW: Conversation header with counter ── */
.conv-header { padding: 28px 0 16px; display: flex; align-items: center; gap: 10px; }
.conv-title { font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: var(--text-muted); }
.conv-count {
    font-size: 10px; background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.15); border-radius: 24px;
    padding: 2px 8px; color: var(--text-secondary); font-weight: 500;
}

/* ── NEW: Mobile Media Queries ── */
@media (max-width: 768px) {
    .main-wrap { padding: 0 16px; }
    .cards-row { grid-template-columns: 1fr; gap: 12px; }
    .nav-links { gap: 12px; }
    .nav-link { font-size: 11px; }
    .conv-header { 
        padding: 16px 0 8px; 
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    /* Give chat input container some breathing room on mobile to avoid overlapping */
    [data-testid="stChatInput"] {
        padding-bottom: 24px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-mark">D</div>
        <div>
            <div class="sb-brand-name">DocPilot</div>
            <div class="sb-brand-sub">AI Documentation Assistant</div>
        </div>
    </div>
    <div class="sb-status">
        <span class="sb-status-dot"></span> Groq LLaMA 3.1 — Online
    </div>
    """, unsafe_allow_html=True)

    # UPDATED: 7 sources including Scikit-learn
    st.markdown('<div class="sb-label">Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
        <div class="sb-source"><span class="sb-dot"></span>HuggingFace Transformers</div>
        <div class="sb-source"><span class="sb-dot"></span>HuggingFace Datasets</div>
        <div class="sb-source"><span class="sb-dot"></span>HuggingFace Pipelines</div>
        <div class="sb-source"><span class="sb-dot"></span>PyTorch Tensors</div>
        <div class="sb-source"><span class="sb-dot"></span>PyTorch Autograd</div>
        <div class="sb-source"><span class="sb-dot"></span>PyTorch Model Building</div>
        <div class="sb-source"><span class="sb-dot"></span>Scikit-learn Basics</div>
    </div>
    """, unsafe_allow_html=True)

    # UPDATED: 6 suggested questions
    st.markdown('<div class="sb-label">Suggested Questions</div>', unsafe_allow_html=True)
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
    if st.button("Clear Conversation", use_container_width=True, key="clear"):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sb-footer">Built with ChromaDB, Groq LLaMA 3.1<br>and Streamlit — 100% free stack</div>', unsafe_allow_html=True)

# ── STATE ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good evening" if hour >= 18 else "Good afternoon"

# ── MAIN ──
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# UPDATED: Scikit-learn added to nav
st.markdown("""
<div class="top-nav">
    <div class="nav-badge"><span class="nav-dot"></span> AI · Docs · Live</div>
    <div class="nav-links">
        <span class="nav-link">HuggingFace</span>
        <span class="nav-link">PyTorch</span>
        <span class="nav-link">Scikit-learn</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    # UPDATED: body text mentions Scikit-learn
    st.markdown(f"""
    <div class="welcome-wrap">
        <div class="welcome-eyebrow">◈ &nbsp;Navigate your docs, not your frustration</div>
        <div class="welcome-heading">{greeting}.<br>What are you <em>building</em>?</div>
        <div class="welcome-body">Ask anything about HuggingFace, PyTorch or Scikit-learn and get precise answers drawn directly from official documentation — with sources cited.</div>
    </div>
    <div class="chips-label">Try one of these</div>
    """, unsafe_allow_html=True)

    # UPDATED: functional chip buttons (replaces static HTML chips)
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
                st.rerun()

    # UPDATED: third card is now Scikit-learn
    st.markdown("""
    <div class="cards-row">
        <div class="glass-card">
            <div class="card-num">01 — HuggingFace</div>
            <div class="card-title">Transformers & Datasets</div>
            <div class="card-body">Model loading, training pipelines, tokenizers and the full HF ecosystem.</div>
        </div>
        <div class="glass-card">
            <div class="card-num">02 — PyTorch</div>
            <div class="card-title">Tensors & Neural Nets</div>
            <div class="card-body">Tensor ops, autograd, building models and training loops.</div>
        </div>
        <div class="glass-card">
            <div class="card-num">03 — Scikit-learn</div>
            <div class="card-title">Classical ML</div>
            <div class="card-body">Supervised learning, preprocessing, model evaluation and pipelines.</div>
        </div>
    </div>
    <div class="section-rule">
        <div class="rule-line"></div>
        <div class="rule-label">or type your own question below</div>
        <div class="rule-line"></div>
    </div>
    """, unsafe_allow_html=True)

else:
    # UPDATED: conversation counter
    n = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.markdown(f"""
    <div class="conv-header">
        <div class="conv-title">Conversation</div>
        <div class="conv-count">{n} question{"s" if n != 1 else ""}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── NEW: Action row with Back button ──
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", use_container_width=True, key="back_btn"):
            st.session_state.messages = []
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.markdown(f"- [{source}]({source})")

st.markdown('</div>', unsafe_allow_html=True)

# ── INPUT → RAG ──
if st.session_state.pending_question:
    prompt = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    # UPDATED: placeholder mentions all 3 libraries
    prompt = st.chat_input("Ask anything about HuggingFace, PyTorch or Scikit-learn...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching documentation..."):
            result = ask(prompt)
        st.markdown(result["answer"])
        with st.expander("View Sources"):
            for source in result["sources"]:
                st.markdown(f"- [{source}]({source})")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })
    st.rerun()