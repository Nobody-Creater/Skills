---
name: reviewer-response-writing
description: Write academic paper reviewer response letters (审稿意见回复/回复审稿人/rebuttal/revision response/response letter/修改回复). Use whenever the user needs to draft, revise, or review a response-to-reviewers document for a journal or conference paper revision — whether a major revision (大修), minor revision (小修), or conference rebuttal. Also trigger when the user mentions "审稿意见", "审稿人", "reviewer comments", "response letter", "rebuttal letter", or asks to address reviewer feedback on a manuscript. Handles novelty challenges, missing-experiment requests, method-design questions, complexity/efficiency concerns, writing-quality feedback, and cross-reviewer coordination. Supports both LaTeX and Word manuscript contexts.
---

# Reviewer Response Writing

## Core Rules

Two immutable rules govern every response letter:

1. **Always grateful, never defensive.** Every response begins with gratitude. Disagreeing with a reviewer is acceptable but must be done with deferential language, specific evidence, and an offer to accommodate. Never use dismissive phrases like "the reviewer misunderstands" — instead say "we realize the description was unclear."

2. **Evidence anchors every claim.** Never make a vague claim about changes made. Every substantive claim must cite a specific table, figure, section, equation number, or exact numerical value from the revised manuscript. If a change has not actually been made in the manuscript, flag it — do not invent evidence (see Step 5).

## Workflow

### Step 1: Parse Reviewer Comments

Extract every numbered comment from all reviewer files (supporting PDF, docx, plain text, or embedded email formats). Build a comment index:

```
Reviewer X:
  Comment 1: [full text]
  Comment 2: [full text]
  ...
```

Preserve the original numbering. If comments are unnumbered, number them sequentially.

**Non-English comments** (e.g., Chinese 中文审稿意见): When reviewer comments are not in English, retain the original text alongside an English translation in the response. For each response, quote the reviewer's original language first, followed by the English reply. This preserves the reviewer's exact wording and avoids translation disputes. Use the format:
```
Comment N (original): [原文]
Response: [English reply]
```

### Step 2: Classify Each Comment by Type

Read each comment and determine its primary type based on its actual meaning and intent — do not rely on keyword matching alone. A reviewer may ask for an ablation study without using the word "ablation." Use the table below as a framework, but apply your own understanding of what the reviewer is really asking:

| Type | What the Reviewer Is Really Asking |
|------|-----------------------------------|
| **novelty/contribution** | "Why is this work new? How does it differ from existing methods X, Y, Z?" |
| **missing-experiment** | "I need more evidence to be convinced. Run additional experiments or ablations." |
| **method/theory** | "Why did you design it this way? What is the theoretical basis or motivation?" |
| **complexity/efficiency** | "Is this practical? What are the computational costs and deployment feasibility?" |
| **writing/figure** | "The presentation needs improvement — clarity, grammar, figure quality, or readability." |
| **channel/condition** | "Does this work under different conditions (noise, fading, domain shifts)?" |
| **metric/evaluation** | "Are you measuring the right things? Add metrics beyond the obvious ones." |
| **literature/references** | "You missed relevant prior work. Cite and discuss these papers." |

A single comment may span multiple types (e.g., "add ablation AND discuss complexity"). Mark these as compound comments and address each sub-concern separately.

### Step 3: Identify Cross-Reviewer Overlaps

Scan all classified comments for topics raised by multiple reviewers. Mark these as **shared concerns**. They will need:
- Explicit cross-reference: "We note that Reviewer X also raised a similar concern..."
- Consistent evidence across responses — never give two reviewers different numbers for the same fact
- Where appropriate, a pointer to avoid duplication: "For the detailed results, please refer to the response to Comment N of Reviewer X."

### Step 4: Match Each Comment to Its Response Template

For the full template library and response depth selection guide, read `references/templates.md`. Select the template that matches the comment type:
- **A**: Novelty / Contribution Challenge
- **B**: Missing Experiment / Evaluation Request
- **C**: Method / Theory Question
- **D**: Complexity / Efficiency Request
- **E**: Writing / Figure Quality (keep brief)
- **F**: Cross-Reviewer Reference (incl. partial overlaps)

For compound comments, nest multiple templates in sequence.

### Step 5: Draft Each Response

Work reviewer-by-reviewer, comment-by-comment. For every response:
- Open with gratitude — consult `references/language-patterns.md` for the appropriate opening
- Follow the structural pattern from the matched template
- At every evidence slot, consult the revised manuscript to retrieve exact numbers, table references, section numbers

**When evidence is missing:** If after searching the revised manuscript you cannot find the table, figure, or experimental result that a response needs to cite, do NOT invent or guess. Instead, insert a clearly visible marker:

