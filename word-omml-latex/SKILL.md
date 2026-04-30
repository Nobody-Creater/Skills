---
name: word-omml-latex
description: Convert Microsoft Word OMML equations and LaTeX math formulas in both directions. Use when Codex needs to extract equations from .docx files or raw m:oMath/m:oMathPara XML as LaTeX, generate Word-compatible OMML XML from LaTeX formulas, inspect or transform Office Math XML, or prepare equation fragments for insertion into Word documents.
---

# Word OMML LaTeX

## Overview

Use this skill to convert between Word Office Math Markup Language (OMML) and LaTeX math. Prefer the bundled Python script for deterministic conversion and use direct XML inspection for edge cases.

Bundled script: `scripts/omml_latex.py`

## Quick Start

Convert LaTeX to an OMML XML fragment:

```powershell
python .\scripts\omml_latex.py latex-to-omml "\frac{x^2}{\sqrt{y}}" -o equation.omml.xml
```

Convert raw OMML XML to LaTeX:

```powershell
python .\scripts\omml_latex.py omml-to-latex equation.omml.xml
```

Extract every equation from a `.docx` as LaTeX:

```powershell
python .\scripts\omml_latex.py omml-to-latex paper.docx --json -o equations.json
```

Generate display math wrapped in `m:oMathPara`:

```powershell
python .\scripts\omml_latex.py latex-to-omml "\sum_{i=1}^n x_i" --display
```

## Workflow

1. Identify the input form:
   - Use `latex-to-omml` for a LaTeX math string or UTF-8 text file.
   - Use `omml-to-latex` for raw OMML XML, XML containing `m:oMath`, or a `.docx` file.
2. Run the script from this skill directory or call its Python functions:
   - `latex_to_omml(latex: str, display: bool = False) -> str`
   - `omml_to_latex(omml_xml: str) -> str`
   - `extract_omml_from_docx(docx_path: Path) -> list[str]`
3. Validate the result:
   - Parse generated OMML with `xml.etree.ElementTree.fromstring`.
   - For Word insertion, place `<m:oMath>` directly in a Word paragraph (`w:p`), not inside a text run (`w:r`).
   - Open a copy of the `.docx` in Word when final visual fidelity matters.

## Supported Formula Shapes

The bundled converter handles common scientific formulas:

- Fractions: `\frac{a}{b}`, `\dfrac`, `\tfrac`
- Radicals: `\sqrt{x}`, `\sqrt[n]{x}`
- Subscripts and superscripts: `x_i`, `x^2`, `x_i^2`
- Greek letters and common operators/symbols such as `\alpha`, `\sum`, `\int`, `\leq`, `\times`
- Basic functions: `\sin`, `\cos`, `\log`, `\ln`, `\exp`, `\lim`
- Basic matrix environments: `matrix`, `pmatrix`, `bmatrix`, `Bmatrix`, `vmatrix`, `Vmatrix`
- Raw `.docx` equation extraction from `word/document.xml`

Unsupported LaTeX commands are preserved as literal text so they are visible for manual correction instead of being silently removed.

## DOCX Editing Notes

When inserting generated OMML into a Word document, edit the document XML deliberately:

- Unzip or unpack the `.docx`.
- Insert the generated `<m:oMath>` as a child of `<w:p>`.
- Ensure the document part declares the math namespace:
  `xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"`.
- Repack and validate the `.docx`.

For broader Word document editing, use the repository's DOCX workflow and keep equation conversion scoped to this skill.

## References

Read `references/conversion-notes.md` when adding support for new OMML or LaTeX constructs.
