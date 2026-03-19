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
4️⃣ Reassess after new information
""")

st.divider()

# --- SIDEBAR ---

st.sidebar.header("Case File")

victim = st.sidebar.text_input("Victim ID","Case-001")
officer = st.sidebar.text_input("Officer Name")
location = st.sidebar.text_input("Police Unit")

st.sidebar.info("Training Simulation Mode")

# --- RESET AUDIO WHEN CASE CHANGES ---

if st.session_state.last_case != victim:
    st.session_state.audio1 = False
    st.session_state.audio2 = False
    st.session_state.audio3 = False
    st.session_state.audio4 = False
    st.session_state.interview_done = False
    st.session_state.last_case = victim

# --- CASE AUDIO FILES ---

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

# --- POLICE DATABASE ---

st.header("Police Intelligence Database")

aggressor_name = st.text_input("Search aggressor's name")

database = {

"Juan Martinez":{
"Criminal record":"No",
"Cautionary measure":"No",
"Violence against others":"No"
},

"Alejandro Garcia":{
"Criminal record":"Intimate Partner Violence",
"Cautionary measure":"Protection order: no approach within 500m + no weapons",
"Violence against others":"2016 nightclub assault"
},

"Ahmed Hassan":{
"Criminal record":"No",
"Cautionary measure":"No",
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

indicators = {
"History of Violence":{
"Psychological abuse":["None","Mild","Severe","Very Severe","Unknown"],
"Physical violence":["None","Mild","Severe","Very Severe","Unknown"],
"Sexual violence":["None","Mild","Severe","Very Severe","Unknown"],
"Use of weapons":["None","Knife / sharp weapon","Firearm","Other object","Unknown"],
"Threats":["None","Mild threats","Serious threats","Threats of death/suicide","Unknown"],
"Suicide threats":["No","Yes"],
"Escalation":["No","Yes","Unknown"]
},
"Aggressor Characteristics":{
"Jealousy":["No","Yes","Unknown"],
"Control":["No","Yes","Unknown"],
"Stalking":["No","Yes","Unknown"],
"Stressors":["No","Work problems","Legal problems","Both","Unknown"],
"Property damage":["No","Yes","Unknown"],
"Disrespect police":["No","Yes","Unknown"],
"Aggression others":["No","Yes","Unknown"],
"Threats others":["No","Yes","Unknown"],
"Criminal record":["No","Yes","Unknown"],
"Order violations":["No","Yes","Unknown"],
"Previous assaults":["No","Yes","Unknown"],
"Violence history":["No","Yes","Unknown"],
"Mental disorder":["No","Yes","Unknown"],
"Suicidal behaviour":["No","Yes","Unknown"],
"Substance abuse":["No","Yes","Unknown"],
"Family violence":["No","Yes","Unknown"],
"Under 24":["No","Yes","Unknown"]
},
"Victim Vulnerability":{
"Illness":["No","Yes","Unknown"],
"Suicidal thoughts":["No","Yes","Unknown"],
"Substance abuse":["No","Yes","Unknown"],
"Isolation":["No","Yes","Unknown"],
"Foreign":["No","Yes","Unknown"]
},
"Children":{
"Children":["No","Yes","Unknown"],
"Threats children":["No","Yes","Unknown"],
"Fear children":["No","Yes","Unknown"]
},
"Aggravating":{
"Previous reports":["No","Yes","Unknown"],
"Reciprocal violence":["No","Yes","Unknown"],
"Separation attempt":["No","Yes","Unknown"],
"Fear of homicide":["No","Yes","Unknown"]
}
}

# --- FLATTEN ---

all_indicators = [q for cat in indicators for q in indicators[cat]]

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
    st.subheader(cat)
    cols=st.columns(2)
    i=0
    for q,opts in indicators[cat].items():
        with cols[i%2]:
            answers[q]=st.radio(q,opts,horizontal=True)
        i+=1

# --- SCORE ---

def calculate_score():
    severity={
"None":0,"No":0,"Unknown":0,
"Yes":1,
"Mild":1,"Severe":2,"Very Severe":3,
"Knife / sharp weapon":2,"Firearm":3,"Other object":2,
"Mild threats":1,"Serious threats":2,"Threats of death/suicide":3,
"Work problems":1,"Legal problems":1,"Both":2
}
    return sum(weights[q]*severity.get(answers[q],0) for q in all_indicators)

def classify(score):
    if score<=10: return "LOW RISK"
    elif score<=20: return "MEDIUM RISK"
    elif score<=30: return "HIGH RISK"
    else: return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):
    st.session_state.interview_done=True

    score=calculate_score()
    risk=classify(score)

    st.metric("Risk Score",score)
    st.metric("Risk Level",risk)

    if risk=="EXTREME RISK":
        st.error("Immediate protection required")
    elif risk=="HIGH RISK":
        st.warning("High monitoring")
    elif risk=="MEDIUM RISK":
        st.info("Monitor situation")
    else:
        st.success("Low risk")

st.divider()

# --- TESTIMONIES ---

st.header("Witness Testimonies")

if not st.session_state.interview_done:
    st.warning("Generate risk assessment first")

else:

    if victim=="Case-003":
        st.warning("No witness testimonies available")

    else:

        st.success("Testimonies unlocked")

        if st.button("Request Neighbor A"):
            time.sleep(2)
            st.session_state.audio1=True

        if st.session_state.audio1:
            st.audio(selected_case["neighborA"])

        if st.button("Request Friend"):
            time.sleep(2)
            st.session_state.audio2=True

        if st.session_state.audio2:
            st.audio(selected_case["friend"])

# --- REASSESS ---

st.divider()

st.header("Reassessment")

if st.button("🔄 Reassess Risk After New Information"):

    score=calculate_score()
    risk=classify(score)

    st.metric("Updated Score",score)
    st.metric("Updated Risk",risk)

    st.info("Discuss whether new information justifies changing risk level")

# --- REQUESTS ---

st.divider()

st.header("Inter-Agency Information Requests")

email=st.text_input("Email")

if st.button("Send Request"):
    requests.post("https://formspree.io/f/xgonleql",data={"email":email})
    st.success("Request sent")
