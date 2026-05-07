---
name: reference-verification
description: Verify and repair academic references in Word or LaTeX manuscripts. Use when Codex needs to check whether in-text citations support the manuscript's claims, reconcile citations with the reference list or .bib/.bbl files, strictly apply a supplied reference style from an image/document/template/journal guide, correct malformed references, or search authoritative online sources for missing bibliographic metadata. Triggers include citation support, reference format, BibTeX, .bib, .bbl, .tex, .docx, and reference-list cleanup.
---

# Reference Verification

## Core Rule

Treat reference checking as two separate tasks that must both pass:

1. **Citation support**: each cited source must actually support the specific sentence, clause, data point, method attribution, or comparison that cites it.
2. **Reference integrity**: each reference-list entry must contain correct metadata and match the required style exactly.

Do not infer missing bibliographic facts from memory. When information is incomplete, inconsistent, or likely to have changed, search authoritative sources and record the source used. If the information cannot be verified, mark it unresolved instead of inventing it.

## Inputs

Collect or infer these before editing:

- Manuscript source: `.docx`, `.tex`, `.bib`, `.bbl`, compiled PDF, or a folder containing LaTeX sources.
- Required reference style: uploaded image, sample references, journal template, author guideline, previous accepted paper, or explicit style name.
- Editing target: revised manuscript, revised `.bib`, audit report only, tracked changes, or direct edits.

If the style source is missing and the user asks for formatting, ask for it unless a target journal/style is explicitly named and can be verified from authoritative instructions.

## Workflow

### 1. Preserve and Extract

- Work on a copy unless the user explicitly requests in-place edits.
- For Word manuscripts, use document-aware extraction; include body text, captions, tables, footnotes/endnotes, and comments when relevant. Preserve citation fields from Zotero, EndNote, Mendeley, or Word fields where possible; do not flatten live citation fields unless the user approves.
- For LaTeX manuscripts, parse citation commands including `\cite`, `\citep`, `\citet`, `\autocite`, `\parencite`, `\textcite`, optional arguments, multi-key citations, and compressed numeric ranges. Map keys to `.bib`; if no `.bib` exists, use `.bbl` or the compiled reference list.
- Exclude the reference section itself when collecting in-text citations.
- Build an inventory with: citation location, citation marker/key, surrounding sentence, cited reference entry, and first-appearance order.

### 2. Check Citation-Reference Consistency

Verify these mechanically before judging support:

- Every in-text citation resolves to exactly one reference-list or BibTeX entry.
- Every cited key/number/author-year label is present and not duplicated.
- Every reference-list entry is cited, unless the target style allows uncited bibliography items.
- Numeric styles follow the required ordering rule, usually first appearance for IEEE/Vancouver unless the supplied style says otherwise.
- Author-year citations match author names and years in the reference list.
- Citation ranges and grouped citations expand correctly and do not hide missing references.

Record mismatches separately from evidence problems.

### 3. Verify Whether References Support Claims

For each cited claim:

- Identify the exact proposition being supported: background fact, definition, method origin, dataset use, numerical result, comparison, limitation, or prior-work attribution.
- Read enough of the cited work to test the proposition. Prefer the paper itself, publisher page, DOI landing page, PubMed/PMC, arXiv, IEEE/ACM/Springer/Elsevier pages, official standards, or official datasets. Abstract-only evidence is acceptable only when the claim is fully supported by the abstract.
- Classify support as:
  - `Supported`: the source directly supports the claim.
  - `Partially supported`: the source supports a weaker, broader, or adjacent claim.
  - `Unsupported`: the source does not support the claim.
  - `Wrong source`: another cited or known source is more appropriate.
  - `Cannot verify`: full text or reliable metadata is unavailable.
- For unsupported or partially supported claims, propose one concrete fix: revise the claim, replace/add a citation, split the sentence, narrow the wording, or mark for author review.
- Do not let a source title alone count as evidence. For quantitative values, equations, algorithm details, or "first/best/state-of-the-art" claims, verify the exact value or wording against the source.

### 4. Derive the Required Reference Style

Before editing references, convert the supplied format example into explicit rules:

- Entry order: citation order, alphabetical, chronological, or grouped by type/language.
- Numbering and indentation: bracket style, hanging indent, spacing after number, line spacing.
- Author format: surname order, initials, full names, separators, final delimiter, `et al.` threshold, capitalization.
- Title format: sentence case/title case, quotation marks, italics, translated titles, capitalization after colon.
- Container format: journal/conference/book names, abbreviations, italics, proceedings wording.
- Publication fields: year position, volume, issue, article number, pages, publisher, city, edition.
- DOI/URL/arXiv/PubMed fields: required or omitted, prefix format, access date requirements.
- Punctuation: commas, periods, colons, parentheses, spaces, en-dashes or hyphens in page ranges.
- Special cases: Chinese GB/T-style entries, bilingual references, patents, standards, datasets, preprints, dissertations, websites, software, and online-first articles.

If examples conflict, follow the closest matching entry type and flag the ambiguity in the audit report.

### 5. Complete and Correct Bibliographic Metadata

For every reference entry:

- Prefer DOI-based lookup when available.
- Search authoritative sources for missing or suspicious fields. Use Crossref, DataCite, PubMed, DOI.org, publisher pages, arXiv, IEEE, ACM, official standards bodies, official dataset/software pages, or the work's official repository.
- Verify at least: authors, title, venue, year, volume/issue, pages or article number, DOI/URL, and publication type.
- Normalize journal abbreviations only if the target style requires abbreviations; use a reliable abbreviation source when possible.
- Keep original language where required. Do not translate titles unless the style requires translated titles.
- Preserve identifiers that are useful for future maintenance in BibTeX, such as `doi`, `url`, `eprint`, `archivePrefix`, and `primaryClass`, unless the target style forbids them in the rendered list.

If reliable sources disagree, prefer the publisher/DOI record for formal metadata and note the disagreement.

### 6. Edit Safely

- For Word output, update the reference list and citation labels without breaking fields. If citation-manager fields control the bibliography, prefer editing the source library/exported data or provide exact changes for the user to refresh the bibliography.
- For LaTeX output, edit `.bib` entries for metadata and style-independent fields; edit `.bst`, package options, or reference text only when the requested style cannot be achieved through normal BibTeX/Biber settings.
- Keep edits narrowly scoped to references and citation text unless a claim must be rewritten to match evidence.
- For each change, preserve enough audit detail to explain why it was made.

### 7. Validate After Editing

Re-extract citations and references after edits and check:

- No unresolved in-text citations remain.
- No required references are missing.
- No new duplicate entries or duplicate labels were introduced.
- Reference ordering and numbering match the target style.
- Formatting is consistent across all entry types.
- LaTeX compiles or Word opens cleanly when feasible.

When compilation or document validation cannot be run, state that explicitly.

## Deliverables

Provide the edited file(s) and a concise audit report with:

- Citation-reference consistency issues and fixes.
- Claim-support findings, grouped by severity.
- Reference-format corrections made.
- Metadata fields searched and source URLs used.
- Unresolved items with the reason they could not be verified.

Use exact locations whenever possible: section, paragraph, page, citation key, reference number, or BibTeX key.

## Quality Bar

- Do not silently replace a citation simply because another source seems better; explain the reason.
- Do not remove references only because they are uncited without confirming the target style and manuscript intent.
- Do not fabricate page ranges, issue numbers, DOIs, author initials, or access dates.
- Do not treat reference formatting as complete until every entry type in the manuscript has been checked against the derived style rules.
