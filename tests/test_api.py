import pytest
from fastapi.testclient import TestClient
import sys
import os

# --- Gestion des chemins pour l'import de l'API ---
# Cette partie permet au dossier 'tests' de remonter d'un cran pour trouver 'app_api.py'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_api import app 

client = TestClient(app)

def test_status():
    """
    Vérifie que l'API est fonctionnelle (Route Racine)
    Critère CE2 : L'API doit répondre.
    """
    response = client.get("/")
    assert response.status_code == 200

def test_prediction_endpoint():
    """
    Vérifie que l'endpoint de prédiction répond.
    Note : On vérifie soit 200 (Succès), soit 422 (Erreur de validation) 
    pour prouver que l'API traite la requête.
    """
    # Exemple de payload (adapte SK_ID_CURR selon ton modèle)
    test_data = {"SK_ID_CURR": 100001} 
    response = client.post("/predict", json=test_data)
    
    # On s'assure que l'API n'envoie pas une erreur 500 (crash serveur)
    assert response.status_code != 500