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

# Load GEAA instructions from a separate file
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

# Task input
st.markdown("### What would you like GEAA to help you with?")

task = st.text_area(
    "Enter your task",
    placeholder="Example: Explain chemical kinetics to Form 3 students..."
)

# Run task
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

                with st.expander("Technical details"):
                    st.code(str(e))

    else:
        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.6 — George's Education & Analytics Agent"
)
