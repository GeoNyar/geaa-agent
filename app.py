import time
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="GEAA",
    page_icon="🎓",
    layout="wide"
)

# Connect to Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Load GEAA instructions
try:
    with open("geaa_instructions.txt", "r", encoding="utf-8") as file:
        GEAA_INSTRUCTIONS = file.read()
except FileNotFoundError:
    GEAA_INSTRUCTIONS = """
    You are GEAA, George's Education & Analytics Agent.
    Be accurate, practical, clear and evidence-aware.
    Do not invent facts, sources, data or experience.
    """

# Main page
st.title("🎓 GEAA")
st.subheader("George's Education & Analytics Agent")

st.write(
    "A personal AI workspace for teaching, education leadership, "
    "research, data analytics and TVET work."
)

st.divider()

# GEAA mode
st.markdown("### Select GEAA Mode")

mode = st.selectbox(
    "What type of task are you working on?",
    [
        "Teaching",
        "Research",
        "Analytics",
        "Education Leadership",
        "TVET",
        "General"
    ]
)

# Task input
st.markdown("### What would you like GEAA to help you with?")

task = st.text_area(
    "Enter your task",
    placeholder="Example: Explain chemical kinetics to Form 3 students..."
)

# Mode-specific instructions
mode_instructions = {
    "Teaching": """
Focus on teaching and learning.
Adapt explanations to the stated learner level.
Use clear language, examples, activities and assessment where useful.
Prioritize learner understanding and classroom practicality.
""",

    "Research": """
Focus on educational and scientific research.
Pay attention to research questions, methodology, evidence,
data analysis, academic writing and limitations.
Never fabricate references, findings or data.
""",

    "Analytics": """
Focus on data analysis and evidence-based decision-making.
When data are provided, check the data before interpreting them.
Use appropriate statistical or analytical methods.
Do not invent data or results.
Explain assumptions and limitations.
""",

    "Education Leadership": """
Focus on educational leadership and management.
Consider school improvement, quality assurance, teacher development,
planning, monitoring, decision-making and evidence.
Provide practical approaches that can work in an education setting.
""",

    "TVET": """
Focus on TVET, CBET and competency-based assessment.
Consider practical skills, assessment evidence, laboratory work,
performance criteria, portfolios and workplace relevance.
Use clear competency-oriented language.
""",

    "General": """
Provide a practical response appropriate to the task.
"""
}

# Run task
if st.button("🚀 Run Task"):

    if task.strip():

        # Combine general GEAA instructions with selected mode
        full_instructions = (
            GEAA_INSTRUCTIONS
            + "\n\nSELECTED MODE:\n"
            + mode
            + "\n\nMODE-SPECIFIC INSTRUCTIONS:\n"
            + mode_instructions[mode]
        )

        with st.spinner("GEAA is thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=task,
                    config=types.GenerateContentConfig(
                        system_instruction=full_instructions
                    )
                )

                st.markdown("### GEAA's Response")
                st.write(response.text)

            except Exception as e:

                st.error("GEAA could not complete the request.")

                with st.expander("Technical details"):
                    st.code(str(e))

    else:
        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.7 — George's Education & Analytics Agent"
)
