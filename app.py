import streamlit as st
from google import genai
from google.genai import types
from geaa_ai import (
    FALLBACK_MODEL,
    GeminiFallbackError,
    classify_gemini_error,
    generate_content_with_fallback,
)
from pptx import Presentation
from pptx.util import Inches, Pt
# GEAA query expansion terms
QUERY_EXPANSION = {
    "hess": ["enthalpy", "energy", "reaction", "steps"],
    "heat change": ["enthalpy", "delta h", "thermodynamics"],
    "rate": ["kinetics", "activation energy", "reaction rate"],
    "equilibrium": ["ionic equilibrium", "ions", "equilibrium constant"],
    "electrochemistry": ["electrochemical", "electrode", "cell", "oxidation", "reduction"],
    "kinetics": ["rate", "activation energy", "collision theory"],
    "thermodynamics": ["enthalpy", "heat", "energy", "exothermic", "endothermic"],
    "photosynthesis": ["biochemistry", "thermodynamics", "endothermic", "energy", "sunlight", "glucose"],
    "several steps": ["hess", "hess's law", "route", "reaction pathway"],
}

def create_geaa_presentation(slide_text):
    """Convert GEAA's numbered slide response into an editable PowerPoint."""

    prs = Presentation()
    prs.core_properties.title = "GEAA Education and Research Presentation"
    prs.core_properties.author = "GEAA — George's Education & Analytics Agent"

    current_slide = None

    for raw_line in slide_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        # Recognise headings such as: Slide 1: Title
        if re.match(r"^(#{1,3}\s*)?Slide\s+\d+\s*[:—-]", line, re.IGNORECASE):
            heading = re.sub(r"^#{1,3}\s*", "", line)
            heading = re.sub(r"^Slide\s+\d+\s*[:—-]\s*", "", heading, flags=re.IGNORECASE)

            current_slide = prs.slides.add_slide(prs.slide_layouts[1])
            current_slide.shapes.title.text = heading or "Untitled Slide"
            continue

        # Treat Markdown headings as slide headings if no slide exists yet.
        if line.startswith("# "):
            current_slide = prs.slides.add_slide(prs.slide_layouts[1])
            current_slide.shapes.title.text = line[2:].strip()
            continue

        # Start a title slide if the response does not use slide headings.
        if current_slide is None:
            current_slide = prs.slides.add_slide(prs.slide_layouts[1])
            current_slide.shapes.title.text = "GEAA Presentation"
            body = current_slide.placeholders[1].text_frame
            body.text = line
            continue

        # Add response lines as editable bullet points.
        body = current_slide.placeholders[1].text_frame
        paragraph = body.add_paragraph()
        paragraph.text = re.sub(r"^[-*•]\s*", "", line)
        paragraph.level = 0
        paragraph.font.size = Pt(20)

    if len(prs.slides) == 0:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "GEAA Presentation"
        slide.placeholders[1].text = slide_text[:1000]

    output = __import__("io").BytesIO()
    prs.save(output)
    output.seek(0)
    return output.getvalue()

# Page configuration
st.set_page_config(
    page_title="GEAA",
    page_icon="🎓",
    layout="wide"
)

# Connect to Gemini when an API key is available.
# Research Data mode should remain usable without Gemini.
try:
    gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")
    client = (
        genai.Client(
            api_key=gemini_api_key,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=5,
                    http_status_codes=[408, 500, 502, 503, 504],
                    initial_delay=1.0,
                    max_delay=16.0,
                    exp_base=2.0,
                    jitter=0.5,
                )
            ),
        )
        if gemini_api_key
        else None
    )
