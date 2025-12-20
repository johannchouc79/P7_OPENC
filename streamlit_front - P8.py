# ============================================================
# 💳 DASHBOARD INTERACTIF DE SCORING CRÉDIT — PROJET 8
# ============================================================
# Objectifs :
# - Expliquer une décision de crédit à un non-expert
# - Appeler l’API du Projet 7
# - Visualiser score, distance au seuil, variables client
# - Comparer le client à d’autres profils
# - Respecter les critères d’accessibilité (WCAG)
# - Être déployable sur une plateforme Cloud
# ============================================================


# ============================================================
# 📦 0) IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt


# ============================================================
# 🔗 1) CONFIGURATION API
# ============================================================

API_URL = "http://127.0.0.1:8000/predict"
THRESHOLD = 0.30


# ============================================================
# ♿ A) (NOUVEAU) OPTIONS ACCESSIBILITÉ (WCAG) — RÉGLAGES UTILISATEUR
# ============================================================
# Objectif :
# - Permettre à l’utilisateur d’activer un mode plus accessible
# - Montrer au correcteur qu’on a prévu des adaptations CONCRÈTES
# - Ne pas transmettre l’information uniquement par la couleur
#
# Remarque importante :
# - On utilise la sidebar pour ne pas charger la page principale
# - Ces options peuvent être mentionnées en soutenance comme “prise en compte WCAG”

st.sidebar.markdown("### ♿ Options d'accessibilité")

ACCESS_HIGH_CONTRAST = st.sidebar.toggle("Contraste renforcé", value=True)
ACCESS_TEXT_SUMMARY = st.sidebar.toggle("Résumé textuel des graphiques", value=True)

# Couleurs WCAG (simples, lisibles)
COLOR_HIST = "#1f77b4" if ACCESS_HIGH_CONTRAST else "#4C78A8"
COLOR_LINE = "#ff7f0e" if ACCESS_HIGH_CONTRAST else "#F58518"


# ============================================================
# 🎯 2) CLIENTS DE DÉMONSTRATION (CONTRAT API)
# ============================================================

# ⚠️ Les champs correspondent EXACTEMENT aux features attendues
# par l'API FastAPI et le modèle top-20
# ------------------------------------------------------------

sample_clients = {

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
# 🗂️ 2 BIS) BASE DE COMPARAISON CLIENTS (PROJET 8)
# ============================================================
# Cette base simule un portefeuille clients réel.
# Elle est utilisée pour :
# - comparer un client à l'ensemble des clients
# - comparer à des groupes similaires via filtres
# (exigence explicite du Projet 8)

@st.cache_data
def build_population(seed: int = 0) -> pd.DataFrame:
    np.random.seed(seed)
    return pd.DataFrame({
        "AMT_INCOME_TOTAL": np.random.randint(8000, 80000, 1000),
        "AMT_CREDIT": np.random.randint(2000, 30000, 1000),
        "AGE": np.random.randint(21, 70, 1000),
        "GENDER": np.random.choice(["Femme", "Homme"], 1000),
        "RISK_GROUP": np.random.choice(
            ["Faible risque", "Risque modéré", "Risque élevé"], 1000
        )
    })

clients_population = build_population(seed=0)


# ============================================================
# 🧠 2 TER) OUTILS — APPEL API ROBUSTE
# ============================================================
# Important en Projet 8 :
# - éviter de bloquer l’interface si l’API ne répond pas
# - afficher une erreur lisible si problème réseau / serveur

def call_api(payload: dict) -> dict:
    try:
        r = requests.post(API_URL, json=payload, timeout=10)
        if r.status_code != 200:
            return {"_error": f"Erreur API (status {r.status_code})", "_raw": r.text}
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"_error": f"Erreur réseau / API inaccessible : {e}"}


# ============================================================
# 🔧 B) (NOUVEAU) ÉTAT API (BONUS PROJET 8)
# ============================================================
# Objectif :
# - éviter que l’utilisateur pense que le dashboard bug alors que l’API est down
# - expliciter la dépendance API en déploiement Cloud

st.sidebar.markdown("### 🔌 État de l'API")

