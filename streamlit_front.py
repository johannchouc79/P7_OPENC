import streamlit as st
import requests




# ============================================================
# 🎯 0) Clients de démonstration (CONTRAT API — 20 FEATURES)
# ============================================================
# ⚠️ Les champs correspondent EXACTEMENT aux features attendues
# par l'API FastAPI et le modèle top-20
# ------------------------------------------------------------




sample_clients = {
    "Client_1 — Profil faible risque": {
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


    "Client_2 — Profil intermédiaire": {
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


    "Client_3 — Profil risqué": {
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
    - une **règle métier indépendante** (seuil = 0,65)


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
            threshold = result.get("threshold", 0.65)


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
