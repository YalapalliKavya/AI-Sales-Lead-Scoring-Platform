import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_lead(company_size, budget, interaction_score):

    
    budget_per_employee = budget / (company_size + 1)

   
    data = pd.DataFrame([{
        "company_size": company_size,
        "budget": budget,
        "interaction_score": interaction_score,
        "budget_per_employee": budget_per_employee
    }])

    
    data_scaled = scaler.transform(data)

    
    probability = model.predict_proba(data_scaled)[0][1]

    
    score = int(probability * 100)

    return score, probability