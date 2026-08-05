import streamlit as st
import pandas as pd
import joblib

# Load model, encoders and scaler
model = joblib.load("credit_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(
    page_title="AI Credit Risk Assessment System",
    page_icon="💳",
    layout="centered"
)

st.title("💳 AI-Based Credit Risk Assessment System")

st.write(
    "Predict whether a customer is at **Low Credit Risk** or **High Credit Risk**."
)

st.markdown("---")

# ----------------------------
# User Inputs
# ----------------------------

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

married = st.selectbox(
    "Marital Status",
    ["Yes", "No"]
)

dependents = st.selectbox(
    "Dependents",
    ["0", "1", "2", "3+"]
)

education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

applicant_income = st.number_input(
    "Applicant Income",
    min_value=0,
    value=5000
)

coapplicant_income = st.number_input(
    "Coapplicant Income",
    min_value=0.0,
    value=0.0
)

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0.0,
    value=150.0
)

loan_term = st.number_input(
    "Loan Amount Term (Months)",
    min_value=1.0,
    value=360.0
)

credit_history = st.selectbox(
    "Credit History",
    [1.0, 0.0],
    format_func=lambda x: "Good" if x == 1 else "Poor"
)

property_area = st.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)

st.markdown("---")
if st.button("Predict Credit Risk", use_container_width=True):

    input_data = pd.DataFrame({

        "Gender": [gender],
        "Married": [married],
        "Dependents": [dependents],
        "Education": [education],
        "Self_Employed": [self_employed],
        "ApplicantIncome": [applicant_income],
        "CoapplicantIncome": [coapplicant_income],
        "LoanAmount": [loan_amount],
        "Loan_Amount_Term": [loan_term],
        "Credit_History": [credit_history],
        "Property_Area": [property_area]

    })

    # Encode categorical columns
    categorical_columns = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area"
    ]

    for col in categorical_columns:
        input_data[col] = label_encoders[col].transform(input_data[col])

    # ----------------------------
    # Feature Engineering
    # ----------------------------

    input_data["TotalIncome"] = (
        input_data["ApplicantIncome"] +
        input_data["CoapplicantIncome"]
    )

    input_data["LoanIncomeRatio"] = (
        input_data["LoanAmount"] /
        (input_data["TotalIncome"] + 1)
    )

    input_data["EstimatedEMI"] = (
        input_data["LoanAmount"] /
        input_data["Loan_Amount_Term"]
    )

    # Scale Input
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    confidence = max(probability) * 100

    st.markdown("## Prediction Result")

    if prediction == 1:

        st.success("🟢 LOW CREDIT RISK")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.info("🟢 Recommendation : Loan can be approved.")

    else:

        st.error("❌ HIGH CREDIT RISK")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.warning("🔴 Recommendation : Loan approval is risky.")
        st.markdown("### Customer Summary")

    st.write(f"**Applicant Income:** ₹ {applicant_income}")

    st.write(f"**Coapplicant Income:** ₹ {coapplicant_income}")

    st.write(f"**Loan Amount:** {loan_amount}")

    st.write(f"**Loan Amount Term:** {loan_term} Months")

    st.write(f"**Credit History:** {'Good' if credit_history == 1 else 'Poor'}")

    st.write(f"**Education:** {education}")

    st.write(f"**Self Employed:** {self_employed}")

    st.write(f"**Property Area:** {property_area}")

    st.markdown("---")

st.caption(
    "Developed using Python • Streamlit • Scikit-learn • Random Forest"
)