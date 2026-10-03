import streamlit as st
from google import genai
from google.genai import types
# GEAA query expansion terms
QUERY_EXPANSION = {
    "hess": ["enthalpy", "energy", "reaction", "steps"],
    "heat change": ["enthalpy", "delta h", "thermodynamics"],
    "rate": ["kinetics", "activation energy", "reaction rate"],
    "equilibrium": ["ionic equilibrium", "ions", "equilibrium constant"],
    "electrochemistry": ["electrochemical", "electrode", "cell", "oxidation", "reduction"],
    "kinetics": ["rate", "activation energy", "collision theory"],
    "thermodynamics": ["enthalpy", "heat", "energy", "exothermic", "endothermic"],    "several steps": ["hess", "hess's law", "route", "reaction pathway"],
}
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
with st.expander("🔍 Knowledge Parser Test"):
    for document in KNOWLEDGE_DOCUMENTS:
        st.write(f"**Document:** {document['filename']}")
        st.write(f"**Type:** {document['document_type']}")
        st.write(f"**Number of sections:** {len(document['sections'])}")

        for index, section in enumerate(document["sections"], start=1):
            st.write(f"Section {index}: {section['heading']}")
            st.caption(section["content"][:300])You are GEAA, George's Education & Analytics Agent.
Be accurate, practical, clear and evidence-aware.
Do not invent facts, sources, data or experience.
"""
# Load GEAA knowledge documents
# Load GEAA knowledge documents
# Load GEAA knowledge documents
import os
import re


def parse_knowledge_sections(content, document_type):
    """Split a knowledge document into meaningful sections."""

    # Remove YAML-style metadata at the beginning.
    content = re.sub(
        r"\A---\s*\n.*?\n---\s*\n?",
        "",
        content,
        flags=re.DOTALL
    ).strip()

    if document_type == "course_outline":
        # Split only at major learning outcomes such as 1. Apply...
        pattern = r"(?m)(?=^\s*[1-4]\.\s+[A-Z])"

    elif document_type == "learning_notes":
        # Split at numbered topic headings such as 4.1 WHAT IS...
        pattern = r"(?m)(?=^\s*4\.\d+\s+[A-Z])"

    else:
        # Generic numbered headings.
        pattern = r"(?m)(?=^\s*\d+(?:\.\d+)*\s+[A-Z])"

    raw_sections = re.split(pattern, content)

    sections = []

    for raw_section in raw_sections:
        section_text = raw_section.strip()

        if not section_text:
            continue

        # Capture the first meaningful line as a provisional heading.
        first_line = next(
            (
                line.strip()
                for line in section_text.splitlines()
                if line.strip()
            ),
            "Untitled section"
        )

        sections.append({
            "heading": first_line,
            "content": section_text
        })

    return sections


KNOWLEDGE_DOCUMENTS = []

try:
    knowledge_folder = "knowledge"

    for filename in sorted(os.listdir(knowledge_folder)):
        if filename.endswith(".md"):
            filepath = os.path.join(knowledge_folder, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            filename_lower = filename.lower()

            if "course_outline" in filename_lower:
                document_type = "course_outline"
            elif "notes" in filename_lower:
                document_type = "learning_notes"
            else:
                document_type = "general_knowledge"

            sections = parse_knowledge_sections(
                content,
                document_type
            )

            KNOWLEDGE_DOCUMENTS.append({
                "filename": filename,
                "content": content,
                "document_type": document_type,
                "sections": sections
            })

except FileNotFoundError:
    KNOWLEDGE_DOCUMENTS = []
    KNOWLEDGE_DOCUMENTS = []


def retrieve_knowledge(task, documents, max_sections=5):
    """
    Retrieve the most relevant sections from GEAA knowledge documents.

    Uses:
    - document-aware section parsing
    - keyword matching
    - query expansion
    - exact phrase matching
    - filename matching
    - document-type relevance
    - section heading detection
    - duplicate removal
    """

    if not documents:
        return "", []

    task_lower = task.lower()

    task_words = set(
        word.lower()
        for word in re.findall(r"[A-Za-z0-9Δ]+", task)
        if len(word) > 2
    )

    expanded_terms = set(task_words)

    for phrase, related_terms in QUERY_EXPANSION.items():
        if phrase in task_lower:
            expanded_terms.update(
                term.lower()
                for term in related_terms
            )

    DOCUMENT_TYPE_HINTS = {
        "course_outline": [
            "course",
            "unit",
            "learning outcome",
            "duration",
            "assessment",
            "competency",
            "curriculum",
            "topics",
            "covered",
            "hours",
        ],
        "learning_notes": [
            "explain",
            "define",
            "calculate",
            "formula",
            "example",
            "concept",
            "how",
            "why",
            "reaction",
            "enthalpy",
            "activation energy",
            "energy",
            "theory",
            "application",
        ],
        "general_knowledge": []
    }

    matches = []
    seen_sections = set()

    phrase_list = [
        "activation energy",
        "enthalpy change",
        "hess's law",
        "reaction rate",
        "energy profile",
        "collision theory",
    ]

    for document in documents:

        content = document["content"]

        document_type = document.get(
            "document_type",
            "general_knowledge"
        )

        filename_words = set(
            word.lower()
            for word in re.findall(
                r"[A-Za-z0-9Δ]+",
                document["filename"]
            )
            if len(word) > 2
        )

        content = re.sub(
            r"^---.*?---\s*",
            "",
            content,
            flags=re.DOTALL
        )

        # Document-aware section parsing.
        if document_type == "course_outline":

            sections = re.split(
                r"(?m)(?=^\s*[1-4]\.\s+[A-Z])",
                content
            )

        elif document_type == "learning_notes":

            sections = re.split(
                r"(?m)(?=^4\.\d+\s+[A-Z])",
                content
            )

        else:

            sections = re.split(
                r"(?m)(?=^\s*\d+(?:\.\d+)*\s+[A-Z])",
                content
            )

        for section in sections:

            section_text = section.strip()

            if not section_text:
                continue

            section_lower = section_text.lower()

            section_words = set(
                word.lower()
                for word in re.findall(
                    r"[A-Za-z0-9Δ]+",
                    section_text
                )
                if len(word) > 2
            )

            score = len(
                expanded_terms.intersection(section_words)
            )

            # Exact phrase bonus.
            phrase_matches = [
                phrase
                for phrase in phrase_list
                if phrase in task_lower
                and phrase in section_lower
            ]

            score += 4 * len(phrase_matches)

            # Filename relevance.
            score += 3 * len(
                task_words.intersection(filename_words)
            )

            # Document-type relevance.
            document_type_hints = DOCUMENT_TYPE_HINTS.get(
                document_type,
                []
            )

            document_type_matches = [
                hint
                for hint in document_type_hints
                if hint in task_lower
            ]

            score += 3 * len(document_type_matches)

            # Section heading detection.
            if document_type == "course_outline":

                heading_match = re.search(
                    r"(?m)^\s*([1-4]\.\s+[A-Z][^\n]*)",
                    section_text
                )

            elif document_type == "learning_notes":

                heading_match = re.search(
                    r"(?m)^(4\.\d+\s+[A-Z][A-Z0-9\s&'():,\-]*)$",
                    section_text
                )

            else:

                heading_match = re.search(
                    r"(?m)^(\d+(?:\.\d+)*\s+[A-Z][A-Z0-9\s&'():,\-]*)$",
                    section_text
                )

            if heading_match:
                section_heading = heading_match.group(1).strip()
            else:
                section_heading = "Section heading not captured"

            # Heading-based relevance.
            heading_lower = section_heading.lower()

            heading_concepts = [
                "activation energy",
                "enthalpy change",
                "energy profile",
                "catalyst",
                "reaction rate",
                "collision theory",
                "hess's law",
                "bond energy",
                "chemical thermodynamics",
                "physical chemistry",
            ]

            for concept in heading_concepts:

                if (
                    concept in task_lower
                    and concept in heading_lower
                ):
                    score += 8

            # Course-outline concept relevance.
            if document_type == "course_outline":

                course_concepts = [
                    "chemical thermodynamics",
                    "physical chemistry",
                    "ionic equilibrium",
                    "electrochemistry",
                    "chemical kinetics",
                    "organic chemistry",
                    "inorganic chemistry",
                    "biochemistry",
                    "learning outcome",
                    "assessment",
                ]

                for concept in course_concepts:

                    if (
                        concept in task_lower
                        and concept in section_lower
                    ):
                        score += 8

            if score <= 0:
                continue

            # Prevent duplicate sections.
            section_key = (
                document["filename"],
                section_text
            )

            if section_key in seen_sections:
                continue

            seen_sections.add(section_key)

            matches.append({
                "score": score,
                "filename": document["filename"],
                "document_type": document_type,
                "section": section_text,
                "heading": section_heading
            })

    # Rank retrieved sections.
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    selected = matches[:max_sections]

    # Build retrieved context.
    retrieved_text = []

    for item in selected:

        retrieved_text.append(
            f"\n--- RETRIEVED KNOWLEDGE: "
            f"{item['filename']} | "
            f"Type: {item['document_type']} | "
            f"{item['heading']} ---\n"
            f"{item['section']}\n"
        )

    return "\n".join(retrieved_text), selected
try:
    knowledge_folder = "knowledge"
    knowledge_sections = []

    for filename in sorted(os.listdir(knowledge_folder)):
        if filename.endswith(".md"):
            filepath = os.path.join(knowledge_folder, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            knowledge_sections.append(
                f"\n--- KNOWLEDGE SOURCE: {filename} ---\n"
                f"{content}\n"
            )

    KNOWLEDGE_TEXT = "\n".join(knowledge_sections)

except FileNotFoundError:
    KNOWLEDGE_TEXT = ""
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

# Mode selection
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

# Mode-specific workflows
workflows = {

    "Teaching": """
