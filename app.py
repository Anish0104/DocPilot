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
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,600;1,500&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─────────────────────────────────────────────────────────
   Design tokens
───────────────────────────────────────────────────────── */
:root {
    --bg:          #EDE9F8;
    --surface:     #FFFFFF;
    --border:      #E0D9F2;
    --accent:      #7C3AED;
    --accent-dark: #5B21B6;
    --accent-pale: #EDE9FE;
    --text-1:      #16102A;
    --text-2:      #52437A;
    --text-3:      #9282B8;
    --sb-bg:       #0D0920;
    --radius-sm:   10px;
    --radius-md:   16px;
    --radius-lg:   22px;
    --shadow-sm:   0 1px 3px rgba(20,5,70,.05), 0 2px 10px rgba(20,5,70,.04);
    --shadow-md:   0 4px 20px rgba(20,5,70,.08);
    --shadow-lg:   0 12px 48px rgba(20,5,70,.14);
    --shadow-purple: 0 8px 32px rgba(124,58,237,.22);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, * { font-family: 'Inter', sans-serif; }

/* ─────────────────────────────────────────────────────────
   App shell
───────────────────────────────────────────────────────── */
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottom"] > div > div > div { background: var(--bg) !important; }

[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div {
    background: var(--bg) !important;
    border: none !important;
    box-shadow: none !important;
    padding: 10px 0 6px !important;
}

/* ─────────────────────────────────────────────────────────
   Columns — persistent sidebar via :has()
───────────────────────────────────────────────────────── */
[data-testid="stHorizontalBlock"]:has(.sb-anchor) {
    gap: 0 !important;
    align-items: stretch !important;
}

/* Sidebar column */
div[data-testid="stColumn"]:has(.sb-anchor) {
    background: var(--sb-bg) !important;
    border-right: 1px solid rgba(255,255,255,.05) !important;
    padding: 0 !important;
    min-height: 100vh !important;
}
div[data-testid="stColumn"]:has(.sb-anchor) > div,
div[data-testid="stColumn"]:has(.sb-anchor) [data-testid="stVerticalBlock"],
div[data-testid="stColumn"]:has(.sb-anchor) [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--sb-bg) !important;
    min-height: 100vh !important;
    padding: 0 !important;
}

/* Nuke every Streamlit wrapper background inside sidebar */
div[data-testid="stColumn"]:has(.sb-anchor) .stMarkdown,
div[data-testid="stColumn"]:has(.sb-anchor) .stMarkdown > div,
div[data-testid="stColumn"]:has(.sb-anchor) .stMarkdown p,
div[data-testid="stColumn"]:has(.sb-anchor) .stMarkdown div,
div[data-testid="stColumn"]:has(.sb-anchor) .element-container,
div[data-testid="stColumn"]:has(.sb-anchor) [data-testid="element-container"],
div[data-testid="stColumn"]:has(.sb-anchor) .stButton > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Main column */
div[data-testid="stColumn"]:not(:has(.sb-anchor)) {
    padding: 0 36px 0 32px !important;
}

/* ─────────────────────────────────────────────────────────
   Sidebar — suggested-question buttons
───────────────────────────────────────────────────────── */
div[data-testid="stColumn"]:has(.sb-anchor) .stButton {
    padding: 0 !important;
    margin: 0 !important;
}
div[data-testid="stColumn"]:has(.sb-anchor) .stButton button {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: rgba(185,165,230,.65) !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    padding: 7px 20px 7px 20px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all .18s !important;
    line-height: 1.45 !important;
    letter-spacing: .01em !important;
    box-shadow: none !important;
    border-left: 2px solid transparent !important;
}
div[data-testid="stColumn"]:has(.sb-anchor) .stButton button:hover {
    background: rgba(124,58,237,.12) !important;
    color: #D4C4F8 !important;
    border-left-color: rgba(124,58,237,.6) !important;
    padding-left: 24px !important;
}
div[data-testid="stColumn"]:has(.sb-anchor) .stButton button:active {
    background: rgba(124,58,237,.18) !important;
}
div[data-testid="stColumn"]:has(.sb-anchor) hr {
    border-color: rgba(255,255,255,.06) !important;
    margin: 4px 0 !important;
}

/* ─────────────────────────────────────────────────────────
   Chat input
───────────────────────────────────────────────────────── */
[data-testid="stChatInput"] * { border-radius: 14px !important; }
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text-1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 14px 20px !important;
    box-shadow: var(--shadow-md) !important;
    transition: border-color .2s, box-shadow .2s !important;
    resize: none !important;
    outline: none !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(124,58,237,.5) !important;
    box-shadow: var(--shadow-md), 0 0 0 4px rgba(124,58,237,.07) !important;
    outline: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-3) !important; }

