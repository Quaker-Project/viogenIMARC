import streamlit as st
import pandas as pd

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

# --- HEADER ---

st.title("🚔 VioGén Police Risk Assessment System")

st.markdown("""
Internal Police Tool — Gender Violence Risk Assessment

1️⃣ Define indicator weights  
2️⃣ Conduct victim interview  
3️⃣ Generate risk classification
""")

st.divider()

# --- POLICE DATABASE LOOKUP ---

st.header("Police Intelligence Database")

aggressor_name = st.text_input("Search aggressor name")

police_database = {

"Juan Martinez": {
"Criminal record": "Yes",
"Substance abuse": "Alcohol abuse",
"Previous restraining order": "Yes",
"Violence against others": "Yes",
"Notes": "Previous arrest for assault (2019)"
},

"David Lopez": {
"Criminal record": "No",
"Substance abuse": "No known issues",
"Previous restraining order": "No",
"Violence against others": "No",
"Notes": "No police incidents recorded"
},

"Ahmed Hassan": {
"Criminal record": "Yes",
"Substance abuse": "Drug use suspected",
"Previous restraining order": "Unknown",
"Violence against others": "Yes",
"Notes": "Police intervention for street fight (2022)"
}

}

if st.button("Search Police Records"):

    if aggressor_name in police_database:

        record = police_database[aggressor_name]

        st.success("Record found")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Criminal record:**", record["Criminal record"])
            st.write("**Substance abuse:**", record["Substance abuse"])

        with col2:
            st.write("**Previous restraining order:**", record["Previous restraining order"])
            st.write("**Violence against others:**", record["Violence against others"])

        st.write("**Notes:**", record["Notes"])

    else:

        st.warning("No police records found for this individual")

st.divider()

# --- INDICATORS ---

indicators = {

"History of Violence": {

"Psychological abuse (insults, humiliation)": ["None","Mild","Severe","Very Severe","Unknown"],
"Physical violence": ["None","Mild","Severe","Very Severe","Unknown"],
"Forced sexual activity": ["None","Mild","Severe","Very Severe","Unknown"],

"Use of weapons against victim": [
"None","Knife / sharp weapon","Firearm","Other object","Unknown"
],

"Threats or plans to harm the victim": [
"None","Mild threats","Serious threats","Threats of death/suicide","Unknown"
],

"Escalation of violence in last 6 months": ["No","Yes","Unknown"]

},

"Aggressor Characteristics": {

"Extreme jealousy or suspicions of infidelity": ["No","Yes","Unknown"],
"Controlling behaviour": ["No","Yes","Unknown"],
"Stalking or harassment behaviour": ["No","Yes","Unknown"],

"Aggressor experienced major stressors in last 6 months": [
"No","Work/financial problems","Legal problems","Both","Unknown"
],

"Property damage by aggressor in last year": ["No","Yes","Unknown"],
"Disrespect toward police or authorities": ["No","Yes","Unknown"],
"Aggression toward third persons or animals": ["No","Yes","Unknown"],
"Threats or insults toward third parties": ["No","Yes","Unknown"],
"Criminal or police record": ["No","Yes","Unknown"],
"Previous restraining order violations": ["No","Yes","Unknown"],
"Previous physical or sexual assaults": ["No","Yes","Unknown"],
"Gender violence against previous partners": ["No","Yes","Unknown"],
"Mental or psychiatric disorder": ["No","Yes","Unknown"],
"Suicidal ideation or attempts": ["No","Yes","Unknown"],
"Substance abuse": ["No","Yes","Unknown"],
"Family history of domestic violence": ["No","Yes","Unknown"],
"Aggressor under 24 years old": ["No","Yes","Unknown"]

},

"Victim Vulnerability": {

"Victim has serious illness or disability": ["No","Yes","Unknown"],
"Victim suicidal thoughts or attempts": ["No","Yes","Unknown"],
"Victim substance abuse": ["No","Yes","Unknown"],
"Lack of social or family support": ["No","Yes","Unknown"],
"Foreign victim": ["No","Yes","Unknown"]

},

"Children Related Factors": {

"Victim has minor children": ["No","Yes","Unknown"],
"Threats against children": ["No","Yes","Unknown"],
"Victim fears harm to children": ["No","Yes","Unknown"]

},

"Aggravating Circumstances": {

"Victim previously reported other aggressors": ["No","Yes","Unknown"],
"Reciprocal or lateral violence between partners": ["No","Yes","Unknown"],
"Victim expressed intention to end relationship in last 6 months": ["No","Yes","Unknown"],
"Victim believes aggressor could seriously harm or kill her": ["No","Yes","Unknown"]

}

}

