import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler

import xgboost as xgb

# PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "leads_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# LOAD DATA
data = pd.read_csv(DATA_PATH)

# CLEAN DATA
data.fillna(0, inplace=True)

# FEATURE ENGINEERING
data["budget_per_employee"] = data["budget"] / (data["company_size"] + 1)

X = data[['company_size', 'budget', 'interaction_score', 'budget_per_employee']]
y = data['converted']

# SCALE FEATURES
scaler = StandardScaler()
X = scaler.fit_transform(X)

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# LOGISTIC REGRESSION
lr_model = LogisticRegression(max_iter=1000, class_weight='balanced')
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

lr_acc = accuracy_score(y_test, lr_pred)
lr_prec = precision_score(y_test, lr_pred, zero_division=0)
lr_rec = recall_score(y_test, lr_pred, zero_division=0)
lr_auc = roc_auc_score(y_test, lr_model.predict_proba(X_test)[:, 1])

# XGBOOST
xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

xgb_acc = accuracy_score(y_test, xgb_pred)
xgb_prec = precision_score(y_test, xgb_pred, zero_division=0)
xgb_rec = recall_score(y_test, xgb_pred, zero_division=0)
xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1])

# PRINT RESULTS
print("\n===== Logistic Regression =====")
print("Accuracy:", lr_acc)
print("Precision:", lr_prec)
print("Recall:", lr_rec)
print("ROC-AUC:", lr_auc)

print("\n===== XGBoost =====")
print("Accuracy:", xgb_acc)
print("Precision:", xgb_prec)
print("Recall:", xgb_rec)
print("ROC-AUC:", xgb_auc)

# SELECT BEST MODEL
if xgb_auc > lr_auc:
    best_model = xgb_model
    best_name = "XGBoost"
    best_score = xgb_auc
else:
    best_model = lr_model
    best_name = "Logistic Regression"
    best_score = lr_auc

# SAVE MODEL + SCALER
joblib.dump(best_model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print(f"\nBest model saved: {best_name} (ROC-AUC: {best_score:.4f})")
print("Model saved at:", MODEL_PATH)