/* ─────────────────────────────────────────────────────────
   Chat messages
───────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-1) !important;
    margin-bottom: 14px !important;
    padding: 16px 20px !important;
    animation: msgIn .32s cubic-bezier(.16,1,.3,1) both;
}
@keyframes msgIn {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0);    }
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 40%, #6D28D9 100%) !important;
    border-color: transparent !important;
    box-shadow: var(--shadow-purple) !important;
    margin-left: 12% !important;
    margin-right: 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) > div:nth-child(2) {
    margin-right: 14px !important;
    margin-left: 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) li,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span {
    color: rgba(255,255,255,.94) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .msg-time {
    color: rgba(255,255,255,.35) !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    margin-right: 8% !important;
}

/* ── Code blocks — light bg, syntax highlighting untouched ── */
[data-testid="stChatMessage"] pre {
    background: #F6F4FF !important;
    border: 1px solid #D9D2F5 !important;
    border-radius: var(--radius-sm) !important;
    padding: 14px 18px !important;
    margin: 12px 0 6px !important;
    overflow-x: auto !important;
}
[data-testid="stChatMessage"] pre code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
    line-height: 1.7 !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stChatMessage"] code:not(pre > code) {
    background: rgba(124,58,237,.08) !important;
    border: 1px solid rgba(124,58,237,.15) !important;
    border-radius: 5px !important;
    padding: 1px 6px !important;
    font-size: 88% !important;
    color: #5028A8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) pre {
    background: rgba(255,255,255,.12) !important;
    border-color: rgba(255,255,255,.18) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) pre code {
    color: #EDE9FF !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) code:not(pre > code) {
    background: rgba(255,255,255,.16) !important;
    border-color: rgba(255,255,255,.24) !important;
    color: #fff !important;
}

/* ── Timestamps ── */
.msg-time {
    font-size: 10px;
    color: var(--text-3);
    margin-top: 8px;
    display: block;
    font-weight: 400;
}

/* ── Source pills ── */
.src-wrap {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 6px; margin-top: 14px; padding-top: 12px;
    border-top: 1px solid var(--border);
}
.src-label {
    width: 100%;
    font-size: 9px !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 1.5px !important;
    color: var(--text-3) !important; margin: 0 0 4px !important;
}
.src-pill {
    display: inline-flex; align-items: center; gap: 5px;
    border: 1px solid; border-radius: 99px;
    padding: 4px 11px;
    font-family: 'Inter', sans-serif; font-size: 11.5px; font-weight: 500;
    text-decoration: none; white-space: nowrap;
    transition: all .15s ease;
}
.src-pill:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,.08); }
.src-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; opacity: .7; }
.src-lib { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .6px; opacity: .6; }
.src-sep { opacity: .3; }

/* ── Thinking animation ── */
.thinking {
    display: flex; align-items: center; gap: 10px;
    color: var(--text-3); font-size: 13px; padding: 4px 0;
}
.dots { display: flex; gap: 5px; }
.dots span {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent); opacity: .3;
    animation: dp 1.3s ease-in-out infinite;
}
.dots span:nth-child(2) { animation-delay: .15s; }
.dots span:nth-child(3) { animation-delay: .3s; }
@keyframes dp {
    0%,80%,100% { transform: scale(.55); opacity: .25; }
    40%          { transform: scale(1.1); opacity: 1; }
}

/* ─────────────────────────────────────────────────────────
   Welcome chip buttons (3-col grid inside main)
───────────────────────────────────────────────────────── */
div[data-testid="stColumn"]:not(:has(.sb-anchor)) div[data-testid="stColumn"] .stButton button {
    background: transparent !important;
    border: 1.5px solid rgba(124,58,237,.25) !important;
    border-radius: var(--radius-sm) !important;
    padding: 11px 16px !important;
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--accent) !important;
    transition: all .18s ease !important;
    width: 100% !important;
    box-shadow: none !important;
}
div[data-testid="stColumn"]:not(:has(.sb-anchor)) div[data-testid="stColumn"] .stButton button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,.25) !important;
}

