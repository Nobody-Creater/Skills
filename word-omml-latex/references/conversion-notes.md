# Conversion Notes

## Namespaces

OMML uses:

```xml
xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
```

WordprocessingML paragraphs use:

```xml
xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
```

An inline equation is usually an `m:oMath` element under a `w:p`. A display equation may be wrapped in `m:oMathPara`.

## Common OMML Elements

- `m:r` / `m:t`: math run text
- `m:f`: fraction, with `m:num` and `m:den`
- `m:sSup`: superscript, with `m:e` and `m:sup`
- `m:sSub`: subscript, with `m:e` and `m:sub`
- `m:sSubSup`: subscript plus superscript
- `m:rad`: radical, with optional `m:deg` and required `m:e`
- `m:m`: matrix, containing `m:mr` rows and `m:e` cells
- `m:d`: delimiter wrapper, with `m:dPr/m:begChr` and `m:dPr/m:endChr`

## Extending the Converter

Add support in both directions:

1. Add a failing test in `scripts/test_omml_latex.py`.
2. Extend `LatexParser` for LaTeX to OMML.
3. Extend `omml_node_to_latex` for OMML to LaTeX.
4. Run:

```powershell
python .\scripts\test_omml_latex.py
```

Use a real Word round trip for constructs that are visually sensitive, especially delimiters, equation arrays, accents, and n-ary operators with limits.
