import joblib
import pandas as pd
import os

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "loan_model_clean.sav")
FEATURE_PATH = os.path.join(BASE_DIR, "features.pkl")


# ✅ Load model and feature list
def load_model():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURE_PATH)
    return model, features


# ✅ Build input EXACTLY like training/Jupyter
def build_model_input(raw_input, feature_names):

    # ✅ Initialize dataframe with required features
    X = pd.DataFrame(0, index=[0], columns=feature_names)

    # ✅ Direct numeric features
    if "ApplicantIncome" in X.columns:
        X.loc[0, "ApplicantIncome"] = float(raw_input["ApplicantIncome"])

    if "CoapplicantIncome" in X.columns:
        X.loc[0, "CoapplicantIncome"] = float(raw_input["CoapplicantIncome"])

    # ✅ Derived features (VERY IMPORTANT)

    # Education_Not Graduate
    if "Education_Not Graduate" in X.columns:
        X.loc[0, "Education_Not Graduate"] = (
            1 if raw_input["Education"] == "Not Graduate" else 0
        )

    # Credit_History_No_History
    if "Credit_History_No_History" in X.columns:
        X.loc[0, "Credit_History_No_History"] = (
            0 if int(raw_input["Credit_History"]) == 0 else 1
        )


    # Self_Employed_Yes (safe fallback)
    if "Self_Employed_Yes" in X.columns:
        X.loc[0, "Self_Employed_Yes"] = (
            1 if raw_input.get("Self_Employed") == "Yes" else 0
        )


    return X


# ✅ Prediction function
def get_prediction(raw_data):

    model, features = load_model()

    # ✅ Convert list to dictionary
    raw_input = {
        'ApplicantIncome': raw_data[0],
        'CoapplicantIncome': raw_data[1],
        'LoanAmount': raw_data[2],
        'Loan_Amount_Term': raw_data[3],
        'Credit_History': raw_data[4],
        'Gender': raw_data[5],
        'Education': raw_data[6],
        'Married': raw_data[7],
        'Dependents': raw_data[8],
        'Property_Area': raw_data[9]
    }

    # ✅ Build model input (same as Jupyter)
    X_new = build_model_input(raw_input, features)

    # ✅ Predict
    prediction = model.predict(X_new)[0]
    probability = model.predict_proba(X_new)[0][1]

    return prediction, round(probability * 100, 2)
