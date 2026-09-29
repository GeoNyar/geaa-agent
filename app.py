import time
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="GEAA",
    page_icon="🎓",
    layout="wide"
)

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

GEAA_INSTRUCTIONS = """
You are GEAA — George's Education & Analytics Agent.

Support teaching, education leadership, educational research, data
analytics, TVET, monitoring and evaluation, and professional development.

Be accurate, practical and clear.
Do not invent facts, sources, data or experience.
Adapt explanations to the intended audience.
For educational tasks, prioritize learner understanding and assessment.
For research, maintain academic integrity and do not fabricate citations.
For data analysis, never invent data and explain assumptions.
Use structured responses when helpful.
"""

st.title("🎓 GEAA")
st.subheader("George's Education & Analytics Agent")

st.write(
    "A personal AI workspace for teaching, education leadership, "
    "research, data analytics and TVET work."
)

st.divider()

st.markdown("### What would you like GEAA to help you with?")

task = st.text_area(
    "Enter your task",
    placeholder="Example: Explain chemical kinetics to Form 3 students..."
)

if st.button("🚀 Run Task"):

    if task.strip():

        with st.spinner("GEAA is thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=task,
                    config=types.GenerateContentConfig(
                        system_instruction=GEAA_INSTRUCTIONS
                    )
                )

                st.markdown("### GEAA's Response")
                st.write(response.text)

            except Exception as e:

                st.error("GEAA could not complete the request.")

                st.markdown("### 🔎 Diagnostic information")
                st.code(str(e))

    else:
        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.5 — Diagnostic version"
)
