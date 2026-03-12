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

body {
background-color: #0f172a;
}

.main {
background-color: #0f172a;
color: white;
}

h1, h2, h3 {
color:#e5e7eb;
}

.stButton>button {
background-color:#dc2626;
color:white;
font-weight:bold;
border-radius:6px;
}

[data-testid="stMetricValue"] {
font-size:30px;
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---

st.title("🚔 VioGén Police Risk Assessment System")

st.markdown("""
Internal Police Tool — Gender Violence Risk Assessment

**Procedure**

1️⃣ Define **indicator weights**

2️⃣ Conduct **victim interview**

3️⃣ Generate **risk classification**
""")

st.divider()

# --- INDICATORS ---

indicators = {

"History of Violence": [

"Psychological violence (insults, humiliation)",
"Physical violence",
"Sexual violence",
"Use of weapons",
"Threats to kill the victim",
"Aggressor jealousy",
"Stalking behaviour",
"Escalation of violence recently"

],

"Aggressor Characteristics": [

"Extreme jealousy",
"Harassment behaviour",
"Economic or life problems",
"Lack of respect for authorities",
"Aggression against others",
"Previous criminal record",
"Violation of restraining orders",
"Violence against previous partners",
"Mental health problems",
"Suicidal thoughts",
"Substance abuse",
"Family history of violence",
"Aggressor under 24 years"

],

"Victim Vulnerability": [

"Victim disability or serious illness",
"Victim suicidal thoughts",
"Victim substance abuse",
"Lack of social support",
"Economic dependence"

],

"Children Risk Factors": [

"Children with aggressor",
"Threats or violence against children",
"Victim fears harm to children"

],

"Aggravating Circumstances": [

"Previous complaints",
"Previous gender violence reports",
"Victim intends to end relationship",
"Victim believes aggressor could kill her"

]

}

all_indicators = []
for cat in indicators:
    all_indicators.extend(indicators[cat])

# --- SIDEBAR CASE FILE ---

st.sidebar.header("Case File")

victim = st.sidebar.text_input("Victim ID","Case-001")

officer = st.sidebar.text_input("Officer Name")

location = st.sidebar.text_input("Police Unit")

st.sidebar.markdown("---")

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

    for q in indicators[cat]:

        with cols[i % 2]:

            answers[q] = st.radio(
                q,
                ["No","Yes","Unknown"],
                horizontal=True
            )

        i += 1

# --- CALCULATION ---

def calculate_score():

    score = 0

    for q in all_indicators:

        if answers[q] == "Yes":
            score += weights[q]

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

# --- STEP 3 ANALYSIS ---

st.header("Step 3 — Risk Analysis")

if st.button("🚨 Generate Risk Assessment"):

    score = calculate_score()
    risk = classify(score)

    col1, col2, col3 = st.columns(3)

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

    # Table

    data = []

    for q in all_indicators:

        val = 1 if answers[q] == "Yes" else 0

        data.append([
            q,
            answers[q],
            weights[q],
            val * weights[q]
        ])

    df = pd.DataFrame(data,columns=[
        "Indicator",
        "Answer",
        "Weight",
        "Contribution"
    ])

    st.subheader("Indicator Contribution")

    st.dataframe(df,use_container_width=True)
