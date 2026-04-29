---
name: semantic-image-transmission-writing
description: Use when Codex needs to plan, draft, revise, or review an IEEE-style paper, thesis section, rebuttal, outline, or literature review about semantic communication, DeepJSCC, task-oriented communication, or wireless image transmission. Helps turn classic high-citation papers into reusable writing logic for abstracts, introductions, related work, methods, experiments, and contribution framing.
---

# Semantic Image Transmission Writing

## Quick Start

Use this skill to write or revise papers on semantic communication for image transmission. Treat it as a writing architecture guide, not a technical tutorial.

If the user asks for a literature-grounded draft, first read `references/paper-writing-patterns.md` for the source map and paper-specific writing moves. If the user only asks for section polishing, use the workflow below directly.

## Core Writing Logic

Build the paper around a three-layer story:

1. **Communication bottleneck**: conventional bit-level transmission, separated coding, or fixed-rate DeepJSCC fails under practical constraints such as channel mismatch, bandwidth variation, low SNR, feedback delay, semantic redundancy, personalization, or downstream task needs.
2. **Semantic principle**: not every pixel has equal value. The transmitter, receiver, or feedback loop should preserve information according to image content, task utility, user saliency, or learned latent importance.
3. **System evidence**: the proposed model must prove robustness through channel sweeps, bandwidth sweeps, baselines, ablations, visual examples, and semantic or task metrics.

Avoid writing semantic communication as a slogan. Define exactly what "semantic" means in the paper: saliency map, task label, segmentation, scene graph, caption, latent feature, hyperprior, receiver-side knowledge, human preference, or downstream task accuracy.

## Paper Structure

### Title

Use a title that names the mechanism and the communication setting:

- `Adaptive Semantic-Aware DeepJSCC for Wireless Image Transmission`
- `Task-Oriented Semantic Image Transmission over Noisy Channels`
- `Receiver-Guided Semantic Coding for Robust Wireless Image Delivery`

Prefer mechanism words such as `adaptive`, `task-oriented`, `semantic-aware`, `attention-guided`, `feedback-assisted`, `rate-controllable`, `personalized`, or `receiver-guided`.

### Abstract

Write the abstract in five moves:

1. State the practical image transmission problem.
2. Name the limitation of conventional codecs, channel coding, or existing DeepJSCC.
3. Introduce the proposed framework and the semantic variable it uses.
4. Explain the technical mechanism in one compact sentence.
5. Report evidence across SNR, bandwidth, channel model, visual quality, or task metrics.

Good abstract pattern:

```text
Wireless image transmission under limited bandwidth and time-varying channels remains challenging because existing bit-accurate or fixed-rate schemes treat visual content with uniform importance. This paper proposes [method], a [semantic/task/adaptive] JSCC framework that [core mechanism]. The transmitter extracts [semantic signal] and allocates channel resources according to [criterion], while the receiver reconstructs images or task outputs via [decoder/prior/feedback]. Experiments on [datasets] over [channels] show that [method] improves [metrics] over [baselines], especially under [hard regime].
```

### Introduction

Use a funnel, not a chronology:

1. **Macro setting**: wireless visual services, 6G, edge intelligence, XR, remote sensing, autonomous systems, or IoT.
2. **Classical limitation**: separated source-channel coding and bit accuracy are fragile under finite blocklength, low latency, bandwidth limits, or channel mismatch.
3. **DeepJSCC bridge**: learned JSCC gives graceful degradation but often optimizes pixel fidelity uniformly.
4. **Semantic gap**: existing systems do not fully exploit task relevance, content saliency, user preference, receiver-side knowledge, or dynamic data semantics.
5. **Proposed idea**: define the semantic signal and show how it changes encoding, channel allocation, feedback, or decoding.
6. **Contributions**: list three concrete contributions, each with a method noun and a validation noun.

Contribution bullets should be testable:

- `We propose a receiver-guided semantic JSCC architecture that conditions the transmitter on task-relevant feedback instead of reconstructing all pixels uniformly.`
- `We design a semantic importance allocation module that maps latent features to bandwidth or power allocation under channel constraints.`
- `We validate the method on AWGN and Rayleigh channels using PSNR, MS-SSIM, LPIPS, task accuracy, ablations, and channel mismatch tests.`

### Related Work

Organize related work by problem axis:

- **Classical and learned JSCC**: separation theorem baseline, JPEG/BPG plus channel coding, DeepJSCC, feedback DeepJSCC.
- **Adaptive image transmission**: SNR adaptation, bandwidth ratio adaptation, attention modules, rate control, feedback.
- **Semantic/task-oriented communication**: task utility, saliency, scene graph, labels, segmentation, retrieval, receiver-leading semantic coding.
- **Neural compression and generative priors**: nonlinear transforms, entropy models, hyperpriors, perceptual or semantic restoration.

