import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas

st.set_page_config(
    page_title="VIGILANCE AI — Visualisations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "mode_sombre" not in st.session_state:
    st.session_state.mode_sombre = True

sombre = st.session_state.mode_sombre

if sombre:
    bg      = "#0d0f14"
    bgcard  = "#181c26"
    bordure = "rgba(255,255,255,0.07)"
    txt1    = "#e8eaf0"
    txt2    = "#8892a4"
    txt3    = "#4a5568"
    bleu    = "#63b3ed"
    rouge   = "#fc8181"
    vert    = "#68d391"
    orange  = "#f6ad55"
    sidebar = "#0a0c10"
    pbg     = "#181c26"
    pfont   = "#8892a4"
    pgrid   = "rgba(255,255,255,0.05)"
    bleu_alfa  = "rgba(99,179,237,0.47)"
    rouge_alfa = "rgba(252,129,129,0.60)"
else:
    bg      = "#f0f2f8"
    bgcard  = "#ffffff"
    bordure = "rgba(0,0,0,0.08)"
    txt1    = "#1a202c"
    txt2    = "#4a5568"
    txt3    = "#a0aec0"
    bleu    = "#3182ce"
    rouge   = "#e53e3e"
    vert    = "#276749"
    orange  = "#dd6b20"
    sidebar = "#1a202c"
    pbg     = "#ffffff"
    pfont   = "#4a5568"
    pgrid   = "rgba(0,0,0,0.06)"
    bleu_alfa  = "rgba(49,130,206,0.47)"
    rouge_alfa = "rgba(229,62,62,0.60)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'Syne', sans-serif !important; }}
.stApp {{ background: {bg} !important; }}
.block-container {{ padding: 1.5rem 2rem !important; max-width: 100% !important; }}
[data-testid="stSidebar"] {{
    background: {sidebar} !important;
    min-width: 220px !important; max-width: 220px !important;
    border-right: 1px solid {bordure} !important;
}}
[data-testid="stSidebar"] * {{ color: #c8d0e0 !important; }}
h1, h2, h3 {{ color: {txt1} !important; font-family: 'Syne', sans-serif !important; }}
.stButton > button {{
    background: linear-gradient(135deg, {bleu}, #4299e1) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
}}
.kpi-carte {{
    background: {bgcard}; border: 1px solid {bordure};
    border-radius: 12px; padding: 18px 20px;
}}
.kpi-label {{
    font-size: 11px; font-weight: 700; color: {txt3};
    letter-spacing: 1px; text-transform: uppercase;
    font-family: 'Space Mono', monospace !important; margin-bottom: 8px;
}}
.kpi-valeur {{
    font-size: 26px; font-weight: 800; color: {txt1};
    font-family: 'Syne', sans-serif !important; margin-bottom: 4px;
}}
.titre-section {{
    font-size: 12px; font-weight: 700; color: {txt1};
    letter-spacing: 1.2px; text-transform: uppercase;
    font-family: 'Space Mono', monospace !important; margin-bottom: 12px;
}}
.session-badge {{
    margin: auto 12px 16px; padding: 10px 12px;
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.2);
    border-radius: 8px; font-size: 11px;
    color: #68d391 !important;
    font-family: 'Space Mono', monospace !important;
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;
                padding:20px 16px 12px;
                border-bottom:1px solid rgba(255,255,255,0.06);
                margin-bottom:8px'>
        <div style='width:32px;height:32px;
                    background:linear-gradient(135deg,#63b3ed,#4299e1);
                    border-radius:8px;display:flex;align-items:center;
                    justify-content:center;font-size:16px'>🛡️</div>
        <span style='font-family:Syne,sans-serif;font-weight:800;
                     font-size:15px;color:#e8eaf0;letter-spacing:1.5px'>
            VIGILANCE AI
        </span>
    </div>
    <div style='margin:8px 12px 16px;padding:10px 12px;
                background:rgba(255,255,255,0.04);border-radius:8px;
                border:1px solid rgba(255,255,255,0.06)'>
        <div style='font-size:13px;font-weight:700;color:#e8eaf0'>
            Investigateur Principal
        </div>
        <div style='font-size:11px;color:#8892a4;
                    font-family:Space Mono,monospace'>
            Sécurité Institutionnelle
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                    label="📊  Tableau de Bord")
    st.page_link("pages/1_exploration.py",    label="🗄️  Exploration")
    st.page_link("pages/2_nettoyage.py",      label="🧹  Nettoyage")
    st.page_link("pages/3_analyse.py",        label="📈  Analyse")
    st.page_link("pages/4_visualisations.py", label="👁️  Visualisations")
    st.page_link("pages/5_faudes.py",         label="🚨  Profil des Fraudes")

    st.markdown("<br>", unsafe_allow_html=True)
    label_theme = "☀️ Mode Clair" if sombre else "🌙 Mode Sombre"
    if st.button(label_theme, use_container_width=True):
        st.session_state.mode_sombre = not sombre
        st.rerun()

    st.markdown(f"""
    <br>
    <div class='session-badge'>
        🟢 &nbsp;Session Active<br>
        <span style='opacity:0.7'>Système: v1.0.0</span>
    </div>
    """, unsafe_allow_html=True)

df_brut, df = charger_donnees()
stats       = get_stas(df)
df_fraude   = df[df["fraude"] == 1]
df_legitime = df[df["fraude"] == 0]

st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:24px;padding-bottom:16px;
            border-bottom:1px solid {bordure}'>
    <div style='display:flex;align-items:center;gap:10px'>
        <div style='width:28px;height:28px;background:{bleu}22;
                    border:1px solid {bleu}44;border-radius:6px;
                    display:flex;align-items:center;
                    justify-content:center;font-size:14px'>👁️</div>
        <span style='font-size:16px;font-weight:700;color:{txt1};
                     letter-spacing:1.5px;text-transform:uppercase;
                     font-family:Space Mono,monospace'>
            VISUALISATIONS
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown(f"<div class='titre-section'>Distribution des Montants</div>",
                unsafe_allow_html=True)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df_legitime["montant_transaction"],
        name="Légitime",
        marker_color=bleu_alfa,
        nbinsx=40,
    ))
    fig_hist.add_trace(go.Histogram(
        x=df_fraude["montant_transaction"],
        name="Fraude",
        marker_color=rouge_alfa,
        nbinsx=40,
    ))
    fig_hist.update_layout(
        barmode="overlay", height=320,
        paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=40),
        legend=dict(font=dict(size=9, family="Space Mono", color=pfont),
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(title="Montant (FCFA)", showgrid=False,
                   tickfont=dict(size=9, family="Space Mono")),
        yaxis=dict(showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
    )
    fig_hist.update_traces(opacity=0.75)
    st.plotly_chart(fig_hist, use_container_width=True,
                    config={"displayModeBar": False})

with col2:
    st.markdown(f"<div class='titre-section'>Score de Crédit par Statut</div>",
                unsafe_allow_html=True)
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=df_legitime["score_credit"],
        name="Légitime",
        marker_color=bleu_alfa,
        line_color=bleu,
    ))
    fig_box.add_trace(go.Box(
        y=df_fraude["score_credit"],
        name="Fraude",
        marker_color=rouge_alfa,
        line_color=rouge,
    ))
    fig_box.update_layout(
        height=320,
        paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=40),
        legend=dict(font=dict(size=9, family="Space Mono", color=pfont),
                    bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
        xaxis=dict(tickfont=dict(size=9, family="Space Mono")),
    )
    st.plotly_chart(fig_box, use_container_width=True,
                    config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns(2, gap="medium")

with col3:
    st.markdown(f"<div class='titre-section'>Âge vs Montant</div>",
                unsafe_allow_html=True)
    fig_scatter = go.Figure()
    sample = df.sample(min(500, len(df)), random_state=42)
    fig_scatter.add_trace(go.Scatter(
        x=sample[sample["fraude"]==0]["age"],
        y=sample[sample["fraude"]==0]["montant_transaction"],
        mode="markers",
        name="Légitime",
        marker=dict(color=bleu_alfa, size=5),
    ))
    fig_scatter.add_trace(go.Scatter(
        x=sample[sample["fraude"]==1]["age"],
        y=sample[sample["fraude"]==1]["montant_transaction"],
        mode="markers",
        name="Fraude",
        marker=dict(color=rouge, size=6, symbol="x"),
    ))
    fig_scatter.update_layout(
        height=320,
        paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=40),
        legend=dict(font=dict(size=9, family="Space Mono", color=pfont),
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(title="Âge", showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
        yaxis=dict(title="Montant (FCFA)", showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
    )
    st.plotly_chart(fig_scatter, use_container_width=True,
                    config={"displayModeBar": False})

with col4:
    st.markdown(f"<div class='titre-section'>Salaire vs Score de Crédit</div>",
                unsafe_allow_html=True)
    fig_scatter2 = go.Figure()
    fig_scatter2.add_trace(go.Scatter(
        x=sample[sample["fraude"]==0]["salaire"],
        y=sample[sample["fraude"]==0]["score_credit"],
        mode="markers",
        name="Légitime",
        marker=dict(color=bleu_alfa, size=5),
    ))
    fig_scatter2.add_trace(go.Scatter(
        x=sample[sample["fraude"]==1]["salaire"],
        y=sample[sample["fraude"]==1]["score_credit"],
        mode="markers",
        name="Fraude",
        marker=dict(color=rouge, size=6, symbol="x"),
    ))
    fig_scatter2.update_layout(
        height=320,
        paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=40),
        legend=dict(font=dict(size=9, family="Space Mono", color=pfont),
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(title="Salaire (FCFA)", showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
        yaxis=dict(title="Score de Crédit", showgrid=True, gridcolor=pgrid,
                   tickfont=dict(size=9, family="Space Mono")),
    )
    st.plotly_chart(fig_scatter2, use_container_width=True,
                    config={"displayModeBar": False})
