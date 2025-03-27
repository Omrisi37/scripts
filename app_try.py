import streamlit as st
import pandas as pd
import hashlib
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
from yaml.loader import SafeLoader

# ========================
# USER AUTHENTICATION SETUP
# ========================
# Using a YAML file for credentials (safer)
users = {
    "usernames": {
        "researcher1": {
            "email": "r1@lab.com",
            "name": "Dr. Smith",
            "password": stauth.Hasher(["Lab123!"]).generate()[0]
        }
    }
}

authenticator = stauth.Authenticate(
    users,
    "lab_app_cookie",
    "auth_key",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    
    # ========================
    # FORM SECTIONS
    # ========================
    with st.form("procedure_settings"):
        st.subheader("Procedure - Settings")
        num = st.text_input("#Num", "1-Infinity")
        date = st.date_input("Date")
        labeling = st.text_input("Labeling")
        protein_type = st.selectbox("Protein type", ["Type A", "Type B", "Type C"])
        concentration = st.number_input("Concentration [wt/wt%]")
        submit_settings = st.form_submit_button("Save Settings")

    with st.form("physical_treatments"):
        st.subheader("Procedure - Physical treatments")
        right_valve = st.number_input("Right valve [bar]", value=0.0)
        left_valve = st.number_input("Left valve 2 [bar]", value=0.0)
        temp_after_HPH = st.number_input("Temp after HPH [°C]", value=0.0)
        HPH_fraction = st.number_input("HPH fraction [%]", value=0.0)
        acid_name = st.text_input("Acid name")
        concentration_acid = st.number_input("Concentration [%]", value=0.0)
        submit_physical = st.form_submit_button("Save Physical Treatments")

    with st.form("enzymes_hydrolyzing"):
        st.subheader("Procedure - Enzymes Hydrolyzing")
        YN = st.selectbox("Y/N", ["Yes", "No"])
        enz_num = st.number_input("Enz num.", value=0.0)
        name_enz = st.selectbox("Name", ["Enzyme A", "Enzyme B"])
        concentration_enz = st.number_input("Concentration [%]", value=0.0)
        submit_hydrolyzing = st.form_submit_button("Save Enzymes Hydrolyzing")

    # ========================
    # DATA STORAGE & EXPORT
    # ========================
    if submit_settings or submit_physical or submit_hydrolyzing:
        if 'protocol_data' not in st.session_state:
            st.session_state.protocol_data = []
        
        st.session_state.protocol_data.append({
            "Procedure Settings": {
                "Num": num,
                "Date": date.strftime("%Y-%m-%d"),
                "Labeling": labeling,
                "Protein Type": protein_type,
                "Concentration": concentration
            },
            "Physical Treatments": {
                "Right Valve": right_valve,
                "Left Valve": left_valve,
                "Temp after HPH": temp_after_HPH,
                "HPH Fraction": HPH_fraction,
                "Acid Name": acid_name,
                "Concentration Acid": concentration_acid
            },
            "Enzymes Hydrolyzing": {
                "Y/N": YN,
                "Enz Num": enz_num,
                "Name": name_enz,
                "Concentration": concentration_enz
            }
        })
        st.success("Data saved successfully!")
    
    # Export to Excel
    if st.button("Export to Excel"):
        df = pd.DataFrame(st.session_state.protocol_data)
        df.to_excel("protocol_data.xlsx", index=False)
        with open("protocol_data.xlsx", "rb") as f:
            st.download_button(
                label="Download Excel file",
                data=f,
                file_name="protocol_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

elif authentication_status is False:
    st.error("Invalid credentials")
elif authentication_status is None:
    st.warning("Please log in to access the lab portal")
