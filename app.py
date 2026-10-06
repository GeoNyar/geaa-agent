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
You are GEAA, George's Education & Analytics Agent.
Be accurate, practical, clear and evidence-aware.
Do not invent facts, sources, data or experience.
"""
# Load GEAA knowledge documents
# Load GEAA knowledge documents
# Load GEAA knowledge documents
import os
import re
import pandas as pd



def parse_knowledge_sections(content, document_type):
    """Split knowledge documents into meaningful sections."""

    # Remove YAML-style metadata at the beginning.
    content = re.sub(
        r"\A---\s*\n.*?\n---\s*\n?",
        "",
        content,
        flags=re.DOTALL
    ).strip()

    sections = []

    # ---------------------------------------------------------
    # Thermodynamics learning notes
    # ---------------------------------------------------------
    if document_type == "learning_notes":

        pattern = r"(?m)(?=^\s*4\.\d+\s+[A-Z])"
        raw_sections = re.split(pattern, content)

        for raw_section in raw_sections:
            section_text = raw_section.strip()

            if not section_text:
                continue

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

    # ---------------------------------------------------------
    # Chemistry Principles course outline
    # ---------------------------------------------------------
    if document_type == "course_outline":

        # These are the actual learning outcomes and their
        # corresponding subtopics in the course outline.
        outcomes = [
            {
                "number": "1",
                "heading": "1. Apply physical chemistry concepts",
                "hours": 25,
                "topics": [
                    "1.1 Ionic equilibrium",
                    "1.2 Electrochemistry principles",
                    "1.3 Chemical kinetics",
                    "1.4 Chemical thermodynamics",
                ],
            },
            {
                "number": "2",
                "heading": "2. Apply organic chemistry concepts",
                "hours": 25,
                "topics": [
                    "2.1 Aldehydes",
                    "2.2 Synthesize organic compounds",
                    "2.3 Purify synthesized compounds",
                    "2.4 Characterize purified compounds",
                ],
            },
            {
                "number": "3",
                "heading": "3. Apply inorganic chemistry concepts",
                "hours": 25,
                "topics": [
                    "3.1 Identify elements",
                    "3.2 Classify elements",
                    "3.3 Determine chemical bonds",
                    "3.4 Test inorganic salts",
                ],
            },
            {
                "number": "4",
                "heading": "4. Apply biochemistry concepts",
                "hours": 45,
                "topics": [
                    "4.1 Identify biochemical molecules",
                    "4.2 Carry out biochemical reactions",
                    "4.3 Determine biochemical processes",
                ],
            },
        ]

        # Preserve the course identity and duration as a
        # separate introductory section.
        intro_parts = []

        intro_patterns = [
            r"CHEMISTRY PRINCIPLES",
            r"ISCED UNIT CODE:\s*0531\s*541\s*14A",
            r"TVET CDACC UNIT CODE:\s*SLT/CU/SL/CC/03/6/MA",
            r"UNIT DURATION:\s*120\s*hours",
            r"Relationship to Occupational Standards",
            r"Unit Description",
            r"Summary of Learning Outcomes",
        ]

        for pattern in intro_patterns:
            match = re.search(
                pattern,
                content,
                flags=re.IGNORECASE
            )
            if match:
                intro_parts.append(match.group(0))

        intro_text = "\n".join(dict.fromkeys(intro_parts))

        if intro_text:
            sections.append({
                "heading": "Chemistry Principles — Course Overview",
                "content": intro_text
            })

        # Reconstruct each outcome as one structured section.
        for outcome in outcomes:

            topic_text = "\n".join(outcome["topics"])

            section_content = (
                f"{outcome['heading']} — "
                f"{outcome['hours']} hours\n"
                f"{topic_text}"
            )

            sections.append({
                "heading": outcome["heading"],
                "content": section_content,
                "hours": outcome["hours"],
                "topics": outcome["topics"],
            })

        return sections

    # ---------------------------------------------------------
    # Generic knowledge documents
    # ---------------------------------------------------------
    pattern = r"(?m)(?=^\s*\d+(?:\.\d+)*\s+[A-Z])"
    raw_sections = re.split(pattern, content)

    for raw_section in raw_sections:
        section_text = raw_section.strip()

        if not section_text:
            continue

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

    # ---------------------------------------------------------
    # Generic knowledge documents
    # ---------------------------------------------------------

    pattern = r"(?m)(?=^\s*\d+(?:\.\d+)*\s+[A-Z])"

    raw_sections = re.split(pattern, content)

    for raw_section in raw_sections:

        section_text = raw_section.strip()

        if not section_text:
            continue

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
with st.expander("🔍 Knowledge Parser Test"):
    for document in KNOWLEDGE_DOCUMENTS:
        st.write(f"**Document:** {document['filename']}")
        st.write(f"**Type:** {document['document_type']}")
        st.write(f"**Number of sections:** {len(document['sections'])}")

        for index, section in enumerate(document["sections"], start=1):
            st.write(f"Section {index}: {section['heading']}")
            st.caption(section["content"][:300])


def retrieve_knowledge(task, documents, max_sections=5):
    """
    Retrieve the most relevant structured sections from GEAA knowledge documents.
    """

    if not documents:
        return "", []

    task_lower = task.lower()

    task_words = set(
        word.lower()
        for word in re.findall(r"[A-Za-z0-9Δ]+", task)
        if len(word) > 2
    )

    # Expand important concepts into related terms.
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

    phrase_list = [
        "activation energy",
        "enthalpy change",
        "hess's law",
        "reaction rate",
        "energy profile",
        "collision theory",
    ]

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
        "organic chemistry",
        "inorganic chemistry",
        "biochemistry",
    ]

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

    matches = []
    seen_sections = set()

    for document in documents:

        document_type = document.get(
            "document_type",
            "general_knowledge"
        )

        filename = document["filename"]

        filename_words = set(
            word.lower()
            for word in re.findall(
                r"[A-Za-z0-9Δ]+",
                filename
            )
            if len(word) > 2
        )

        sections = document.get("sections", [])

        for section_data in sections:

            section_text = section_data.get(
                "content",
                ""
            ).strip()

            section_heading = section_data.get(
                "heading",
                "Untitled section"
            ).strip()

            if not section_text:
                continue

            section_lower = section_text.lower()
            heading_lower = section_heading.lower()

            section_words = set(
                word.lower()
                for word in re.findall(
                    r"[A-Za-z0-9Δ]+",
                    section_text
                )
                if len(word) > 2
            )

            # 1. Basic keyword relevance
            score = len(
                expanded_terms.intersection(section_words)
            )

            # 2. Exact phrase relevance
            phrase_matches = [
                phrase
                for phrase in phrase_list
                if phrase in task_lower
                and phrase in section_lower
            ]

            score += 4 * len(phrase_matches)

            # 3. Filename relevance
            score += 3 * len(
                task_words.intersection(filename_words)
            )

            # 4. Document-type relevance
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

            # 5. Subject-specific heading relevance

            subject_areas = [
                "physical chemistry",
                "organic chemistry",
                "inorganic chemistry",
                "biochemistry",
            ]

            requested_subject = None

            for subject in subject_areas:
                if subject in task_lower:
                    requested_subject = subject
                    break

            for concept in heading_concepts:

                if concept in task_lower:

                    # Normal heading match
                    if concept in heading_lower:
                        score += 8

                    # Strong subject-area matching
                    if concept in subject_areas:

                        if concept in heading_lower:

                            # Strong bonus for exact requested subject
                            if concept == requested_subject:
                                score += 20

                            # Penalty for competing subject
                            elif requested_subject is not None:
                                score -= 20

            # 6. Course-outline concept relevance
            if document_type == "course_outline":

                for concept in course_concepts:

                    if (
                        concept in task_lower
                        and concept in section_lower
                    ):
                        score += 8

            # -------------------------------------------------
            # 7. Exclude competing subject areas.
            #
            # If the user explicitly asks about one chemistry
            # subject, do not retrieve another subject's section.
            # -------------------------------------------------

            if requested_subject is not None:

                competing_subject = None

                for subject in subject_areas:

                    if (
                        subject in heading_lower
                        and subject != requested_subject
                    ):
                        competing_subject = subject
                        break

                if competing_subject is not None:
                    continue

            # Ignore sections with no meaningful connection.
            if score <= 0:
                continue

            # 7. Prevent duplicate sections
            section_key = (
                filename,
                section_heading,
                section_text
            )

            if section_key in seen_sections:
                continue

            seen_sections.add(section_key)

            matches.append({
                "score": score,
                "filename": filename,
                "document_type": document_type,
                "section": section_text,
                "heading": section_heading
            })

    # Rank sections from most relevant to least relevant.
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Select the strongest relevant sections.
    if matches:

        best_score = matches[0]["score"]

        relevance_threshold = best_score * 0.75

        selected = [
            item
            for item in matches
            if item["score"] >= relevance_threshold
        ][:max_sections]

    else:
        selected = []

    # Build the retrieved context sent to Gemini.
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

st.markdown("### 📊 Optional Data File")

uploaded_file = st.file_uploader(
    "Upload a CSV file for GEAA to inspect",
    type=["csv"],
    help="Upload a CSV dataset when your task requires data analysis."
)

# Run task
# Inspect uploaded data
uploaded_data = None

if uploaded_file is not None:

    try:
        uploaded_data = pd.read_csv(uploaded_file)

        st.markdown("### 📋 Uploaded Data")

        st.write(
            f"**File:** {uploaded_file.name}"
        )

        st.write(
            f"**Rows:** {uploaded_data.shape[0]} | "
            f"**Columns:** {uploaded_data.shape[1]}"
        )

        st.markdown("#### Variables")

        variable_table = pd.DataFrame({
            "Variable": uploaded_data.columns,
            "Data type": [
                str(dtype)
                for dtype in uploaded_data.dtypes
            ],
            "Missing values": [
                int(uploaded_data[column].isna().sum())
                for column in uploaded_data.columns
            ]
        })

        st.dataframe(
            variable_table,
            use_container_width=True
        )

        st.markdown("#### Preview")

        st.dataframe(
            uploaded_data.head(10),
            use_container_width=True
        )

        st.markdown("#### 🔎 Data Quality Check")

        duplicate_rows = int(
            uploaded_data.duplicated().sum()
        )

        missing_cells = int(
            uploaded_data.isna().sum().sum()
        )

        numeric_columns = [
            column
            for column in uploaded_data.columns
            if pd.api.types.is_numeric_dtype(
                uploaded_data[column]
            )
        ]

        st.write(
            f"**Duplicate rows:** {duplicate_rows}"
        )

        st.write(
            f"**Missing cells:** {missing_cells}"
        )

        st.write(
            f"**Numeric variables:** "
            f"{len(numeric_columns)}"
        )

        if numeric_columns:

            numeric_summary = pd.DataFrame({
                "Variable": numeric_columns,
                "Minimum": [
                    uploaded_data[column].min()
                    for column in numeric_columns
                ],
                "Maximum": [
                    uploaded_data[column].max()
                    for column in numeric_columns
                ]
            })

            st.markdown("#### Numerical Range")

            st.dataframe(
                numeric_summary,
                use_container_width=True
            )
            st.markdown("#### 📊 Descriptive Statistics")

            descriptive_summary = pd.DataFrame({
                "Variable": numeric_columns,
                "Count": [
                    uploaded_data[column].count()
                    for column in numeric_columns
                ],
                "Mean": [
                    uploaded_data[column].mean()
                    for column in numeric_columns
                ],
                "Median": [
                    uploaded_data[column].median()
                    for column in numeric_columns
                ],
                "Minimum": [
                    uploaded_data[column].min()
                    for column in numeric_columns
                ],
                "Maximum": [
                    uploaded_data[column].max()
                    for column in numeric_columns
                ],
                "Standard deviation": [
                    uploaded_data[column].std()
                    for column in numeric_columns
                ]
            })

            st.dataframe(
                descriptive_summary,
                use_container_width=True
            )

            st.markdown("#### 📌 Calculated Values")

            for _, row in descriptive_summary.iterrows():

                st.write(
                    f"**{row['Variable']}** — "
                    f"Count: {int(row['Count'])}, "
                    f"Mean: {row['Mean']:.2f}, "
                    f"Median: {row['Median']:.2f}, "
                    f"Minimum: {row['Minimum']:.2f}, "
                    f"Maximum: {row['Maximum']:.2f}, "
                    f"Sample standard deviation: {row['Standard deviation']:.2f}"
                )

            categorical_columns = [
                column
                for column in uploaded_data.columns
                if not pd.api.types.is_numeric_dtype(
                    uploaded_data[column]
                )
            ]

            if (
                len(numeric_columns) == 1
                and len(categorical_columns) >= 1
            ):

                chart_data = uploaded_data[
                    [
                        categorical_columns[0],
                        numeric_columns[0]
                    ]
                ].copy()

                st.markdown("#### 📊 Data Visualization")

                st.bar_chart(
                    chart_data,
                    x=categorical_columns[0],
                    y=numeric_columns[0]
                )
    except Exception as e:

        st.error(
            "GEAA could not read the uploaded CSV file."
        )

        with st.expander("Technical details"):
            st.code(str(e))# Run task
if st.button("🚀 Run Task"):
    if uploaded_data is not None:
        retrieved_knowledge = ""
        retrieval_details = []
    else:
        retrieved_knowledge, retrieval_details = retrieve_knowledge(
            task,
            KNOWLEDGE_DOCUMENTS
        )

    with st.expander("🔎 Retrieved Knowledge"):
        if retrieval_details:
            for item in retrieval_details:
                display_section = item.get(
                    "heading",
                    "Section heading not captured"
                )

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
        full_instructions = (
            GEAA_INSTRUCTIONS
            + "\n\nSELECTED MODE:\n"
            + mode
            + "\n\nMODE WORKFLOW:\n"
            + workflows[mode]
        )

        with st.spinner("GEAA is working through the task..."):

            try:
                # Prepare uploaded data for Gemini
                data_context = ""

                if uploaded_data is not None:

                    data_context = (
                        "UPLOADED DATASET:\n"
                        + f"File: {uploaded_file.name}\n"
                        + f"Rows: {uploaded_data.shape[0]}\n"
                        + f"Columns: {uploaded_data.shape[1]}\n\n"
                        + "DATA:\n"
                        + uploaded_data.to_string(index=False)
                        + "\n\nDATA QUALITY:\n"
                        + f"Duplicate rows: {uploaded_data.duplicated().sum()}\n"
                        + f"Missing cells: {uploaded_data.isna().sum().sum()}\n\n"
                        + "DESCRIPTIVE STATISTICS:\n"
                        + descriptive_summary.to_string(index=False)
                    )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=(
                        "USER TASK:\n"
                        + task
                        + "\n\nRETRIEVED GEAA KNOWLEDGE:\n"
                        + retrieved_knowledge
                        + "\n\nUPLOADED DATA CONTEXT:\n"
                        + data_context
                    ),
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