/* ─────────────────────────────────────────────────────────
   Scrollbar
───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,.18); border-radius: 4px; }

/* ─────────────────────────────────────────────────────────
   Sidebar HTML components
───────────────────────────────────────────────────────── */
.sb-anchor { display: none; }

.sb-logo {
    display: flex; align-items: center; gap: 11px;
    padding: 24px 20px 16px;
    border-bottom: 1px solid rgba(255,255,255,.05);
}
.sb-logo-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px; color: #fff;
    box-shadow: 0 0 0 1px rgba(139,92,246,.4), 0 4px 16px rgba(124,58,237,.5);
    flex-shrink: 0; letter-spacing: -.5px;
}
.sb-name { font-size: 14px; font-weight: 600; color: #E8E0FF; letter-spacing: -.2px; line-height: 1.2; }
.sb-sub  { font-size: 10.5px; color: rgba(180,160,230,.5); font-weight: 400; margin-top: 2px; }

.sb-online {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 20px; font-size: 11px; color: #34D399; font-weight: 500;
    background: rgba(52,211,153,.06);
    border-bottom: 1px solid rgba(255,255,255,.05);
    letter-spacing: .01em;
}
.sb-online-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #34D399; flex-shrink: 0;
    box-shadow: 0 0 0 2px rgba(52,211,153,.2);
    animation: pulse 2.2s ease infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.5; transform:scale(.75); }
}

.sb-section {
    font-size: 9px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.8px; color: rgba(130,110,190,.6);
    padding: 16px 20px 4px;
}
.sb-item {
    display: flex; align-items: center; gap: 9px;
    padding: 5px 20px; font-size: 12px; color: rgba(175,155,225,.55);
    line-height: 1.4;
}
.sb-item-dot {
    width: 3px; height: 3px; border-radius: 50%;
    background: rgba(124,58,237,.6); flex-shrink: 0;
}
.sb-footer {
    padding: 12px 20px;
    border-top: 1px solid rgba(255,255,255,.05);
    font-size: 10px; color: rgba(130,110,180,.45); line-height: 1.7;
}

/* ─────────────────────────────────────────────────────────
   Top nav
───────────────────────────────────────────────────────── */
.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 0 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 4px;
}
.topnav-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 99px; padding: 5px 14px;
    font-size: 11px; color: var(--accent); font-weight: 600;
    box-shadow: var(--shadow-sm);
    letter-spacing: .02em;
}
.topnav-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 0 2px rgba(124,58,237,.2);
    animation: pulse 2.2s ease infinite;
}
.topnav-links { display: flex; gap: 20px; }
.topnav-link  { font-size: 12px; color: var(--text-3); font-weight: 400; letter-spacing: .01em; }

/* ─────────────────────────────────────────────────────────
   Hero
───────────────────────────────────────────────────────── */
.hero {
    padding: 56px 0 32px; text-align: center;
    position: relative;
}
.hero-glow {
    position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    width: 700px; height: 340px; pointer-events: none;
    background: radial-gradient(ellipse 60% 60% at 50% 0%,
        rgba(124,58,237,.10) 0%, transparent 70%);
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 7px;
    background: var(--surface);
    border: 1px solid rgba(124,58,237,.18);
    border-radius: 99px; padding: 6px 16px;
    font-size: 11px; color: var(--accent); font-weight: 600;
    margin-bottom: 22px;
    box-shadow: var(--shadow-sm), 0 0 0 4px rgba(124,58,237,.04);
    letter-spacing: .02em;
}
.hero-heading {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 3.8vw, 2.9rem);
    font-weight: 600; color: var(--text-1);
    line-height: 1.15; letter-spacing: -.5px;
    margin-bottom: 14px;
}
.hero-heading em { font-style: italic; color: var(--accent); }
.hero-body {
    font-size: 15px; color: var(--text-2); font-weight: 400;
    line-height: 1.65; max-width: 420px; margin: 0 auto 32px;
}
.chips-label {
    font-size: 9px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; color: var(--text-3); margin-bottom: 12px;
}

