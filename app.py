import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="CBC Neurological Risk Dashboard",
    layout="wide"
)

# -----------------------------------
# HEADER
# -----------------------------------
st.title("🩺 CBC Neurological Risk Dashboard")

st.markdown(
    "AI-assisted CBC interpretation and neurological risk analysis."
)

st.markdown("---")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "Upload CBC CSV File",
    type=["csv"]
)

# -----------------------------------
# MAIN LOGIC
# -----------------------------------
if uploaded_file is not None:

    try:

        # -----------------------------------
        # LOAD DATA
        # -----------------------------------
        df = pd.read_csv(uploaded_file)

        # Clean data
        df.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True
        )

        df.fillna(0, inplace=True)

        st.success("Dataset loaded successfully!")

        # -----------------------------------
        # DATA PREVIEW
        # -----------------------------------
        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        st.write("Detected Columns:")

        st.write(list(df.columns))

        # -----------------------------------
        # SIDEBAR
        # -----------------------------------
        st.sidebar.header("Patient Selection")

        patient_id = st.sidebar.selectbox(
            "Select Patient Row",
            df.index
        )

        patient = df.loc[patient_id]

        # -----------------------------------
        # DETECT CBC COLUMNS
        # -----------------------------------
        possible_cols = [
            'HGB',
            'WBC',
            'PLT',
            'RBC',
            'HCT',
            'MCV',
            'MCH',
            'LYMPH',
            'NEUT'
        ]

        available_cols = [
            col for col in possible_cols
            if col in df.columns
        ]

        # -----------------------------------
        # PATIENT METRICS
        # -----------------------------------
        st.subheader("Patient CBC Metrics")

        metric_cols = st.columns(
            min(4, len(available_cols))
        )

        for i, col_name in enumerate(
            available_cols[:4]
        ):

            try:

                value = round(
                    float(patient[col_name]),
                    2
                )

            except:

                value = 0

            metric_cols[i].metric(
                col_name,
                value
            )

        # -----------------------------------
        # CBC CHART
        # -----------------------------------
        st.subheader("CBC Parameter Visualization")

        chart_df = pd.DataFrame({

            "Parameter": available_cols,

            "Value": [

                float(patient[c])

                if pd.notnull(patient[c])

                else 0

                for c in available_cols
            ]
        })

        fig = px.bar(

            chart_df,

            x="Parameter",

            y="Value",

            text="Value",

            title="CBC Parameters"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -----------------------------------
        # RAW PATIENT DATA
        # -----------------------------------
        st.subheader("Patient Details")

        patient_df = pd.DataFrame(
            patient
        ).reset_index()

        patient_df.columns = [
            "Parameter",
            "Value"
        ]

        st.dataframe(
            patient_df,
            use_container_width=True
        )

        # -----------------------------------
        # CLINICAL INTERPRETATION
        # -----------------------------------
        st.subheader("Clinical Interpretation")

        interpretations = []

        # -----------------------------
        # HGB
        # -----------------------------
        if 'HGB' in df.columns:

            if patient['HGB'] < 12:

                interpretations.append(
                    "⚠️ Low Hemoglobin detected — possible anemia."
                )

                interpretations.append(
                    "🧠 Severe anemia may contribute to fatigue, dizziness, cognitive slowing, and neurological symptoms."
                )

        # -----------------------------
        # WBC
        # -----------------------------
        if 'WBC' in df.columns:

            if patient['WBC'] > 11:

                interpretations.append(
                    "⚠️ Elevated WBC count detected — possible infection or inflammation."
                )

                interpretations.append(
                    "🧠 Significant inflammatory conditions may occasionally correlate with neurological complications."
                )

            elif patient['WBC'] < 4:

                interpretations.append(
                    "⚠️ Low WBC count detected — possible immune suppression."
                )

        # -----------------------------
        # PLATELETS
        # -----------------------------
        if 'PLT' in df.columns:

            if patient['PLT'] < 150:

                interpretations.append(
                    "⚠️ Low platelet count detected."
                )

                interpretations.append(
                    "🧠 Severe thrombocytopenia may increase neurological bleeding risk in critical cases."
                )

        # -----------------------------
        # RBC
        # -----------------------------
        if 'RBC' in df.columns:

            if patient['RBC'] < 4:

                interpretations.append(
                    "⚠️ Reduced RBC count detected."
                )

        # -----------------------------
        # MCV
        # -----------------------------
        if 'MCV' in df.columns:

            if patient['MCV'] > 100:

                interpretations.append(
                    "⚠️ Elevated MCV detected — possible macrocytic anemia."
                )

                interpretations.append(
                    "🧠 Macrocytic anemia may correlate with Vitamin B12 deficiency and neurological impairment."
                )

        # -----------------------------------
        # RISK SCORING
        # -----------------------------------
        risk_score = 0

        if 'HGB' in df.columns:

            if patient['HGB'] < 10:

                risk_score += 2

        if 'WBC' in df.columns:

            if patient['WBC'] > 15:

                risk_score += 2

        if 'PLT' in df.columns:

            if patient['PLT'] < 100:

                risk_score += 2

        if 'MCV' in df.columns:

            if patient['MCV'] > 100:

                risk_score += 1

        # -----------------------------------
        # NEUROLOGICAL RISK
        # -----------------------------------
        st.subheader(
            "Neurological Risk Assessment"
        )

        if risk_score >= 5:

            st.error(
                "🔴 High neurological risk indicators detected based on CBC abnormalities."
            )

        elif risk_score >= 3:

            st.warning(
                "🟠 Moderate neurological risk indicators detected."
            )

        elif risk_score >= 1:

            st.info(
                "🟡 Mild neurological correlation factors detected."
            )

        else:

            st.success(
                "🟢 No major neurological risk correlations identified from CBC parameters."
            )

        # -----------------------------------
        # DISPLAY INTERPRETATIONS
        # -----------------------------------
        if len(interpretations) == 0:

            st.success(
                "CBC parameters appear within expected ranges."
            )

        else:

            for item in interpretations:

                st.write(item)

        # -----------------------------------
        # DOWNLOAD SECTION
        # -----------------------------------
        st.subheader("Download Processed Data")

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_cbc.csv",
            mime="text/csv"
        )

        # -----------------------------------
        # DISCLAIMER
        # -----------------------------------
        st.markdown("---")

        st.caption(
            "Disclaimer: CBC-based neurological risk analysis is supportive only and not a definitive medical diagnosis."
        )

    except Exception as e:

        st.error(
            "Error while processing the file."
        )

        st.exception(e)

# -----------------------------------
# EMPTY STATE
# -----------------------------------
else:

    st.info(
        "Please upload a CBC CSV file to begin analysis."
    )
