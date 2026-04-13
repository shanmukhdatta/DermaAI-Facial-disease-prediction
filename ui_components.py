"""
ui_components.py - All UI rendering functions and custom CSS
"""

import streamlit as st
import numpy as np
from typing import Dict, Any, List, Tuple


def inject_custom_css():
    """Inject all custom styling."""
    st.markdown("""
    <style>
    /* ── Google Fonts ───────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── CSS Variables ──────────────────────────────────── */
    :root {
        --bg-primary:    #0a0e1a;
        --bg-secondary:  #111827;
        --bg-card:       #1a2235;
        --bg-card-hover: #1e2940;
        --accent-teal:   #00d4aa;
        --accent-blue:   #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-red:    #ef4444;
        --accent-green:  #10b981;
        --text-primary:  #f1f5f9;
        --text-secondary:#94a3b8;
        --text-muted:    #64748b;
        --border:        #1e2d47;
        --border-accent: #2d4a6e;
        --radius:        14px;
        --shadow:        0 4px 24px rgba(0,0,0,0.4);
        --glow-teal:     0 0 30px rgba(0,212,170,0.15);
        --glow-blue:     0 0 30px rgba(59,130,246,0.15);
    }

    /* ── Global Reset ───────────────────────────────────── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* Remove default padding */
    .block-container { 
        padding-top: 1.5rem !important; 
        max-width: 1400px !important;
    }

    /* ── Sidebar ────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    .sidebar-brand {
        display: flex; align-items: center; gap: 10px;
        padding: 8px 0 16px;
    }
    .brand-icon { font-size: 2rem; }
    .brand-text { 
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem; font-weight: 700;
        background: linear-gradient(135deg, var(--accent-teal), var(--accent-blue));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* ── Header ─────────────────────────────────────────── */
    .derma-header {
        background: linear-gradient(135deg, #0f1923 0%, #1a2235 50%, #0f2030 100%);
        border: 1px solid var(--border-accent);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow), var(--glow-teal);
    }
    .derma-header::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at top left, rgba(0,212,170,0.08) 0%, transparent 60%),
                    radial-gradient(ellipse at bottom right, rgba(59,130,246,0.08) 0%, transparent 60%);
        pointer-events: none;
    }
    .header-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(0,212,170,0.1); border: 1px solid rgba(0,212,170,0.3);
        border-radius: 20px; padding: 4px 12px;
        font-size: 0.75rem; font-weight: 600; color: var(--accent-teal);
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }
    .header-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem; font-weight: 700;
        background: linear-gradient(135deg, #f1f5f9 0%, var(--accent-teal) 60%, var(--accent-blue) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0; line-height: 1.2;
    }
    .header-sub {
        color: var(--text-secondary); font-size: 1rem; margin-top: 0.5rem;
    }
    .header-stats {
        display: flex; gap: 1.5rem; margin-top: 1.2rem; flex-wrap: wrap;
    }
    .stat-pill {
        background: rgba(255,255,255,0.05); border: 1px solid var(--border);
        border-radius: 10px; padding: 6px 14px;
        font-size: 0.82rem; color: var(--text-secondary);
    }
    .stat-pill strong { color: var(--text-primary); }

    /* ── Cards ──────────────────────────────────────────── */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .card:hover {
        border-color: var(--border-accent);
        box-shadow: var(--shadow);
    }

    /* ── Prediction Card ────────────────────────────────── */
    .pred-card {
        background: linear-gradient(135deg, #1a2235, #131e30);
        border-radius: 18px;
        padding: 0;
        overflow: hidden;
        box-shadow: var(--shadow), var(--glow-teal);
        border: 1px solid var(--border-accent);
    }
    .pred-header {
        padding: 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    .pred-disease-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem; font-weight: 700;
        margin: 0;
    }
    .pred-body { padding: 1.5rem; }
    .confidence-bar-wrapper {
        background: rgba(255,255,255,0.05);
        border-radius: 50px; height: 10px;
        overflow: hidden; margin: 8px 0;
    }
    .confidence-bar {
        height: 100%; border-radius: 50px;
        background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue));
        transition: width 0.8s ease;
    }
    .severity-badge {
        display: inline-block;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
        background: rgba(255,255,255,0.08);
        color: var(--text-secondary);
        margin-top: 4px;
    }

    /* Top-3 items */
    .top3-item {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 14px; border-radius: 10px;
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        margin-bottom: 6px;
        font-size: 0.88rem;
    }
    .top3-rank {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-muted); font-size: 0.75rem; min-width: 20px;
    }
    .top3-name { flex: 1; color: var(--text-primary); font-weight: 500; }
    .top3-pct {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent-teal); font-weight: 600;
    }
    .top3-mini-bar {
        width: 60px; height: 4px; border-radius: 2px;
        background: rgba(255,255,255,0.08);
        overflow: hidden;
    }
    .top3-mini-fill {
        height: 100%; border-radius: 2px;
        background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue));
    }

    /* Precautions list */
    .precaution-item {
        display: flex; align-items: flex-start; gap: 10px;
        padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 0.875rem; color: var(--text-secondary);
        line-height: 1.5;
    }
    .precaution-icon { color: var(--accent-teal); flex-shrink: 0; margin-top: 2px; }

    /* ── Validation badges ──────────────────────────────── */
    .validation-row {
        display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0;
    }
    .val-badge {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;
        font-weight: 500; border: 1px solid;
    }
    .val-pass {
        background: rgba(16,185,129,0.1); color: #10b981;
        border-color: rgba(16,185,129,0.3);
    }
    .val-fail {
        background: rgba(239,68,68,0.1); color: #ef4444;
        border-color: rgba(239,68,68,0.3);
    }

    /* ── Loading animation ──────────────────────────────── */
    .loading-wrapper {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding: 3rem 1rem;
        min-height: 200px;
    }
    .loading-spinner {
        width: 56px; height: 56px;
        border: 3px solid rgba(0,212,170,0.15);
        border-top-color: var(--accent-teal);
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
        margin-bottom: 1.2rem;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading-text {
        font-size: 0.9rem; color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }

    /* ── Empty state ────────────────────────────────────── */
    .empty-state {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding: 4rem 2rem;
        border: 2px dashed var(--border);
        border-radius: 18px; text-align: center;
        min-height: 300px;
    }
    .empty-icon { font-size: 3rem; margin-bottom: 1rem; }
    .empty-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem; font-weight: 600; color: var(--text-primary);
    }
    .empty-sub { font-size: 0.9rem; color: var(--text-muted); margin-top: 0.3rem; }

    /* ── History item ───────────────────────────────────── */
    .history-item {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: var(--radius); padding: 1rem 1.2rem;
        margin-bottom: 0.8rem; display: flex;
        align-items: center; gap: 1rem;
        transition: border-color 0.2s;
    }
    .history-item:hover { border-color: var(--border-accent); }
    .history-thumb { 
        width: 56px; height: 56px; object-fit: cover; 
        border-radius: 10px; flex-shrink: 0;
    }
    .history-info { flex: 1; }
    .history-disease {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600; color: var(--text-primary); font-size: 0.95rem;
    }
    .history-meta { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
    .history-conf {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem; font-weight: 700; color: var(--accent-teal);
    }

    /* ── Camera guide overlay ───────────────────────────── */
    .camera-guide {
        background: rgba(0,0,0,0.3); border-radius: 12px;
        padding: 8px; margin-bottom: 8px; text-align: center;
        border: 1px dashed var(--border-accent);
    }
    .alignment-frame {
        display: inline-block; position: relative;
        width: 200px; height: 200px;
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 8px; margin: 8px auto;
    }
    .corner {
        position: absolute; width: 20px; height: 20px;
        border-color: var(--accent-teal); border-style: solid;
    }
    .tl { top: -2px; left: -2px; border-width: 3px 0 0 3px; }
    .tr { top: -2px; right: -2px; border-width: 3px 3px 0 0; }
    .bl { bottom: -2px; left: -2px; border-width: 0 0 3px 3px; }
    .br { bottom: -2px; right: -2px; border-width: 0 3px 3px 0; }
    .guide-text {
        position: absolute; bottom: -28px; left: 50%;
        transform: translateX(-50%);
        font-size: 0.72rem; color: var(--text-muted);
        white-space: nowrap;
    }

    /* ── Disclaimer ─────────────────────────────────────── */
    .disclaimer-box {
        background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25);
        border-radius: 10px; padding: 12px;
        font-size: 0.78rem; color: #fca5a5; line-height: 1.5;
    }
    .disclaimer-title {
        font-weight: 700; color: #ef4444; margin-bottom: 4px;
        display: flex; align-items: center; gap: 5px;
    }

    /* ── Tabs ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important;
        gap: 4px !important;
        padding: 4px !important;
        border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: var(--text-muted) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-accent) !important;
    }

    /* ── Buttons ────────────────────────────────────────── */
    .stButton > button {
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-teal), var(--accent-blue)) !important;
        border: none !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(0,212,170,0.25) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(0,212,170,0.35) !important;
    }

    /* ── Upload area ────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        border: 2px dashed var(--border-accent) !important;
        border-radius: 12px !important;
        background: rgba(255,255,255,0.02) !important;
    }

    /* ── Headings ───────────────────────────────────────── */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Scrollbar ──────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border-accent); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-teal); }

    /* ── Success/Warning/Error ──────────────────────────── */
    .stSuccess { border-radius: 10px !important; }
    .stAlert { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="derma-header">
        <div class="header-badge">🔬 AI-Powered • Multi-Model Ensemble</div>
        <h1 class="header-title">DermaAI</h1>
        <p class="header-sub">Professional Skin Disease Classification System</p>
        <div class="header-stats">
            <div class="stat-pill"><strong>13</strong> Disease Classes</div>
            <div class="stat-pill"><strong>5+</strong> Ensemble Models</div>
            <div class="stat-pill"><strong>Weighted</strong> SVM Priority</div>
            <div class="stat-pill"><strong>Real-Time</strong> Validation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_validation_badge(validation: dict):
    checks = validation["checks"]
    label_map = {
        "brightness": "💡 Brightness",
        "blur": "🔍 Focus",
        "skin": "🤚 Skin Region",
        "resolution": "📐 Resolution",
    }
    badges_html = '<div class="validation-row">'
    for key, check in checks.items():
        cls = "val-pass" if check["passed"] else "val-fail"
        icon = "✓" if check["passed"] else "✗"
        label = label_map.get(key, key)
        badges_html += f'<span class="val-badge {cls}">{icon} {label}</span>'
    badges_html += "</div>"

    if not validation["passed"]:
        failed = [v["msg"] for v in checks.values() if not v["passed"]]
        badges_html += "<ul style='margin:6px 0 0 0;padding-left:18px;font-size:0.82rem;color:#f87171;'>"
        for msg in failed:
            badges_html += f"<li>{msg}</li>"
        badges_html += "</ul>"

    st.markdown(badges_html, unsafe_allow_html=True)


def render_prediction_card(results: dict, disease_info: dict):
    top_class   = results["top_class"]
    confidence  = results["confidence"]
    top3        = results["top3"]
    models_used = results["models_used"]

    info = disease_info.get(top_class, {})
    color     = info.get("color", "#00d4aa")
    emoji     = info.get("emoji", "🔬")
    severity  = info.get("severity", "Unknown")
    desc      = info.get("description", "No description available.")
    prec_list = info.get("precautions", [])

    conf_pct = f"{confidence * 100:.1f}%"

    # ── Main card ─────────────────────────────────────────
    st.markdown(f"""
    <div class="pred-card">
        <div class="pred-header" style="background: linear-gradient(135deg, {color}18, transparent);">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:2.5rem;">{emoji}</span>
                <div>
                    <p class="pred-disease-name" style="color:{color};">
                        {top_class.replace("_", " ")}
                    </p>
                    <span class="severity-badge">Severity: {severity}</span>
                </div>
                <div style="margin-left:auto; text-align:right;">
                    <div style="font-family:'JetBrains Mono',monospace; font-size:2rem; 
                                font-weight:700; color:{color};">{conf_pct}</div>
                    <div style="font-size:0.75rem; color:#64748b;">Confidence</div>
                </div>
            </div>
            <div class="confidence-bar-wrapper" style="margin-top:12px;">
                <div class="confidence-bar" style="width:{confidence*100}%;
                    background: linear-gradient(90deg, {color}, {color}88);"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Description
    st.markdown(f"""
        <div class="pred-body">
            <p style="font-size:0.9rem; color:#94a3b8; line-height:1.6; margin:0 0 1rem;">
                {desc}
            </p>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Top 3 ─────────────────────────────────────────────
    st.markdown("#### 🏆 Top 3 Predictions")
    top1_prob = top3[0][1] if top3 else 1
    for rank, (cls, prob) in enumerate(top3, 1):
        pct = prob * 100
        bar_width = int((prob / max(top1_prob, 1e-6)) * 100)
        rank_emoji = ["🥇", "🥈", "🥉"][rank - 1]
        d_info = disease_info.get(cls, {})
        cls_color = d_info.get("color", "#64748b")
        st.markdown(f"""
        <div class="top3-item">
            <span class="top3-rank">{rank_emoji}</span>
            <span style="font-size:1.1rem;">{d_info.get('emoji','🔬')}</span>
            <span class="top3-name">{cls.replace('_', ' ')}</span>
            <div class="top3-mini-bar">
                <div class="top3-mini-fill" style="width:{bar_width}%;
                    background: linear-gradient(90deg, {cls_color}, {cls_color}88);"></div>
            </div>
            <span class="top3-pct">{pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Precautions ───────────────────────────────────────
    if prec_list:
        st.markdown("#### 🛡️ Suggested Precautions")
        st.markdown("*General guidance only — not medical advice.*")
        for p in prec_list:
            st.markdown(f"""
            <div class="precaution-item">
                <span class="precaution-icon">→</span>
                <span>{p}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Models used ───────────────────────────────────────
    if models_used:
        st.markdown(
            f"<div style='margin-top:10px; font-size:0.78rem; color:#64748b;'>"
            f"🧠 Ensemble models: {', '.join(models_used)}</div>",
            unsafe_allow_html=True
        )

    # Disclaimer inline
    st.markdown("""
    <div style='margin-top:14px; padding:10px 14px; background:rgba(239,68,68,0.07);
                border-left:3px solid #ef4444; border-radius:8px; font-size:0.78rem;
                color:#fca5a5;'>
        ⚠️ <strong>This is not a medical diagnosis.</strong> Always consult a 
        licensed dermatologist for accurate diagnosis and treatment.
    </div>
    """, unsafe_allow_html=True)


def render_history_item(entry: dict, index: int):
    results = entry["results"]
    image   = entry["image"]
    ts      = entry["timestamp"]
    cls     = results["top_class"]
    conf    = results["confidence"]

    import io, base64
    from PIL import Image
    pil = Image.fromarray(image).resize((56, 56))
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=70)
    b64 = base64.b64encode(buf.getvalue()).decode()

    from disease_info import DISEASE_INFO
    info  = DISEASE_INFO.get(cls, {})
    emoji = info.get("emoji", "🔬")
    color = info.get("color", "#00d4aa")

    st.markdown(f"""
    <div class="history-item">
        <img class="history-thumb" src="data:image/jpeg;base64,{b64}" alt="skin"/>
        <div class="history-info">
            <div class="history-disease">{emoji} {cls.replace('_', ' ')}</div>
            <div class="history-meta">🕐 {ts}</div>
        </div>
        <div class="history-conf" style="color:{color};">{conf*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


def render_disclaimer():
    st.markdown("""
    <div class="disclaimer-box">
        <div class="disclaimer-title">⚠️ Medical Disclaimer</div>
        This tool is for <strong>educational and research purposes only</strong>.
        It is NOT a substitute for professional medical advice, diagnosis, or treatment.
        Always consult a qualified dermatologist.
    </div>
    """, unsafe_allow_html=True)


def render_loading_animation(text: str = "Analyzing...") -> str:
    return f"""
    <div class="loading-wrapper">
        <div class="loading-spinner"></div>
        <div class="loading-text">{text}</div>
    </div>
    """