/* ─────────────────────────────────────────────────────────
   Feature cards
───────────────────────────────────────────────────────── */
.cards {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 14px; margin: 28px 0 32px;
}
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px 18px 22px;
    box-shadow: var(--shadow-sm);
    transition: all .22s ease;
    position: relative; overflow: hidden;
}
.card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--card-c1), var(--card-c2));
    opacity: .7;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(124,58,237,.15);
}
.card-tag   { font-size: 9px; font-weight: 700; letter-spacing: 1.3px; text-transform: uppercase; color: var(--text-3); margin-bottom: 9px; }
.card-title { font-size: 13.5px; font-weight: 600; color: var(--text-1); margin-bottom: 6px; }
.card-desc  { font-size: 12px; color: var(--text-2); line-height: 1.65; }

.divider {
    display: flex; align-items: center; gap: 14px;
    margin: 6px 0 20px;
}
.divider-line { flex:1; height:1px; background: var(--border); }
.divider-text {
    font-size: 9.5px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1.8px; color: var(--text-3); white-space: nowrap;
}

/* ─────────────────────────────────────────────────────────
   Conversation view
───────────────────────────────────────────────────────── */
.conv-header {
    padding: 22px 0 14px; display: flex; align-items: center; gap: 10px;
}
.conv-title {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; color: var(--text-3);
}
.conv-count {
    font-size: 10px; background: var(--accent-pale);
    border: 1px solid rgba(124,58,237,.18); border-radius: 99px;
    padding: 2px 9px; color: var(--accent); font-weight: 600;
}

/* ─────────────────────────────────────────────────────────
   Mobile
───────────────────────────────────────────────────────── */
@media (max-width: 700px) {
    .cards { grid-template-columns: 1fr; }
    div[data-testid="stColumn"]:not(:has(.sb-anchor)) { padding: 0 14px !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])     { margin-left: 5% !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { margin-right: 5% !important; }
}
</style>
""", unsafe_allow_html=True)

# ── STATE ─────────────────────────────────────────────────────────────────────
if "messages"         not in st.session_state: st.session_state.messages         = []
if "pending_question" not in st.session_state: st.session_state.pending_question = None
if "pending_prompt"   not in st.session_state: st.session_state.pending_prompt   = None

hour     = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good evening" if hour >= 18 else "Good afternoon"

# ── LAYOUT ────────────────────────────────────────────────────────────────────
sb_col, main_col = st.columns([1.55, 4], gap="small")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with sb_col:
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

# ─── MAIN ─────────────────────────────────────────────────────────────────────
with main_col:
    st.markdown("""
    <div class="topnav">
      <div class="topnav-badge">
        <span class="topnav-dot"></span> AI · Docs · Live
      </div>
      <div class="topnav-links">
        <span class="topnav-link">HuggingFace</span>
        <span class="topnav-link">PyTorch</span>
        <span class="topnav-link">Scikit-learn</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WELCOME ──────────────────────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="hero">
          <div class="hero-glow"></div>
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
          <div class="card" style="--card-c1:#8B5CF6;--card-c2:#A78BFA;">
            <div class="card-tag">01 · HuggingFace</div>
            <div class="card-title">Transformers & Datasets</div>
            <div class="card-desc">Model loading, training pipelines, tokenizers and the full HF ecosystem.</div>
          </div>
          <div class="card" style="--card-c1:#EF4444;--card-c2:#F97316;">
            <div class="card-tag">02 · PyTorch</div>
            <div class="card-title">Tensors & Neural Nets</div>
            <div class="card-desc">Tensor ops, autograd, building models and custom training loops.</div>
          </div>
          <div class="card" style="--card-c1:#3B82F6;--card-c2:#06B6D4;">
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

    # ── CONVERSATION ─────────────────────────────────────────────────────────
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

    # ── PROCESS ACTIVE PROMPT (inside main_col so messages appear here) ──────
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
            "time":    ans_time,
        })
        st.rerun()

# ── CHAT INPUT ────────────────────────────────────────────────────────────────
raw = st.chat_input("Ask about HuggingFace, PyTorch or Scikit-learn…")
if raw:
    st.session_state.pending_prompt = raw
    st.rerun()
