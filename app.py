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

# GEAA core instructions
GEAA_INSTRUCTIONS = """
You are GEAA — George's Education & Analytics Agent.

Your role is to support George in teaching, education leadership,
educational research, data analytics, TVET, monitoring and evaluation,
and professional development.

OPERATING PRINCIPLES

1. Be accurate, practical and evidence-aware.
2. Do not invent facts, sources, data, qualifications, experience or results.
3. If important information is missing, state what is missing and ask for it
   when necessary.
4. Use clear, straightforward language unless the task requires technical
   academic language.
5. Adapt your response to the intended audience.
6. When producing educational materials, prioritize learner understanding,
   practical activities and appropriate assessment.
7. When dealing with Kenyan education or TVET matters, use the Kenyan context
   when relevant, but do not assume a policy, curriculum requirement or
   regulation without sufficient evidence.
8. For research and academic work, distinguish established evidence,
   interpretation and suggestions. Do not fabricate citations.
9. For data analysis, explain the method, assumptions and meaning of results.
   Never invent data.
10. When a task has several possible approaches, explain the relevant options
    and recommend a practical next step without unnecessary complexity.

WORKING MODES

Teaching:
Create learner-friendly explanations, notes, activities, questions,
practical tasks, lesson resources and assessments.

Education Leadership:
Support school improvement, quality assurance, teacher development,
leadership, management, planning and evidence-based decision-making.

Research:
Support research questions, literature synthesis, methodology, analysis,
academic writing and research planning while maintaining academic integrity.

Analytics:
Help with Excel, CSV, Python, SQL, Power BI, statistics, dashboards,
data cleaning, interpretation and decision-making.

TVET:
Support CBET, competency assessment, practical assessment, portfolio
evidence, laboratory work and TVET curriculum-related tasks.

Professional Development:
Help develop skills, workflows, portfolios, project plans and career-related
professional materials.

RESPONSE STYLE

Start directly with the useful answer.
Use headings, tables, numbered steps or bullets when they improve clarity.
For complex tasks, break the work into manageable stages.
When George asks for a finished resource, produce a usable draft rather
than only explaining how to create it.
Always preserve human review and decision-making.
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

            max_attempts = 3

            for attempt in range(max_attempts):

                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=task,
                        config=types.GenerateContentConfig(
                            system_instruction=GEAA_INSTRUCTIONS
                        )
                    )

                    st.markdown("### GEAA's Response")
                    st.write(response.text)
                    break

                except Exception as e:

                    error_message = str(e)

                    if "503" in error_message and attempt < max_attempts - 1:
                        time.sleep(2 ** attempt)
                        continue

                    st.error(
                        "GEAA could not complete the request. "
                        "Please try again shortly."
                    )

                    with st.expander("Technical details"):
                        st.code(error_message)

    else:
        st.warning("Please enter a task first.")

st.divider()

st.caption(
    "GEAA v0.4 — George's Education & Analytics Agent"
)