TEACHING WORKFLOW

Follow this sequence when appropriate:

1. Identify the learner level and subject.
2. Identify exactly what the learner or teacher needs.
3. Identify the relevant learning objective or intended outcome.
4. Explain the content using language appropriate to the learner level.
5. Use examples, illustrations or analogies where they improve understanding.
6. If an activity is requested, make it practical, realistic and safe.
7. If assessment is appropriate, provide suitable questions or tasks.
8. Check scientific accuracy and ensure that models or analogies are clearly
   distinguished from the actual scientific process.
9. Present a classroom-ready response.

Do not add unnecessary advanced content simply to make the response longer.
""",

    "Research": """
RESEARCH WORKFLOW

Follow this sequence when appropriate:

1. Identify the research problem or purpose.
2. Identify the research question(s) or objective(s).
3. Identify the relevant concepts, variables or constructs.
4. Consider appropriate theory or conceptual framing.
5. Consider the appropriate research design and methodology.
6. Identify what evidence or data would be required.
7. Explain appropriate analysis methods.
8. Distinguish evidence from interpretation.
9. Identify limitations, assumptions and possible sources of bias.
10. Provide a clear research-oriented response.

Never fabricate references, participants, findings, datasets or results.
""",

    "Analytics": """
ANALYTICS WORKFLOW