End each subsection with a limitation sentence that points to the exact gap your method addresses. Do not merely say "few works study..." unless you name the missing variable.

### System Model

Put the communication problem before the neural network. Define:

- Source image `x`, channel input `z`, channel output `y`, reconstructed image `x_hat`, and optional task output `t_hat`.
- Bandwidth ratio, channel uses per pixel, SNR range, channel model, feedback availability, latency or complexity constraints.
- Objective: pixel distortion, perceptual loss, semantic/task loss, rate or bandwidth penalty, and robustness criterion.

Then introduce modules with role-first writing:

```text
The semantic encoder extracts [semantic variable] from the source image. The channel encoder maps this representation into complex channel symbols under a power constraint. The allocation module assigns [bandwidth/power/latent dimensions] according to [semantic importance and channel state]. The decoder reconstructs [image/task] from noisy channel observations and optional side information.
```

### Method

For each module, use the same paragraph order:

1. Role in the communication chain.
2. Input and output tensors.
3. Why this module is needed for semantic image transmission.
4. Equation or algorithm.
5. Training signal and inference behavior.

Name every module according to function, not architecture fashion. `Semantic Importance Allocator` is clearer than `Hybrid Attention Block` unless attention is the paper's main claim.

### Experiments

Design experiments so they support the story, not just the model:

- **Datasets**: CIFAR-10, Kodak, DIV2K, ImageNet subsets, Cityscapes, COCO, remote sensing, or a task-specific dataset.
- **Channels**: AWGN and Rayleigh fading at minimum when claiming wireless robustness.
- **Baselines**: JPEG/BPG plus LDPC or capacity-achieving proxy, DeepJSCC, DeepJSCC-f, ADJSCC, NTSCC, PADC, and the closest task-semantic method.
- **Metrics**: PSNR, SSIM/MS-SSIM, LPIPS, FID if generative restoration is used, classification accuracy, mIoU, retrieval recall, detection mAP, semantic similarity, complexity, and latency.
- **Stress tests**: SNR mismatch, bandwidth mismatch, low SNR, finite blocklength, unseen channel, unseen task, data distribution shift.
- **Ablations**: remove semantic signal, remove adaptation, fixed allocation, no feedback, pixel-only loss, task-only loss, no channel-state input.
- **Visual evidence**: show hard images where semantic allocation preserves important regions better, not only easy images with high PSNR.

Use tables for broad numeric comparisons and figures for channel curves. Always include at least one curve across SNR or bandwidth ratio.

## Writing Common Strengths to Emulate

- **Problem-first framing**: the best papers start from a communication constraint, then justify the neural design.
- **Named framework**: a concise method name makes the contribution citable and easy to discuss.
- **Graceful-degradation evidence**: DeepJSCC-style papers win rhetorically by showing performance curves across channel quality, not a single operating point.
- **Mechanism-gap alignment**: the gap in the introduction should map directly to one module and one ablation.
- **Task-aware metrics**: semantic papers are stronger when they evaluate task utility or semantic fidelity in addition to PSNR.
- **Engineering realism**: claims become credible when the paper includes channel mismatch, rate adaptation, computational cost, and comparisons against practical codecs.

## Revision Checklist

Before finalizing a section, verify:

- The abstract names the semantic variable, not only "semantic information".
- The introduction gap is narrower than "existing methods ignore semantics".
- Each contribution contains both a method and a validation target.
- The related work categories match the experimental baselines.
- The system model defines channel, bandwidth ratio, SNR, and objective before architecture details.
- Every module has a reason tied to the communication problem.
- Experiments include SNR or bandwidth sweeps, ablations, and at least one semantic/task metric when claiming semantic communication.
- Visual examples demonstrate semantic benefit under difficult channel conditions.

## Common Failure Modes

- Calling a method "semantic" while optimizing only MSE or PSNR with no semantic definition.
- Writing related work as a chronological list instead of a gap map.
- Introducing large neural modules without explaining the communication constraint they solve.
- Comparing only with weak baselines such as uncoded JPEG.
- Claiming robustness from one SNR point.
- Reporting visual quality without task or semantic fidelity when the title promises task-oriented communication.

## Source Map

Read `references/paper-writing-patterns.md` when you need:

- Paper-specific examples from DeepJSCC, DeepJSCC-f, ADJSCC, adaptive rate control, NTSCC, receiver-leading semantic systems, personalized saliency, and JSAC semantic communication surveys.
- A compact list of classic papers and URLs to re-check current citation counts or publication metadata.
- More detailed writing templates for introductions, contributions, method paragraphs, and experiments.
