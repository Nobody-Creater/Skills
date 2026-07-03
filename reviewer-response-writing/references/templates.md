# Response Templates

选择模板时，根据 Step 2 的分类结果匹配。每条评论应使用最匹配的模板；复合型评论按顺序嵌套多个模板。

## Response Depth Selection

| Depth | When to Use | Structure |
|-------|-------------|-----------|
| **Deep** | Novelty challenges, missing core experiments, theoretical questions, complexity concerns | 3+ paragraphs, numbered sub-points, equations, multiple table/figure references, closing conclusion |
| **Medium** | Supplementary experiments, metric additions, literature requests, channel/condition additions | 1-2 paragraphs with quantified evidence and at least one table/figure reference |
| **Brief** | Writing quality, figure redraws, typos, minor clarifications | 1-2 sentences of acknowledgment and action statement |

**Decision rule:** If the comment could cause a rejection if left unanswered, use Deep. If it is a reviewer suggestion to improve rigor, use Medium. If it is cosmetic, use Brief.

---

## Template A: Novelty / Contribution Challenge

**When to use:** Reviewer questions whether the work is novel, says it is incremental, or asks how it differs from existing methods.

**Pattern:**
1. Gratitude sentence
2. Transition: name what was questioned, frame the response
3. Numbered innovation points (typically 3), each following the structure:
   - **Point title.** Gap in prior work → What your method does differently → Advantage/outcome
4. Closing sentence tying back to the revised manuscript

**Language slots:**

> We sincerely thank the reviewer for this [insightful/constructive] comment. We summarize the [novelty/contributions/distinctions] of our work compared to existing methods (such as [baseline names]) in the following [N] key aspects:

> **[Innovation name].** [Prior methods / Traditional approaches] [limitation or gap]. [Our method / module] [specific innovation], which [advantage / outcome]. Unlike [competing approach], our design [key differentiator].

> This combination of [A] and [B] has not been proposed in prior [field] literature.

**Worked example:**

> *以下为通信/遥感领域示例，实际使用时应替换为当前论文的具体领域和内容。*
>
> **Introduction of Mobile Mamba for Lightweight and Global Perception.** Traditional deep learning-based JSCC methods predominantly rely on CNNs or Transformers. CNNs are inherently limited by local receptive fields, while Transformers, despite their global modeling capabilities, suffer from quadratic computational complexity. This imposes a heavy burden on the limited power and computing resources of UAVs. Therefore, we design a specific Lightweight Feature Extraction Module that innovatively integrates Residual Blocks with Mobile Mamba Blocks. Unlike Transformers, the Mobile Mamba block captures global context and long-range dependencies with linear complexity. This design achieves a superior balance between performance and efficiency.

**Critical rule:** Each novelty point must distinguish from specifically named prior methods, not generic "existing works."

---

## Template B: Missing Experiment / Evaluation Request

**When to use:** Reviewer asks for additional experiments, ablation studies, or evaluations not present in the original manuscript.

**Pattern:**
1. Gratitude sentence
2. (Optional) Cross-reference if shared concern
3. What was added: "According to your suggestion, we have incorporated..."
4. Experimental setup: dataset, parameters, hardware, conditions
5. Quantitative results table with exact numbers
6. Interpretation of results: what they prove
7. Closing: deployment suitability or method validation statement

**Language slots:**

> We sincerely thank the reviewer for this [crucial/insightful] comment.

> [Optional: We note that Reviewer X also raised a similar concern regarding [topic].]

> According to your suggestion, we have incorporated [a comprehensive evaluation of / additional experiments on] [what was added] into the revised manuscript. Specifically, [experimental setup details — dataset, SNR, CBR, hardware].

> The results are summarized in Table X (Section Y):

> As shown in Table X, [interpretation with exact numbers]. Specifically, on the [dataset], our method achieves [metric] values of [numbers], representing a [consistent/significant/substantial] improvement over [baseline] which achieves [numbers].

> This performance gap highlights the effectiveness of our [module] in [function], demonstrating [broader implication].

> Based on the above analysis, our proposed method is [suitable/validated/robust] for [application context].

**Worked example:**

> *以下为通信/遥感领域示例，实际使用时应替换为当前论文的具体领域和内容。*
>
> Thank you for this crucial comment. According to your suggestion, we have incorporated a comprehensive evaluation of Model Parameters, Inference Latency and FLOPs into the revised manuscript. Specifically, all measurements were conducted on a single NVIDIA RTX 3090 GPU, with the Channel Bandwidth Ratio (CBR) fixed at 0.0416 to ensure a consistent comparison baseline. The results are summarized in Table X (Section IV.F):
>
> Our method reduces the computational complexity to 3.05 G FLOPs (approximately 30% of JSCCformer) and achieves an inference latency of 11.35 ms. Although our method introduces a moderate increase in parameters over Deep JSCC and VAE, the resulting performance improvements are substantial — for instance, on the AID dataset under the AWGN channel, our method achieves a PSNR of 30.95 dB, surpassing Deep JSCC (22.94 dB) and VAE (23.07 dB) by approximately 8 dB.

---

## Template C: Method / Theory Question

**When to use:** Reviewer asks for theoretical justification, design rationale, hyperparameter motivation, or clarification of the methodology.

