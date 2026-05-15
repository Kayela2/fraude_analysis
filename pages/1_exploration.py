import streamlit as st
import pandas as pd
import sys  
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.data import charger_donnees, get_stas

st.set_page_config(page_title="Exploration des données", layout="wide", initial_sidebar_state="collapsed")

if "mode_sombre" not in st.session_state:
    st.session_state["mode_sombre"] = True

sombre = st.session_state.mode_sombre
 
if sombre:
    bg = "#0d0f14"
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

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
html, body, [class*="css"]  {{
    font-family: 'Syne', sans-serif; !important;}} .stApp {{ background: {bg} !important; }} .block-container {{
    padding: 1.5rem 2rem !important; max-width: 100% !important; }} .block-container {{ padding:  1.4rem 2rem !important;}} [data-testid="stSidebar"] {{
    background: {sidebar} !important;
    min-width: 220px !important;
    max-width: 220px !important;
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
    font-family: 'Syne', sans-serif !important;
}}
.kpi-sous {{
    font-size: 11px; color: {txt3};
    font-family: 'Space Mono', monospace !important;
}}
.titre-section {{
    font-size: 12px; font-weight: 700; color: {txt1};
    letter-spacing: 1.2px; text-transform: uppercase;
    font-family: 'Space Mono', monospace !important;
    margin-bottom: 12px;
}}
.badge-type {{
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 10px; font-weight: 700;
    font-family: 'Space Mono', monospace !important;
    background: rgba(99,179,237,0.12); color: {bleu};
    border: 1px solid rgba(99,179,237,0.2);
}}
.ligne-schema {{
    display: flex; align-items: center;
    padding: 10px 0; border-bottom: 1px solid {bordure};
}}
.ligne-schema:last-child {{ border-bottom: none; }}
.session-badge {{
    margin: auto 12px 16px; padding: 10px 12px;
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.2);
    border-radius: 8px; font-size: 11px;
    color: #68d391 !important;
    font-family: 'Space Mono', monospace !important;
}}
.nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; border-radius: 7px;
    margin-bottom: 2px; font-size: 13px; font-weight: 600;
    color: #8892a4 !important;
}}

