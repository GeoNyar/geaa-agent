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
    Retrieve knowledge sections using concept-aware relevance scoring.

    The retrieval system is deliberately conservative:
    generic word overlap alone should not be enough to retrieve
    unrelated knowledge.
    """

    if not documents or not task.strip():
        return "", []

    task_lower = task.lower()

    # ---------------------------------------------------------
    # 1. Stop words
    # ---------------------------------------------------------
    stop_words = {
        "what", "why", "how", "when", "where", "which",
        "who", "does", "do", "did", "is", "are", "was",
        "were", "the", "and", "or", "for", "from", "with",
        "about", "into", "between", "this", "that", "these",
        "those", "can", "could", "would", "should", "will",
        "may", "might", "explain", "describe", "discuss",
        "identify", "state", "give", "define", "show",
        "calculate", "using", "use", "student", "students",
        "teacher", "teachers", "school", "schools"
    }

    task_words = {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9Δ]+", task)
        if len(word) > 2 and word.lower() not in stop_words
    }

    # ---------------------------------------------------------
    # 2. Query expansion
    # ---------------------------------------------------------
    expanded_terms = set(task_words)

    for phrase, related_terms in QUERY_EXPANSION.items():

        if phrase in task_lower:

            expanded_terms.update(
                term.lower()
                for term in related_terms
            )

    # ---------------------------------------------------------
    # 3. Explicit knowledge domains
    #
    # These help GEAA distinguish chemistry questions from
    # education/research/analytics questions.
    # ---------------------------------------------------------
    DOMAIN_TERMS = {

        "thermodynamics": {
            "thermodynamics",
            "enthalpy",
            "enthalpy change",
            "heat change",
            "exothermic",
            "endothermic",
            "heat energy",
            "energy profile",
            "bond energy",
            "bonds broken",
            "bonds formed",
            "hess",
            "hess's law",
            "activation energy",
            "energy change",
            "calorimetry",
            "q=mc",
            "delta h"
        },

        "kinetics": {
            "kinetics",
            "reaction rate",
            "rate of reaction",
            "activation energy",
            "collision theory",
            "catalyst",
            "reaction mechanism"
        },

        "electrochemistry": {
            "electrochemistry",
            "electrochemical",
            "electrode",
            "electrolyte",
            "electrolysis",
            "oxidation",
            "reduction",
            "redox",
            "cell potential",
            "electrochemical cell"
        },

        "equilibrium": {
            "equilibrium",
            "equilibrium constant",
            "ionic equilibrium",
            "le chatelier",
            "equilibrium concentration",
            "reversible reaction"
        },

        "organic_chemistry": {
            "organic chemistry",
            "aldehyde",
            "ketone",
            "alcohol",
            "carboxylic acid",
            "ester",
            "amine",
            "organic compound",
            "synthesis",
            "purification"
        },

        "inorganic_chemistry": {
            "inorganic chemistry",
            "element",
            "periodicity",
            "periodic table",
            "inorganic salt",
            "chemical bond",
            "group i",
            "group ii"
        },

        "biochemistry": {
            "biochemistry",
            "biochemical",
            "protein",
            "carbohydrate",
            "lipid",
            "enzyme",
            "respiration",
            "photosynthesis",
            "atp",
            "metabolism"
        },

        "education_research": {
            "research",
            "research question",
            "research problem",
            "research objective",
            "research design",
            "research methodology",
            "methodology",
            "variable",
            "variables",
            "independent variable",
            "dependent variable",
            "predictor variable",
            "outcome variable",
            "student achievement",
            "academic achievement",
            "teacher competence",
            "teacher digital competence",
            "digital competence",
            "teacher performance",
            "school leadership",
            "educational leadership",
            "education policy",
            "education management",
            "educational management",
            "public secondary schools",
            "secondary schools",
            "school effectiveness"
        },

        "analytics": {
            "data",
            "dataset",
            "analysis",
            "analytics",
            "correlation",
            "regression",
            "mean",
            "median",
            "standard deviation",
            "visualization",
            "dashboard",
            "trend",
            "relationship"
        }
    }

    # ---------------------------------------------------------
    # 4. Detect the user's main domain
    # ---------------------------------------------------------
    requested_domains = []

    for domain, terms in DOMAIN_TERMS.items():

        domain_matches = 0

        for term in terms:

            if term in task_lower:
                domain_matches += 1

        if domain_matches > 0:
            requested_domains.append(
                (domain, domain_matches)
            )

    requested_domains.sort(
        key=lambda item: item[1],
        reverse=True
    )

    requested_domain = (
        requested_domains[0][0]
        if requested_domains
        else None
    )

    # ---------------------------------------------------------
    # 5. Document type hints
    # ---------------------------------------------------------
    DOCUMENT_TYPE_HINTS = {

        "course_outline": {
            "course",
            "unit",
            "learning outcome",
            "duration",
            "assessment",
            "competency",
            "curriculum",
            "topics",
            "covered",
            "hours"
        },

        "learning_notes": {
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
            "application"
        },

        "general_knowledge": set()
    }

    matches = []
    seen_sections = set()

    # ---------------------------------------------------------
    # 6. Score each knowledge section
    # ---------------------------------------------------------
    for document in documents:

        document_type = document.get(
            "document_type",
            "general_knowledge"
        )

        filename = document["filename"]

        filename_lower = filename.lower()

        sections = document.get("sections", [])

        # -----------------------------------------------------
        # Infer document domain from filename/content
        # -----------------------------------------------------
        document_domains = set()

        for domain, terms in DOMAIN_TERMS.items():

            for term in terms:

                if term in filename_lower:
                    document_domains.add(domain)

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

            # -------------------------------------------------
            # Determine domains represented by this section
            # -------------------------------------------------
            section_domains = set(document_domains)

            for domain, terms in DOMAIN_TERMS.items():

                matched_domain_terms = 0

                for term in terms:

                    if (
                        term in heading_lower
                        or term in section_lower
                    ):
                        matched_domain_terms += 1

                # A domain should normally require at least
                # two meaningful domain indicators.
                #
                # A highly specific phrase can establish the
                # domain by itself.
                specific_terms = {
                    "teacher digital competence",
                    "student achievement",
                    "research question",
                    "research problem",
                    "independent variable",
                    "dependent variable",
                    "chemical thermodynamics",
                    "ionic equilibrium",
                    "electrochemistry",
                    "chemical kinetics",
                    "organic chemistry",
                    "inorganic chemistry",
                    "biochemistry",
                    "hess's law",
                    "collision theory",
                    "energy profile"
                }

                specific_match = any(
                    term in heading_lower
                    or term in section_lower
                    for term in specific_terms.intersection(terms)
                )

                if (
                    matched_domain_terms >= 2
                    or specific_match
                ):
                    section_domains.add(domain)

            # -------------------------------------------------
            # Basic word overlap
            # -------------------------------------------------
            section_words = {
                word.lower()
                for word in re.findall(
                    r"[A-Za-z0-9Δ]+",
                    section_text
                )
                if len(word) > 2
                and word.lower() not in stop_words
            }

            keyword_matches = expanded_terms.intersection(
                section_words
            )

            score = len(keyword_matches)

            # -------------------------------------------------
            # Exact task phrase matches
            # -------------------------------------------------
            important_phrases = [
                "teacher digital competence",
                "student achievement",
                "research question",
                "research problem",
                "independent variable",
                "dependent variable",
                "enthalpy change",
                "activation energy",
                "reaction rate",
                "chemical thermodynamics",
                "hess's law",
                "energy profile",
                "collision theory"
            ]

            exact_phrase_matches = [
                phrase
                for phrase in important_phrases
                if phrase in task_lower
                and phrase in section_lower
            ]

            score += 8 * len(exact_phrase_matches)

            # -------------------------------------------------
            # Heading relevance
            # -------------------------------------------------
            heading_matches = [
                term
                for term in expanded_terms
                if term in heading_lower
            ]

            score += 5 * len(heading_matches)

            # -------------------------------------------------
            # Document-type relevance
            # -------------------------------------------------
            document_type_hints = DOCUMENT_TYPE_HINTS.get(
                document_type,
                set()
            )

            for hint in document_type_hints:

                if hint in task_lower:
                    score += 2

            # -------------------------------------------------
            # Domain relevance
            #
            # Strong positive bonus if the document section
            # belongs to the same domain as the user's task.
            # -------------------------------------------------
            if requested_domain is not None:

                if requested_domain in section_domains:

                    score += 15

                else:

                    # A clear domain mismatch should prevent
                    # generic keyword overlap from rescuing
                    # an unrelated knowledge section.
                    continue

            # -------------------------------------------------
            # Competing-domain protection
            #
            # If the user clearly asks an education/research
            # question, chemistry learning notes should not
            # survive simply because of generic word overlap.
            # -------------------------------------------------
            if requested_domain in {
                "education_research",
                "analytics"
            }:

                chemistry_domains = {
                    "thermodynamics",
                    "kinetics",
                    "electrochemistry",
                    "equilibrium",
                    "organic_chemistry",
                    "inorganic_chemistry",
                    "biochemistry"
                }

                if section_domains.intersection(
                    chemistry_domains
                ):

                    score -= 25

            # -------------------------------------------------
            # Ignore sections with no meaningful connection.
            # -------------------------------------------------
            if score <= 0:
                continue

            # -------------------------------------------------
            # Prevent duplicate sections.
            # -------------------------------------------------
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

    # ---------------------------------------------------------
    # 7. Rank results
    # ---------------------------------------------------------
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # ---------------------------------------------------------
    # 8. Conservative selection
    #
    # A result must either have a meaningful absolute score
    # or be reasonably close to the strongest result.
    # ---------------------------------------------------------
    if matches:

        best_score = matches[0]["score"]

        minimum_score = 8

        relative_threshold = best_score * 0.70

        selected = [
            item
            for item in matches
            if (
                item["score"] >= minimum_score
                and item["score"] >= relative_threshold
            )
        ][:max_sections]

    else:

        selected = []

    # ---------------------------------------------------------
    # 9. Build retrieved context
    # ---------------------------------------------------------
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

visualization_requested = any(
    keyword in task.lower()
    for keyword in [
        "visualize",
        "visualisation",
        "visualization",
        "chart",
        "graph",
        "plot",
        "bar chart",
        "line graph",
        "pie chart",
        "scatter plot"
    ]
)

research_question_requested = any(
    phrase in task.lower()
    for phrase in [
        "research question",
        "research problem",
        "research variables",
        "identify variables",
        "independent variable",
        "dependent variable",
        "predictor variable",
        "outcome variable",
        "research design",
        "methodology",
        "study variables"
    ]
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

            if visualization_requested:

                st.markdown("#### 📊 Data Visualization")

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

                    st.bar_chart(
                        chart_data,
                        x=categorical_columns[0],
                        y=numeric_columns[0]
                    )

                elif len(numeric_columns) == 2:

                    predictor_terms = [
                        "study",
                        "hours",
                        "attendance",
                        "age",
                        "experience",
                        "time",
                        "practice",
                        "training",
                        "input",
                        "exposure"
                    ]

                    outcome_terms = [
                        "score",
                        "mark",
                        "grade",
                        "result",
                        "performance",
                        "achievement",
                        "outcome",
                        "rating"
                    ]

                    x_column = numeric_columns[0]
                    y_column = numeric_columns[1]

                    for column in numeric_columns:

                        column_lower = column.lower()

                        if any(
                            term in column_lower
                            for term in predictor_terms
                        ):
                            x_column = column

                        if any(
                            term in column_lower
                            for term in outcome_terms
                        ):
                            y_column = column

                    scatter_data = uploaded_data[
                        [
                            x_column,
                            y_column
                        ]
                    ].copy()

                    st.scatter_chart(
                        scatter_data,
                        x=x_column,
                        y=y_column
                    )
    except Exception as e:

        st.error(
            "GEAA could not read the uploaded CSV file."
        )

        with st.expander("Technical details"):
            st.code(str(e))# Run task
if st.button("🚀 Run Task"):
if uploaded_data is not None or research_question_requested:
    retrieved_knowledge = ""
    retrieval_details = []
else:
    retrieved_knowledge, retrieval_details = retrieve_knowledge(
        task,
        KNOWLEDGE_DOCUMENTS
    )

# Determine the provenance of the knowledge available to GEAA.
if retrieved_knowledge.strip():
    knowledge_status = (
        "RELEVANT GEAA KNOWLEDGE RETRIEVED. "
        "The response may use the retrieved knowledge as "
        "user-provided evidence."
    )
else:
    knowledge_status = (
        "NO RELEVANT GEAA KNOWLEDGE RETRIEVED. "
        "The response must rely on the user's task, "
        "general AI knowledge, reasoning, and clearly "
        "labelled proposals or inferences."
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
            + """

