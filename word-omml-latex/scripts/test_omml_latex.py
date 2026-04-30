import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))

from omml_latex import extract_omml_from_docx, latex_to_omml, omml_to_latex


class OmmlLatexConversionTests(unittest.TestCase):
    def test_latex_fraction_superscript_and_radical_to_valid_omml(self):
        omml = latex_to_omml(r"\frac{x^2}{\sqrt{y}}")

        root = ET.fromstring(omml)
        self.assertTrue(root.tag.endswith("oMath"))
        self.assertIn("<m:f>", omml)
        self.assertIn("<m:sSup>", omml)
        self.assertIn("<m:rad>", omml)

    def test_generated_omml_round_trips_to_latex(self):
        omml = latex_to_omml(r"\frac{x^2}{\sqrt{y}}")

        latex = omml_to_latex(omml)

        self.assertEqual(latex, r"\frac{x^{2}}{\sqrt{y}}")

    def test_subscript_and_superscript_round_trip(self):
        omml = latex_to_omml(r"x_i^2+\alpha")

        latex = omml_to_latex(omml)

        self.assertEqual(latex, r"x_{i}^{2}+\alpha")

    def test_extracts_equations_from_docx(self):
        omml = latex_to_omml(r"\sqrt{x}")
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f"<w:body><w:p><w:r><w:t>Formula:</w:t></w:r>{omml}</w:p></w:body>"
            "</w:document>"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            docx_path = Path(tmpdir) / "sample.docx"
            with zipfile.ZipFile(docx_path, "w") as docx:
                docx.writestr("word/document.xml", document_xml)

            extracted = extract_omml_from_docx(docx_path)

        self.assertEqual(len(extracted), 1)
        self.assertEqual(omml_to_latex(extracted[0]), r"\sqrt{x}")


if __name__ == "__main__":
    unittest.main()
