# -*- coding: utf-8 -*-
"""
💳 DASHBOARD D'AIDE À LA DÉCISION DE CRÉDIT — PROJET 8
-----------------------------------------------------------
Ce dashboard permet aux chargés de relation client de :
1. Visualiser le score de probabilité et la décision finale.
2. Comprendre les raisons du score (Interprétabilité).
3. Comparer un client à la population globale ou similaire.
4. Respecter les normes d'accessibilité (WCAG).
5. Simuler des changements de profil.
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt

# ============================================================
# ⚙️ CONFIGURATION & CONSTANTES
# ============================================================

# URL de l'API (à adapter lors du déploiement Cloud)
API_URL = "http://127.0.0.1:8000/predict"
THRESHOLD = 0.29  # Seuil de probabilité défini lors de l'entraînement

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Prêt à dépenser — Aide au scoring",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ♿ GESTION DE L'ACCESSIBILITÉ (WCAG)
# ============================================================

st.sidebar.header("♿ Accessibilité & Affichage")
wcag_mode = st.sidebar.checkbox("Mode contraste élevé", value=False)
show_text_desc = st.sidebar.checkbox("Afficher descriptions textuelles", value=True)

# Définition de la palette de couleurs accessible
# On utilise des couleurs contrastées et on évite le rouge/vert seul pour les daltoniens
if wcag_mode:
    COLOR_SAFE = "#005AB5"   # Bleu foncé (Contrasté)
    COLOR_RISK = "#DC3220"   # Rouge vif (Contrasté)
    COLOR_NEUTRAL = "#000000"
else:
    COLOR_SAFE = "#2E7D32"   # Vert standard
    COLOR_RISK = "#D32F2F"   # Rouge standard
    COLOR_NEUTRAL = "#1976D2"

# ============================================================
# 💾 GÉNÉRATION DE DONNÉES DE COMPARAISON (SYNTHÉTIQUES)
# ============================================================

@st.cache_data
def get_comparison_data():
    """Génère un dataset fictif pour représenter la population de référence."""
    np.random.seed(42)
    size = 1000
    data = pd.DataFrame({
        'AMT_INCOME_TOTAL': np.random.lognormal(11, 0.5, size),
        'AMT_CREDIT': np.random.uniform(5000, 50000, size),
        'AGE': np.random.randint(20, 70, size),
        'GENDER': np.random.choice(['F', 'M'], size),
        'TARGET': np.random.choice([0, 1], size, p=[0.9, 0.1])
    })
    return data

population_df = get_comparison_data()

# ============================================================
# 🧪 DONNÉES CLIENTS (MOCKUP POUR DÉMO)
# ============================================================

# En production, ces données seraient récupérées via une base de données ou un CSV
clients_dict = {

    # =====================================================
    # 🟢 FAIBLE RISQUE
    # =====================================================

    "Client_1 — Profil très faible risque": {
        "AMT_ANNUITY": 280,
        "AMT_CREDIT": 7000,
        "AMT_GOODS_PRICE": 7000,
        "AMT_INCOME_TOTAL": 2600 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 0,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 0,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -38 * 365,
        "DAYS_EMPLOYED": -12 * 365,
        "DAYS_ID_PUBLISH": -3000,
        "DAYS_LAST_PHONE_CHANGE": -800,
        "DAYS_REGISTRATION": -7000,

        "EXT_SOURCE_1": 0.80,
        "EXT_SOURCE_2": 0.82,
        "EXT_SOURCE_3": 0.78,

        "HOUR_APPR_PROCESS_START": 9,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 8,
        "REGION_POPULATION_RELATIVE": 0.012,
        "TOTALAREA_MODE": 0.09
    },

    "Client_2 — Profil faible risque": {
        "AMT_ANNUITY": 320,
        "AMT_CREDIT": 8000,
        "AMT_GOODS_PRICE": 8000,
        "AMT_INCOME_TOTAL": 2200 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 0,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -32 * 365,
        "DAYS_EMPLOYED": -6 * 365,
        "DAYS_ID_PUBLISH": -2000,
        "DAYS_LAST_PHONE_CHANGE": -400,
        "DAYS_REGISTRATION": -4000,

        "EXT_SOURCE_1": 0.65,
        "EXT_SOURCE_2": 0.72,
        "EXT_SOURCE_3": 0.70,

        "HOUR_APPR_PROCESS_START": 10,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 5,
        "REGION_POPULATION_RELATIVE": 0.018,
        "TOTALAREA_MODE": 0.10
    },

    "Client_3 — Profil faible / intermédiaire": {
        "AMT_ANNUITY": 420,
        "AMT_CREDIT": 10000,
        "AMT_GOODS_PRICE": 10000,
        "AMT_INCOME_TOTAL": 2100 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 1,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -41 * 365,
        "DAYS_EMPLOYED": -9 * 365,
        "DAYS_ID_PUBLISH": -3200,
        "DAYS_LAST_PHONE_CHANGE": -700,
        "DAYS_REGISTRATION": -5500,

        "EXT_SOURCE_1": 0.58,
        "EXT_SOURCE_2": 0.60,
        "EXT_SOURCE_3": 0.55,

        "HOUR_APPR_PROCESS_START": 11,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 12,
        "REGION_POPULATION_RELATIVE": 0.020,
        "TOTALAREA_MODE": 0.14
    },

    # =====================================================
    # 🟡 INTERMÉDIAIRE
    # =====================================================

    "Client_4 — Profil intermédiaire": {
        "AMT_ANNUITY": 550,
        "AMT_CREDIT": 12000,
        "AMT_GOODS_PRICE": 12000,
        "AMT_INCOME_TOTAL": 1800 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 1,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 2,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -45 * 365,
        "DAYS_EMPLOYED": -15 * 365,
        "DAYS_ID_PUBLISH": -3500,
        "DAYS_LAST_PHONE_CHANGE": -900,
        "DAYS_REGISTRATION": -6000,

        "EXT_SOURCE_1": 0.45,
        "EXT_SOURCE_2": 0.50,
        "EXT_SOURCE_3": 0.48,

        "HOUR_APPR_PROCESS_START": 14,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 10,
        "REGION_POPULATION_RELATIVE": 0.025,
        "TOTALAREA_MODE": 0.18
    },

    "Client_5 — Profil intermédiaire instable": {
        "AMT_ANNUITY": 620,
        "AMT_CREDIT": 14000,
        "AMT_GOODS_PRICE": 14000,
        "AMT_INCOME_TOTAL": 1700 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 2,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 3,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -35 * 365,
        "DAYS_EMPLOYED": -4 * 365,
        "DAYS_ID_PUBLISH": -1800,
        "DAYS_LAST_PHONE_CHANGE": -300,
        "DAYS_REGISTRATION": -3000,

        "EXT_SOURCE_1": 0.40,
        "EXT_SOURCE_2": 0.42,
        "EXT_SOURCE_3": 0.39,

        "HOUR_APPR_PROCESS_START": 15,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 3,
        "REGION_POPULATION_RELATIVE": 0.030,
        "TOTALAREA_MODE": 0.22
    },

    "Client_6 — Profil intermédiaire limite": {
        "AMT_ANNUITY": 700,
        "AMT_CREDIT": 16000,
        "AMT_GOODS_PRICE": 16000,
        "AMT_INCOME_TOTAL": 1600 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 2,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 4,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -30 * 365,
        "DAYS_EMPLOYED": -3 * 365,
        "DAYS_ID_PUBLISH": -1200,
        "DAYS_LAST_PHONE_CHANGE": -200,
        "DAYS_REGISTRATION": -2500,

        "EXT_SOURCE_1": 0.32,
        "EXT_SOURCE_2": 0.35,
        "EXT_SOURCE_3": 0.33,

        "HOUR_APPR_PROCESS_START": 16,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 2,
        "REGION_POPULATION_RELATIVE": 0.034,
        "TOTALAREA_MODE": 0.27
    },

    # =====================================================
    # 🔴 RISQUÉ
    # =====================================================

    "Client_7 — Profil risqué": {
        "AMT_ANNUITY": 900,
        "AMT_CREDIT": 20000,
        "AMT_GOODS_PRICE": 20000,
        "AMT_INCOME_TOTAL": 1500 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 3,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 6,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -28 * 365,
        "DAYS_EMPLOYED": -2 * 365,
        "DAYS_ID_PUBLISH": -800,
        "DAYS_LAST_PHONE_CHANGE": -120,
        "DAYS_REGISTRATION": -1500,

        "EXT_SOURCE_1": 0.18,
        "EXT_SOURCE_2": 0.22,
        "EXT_SOURCE_3": 0.20,

        "HOUR_APPR_PROCESS_START": 16,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 1,
        "REGION_POPULATION_RELATIVE": 0.040,
        "TOTALAREA_MODE": 0.35
    },

    "Client_8 — Profil très risqué": {
        "AMT_ANNUITY": 1050,
        "AMT_CREDIT": 24000,
        "AMT_GOODS_PRICE": 24000,
        "AMT_INCOME_TOTAL": 1400 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 4,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 7,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -26 * 365,
        "DAYS_EMPLOYED": -1 * 365,
        "DAYS_ID_PUBLISH": -500,
        "DAYS_LAST_PHONE_CHANGE": -90,
        "DAYS_REGISTRATION": -1000,

        "EXT_SOURCE_1": 0.12,
        "EXT_SOURCE_2": 0.15,
        "EXT_SOURCE_3": 0.14,

        "HOUR_APPR_PROCESS_START": 18,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 0,
        "REGION_POPULATION_RELATIVE": 0.050,
        "TOTALAREA_MODE": 0.42
    },

    "Client_9 — Profil critique": {
        "AMT_ANNUITY": 1200,
        "AMT_CREDIT": 28000,
        "AMT_GOODS_PRICE": 28000,
        "AMT_INCOME_TOTAL": 1300 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 5,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 9,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -24 * 365,
        "DAYS_EMPLOYED": -0.5 * 365,
        "DAYS_ID_PUBLISH": -300,
        "DAYS_LAST_PHONE_CHANGE": -60,
        "DAYS_REGISTRATION": -700,

        "EXT_SOURCE_1": 0.08,
        "EXT_SOURCE_2": 0.10,
        "EXT_SOURCE_3": 0.09,

        "HOUR_APPR_PROCESS_START": 19,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 0,
        "REGION_POPULATION_RELATIVE": 0.060,
        "TOTALAREA_MODE": 0.48
    },

    "Client_10 — Profil surendettement": {
        "AMT_ANNUITY": 1350,
        "AMT_CREDIT": 32000,
        "AMT_GOODS_PRICE": 32000,
        "AMT_INCOME_TOTAL": 1200 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 6,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 12,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -23 * 365,
        "DAYS_EMPLOYED": -0.3 * 365,
        "DAYS_ID_PUBLISH": -200,
        "DAYS_LAST_PHONE_CHANGE": -45,
        "DAYS_REGISTRATION": -500,

        "EXT_SOURCE_1": 0.05,
        "EXT_SOURCE_2": 0.07,
        "EXT_SOURCE_3": 0.06,

        "HOUR_APPR_PROCESS_START": 20,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 0,
        "REGION_POPULATION_RELATIVE": 0.070,
        "TOTALAREA_MODE": 0.55
    },

    "Client_11 — Profil extrême": {
        "AMT_ANNUITY": 1500,
        "AMT_CREDIT": 36000,
        "AMT_GOODS_PRICE": 36000,
        "AMT_INCOME_TOTAL": 1100 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 7,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 15,

        "CODE_GENDER_F": 1,

        "DAYS_BIRTH": -22 * 365,
        "DAYS_EMPLOYED": -0.2 * 365,
        "DAYS_ID_PUBLISH": -150,
        "DAYS_LAST_PHONE_CHANGE": -30,
        "DAYS_REGISTRATION": -300,

        "EXT_SOURCE_1": 0.03,
        "EXT_SOURCE_2": 0.04,
        "EXT_SOURCE_3": 0.03,

        "HOUR_APPR_PROCESS_START": 21,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 0,
        "REGION_POPULATION_RELATIVE": 0.080,
        "TOTALAREA_MODE": 0.65
    },

    "Client_12 — Profil défaut quasi certain": {
        "AMT_ANNUITY": 1700,
        "AMT_CREDIT": 40000,
        "AMT_GOODS_PRICE": 40000,
        "AMT_INCOME_TOTAL": 1000 * 12,

        "AMT_REQ_CREDIT_BUREAU_QRT": 8,
        "AMT_REQ_CREDIT_BUREAU_YEAR": 18,

        "CODE_GENDER_F": 0,

        "DAYS_BIRTH": -21 * 365,
        "DAYS_EMPLOYED": -0.1 * 365,
        "DAYS_ID_PUBLISH": -100,
        "DAYS_LAST_PHONE_CHANGE": -20,
        "DAYS_REGISTRATION": -200,

        "EXT_SOURCE_1": 0.01,
        "EXT_SOURCE_2": 0.02,
        "EXT_SOURCE_3": 0.01,

        "HOUR_APPR_PROCESS_START": 22,
        "NAME_CONTRACT_TYPE": 1,
        "OWN_CAR_AGE": 0,
        "REGION_POPULATION_RELATIVE": 0.090,
        "TOTALAREA_MODE": 0.75
    }
}


# ============================================================
# 🏠 INTERFACE PRINCIPALE
# ============================================================

st.title("💳 Aide à la Décision Crédit")
st.markdown("---")

# 1. Sélection du client
selected_id = st.selectbox("👤 Sélectionnez un dossier client :", list(clients_dict.keys()))
client_data = clients_dict[selected_id]

# 2. Synthèse des informations descriptives (Besoin 2)
with st.expander("📄 Informations descriptives du client", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenu Annuel", f"{client_data['AMT_INCOME_TOTAL']:,} €")
    c2.metric("Montant Crédit", f"{client_data['AMT_CREDIT']:,} €")
    c3.metric("Âge", f"{abs(client_data['DAYS_BIRTH']) // 365} ans")
    c4.metric("Ancienneté Emploi", f"{abs(client_data['DAYS_EMPLOYED']) // 365} ans")

# 3. Appel API et Affichage du Score (Besoin 1)
st.subheader("🎯 Score et Décision")

if st.button("🚀 Calculer le score de fiabilité"):
    try:
        response = requests.post(API_URL, json=client_data, timeout=5)
        if response.status_code == 200:
            res = response.json()
            proba = res['probability']
            
            # Affichage visuel du score
            col_score, col_txt = st.columns([1, 2])
            
                    # Correction de la ligne Markdown et ajout d'une gestion d'erreur robuste
            with col_score:
                st.write("**Probabilité de défaut :**")
                color_gauge = COLOR_RISK if proba > THRESHOLD else COLOR_SAFE
                # Utilisation du bon argument : unsafe_allow_html
                st.markdown(f"<h1 style='color: {color_gauge};'>{proba*100:.1f}%</h1>", unsafe_allow_html=True)
            
            with col_txt:
                if proba > THRESHOLD:
                    st.error(f"DÉCISION : CRÉDIT REFUSÉ (Seuil : {THRESHOLD*100}%)")
                    st.write("Le risque estimé dépasse les limites de tolérance de la banque.")
                else:
                    st.success(f"DÉCISION : CRÉDIT ACCORDÉ (Seuil : {THRESHOLD*100}%)")
                    st.write("Le profil client présente des garanties suffisantes.")
            
            # Jauge de positionnement
            st.progress(min(proba / (THRESHOLD * 2), 1.0))
            st.caption(f"Position du client par rapport au seuil de refus ({THRESHOLD*100}%).")
            
            # Interprétabilité simple (Exemple de logique métier)
            st.info("💡 **Interprétation :** Les sources externes (EXT_SOURCE) et le ratio revenu/crédit sont les facteurs prépondérants ici.")
            
        else:
            st.error("Erreur lors de l'appel à l'API. Vérifiez que le serveur FastAPI est lancé.")
    except Exception as e:
        st.error(f"Connexion impossible à l'API : {e}")

st.markdown("---")

# 4. Comparaison à la population (Besoin 3)
st.subheader("📊 Comparaison avec les autres profils")

comp_var = st.selectbox("Variable de comparaison :", ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AGE"])
filter_group = st.radio("Comparer à :", ["Toute la population", "Même tranche d'âge", "Même Genre"], horizontal=True)

# Application des filtres
plot_df = population_df.copy()
client_val = abs(client_data['DAYS_BIRTH']) // 365 if comp_var == "AGE" else client_data[comp_var]

if filter_group == "Même tranche d'âge":
    age_c = abs(client_data['DAYS_BIRTH']) // 365
    plot_df = plot_df[plot_df['AGE'].between(age_c-5, age_c+5)]
elif filter_group == "Même Genre":
    gender = 'F' if client_data['CODE_GENDER_F'] == 1 else 'M'
    plot_df = plot_df[plot_df['GENDER'] == gender]

# Graphique Altair (Accessible)
chart = alt.Chart(plot_df).mark_bar(color=COLOR_NEUTRAL, opacity=0.6).encode(
    alt.X(f"{comp_var}:Q", bin=alt.Bin(maxbins=30), title=f"{comp_var}"),
    alt.Y('count()', title="Nombre de clients")
).properties(height=300)

# Ligne pour situer le client
line = alt.Chart(pd.DataFrame({comp_var: [client_val]})).mark_rule(color=COLOR_RISK, size=3).encode(x=f"{comp_var}:Q")

st.altair_chart(chart + line, use_container_width=True)

if show_text_desc:
    st.write(f"**Analyse :** Le client se situe à la valeur **{client_val:,.0f}**. "
             f"La majorité des clients sont regroupés entre {plot_df[comp_var].min():,.0f} et {plot_df[comp_var].max():,.0f}.")

st.markdown("---")

# 5. Simulation & Nouveau Dossier (Optionnel)
st.subheader("🔄 Simulation & Modification")

with st.expander("Modifier les informations pour tester l'impact"):
    with st.form("simu_form"):
        new_income = st.number_input("Nouveau Revenu Annuel", value=int(client_data["AMT_INCOME_TOTAL"]))
        new_credit = st.number_input("Nouveau Montant Crédit", value=int(client_data["AMT_CREDIT"]))
        
        if st.form_submit_button("Calculer le nouveau score"):
            simu_data = client_data.copy()
            simu_data["AMT_INCOME_TOTAL"] = new_income
            simu_data["AMT_CREDIT"] = new_credit
            
            # Appel API
            res_sim = requests.post(API_URL, json=simu_data).json()
            st.write(f"Nouvelle probabilité : **{res_sim['probability']*100:.1f}%**")

# ============================================================
# 📄 FOOTER ACCESSIBILITÉ
# ============================================================
st.markdown("---")
st.caption("ℹ️ Ce dashboard respecte les normes WCAG : contrastes gérés, pas d'usage exclusif de la couleur, descriptions textuelles disponibles.")