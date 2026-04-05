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

victim = st.sidebar.text_input("Victim ID", "Case-001")
officer = st.sidebar.text_input("Officer's Name")
location = st.sidebar.text_input("Police Unit")

st.sidebar.info("Training Simulation Mode")

# --- RESET AUDIOS WHEN CASE CHANGES ---

if st.session_state.last_case != victim:
    st.session_state.audio1 = False
    st.session_state.audio2 = False
    st.session_state.audio3 = False
    st.session_state.audio4 = False
    st.session_state.last_case = victim

# --- CASE AUDIO CONFIGURATION ---

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

if victim in case_audios:
    selected_case = case_audios[victim]
else:
    selected_case = case_audios["Case-001"]

# --- POLICE DATABASE ---

st.header("Police Intelligence Database")

aggressor_name = st.text_input("Search aggressor's name")

database = {
    "Juan Martinez": {
        "Criminal record": "No",
        "Cautionary meassure": "No",
        "Violence against others": "No"
    },
    "Alejandro Garcia": {
        "Criminal record": "Intimate Partner Violence",
        "Cautionary meassure": "Injunction for protection. A prohibition on approaching the victim within 500 metres. Also prohibition on the possession and use of weapons",
        "Violence against others": "In 2016, he threw a glass at a man outside a nightclub"
    },
    "David Gold": {
        "Criminal record": "Drug trafficking. In 2025, he was caught with 250 grams of hashish in the boot of his car.",
        "Cautionary meassure": "No",
        "Violence against others": "No"
    }
}

if st.button("Search Police Records"):
    if aggressor_name in database:
        record = database[aggressor_name]
        st.success("Record found")
        st.write(record)
    else:
        st.warning("No police record found")

st.divider()

# --- INDICATORS ---

indicators = {
    "History of Violence": {
        "Psychological abuse (insults, humiliation)": ["None","Mild","Severe","Very Severe","Unknown"],
        "Physical violence": ["None","Mild","Severe","Very Severe","Unknown"]
    }
}

# --- FLATTEN LIST ---

all_indicators = []
for cat in indicators:
    for q in indicators[cat]:
        all_indicators.append(q)

# --- WEIGHTS ---

st.header("Step 1 — Indicator Weight Configuration")

weights = {}

for cat in indicators:
    with st.expander(cat):
        for q in indicators[cat]:
            weights[q] = st.slider(q, 0, 5, 1)

# --- INTERVIEW ---

st.header("Step 2 — Victim Interview")

answers = {}

for cat in indicators:
    st.subheader(cat)
    for q, options in indicators[cat].items():
        answers[q] = st.radio(q, options)

# --- SCORE ---

def calculate_score():
    severity = {
        "None":0,"No":0,"Unknown":0,
        "Yes":1,"Mild":1,"Severe":2,"Very Severe":3
    }
    score = 0
    for q in all_indicators:
        multiplier = severity.get(answers[q], 0)
        score += weights[q] * multiplier
    return score

def classify(score):
    if score <= 25:
        return "LOW RISK"
    elif score <= 60:
        return "MEDIUM RISK"
    elif score <= 110:
        return "HIGH RISK"
    else:
        return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):
    st.session_state.interview_done = True

    score = calculate_score()
    risk = classify(score)

    st.metric("Risk Score", score)
    st.metric("Risk Level", risk)

st.divider()

# --- TESTIMONIES ---

st.header("Witness Testimonies")

if not st.session_state.interview_done:
    st.warning("Complete victim interview first")
else:
    if victim == "Case-003":
        st.warning("⚠ No witness testimonies available for this case")
    else:
        if st.button("Request Neighbor A"):
            st.audio(selected_case["neighborA"])

st.divider()

# --- PEER REVIEW ---

st.header("📄 Risk Justification Exchange")

group = st.selectbox("Select your group:", ["Group A","Group B"])

group_a_link = "https://drive.google.com/drive/folders/1DL3-WunHe6-x0DVDp7HyEliSHA7b9Csg"
group_b_link = "https://drive.google.com/drive/folders/1RON9R9DX7e0VK95QmNYLBp-lWrv9W0KB"

if group == "Group A":
    st.markdown(f"[Open Group A Folder]({group_a_link})")
    st.markdown(f"[Open Group B Folder]({group_b_link})")
else:
    st.markdown(f"[Open Group B Folder]({group_b_link})")
    st.markdown(f"[Open Group A Folder]({group_a_link})")
