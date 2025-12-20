import streamlit as st
import requests




# ============================================================
# 🎯 0) Clients de démonstration (CONTRAT API — 20 FEATURES)
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



API_URL = "http://127.0.0.1:8000/predict"




# ============================================================
# 🎨 PAGE CONFIG
# ============================================================


st.set_page_config(
    page_title="Home Credit — Scoring",
    page_icon="💳",
    layout="centered"
)


st.title("💳 Home Credit — Simulation de décision de crédit")


st.write(
    """
    Cette application illustre un **système de scoring crédit** basé sur :
    - un **modèle de machine learning**
    - une **API FastAPI**
    - une **règle métier indépendante** (seuil = 0,29)


    Le modèle prédit une **probabilité de défaut**,
    la décision finale est ensuite appliquée.
    """
)




# ============================================================
# 📌 1) Sélecteur de client
# ============================================================


client_name = st.selectbox(
    "Choisissez un client de démonstration :",
    list(sample_clients.keys())
)


client_data = sample_clients[client_name]


st.subheader("📄 Données envoyées à l’API")
st.json(client_data)




# ============================================================
# 📌 2) Appel API
# ============================================================


if st.button("🔮 Calculer la décision"):


    with st.spinner("Appel du modèle en cours..."):


        response = requests.post(API_URL, json=client_data)


        if response.status_code != 200:
            st.error("❌ Erreur lors de l'appel à l'API.")
        else:
            result = response.json()


            proba = result["probability"]
            decision = result["decision"]
            threshold = result.get("threshold", 0.29)


            st.subheader("🎯 Résultat du scoring")


            st.metric(
                label="Probabilité de défaut",
                value=f"{proba:.3f}"
            )


            st.write(f"**Seuil métier appliqué :** {threshold}")


            # ⚠️ LOGIQUE MÉTIER CORRECTE
            if decision == 0:
                st.success("✔️ Décision : **Crédit accordé**")
            else:
                st.error("❌ Décision : **Crédit refusé**")


            st.caption(
                "ℹ️ Le modèle prédit une probabilité. "
                "La décision finale est prise via une règle métier indépendante."
            )