```
[NEEDS EVIDENCE: e.g., "Table comparing latency and FLOPs across baselines on RTX 3090"]
```

This tells the user exactly what is missing so they can provide the data or make the change before finalizing. Continue drafting the rest of the response with placeholder slots — the structure and language can still be reviewed while the evidence is pending.

### Step 6: Cross-Check Consistency

After drafting all responses, verify:

- Shared concerns reference each other and present consistent evidence
- No two responses contradict each other
- Every table/figure/section reference actually exists in the revised manuscript
- All `[NEEDS EVIDENCE]` markers are still in place (none were accidentally left as invented numbers)
- Comment numbering matches the original reviewer comments
- The tone is uniformly grateful — scan the first sentence of every response

### Step 7: Polish and Format

- Ensure a clear title: "Responses to Reviewer X:"
- Verify sequential comment numbering
- Check formatting consistency (fonts, spacing, emphasis)
- For LaTeX manuscripts, verify equation references compile; for Word, verify cross-references update
- For non-English responses: verify that original-language quotes are correctly preserved

---

## Quality Checklist

Before finalizing any response document, verify every item.

### Content Integrity
- [ ] Every response begins with gratitude ("We sincerely thank" / "Thanks a lot" / "We appreciate")
- [ ] Every substantive claim has corresponding evidence (table, figure, section, or exact number)
- [ ] No `[NEEDS EVIDENCE]` markers remain unresolved — each is either filled in or explicitly acknowledged as pending
- [ ] No response is defensive, argumentative, or dismissive
- [ ] No vague claims like "we improved performance" without a specific number
- [ ] Every evidence reference (table, figure, section) actually exists in the revised manuscript
- [ ] Shared concerns across reviewers are cross-referenced and present consistent evidence

### Language and Tone
- [ ] All responses use "we" consistently (not "I", not "the authors")
- [ ] No sentence begins with "No," "But," or any dismissal of the reviewer's concern
- [ ] The word "admit" or "failure" is never used — use "acknowledge" and "limitation" instead
- [ ] Present perfect tense used for changes: "we have added" (not "we added")
- [ ] Deferential phrasing throughout: "according to your suggestion", "in response to your comment"

### Structure
- [ ] Comment numbering is sequential and matches the original reviewer document
- [ ] Deep responses use internal structure (numbered points, paragraph breaks) for readability
- [ ] Clear title: "Responses to Reviewer X:"
- [ ] Each comment clearly separated: "Comment N: [text]" → "Response: [text]"

### Cross-Consistency
- [ ] No two responses contradict each other
- [ ] Shared concerns are explicitly cross-referenced
- [ ] The same table/figure is never referenced differently across responses (e.g., "Table 2" vs "Table II")

---

## Common Failure Modes

1. **Starting without thanking.** "We added..." → Always open with gratitude.
2. **Promise without evidence.** "We have improved the results." → Must specify the number, table, and section.
3. **Defensive tone.** "The reviewer misunderstands our method." → Instead: "We realize the description was unclear. We have revised Section X to clarify..."
4. **Inconsistent cross-references.** When Reviewer 1 and Reviewer 2 ask about the same thing, giving them different evidence or numbers.
5. **Over-explaining minor fixes.** Three paragraphs about fixing a typo. Use Template E (brief).
6. **Inventing evidence.** Claiming "results improved by 15%" when no such experiment was run. If evidence does not exist, use `[NEEDS EVIDENCE: ...]` — never fabricate.
7. **Forgetting section mapping.** Not specifying where changes were made (Section, Table, Figure, Equation). Reviewer needs to find the change.
8. **Using passive voice excessively.** "Changes were made to the manuscript." → "We have revised Section X to include..."
9. **Inconsistent naming.** Referring to the same module/acronym differently across responses.
10. **Hiding weaknesses.** If a limitation genuinely cannot be fixed, acknowledge it openly and explain why the contribution still stands.

---

## Input Requirements

When invoking this skill, provide:

1. **Reviewer comments** — as text, PDF, or docx file (Chinese or English)
2. **Revised manuscript** — ideally as LaTeX source or compiled PDF (to verify section/table/figure references)
3. **Original manuscript** (optional) — useful for understanding what changed
4. **Target output format** — plain text, markdown, docx, or LaTeX

The skill will infer the comment structure from the input format. Confirm the reviewer count and comment numbering before drafting.

---

## Bundled Resources

- `references/templates.md` — Full response templates (A–F), response depth selection, compound comment handling
- `references/language-patterns.md` — Gratitude openings, change descriptions, evidence citations, interpreting results, closing statements, cross-referencing