EVIDENCE AND PROVENANCE RULES

GEAA must clearly distinguish between information obtained
from the user's knowledge base, general AI knowledge, and
new reasoning or proposals.

1. KNOWLEDGE-BASE EVIDENCE
Use this label when a statement is directly supported by
RETRIEVED GEAA KNOWLEDGE supplied in the prompt.

Do not claim that a statement comes from the GEAA knowledge
base unless relevant retrieved knowledge was actually supplied.

2. GENERAL AI KNOWLEDGE
When no relevant GEAA knowledge has been retrieved, answer
using general knowledge and reasoning available to the model.
Do not present general AI knowledge as if it came from the
user's knowledge base.

3. USER-PROVIDED INFORMATION
Clearly identify information that comes directly from the
USER TASK or UPLOADED DATA.

4. PROPOSED / INFERRED CONTENT
Clearly label interpretations, suggestions, operational
definitions, methodological recommendations, assumptions,
examples, or other content that is not directly established
by the user's task, uploaded data, or retrieved knowledge.

Use labels such as:
- QUESTION-PROVIDED
- UPLOADED-DATA
- KNOWLEDGE-BASE
- GENERAL KNOWLEDGE
- PROPOSED
- INFERRED
- NEEDS VERIFICATION

5. NO FABRICATION OF KNOWLEDGE-BASE SUPPORT
If GEAA KNOWLEDGE STATUS says that no relevant knowledge was
retrieved, do not cite, imply, or suggest that the user's
knowledge base supports the answer.

