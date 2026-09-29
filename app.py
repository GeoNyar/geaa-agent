import streamlit as st

# Page configuration
st.set_page_config(
    page_title="GEAA",
    page_icon="🎓",
    layout="wide"
)

# Main title
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
    placeholder="Example: Analyse this Form 3 Chemistry performance data..."
)

# Run button
if st.button("🚀 Run Task"):

    if task.strip():

        st.markdown("### Your task")

        st.write(task)

        st.info(
            "GEAA v0.1 received your task. "
            "The AI reasoning engine will be connected next."
        )

    else:

        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.1 — George's Education & Analytics Agent"
)