.nav-item.actif {{
    background: rgba(99,179,237,0.18);
    color: {bleu} !important;
}}
.nav-point {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {bleu}; margin-left: auto;
}}
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
        <span style='opacity:0.7'>Système: v1.0.0</span>
    </div>
    """, unsafe_allow_html=True)

# ── Chargement ───────────────────────────────────────────────
df_brut, df = charger_donnees()
stats       = get_stas(df)

# ── Barre du haut ────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:24px;padding-bottom:16px;
            border-bottom:1px solid {bordure}'>
    <div style='display:flex;align-items:center;gap:10px'>
        <div style='width:28px;height:28px;background:{bleu}22;
                    border:1px solid {bleu}44;border-radius:6px;
                    display:flex;align-items:center;
                    justify-content:center;font-size:14px'>🗄️</div>
        <span style='font-size:16px;font-weight:700;color:{txt1};
                     letter-spacing:1.5px;text-transform:uppercase;
                     font-family:Space Mono,monospace'>
            EXPLORATION DES DONNÉES
        </span>
    </div>
    <span style='font-size:11px;color:{txt3};font-family:Space Mono'>
        Données › fraude_bancaire_synthetique_final.csv
    </span>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Total Enregistrements</div>
        <div class='kpi-valeur'>{len(df_brut):,}</div>
        <div class='kpi-sous'>✓ Données originales</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Score Crédit Moyen</div>
        <div class='kpi-valeur'>{stats['score_moy']:.1f}</div>
        <div class='kpi-sous'>Sur 100 points</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Salaire Moyen</div>
        <div class='kpi-valeur'>{stats['salaire_moy']:,.0f}</div>
        <div class='kpi-sous'>En francs CFA</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-carte'>
        <div class='kpi-label'>Risque Critique</div>
        <div class='kpi-valeur' style='color:{rouge}'>{stats['taux_fraude']}%</div>
        <div class='kpi-sous'>Taux de fraude détecté</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filtres + Tableau ────────────────────────────────────────
col_filtres, col_tableau = st.columns([1, 2.8], gap="medium")

with col_filtres:
    st.markdown(f"<div class='titre-section'>⚙ Filtres</div>",
                unsafe_allow_html=True)

    # Filtre par âge
    age_min = int(df["age"].min())
    age_max = int(df["age"].max())
    age_range = st.slider(
        "Tranche d'âge",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max)
    )

    # Filtre par score de crédit
    score_min = int(df["score_credit"].min())
    score_max = int(df["score_credit"].max())
    score_range = st.slider(
        "Score de Crédit minimum",
        min_value=score_min,
        max_value=score_max,
        value=score_min
    )

    # Filtre par région
    regions = ["Toutes"] + sorted(df["region"].unique().tolist())
    region_choisie = st.selectbox("Région", regions)

    # Filtre par type de transaction
    st.markdown(f"<div class='titre-section' style='margin-top:12px'>Statut</div>",
                unsafe_allow_html=True)
    afficher_legitime = st.checkbox("Transactions Légitimes", value=True)
    afficher_fraude   = st.checkbox("Cas de Fraude", value=True)

    st.button("Mettre à Jour", use_container_width=True)

    # Schéma des colonnes
    st.markdown(f"<br><div class='titre-section'>⬛ Schéma des Colonnes</div>",
                unsafe_allow_html=True)

    schema = [
        ("age",                 "int"),
        ("salaire",             "float"),
        ("score_credit",        "float"),
        ("montant_transaction", "float"),
        ("anciennete_compte",   "int"),
        ("type_carte",          "str"),
        ("region",              "str"),
        ("genre",               "str"),
        ("fraude",              "int"),
    ]
    for col_nom, col_type in schema:
        st.markdown(f"""
        <div class='ligne-schema'>
            <span style='font-size:12px;font-weight:700;
                         color:{txt1};font-family:Space Mono;
                         flex:1'>{col_nom}</span>
            <span class='badge-type'>{col_type}</span>
        </div>
        """, unsafe_allow_html=True)

with col_tableau:
    # ── Application des filtres ──────────────────────────────
    masque = (
        (df["age"]          >= age_range[0]) &
        (df["age"]          <= age_range[1]) &
        (df["score_credit"] >= score_range)
    )
    if region_choisie != "Toutes":
        masque &= df["region"] == region_choisie
    if not afficher_legitime:
        masque &= df["fraude"] == 1
    if not afficher_fraude:
        masque &= df["fraude"] == 0

    df_filtre = df[masque].copy()

    st.markdown(f"""
    <div class='titre-section'>
        Aperçu des Données &nbsp;
        <span style='font-size:10px;color:{txt3};
                     font-family:Space Mono;font-weight:400'>
            {len(df_filtre):,} enregistrements trouvés
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Préparation de l'affichage
    df_affiche = df_filtre[[
        "age", "salaire", "score_credit",
        "montant_transaction", "anciennete_compte",
        "type_carte", "region", "genre", "fraude"
    ]].head(20).copy()

    # On renomme les colonnes en français
    df_affiche.columns = [
        "ÂGE", "SALAIRE", "SCORE",
        "MONTANT", "ANCIENNETÉ",
        "CARTE", "RÉGION", "GENRE", "FRAUDE"
    ]

    # On formate les colonnes numériques
    df_affiche["ÂGE"]      = df_affiche["ÂGE"].round(0).astype(int)
    df_affiche["SALAIRE"]  = df_affiche["SALAIRE"].apply(
                                lambda x: f"{x:,.0f} FCFA")
    df_affiche["MONTANT"]  = df_affiche["MONTANT"].apply(
                                lambda x: f"{x:,.0f} FCFA")
    df_affiche["SCORE"]    = df_affiche["SCORE"].round(1)
    df_affiche["FRAUDE"]   = df_affiche["FRAUDE"].map(
                                {0: "✅ Légitime", 1: "🚨 Fraude"})

    st.dataframe(df_affiche, use_container_width=True,
                 height=450, hide_index=True)

    # Pagination indicative
    total_pages = max(1, len(df_filtre) // 20)
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;
                align-items:center;margin-top:8px'>
        <span style='font-size:11px;color:{txt3};font-family:Space Mono'>
            Page 1 sur {total_pages} &nbsp;|&nbsp; 20 lignes par page
        </span>
        <div style='display:flex;gap:8px'>
            <span style='font-size:11px;color:{txt2};
                         font-family:Space Mono'>‹‹ Précédent</span>
            <span style='font-size:11px;color:{bleu};
                         font-family:Space Mono'>Suivant ››</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
