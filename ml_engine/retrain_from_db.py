import os
import sys
from pathlib import Path


CURRENT_FILE = Path(__file__).resolve()
ML_ENGINE_DIR = CURRENT_FILE.parent
BACKEND_DIR = ML_ENGINE_DIR.parent   
PROJECT_ROOT = BACKEND_DIR.parent    

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

try:
    from xgboost import XGBClassifier
    xgb_available = True
except ImportError:
    xgb_available = False

from crm.models import Lead


def load_training_data():
    leads = Lead.objects.filter(crm_status__in=["Converted", "Lost"]).values(
        "company_size",
        "budget",
        "interaction_score",
        "crm_status"
    )

    df = pd.DataFrame(list(leads))

    if df.empty:
        print("No Converted/Lost lead data found for retraining.")
        return None, None

    df["converted"] = df["crm_status"].apply(lambda x: 1 if x == "Converted" else 0)

    X = df[["company_size", "budget", "interaction_score"]]
    y = df["converted"]

    return X, y


def train_and_save_model():
    X, y = load_training_data()

    if X is None or y is None:
        return

    if len(X) < 4:
        print("Not enough Converted/Lost leads for retraining. Add more records first.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_preds)

    best_model = lr_model
    best_name = "Logistic Regression"
    best_acc = lr_acc

    print(f"Logistic Regression Accuracy: {lr_acc:.2f}")

    
    if xgb_available:
        xgb_model = XGBClassifier(
            eval_metric="logloss",
            random_state=42
        )
        xgb_model.fit(X_train, y_train)
        xgb_preds = xgb_model.predict(X_test)
        xgb_acc = accuracy_score(y_test, xgb_preds)

        print(f"XGBoost Accuracy: {xgb_acc:.2f}")

        if xgb_acc > lr_acc:
            best_model = xgb_model
            best_name = "XGBoost"
            best_acc = xgb_acc
    else:
        print("XGBoost not installed. Using Logistic Regression only.")

    model_path = ML_ENGINE_DIR / "model.pkl"
    joblib.dump(best_model, model_path)

    print(f"Best model saved: {best_name} (Accuracy: {best_acc:.2f})")
    print(f"Model saved at: {model_path}")


if __name__ == "__main__":
    train_and_save_model()