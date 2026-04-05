import streamlit as st
import pandas as pd
import random
from docx import Document
from io import BytesIO

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="UrbanLab System", layout="wide")

st.markdown("""
<div style="background-color:#1e3a8a;color:white;padding:12px;border-radius:8px;text-align:center;font-weight:bold;margin-bottom:20px;">
🏙️ URBAN POLICY SIMULATION SYSTEM
</div>
""", unsafe_allow_html=True)

st.title("UrbanLab — Social Disorganization Simulator")

st.markdown("""
1️⃣ Analyse neighbourhood  
2️⃣ Design intervention  
3️⃣ Evaluate outcomes  
4️⃣ Exchange and assess reports  
""")

st.divider()

# -----------------------------
# BARRIOS
# -----------------------------
barrios = {
    "Exclusión severa": {
        "desorganizacion":85,"cohesion":25,"pobreza":90,
        "desc":"Alta marginalidad, economías informales y fuerte desorganización social."
    },
    "Centro degradado": {
        "desorganizacion":70,"cohesion":35,"pobreza":65,
        "desc":"Alta densidad, rotación poblacional y conflictos de convivencia."
    },
    "Barrio en transformación": {
        "desorganizacion":60,"cohesion":40,"pobreza":60,
        "desc":"Proceso de cambio urbano con tensiones sociales."
    },
    "Periferia obrera": {
        "desorganizacion":55,"cohesion":50,"pobreza":55,
        "desc":"Identidad comunitaria con desigualdades emergentes."
    }
}

# -----------------------------
# INTERPRETADOR AVANZADO
# -----------------------------
def interpretar_plan(plan):

    texto = plan.lower()

    categorias = {
        "Control formal": {
            "kw":["polic","vigilancia","cámaras"],
            "impacto":{"policia":15,"control":10},
            "tipo":"punitiva"
        },
        "Cohesión social": {
            "kw":["vecin","comunit","asociaciones"],
            "impacto":{"cohesion":15,"control":10},
            "tipo":"estructural"
        },
        "Urbanismo": {
            "kw":["urban","espacio","rehabilitación"],
            "impacto":{"desorganizacion":-15},
            "tipo":"estructural"
        },
        "Intervención económica": {
            "kw":["empleo","educa","formación"],
            "impacto":{"pobreza":-15},
            "tipo":"estructural"
        }
    }

    cambios = {"policia":0,"cohesion":0,"control":0,"desorganizacion":0,"pobreza":0}
    contribuciones = []
    tipos = set()

    for nombre,data in categorias.items():
        for kw in data["kw"]:
            if kw in texto:
                tipos.add(data["tipo"])
                for k,v in data["impacto"].items():
                    cambios[k]+=v
                contribuciones.append(nombre)
                break

    tipo_final = "mixta" if len(tipos)>1 else list(tipos)[0] if tipos else "indefinida"

    score = len(contribuciones)*2

    return cambios, contribuciones, tipo_final, min(score,10)

# -----------------------------
# SIMULACIÓN
# -----------------------------
st.header("Step 1 — Select neighbourhood")

barrio_sel = st.selectbox("Neighbourhood", list(barrios.keys()))
st.info(barrios[barrio_sel]["desc"])

if st.button("Start simulation"):

    b = barrios[barrio_sel]

    estado = {
        "desorganizacion": b["desorganizacion"],
        "cohesion": b["cohesion"],
        "control":30,
        "pobreza": b["pobreza"],
        "policia":40
    }

    st.session_state.estado = estado

# -----------------------------
# INTERVENCIÓN
# -----------------------------
if "estado" in st.session_state:

    st.header("Step 2 — Intervention design")

    plan = st.text_area("Describe your intervention")

    if st.button("Run simulation"):

        cambios, contribuciones, tipo, score = interpretar_plan(plan)

        b = st.session_state.estado

        for k in cambios:
            if k in b:
                b[k]+=cambios[k]

        delincuencia = (
            b["desorganizacion"]*0.4 +
            b["pobreza"]*0.3 -
            b["cohesion"]*0.3 -
            b["control"]*0.2
        )

        st.session_state.resultado = delincuencia
        st.session_state.contrib = contribuciones
        st.session_state.tipo = tipo
        st.session_state.score = score

# -----------------------------
# RESULTADOS
# -----------------------------
if "resultado" in st.session_state:

    st.header("Step 3 — Results")

    col1,col2,col3 = st.columns(3)

    col1.metric("Crime level", round(st.session_state.resultado,2))
    col2.metric("Strategy", st.session_state.tipo)
    col3.metric("Theoretical score", st.session_state.score)

    df = pd.DataFrame(st.session_state.contrib, columns=["Interventions detected"])
    st.dataframe(df, use_container_width=True)

# -----------------------------
# INFORME WORD
# -----------------------------
if "resultado" in st.session_state:

    st.header("Step 4 — Generate report")

    if st.button("Generate Word report"):

        doc = Document()

        doc.add_heading('URBAN POLICY REPORT', 1)

        doc.add_paragraph(f"Neighbourhood: {barrio_sel}")
        doc.add_paragraph(f"Crime level: {round(st.session_state.resultado,2)}")
        doc.add_paragraph(f"Strategy: {st.session_state.tipo}")

        doc.add_heading('Interventions', level=2)
        for c in st.session_state.contrib:
            doc.add_paragraph(c)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            "Download report",
            buffer,
            file_name="urban_report.docx"
        )

# -----------------------------
# DRIVE + EVALUACIÓN
# -----------------------------
st.divider()
st.header("📄 Report exchange & evaluation")

grupo = st.selectbox("Select your group", ["Group A","Group B","Group C"])

links = {
    "Group A":{"upload":"LINK_A","review":"LINK_B"},
    "Group B":{"upload":"LINK_B","review":"LINK_C"},
    "Group C":{"upload":"LINK_C","review":"LINK_A"}
}

st.subheader("Upload your report")
st.markdown(f"[Open folder]({links[grupo]['upload']})")

st.subheader("Review other reports")
st.markdown(f"[Open reports]({links[grupo]['review']})")

# -----------------------------
# RÚBRICA
# -----------------------------
st.header("Peer evaluation")

c1,c2 = st.columns(2)

with c1:
    coherencia = st.slider("Theoretical coherence",0,10,5)
    analisis = st.slider("Quality of analysis",0,10,5)

with c2:
    viabilidad = st.slider("Feasibility",0,10,5)
    innovacion = st.slider("Innovation",0,10,5)

nota = (coherencia+analisis+viabilidad+innovacion)/4
st.metric("Final grade", round(nota,2))

comentario = st.text_area("Comment")

# -----------------------------
# EXPORTAR EVALUACIÓN
# -----------------------------
if st.button("Generate evaluation report"):

    doc = Document()

    doc.add_heading('PEER EVALUATION REPORT',1)

    doc.add_paragraph(f"Group: {grupo}")
    doc.add_paragraph(f"Final grade: {round(nota,2)}")

    doc.add_heading("Scores",2)
    doc.add_paragraph(f"Coherence: {coherencia}")
    doc.add_paragraph(f"Analysis: {analisis}")
    doc.add_paragraph(f"Feasibility: {viabilidad}")
    doc.add_paragraph(f"Innovation: {innovacion}")

    doc.add_heading("Comment",2)
    doc.add_paragraph(comentario)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        "Download evaluation",
        buffer,
        file_name="evaluation.docx"
    )
