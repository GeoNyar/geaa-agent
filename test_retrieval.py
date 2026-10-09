
import ast
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP_FILE = ROOT / "app.py"
KNOWLEDGE_DIR = ROOT / "knowledge"


def load_retrieval_functions():
    """Load only the retrieval-related code, not the Streamlit app."""
    source = APP_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    namespace = {"re": re}

    required_functions = {
        "parse_knowledge_sections",
        "retrieve_knowledge",
    }
    found_functions = set()
    found_query_expansion = False

    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = (
                node.targets
                if isinstance(node, ast.Assign)
                else [node.target]
            )

            if any(
                isinstance(target, ast.Name)
                and target.id == "QUERY_EXPANSION"
                for target in targets
            ):
                code = ast.get_source_segment(source, node)
                exec(code, namespace)
                found_query_expansion = True

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in required_functions:
                code = ast.get_source_segment(source, node)
                exec(code, namespace)
                found_functions.add(node.name)

    missing = required_functions - found_functions

    if missing:
        raise RuntimeError(
            f"Could not find these functions in app.py: {sorted(missing)}"
        )

    if not found_query_expansion:
        raise RuntimeError(
            "Could not find the QUERY_EXPANSION assignment in app.py."
        )

    return namespace


def load_knowledge_documents(namespace):
    """Load the Markdown knowledge files using GEAA's existing parser."""
    documents = []

    if not KNOWLEDGE_DIR.is_dir():
        raise RuntimeError(
            f"Knowledge folder not found: {KNOWLEDGE_DIR}"
        )

    for filepath in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        filename_lower = filepath.name.lower()

        if "course_outline" in filename_lower:
            document_type = "course_outline"
        elif "notes" in filename_lower:
            document_type = "learning_notes"
        else:
            document_type = "general_knowledge"

        sections = namespace["parse_knowledge_sections"](
            content,
            document_type,
        )

        documents.append({
            "filename": filepath.name,
            "content": content,
            "document_type": document_type,
            "sections": sections,
        })

    return documents


class TestKnowledgeRetrieval(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.namespace = load_retrieval_functions()
        cls.documents = load_knowledge_documents(cls.namespace)
        cls.retrieve = cls.namespace["retrieve_knowledge"]

    def retrieve_text(self, query):
        text, selected = self.retrieve(query, self.documents)
        return text, selected

    def test_01_thermodynamics_fundamentals_rank_first(self):
        text, _ = self.retrieve_text("Explain thermodynamics.")

        self.assertIn("4.1 WHAT IS THERMODYNAMICS?", text)
        self.assertLess(
            text.find("4.1 WHAT IS THERMODYNAMICS?"),
            text.find("4.9 ACTIVATION ENERGY AND THERMODYNAMICS")
            if "4.9 ACTIVATION ENERGY AND THERMODYNAMICS" in text
            else len(text),
        )

    def test_02_hess_law_is_retrieved(self):
        text, _ = self.retrieve_text(
            "Explain Hess's Law and how it is used to calculate "
            "enthalpy change."
        )

        self.assertIn("4.18 HESS'S LAW", text)

    def test_03_activation_energy_and_catalyst_are_retrieved(self):
        text, _ = self.retrieve_text(
            "Explain activation energy and how a catalyst affects "
            "the rate of reaction."
        )

        self.assertIn("4.9 ACTIVATION ENERGY", text)
        self.assertIn("4.10 EFFECT OF A CATALYST", text)

    def test_04_photosynthesis_retrieves_relevant_sections(self):
        text, _ = self.retrieve_text("Explain photosynthesis.")

        self.assertIn("4.5 ENDOTHERMIC REACTIONS", text)
        self.assertIn(
            "4.6 COMPARING EXOTHERMIC AND ENDOTHERMIC REACTIONS",
            text,
        )
        self.assertIn("4.21 THERMODYNAMICS AND BIOCHEMISTRY", text)

    def test_05_education_research_does_not_retrieve_chemistry(self):
        text, selected = self.retrieve_text(
            "What is the relationship between teacher digital "
            "competence and student achievement in public secondary "
            "schools in Kilifi County?"
        )

        self.assertEqual(text.strip(), "")
        self.assertEqual(selected, [])

    def test_06_soil_erosion_does_not_retrieve_irrelevant_knowledge(self):
        text, selected = self.retrieve_text(
            "Explain the causes of soil erosion."
        )

        self.assertEqual(text.strip(), "")
        self.assertEqual(selected, [])

    def test_07_respiration_retrieves_relevant_energy_content(self):
        text, _ = self.retrieve_text(
            "How can thermodynamics explain energy changes during "
            "respiration?"
        )

        self.assertTrue(
            "4.21 THERMODYNAMICS AND BIOCHEMISTRY" in text
            or "4.1 WHAT IS THERMODYNAMICS?" in text,
            "Expected relevant thermodynamics or biochemistry content.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
