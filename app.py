import streamlit as st
from google import genai

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
                    model="gemini-3.8-flash",
                    contents=task
                )

                st.markdown("### GEAA's Response")
                st.write(response.text)

            except Exception as e:
                st.error(
                    "GEAA could not connect to the AI service."
                )
                st.code(str(e))

    else:
        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.2 — Powered by Gemini"
)
