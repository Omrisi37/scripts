# %%writefile app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ========================
# FORM SECTIONS
# ========================

with st.form("procedure_settings"):
    st.subheader("Procedure - Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        num = st.text_input("#Num", "1-Infinity")
    with col2:
        date = st.date_input("Date")
    with col3:
        labeling = st.text_input("Labeling")
    protein_type = st.selectbox("Protein type", ["Type A", "Type B", "Type C"])
    concentration = st.number_input("Concentration [wt/wt%]")
    submit_settings = st.form_submit_button("Save Settings")

with st.form("physical_treatments"):
    st.subheader("Procedure - Physical treatments")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        right_valve = st.number_input("right valve [bar]", value=0.0)
    with col2:
        left_valve = st.number_input("left valve 2 [bar]", value=0.0)
    with col3:
        temp_after_HPH = st.number_input("Temp after HPH [°C]", value=0.0)
    with col4:
        HPH_fraction = st.number_input("HPH fraction [%]", value=0.0)
    
    col5, col6 = st.columns(2)
    with col5:
        acid_name = st.text_input("Acid name")
    with col6:
        concentration_acid = st.number_input("Concentration [%]", value=0.0)
    
    mixing_temp = st.number_input("Mixing temp[°C]", value=0.0)
    mixing_time = st.number_input("Mixing time", value=0.0)
    heat_treatment_fraction = st.number_input("Heat treatment fraction[%]", value=0.0)
    pH = st.number_input("pH", value=7.0)
    
    initial_water_temp = st.number_input("Initial water temp", value=0.0)
    
    submit_physical = st.form_submit_button("Save Physical Treatments")

with st.form("enzymes_hydrolyzing"):
    st.subheader("Black box ? + Procedure - Enzymes Hydrolyzing")
    YN = st.selectbox("Y/N", ["Yes", "No"])
    col1, col2 = st.columns(2)
    with col1:
        enz_num = st.number_input("Enz num.", value=0.0)
    with col2:
        name_enz = st.selectbox("Name", ["Enzyme A", "Enzyme B"])
    concentration_enz = st.number_input("Concentration [%]", value=0.0)
    added_enz = st.number_input("Added enz [g]", value=0.0)
    addition_temp = st.number_input("Addition temp [°C]", value=0.0)
    ino_time = st.number_input("Ino. time [min]", value=0.0)
    ino_temp = st.number_input("Ino. temp. [°C]", value=0.0)
    stirring = st.number_input("stirring [RPM]", value=0.0)
    
    black_box_protein_fraction = st.number_input("black box protein fraction[%]", value=0.0)
    
    submit_hydrolyzing = st.form_submit_button("Save Enzymes Hydrolyzing")

with st.form("enzymes_crosslinking"):
    st.subheader("Procedure - Enzymes Crosslinking")
    col1, col2 = st.columns(2)
    with col1:
        enz_num_cross = st.number_input("Enz num.", value=0.0)
    with col2:
        name_enz_cross = st.selectbox("Name", ["Crosslinker X", "Crosslinker Y"])
    concentration_enz_cross = st.number_input("Concentration [%]", value=0.0)
    added_enz_cross = st.number_input("Added enz [g]", value=0.0)
    addition_temp_cross = st.number_input("Addition temp [°C]", value=0.0)
    ino_time_cross = st.number_input("Ino. time [min]", value=0.0)
    ino_temp_cross = st.number_input("Ino. temp. [°C]", value=0.0)
    stirring_cross = st.number_input("stirring [RPM]", value=0.0)
    
    submit_crosslinking = st.form_submit_button("Save Enzymes Crosslinking")

# ========================
# DATA STORAGE AND EXPORT
# ========================

if submit_settings or submit_physical or submit_hydrolyzing or submit_crosslinking:
    data = {
        "Procedure Settings": {
            "Num": num,
            "Date": date.strftime("%Y-%m-%d"),
            "Labeling": labeling,
            "Protein type": protein_type,
            "Concentration": concentration
        },
        "Physical Treatments": {
            "Right Valve": right_valve,
            "Left Valve": left_valve,
            "Temp after HPH": temp_after_HPH,
            "HPH Fraction": HPH_fraction,
            "Acid Name": acid_name,
            "Concentration Acid": concentration_acid,
            "Mixing Temp": mixing_temp,
            "Mixing Time": mixing_time,
            "Heat Treatment Fraction": heat_treatment_fraction,
            "pH": pH,
            "Initial Water Temp": initial_water_temp
        },
        "Enzymes Hydrolyzing": {
            "Y/N": YN,
            "Enz Num": enz_num,
            "Name": name_enz,
            "Concentration": concentration_enz,
            "Added Enz": added_enz,
            "Addition Temp": addition_temp,
            "Ino. Time": ino_time,
            "Ino. Temp": ino_temp,
            "Stirring": stirring,
            "Black Box Protein Fraction": black_box_protein_fraction
        },
        "Enzymes Crosslinking": {
            "Enz Num": enz_num_cross,
            "Name": name_enz_cross,
            "Concentration": concentration_enz_cross,
            "Added Enz": added_enz_cross,
            "Addition Temp": addition_temp_cross,
            "Ino. Time": ino_time_cross,
            "Ino. Temp": ino_temp_cross,
            "Stirring": stirring_cross
        }
    }

    # Store to session state
    if 'protocol_data' not in st.session_state:
        st.session_state.protocol_data = []
    st.session_state.protocol_data.append(data)
    st.success("Data saved successfully!")

# ========================
# EXPORT TO EXCEL
# ========================
if st.button("Export to Excel"):
    # Create DataFrame
    df = pd.DataFrame(st.session_state.protocol_data)
    df = df.transpose()  # Transpose for a more readable format
    
    # Convert dictionary-like columns to string representation
    for col in df.columns:
        if isinstance(df[col].iloc[0], dict):
            df[col] = df[col].apply(lambda x: str(x))

    # Export to Excel
    df.to_excel("protocol_data.xlsx")

    # Download button
    st.download_button(
        label="Download Excel file",
        data=open("protocol_data.xlsx", "rb").read(),
        file_name="protocol_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
