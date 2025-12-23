from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os


# ============================================================
# ⚙️ CONFIGURATION
# ============================================================


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Vérifie bien que ton dossier s'appelle "models" sur GitHub
MODEL_PATH = os.path.join(BASE_DIR, "models", "pipeline_best_model_top20.joblib")
SEUIL_METIER = 0.29


# ============================================================
# 🚀 INITIALISATION API
# ============================================================


app = FastAPI(
    title="API Scoring Crédit — Projet 7",
    description="API de prédiction du risque de défaut (20 variables)",
    version="1.0"
)


# ============================================================
# 📦 CHARGEMENT DU MODÈLE (ROBUSTE)
# ============================================================


model = None
try:
    if os.path.exists(MODEL_PATH):
        # Le chargement peut échouer ici si les versions de sklearn divergent
        model = joblib.load(MODEL_PATH)
        print("✅ Modèle chargé avec succès")
    else:
        print(f"❌ Erreur : Fichier introuvable à {MODEL_PATH}")
except Exception as e:
    # Apparaîtra dans tes logs Render en cas de crash
    print(f"💥 Erreur fatale lors du chargement du modèle : {str(e)}")


# ============================================================
# 🔐 SCHÉMA OFFICIEL — CONTRAT API
# ============================================================


class InputFeatures(BaseModel):
    AMT_ANNUITY: float
    AMT_CREDIT: float
    AMT_GOODS_PRICE: float
    AMT_INCOME_TOTAL: float
    AMT_REQ_CREDIT_BUREAU_QRT: float
    AMT_REQ_CREDIT_BUREAU_YEAR: float
    CODE_GENDER_F: int
    DAYS_BIRTH: float
    DAYS_EMPLOYED: float
    DAYS_ID_PUBLISH: float
    DAYS_LAST_PHONE_CHANGE: float
    DAYS_REGISTRATION: float
    EXT_SOURCE_1: float
    EXT_SOURCE_2: float
    EXT_SOURCE_3: float
    HOUR_APPR_PROCESS_START: int
    NAME_CONTRACT_TYPE: int
    OWN_CAR_AGE: float
    REGION_POPULATION_RELATIVE: float
    TOTALAREA_MODE: float


# ============================================================
# 🏠 ENDPOINT RACINE (AVEC FIX POUR RENDER)
# ============================================================


@app.get("/")
@app.head("/")  # <--- FIX : Répond positivement aux tests de connexion de Render
def home():
    return {
        "message": "API opérationnelle",
        "nb_features": 20,
        "seuil_metier": SEUIL_METIER,
        "model_loaded": model is not None
    }


# ============================================================
# 🔮 ENDPOINT DE PRÉDICTION
# ============================================================


@app.post("/predict")
def predict(features: InputFeatures):


    if model is None:
        raise HTTPException(
            status_code=500, 
            detail="Le modèle n'est pas disponible sur le serveur."
        )


    try:
        # Conversion des données reçues en DataFrame pour le pipeline
        X = pd.DataFrame([features.dict()])
        
        # Prédiction de probabilité
        proba = model.predict_proba(X)[0, 1]
        decision = int(proba >= SEUIL_METIER)


        return {
            "probability": float(proba),
            "decision": decision,   # 1 = refus, 0 = accord
            "threshold": SEUIL_METIER
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")


