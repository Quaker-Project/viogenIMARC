import streamlit as st 
import pandas as pd
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="GenderVio Police Risk System",
    page_icon="🚔",
    layout="wide"
)

# --- SYSTEM WARNING BANNER ---

st.markdown("""
<div style="
    background-color:#7f1d1d;
    color:white;
    padding:12px;
    border-radius:8px;
    text-align:center;
    font-weight:bold;
    margin-bottom:20px;
">
⚠️ SYSTEM NOTICE: We are experiencing unusual issues — Please excuse the inconvenience
</div>
""", unsafe_allow_html=True)

# --- STYLE ---

st.markdown("""
<style>
body {background-color:#0f172a;}
.main {background-color:#0f172a;color:white;}
h1,h2,h3 {color:#e5e7eb;}
.stButton>button {background-color:#dc2626;color:white;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---

if "interview_done" not in st.session_state:
    st.session_state.interview_done = False

if "audio1" not in st.session_state:
    st.session_state.audio1 = False

if "audio2" not in st.session_state:
    st.session_state.audio2 = False

if "audio3" not in st.session_state:
    st.session_state.audio3 = False

if "audio4" not in st.session_state:
    st.session_state.audio4 = False

if "last_case" not in st.session_state:
    st.session_state.last_case = "Case-001"

# --- HEADER ---

st.title("🚔 GenderVio Police Risk Assessment System")

st.markdown("""
Internal Police Tool — Gender Violence Risk Assessment

1️⃣ Define indicator weights  
2️⃣ Conduct victim interview  
3️⃣ Generate risk classification
""")

st.divider()

# --- SIDEBAR ---

st.sidebar.header("Case File")

victim = st.sidebar.text_input("Victim ID","Case-001")
officer = st.sidebar.text_input("Officer's Name")
location = st.sidebar.text_input("Police Unit")

st.sidebar.info("Training Simulation Mode")

# --- RESET AUDIOS ---

if st.session_state.last_case != victim:
    st.session_state.audio1 = False
    st.session_state.audio2 = False
    st.session_state.audio3 = False
    st.session_state.audio4 = False
    st.session_state.last_case = victim

# --- CASE AUDIO CONFIG ---

case_audios = {
"Case-001": {
"neighborA": "case1_vecinoA.mp3",
"neighborB": "case1_vecinaB.mp3",
"friend": "case1_amigo.mp3",
"doctor": "case1_medico.mp3"
},
"Case-002": {
"neighborA": "case2_vecinoA.mp3",
"neighborB": "case2_vecinaB.mp3",
"friend": "case2_amigo.mp3",
"doctor": "case2_medico.mp3"
},
"Case-003": {
"neighborA": "",
"neighborB": "",
"friend": "",
"doctor": ""
}
}

selected_case = case_audios.get(victim, case_audios["Case-001"])

# --- DATABASE ---

st.header("Police Intelligence Database")

aggressor_name = st.text_input("Search aggressor's name")

database = {
"Juan Martinez":{
"Criminal record":"No",
"Cautionary meassure":"No",
"Violence against others":"No"
},
"Alejandro Garcia":{
"Criminal record":"Intimate Partner Violence",
"Cautionary meassure":"Injunction for protection...",
"Violence against others":"In 2016, he threw a glass at a man"
},
"David Gold":{
"Criminal record":"Drug trafficking",
"Cautionary meassure":"No",
"Violence against others":"No"
}
}

if st.button("Search Police Records"):
    if aggressor_name in database:
        st.success("Record found")
        st.write(database[aggressor_name])
    else:
        st.warning("No police record found")

st.divider()

# --- INDICATORS ---

indicators = { ... }  # (NO CAMBIO NADA AQUÍ, usa el tuyo completo)

# --- FLATTEN ---

all_indicators = [q for cat in indicators for q in indicators[cat]]

# --- WEIGHTS ---

st.header("Step 1 — Indicator Weight Configuration")

weights = {}
for cat in indicators:
    with st.expander(cat):
        for q in indicators[cat]:
            weights[q] = st.slider(q,0,5,1)

# --- INTERVIEW ---

st.header("Step 2 — Victim Interview")

answers = {}
for cat in indicators:
    st.subheader(cat)
    cols = st.columns(2)
    i = 0
    for q,options in indicators[cat].items():
        with cols[i%2]:
            answers[q] = st.radio(q,options,horizontal=True)
        i += 1

# --- SCORE ---

def calculate_score():
    severity = {
        "None":0,"No":0,"Unknown":0,
        "Yes":1,
        "Mild":1,"Severe":2,"Very Severe":3,
        "Knife / sharp weapon":2,"Firearm":3,"Other object":2,
        "Mild threats":1,"Serious threats":2,"Threats of death/suicide":3,
        "Work problems":1,"Legal problems":1,"Both":2
    }
    score = 0
    for q in all_indicators:
        score += weights[q] * severity.get(answers[q],0)
    return score

# --- FIXED CLASSIFICATION ---

def classify(score):
    if score <= 40:
        return "LOW RISK"
    elif score <= 90:
        return "MEDIUM RISK"
    elif score <= 160:
        return "HIGH RISK"
    else:
        return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):

    st.session_state.interview_done = True

    score = calculate_score()
    risk = classify(score)

    col1,col2,col3 = st.columns(3)

    col1.metric("Risk Score",score)
    col2.metric("Risk Level",risk)
    col3.metric("Case ID",victim)

    if risk == "EXTREME RISK":
        st.error("⚠ Immediate protection measures required")
    elif risk == "HIGH RISK":
        st.warning("⚠ High monitoring recommended")
    elif risk == "MEDIUM RISK":
        st.info("Monitor situation and reassess regularly")
    else:
        st.success("No immediate protection measures required")

    data=[]
    for q in all_indicators:
        val = 1 if answers[q] not in ["No","None","Unknown"] else 0
        data.append([q,answers[q],weights[q],val*weights[q]])

    df = pd.DataFrame(data,columns=["Indicator","Answer","Weight","Contribution"])

    st.subheader("Indicator Contribution")
    st.dataframe(df,use_container_width=True)

# --- TESTIMONIES ---

st.divider()
st.header("Witness Testimonies")

if not st.session_state.interview_done:
    st.warning("Complete victim interview first")
else:
    if victim == "Case-003":
        st.warning("⚠ No witness testimonies available for this case")
        st.info("Officers must rely solely on victim statement")
    else:
        col1,col2 = st.columns(2)
        if col1.button("Request Neighbor A"):
            time.sleep(2)
            st.session_state.audio1=True
        if col1.button("Request Friend"):
            time.sleep(2)
            st.session_state.audio2=True
        if col2.button("Request Neighbor B"):
            time.sleep(2)
            st.session_state.audio3=True
        if col2.button("Request Doctor"):
            time.sleep(2)
            st.session_state.audio4=True

        if st.session_state.audio1:
            st.audio(selected_case["neighborA"])
        if st.session_state.audio2:
            st.audio(selected_case["friend"])
        if st.session_state.audio3:
            st.audio(selected_case["neighborB"])
        if st.session_state.audio4:
            st.audio(selected_case["doctor"])