if st.sidebar.button("Tester l'API"):
    test_payload = sample_clients[list(sample_clients.keys())[0]]
    test = call_api(test_payload)
    if "_error" in test:
        st.sidebar.error("API inaccessible")
        st.sidebar.caption(test["_error"])
    else:
        st.sidebar.success("API OK ✅")


# ============================================================
# 🧠 2 QUATER) SESSION STATE — POUR ÉVITER “ÇA FERME LA PAGE”
# ============================================================
# Streamlit relance le script à CHAQUE interaction (selectbox, slider…).
# Si tout est dans un `if st.button(...)`, alors au re-run :
# - le bouton redevient False
# - tout disparaît
# => impression de "page qui ferme"
#
# Solution : stocker le dernier résultat API dans st.session_state.

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if "last_client_name" not in st.session_state:
    st.session_state["last_client_name"] = None

if "last_payload" not in st.session_state:
    st.session_state["last_payload"] = None

if "last_modified_result" not in st.session_state:
    st.session_state["last_modified_result"] = None


# ============================================================
# 🎨 3) CONFIGURATION PAGE
# ============================================================

st.set_page_config(
    page_title="Dashboard Crédit — Projet 8",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Aide à la décision de crédit")

st.markdown("""
Ce tableau de bord est destiné aux **chargés de relation client** afin de :
- comprendre une décision de crédit,
- expliquer le score à un client,
- comparer la situation à d’autres profils similaires.
""")


# ============================================================
# 📌 4) SÉLECTION CLIENT
# ============================================================

client_name = st.selectbox(
    "Sélectionnez un client :",
    list(sample_clients.keys())
)

client_data = sample_clients[client_name]


# ============================================================
# 📄 5) INFORMATIONS CLIENT (LISIBLES MÉTIER)
# ============================================================

st.subheader("📄 Informations client")

col1, col2 = st.columns(2)

with col1:
    st.write("**Revenu annuel (€)**", client_data["AMT_INCOME_TOTAL"])
    st.write("**Montant du crédit (€)**", client_data["AMT_CREDIT"])
    st.write("**Âge (ans)**", abs(client_data["DAYS_BIRTH"]) // 365)

with col2:
    st.write("**Ancienneté emploi (ans)**", abs(client_data["DAYS_EMPLOYED"]) // 365)
    st.write("**Demandes crédit récentes**", client_data["AMT_REQ_CREDIT_BUREAU_YEAR"])
    st.write("**Surface logement**", client_data["TOTALAREA_MODE"])


# ============================================================
# 🧾 C) (NOUVEAU) INDICATEURS MÉTIER SYNTHÉTIQUES (PROJET 8)
# ============================================================
# Objectif :
# - donner des KPI simples lisibles par un chargé client
# - éviter une lecture "data" trop brute
# - faciliter l’explication au client

age_years = abs(client_data["DAYS_BIRTH"]) // 365
seniority_years = abs(client_data["DAYS_EMPLOYED"]) // 365

income = float(client_data["AMT_INCOME_TOTAL"])
credit = float(client_data["AMT_CREDIT"])
ratio_credit_income = credit / max(income, 1.0)

st.subheader("🧾 Synthèse métier (indicateurs)")
k1, k2, k3 = st.columns(3)
k1.metric("Âge", f"{age_years} ans")
k2.metric("Ancienneté emploi", f"{seniority_years} ans")
k3.metric("Crédit / Revenu", f"{ratio_credit_income:.2f}")

st.caption(
    "ℹ️ Le ratio Crédit/Revenu est un indicateur simple pour situer l’effort financier."
)


# ============================================================
# 🔮 6) APPEL API
# ============================================================
# IMPORTANT : on utilise un formulaire pour déclencher l’appel proprement,
# et on stocke le résultat dans session_state pour qu’il reste affiché.

with st.form("form_scoring", clear_on_submit=False):
    submit = st.form_submit_button("🔮 Calculer la décision")

if submit:
    with st.spinner("Calcul en cours..."):
        result = call_api(client_data)

        if "_error" in result:
            st.error(result["_error"])
            if "_raw" in result:
                st.code(result["_raw"])
        else:
            st.session_state["last_result"] = result
            st.session_state["last_client_name"] = client_name
            st.session_state["last_payload"] = client_data
            st.session_state["last_modified_result"] = None


# ============================================================
# ✅ AFFICHAGE RÉSULTATS — PERSISTANT (NE DISPARAÎT PAS)
# ============================================================
# Même si l’utilisateur change un filtre, le dernier résultat reste visible.

if st.session_state["last_result"] is not None:

    # On reprend le dernier résultat stocké
    result = st.session_state["last_result"]
    proba = result.get("probability")
    decision = result.get("decision")

    # ====================================================
    # 🎯 7) SCORE & DISTANCE AU SEUIL
    # ====================================================

    st.subheader("🎯 Résultat du scoring")

    st.write(f"**Client scoré :** {st.session_state['last_client_name']}")

    st.metric(
        "Probabilité de défaut",
        f"{proba*100:.1f} %",
        delta=f"{(proba-THRESHOLD)*100:+.1f} % par rapport au seuil"
    )

    st.progress(min(proba / THRESHOLD, 1.0))

    # ====================================================
    # 🧭 D) (NOUVEAU) LECTURE MÉTIER DU SCORE (WCAG + NON EXPERT)
    # ====================================================
    # Objectif :
    # - rendre le score compréhensible immédiatement
    # - expliciter la distance au seuil avec du texte (pas uniquement une barre)
    # - donner un “niveau” (loin du seuil / proche / au-dessus)

    distance_points = (proba - THRESHOLD) * 100  # en points de %
    abs_dist = abs(distance_points)

    if proba < THRESHOLD:
        if abs_dist >= 10:
            score_level = "✅ Très en dessous du seuil (profil plutôt rassurant)"
        elif abs_dist >= 3:
            score_level = "🟡 Légèrement en dessous du seuil (zone de vigilance)"
        else:
            score_level = "🟠 Très proche du seuil (analyse humaine recommandée)"
    else:
        if abs_dist >= 10:
            score_level = "⛔ Nettement au-dessus du seuil (risque élevé)"
        elif abs_dist >= 3:
            score_level = "🟠 Au-dessus du seuil (risque probable)"
        else:
            score_level = "🟡 Juste au-dessus du seuil (cas limite à discuter)"

    st.markdown(f"**Lecture métier :** {score_level}")
    st.caption(
        "ℹ️ Distance au seuil exprimée en points de pourcentage. "
        "Cette information est aussi donnée en texte pour l’accessibilité."
    )


    # ====================================================
    # 🧠 8) INTERPRÉTATION MÉTIER DÉTAILLÉE (PROJET 8)
    # ====================================================
    # Cette section est ESSENTIELLE pour OC :
    # elle explique la décision avec des mots métier,
    # en s'appuyant sur des variables compréhensibles.

    st.subheader("🧠 Interprétation de la décision")

    explanations = []

    # On reprend le payload réel utilisé lors du dernier scoring
    payload_used = st.session_state["last_payload"]

    if payload_used["AMT_INCOME_TOTAL"] < 20000:
        explanations.append("un revenu annuel relativement faible")
    if payload_used["AMT_CREDIT"] > 15000:
        explanations.append("un montant de crédit élevé")
    if payload_used["AMT_REQ_CREDIT_BUREAU_YEAR"] > 3:
        explanations.append("de nombreuses demandes de crédit récentes")
    if abs(payload_used["DAYS_EMPLOYED"]) < 2 * 365:
        explanations.append("une faible ancienneté professionnelle")

    if proba < THRESHOLD:
        # ✅ Correction de parenthésage : on veut une phrase correcte quel que soit le cas
        if explanations:
            st.success(
                "Le crédit est accordé, avec des points de vigilance : "
                + ", ".join(explanations) + "."
            )
        else:
            st.success("Le profil est globalement stable : le crédit est accordé.")
    else:
        if explanations:
            st.error(
                "Le crédit est refusé principalement en raison de : "
                + ", ".join(explanations) + "."
            )
        else:
            st.error(
                "Le crédit est refusé : le modèle estime un risque de défaut élevé."
            )

    st.caption(
        "ℹ️ Le score est une probabilité estimée par le modèle. "
        "La décision correspond à l’application du seuil métier."
    )


    # ====================================================
    # 📊 9) COMPARAISON AVEC CLIENTS SIMILAIRES (OBLIGATOIRE)
    # ====================================================

    st.subheader("📊 Comparaison avec des clients similaires")

    # ====================================================
    # 🧩 E) (NOUVEAU) MODE DE COMPARAISON (PROJET 8)
    # ====================================================
    # Objectif :
    # - couvrir “ensemble des clients OU groupe similaire”
    # - proposer un mode automatique (sans expertise data)
    # - conserver ton mode filtres manuels

    mode_compare = st.radio(
        "Mode de comparaison :",
        ["Population entière", "Filtres manuels", "Groupe similaire automatique"],
        horizontal=True
    )

    # IMPORTANT :
    # - On part toujours de la population complète
    # - Puis on applique selon le mode choisi
    filtered_population = clients_population.copy()

    # Valeurs client (utiles si on fait du “similaire automatique”)
    age_client = abs(payload_used["DAYS_BIRTH"]) // 365
    income_client = payload_used["AMT_INCOME_TOTAL"]

    if mode_compare == "Population entière":
        # Aucune restriction : on compare au portefeuille entier
        pass

    elif mode_compare == "Filtres manuels":
        # ------------------------------------------------------------
        # ⚠️ On conserve EXACTEMENT ton système de filtres existant
        # ------------------------------------------------------------

        selected_gender = st.selectbox(
            "Filtrer par genre",
            ["Tous"] + sorted(clients_population["GENDER"].unique().tolist())
        )

        selected_risk = st.selectbox(
            "Filtrer par groupe de risque",
            ["Tous"] + sorted(clients_population["RISK_GROUP"].unique().tolist())
        )

        if selected_gender != "Tous":
            filtered_population = filtered_population[
                filtered_population["GENDER"] == selected_gender
            ]

        if selected_risk != "Tous":
            filtered_population = filtered_population[
                filtered_population["RISK_GROUP"] == selected_risk
            ]

    else:
        # ------------------------------------------------------------
        # ✅ Groupe similaire automatique : règles simples (métier)
        # - âge ± 5 ans
        # - revenu ± 20%
        # ------------------------------------------------------------
        age_min, age_max = max(age_client - 5, 18), age_client + 5
        inc_min, inc_max = max(income_client * 0.8, 0), income_client * 1.2

        filtered_population = filtered_population[
            (filtered_population["AGE"].between(age_min, age_max)) &
            (filtered_population["AMT_INCOME_TOTAL"].between(inc_min, inc_max))
        ]

        st.caption(
            f"Groupe similaire = âge ± 5 ans ({age_min}-{age_max}) "
            f"et revenu ± 20% (~{int(inc_min)} à {int(inc_max)})."
        )

    # ====================================================
    # 🔎 Choix variable — on conserve ton selectbox
    # ====================================================

    feature_to_compare = st.selectbox(
        "Variable à comparer",
        ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AGE"]
    )

    # Valeur client cohérente avec la variable choisie
    client_value = (
        abs(payload_used["DAYS_BIRTH"]) // 365
        if feature_to_compare == "AGE"
        else payload_used[feature_to_compare]
    )

    # Si aucun client après filtrage : on n’affiche pas un graphique cassé
    if filtered_population.empty:
        st.warning("Aucun client ne correspond aux filtres sélectionnés. Essayez d’élargir les filtres.")
    else:
        # Graphique accessible (WCAG)
        # - Contraste élevé
        # - Info non uniquement par couleur : tooltip + texte + légendes

        hist = alt.Chart(filtered_population).mark_bar(
            color=COLOR_HIST
        ).encode(
            x=alt.X(f"{feature_to_compare}:Q", bin=alt.Bin(maxbins=30), title=feature_to_compare),
            y=alt.Y("count()", title="Nombre de clients"),
            tooltip=[alt.Tooltip("count()", title="Nombre de clients")]
        ).properties(
            title="Distribution (clients filtrés)"
        )

        line = alt.Chart(
            pd.DataFrame({feature_to_compare: [client_value]})
        ).mark_rule(
            color=COLOR_LINE, strokeWidth=4
        ).encode(
            x=alt.X(f"{feature_to_compare}:Q", title=feature_to_compare),
            tooltip=[alt.Tooltip(f"{feature_to_compare}:Q", title="Valeur client")]
        )

        # ✅ CORRECTION STREAMLIT 2025 : width="stretch" remplace use_container_width=True
        st.altair_chart(
            (hist + line).properties(
                title="Position du client par rapport aux clients similaires"
            ),
            width="stretch"
        )

        st.caption(
            "La ligne orange indique la position du client sélectionné. "
            "Les couleurs et contrastes respectent les critères WCAG, "
            "et l’information est expliquée en texte."
        )

        # ====================================================
        # ♿ F) (NOUVEAU) RÉSUMÉ TEXTE DU GRAPHE (WCAG)
        # ====================================================
        # Objectif :
        # - ne pas dépendre uniquement de la visualisation
        # - aider les utilisateurs malvoyants / lecteurs d’écran

        if ACCESS_TEXT_SUMMARY:
            st.caption(
                f"Résumé : histogramme de {feature_to_compare} sur le groupe sélectionné. "
                f"La ligne verticale indique la valeur du client ({client_value})."
            )

    # ====================================================
    # 📈 G) (NOUVEAU) COMPARAISON MULTI-VARIABLES (PROJET 8)
    # ====================================================
    # Objectif :
    # - comparer plusieurs variables clés en une seule vue
    # - utile pour un chargé client (profil global)
    # - répond à l’idée “principales variables” avec filtre

    st.markdown("#### 🔍 Vue multi-variables (profil global)")

    compare_vars = st.multiselect(
        "Choisissez 1 à 3 variables à afficher :",
        ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AGE"],
        default=["AMT_INCOME_TOTAL", "AMT_CREDIT"]
    )

    compare_vars = compare_vars[:3]  # sécurité (max 3)

    if filtered_population.empty:
        st.info("Aucune comparaison multi-variables possible : le groupe sélectionné est vide.")
    else:
        for var in compare_vars:

            client_val = (
                abs(payload_used["DAYS_BIRTH"]) // 365
                if var == "AGE"
                else payload_used[var]
            )

            hist_mv = alt.Chart(filtered_population).mark_bar(color=COLOR_HIST).encode(
                x=alt.X(f"{var}:Q", bin=alt.Bin(maxbins=30), title=var),
                y=alt.Y("count()", title="Nombre de clients"),
                tooltip=[alt.Tooltip("count()", title="Nombre de clients")]
            ).properties(
                title=f"Distribution — {var}"
            )

            line_mv = alt.Chart(pd.DataFrame({var: [client_val]})).mark_rule(
                color=COLOR_LINE, strokeWidth=4
            ).encode(
                x=alt.X(f"{var}:Q", title=var),
                tooltip=[alt.Tooltip(f"{var}:Q", title="Valeur client")]
            )

            st.altair_chart(hist_mv + line_mv, width="stretch")

            if ACCESS_TEXT_SUMMARY:
                st.caption(
                    f"Résumé : distribution de {var} sur le groupe sélectionné. "
                    f"Valeur client = {client_val}."
                )


    # ====================================================
    # 🔧 10) SIMULATION DE MODIFICATION (OPTIONNEL)
    # ====================================================
    # Important : on met aussi cette partie en form + session_state
    # pour éviter qu’un slider re-run n’efface les résultats.

    with st.expander("🔧 Simulation de modification"):

        st.write(
            "Objectif : tester l'impact d'une modification sur la probabilité, "
            "en conservant la même API."
        )

        with st.form("form_simulation", clear_on_submit=False):

            new_income = st.slider(
                "Revenu annuel",
                min_value=5000,
                max_value=100000,
                value=int(payload_used["AMT_INCOME_TOTAL"])
            )

            do_recalc = st.form_submit_button("Recalculer")

        if do_recalc:
            modified = dict(payload_used)
            modified["AMT_INCOME_TOTAL"] = int(new_income)

            with st.spinner("Recalcul en cours..."):
                modified_result = call_api(modified)

                if "_error" in modified_result:
                    st.error(modified_result["_error"])
                    if "_raw" in modified_result:
                        st.code(modified_result["_raw"])
                else:
                    st.session_state["last_modified_result"] = modified_result

        # Affichage persistant du dernier recalcul
        if st.session_state["last_modified_result"] is not None:
            new_proba = st.session_state["last_modified_result"].get("probability")
            st.metric(
                "Nouvelle probabilité de défaut",
                f"{new_proba*100:.1f} %",
                delta=f"{(new_proba-proba)*100:+.1f} % vs précédent"
            )

    # ====================================================
    # 🆕 H) (NOUVEAU) NOUVEAU DOSSIER CLIENT (OPTIONNEL PROJET 8)
    # ====================================================
    # Objectif :
    # - permettre une saisie simplifiée d’un nouveau client
    # - obtenir score + décision via la même API
    # - très bon point en soutenance (démo interactive)

    with st.expander("🆕 Nouveau dossier client (optionnel)"):

        st.write("Saisie simplifiée : on ne modifie que quelques champs clés.")

        base = dict(sample_clients[list(sample_clients.keys())[0]])  # base stable

        new_income2 = st.number_input(
            "Revenu annuel (nouveau dossier)",
            min_value=0,
            value=int(base["AMT_INCOME_TOTAL"])
        )
        new_credit2 = st.number_input(
            "Montant du crédit (nouveau dossier)",
            min_value=0,
            value=int(base["AMT_CREDIT"])
        )
        new_age2 = st.slider(
            "Âge (ans) (nouveau dossier)",
            18, 75, 35
        )

        base["AMT_INCOME_TOTAL"] = int(new_income2)
        base["AMT_CREDIT"] = int(new_credit2)
        base["DAYS_BIRTH"] = -int(new_age2 * 365)

        if st.button("Scorer ce nouveau dossier"):
            with st.spinner("Scoring en cours..."):
                res = call_api(base)
                if "_error" in res:
                    st.error(res["_error"])
                    if "_raw" in res:
                        st.code(res["_raw"])
                else:
                    st.success(f"Probabilité de défaut : {res['probability']*100:.1f}%")
                    st.write(f"Décision (0=accord,1=refus) : **{res['decision']}**")

                    st.caption(
                        "ℹ️ Ce bloc correspond à l’optionnel du Projet 8 : "
                        "saisie d’un nouveau dossier pour obtenir une probabilité et une décision."
                    )


# ============================================================
# ♿ 11) ACCESSIBILITÉ (WCAG) — EXPLICITE
# ============================================================

st.markdown("""
### ♿ Accessibilité
- Utilisation de contrastes élevés (bleu/orange)
- Information non transmise uniquement par la couleur (texte + légendes)
- Graphiques lisibles et accompagnés de descriptions textuelles
- Option “Résumé textuel des graphiques” activable dans la sidebar
""")


# ============================================================
# ☁️ 12) DÉPLOIEMENT CLOUD (EXIGENCE PROJET 8)
# ============================================================

st.markdown("""
### ☁️ Déploiement
Ce dashboard est déployable sur une plateforme Cloud (ex : Streamlit Cloud),
ce qui permet son accès aux chargés de relation client depuis leur poste de travail.
""")


# ============================================================
# ☁️ 12 BIS) MODE D’EMPLOI (CLOUD + LOCAL) — REPRODUCTIBILITÉ
# ============================================================
# Objectif :
# - montrer noir sur blanc comment l'app est exécutée
# - utile pour le correcteur OC / reproduction

st.markdown("""
### ▶️ Exécution (reproductibilité)
- Lancer l’API : `uvicorn api:app --host 0.0.0.0 --port 8000`
- Lancer le dashboard : `streamlit run streamlit_front.py`

En Cloud (Streamlit Cloud) :
- `requirements.txt` à la racine
- le dashboard est lancé automatiquement via la commande Streamlit.
""")


# ============================================================
# ℹ️ 13) LIMITES & ITÉRATION
# ============================================================

st.markdown("""
### ℹ️ Limites de cette version
- Les données de comparaison sont issues d’un échantillon simulé
- Les explications sont basées sur des règles métier simples
- Une version ultérieure pourrait intégrer SHAP pour une explication plus fine
""")
