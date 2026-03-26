import streamlit as st 
import pandas as pd
import requests
import time
from datetime import datetime
from docx import Document
from docx.shared import Inches
from io import BytesIO

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
4️⃣ Peer review exchange
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

# --- AUDIO CONFIG ---

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
"Juan Martinez":{"Criminal record":"No","Cautionary meassure":"No","Violence against others":"No"},
"Alejandro Garcia":{"Criminal record":"Intimate Partner Violence","Cautionary meassure":"Restraining order","Violence against others":"Yes"},
"David Gold":{"Criminal record":"Drug trafficking","Cautionary meassure":"No","Violence against others":"No"}
}

if st.button("Search Police Records"):
    if aggressor_name in database:
        st.success("Record found")
        st.write(database[aggressor_name])
    else:
        st.warning("No police record found")

st.divider()

# --- INDICATORS (igual que tenías) ---

indicators = {
"History of Violence":{
"Psychological abuse (insults, humiliation)":["None","Mild","Severe","Very Severe","Unknown"],
"Physical violence":["None","Mild","Severe","Very Severe","Unknown"],
"Forced sexual activity":["None","Mild","Severe","Very Severe","Unknown"],
"Use of weapons":["None","Knife / sharp weapon","Firearm","Other object","Unknown"],
"Threats":["None","Mild threats","Serious threats","Threats of death/suicide","Unknown"],
"Escalation":["No","Yes","Unknown"]
}
}

# --- FLATTEN ---

all_indicators = []
for cat in indicators:
    for q in indicators[cat]:
        all_indicators.append(q)

# --- WEIGHTS ---

st.header("Step 1 — Indicator Weight Configuration")

weights={}
for cat in indicators:
    with st.expander(cat):
        for q in indicators[cat]:
            weights[q]=st.slider(q,0,5,1)

# --- INTERVIEW ---

st.header("Step 2 — Victim Interview")

answers={}
for cat in indicators:
    for q,options in indicators[cat].items():
        answers[q]=st.radio(q,options,horizontal=True)

# --- SCORE ---

def calculate_score():
    severity={"None":0,"No":0,"Unknown":0,"Yes":1,"Mild":1,"Severe":2,"Very Severe":3}
    score=0
    for q in all_indicators:
        score+=weights[q]*severity.get(answers[q],0)
    return score

def classify(score):
    if score<=40: return "LOW RISK"
    elif score<=90: return "MEDIUM RISK"
    elif score<=160: return "HIGH RISK"
    else: return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):
    st.session_state.interview_done=True
    score=calculate_score()
    risk=classify(score)

    st.metric("Risk Score",score)
    st.metric("Risk Level",risk)

# --- TESTIMONIES ---

st.divider()
st.header("Witness Testimonies")

if not st.session_state.interview_done:
    st.warning("Complete interview first")
else:
    if victim=="Case-003":
        st.warning("⚠ No witness testimonies available")
    else:
        if st.button("Request Neighbor A"):
            st.session_state.audio1=True
        if st.session_state.audio1:
            st.audio(selected_case["neighborA"])

# ================================
# 🔥 PEER REVIEW SECTION
# ================================

st.divider()
st.header("📄 Risk Justification Exchange")

group = st.selectbox("Select your group:", ["Group A","Group B"])

group_a_link = "https://drive.google.com/drive/folders/1DL3-WunHe6-x0DVDp7HyEliSHA7b9Csg?usp=sharing"
group_b_link = "https://drive.google.com/drive/folders/1RON9R9DX7e0VK95QmNYLBp-lWrv9W0KB?usp=sharing"

if group == "Group A":
    st.subheader("📤 Upload your report")
    st.markdown(f"[Open Group A Folder]({group_a_link})")
    st.subheader("📥 Review Group B reports")
    st.markdown(f"[Open Group B Folder]({group_b_link})")
else:
    st.subheader("📤 Upload your report")
    st.markdown(f"[Open Group B Folder]({group_b_link})")
    st.subheader("📥 Review Group A reports")
    st.markdown(f"[Open Group A Folder]({group_a_link})")

# --- WORD GENERATOR ---

st.subheader("🧠 Peer Review")

peer_review = st.text_area("Your review")

if st.button("Generate Word Review"):

    doc = Document()

    unit = location.strip().upper()

    if unit == "CNP":
        doc.add_picture("assets/cnp_logo.png", width=Inches(1.5))
        doc.add_heading('SPANISH NATIONAL POLICE', 1)
    elif unit == "GC":
        doc.add_picture("assets/gc_logo.png", width=Inches(1.5))
        doc.add_heading('GUARDIA CIVIL', 1)
    else:
        doc.add_heading('MINISTRY OF INTERIOR', 1)

    doc.add_paragraph('Risk Assessment Peer Review Unit')

    doc.add_heading('Case Information', level=2)
    doc.add_paragraph(f"Group: {group}")
    doc.add_paragraph(f"Case: {victim}")
    doc.add_paragraph(f"Officer: {officer}")

    doc.add_heading('Assessment', level=2)
    doc.add_paragraph(peer_review)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Download Word",
        data=buffer,
        file_name=f"{group}_{victim}.docx"
    )
