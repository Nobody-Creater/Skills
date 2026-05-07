# Context Consistency Checks for Semantic Image Transmission Papers

Use this reference when revising a full paper, multiple sections, a response letter, or a draft whose terminology, formulas, method claims, and experiments must remain consistent under reviewer scrutiny.

## Core Principle

Treat consistency as a traceability problem. Every important statement should connect across this chain:

```text
communication bottleneck -> semantic variable -> method component -> equation or algorithm -> training objective -> experiment or ablation -> claim
```

If a link is missing, either add evidence, narrow the claim, or remove the statement.

## Paper Ledger

Build a compact ledger before rewriting. Keep it in working notes; do not necessarily include it in the paper.

| Item | Canonical entry | Where it must match |
| --- | --- | --- |
| Method name and acronym | Full method name, acronym, variants | Title, abstract, introduction, method, captions, conclusion |
| Core problem | Channel, bandwidth, latency, task, semantic, or mismatch bottleneck | Abstract, introduction, system model, experiments |
| Semantic variable | Saliency, task label, scene graph, segmentation, latent importance, hyperprior, receiver knowledge, user profile, etc. | Abstract, method, objective, ablation, metrics |
| System assumptions | SNR range, channel model, CSI, feedback, power constraint, bandwidth ratio | System model, method, experiment setup, limitations |
| Main modules | Functional names and input-output roles | Contributions, method subsections, ablations |
| Symbols | `x`, `z`, `y`, `x_hat`, `s`, `m`, `gamma`, `k/n`, losses | System model, equations, algorithms, captions |
| Losses and objectives | Distortion, perceptual, semantic/task, rate, power, robustness terms | Method, training details, ablations |
| Innovations | Exact gap and the component that addresses it | Introduction, related work endings, method, ablations |
| Evidence | Baselines, metrics, datasets, channel sweeps, stress tests | Abstract, experiments, conclusion |

## Consistency Passes

### 1. Terminology Pass

Check that one concept has one name.

- Use one canonical acronym for the proposed method.
- Do not alternate between "semantic feature", "semantic information", "semantic prior", and "importance map" unless they are distinct variables.
- Name modules by function: `Semantic Importance Allocator`, `Receiver-Guided Encoder`, `Hyperprior-Aided Channel Decoder`.
- Keep baseline names identical in related work, experiment tables, and captions.
- Keep metric names exact: `MS-SSIM` is not interchangeable with `SSIM`; `LPIPS` is not a semantic metric unless argued.

### 2. Formula Pass

Check equations as if a reviewer is trying to reproduce the method.

- Define every symbol before or immediately after first use.
- Keep the same symbol for the same object across the paper; do not use `s` for both semantic representation and channel state.
- State tensor shape or domain when ambiguity matters: real vs complex channel symbols, image tensor, latent tensor, binary mask, probability map.
- Verify constraints match the communication model: average power, bandwidth ratio, channel uses per pixel, feedback availability.
- Ensure loss weights appear in both the objective and training details.
- Make algorithm steps use the same variables as the equations.

### 3. Claim Trace Pass

For every abstract sentence and contribution bullet, fill this trace:

```text
Claim:
Gap:
Mechanism:
Equation/module:
Evidence:
Limitation or scope:
```

Rules:

- If evidence is only one dataset, do not claim general robustness.
- If experiments cover only AWGN, do not claim wireless fading robustness.
- If no task metric is reported, do not claim task-oriented semantic superiority.
- If only PSNR/MS-SSIM improve, call the gain reconstruction quality rather than semantic fidelity.
- If the method depends on CSI, feedback, a side model, or a semantic extractor, state that dependency explicitly.

### 4. Innovation Alignment Pass

Strong papers make the gap, module, and ablation inseparable.

Use this alignment test:

| Paper part | Required alignment |
| --- | --- |
| Introduction gap | Names one missing operational variable, not a vague lack of semantics |
| Contribution | Names a concrete module/objective/protocol |
| Method | Shows how the module acts on the missing variable |
| Experiment | Includes a stress test where the missing variable matters |
| Ablation | Removes or freezes the proposed mechanism |
| Conclusion | Restates only the proven benefit |

If the paper claims semantic-aware allocation, the ablation must remove semantic allocation or replace it with uniform allocation. If it claims channel adaptation, include channel mismatch or SNR sweep. If it claims receiver guidance, compare with no receiver-side signal.

### 5. Reviewer Stress Test

Ask these questions before finalizing:

- What exactly is "semantic" in this paper, and can it be measured?
- Why is the proposed semantic variable necessary rather than decorative?
- Does the method solve a communication bottleneck or only add a vision module?
- Are baselines matched at equal bandwidth ratio, channel uses, model capacity, and training data?
- Are separated digital baselines implemented fairly, or is the comparison too weak?
- Does the method require extra side information, feedback, CSI, or task labels at inference?
- Is complexity, latency, or memory cost acceptable for the claimed scenario?
- Does each formula match the actual training and inference pipeline?
- Are the datasets, channels, SNR range, and task settings broad enough for the claim?
- Could the same improvement come from a stronger backbone, loss, or data augmentation?

Convert each vulnerable answer into one of four actions: add an experiment, add an ablation, narrow a claim, or disclose a limitation.

## Writing Moves to Emulate from Representative Papers

Use these as writing patterns, not as text to copy.

- **DeepJSCC**: Start from separation-based transmission and the cliff effect, then prove robustness with SNR and bandwidth curves rather than a single number. Source: https://arxiv.org/abs/1809.01733
- **DeepJSCC-f**: Open with the information-theoretic expectation, then identify the finite-blocklength practical gap where feedback becomes useful. Source: https://arxiv.org/abs/1911.11174
- **ADJSCC**: Frame adaptation as a deployment mismatch problem: one trained model should handle multiple SNR regimes with less storage and better robustness. Source: https://arxiv.org/abs/2012.00533
- **NTSCC**: Tie semantic claims to an explicit latent prior, entropy model, and rate-distortion or perceptual objective. Source: https://arxiv.org/abs/2112.10961
- **Task-unaware transmitter semantic systems**: Let the receiver task define semantics, then check whether transmitter assumptions and dynamic data adaptation are consistent. Source: https://arxiv.org/abs/2205.00271
- **Context/task-oriented communication survey writing**: Treat context, semantics, and task value as design objectives, not as slogans. Source: https://arxiv.org/abs/2207.09353
- **Personalized saliency semantic communication**: Connect user-specific saliency to semantic encoding and resource allocation, then evaluate whether personalization is measured directly. Source: https://arxiv.org/abs/2209.12274

## Output Pattern for a Whole-Paper Audit

When asked to review or revise a draft, report issues in this order:

1. Critical inconsistencies that could break the paper's logic.
2. Claim-evidence gaps that a reviewer could attack.
3. Formula, notation, and variable conflicts.
4. Terminology and naming drift.
5. Suggested rewrites or experiments.

For each issue, cite the affected section, quote only the minimum needed phrase, explain the risk, and give a concrete fix.
