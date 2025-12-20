from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


app = FastAPI(
    title="API Scoring Crédit — Projet 7",
    description="API de prédiction du risque de défaut (20 variables)",
    version="1.0"
)


MODEL_PATH = "models/pipeline_best_model_top20.joblib"
SEUIL_METIER = 0.65


model = joblib.load(MODEL_PATH)


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




@app.get("/")
def home():
    return {
        "message": "API opérationnelle",
        "nb_features": 20,
        "seuil_metier": SEUIL_METIER
    }




@app.post("/predict")
def predict(features: InputFeatures):


    X = pd.DataFrame([features.dict()])


    proba = model.predict_proba(X)[0, 1]
    decision = int(proba >= SEUIL_METIER)


    return {
        "probability": float(proba),
        "decision": decision,   # 1 = refus, 0 = accord
        "threshold": SEUIL_METIER
    }