**Pattern:**
1. Gratitude sentence
2. Restate what was asked
3. Explain theoretical motivation or design rationale (1-2 paragraphs)
4. Reference specific equation/section
5. For hyperparameters: provide quantitative justification
6. Connect back to the paper's contribution

**Language slots:**

> We sincerely thank the reviewer for this [constructive/detailed] [comment/feedback].

> The [loss function / module / design] is used to [mathematical purpose]. Its purpose is to ensure [metric / property / behavior]. In the process of [task], [metrics] are used to measure [aspect]. Therefore, [design element] is needed to [function].

> In this study, [different aspects / metrics] are equally important for measuring [performance / task]. Therefore, the hyperparameter is set to [value]. [Additional justification: empirical, literature-based, or theoretical].

> The design of [module] addresses the limitations of [prior approach]. [Prior approach] [limitation]. Our [module] introduces [mechanism], where [how it works]. Theoretically, this allows [benefit], ensuring [outcome] without [cost].

**Worked example:**

> *以下为通信/遥感领域示例，实际使用时应替换为当前论文的具体领域和内容。*
>
> The reconstruction loss is used to calculate the mean squared error between the reconstructed image and the original image. Its purpose is to ensure consistent pixel values (PSNR metric). In the process of remote sensing images semantic transmission, the LPIPS, MS-SSIM, ACC metrics are used to measure semantic similarity. Therefore, the perceptual level loss is needed to constrain the distance between latent features. In this study, different metrics are equally important for measuring the remote sensing images transmission. Therefore, the hyperparameter is set to 1.

---

## Template D: Complexity / Efficiency Request

**When to use:** Reviewer asks about computational cost, inference time, model size, energy consumption, or deployment feasibility.

**Pattern:**
1. Gratitude + optional cross-reference
2. What was measured: "We have incorporated a comprehensive evaluation of..."
3. Measurement conditions: hardware, software, fixed parameters
4. Results with exact numbers across comparison baselines
5. Trade-off interpretation: if your method uses more parameters but less compute, explain why that is acceptable
6. Deployment feasibility conclusion

**Language slots:**

> We sincerely thank the reviewer for this [insightful/valuable] [comment/recommendation].

> We have incorporated a comprehensive evaluation of Model Parameters, Inference Latency, and FLOPs into the revised manuscript. Specifically, all measurements were conducted on [hardware], with [key parameter] fixed at [value] to ensure a consistent comparison baseline.

> Our method demonstrates a significant advantage in lightweight deployment compared to [heaviest baseline]. While [baseline] achieves competitive [performance metric], its heavy reliance on [mechanism] results in prohibitive computational costs, requiring [X] G FLOPs and [Y] ms inference latency. In contrast, our proposed method reduces the computational complexity to [X'] G FLOPs (approximately [Z]% of [baseline]) and achieves an inference latency of [Y'] ms.

> Although our method introduces a moderate increase in [parameters/computation] over [lighter baselines], the resulting performance improvements are substantial — for example, [specific improvement] as shown in Table [N].

> Based on the above analysis, our proposed method is [suitable/well-suited] for deployment in [resource-constrained / real-time] scenarios.

---

## Template E: Writing / Figure Quality

**When to use:** Reviewer comments on writing quality, grammar, typos, figure readability, or presentation clarity.

**Pattern (keep it brief — do not over-explain):**
1. Apology or appreciation
2. Concise statement of what was fixed
3. Stop

**Language slots:**

> We sincerely apologize for the [poor quality / errors] in the original manuscript and thank the reviewer for pointing this out. To address this, we have [completely redrawn Figure X / carefully reviewed the entire manuscript to improve clarity, grammar, and conciseness / carefully polished the manuscript to enhance both visual quality and overall layout].

> We sincerely appreciate this constructive comment. We have carefully [reviewed / revised / polished] the [entire manuscript / specific section] to improve [clarity / grammar / conciseness / readability].

**Anti-pattern:** Do not write three paragraphs about fixing a typo. One or two sentences are sufficient.

---

## Template F: Cross-Reviewer Reference

**When to use:** Multiple reviewers raise the same or similar concern.

**Pattern F1 — second reviewer, full response shared:**

> We sincerely thank you for this insightful comment. We note that Reviewer X also raised a similar concern regarding [topic].
>
> [Full response body — identical or near-identical to the other reviewer's response.]
>
> For the detailed experimental results, please refer to the response to Comment N of Reviewer X.

**Pattern F2 — brief pointer (when the concern truly overlaps):**

> We sincerely thank the reviewer for this valuable recommendation. We have [one-sentence summary of action taken]. For the detailed experimental results and comparative analysis, please refer to the response to Comment N.

**Critical:** Even when using a pointer, provide at least a one-sentence summary so each reviewer can understand the response without jumping to another section.

**Partial overlap handling:** When two reviewers raise related but not identical concerns, respond to each independently using the appropriate template, then add a cross-reference noting the connection:

> We note that Reviewer X also raised a related point regarding [shared aspect]. While addressing different specifics, both responses reflect the same underlying design principle described in Section [N].

---

## Compound Comments (Multiple Types)

When one comment spans multiple types (e.g., "add ablation AND improve efficiency"), structure as:

1. Overall gratitude
2. Address each sub-concern in sequence using the relevant template
3. Unified closing (if applicable)