# --- FLATTEN INDICATORS ---

all_indicators = []

for cat in indicators:
    for q in indicators[cat]:
        all_indicators.append(q)

# --- SIDEBAR ---

st.sidebar.header("Case File")

victim = st.sidebar.text_input("Victim ID","Case-001")
officer = st.sidebar.text_input("Officer Name")
location = st.sidebar.text_input("Police Unit")

st.sidebar.info("Training Simulation Mode")

# --- STEP 1 WEIGHTS ---

st.header("Step 1 — Indicator Weight Configuration")

weights = {}

for cat in indicators:

    with st.expander(cat):

        for q in indicators[cat]:

            weights[q] = st.slider(q,0,5,1)

# --- STEP 2 INTERVIEW ---

st.header("Step 2 — Victim Interview")

answers = {}

for cat in indicators:

    st.subheader(cat)

    cols = st.columns(2)

    i = 0

    for q,options in indicators[cat].items():

        with cols[i % 2]:

            answers[q] = st.radio(
                q,
                options,
                horizontal=True
            )

        i += 1

# --- SCORE CALCULATION ---

def calculate_score():

    severity_multiplier = {

    "None":0,
    "No":0,
    "Unknown":0,

    "Yes":1,

    "Mild":1,
    "Severe":2,
    "Very Severe":3,

    "Knife / sharp weapon":2,
    "Firearm":3,
    "Other object":2,

    "Mild threats":1,
    "Serious threats":2,
    "Threats of death/suicide":3,

    "Work/financial problems":1,
    "Legal problems":1,
    "Both":2

    }

    score = 0

    for q in all_indicators:

        answer = answers[q]

        multiplier = severity_multiplier.get(answer,0)

        score += weights[q] * multiplier

    return score


def classify(score):

    if score <= 10:
        return "LOW RISK"
    elif score <= 20:
        return "MEDIUM RISK"
    elif score <= 30:
        return "HIGH RISK"
    else:
        return "EXTREME RISK"

# --- ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):

    score = calculate_score()
    risk = classify(score)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Risk Score",score)

    with col2:
        st.metric("Risk Level",risk)

    with col3:
        st.metric("Case ID",victim)

    if risk == "EXTREME RISK":
        st.error("⚠ Immediate protection measures recommended")

    elif risk == "HIGH RISK":
        st.warning("⚠ High monitoring recommended")

    elif risk == "MEDIUM RISK":
        st.info("Monitor situation")

    else:
        st.success("No immediate protection measures required")

    data = []

    severity_multiplier = {
        "None":0,"No":0,"Unknown":0,
        "Yes":1,
        "Mild":1,"Severe":2,"Very Severe":3,
        "Knife / sharp weapon":2,"Firearm":3,"Other object":2,
        "Mild threats":1,"Serious threats":2,"Threats of death/suicide":3,
        "Work/financial problems":1,"Legal problems":1,"Both":2
    }

    for q in all_indicators:

        answer = answers[q]
        multiplier = severity_multiplier.get(answer,0)

        contribution = weights[q] * multiplier

        data.append([
            q,
            answer,
            weights[q],
            contribution
        ])

    df = pd.DataFrame(data,columns=[
        "Indicator",
        "Answer",
        "Weight",
        "Contribution"
    ])

    st.subheader("Indicator Contribution")

    st.dataframe(df,use_container_width=True)