Follow this sequence when appropriate:

1. Identify the analytical question.
2. Identify the available data and its structure.
3. Check data quality, missing values and obvious inconsistencies.
4. Determine appropriate calculations or analytical methods.
5. Analyse the data rather than assuming the result.
6. Select appropriate tables, charts or visualisations where useful.
7. Interpret the results in relation to the original question.
8. Identify limitations and important assumptions.
9. Provide practical implications or next steps where appropriate.

Never invent data or analytical results.
""",

    "Education Leadership": """
EDUCATION LEADERSHIP WORKFLOW

Follow this sequence when appropriate:

1. Identify the education leadership or management problem.
2. Identify the relevant stakeholders.
3. Identify available evidence and information gaps.
4. Consider the relevant school, institutional or policy context.
5. Identify possible approaches or interventions.
6. Consider implementation requirements.
7. Identify indicators that could be used to monitor progress.
8. Consider risks, limitations and unintended effects.
9. Provide practical next steps.
10. Preserve professional judgement and distinguish evidence from judgement.
""",

    "TVET": """
TVET WORKFLOW

Follow this sequence when appropriate:

1. Identify the competency, unit or skill involved.
2. Identify the expected learner performance.
3. Identify the relevant knowledge, skills and attitudes.
4. Identify the practical task or workplace application where appropriate.
5. Identify required resources, equipment and safety considerations.
6. Determine suitable assessment methods.
7. Identify appropriate evidence for the learner's portfolio where relevant.
8. Develop clear assessment criteria or indicators where requested.
9. Check that the task is practical, observable and assessable.
10. Present the result in a format suitable for TVET use.
""",

    "General": """
GENERAL WORKFLOW

1. Identify the user's actual task.
2. Identify important constraints and requirements.
3. Produce the most useful practical response.
4. Check accuracy, completeness and clarity.
5. State important limitations where necessary.
"""
}

# Task input
st.markdown("### What would you like GEAA to help you with?")

task = st.text_area(
    "Enter your task",
    placeholder="Example: Explain chemical kinetics to Form 3 students..."
)

# Run task
if st.button("🚀 Run Task"):
    retrieved_knowledge, retrieval_details = retrieve_knowledge(
        task,
        KNOWLEDGE_DOCUMENTS
    )

    with st.expander("🔎 Retrieved Knowledge"):
        if retrieval_details:
            for item in retrieval_details:
                lines = item["section"].splitlines()

                section_heading = next(
                    (
                        line.strip()
                        for line in lines
                        if re.match(
                            r"^\d+(?:\.\d+)*\s+",
                            line.strip()
                        )
                    ),
                    None
                )

                if section_heading:
                    display_section = section_heading
                else:
                    display_section = "Section heading not captured"

                st.write(
                    f"📄 {item['filename']} | "
                    f"Section: {display_section} | "
                    f"Keyword match score: {item['score']}"
                )
        else:
            st.write("No relevant knowledge was retrieved.")

    st.write("### 📚 Retrieved Text Passed to GEAA")
    st.text(retrieved_knowledge)



    if task.strip():

        # Combine instructions and workflow
        full_instructions = (
            GEAA_INSTRUCTIONS
            + "\n\nSELECTED MODE:\n"
            + mode
            + "\n\nMODE WORKFLOW:\n"
            + workflows[mode]
        )

        with st.spinner("GEAA is working through the task..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                   contents=f"""
USER TASK:
{task}

RETRIEVED GEAA KNOWLEDGE:
{retrieved_knowledge}
""",
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
    "GEAA v1.2 — George's Education & Analytics Agent"
)