6. AVOID FALSE CERTAINTY
When evidence is unavailable, distinguish established facts
from reasonable interpretation and proposed methodology.

7. RESEARCH TASKS
For research questions, distinguish:
- what the research question explicitly provides;
- what can reasonably be inferred from the wording;
- what is being proposed for a possible study design;
- what requires verification from literature, policy documents,
  or empirical data.

Do not fabricate citations, studies, statistics, instruments,
policy requirements, or findings.
"""
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
                        + f"Missing cells: {uploaded_data.isna().sum().sum()}\n"
                    )

                    numeric_columns_for_analysis = [
                        column
                        for column in uploaded_data.columns
                        if pd.api.types.is_numeric_dtype(
                            uploaded_data[column]
                        )
                    ]

                    if numeric_columns_for_analysis:

                        descriptive_summary_for_analysis = pd.DataFrame({
                            "Variable": numeric_columns_for_analysis,
                            "Count": [
                                uploaded_data[column].count()
                                for column in numeric_columns_for_analysis
                            ],
                            "Mean": [
                                uploaded_data[column].mean()
                                for column in numeric_columns_for_analysis
                            ],
                            "Median": [
                                uploaded_data[column].median()
                                for column in numeric_columns_for_analysis
                            ],
                            "Minimum": [
                                uploaded_data[column].min()
                                for column in numeric_columns_for_analysis
                            ],
                            "Maximum": [
                                uploaded_data[column].max()
                                for column in numeric_columns_for_analysis
                            ],
                            "Standard deviation": [
                                uploaded_data[column].std()
                                for column in numeric_columns_for_analysis
                            ]
                        })

                        data_context += (
                            "\nDESCRIPTIVE STATISTICS:\n"
                            + descriptive_summary_for_analysis.to_string(
                                index=False
                            )
                        )

                        if len(numeric_columns_for_analysis) == 2:

                            x_column = numeric_columns_for_analysis[0]
                            y_column = numeric_columns_for_analysis[1]

                            predictor_terms = [
                                "study",
                                "hours",
                                "attendance",
                                "age",
                                "experience",
                                "time",
                                "practice",
                                "training",
                                "input",
                                "exposure"
                            ]

                            outcome_terms = [
                                "score",
                                "mark",
                                "grade",
                                "result",
                                "performance",
                                "achievement",
                                "outcome",
                                "rating"
                            ]

                            for column in numeric_columns_for_analysis:

                                column_lower = column.lower()

                                if any(
                                    term in column_lower
                                    for term in predictor_terms
                                ):
                                    x_column = column

                                if any(
                                    term in column_lower
                                    for term in outcome_terms
                                ):
                                    y_column = column

                            relationship_data = uploaded_data[
                                [
                                    x_column,
                                    y_column
                                ]
                            ].dropna()

                            if len(relationship_data) >= 2:

                                x_values = relationship_data[x_column]
                                y_values = relationship_data[y_column]

                                correlation = x_values.corr(y_values)

                                if x_values.var() != 0:

                                    slope = (
                                        x_values.cov(y_values)
                                        / x_values.var()
                                    )

                                    intercept = (
                                        y_values.mean()
                                        - slope * x_values.mean()
                                    )

                                    r_squared = correlation ** 2

                                    data_context += (
                                        "\nRELATIONSHIP ANALYSIS:\n"
                                        + f"X variable: {x_column}\n"
                                        + f"Y variable: {y_column}\n"
                                        + f"Pearson correlation (r): "
                                        + f"{correlation:.3f}\n"
                                        + f"Regression slope: "
                                        + f"{slope:.3f}\n"
                                        + f"Regression intercept: "
                                        + f"{intercept:.3f}\n"
                                        + f"R-squared (R²): "
                                        + f"{r_squared:.3f}\n"
                                        + "Regression equation: "
                                        + f"{y_column} = "
                                        + f"{intercept:.3f} + "
                                        + f"{slope:.3f} × {x_column}\n"
                                    )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
contents=(
    "USER TASK:\n"
    + task
    + "\n\nGEAA KNOWLEDGE STATUS:\n"
    + knowledge_status
    + "\n\nRETRIEVED GEAA KNOWLEDGE:\n"
    + (
        retrieved_knowledge
        if retrieved_knowledge.strip()
        else "[NO RELEVANT GEAA KNOWLEDGE RETRIEVED]"
    )
    + "\n\nUPLOADED DATA CONTEXT:\n"
    + data_context
                        + "\n\nAPPLICATION VISUALIZATION STATUS:\n"
                        + (
                            "A native interactive visualization has already "
                            "been generated in the application interface. "
                            "Do not create a second text-based, ASCII or "
                            "Markdown chart. Interpret the existing "
                            "visualization and the underlying data instead."
                            if visualization_requested
                            else
                            "No native visualization has been generated. "
                            "Do not create a visualization unless the user "
                            "specifically requests one."
                        )
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