except Exception:
    client = None
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



        pattern = r"(?im)(?=^\s*(?:#+\s*)?(?:4\.\d+(?:\.\d+)*\s+.*|TOPIC SUMMARY|KEY FORMULAE|SELF-ASSESSMENT|CHECK YOUR UNDERSTANDING|CHALLENGE TASK)\s*$)"
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

        # Preserve the original course document as searchable
        # sections instead of relying only on reconstructed data.
        original_content = content.strip()

        # These outcomes preserve the known course structure.
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

        # Keep the course identity and duration together.
        intro_patterns = [
            r"CHEMISTRY PRINCIPLES",
            r"ISCED UNIT CODE:\s*0531\s*541\s*14A",
            r"TVET CDACC UNIT CODE:\s*SLT/CU/SL/CC/03/6/MA",
            r"UNIT DURATION:\s*120\s*hours",
        ]

        intro_parts = []

        for pattern in intro_patterns:
            match = re.search(
                pattern,
                original_content,
                flags=re.IGNORECASE
            )
            if match:
                intro_parts.append(match.group(0))

        intro_text = "\n".join(dict.fromkeys(intro_parts))

        if intro_text:
            sections.append({
                "heading": "Chemistry Principles — Course Overview",
                "content": intro_text,
            })

        # Preserve detailed source sections under their original
        # headings wherever the Markdown uses heading syntax.
        raw_sections = re.split(
            r"(?m)(?=^#{1,6}\s+)",
            original_content
        )

        for raw_section in raw_sections:
            section_text = raw_section.strip()

            if not section_text:
                continue

            first_line = next(
                (
                    line.strip().lstrip("#").strip()
                    for line in section_text.splitlines()
                    if line.strip()
                ),
                "Untitled section"
            )

            # Avoid adding the whole document as one section.
            if len(section_text) > 12000:
                continue

            # Skip the introductory metadata block if present.
            if first_line == "---":
                continue

            sections.append({
                "heading": first_line,
                "content": section_text,
            })

        # Retain the existing structured outcome sections.
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

        # Remove exact duplicate sections without changing order.
        unique_sections = []
        seen = set()

        for section in sections:
            key = (
                section.get("heading", ""),
                section.get("content", ""),
            )

            if key not in seen:
                seen.add(key)
                unique_sections.append(section)

        return unique_sections



    # ---------------------------------------------------------
    # Generic knowledge documents
    # ---------------------------------------------------------
    # Split only on numbered headings written in uppercase.
    # This avoids splitting on ordinary numbered objectives
    # such as "3. To examine the association...".
    pattern = (
        r"(?im)(?=^\s*(?:#{1,6}\s*)?"
        r"\d+(?:\.\d+)*\.?\s+[A-Z][A-Z0-9\s:&(),/'-]*$)"
    )

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

        heading = re.sub(
            r"^#{1,6}\s*",
            "",
            first_line
        ).strip()

        sections.append({
            "heading": heading,
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
            elif "education_research" in filename_lower:
                document_type = "education_research"
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
debug_mode = st.sidebar.checkbox(
    "Enable developer diagnostics",
    value=False,
    key="geaa_debug_mode",
)

if debug_mode:
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
    Retrieve knowledge sections using precision-oriented,
    concept-aware relevance scoring.

    The retrieval system prioritizes:
    - exact concept matches
    - specific subject terminology
    - heading relevance
    - domain compatibility
    - meaningful keyword overlap
    - primary concepts for broad queries
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
        if len(word) > 2
        and word.lower() not in stop_words
    }

    # ---------------------------------------------------------
    # 2. Query expansion
    # ---------------------------------------------------------
    primary_terms = set(task_words)

    expanded_terms = set(primary_terms)

    for phrase, related_terms in QUERY_EXPANSION.items():

        if phrase in task_lower:

            expanded_terms.update(
                term.lower()
                for term in related_terms
            )

    # Terms introduced by query expansion rather than
    # explicitly written by the user.
    expansion_terms = (
        expanded_terms - primary_terms
    )

    # ---------------------------------------------------------
    # Detect broad-topic queries
    # ---------------------------------------------------------
    broad_topic_patterns = [
        "explain",
        "describe",
        "introduction to",
        "overview of",
        "what is",
        "teach me",
        "give an overview",
        "discuss"
    ]

    is_broad_query = (
        any(
            pattern in task_lower
            for pattern in broad_topic_patterns
        )
        and len(primary_terms) <= 4
    )

    # ---------------------------------------------------------
    # 3. Explicit knowledge domains
    # ---------------------------------------------------------
    DOMAIN_TERMS = {

        "curriculum": {
            "chemistry principles",
            "physical chemistry",
            "course outline",
            "unit duration",
            "course duration",
            "learning outcome",
            "curriculum",
            "assessment",
            "topics covered"
        },
        "thermodynamics": {
            "thermodynamics",
            "gibbs free energy",
            "gibbs energy",
            "delta g",
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
            "educational research",
            "descriptive statistics",
            "inferential statistics",
            "school leaders",
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
        "school effectiveness",
        "gibbs free energy",
        "photosynthesis",
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
    # 4A. Reject queries outside supported knowledge domains
    # ---------------------------------------------------------
    if requested_domain is None:
        return "", []
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

    # ---------------------------------------------------------
    # 6. Terms that are too generic to strongly influence
    #    retrieval on their own
    # ---------------------------------------------------------

    weak_terms = {
        # Broad subject words
        "energy",
        "change",
        "reaction",
        "chemical",
        "compound",
        "process",
        "theory",
        "application",
        "concept",
        "system",
        "data",
        "analysis",
        "relationship",
        "education",
        "learning",
        "teaching",
        "performance",
        "school",
        "student",
        "teacher",

        # Generic instruction and question words
        "explain",
        "describe",
        "discuss",
        "define",
        "identify",
        "outline",
        "state",
        "show",
        "give",
        "provide",
        "answer",
        "distinguish",
        "compare",
        "contrast",
        "illustrate",
        "calculate",
        "determine",
        "explain why",
        "occur",
        "occurs",
        "occurring",
        "happen",
        "happens",
        "slowly",
        "still",
        "however",
        "therefore",
        "using",
        "used",
        "use",
        "how",
        "why",
        "what",
        "when",
        "where",
        "which",
        "their",
        "your",
        "this",
        "that",
        "can",
        "does",
        "do",
        "is",
        "are",
        "and",
        "but",
        "for",
        "with",
        "from",
        "into",
        "between",
        "the",
        "a",
        "an",
        "of",
        "to",
        "in",
        "on",
        "at",
        "by",

        # Additional low-information terms seen in retrieval output
        "not",
        "possible",
        "possibly",
        "may",
        "might",
        "could",
        "should",
        "would",
        "must",
        "need",
        "needs",
        "needed",
        "based",
        "specific",
        "example",
        "examples",
        "include",
        "includes",
        "including",
        "such",
        "also",
        "each",
        "both",
        "other",
        "more",
        "most",
        "many",
        "some",
        "any",
        "all",
        "within",
        "across",
        "appropriate",
        "relevant",
        "clearly",
        "exact",
        "general",
    }
    # ---------------------------------------------------------
    # 7. Highly specific concepts
    # ---------------------------------------------------------
    specific_terms = {
        "teacher digital competence",
        "student achievement",
        "research question",
        "research problem",
        "independent variable",
        "dependent variable",
        "predictor variable",
        "outcome variable",
        "public secondary schools",
        "school effectiveness",
                "photosynthesis",
        "respiration",
        "atp",
        "metabolism",
        "enzyme",
        "protein",
        "carbohydrate",
        "lipid","chemical thermodynamics",
        "ionic equilibrium",
        "electrochemistry",
        "chemical kinetics",
        "organic chemistry",
        "inorganic chemistry",
        "biochemistry",
        "hess's law",
        "enthalpy change",
        "activation energy",
        "collision theory",
        "energy profile",
        "reaction rate",
        "le chatelier",
        "equilibrium constant"
    }

    # ---------------------------------------------------------
    # 8. Important phrases that deserve exact-match weighting
    # ---------------------------------------------------------
    important_phrases = [
        "teacher digital competence",
        "student achievement",
        "research question",
        "research problem",
        "independent variable",
        "dependent variable",
        "predictor variable",
        "outcome variable",
        "public secondary schools",
        "school effectiveness",
        "gibbs free energy",
        "enthalpy change",
        "enthalpy change",
        "activation energy",
        "reaction rate",
        "chemical thermodynamics",
        "hess's law",
        "energy profile",
        "collision theory",
        "ionic equilibrium",
        "electrochemistry",
        "organic chemistry",
        "inorganic chemistry",
        "biochemistry"
    ]

    matches = []
    seen_sections = set()

    # ---------------------------------------------------------
    # 9. Score each knowledge section
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
        # Infer document domain from filename
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
            # Classify the role of the knowledge section
            # -------------------------------------------------
            section_role = "general"

            foundational_patterns = [
                "what is",
                "introduction",
                "overview",
                "basic",
                "fundamental",
                "topic overview",
                "course overview"
            ]

            application_patterns = [
                "application",
                "applications",
                "and biochemistry",
                "in biology",
                "in biological",
                "industrial",
                "real life"
            ]

            definition_patterns = [
                "definition",
                "defined as",
                "meaning of",
                "is the study of"
            ]

            if any(
                pattern in heading_lower
                for pattern in foundational_patterns
            ):
                section_role = "foundational"

            elif any(
                pattern in heading_lower
                for pattern in definition_patterns
            ):
                section_role = "foundational"

            elif any(
                pattern in heading_lower
                for pattern in application_patterns
            ):
                section_role = "application"

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

                domain_specific_match = any(
                    term in heading_lower
                    or term in section_lower
                    for term in specific_terms.intersection(terms)
                )

                if (
                    matched_domain_terms >= 2
                    or domain_specific_match
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

            strong_keyword_matches = {
                word
                for word in keyword_matches
                if word not in weak_terms
            }

            weak_keyword_matches = (
                keyword_matches - strong_keyword_matches
            )

            score = (
                len(strong_keyword_matches) * 3
                + len(weak_keyword_matches) * 1
            )

            # -------------------------------------------------
            # Exact phrase matches
            # -------------------------------------------------
            exact_phrase_matches = [
                phrase
                for phrase in important_phrases
                if phrase in task_lower
                and phrase in section_lower
            ]

            score += 12 * len(exact_phrase_matches)


            # -------------------------------------------------
            # Specific concept matches
            # -------------------------------------------------
            specific_matches = [
                term
                for term in specific_terms
                if term in task_lower
                and term in section_lower
            ]

            meaningful_specific_matches = [
                term
                for term in specific_matches
                if term not in weak_terms
            ]

            score += 8 * len(meaningful_specific_matches)
            # -------------------------------------------------
            # -------------------------------------------------
            # Heading relevance
            # -------------------------------------------------
            heading_matches = [
                term
                for term in expanded_terms
                if len(term) > 2
                and term not in weak_terms
                and term in heading_lower
            ]

            score += 7 * len(heading_matches)

            # Give an exact primary-topic heading additional
            # weight for broad explanatory queries.
            if is_broad_query:
                if any(
                    term in heading_lower
                    for term in primary_terms
                    if len(term) > 2
                    and term not in weak_terms
                ):
                    score += 12

            heading_phrase_matches = [
                phrase
                for phrase in important_phrases
                if phrase in task_lower
                and phrase in heading_lower
            ]

            score += 10 * len(heading_phrase_matches)

            # -------------------------------------------------
            # Primary concept priority for broad queries
            # -------------------------------------------------
            primary_heading_matches = []

            primary_content_matches = []

            if is_broad_query:

                primary_heading_matches = [
                    term
                    for term in primary_terms
                    if len(term) > 2
                    and term not in weak_terms
                    and term in heading_lower
                ]

                primary_content_matches = [
                    term
                    for term in primary_terms
                    if len(term) > 2
                    and term not in weak_terms
                    and term in section_lower
                ]

                score += (
                    20
                    * len(primary_heading_matches)
                )

                score += (
                    8
                    * len(primary_content_matches)
                )


                # Foundational sections should be preferred
                # for broad explanatory questions.
                if section_role == "foundational":
                    score += 15

                # Application sections remain useful, but
                # should not outrank introductory material
                # merely because they contain the topic word.
                elif section_role == "application":
                    score -= 5


            # -------------------------------------------------
            # Document-type relevance
            # -------------------------------------------------
            document_type_hints = DOCUMENT_TYPE_HINTS.get(
                document_type,
                set()
            )

            for hint in document_type_hints:

                if hint in task_lower:
                    score += 1

            # -------------------------------------------------
            # Domain relevance
            # -------------------------------------------------
            domain_match = False
            strong_query_concept_match = False

            domain_match = False
            strong_query_concept_match = False

            if requested_domain is not None:

                domain_match = (
                    requested_domain in section_domains
                )

                # A strong query-specific concept can establish
                # relevance even when the section's broader
                # domain classification is incomplete.
                #
                # Example:
                # "photosynthesis" should retrieve a section
                # containing photosynthesis even if that section
                # was not automatically classified as
                # biochemistry.

                strong_query_concept_match = (
                    len(exact_phrase_matches) > 0
                    or len(specific_matches) > 0
                )

                if domain_match:

                    score += 20

                elif strong_query_concept_match:

                    score += 10

                else:

                    continue
            # -------------------------------------------------
            # Minimum relevance evidence gate
            # -------------------------------------------------
            # A domain match by itself is not sufficient to
            # retrieve a section.
            #
            # The section must also contain meaningful evidence
            # connecting it to the user's actual query.
            #
            # This prevents unrelated sections from being
            # retrieved merely because they belong to the same
            # broad subject domain.

            meaningful_primary_matches = {
                term
                for term in keyword_matches
                if term in primary_terms
                and term not in weak_terms
            }

            meaningful_expansion_matches = {
                term
                for term in keyword_matches
                if term in expansion_terms
                and term not in weak_terms
            }

            has_relevance_evidence = (
                len(exact_phrase_matches) > 0
                or len(specific_matches) > 0
                or len(heading_matches) > 0
                or len(heading_phrase_matches) > 0
                or len(primary_heading_matches) > 0
                or len(primary_content_matches) > 0
                or len(meaningful_primary_matches) > 0
                or len(meaningful_expansion_matches) > 0
            )

            if not has_relevance_evidence:
                continue

            # -------------------------------------------------
            # Competing-domain protection
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

                    score -= 30

            # -------------------------------------------------
            # Peripheral-match penalty
            # -------------------------------------------------
            has_strong_evidence = (
                len(exact_phrase_matches) > 0
                or len(specific_matches) > 0
                or len(heading_matches) > 0
                or len(heading_phrase_matches) > 0
                or len(primary_heading_matches) > 0
            )

            if not has_strong_evidence:
                score -= 3

            if score <= 0:
                continue

            # -------------------------------------------------
            # Explain why this section was retrieved
            # -------------------------------------------------
            retrieval_reasons = []


            # Primary query matches
            primary_matches = {
                term
                for term in keyword_matches
                if term in primary_terms
                and term not in weak_terms
                and len(term) > 2
            }

            if primary_matches:
                retrieval_reasons.append(
                    "Primary query match: "
                    + ", ".join(
                        sorted(primary_matches)
                    )
                )


            # Expanded query matches
            expansion_matches = {
                term
                for term in keyword_matches
                if term in expansion_terms
                and term not in weak_terms
                and len(term) > 2
            }

            if expansion_matches:
                retrieval_reasons.append(
                    "Expanded query match: "
                    + ", ".join(
                        sorted(expansion_matches)
                    )
                )

            # Exact phrase matches
            if exact_phrase_matches:
                retrieval_reasons.append(
                    "Exact phrase match: "
                    + ", ".join(exact_phrase_matches)
                )

            # Specific concept matches
            if specific_matches:
                retrieval_reasons.append(
                    "Specific concept match: "
                    + ", ".join(specific_matches)
                )

            # Heading relevance
            if heading_phrase_matches:
                retrieval_reasons.append(
                    "Heading phrase match: "
                    + ", ".join(heading_phrase_matches)
                )

            if heading_matches:
                retrieval_reasons.append(
                    "Heading relevance: "
                    + ", ".join(heading_matches)
                )

            # Broad-query primary concept priority
            if is_broad_query:

                if primary_heading_matches:
                    retrieval_reasons.append(
                        "Broad-query primary heading match: "
                        + ", ".join(
                            primary_heading_matches
                        )
                    )

                if primary_content_matches:
                    retrieval_reasons.append(
                        "Broad-query primary concept match: "
                        + ", ".join(
                            primary_content_matches
                        )
                    )

                if section_role == "foundational":
                    retrieval_reasons.append(
                        "Section role: foundational"
                    )

                elif section_role == "application":
                    retrieval_reasons.append(
                        "Section role: application"
                    )

            # Other keyword overlap
            filtered_strong_keyword_matches = {
                term
                for term in strong_keyword_matches
                if term not in weak_terms
                and len(term) > 2
            }

            filtered_weak_keyword_matches = {
                term
                for term in weak_keyword_matches
                if term not in weak_terms
                and len(term) > 2
            }

            if filtered_strong_keyword_matches:
                retrieval_reasons.append(
                    "Strong keyword overlap: "
                    + ", ".join(
                        sorted(filtered_strong_keyword_matches)
                    )
                )

            if filtered_weak_keyword_matches:
                retrieval_reasons.append(
                    "General keyword overlap: "
                    + ", ".join(
                        sorted(filtered_weak_keyword_matches)
                    )
                )


            # Domain relevance
            if requested_domain is not None:

                if domain_match:

                    retrieval_reasons.append(
                        "Domain match: "
                        + requested_domain
                    )

                elif strong_query_concept_match:

                    retrieval_reasons.append(
                        "Strong concept override: "
                        + ", ".join(
                            sorted(
                                set(exact_phrase_matches)
                                | set(specific_matches)
                            )
                        )
                    )
            if not retrieval_reasons:
                retrieval_reasons.append(
                    "General relevance match"
                )

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
                "heading": section_heading,
                "section_role": section_role,
                "retrieval_reasons": retrieval_reasons
            })

    # ---------------------------------------------------------
    # 10. Rank results
    # ---------------------------------------------------------
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # ---------------------------------------------------------
    # 11. Conservative selection
    # ---------------------------------------------------------
    if matches:

        best_score = matches[0]["score"]

        minimum_score = 12

        relative_threshold = best_score * 0.65

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
    # 12. Build retrieved context
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
        "Research Data",
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

    "Research Data": """
RESEARCH DATA WORKFLOW

Analyse the supplied dataset locally in Python. Do not transmit participant-level
rows to the language model. Describe data quality, measurement limitations,
descriptive findings and suitable exploratory analyses without making causal
claims from observational data.
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
    "Upload a data file for GEAA to inspect",
    type=["csv", "xlsx", "xls"],
    help="CSV and Excel files are supported. Research Data mode analyses records locally in Python."
)

# Run task
# Inspect uploaded data
uploaded_data = None

if uploaded_file is not None:

    try:
        if uploaded_file.name.lower().endswith((".xlsx", ".xls")):
            uploaded_data = pd.read_excel(uploaded_file)
        else:
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
            "GEAA could not read the uploaded file. Check that it is a valid CSV or Excel file."
        )

        with st.expander("Technical details"):
            st.code(str(e))# Run task
run_task_clicked = st.button("🚀 Run Task")

# Tie Research Data results to the exact inputs submitted by the user.
research_data_run_signature = (
    mode,
    getattr(uploaded_file, "name", None),
    getattr(uploaded_file, "size", None),
    task,
)

if run_task_clicked:
    st.session_state["research_data_run_signature"] = (
        research_data_run_signature
        if mode == "Research Data"
        else None
    )

research_data_results_active = (
    mode == "Research Data"
    and st.session_state.get("research_data_run_signature")
    == research_data_run_signature
)

if run_task_clicked or research_data_results_active:

    if mode == "Research Data":
        st.markdown("### Research Data — Local Analysis")
        st.info(
            "Privacy safeguard: this mode analyses the uploaded dataset with Python. "
            "It does not send raw dataset rows to Gemini."
        )

        if uploaded_data is None:
            st.warning("Upload a readable CSV or Excel dataset before running the analysis.")
        else:
            try:
                data = uploaded_data.copy()
                row_count, column_count = data.shape
                numeric_columns = [
                    col for col in data.columns
                    if pd.api.types.is_numeric_dtype(data[col])
                ]

                binary_numeric_columns = [
                    col for col in numeric_columns
                    if data[col].nunique(dropna=True) == 2
                ]

                categorical_columns = list(dict.fromkeys(
                    [
                        col for col in data.columns
                        if col not in numeric_columns
                    ] + binary_numeric_columns
                ))

                quality = pd.DataFrame({
                    "Variable": data.columns.astype(str),
                    "Data type": [str(data[col].dtype) for col in data.columns],
                    "Missing values": [int(data[col].isna().sum()) for col in data.columns],
                    "Missing (%)": [
                        round(float(data[col].isna().mean() * 100), 2)
                        for col in data.columns
                    ],
                    "Unique values": [int(data[col].nunique(dropna=True)) for col in data.columns],
                })
                duplicate_rows = int(data.duplicated().sum())
                missing_cells = int(data.isna().sum().sum())

                st.markdown("#### 1. Dataset overview")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Rows", row_count)
                c2.metric("Columns", column_count)
                c3.metric("Duplicate rows", duplicate_rows)
                c4.metric("Missing cells", missing_cells)
                st.caption(
                    f"File: {uploaded_file.name}. This is a descriptive, exploratory workflow; "
                    "results depend on the quality, definitions and representativeness of the supplied data."
                )

                st.markdown("#### 2. Data-quality profile")
                st.dataframe(quality, use_container_width=True)
                st.markdown("#### 3. Preview")
                st.dataframe(data.head(10), use_container_width=True)

                st.markdown("#### 4. Descriptive statistics")
                if numeric_columns:
                    descriptive = data[numeric_columns].describe().T.reset_index()
                    descriptive = descriptive.rename(columns={"index": "Variable"})
                    st.dataframe(descriptive, use_container_width=True)
                    st.download_button(
                        "Download descriptive statistics (CSV)",
                        data=descriptive.to_csv(index=False).encode("utf-8"),
                        file_name="geaa_descriptive_statistics.csv",
                        mime="text/csv",
                        key="research_data_descriptive_download"
                    )
                else:
                    descriptive = pd.DataFrame()
                    st.write("No numeric columns were detected for numeric descriptive statistics.")

                if categorical_columns:
                    preferred_category = "digital_training_past_2_years"
                    default_category_index = (
                        categorical_columns.index(preferred_category)
                        if preferred_category in categorical_columns
                        else 0
                    )
                    selected_category = st.selectbox(
                        "Choose a categorical variable for frequency analysis",
                        options=categorical_columns,
                        index=default_category_index,
                        key="research_data_category"
                    )
                    frequencies = (
                        data[selected_category]
                        .fillna("[Missing]")
                        .astype(str)
                        .value_counts(dropna=False)
                        .rename_axis("Category")
                        .reset_index(name="Frequency")
                    )
                    frequencies["Percentage"] = (
                        frequencies["Frequency"] / max(row_count, 1) * 100
                    ).round(1)
                    st.dataframe(frequencies, use_container_width=True)
                    st.bar_chart(frequencies.set_index("Category"))
                    st.download_button(
                        "Download category frequencies (CSV)",
                        data=frequencies.to_csv(index=False).encode("utf-8"),
                        file_name="geaa_category_frequencies.csv",
                        mime="text/csv",
                        key="research_data_frequency_download"
                    )

                if len(numeric_columns) >= 2:
                    st.markdown("#### 5. Exploratory correlations")
                    st.caption(
                        "Pearson correlations describe linear association between numeric variables. "
                        "They do not establish causation and may be misleading where assumptions are unsuitable."
                    )
                    correlation = data[numeric_columns].corr(method="pearson")
                    st.dataframe(correlation.round(3), use_container_width=True)
                    st.download_button(
                        "Download correlation matrix (CSV)",
                        data=correlation.to_csv().encode("utf-8"),
                        file_name="geaa_exploratory_correlations.csv",
                        mime="text/csv",
                        key="research_data_correlation_download"
                    )

                # Inspect synthetic-data labels in the uploaded file without treating labels as independent provenance verification.
                data_status_col = "data_status"
                synthetic_label = "SYNTHETIC_NOT_REAL"
                synthetic_status_summary = None
                if data_status_col in data.columns:
                    status_values = data[data_status_col].astype("string").str.strip().str.upper()
                    nonblank_status = status_values.dropna()
                    if len(nonblank_status) == 0:
                        synthetic_status_summary = (
                            "- Synthetic-data status: a `data_status` column is present, but it contains no usable labels. "
                            "Dataset provenance has not been verified."
                        )
                    else:
                        synthetic_count = int((nonblank_status == synthetic_label).sum())
                        labelled_count = int(len(nonblank_status))
                        if synthetic_count == row_count and labelled_count == row_count:
                            synthetic_status_summary = (
                                f"- Synthetic-data status: all {row_count} records are labelled `{synthetic_label}`. "
                                "This verifies the labels in the uploaded file, not the independent provenance of the data."
                            )
                        elif synthetic_count > 0:
                            synthetic_status_summary = (
                                f"- Synthetic-data status: {synthetic_count} of {labelled_count} nonblank `data_status` values "
                                f"are labelled `{synthetic_label}`; labels are mixed or incomplete. Review provenance before interpreting results."
                            )
                        else:
                            observed_labels = ", ".join(sorted(set(nonblank_status.astype(str).tolist()))[:10])
                            synthetic_status_summary = (
                                f"- Synthetic-data status: no `{synthetic_label}` labels were found in the {labelled_count} "
                                f"nonblank `data_status` values (observed labels: {observed_labels}). Do not assume the dataset is real; verify provenance."
                            )
                else:
                    synthetic_status_summary = (
                        "- Synthetic-data status: no `data_status` column was found. Dataset provenance has not been verified; "
                        "do not assign a synthetic or real status based on this check alone."
                    )

                # Task-focused interpretation from calculations actually performed in Python.
                task_analysis_lines = [
                    "## Task-focused exploratory interpretation",
                    "",
                    f"**Task entered:** {task if task.strip() else 'No specific task entered.'}",
                    "",
                    "**Evidence status:** Results below are calculated from the uploaded file and describe this dataset only.",
                    "",
                    "### Descriptive patterns",
                ]
                summary_specs = [
                    ("teacher_digital_competence_score", "Teacher digital competence"),
                    ("school_resource_access_index", "School resource access index"),
                    ("current_class_mean_achievement_score", "Current class mean achievement"),
                ]
                for col, label in summary_specs:
                    if col in data.columns:
                        vals = pd.to_numeric(data[col], errors="coerce").dropna()
                        if not vals.empty:
                            task_analysis_lines.append(
                                f"- {label}: n={len(vals)}, mean={vals.mean():.2f}, median={vals.median():.2f}, "
                                f"range={vals.min():.2f}–{vals.max():.2f}."
                            )
                training_col = "digital_training_past_2_years"
                if training_col in data.columns:
                    vals = pd.to_numeric(data[training_col], errors="coerce").dropna()
                    if not vals.empty and vals.isin([0, 1]).all():
                        task_analysis_lines.append(
                            f"- Digital training in the past two years: {vals.mean()*100:.1f}% coded 1 and "
                            f"{(1-vals.mean())*100:.1f}% coded 0; verify that the codebook defines 1=yes and 0=no."
                        )

                task_analysis_lines.extend(["", "### Teacher digital competence and current achievement"])
                competence_col = "teacher_digital_competence_score"
                achievement_col = "current_class_mean_achievement_score"
                if competence_col in data.columns and achievement_col in data.columns:
                    paired = data[[competence_col, achievement_col]].apply(pd.to_numeric, errors="coerce").dropna()
                    if len(paired) >= 2 and paired[competence_col].nunique() > 1 and paired[achievement_col].nunique() > 1:
                        r_value = paired[competence_col].corr(paired[achievement_col], method="pearson")
                        task_analysis_lines.append(
                            f"- Pearson correlation: r={r_value:.3f}, based on {len(paired)} complete records with values for both variables."
                        )
                        if pd.notna(r_value):
                            if r_value >= 0.70:
                                direction = "strong positive"
                            elif r_value >= 0.30:
                                direction = "moderate positive"
                            elif r_value > 0:
                                direction = "weak positive"
                            elif r_value <= -0.70:
                                direction = "strong negative"
                            elif r_value <= -0.30:
                                direction = "moderate negative"
                            elif r_value < 0:
                                direction = "weak negative"
                            else:
                                direction = "approximately no linear"
                            task_analysis_lines.append(
                                f"- The observed linear association is {direction}. Correlation does not establish causation."
                            )
                    else:
                        task_analysis_lines.append("- Correlation was not calculated: insufficient paired variation.")
                else:
                    task_analysis_lines.append("- Required competence/achievement columns were not both found.")

                task_analysis_lines.extend(["", "### Baseline and current achievement comparison"])
                baseline_col = "baseline_class_mean_score"
                if baseline_col in data.columns and achievement_col in data.columns:
                    paired_scores = data[[baseline_col, achievement_col]].apply(pd.to_numeric, errors="coerce").dropna()
                    if not paired_scores.empty:
                        mean_baseline = paired_scores[baseline_col].mean()
                        mean_current = paired_scores[achievement_col].mean()
                        mean_difference = mean_current - mean_baseline
                        task_analysis_lines.extend([
                            f"- Baseline column mean={mean_baseline:.2f}; current column mean={mean_current:.2f}.",
                            f"- Difference between column means (current minus baseline)={mean_difference:.2f} points, calculated from {len(paired_scores)} records with both values present.",
                            "- The dataset documentation does not establish that these are paired measurements of the same classes at defined time points. This is a comparison of two column means, not a record-level change estimate, longitudinal change estimate or evidence of intervention effectiveness.",
                            "- Verify that score scales and measurement conditions are comparable before interpreting the difference."
                        ])
                else:
                    task_analysis_lines.append("- Required baseline/current score columns were not both found.")

                task_analysis_lines.extend([
                    "",
                    "### Data-quality and methodological limitations",
                    f"- {row_count} rows and {column_count} columns; {duplicate_rows} exact duplicate rows; {missing_cells} missing cells.",
                    "- No missing cells or duplicate rows does not guarantee that values are valid, accurate or representative.",
                    "- Confirm variable definitions, score scales, coding and the data-generation process.",
                    "- Pearson correlation describes linear association; no inferential significance test or causal analysis was performed.",
                    "- If teachers are grouped within schools, observations may be clustered and later analyses should account for school-level structure.",
                    "",
                    "### Three cautious follow-up research questions",
                    "1. How strongly is teacher digital competence associated with current class mean achievement, and does this pattern vary by school?",
                    "2. How are digital training participation and school resource access associated with teacher digital competence?",
                    "3. If baseline and current scores are confirmed to be comparable measurements for the same intended units, how do the differences vary across classes or schools, and what contextual factors may be associated with that variation?",
                    "",
                    synthetic_status_summary,
                    "**Interpretation safeguard:** A `data_status` label is a declaration within the file, not independent proof of data provenance. When the file is confirmed to be synthetic demonstration data, all numerical results are illustrative and must not be presented as findings about real teachers, learners or schools."
                ])

                st.markdown("#### 6. Task-focused interpretation")
                st.markdown("\n".join(task_analysis_lines))
                task_analysis_text = "\n".join(task_analysis_lines) + "\n"
                st.download_button(
                    "Download task-focused interpretation (Markdown)",
                    data=task_analysis_text.encode("utf-8"),
                    file_name="geaa_task_focused_interpretation.md",
                    mime="text/markdown",
                    key="research_data_task_interpretation_download"
                )

                synthetic_report_warning = (
                    "**SYNTHETIC DEMONSTRATION DATA — NOT EMPIRICAL RESEARCH EVIDENCE.** "
                    "All numerical results are illustrative and must not be interpreted as findings "
                    "about real teachers, learners or schools."
                )
                if (
                    data_status_col in data.columns
                    and synthetic_status_summary is not None
                    and row_count > 0
                ):
                    status_values = data[data_status_col].astype("string").str.strip().str.upper()
                    nonblank_status = status_values.dropna()
                    if (
                        len(nonblank_status) == row_count
                        and int((nonblank_status == synthetic_label).sum()) == row_count
                    ):
                        synthetic_report_warning += (
                            " The uploaded file labels every record SYNTHETIC_NOT_REAL; "
                            "this label is not independent verification of provenance."
                        )
                    else:
                        synthetic_report_warning = (
                            "**DATA PROVENANCE NOT VERIFIED.** Do not assume this dataset is real or synthetic "
                            "based on a status-label check alone. Verify provenance before interpreting results."
                        )
                else:
                    synthetic_report_warning = (
                        "**DATA PROVENANCE NOT VERIFIED.** No complete SYNTHETIC_NOT_REAL label check was "
                        "available. Verify provenance before interpreting results."
                    )

                report_lines = [
                    "# GEAA Research Data — Exploratory Report",
                    "",
                    synthetic_report_warning,
                    "",
                    f"- **Source file:** {uploaded_file.name}",
                    f"- **Rows:** {row_count}",
                    f"- **Columns:** {column_count}",
                    f"- **Duplicate rows:** {duplicate_rows}",
                    f"- **Missing cells:** {missing_cells}",
                    f"- **Numeric variables detected:** {len(numeric_columns)}",
                    f"- **Non-numeric variables detected:** {len(categorical_columns)}",
                    "",
                    "## Data-quality notes",
                    "- Review variable names, units, coding, ranges and missingness before substantive interpretation.",
                    "- Duplicate rows are flagged for review, not automatically deleted.",
                    "- Missing values are reported but not imputed.",
                    "- Numeric columns are identified from their imported data types; categorical codes may need recoding.",
                    "",
                    "## Interpretation limits",
                    "- This report describes the uploaded file only; representativeness and data provenance are not verified.",
                    "- Descriptive statistics and correlations do not establish causation.",
                    "- Choose inferential tests only after specifying the research question, unit of analysis, sampling design and assumptions.",
                ]
                report_lines.extend(["", "## Categorical frequency summary"])
                if categorical_columns:
                    report_lines.extend([
                        f"Selected variable: **{selected_category}**",
                        "",
                        "| Category | Frequency | Percentage |",
                        "|---|---:|---:|"
                    ])
                    for _, frequency_row in frequencies.iterrows():
                        category_label = str(frequency_row["Category"]).replace("|", "\\|")
                        report_lines.append(
                            f"| {category_label} "
                            f"| {int(frequency_row['Frequency'])} "
                            f"| {float(frequency_row['Percentage']):.1f}% |"
                        )
                else:
                    report_lines.append("No non-numeric categorical variables were detected.")

                if len(numeric_columns) >= 2:
                    report_lines.extend([
                        "",
                        "## Exploratory Pearson correlation matrix",
                        "",
                        "These correlations describe linear associations and do not establish causation.",
                        "",
                        "| Variable | " + " | ".join(str(col) for col in correlation.columns) + " |",
                        "|---|" + "---:|" * len(correlation.columns)
                    ])
                    for variable, corr_row in correlation.round(3).iterrows():
                        report_lines.append(
                            "| " + str(variable) + " | "
                            + " | ".join(
                                "" if pd.isna(value) else f"{value:.3f}"
                                for value in corr_row
                            ) + " |"
                        )

                report_lines.extend(["", *task_analysis_lines])
                report_text = "\n".join(report_lines) + "\n"
                st.markdown("#### 7. Download report and data-quality profile")
                st.download_button(
                    "Download exploratory report (Markdown)",
                    data=report_text.encode("utf-8"),
                    file_name="geaa_research_data_report.md",
                    mime="text/markdown",
                    key="research_data_report_download"
                )
                st.download_button(
                    "Download data-quality profile (CSV)",
                    data=quality.to_csv(index=False).encode("utf-8"),
                    file_name="geaa_data_quality_profile.csv",
                    mime="text/csv",
                    key="research_data_quality_download"
                )
                st.success("Local exploratory analysis completed. Review the data and methodological limitations before drawing conclusions.")

            except Exception as e:
                st.error("Research Data analysis could not be completed.")
                with st.expander("Technical details"):
                    st.code(str(e))

    else:

        if uploaded_data is not None:
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

                    reasons = item.get(
                        "retrieval_reasons",
                        []
                    )

                    if reasons:

                        st.markdown(
                            "**Why this section was retrieved:**"
                        )

                        for reason in reasons:
                            st.write(
                                f"• {reason}"
                            )

            else:
                st.write(
                    "No relevant knowledge was retrieved."
                )
        st.write("### 📚 Retrieved Text Passed to GEAA")

        if retrieved_knowledge.strip():
            st.text(retrieved_knowledge)
        else:
            st.write("No retrieved knowledge was passed to GEAA.")


        if task.strip():
            full_instructions = (
                GEAA_INSTRUCTIONS
                + "\n\nSELECTED MODE:\n"
                + mode
                + "\n\nMODE WORKFLOW:\n"
                + workflows[mode]
                + r"""

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

    8. RESEARCH DESIGN AND STATISTICAL REASONING

    For research tasks, apply the following methodological checks
    when relevant to the user's question.

    A. UNIT OF ANALYSIS AND LEVELS OF MEASUREMENT
    Identify the proposed unit of analysis, such as teachers,
    students, classes, or schools. Distinguish the unit at which
    each variable is measured. If the unit of analysis is unclear,
    state this and explain why it matters.

    B. LINKAGE BETWEEN VARIABLES
    When explanatory variables and outcomes are measured at
    different levels, identify how the observations would be linked.
    For example, teacher-level digital competence and student-level
    achievement require a defensible way to associate students with
    the teachers whose instruction they receive. Do not assume that
    such linkage or data is available.

    C. NESTED AND CLUSTERED DATA
    Consider whether observations may be nested within classes,
    teachers, or schools. Explain that observations within the same
    group may not be statistically independent. Treat multilevel
    analysis as a possible option when justified by the sampling
    design, data structure, number of groups, and available sample
    size. Do not recommend it automatically.

    D. ALIGNMENT OF RESEARCH QUESTION AND METHOD
    Recommend a statistical or qualitative method only after
    considering the research question, study design, measurement
    level, sampling strategy, and available data. Correlation or
    regression may be appropriate for some associational questions;
    multilevel methods may be appropriate for suitably structured
    nested data. Explain relevant assumptions and limitations.

    E. ASSOCIATION AND CAUSATION
    Do not interpret an observed association as proof of causation.
    Identify plausible confounding factors where relevant, but do
    not assume that adjusting for selected variables eliminates
    all confounding or establishes causal effects.

    F. EVIDENCE AND UNCERTAINTY
    Label methodological recommendations as PROPOSED, general
    methodological principles as GENERAL KNOWLEDGE when they are
    not supported by retrieved knowledge, and unresolved design
    details as NEEDS VERIFICATION. Do not invent sample sizes,
    data linkage arrangements, validated instruments, model results,
    or evidence that a proposed method is feasible.

    G. SOURCE-LABEL ACCURACY

    Apply source labels according to the actual origin of each claim.

    1. Use UPLOADED-DATA only when the user has actually
    provided a dataset or other relevant uploaded evidence.
    Do not use this label for hypothetical data, missing data,
    or proposed data-collection arrangements.

    2. Distinguish the setting from the target population.
    If the question names public secondary schools in Kilifi
    County, identify that as the QUESTION-PROVIDED setting.
    Do not automatically treat all teachers or students in
    that setting as the confirmed target population, sampling
    frame, or study participants.

    3. Distinguish explicitly stated information from inference.
    Use QUESTION-PROVIDED for information directly stated
    in the research question. Use INFERRED for reasonable
    interpretations not explicitly stated. Use PROPOSED for
    recommended designs, procedures, variables, or analyses.
    Use NEEDS VERIFICATION for unresolved information.

    4. Do not combine source labels merely to make an answer
    appear better supported. If a statement contains both
    provided information and a proposed recommendation,
    separate the statement into clearly labelled parts.

    5. For teacher-level and student-level variables, identify
    the proposed unit of analysis and explain how records
    would be linked. Label the linkage procedure PROPOSED
    and NEEDS VERIFICATION unless the user has supplied
    evidence establishing that the linkage exists.

    6. Never describe a proposed sampling frame, instrument,
    dataset, school record, or data-linkage arrangement as
    already available unless the user has confirmed its
    availability.

    7. Before finalizing a research response, check that every
    source label accurately reflects the evidence available
    in the current task, uploaded files, and retrieved
    knowledge. Do not imply that retrieval proves a claim
    when the retrieved material only provides general guidance.

    8. When a research question explicitly names variables,
    label those variables QUESTION-PROVIDED. Use KNOWLEDGE-BASE
    only for definitions, classifications, or methodological
    principles actually supported by the retrieved text.

    9. Distinguish a general measurement principle from a
    specific measurement decision. A requirement to define
    and justify a measure may be KNOWLEDGE-BASE, while the
    choice of an instrument, examination score, or assessment
    procedure is PROPOSED and may require verification.

    10. Distinguish measurement level, unit of analysis, and
    data structure. Do not present several possible units of
    analysis as if they were a single established decision.
    Explain which choices remain unresolved and why.

    11. Recommend a statistical model only conditionally.
    Explain the design and data requirements that would make
    the model suitable. Do not assume that multilevel modelling
    is necessary merely because students attend different
    schools or share teachers.

    H. SOURCE PROVENANCE AND CONTEXTUAL CALIBRATION

    1. Distinguish the origin of each substantive claim:
       - QUESTION-PROVIDED: Explicitly supplied in the user's current task.
       - KNOWLEDGE-BASE: Supported by the retrieved GEAA knowledge presented to the model.
       - GENERAL KNOWLEDGE: Established general disciplinary or methodological knowledge not specifically supported by the retrieved material.
       - PROPOSED: A suggested measurement, method, variable, explanation, or next step that has not been established as a fact about the user's study.
       - INFERRED: A reasonable interpretation that follows from the question but was not explicitly supplied.
       - NEEDS VERIFICATION: Information that must be confirmed before it can be treated as established.

    2. Do not confuse a concept with its measurement. When a user supplies a variable, label the variable QUESTION-PROVIDED. Label suggested instruments, indicators, operational definitions, and data-collection methods PROPOSED. Label the validity, reliability, availability, or suitability of a specific instrument NEEDS VERIFICATION unless supporting evidence is available.

    3. Do not present inferred context as verified local evidence. Potential effects, contextual conditions, administrative practices, population characteristics, and geographical explanations must not be described as established facts about a named county, school, institution, or population unless the supplied or retrieved evidence supports them. Present plausible but unverified explanations as PROPOSED and identify what requires verification.

    4. Calibrate methodological recommendations to the available design information. Do not assume that teacher and student records can be linked, that a sampling frame exists, or that observations are clustered in a particular way. Explain the relevant condition and label the recommendation PROPOSED or NEEDS VERIFICATION where appropriate. Recommend multilevel modelling only when the sampling structure, number of groups, and available data make it potentially appropriate.

    5. Distinguish retrieved support from supplementary explanation. When retrieved knowledge supports a claim, use KNOWLEDGE-BASE. When adding a scientifically or methodologically sound explanation that is not stated in the retrieved text, use GENERAL KNOWLEDGE. Do not label an entire mixed statement KNOWLEDGE-BASE if only part of it is supported by the retrieved material.

    6. Use source labels only where they clarify the evidence status. Avoid contradictory or redundant combinations of labels. Briefly explain uncertainty when material, and do not invent citations, research findings, local facts, data availability, or instrument validation.

    12. GENERAL KNOWLEDGE AND EXTERNAL EVIDENCE

    When no relevant knowledge has been retrieved, distinguish
    general methodological reasoning from verified research
    evidence.

    Do not claim to have consulted research literature,
    official reports, regulations, or administrative records
    unless those sources were actually supplied or consulted.

    Label plausible but unverified local, institutional, or
    context-specific claims NEEDS VERIFICATION.

    Do not invent citations, study findings, statistics,
    administrative boundaries, policy requirements, or local
    conditions.

    For research questions about factors associated with an
    outcome, distinguish the outcome inferred from the question
    from proposed explanatory variables and proposed measures.

    Define the outcome operationally before recommending
    data collection. Where relevant, identify distinctions
    that could affect measurement, such as authorised versus
    unauthorised absence or absence from school versus absence
    from assigned teaching duties.

    13. FORMATTING AND EVIDENCE CALIBRATION

    Use clean Markdown formatting. Do not emit literal HTML
    tags such as <br>, escaped HTML tags, or raw formatting
    instructions in the final answer. Use Markdown paragraphs,
    lists, and tables where appropriate.

    State general methodological principles accurately and
    conditionally. Do not imply that a method is universally
    required or commonly used unless that claim is supported.
    Distinguish statistical principles from claims about the
    frequency or effectiveness of particular methods.

    When references have not been consulted, do not imply that
    the answer is a literature review. Identify claims that
    need verification through relevant research or official
    sources.

    9. EXPLICIT SOURCE LABELING
    Every substantive claim that is not directly provided by the
    USER TASK, UPLOADED DATA, or RETRIEVED GEAA KNOWLEDGE must be
    clearly labelled.

    If a statement comes from the model's general knowledge rather
    than the GEAA knowledge base, label it GENERAL KNOWLEDGE.

    Do not introduce external frameworks, policies, programmes,
    definitions, regulations, instruments, or named organizations
    without identifying them as GENERAL KNOWLEDGE and, where
    appropriate, NEEDS VERIFICATION.

    For research tasks, maintain a clear distinction between:
    - QUESTION-PROVIDED
    - UPLOADED-DATA
    - KNOWLEDGE-BASE
    - GENERAL KNOWLEDGE
    - INFERRED
    - PROPOSED
    - NEEDS VERIFICATION

    14. MATHEMATICAL NOTATION AND SOURCE ATTRIBUTION REFINEMENTS


    A. MATHEMATICAL NOTATION

    1. Keep mathematical expressions complete, readable, and correctly formatted. Do not split symbols, subscripts, or equations across lines unnecessarily.

    2. In Streamlit Markdown responses, use supported inline mathematical notation consistently. Examples: $E_a$, $\Delta H$, $\Delta G$, and Pearson's $r$.

    3. Keep short inline expressions together. Put longer equations on separate lines only when necessary.

    4. If mathematical rendering is unreliable, prefer readable plain-text notation. Keep expressions complete and correctly formatted; never leave duplicated, fragmented, or malformed mathematical notation.

    5. Apply chemistry-specific guidance only when the user's task is about chemistry, chemical reactions, catalysts, or energy-profile diagrams. For those tasks, ensure diagram labels and explanations agree: a catalyst lowers activation energy but does not change the overall enthalpy change, and reactant and product energy levels remain the same for catalysed and uncatalysed pathways. Do not introduce chemistry equations, examples, or energy-profile guidance into unrelated tasks.

    6. Do not place the entire response inside a code block or use a fenced math block. Preserve Markdown headings, bullet points, and source-attribution labels.

    B. SOURCE ATTRIBUTION REFINEMENTS

    1. Use KNOWLEDGE-BASE only when the retrieved text supplied to the model supports the claim.

    2. Use GENERAL KNOWLEDGE for established disciplinary principles that are not explicitly supported by the retrieved text.

    3. When a response combines retrieved information and supplementary knowledge, distinguish the claims clearly. Do not label an entire paragraph KNOWLEDGE-BASE if only some claims are supported by the retrieved material.

    4. A claim being scientifically correct does not mean it appears in the retrieved knowledge base. Do not invent citations or attribute unsupported claims to a retrieved document.

    5. Keep source labels accurate without making the answer unnecessarily repetitive. Preserve the scientific meaning of the retrieved material.
    """
            )

            with st.spinner("GEAA is working through the task..."):

                try:
                    # Prepare uploaded data for Gemini.
                    # Unlike Research Data mode, this general workflow can send
                    # uploaded dataset rows to Gemini, so disclose that clearly.
                    data_context = ""

                    if uploaded_data is not None:
                        st.warning(
                            "Data-handling notice: this mode may send the contents "
                            "of the uploaded dataset to Gemini. Do not upload "
                            "identifiable or confidential participant data unless "
                            "the applicable privacy requirements and service "
                            "arrangements permit it."
                        )

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
                    response, model_used = generate_content_with_fallback(
                        client,
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
                        ),
                    )

                    if model_used == FALLBACK_MODEL:
                        st.info(
                            "The primary Gemini model was temporarily unavailable. "
                            "GEAA verified access to the backup model and generated "
                            "this response using Gemini 3.8 Flash."
                        )

                    st.markdown("### GEAA's Response")
                    st.markdown(response.text, unsafe_allow_html=False)

                    st.download_button(
                        label="📥 Download editable PowerPoint",
                        data=create_geaa_presentation(response.text),
                        file_name="GEAA_presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        key="download_geaa_presentation"
                    )

                except GeminiFallbackError as e:
                    fallback_category = classify_gemini_error(e.fallback_error)
                    if e.stage == "verification":
                        if fallback_category == "authentication":
                            st.error(
                                "The primary Gemini model returned 503. GEAA could "
                                "not verify access to the backup model. Check that "
                                "GEMINI_API_KEY is valid and permitted to use "
                                "Gemini 3.8 Flash."
                            )
                        elif fallback_category == "rate_limited":
                            st.error(
                                "The primary Gemini model returned 503, and Google's "
                                "API rate-limited the backup-model access check. "
                                "Wait and try again."
                            )
                        else:
                            st.error(
                                "The primary Gemini model returned 503. GEAA could "
                                "not verify that the backup model is available to "
                                "this API key. See technical details."
                            )
                    elif fallback_category == "rate_limited":
                        st.error(
                            "The primary model returned 503, but the backup request "
                            "was rate-limited or quota-limited (HTTP 429). Check "
                            "your Gemini API usage and try again later."
                        )
                    elif fallback_category == "authentication":
                        st.error(
                            "The primary model returned 503, but Google rejected "
                            "the backup request. Check the API key and model access."
                        )
                    else:
                        st.error(
                            "The primary Gemini model returned 503 and the backup "
                            "model could not complete the request. Please try again "
                            "later."
                        )

                    with st.expander("Technical details"):
                        st.code(str(e))

                except Exception as e:
                    if client is None:
                        st.error(
                            "GEAA cannot generate this response because the Gemini "
                            "API key is missing or unavailable. Check the app's "
                            "Secrets settings and confirm GEMINI_API_KEY is set. "
                            "Research Data mode and local analysis features remain "
                            "available without Gemini."
                        )
                    else:
                        category = classify_gemini_error(e)
                        if category == "rate_limited":
                            st.error(
                                "Gemini returned HTTP 429: the request was rate- "
                                "limited or the available quota was reached. "
                                "Check your API usage and try again later. "
                                "GEAA does not switch models for quota errors."
                            )
                        elif category == "authentication":
                            st.error(
                                "Gemini rejected the API key or its permissions. "
                                "Check GEMINI_API_KEY in Streamlit Secrets and "
                                "confirm that the key is active."
                            )
                        elif category == "service_unavailable":
                            st.error(
                                "Gemini remained unavailable (HTTP 503) after the "
                                "configured SDK retries. GEAA could not complete "
                                "the request. Please try again later."
                            )
                        elif category == "model_unavailable":
                            st.error(
                                "Google could not find the requested Gemini model "
                                "for this API key (HTTP 404). Check model availability."
                            )
                        else:
                            st.error(
                                "GEAA could not complete the Gemini request. "
                                "See technical details below."
                            )

                    with st.expander("Technical details"):
                        st.code(str(e))

        else:
            st.warning("Please enter a task first.")

st.divider()

APP_BUILD = "research-data-interpretation-4"

st.caption(
    f"GEAA v1.3 — George's Education & Analytics Agent · build: {APP_BUILD}"
)
