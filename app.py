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

victim = st.sidebar.text_input("Victim ID","Case-001")
officer = st.sidebar.text_input("Officer Name")
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

# --- SELECT CASE AUDIO ---

if victim in case_audios:
    selected_case = case_audios[victim]
else:
    selected_case = case_audios["Case-001"]

# --- POLICE DATABASE ---

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
"Cautionary meassure":"Injunction for protection. A prohibition on approaching the victim within 500 metres. Also prohibition on the possession and use of weapons",
"Violence against others":"In 2016, he threw a glass at a man outside a nightclub"
},

"Peter Gold":{
"Criminal record":"No",
"Cautionary meassure":"No",
"Violence against others":"No"
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

"History of Violence":{

"Psychological abuse (insults, humiliation)":["None","Mild","Severe","Very Severe","Unknown"],
"Physical violence":["None","Mild","Severe","Very Severe","Unknown"],
"Forced sexual activity":["None","Mild","Severe","Very Severe","Unknown"],
"Use of weapons or objects against the victim":["None","Knife / sharp weapon","Firearm","Other object","Unknown"],
"Threats or plans to harm victim":["None","Mild threats","Serious threats","Threats of death/suicide","Unknown"],
"Threats of suicide by the aggressor":["No","Yes"],
"Escalation of violence last 6 months":["No","Yes","Unknown"]

},

"Aggressor Characteristics":{

"Over the past 6 months, the aggressor has shown exaggerated jealousy or suspicion of infidelity":["No","Yes","Unknown"],
"Over the past 6 months, the aggressor has shown controlling behaviors":["No","Yes","Unknown"],
"Over the past 6 months, stalking behaviour":["No","Yes","Unknown"],
"Over the past 6 months, major stressors in the aggressor's life":["No","Work or economic problems","Legal problems","Both","Unknown"],
"Over the last year, the perpetrator has caused damage to property":["No","Yes","Unknown"],
"Over the last year, there have been reports of disrespect towards the authorities or their officers":["No","Yes","Unknown"],
"Over the last year, aggression against others":["No","Yes","Unknown"],
"Over the last year, threats against others":["No","Yes","Unknown"],
"The perpetrator has a criminal record and/or a police record":["No","Yes","Unknown"],
"There are prior or current violations (of precautionary measures or criminal orders)":["No","Yes","Unknown"],
"There are prior incidents of physical and/or sexual assaults":["No","Yes","Unknown"],
"There is a history of gender-based violence against other partner(s)":["No","Yes","Unknown"],
"The agressor has mental disorder":["No","Yes","Unknown"],
"He has suicidal ideation or a history of suicide attempts":["No","Yes","Unknown"],
"has some form of addiction or substance abuse (alcohol, drugs, or medication)":["No","Yes","Unknown"],
"Family domestic violence history or gender-based violence history":["No","Yes","Unknown"],
"Aggressor under 24":["No","Yes","Unknown"]

},

"Victim Vulnerability":{

"Victim illness or disability":["No","Yes","Unknown"],
"Victim suicidal thoughts":["No","Yes","Unknown"],
"Victim substance abuse":["No","Yes","Unknown"],
"Lack of social support":["No","Yes","Unknown"],
"Foreign victim":["No","Yes","Unknown"]

},

"Children Related Factors":{

"Minor children":["No","Yes","Unknown"],
"Threats against children":["No","Yes","Unknown"],
"Victim fears harm to children":["No","Yes","Unknown"]

},

"Aggravating Circumstances":{

"The victim has previously reported other perpetrators":["No","Yes","Unknown"],
"Reciprocal violence":["No","Yes","Unknown"],
"The victim has told the aggressor of their intention to end the relationship within the past 6 months":["No","Yes","Unknown"],
"The victim believes that the aggressor is capable of seriously assaulting her or even killing her":["No","Yes","Unknown"]

}

}

# --- FLATTEN LIST ---

all_indicators=[]

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

    st.subheader(cat)

    cols=st.columns(2)

    i=0

    for q,options in indicators[cat].items():

        with cols[i%2]:

            answers[q]=st.radio(q,options,horizontal=True)

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

    score=0

    for q in all_indicators:

        multiplier=severity.get(answers[q],0)
        score+=weights[q]*multiplier

    return score


def classify(score):

    if score<=25:
        return "LOW RISK"
    elif score<=60:
        return "MEDIUM RISK"
    elif score<=110:
        return "HIGH RISK"
    else:
        return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):

    st.session_state.interview_done=True

    score=calculate_score()
    risk=classify(score)

    col1,col2,col3=st.columns(3)

    with col1:
        st.metric("Risk Score",score)

    with col2:
        st.metric("Risk Level",risk)

    with col3:
        st.metric("Case ID",victim)

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

        val=1 if answers[q] not in ["No","None","Unknown"] else 0

        data.append([q,answers[q],weights[q],val*weights[q]])

    df=pd.DataFrame(data,columns=["Indicator","Answer","Weight","Contribution"])

    st.subheader("Indicator Contribution")

    st.dataframe(df,use_container_width=True)

st.divider()

# --- TESTIMONIES ---

st.header("Witness Testimonies")

if not st.session_state.interview_done:

    st.warning("Complete victim interview first")

else:

    if victim == "Case-003":

        st.session_state.audio1 = False
        st.session_state.audio2 = False
        st.session_state.audio3 = False
        st.session_state.audio4 = False

        st.warning("⚠ No witness testimonies available for this case")
        st.info("Officers must rely solely on victim statement and available records")

    else:

        col1,col2=st.columns(2)

        with col1:

            if st.button("Request Neighbor A"):
                with st.spinner("Contacting witness..."):
                    time.sleep(15)
                st.session_state.audio1=True

            if st.button("Request Friend"):
                with st.spinner("Contacting witness..."):
                    time.sleep(25)
                st.session_state.audio2=True

        with col2:

            if st.button("Request Neighbor B"):
                with st.spinner("Contacting witness..."):
                    time.sleep(30)
                st.session_state.audio3=True

            if st.button("Request Doctor"):
                with st.spinner("Requesting medical record..."):
                    time.sleep(10)
                st.session_state.audio4=True

        if st.session_state.audio1:
            st.audio(selected_case["neighborA"])

        if st.session_state.audio2:
            st.audio(selected_case["friend"])

        if st.session_state.audio3:
            st.audio(selected_case["neighborB"])

        if st.session_state.audio4:
            st.audio(selected_case["doctor"])

st.divider()

# --- INFORMATION REQUEST ---

st.header("Inter-Agency Information Requests")

team_email=st.text_input("Police team email")

institution=st.selectbox("Request information from",[
"Social Services",
"Medical Services",
"Police Intelligence Unit",
"School Administration"
])

if st.button("Send Information Request"):

    if team_email=="":
        st.warning("Enter email")

    else:

        url="https://formspree.io/f/xgonleql"

        data={
        "email":team_email,
        "institution":institution,
        "case":victim,
        "officer":officer,
        "location":location,
        "time":datetime.now().isoformat()
        }

        requests.post(url,data=data)

        st.success("Request sent")
