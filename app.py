import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="VioGén Police Risk System",
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


# --- HEADER ---

st.title("🚔 VioGén Police Risk Assessment System")

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

# --- POLICE DATABASE ---

st.header("Police Intelligence Database")

aggressor_name = st.text_input("Search aggressor name")

database = {

"Juan Martinez":{
"Criminal record":"Yes",
"Substance abuse":"Alcohol abuse",
"Restraining order":"Yes",
"Violence against others":"Yes"
},

"David Lopez":{
"Criminal record":"No",
"Substance abuse":"None",
"Restraining order":"No",
"Violence against others":"No"
},

"Ahmed Hassan":{
"Criminal record":"Yes",
"Substance abuse":"Drug use suspected",
"Restraining order":"Unknown",
"Violence against others":"Yes"
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
"Use of weapons against victim":["None","Knife / sharp weapon","Firearm","Other object","Unknown"],
"Threats or plans to harm victim":["None","Mild threats","Serious threats","Threats of death/suicide","Unknown"],
"Escalation of violence last 6 months":["No","Yes","Unknown"]

},

"Aggressor Characteristics":{

"Extreme jealousy":["No","Yes","Unknown"],
"Controlling behaviour":["No","Yes","Unknown"],
"Stalking behaviour":["No","Yes","Unknown"],
"Major stressors last 6 months":["No","Work problems","Legal problems","Both","Unknown"],
"Property damage last year":["No","Yes","Unknown"],
"Disrespect toward authorities":["No","Yes","Unknown"],
"Aggression against others":["No","Yes","Unknown"],
"Threats against others":["No","Yes","Unknown"],
"Criminal record":["No","Yes","Unknown"],
"Restraining order violations":["No","Yes","Unknown"],
"Previous assaults":["No","Yes","Unknown"],
"Violence against previous partners":["No","Yes","Unknown"],
"Mental disorder":["No","Yes","Unknown"],
"Suicidal behaviour":["No","Yes","Unknown"],
"Substance abuse":["No","Yes","Unknown"],
"Family violence history":["No","Yes","Unknown"],
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

"Previous reports":["No","Yes","Unknown"],
"Reciprocal violence":["No","Yes","Unknown"],
"Victim planning separation":["No","Yes","Unknown"],
"Victim fears homicide":["No","Yes","Unknown"]

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

    if score<=10:
        return "LOW RISK"
    elif score<=20:
        return "MEDIUM RISK"
    elif score<=30:
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

    # --- POLICE RESPONSE MESSAGE ---

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

    col1,col2=st.columns(2)

    with col1:

        if st.button("Request Neighbor A"):
            with st.spinner("Contacting witness..."):
                time.sleep(3)
            st.session_state.audio1=True

        if st.button("Request Friend"):
            with st.spinner("Contacting witness..."):
                time.sleep(3)
            st.session_state.audio2=True

    with col2:

        if st.button("Request Neighbor B"):
            with st.spinner("Contacting witness..."):
                time.sleep(3)
            st.session_state.audio3=True

        if st.button("Request Doctor"):
            with st.spinner("Requesting medical record..."):
                time.sleep(4)
            st.session_state.audio4=True

    if st.session_state.audio1:
        st.audio("VECINO A.mp3")

    if st.session_state.audio2:
        st.audio("Amigo de la familia.mp3")

    if st.session_state.audio3:
        st.audio("VECINA B.mp3")

    if st.session_state.audio4:
        st.audio("MEDICO.mp3")

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
