#!/usr/bin/env python
"""Convert common Word OMML equations to and from LaTeX.

This intentionally uses only the Python standard library so the skill remains
usable on machines without Pandoc or extra Python packages. It covers common
scientific equation structures and keeps unsupported LaTeX commands visible as
literal text instead of dropping them.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable, List, Optional
from xml.etree import ElementTree as ET


M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"m": M_NS, "w": W_NS}

ET.register_namespace("m", M_NS)


GREEK = {
    "alpha": "\u03b1",
    "beta": "\u03b2",
    "gamma": "\u03b3",
    "delta": "\u03b4",
    "epsilon": "\u03f5",
    "varepsilon": "\u03b5",
    "zeta": "\u03b6",
    "eta": "\u03b7",
    "theta": "\u03b8",
    "vartheta": "\u03d1",
    "iota": "\u03b9",
    "kappa": "\u03ba",
    "lambda": "\u03bb",
    "mu": "\u03bc",
    "nu": "\u03bd",
    "xi": "\u03be",
    "pi": "\u03c0",
    "varpi": "\u03d6",
    "rho": "\u03c1",
    "varrho": "\u03f1",
    "sigma": "\u03c3",
    "varsigma": "\u03c2",
    "tau": "\u03c4",
    "upsilon": "\u03c5",
    "phi": "\u03d5",
    "varphi": "\u03c6",
    "chi": "\u03c7",
    "psi": "\u03c8",
    "omega": "\u03c9",
    "Gamma": "\u0393",
    "Delta": "\u0394",
    "Theta": "\u0398",
    "Lambda": "\u039b",
    "Xi": "\u039e",
    "Pi": "\u03a0",
    "Sigma": "\u03a3",
    "Upsilon": "\u03a5",
    "Phi": "\u03a6",
    "Psi": "\u03a8",
    "Omega": "\u03a9",
}

SYMBOLS = {
    "cdot": "\u22c5",
    "times": "\u00d7",
    "div": "\u00f7",
    "pm": "\u00b1",
    "mp": "\u2213",
    "leq": "\u2264",
    "le": "\u2264",
    "geq": "\u2265",
    "ge": "\u2265",
    "neq": "\u2260",
    "ne": "\u2260",
    "approx": "\u2248",
    "sim": "\u223c",
    "infty": "\u221e",
    "partial": "\u2202",
    "nabla": "\u2207",
    "sum": "\u2211",
    "prod": "\u220f",
    "int": "\u222b",
    "oint": "\u222e",
    "in": "\u2208",
    "notin": "\u2209",
    "subset": "\u2282",
    "subseteq": "\u2286",
    "cup": "\u222a",
    "cap": "\u2229",
    "rightarrow": "\u2192",
    "to": "\u2192",
    "leftarrow": "\u2190",
    "leftrightarrow": "\u2194",
    "Rightarrow": "\u21d2",
    "Leftarrow": "\u21d0",
    "Leftrightarrow": "\u21d4",
}

REVERSE_SYMBOLS = {value: "\\" + key for key, value in GREEK.items()}
REVERSE_SYMBOLS.update({value: "\\" + key for key, value in SYMBOLS.items()})
FUNCTION_NAMES = {"sin", "cos", "tan", "log", "ln", "exp", "lim", "max", "min"}


class LatexSyntaxError(ValueError):
    """Raised when a LaTeX formula cannot be parsed by this converter."""


def mtag(name: str) -> str:
    return "{" + M_NS + "}" + name


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def make_run(text: str) -> ET.Element:
    run = ET.Element(mtag("r"))
    t = ET.SubElement(run, mtag("t"))
    t.text = text
    return run


def make_container(name: str, children: Iterable[ET.Element]) -> ET.Element:
    node = ET.Element(mtag(name))
    node.extend(children)
    return node


def make_fraction(num: List[ET.Element], den: List[ET.Element]) -> ET.Element:
    frac = ET.Element(mtag("f"))
    frac.append(make_container("num", num))
    frac.append(make_container("den", den))
    return frac


def make_radical(body: List[ET.Element], degree: Optional[List[ET.Element]] = None) -> ET.Element:
    rad = ET.Element(mtag("rad"))
    if degree:
        rad.append(make_container("deg", degree))
    else:
        rad_pr = ET.SubElement(rad, mtag("radPr"))
        ET.SubElement(rad_pr, mtag("degHide"), {mtag("val"): "on"})
    rad.append(make_container("e", body))
    return rad


def make_scripted(
    base: List[ET.Element],
    sub: Optional[List[ET.Element]],
    sup: Optional[List[ET.Element]],
) -> ET.Element:
    if sub is not None and sup is not None:
        node = ET.Element(mtag("sSubSup"))
        node.append(make_container("e", base))
        node.append(make_container("sub", sub))
        node.append(make_container("sup", sup))
        return node
    if sub is not None:
        node = ET.Element(mtag("sSub"))
        node.append(make_container("e", base))
        node.append(make_container("sub", sub))
        return node
    if sup is not None:
        node = ET.Element(mtag("sSup"))
        node.append(make_container("e", base))
        node.append(make_container("sup", sup))
        return node
    raise ValueError("Either sub or sup is required")


def make_matrix(rows: List[List[List[ET.Element]]]) -> ET.Element:
    matrix = ET.Element(mtag("m"))
    for row in rows:
        mr = ET.SubElement(matrix, mtag("mr"))
        for cell in row:
            mr.append(make_container("e", cell))
    return matrix


def strip_math_delimiters(latex: str) -> str:
    text = latex.strip()
    pairs = [
        (r"\(", r"\)"),
        (r"\[", r"\]"),
        ("$$", "$$"),
        ("$", "$"),
    ]
    for left, right in pairs:
        if text.startswith(left) and text.endswith(right) and len(text) >= len(left) + len(right):
            return text[len(left) : len(text) - len(right)].strip()
    return text


class LatexParser:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0

    def parse(self) -> List[ET.Element]:
        nodes = self.parse_until(None)
        self.skip_spaces()
        if self.pos != len(self.source):
            raise LatexSyntaxError("Unexpected trailing LaTeX near: " + self.source[self.pos :])
        return nodes

    def parse_until(self, stop: Optional[str]) -> List[ET.Element]:
        nodes = []
        while self.pos < len(self.source):
            self.skip_spaces()
            if self.pos >= len(self.source):
                break
            if stop and self.source[self.pos] == stop:
                break
            if self.source[self.pos] == "}":
                if stop == "}":
                    break
                raise LatexSyntaxError("Unmatched closing brace")

            atom = self.parse_atom()
            if not atom:
                continue
            nodes.extend(self.parse_scripts(atom))
        return nodes

    def parse_atom(self) -> List[ET.Element]:
        ch = self.peek()
        if ch is None:
            return []
        if ch == "{":
            return self.parse_required_group()
        if ch == "\\":
            return self.parse_command()
        if ch in "^_":
            raise LatexSyntaxError("Script marker has no base near: " + self.source[self.pos :])
        self.pos += 1
        return [make_run(ch)]

    def parse_command(self) -> List[ET.Element]:
        self.expect("\\")
        command = self.read_command_name()

        if command in {"frac", "dfrac", "tfrac"}:
            return [make_fraction(self.parse_required_group(), self.parse_required_group())]
        if command == "sqrt":
            degree = self.parse_optional_bracket()
            return [make_radical(self.parse_required_group(), degree)]
        if command in {"text", "mathrm", "mathbf", "operatorname"}:
            return [make_run(self.read_required_group_raw())]
        if command == "begin":
            env = self.read_required_group_raw().strip()
            if env in {"matrix", "pmatrix", "bmatrix", "Bmatrix", "vmatrix", "Vmatrix"}:
                return [self.parse_matrix_environment(env)]
            return [make_run("\\begin{" + env + "}")]
        if command == "end":
            env = self.read_required_group_raw().strip()
            return [make_run("\\end{" + env + "}")]
        if command in {"left", "right"}:
            delimiter = self.read_delimiter_token()
            return [] if delimiter == "." else [make_run(delimiter)]
        if command in GREEK:
            return [make_run(GREEK[command])]
        if command in SYMBOLS:
            return [make_run(SYMBOLS[command])]
        if command in FUNCTION_NAMES:
            return [make_run(command)]
        if command in {" ", ",", ";", ":", "!", "quad", "qquad"}:
            return []

        return [make_run("\\" + command)]

    def parse_scripts(self, base: List[ET.Element]) -> List[ET.Element]:
        sub = None
        sup = None
        while True:
            self.skip_spaces()
            marker = self.peek()
            if marker not in {"_", "^"}:
                break
            self.pos += 1
            argument = self.parse_required_group()
            if marker == "_":
                sub = argument
            else:
                sup = argument
        if sub is None and sup is None:
            return base
        return [make_scripted(base, sub, sup)]

    def parse_required_group(self) -> List[ET.Element]:
        self.skip_spaces()
        if self.peek() == "{":
            self.pos += 1
            nodes = self.parse_until("}")
            self.expect("}")
            return nodes
        return self.parse_atom()

    def parse_optional_bracket(self) -> Optional[List[ET.Element]]:
        self.skip_spaces()
        if self.peek() != "[":
            return None
        self.pos += 1
        start = self.pos
        depth = 0
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            elif ch == "]" and depth == 0:
                content = self.source[start : self.pos]
                self.pos += 1
                return LatexParser(content).parse()
            self.pos += 1
        raise LatexSyntaxError("Unclosed optional bracket")

    def parse_matrix_environment(self, env: str) -> ET.Element:
        body = self.read_environment_body(env)
        rows = []
        for raw_row in split_top_level(body, row_separator=True):
            if not raw_row.strip():
                continue
            row = []
            for raw_cell in split_top_level(raw_row, row_separator=False):
                row.append(LatexParser(raw_cell).parse())
            rows.append(row)
        matrix = make_matrix(rows)
        if env == "pmatrix":
            return make_delimited("(", ")", [matrix])
        if env == "bmatrix":
            return make_delimited("[", "]", [matrix])
        if env == "Bmatrix":
            return make_delimited("{", "}", [matrix])
        if env == "vmatrix":
            return make_delimited("|", "|", [matrix])
        if env == "Vmatrix":
            return make_delimited("||", "||", [matrix])
        return matrix

    def read_environment_body(self, env: str) -> str:
        end_token = "\\end{" + env + "}"
        start = self.pos
        end = self.source.find(end_token, self.pos)
        if end == -1:
            raise LatexSyntaxError("Missing " + end_token)
        self.pos = end + len(end_token)
        return self.source[start:end]

    def read_required_group_raw(self) -> str:
        self.skip_spaces()
        self.expect("{")
        start = self.pos
        depth = 1
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch == "\\":
                self.pos += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    raw = self.source[start : self.pos]
                    self.pos += 1
                    return raw
            self.pos += 1
        raise LatexSyntaxError("Unclosed braced group")

    def read_delimiter_token(self) -> str:
        self.skip_spaces()
        if self.peek() == "\\":
            self.pos += 1
            name = self.read_command_name()
            return {
                "lbrace": "{",
                "rbrace": "}",
                "langle": "\u27e8",
                "rangle": "\u27e9",
            }.get(name, "\\" + name)
        ch = self.peek()
        if ch is None:
            return ""
        self.pos += 1
        return ch

    def read_command_name(self) -> str:
        if self.pos >= len(self.source):
            return ""
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isalpha():
            self.pos += 1
        if self.pos == start:
            self.pos += 1
        return self.source[start : self.pos]

    def skip_spaces(self) -> None:
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1

    def peek(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def expect(self, token: str) -> None:
        if not self.source.startswith(token, self.pos):
            raise LatexSyntaxError("Expected " + token + " near: " + self.source[self.pos :])
        self.pos += len(token)


def make_delimited(begin: str, end: str, body: List[ET.Element]) -> ET.Element:
    delimiter = ET.Element(mtag("d"))
    dpr = ET.SubElement(delimiter, mtag("dPr"))
    ET.SubElement(dpr, mtag("begChr"), {mtag("val"): begin})
    ET.SubElement(dpr, mtag("endChr"), {mtag("val"): end})
    delimiter.append(make_container("e", body))
    return delimiter


def split_top_level(source: str, row_separator: bool) -> List[str]:
    parts = []
    start = 0
    depth = 0
    i = 0
    while i < len(source):
        ch = source[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif row_separator and depth == 0 and source.startswith("\\\\", i):
            parts.append(source[start:i])
            i += 2
            start = i
            continue
        elif not row_separator and depth == 0 and ch == "&":
            parts.append(source[start:i])
            start = i + 1
        i += 1
    parts.append(source[start:])
    return parts


def latex_to_omml(latex: str, display: bool = False) -> str:
    """Return an OMML XML fragment for a LaTeX math expression."""
    formula = strip_math_delimiters(latex)
    math = ET.Element(mtag("oMath"))
    math.extend(LatexParser(formula).parse())
    if display:
        para = ET.Element(mtag("oMathPara"))
        para.append(math)
        return xml_to_string(para)
    return xml_to_string(math)


def omml_to_latex(omml_xml: str) -> str:
    """Return LaTeX for an OMML XML fragment or XML document containing OMML."""
    root = parse_xml_fragment(omml_xml)
    if local_name(root.tag) in {"oMath", "oMathPara"}:
        return omml_node_to_latex(root)

    equations = root.findall(".//m:oMath", NS)
    if equations:
        return "\n".join(omml_node_to_latex(eq) for eq in equations)
    return omml_node_to_latex(root)


def extract_omml_from_docx(docx_path: Path) -> List[str]:
    """Extract all m:oMath elements from a .docx file as OMML XML strings."""
    with zipfile.ZipFile(docx_path) as docx:
        document_xml = docx.read("word/document.xml")
    root = ET.fromstring(document_xml)
    return [xml_to_string(eq) for eq in root.findall(".//m:oMath", NS)]


def parse_xml_fragment(xml: str) -> ET.Element:
    text = xml.strip()
    text = re.sub(r"^\s*<\?xml[^>]*\?>", "", text).strip()
    try:
        return ET.fromstring(text)
    except ET.ParseError:
        wrapped = (
            '<root xmlns:m="' + M_NS + '" xmlns:w="' + W_NS + '">'
            + text
            + "</root>"
        )
        return ET.fromstring(wrapped)


def omml_node_to_latex(node: ET.Element) -> str:
    name = local_name(node.tag)

    if name == "oMathPara":
        equations = [child for child in node if local_name(child.tag) == "oMath"]
        return "\n".join(omml_node_to_latex(eq) for eq in equations)
    if name in {"oMath", "root", "e", "num", "den", "sub", "sup", "deg"}:
        return children_to_latex(node)
    if name == "r":
        return "".join(text_to_latex(t.text or "") for t in node.findall(".//m:t", NS))
    if name == "t":
        return text_to_latex(node.text or "")
    if name == "f":
        return "\\frac{" + child_latex(node, "num") + "}{" + child_latex(node, "den") + "}"
    if name == "sSup":
        return child_latex(node, "e") + "^{" + child_latex(node, "sup") + "}"
    if name == "sSub":
        return child_latex(node, "e") + "_{" + child_latex(node, "sub") + "}"
    if name == "sSubSup":
        return (
            child_latex(node, "e")
            + "_{"
            + child_latex(node, "sub")
            + "}^{"
            + child_latex(node, "sup")
            + "}"
        )
    if name == "rad":
        degree = child_latex(node, "deg")
        body = child_latex(node, "e")
        if degree:
            return "\\sqrt[" + degree + "]{" + body + "}"
        return "\\sqrt{" + body + "}"
    if name == "d":
        begin = property_value(node, "begChr", "(")
        end = property_value(node, "endChr", ")")
        return "\\left" + begin + child_latex(node, "e") + "\\right" + end
    if name == "m":
        return matrix_to_latex(node)
    if name == "nary":
        operator = property_value(node, "chr", "\u2211")
        latex = text_to_latex(operator)
        sub = child_latex(node, "sub")
        sup = child_latex(node, "sup")
        if sub:
            latex += "_{" + sub + "}"
        if sup:
            latex += "^{" + sup + "}"
        return latex + child_latex(node, "e")
    if name.endswith("Pr"):
        return ""
    return children_to_latex(node)


def children_to_latex(node: ET.Element) -> str:
    return "".join(omml_node_to_latex(child) for child in node if not local_name(child.tag).endswith("Pr"))


def child_latex(node: ET.Element, child_name: str) -> str:
    child = first_child(node, child_name)
    return omml_node_to_latex(child) if child is not None else ""


def first_child(node: ET.Element, child_name: str) -> Optional[ET.Element]:
    for child in node:
        if local_name(child.tag) == child_name:
            return child
    return None


def property_value(node: ET.Element, prop_name: str, default: str) -> str:
    for prop in node.findall(".//m:" + prop_name, NS):
        return prop.attrib.get(mtag("val"), default)
    return default


def matrix_to_latex(node: ET.Element) -> str:
    rows = []
    for row in [child for child in node if local_name(child.tag) == "mr"]:
        cells = [omml_node_to_latex(cell) for cell in row if local_name(cell.tag) == "e"]
        rows.append(" & ".join(cells))
    return "\\begin{matrix}" + r" \\ ".join(rows) + "\\end{matrix}"


def text_to_latex(text: str) -> str:
    pieces = []
    for ch in text:
        if ch in REVERSE_SYMBOLS:
            pieces.append(REVERSE_SYMBOLS[ch])
        elif ch in {"{", "}", "%", "#", "&"}:
            pieces.append("\\" + ch)
        else:
            pieces.append(ch)
    return "".join(pieces)


def xml_to_string(node: ET.Element) -> str:
    return ET.tostring(node, encoding="unicode", short_empty_elements=False)


def read_text_argument(value: Optional[str], input_path: Optional[str]) -> str:
    if input_path:
        return Path(input_path).read_text(encoding="utf-8")
    if value is None:
        return sys.stdin.read()
    return value


def write_output(text: str, output_path: Optional[str]) -> None:
    if output_path:
        Path(output_path).write_text(text, encoding="utf-8")
    else:
        print(text)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert Word OMML equations to and from LaTeX.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    latex_parser = subparsers.add_parser("latex-to-omml", help="Convert a LaTeX formula to OMML XML.")
    latex_parser.add_argument("latex", nargs="?", help="LaTeX formula. Reads stdin when omitted.")
    latex_parser.add_argument("-i", "--input", help="Read LaTeX from a UTF-8 text file.")
    latex_parser.add_argument("-o", "--output", help="Write OMML XML to this file.")
    latex_parser.add_argument("--display", action="store_true", help="Wrap result in m:oMathPara.")

    omml_parser = subparsers.add_parser("omml-to-latex", help="Convert OMML XML or .docx equations to LaTeX.")
    omml_parser.add_argument("input", help="OMML XML file or .docx file.")
    omml_parser.add_argument("-o", "--output", help="Write LaTeX to this file.")
    omml_parser.add_argument("--json", action="store_true", help="For .docx input, emit indexed JSON.")

    args = parser.parse_args(argv)

    if args.command == "latex-to-omml":
        latex = read_text_argument(args.latex, args.input)
        write_output(latex_to_omml(latex, display=args.display), args.output)
        return 0

    input_path = Path(args.input)
    if input_path.suffix.lower() == ".docx":
        equations = extract_omml_from_docx(input_path)
        rows = [{"index": index + 1, "latex": omml_to_latex(eq)} for index, eq in enumerate(equations)]
        output = json.dumps(rows, ensure_ascii=False, indent=2) if args.json else "\n".join(row["latex"] for row in rows)
    else:
        output = omml_to_latex(input_path.read_text(encoding="utf-8"))
    write_output(output, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
