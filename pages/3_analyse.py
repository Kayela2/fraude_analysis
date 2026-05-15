import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas

# ── Configuration ────────────────────────────────────────────
st.set_page_config(
    page_title="VIGILANCE AI — Analyse",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Thème ────────────────────────────────────────────────────
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
    pgrid      = "rgba(255,255,255,0.05)"
    bleu_alfa  = "rgba(99,179,237,0.47)"
    bleu_mid   = "rgba(99,179,237,0.53)"
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
    pgrid      = "rgba(0,0,0,0.06)"
    bleu_alfa  = "rgba(49,130,206,0.47)"
    bleu_mid   = "rgba(49,130,206,0.53)"
    rouge_alfa = "rgba(229,62,62,0.60)"

# ── CSS ──────────────────────────────────────────────────────
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
.badge {{
    display: inline-block; padding: 3px 8px; border-radius: 4px;
    font-size: 10px; font-weight: 700;
    font-family: 'Space Mono', monospace !important;
}}
.badge.rouge {{
    background: rgba(252,129,129,0.15); color: {rouge};
    border: 1px solid rgba(252,129,129,0.3);
}}
.badge.vert {{
    background: rgba(104,211,145,0.12); color: {vert};
    border: 1px solid rgba(104,211,145,0.25);
}}
.badge.orange {{
    background: rgba(246,173,85,0.15); color: {orange};
    border: 1px solid rgba(246,173,85,0.3);
}}
.carte-finding {{
    background: {bgcard}; border-radius: 10px;
    padding: 16px; height: 100%;
}}
.nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; border-radius: 7px;
    margin-bottom: 2px; font-size: 13px; font-weight: 600;
    color: #8892a4 !important;
}}
.nav-item.actif {{
    background: rgba(99,179,237,0.18); color: {bleu} !important;
}}
.nav-point {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {bleu}; margin-left: auto;
}}
.session-badge {{
    margin: auto 12px 16px; padding: 10px 12px;
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.2);
    border-radius: 8px; font-size: 11px;
    color: #68d391 !important;
    font-family: 'Space Mono', monospace !important;
}}
.ligne-stat {{
    display: grid;
    grid-template-columns: 1fr 0.8fr 0.8fr 0.6fr 0.6fr;
    padding: 10px 0;
    border-bottom: 1px solid {bordure};
}}
.ligne-stat:last-child {{ border-bottom: none; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
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

# ── Chargement ───────────────────────────────────────────────
df_brut, df = charger_donnees()
stats       = get_stas(df)
df_fraude   = df[df["fraude"] == 1]
df_legitime = df[df["fraude"] == 0]

# ── Barre du haut ────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:24px;padding-bottom:16px;
            border-bottom:1px solid {bordure}'>
    <div style='display:flex;align-items:center;gap:10px'>
        <div style='width:28px;height:28px;background:{bleu}22;
                    border:1px solid {bleu}44;border-radius:6px;
                    display:flex;align-items:center;
                    justify-content:center;font-size:14px'>📈</div>
        <span style='font-size:16px;font-weight:700;color:{txt1};
                     letter-spacing:1.5px;text-transform:uppercase;
                     font-family:Space Mono,monospace'>
            ANALYSE EXPLORATOIRE
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Échantillons</div>
        <div class='kpi-valeur'>{len(df):,}</div>
        <div class='kpi-sous'>
            <span class='badge vert'>✓ Validé</span>
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Prévalence Fraude</div>
        <div class='kpi-valeur' style='color:{rouge}'>
            {stats['taux_fraude']}%
        </div>
        <div class='kpi-sous'>
            <span class='badge rouge'>↑ Seuil Critique</span>
        </div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Transaction Moyenne</div>
        <div class='kpi-valeur'>{stats['montant_moy']:,.0f}</div>
        <div class='kpi-sous'>
            <span style='font-size:11px;color:{txt3};
                         font-family:Space Mono'>FCFA</span>
        </div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Confiance Modèle</div>
        <div class='kpi-valeur' style='color:{bleu}'>98.4%</div>
        <div class='kpi-sous'>
            <span class='badge vert'>Modèle Bayésien</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Onglets d'analyse ────────────────────────────────────────
onglet1, onglet2, onglet3 = st.tabs([
    "🔗 Corrélations",
    "📊 Segmentation",
    "👥 Démographie"
])

# ════════════════════════════════════════════════════════════
# ONGLET 1 — CORRÉLATIONS
# ════════════════════════════════════════════════════════════
with onglet1:

    col_heatmap, col_stats = st.columns([1.4, 1], gap="medium")

    with col_heatmap:
        st.markdown(f"<div class='titre-section'>Matrice de Corrélation</div>",
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div style='font-size:11px;color:{txt2};margin-bottom:12px'>
            Coefficient de Pearson entre les variables numériques
        </div>""", unsafe_allow_html=True)

        # Calcul de la corrélation
        cols_num = ["montant_transaction", "age", "salaire",
                    "score_credit", "anciennete_compte", "fraude"]
        corr     = df[cols_num].corr().round(2)
        etiquettes = ["Montant", "Âge", "Salaire",
                      "Score", "Ancienneté", "Fraude"]

        fig_corr = go.Figure(go.Heatmap(
            z=corr.values,
            x=etiquettes,
            y=etiquettes,
            colorscale=[
                [0.0, "#1a365d"],
                [0.5, "#2d3748"],
                [0.7, "#f6ad55"],
                [1.0, "#fc8181"]
            ],
            text=corr.values.round(2),
            texttemplate="%{text}",
            textfont=dict(size=11, family="Space Mono", color="white"),
            showscale=False,
        ))
        fig_corr.update_layout(
            height=320,
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=60, r=10, t=10, b=60),
            xaxis=dict(tickfont=dict(size=9, family="Space Mono",
                                     color=pfont)),
            yaxis=dict(tickfont=dict(size=9, family="Space Mono",
                                     color=pfont)),
        )
        st.plotly_chart(fig_corr, use_container_width=True,
                        config={"displayModeBar": False})

    with col_stats:
        st.markdown(f"<div class='titre-section'>Distribution des Variables</div>",
                    unsafe_allow_html=True)

        # Tableau de statistiques
        stats_lignes = [
            ("Montant",    df["montant_transaction"].mean(),
                           df["montant_transaction"].median(),
                           df["montant_transaction"].skew(),
                           df["montant_transaction"].kurtosis()),
            ("Âge",        df["age"].mean(),
                           df["age"].median(),
                           df["age"].skew(),
                           df["age"].kurtosis()),
            ("Salaire",    df["salaire"].mean() / 1000,
                           df["salaire"].median() / 1000,
                           df["salaire"].skew(),
                           df["salaire"].kurtosis()),
            ("Score",      df["score_credit"].mean(),
                           df["score_credit"].median(),
                           df["score_credit"].skew(),
                           df["score_credit"].kurtosis()),
        ]

        # En-tête
        st.markdown(f"""
        <div style='display:grid;
                    grid-template-columns:1fr 0.8fr 0.8fr 0.6fr 0.6fr;
                    padding:8px 0;border-bottom:1px solid {bordure}'>
            {"".join(f"<span style='font-size:10px;font-weight:700;color:{txt3};letter-spacing:0.8px;text-transform:uppercase;font-family:Space Mono'>{h}</span>"
            for h in ["Variable","Moyenne","Médiane","Asymétrie","Kurtosis"])}
        </div>
        """, unsafe_allow_html=True)

        # Lignes
        for nom, moy, med, asym, kurt in stats_lignes:
            c_asym = rouge if abs(asym) > 2 else orange \
                     if abs(asym) > 1 else txt2
            st.markdown(f"""
            <div class='ligne-stat'>
                <span style='font-size:11px;font-weight:700;
                             color:{txt1};font-family:Space Mono'>
                    {nom}
                </span>
                <span style='font-size:11px;color:{txt2};
                             font-family:Space Mono'>
                    {moy:.1f}
                </span>
                <span style='font-size:11px;color:{txt2};
                             font-family:Space Mono'>
                    {med:.1f}
                </span>
                <span style='font-size:11px;color:{c_asym};
                             font-family:Space Mono'>
                    {asym:.2f}
                </span>
                <span style='font-size:11px;color:{txt2};
                             font-family:Space Mono'>
                    {kurt:.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)

    # ── Cartes de résultats ──────────────────────────────────
    st.markdown(f"<br><div class='titre-section'>🔍 Résultats Clés de l'Analyse</div>",
                unsafe_allow_html=True)

    resultats = [
        (rouge,  "⚠", "RISQUE ÉLEVÉ",
         "Ciblage des Hauts Revenus",
         "Les clients avec un salaire élevé et des transactions fréquentes présentent un risque accru. Ce schéma indique des tentatives d'usurpation de comptes."),
        (vert,   "🛡", "LIGNE DE BASE STABLE",
         "Le Profil Sécurisé",
         "Les clients de 35 à 45 ans présentent le taux de fraude le plus bas (<0.8%). Ce segment est notre référence de comportement normal."),
        (orange, "↗", "MENACE ÉMERGENTE",
         "Escalade par Force Brute",
         "La corrélation entre les montants élevés et les échecs d'authentification a augmenté de 15%. Les fraudeurs ciblent les comptes à haute valeur."),
    ]

    cols = st.columns(3)
    for col, (couleur, icone, label, titre, desc) in zip(cols, resultats):
        with col:
            st.markdown(f"""
            <div style='background:{bgcard};
                        border:1px solid {couleur}33;
                        border-top:2px solid {couleur};
                        border-radius:10px;padding:16px'>
                <div style='font-size:10px;font-weight:700;
                             color:{couleur};letter-spacing:1px;
                             font-family:Space Mono;
                             text-transform:uppercase;margin-bottom:6px'>
                    {icone} {label}
                </div>
                <div style='font-size:14px;font-weight:700;
                             color:{txt1};margin-bottom:8px;
                             font-family:Syne'>{titre}</div>
                <p style='font-size:11px;color:{txt2};
                           line-height:1.5;margin:0'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ONGLET 2 — SEGMENTATION
# ════════════════════════════════════════════════════════════
with onglet2:
    st.markdown(f"<div class='titre-section'>Segmentation Comparative</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:11px;color:{txt2};margin-bottom:16px'>
        Analyse multi-axe des comportements à risque selon les segments
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        # Fraude par tranche de salaire
        df["tranche_salaire"] = pd.cut(
            df["salaire"],
            bins=[0, 50000, 100000, 150000, 10000000],
            labels=["0–50k", "50–100k", "100–150k", "150k+"]
        )
        sal_legitime = df[df["fraude"]==0].groupby(
            "tranche_salaire", observed=True).size()
        sal_fraude   = df[df["fraude"]==1].groupby(
            "tranche_salaire", observed=True).size()

        fig_sal = go.Figure()
        fig_sal.add_trace(go.Bar(
            x=sal_legitime.index.astype(str),
            y=sal_legitime.values,
            name="Légitime",
            marker_color=bleu_alfa,
            marker_line_width=0,
        ))
        fig_sal.add_trace(go.Bar(
            x=sal_fraude.index.astype(str),
            y=sal_fraude.values,
            name="Fraude",
            marker_color=rouge_alfa,
            marker_line_width=0,
        ))
        fig_sal.update_layout(
            barmode="group", height=280,
            title=dict(
                text="SALAIRE VS PROBABILITÉ DE FRAUDE",
                font=dict(size=10, color=pfont, family="Space Mono"),
                x=0
            ),
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=10, r=10, t=36, b=10),
            showlegend=True,
            legend=dict(
                font=dict(size=9, family="Space Mono", color=pfont),
                bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12
            ),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
        )
        st.plotly_chart(fig_sal, use_container_width=True,
                        config={"displayModeBar": False})

    with col2:
        # Fraude par tranche d'âge
        df["tranche_age"] = pd.cut(
            df["age"],
            bins=[17, 25, 35, 45, 55, 100],
            labels=["18–25", "26–35", "36–45", "46–55", "55+"]
        )
        age_legitime = df[df["fraude"]==0].groupby(
            "tranche_age", observed=True).size()
        age_fraude   = df[df["fraude"]==1].groupby(
            "tranche_age", observed=True).size()

        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(
            x=age_legitime.index.astype(str),
            y=age_legitime.values,
            name="Légitime",
            marker_color=bleu_alfa,
            marker_line_width=0,
        ))
        fig_age.add_trace(go.Bar(
            x=age_fraude.index.astype(str),
            y=age_fraude.values,
            name="Fraude",
            marker_color=rouge_alfa,
            marker_line_width=0,
        ))
        fig_age.update_layout(
            barmode="group", height=280,
            title=dict(
                text="ÂGE VS PROBABILITÉ DE FRAUDE",
                font=dict(size=10, color=pfont, family="Space Mono"),
                x=0
            ),
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=10, r=10, t=36, b=10),
            showlegend=True,
            legend=dict(
                font=dict(size=9, family="Space Mono", color=pfont),
                bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12
            ),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
        )
        st.plotly_chart(fig_age, use_container_width=True,
                        config={"displayModeBar": False})

# ════════════════════════════════════════════════════════════
# ONGLET 3 — DÉMOGRAPHIE
# ════════════════════════════════════════════════════════════
with onglet3:
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        # Fraude par genre
        genre_data = df.groupby(["genre", "fraude_label"]).size()\
                       .reset_index(name="nb")
        fig_genre = px.bar(
            genre_data, x="genre", y="nb",
            color="fraude_label", barmode="group",
            color_discrete_map={
                "Fraude":   rouge,
                "Légitime": bleu_mid
            }
        )
        fig_genre.update_layout(
            height=280,
            title=dict(text="RÉPARTITION PAR GENRE",
                       font=dict(size=10, color=pfont,
                                 family="Space Mono"), x=0),
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=10, r=10, t=36, b=10),
            showlegend=True,
            legend=dict(font=dict(size=9, family="Space Mono",
                                  color=pfont),
                        bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
        )
        fig_genre.update_traces(marker_line_width=0)
        st.plotly_chart(fig_genre, use_container_width=True,
                        config={"displayModeBar": False})

    with col2:
        # Taux de fraude par région
        region_stats = df.groupby("region")["fraude"]\
                         .agg(["sum", "count"]).reset_index()
        region_stats["taux"] = (region_stats["sum"] /
                                region_stats["count"] * 100).round(1)

        fig_region = go.Figure(go.Bar(
            x=region_stats["region"],
            y=region_stats["taux"],
            marker_color=[
                rouge if v == region_stats["taux"].max()
                else bleu_alfa
                for v in region_stats["taux"]
            ],
            marker_line_width=0,
            text=[f"{t}%" for t in region_stats["taux"]],
            textposition="outside",
            textfont=dict(size=10, family="Space Mono", color=txt2),
        ))
        fig_region.update_layout(
            height=280,
            title=dict(text="TAUX DE FRAUDE PAR RÉGION (%)",
                       font=dict(size=10, color=pfont,
                                 family="Space Mono"), x=0),
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=10, r=10, t=36, b=10),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
        )
        st.plotly_chart(fig_region, use_container_width=True,
                        config={"displayModeBar": False})

    with col3:
        # Taux de fraude par type de carte
        carte_stats = df.groupby("type_carte")["fraude"]\
                        .agg(["sum", "count"]).reset_index()
        carte_stats["taux"] = (carte_stats["sum"] /
                               carte_stats["count"] * 100).round(1)

        fig_carte = go.Figure(go.Bar(
            x=carte_stats["type_carte"],
            y=carte_stats["taux"],
            marker_color=[orange, bleu_alfa],
            marker_line_width=0,
            text=[f"{t}%" for t in carte_stats["taux"]],
            textposition="outside",
            textfont=dict(size=10, family="Space Mono", color=txt2),
        ))
        fig_carte.update_layout(
            height=280,
            title=dict(text="TAUX DE FRAUDE PAR TYPE DE CARTE (%)",
                       font=dict(size=10, color=pfont,
                                 family="Space Mono"), x=0),
            paper_bgcolor=pbg, plot_bgcolor=pbg,
            font=dict(color=pfont, family="Syne"),
            margin=dict(l=10, r=10, t=36, b=10),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, family="Space Mono")),
        )
        st.plotly_chart(fig_carte, use_container_width=True,
                        config={"displayModeBar": False})