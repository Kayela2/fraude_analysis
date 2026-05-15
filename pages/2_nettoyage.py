import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees

st.set_page_config(
    page_title="VIGILANCE AI — Nettoyage",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "mode_sombre" not in st.session_state:
    st.session_state.mode_sombre = True

sombre = st.session_state.mode_sombre

if sombre:
    bg       = "#0d0f14"
    bgcard   = "#181c26"
    bordure  = "rgba(255,255,255,0.07)"
    txt1     = "#e8eaf0"
    txt2     = "#8892a4"
    txt3     = "#4a5568"
    bleu     = "#63b3ed"
    bleu_dim = "rgba(99,179,237,0.33)"
    bleu_mid = "rgba(99,179,237,0.53)"
    rouge    = "#fc8181"
    vert     = "#68d391"
    orange   = "#f6ad55"
    sidebar  = "#0a0c10"
    pbg      = "#181c26"
    pfont    = "#8892a4"
    pgrid    = "rgba(255,255,255,0.05)"
else:
    bg       = "#f0f2f8"
    bgcard   = "#ffffff"
    bordure  = "rgba(0,0,0,0.08)"
    txt1     = "#1a202c"
    txt2     = "#4a5568"
    txt3     = "#a0aec0"
    bleu     = "#3182ce"
    bleu_dim = "rgba(49,130,206,0.33)"
    bleu_mid = "rgba(49,130,206,0.53)"
    rouge    = "#e53e3e"
    vert     = "#276749"
    orange   = "#dd6b20"
    sidebar  = "#1a202c"
    pbg      = "#ffffff"
    pfont    = "#4a5568"
    pgrid    = "rgba(0,0,0,0.06)"

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
[data-testid="stSidebarNav"] {{ display: none !important; }}
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
.badge {{
    display: inline-block; padding: 3px 8px; border-radius: 4px;
    font-size: 10px; font-weight: 700;
    font-family: 'Space Mono', monospace !important;
}}
.badge.rouge {{ background: rgba(252,129,129,0.15); color: {rouge}; border: 1px solid rgba(252,129,129,0.3); }}
.badge.vert  {{ background: rgba(104,211,145,0.12); color: {vert};  border: 1px solid rgba(104,211,145,0.25); }}
.badge.orange {{ background: rgba(246,173,85,0.15); color: {orange}; border: 1px solid rgba(246,173,85,0.3); }}
.ligne-colonne {{
    display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr;
    padding: 12px 0; border-bottom: 1px solid {bordure}; align-items: center;
}}
.ligne-colonne:last-child {{ border-bottom: none; }}
.entete-colonne {{
    display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr;
    padding: 8px 0; border-bottom: 1px solid {bordure};
}}
.session-badge {{
    margin: auto 12px 16px; padding: 10px 12px;
    background: rgba(104,211,145,0.08); border: 1px solid rgba(104,211,145,0.2);
    border-radius: 8px; font-size: 11px; color: #68d391 !important;
    font-family: 'Space Mono', monospace !important;
}}
.log-ligne {{
    font-size: 9px; font-family: 'Space Mono', monospace;
    padding: 4px 0; border-bottom: 1px solid {bordure};
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
        <div style='font-size:11px;color:#8892a4;font-family:Space Mono,monospace'>
            Securite Institutionnelle
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                    label="📊  Tableau de Bord")
    st.page_link("pages/1_exploration.py",    label="🗄️  Exploration")
    st.page_link("pages/2_nettoyage.py",      label="🧹  Nettoyage")
    st.page_link("pages/3_analyse.py",         label="📈  Analyse")
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
        <span style='opacity:0.7'>Systeme: v1.0.0</span>
    </div>
    """, unsafe_allow_html=True)

df_brut, df = charger_donnees()

total_manquants = int(df_brut.isnull().sum().sum())
total_cellules  = df_brut.shape[0] * df_brut.shape[1]
score_sante     = round((1 - total_manquants / total_cellules) * 100, 1)
nb_doublons     = int(df_brut.duplicated().sum())
lignes_perdues  = len(df_brut) - len(df)

st.markdown(f"""
<div style='display:flex;align-items:center;margin-bottom:8px;padding-bottom:16px;
            border-bottom:1px solid {bordure}'>
    <div style='width:28px;height:28px;background:{bleu}22;
                border:1px solid {bleu}44;border-radius:6px;
                display:flex;align-items:center;justify-content:center;
                font-size:14px;margin-right:10px'>🧹</div>
    <span style='font-size:16px;font-weight:700;color:{txt1};
                 letter-spacing:1.5px;text-transform:uppercase;
                 font-family:Space Mono,monospace'>
        NETTOYAGE ET QUALITE DES DONNEES
    </span>
</div>
<p style='color:{txt2};font-size:13px;margin-bottom:20px'>
    Inspection des metriques d'integrite et transformations appliquees.
</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Total Enregistrements</div>
        <div class='kpi-valeur'>{len(df_brut):,}</div>
        <span class='badge vert'>Coherence Verifiee</span>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Doublons</div>
        <div class='kpi-valeur'>{nb_doublons}</div>
        <span class='badge vert'>Aucun doublon</span>
    </div>""", unsafe_allow_html=True)

with c3:
    couleur_mq = rouge if total_manquants > 50 else orange
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Valeurs Manquantes</div>
        <div class='kpi-valeur' style='color:{couleur_mq}'>{total_manquants:,}</div>
        <span class='badge orange'>Lignes supprimees : {lignes_perdues}</span>
    </div>""", unsafe_allow_html=True)

with c4:
    couleur_s = vert if score_sante > 90 else orange
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Score de Sante</div>
        <div class='kpi-valeur' style='color:{couleur_s}'>{score_sante}%</div>
        <span class='badge vert'>Indice de Qualite</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_tableau, col_droite = st.columns([2.2, 1], gap="medium")

with col_tableau:
    st.markdown(f"<div class='titre-section'>Analyse des Valeurs Manquantes par Colonne</div>",
                unsafe_allow_html=True)

    manquants   = df_brut.isnull().sum()
    manquants   = manquants[manquants > 0].sort_values(ascending=False)
    pourcentage = (manquants / len(df_brut) * 100).round(2)

    st.markdown(f"""
    <div class='entete-colonne'>
        <span style='font-size:10px;font-weight:700;color:{txt3};letter-spacing:1px;text-transform:uppercase;font-family:Space Mono'>Colonne</span>
        <span style='font-size:10px;font-weight:700;color:{txt3};letter-spacing:1px;text-transform:uppercase;font-family:Space Mono'>Nb Manquants</span>
        <span style='font-size:10px;font-weight:700;color:{txt3};letter-spacing:1px;text-transform:uppercase;font-family:Space Mono'>Pourcentage</span>
        <span style='font-size:10px;font-weight:700;color:{txt3};letter-spacing:1px;text-transform:uppercase;font-family:Space Mono'>Action</span>
    </div>
    """, unsafe_allow_html=True)

    for col_nom, nb in manquants.items():
        pct     = pourcentage[col_nom]
        col_pct = rouge if pct > 3 else orange if pct > 1.5 else txt2
        action  = "IMPUTATION" if df_brut[col_nom].dtype in ["float64", "int64"] else "MODE"
        st.markdown(f"""
        <div class='ligne-colonne'>
            <span style='font-size:12px;font-weight:700;color:{txt1};font-family:Space Mono'>{col_nom}</span>
            <span style='font-size:12px;color:{txt2};font-family:Space Mono'>{nb:,}</span>
            <span style='font-size:11px;font-weight:700;padding:2px 8px;border-radius:4px;
                         background:{col_pct}22;color:{col_pct};border:1px solid {col_pct}44;
                         font-family:Space Mono'>{pct}%</span>
            <span style='font-size:10px;font-weight:700;padding:4px 10px;border-radius:5px;
                         background:rgba(99,179,237,0.12);color:{bleu};
                         border:1px solid rgba(99,179,237,0.2);font-family:Space Mono'>{action}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='titre-section'>Evolution du Score de Qualite</div>",
                unsafe_allow_html=True)

    semaines = ["Sem. 41", "Sem. 42", "Sem. 43", "Sem. 44 (Actuel)"]
    scores   = [88.1, 90.4, 92.0, score_sante]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=semaines, y=scores,
        marker_color=[bleu_dim] * 3 + [bleu],
        marker_line_width=0,
    ))
    fig_trend.add_trace(go.Scatter(
        x=semaines, y=scores,
        mode="lines+markers",
        line=dict(color=bleu, width=2),
        marker=dict(size=7, color=bleu),
    ))
    fig_trend.add_annotation(
        x=semaines[-1], y=score_sante,
        text=f"{score_sante}%",
        showarrow=False, yshift=16,
        font=dict(size=11, color=txt1, family="Space Mono"),
        bgcolor=bgcard
    )
    fig_trend.update_layout(
        height=200, paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9, family="Space Mono")),
        yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                   tickfont=dict(size=9, family="Space Mono"), range=[80, 100]),
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

with col_droite:
    st.markdown(f"<div class='titre-section'>Distribution score_credit</div>",
                unsafe_allow_html=True)

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Histogram(
        x=df_brut["score_credit"].dropna(),
        nbinsx=15,
        marker_color=bleu_mid,
        marker_line_width=0,
    ))
    fig_dist.update_layout(
        height=160, paper_bgcolor=pbg, plot_bgcolor=pbg,
        font=dict(color=pfont, family="Syne"),
        margin=dict(l=5, r=5, t=5, b=5), showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=8, family="Space Mono")),
        yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False, tickfont=dict(size=8, family="Space Mono")),
    )
    st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"<div class='titre-section' style='margin-top:12px'>Outils de Traitement</div>",
                unsafe_allow_html=True)

    for label, icone in [
        ("Imputation Intelligente",   "✨"),
        ("Suppression Doublons",      "🗂"),
        ("Normalisation des Valeurs", "⚖"),
    ]:
        st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:space-between;
                    padding:12px 14px;background:{bgcard};border:1px solid {bordure};
                    border-radius:8px;margin-bottom:8px'>
            <span style='font-size:12px;font-weight:600;color:{txt1}'>{icone} &nbsp;{label}</span>
            <span style='color:{bleu};font-size:14px'>›</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='titre-section'>Journal de Traitement</div>",
                unsafe_allow_html=True)

    journaux = [
        ("14:01:55", "INFO",  vert,   "Scan termine. Nulls identifies."),
        ("14:01:58", "WARN",  orange, "Doublons verifies : aucun."),
        ("14:02:05", "DEBUG", txt3,   "Asymetrie detectee (+1.2)."),
        ("14:02:10", "READY", vert,   "En attente de validation."),
        ("14:02:15", "INFO",  txt3,   "Connexion stable. Latence 14ms."),
    ]
    log_html = "".join(
        f"<div class='log-ligne' style='color:{c}'>{ts} <strong>{n}</strong>: {m}</div>"
        for ts, n, c, m in journaux
    )
    st.markdown(f"""
    <div style='background:{bg};border:1px solid {bordure};border-radius:8px;
                padding:10px;max-height:180px;overflow-y:auto'>{log_html}</div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<div class='titre-section'>Resume du Nettoyage</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class='kpi-carte' style='text-align:center'>
        <div class='kpi-label'>Avant Nettoyage</div>
        <div class='kpi-valeur'>{len(df_brut):,}</div>
        <div style='font-size:11px;color:{txt3}'>lignes originales</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-carte' style='text-align:center;border-color:{rouge}44'>
        <div class='kpi-label'>Lignes Supprimees</div>
        <div class='kpi-valeur' style='color:{rouge}'>-{lignes_perdues}</div>
        <div style='font-size:11px;color:{txt3}'>lignes avec valeurs manquantes</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-carte' style='text-align:center;border-color:{vert}44'>
        <div class='kpi-label'>Apres Nettoyage</div>
        <div class='kpi-valeur' style='color:{vert}'>{len(df):,}</div>
        <div style='font-size:11px;color:{txt3}'>lignes pretes pour l'analyse</div>
    </div>""", unsafe_allow_html=True)
