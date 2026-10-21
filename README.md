# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

This project classifies forum discussions from Mountain Project, a public rock climbing community, specifically focusing on threads analyzing new climbing hardware and assisted braking belay devices. It sorts community posts into three categories: `technical_analysis` (objective mechanical breakdowns, specs, weight comparisons, and safety certifications), `field_experience` (first-person reports of hands-on physical testing and gym/crag usage), and `chatter` (logistical questions, banter, purchase availability, and casual one-line reactions). By distinguishing evidence-based gear analysis and real-world field trials from conversational noise, the classifier helps climbers quickly filter threads for substantive technical insights.

---

## Label Taxonomy

### `technical_analysis`

**Definition:** Argues mechanics, specs, weights, certifications, or comparative trade-offs.

**Example 1:**

> "Both the Pinch and RIG are EN 12841-C (work positioning and descending a human) and 15151-1 (for belaying and descending only, requires a hand on the brake), unlike most assisted belay devices which are just 15151-1. In the rope access world, the RIG's lack of anti-panic has made it a bit harder to market, because it's way the hell easier to use than an ID but for less experienced techs it's less safe."

**Example 2:**

> "Petzl spirit 45g Plenty of options sub 50g why would someone not use a compact lightweight carabiner for this? there isn’t “the” carabiner the grigri requires. They all work. And you probably already have one… It doesn’t really matter anyway but what you said is just not true. The pinch is significantly (>10%) heavier in every scenario."

### `field_experience`

**Definition:** First-person reports of using/handling the gear in gyms or crags.

**Example 1:**

> "I got to play hands on with one today. It’s cool! The direct attachment to the belay loop is interesting, I see some advantages with this since removes any carabiner failure modes (although it may show to have its own). You can still use a crab if you want though. What’s really cool is that you can orient it in several different ways to create the best option to belay based on your anchor of preferred belay style. ETA: pat, yes, the direct harness attachment is locked. I didn’t see an obvious way for it to come undone accidentally, and it’s slightly awkward to get it on and off the belay loop. The friction teeth seem like a good edition. It does come with an anti panic handle like the dreaded GRIGRI+, but it comes with a tool to deactivate it. It feeds great without needing to touch the device at all."

**Example 2:**

> "Finally got some gym time in with the pinch, I'm stoked. I consider myself a strong grigri proponent but this feeds noticeably smoother. I mainly used it in the direct attach configuration (no carabiner) and appreciated the extra throw distance (though not having a carabiner for the device to flop around on was the best part) Lowering felt slightly more scrunched due to this, but most likely just an ergonomics thing I'll get used to and never think about again after a few sessions."

### `chatter`

**Definition:** Quick questions, purchase availability, one-line opinions, jokes, and thread-drift.

**Example 1:**

> "Anyone seen the pinch or ohm for sale yet?"

**Example 2:**

> "My brother in Christ, let me introduce you to the wonderful world of manscaping. ;-)"

### The hardest boundary

**Which two labels:** `field_experience` vs. `technical_analysis`

**The decision rule I used every time:**
If the writer explicitly reports hands-on, physical use or trial of the device in person (e.g., testing in a gym, racking on their harness, or climbing at a crag), it is `field_experience`—even if they discuss specs, measurements, or mechanical tradeoffs. Reserve `technical_analysis` strictly for armchair, theoretical, or spec-sheet breakdowns where the writer did not personally operate the hardware.

---

## The Dataset

**Where the posts came from:** Mountain Project Gear Discussion Forum (specifically the multi-page public thread evaluating the Edelrid Pinch, Petzl Grigri/Rig, and assisted braking belay devices).

**How I labelled them:** I labelled the first 20 posts cold without assistance to establish ground-truth intuition and operationalize boundary rules. The remaining 185 posts were pre-labelled with AI assistance and then reviewed by me individually for the most part.

**Counts per label:**

| Label                  | Count | Share |
| ---------------------- | ----- | ----- |
| `chatter`            | 109   | 53.2% |
| `technical_analysis` | 58    | 28.3% |
| `field_experience`   | 38    | 18.5% |
| **Total**        | 205   | 100%  |

**Three hard cases**

**1.**

> *The post:* "You’re right but you’re not. I am pretty sure it is no real competition for the grigri, being heavier (175 vs 240g), looking weird, probably being more expensive (apparently 100€ in the one European shop that already has it listed vs 65 for a grigri 3 in the same shop)... This turned into a rant. I’m sorry. Maybe it handles like a dream. Then it’s probably great (but still ugly)."
>
> *Could have been:* `chatter` vs. `technical_analysis`
>
> *I chose, because:* `technical_analysis`. Although the writer acknowledges "This turned into a rant" and uses emotional slang ("ugly", "joke"), the core argument is carried by load-bearing factual specs: comparing manufacturer weights (175 vs 240g) and retail pricing (100€ vs 65€).

**2.**

> *The post:* "Have been using one recently. Feels well-made as you’d expect from Edelrid Paying out slack is smoother than any of the GriGris. This alone is almost enough to make me consider getting one. The no carabiner attachment feels weird to start with but you rapidly get used to it, including racking it on your harness... The no carabiner attachment doesn’t work with a beefy (>3/4”) belay loop as you might find on some metolius harnesses. The edges of the attachment plates feel like they might cause wear to fabric belay loops..."
>
> *Could have been:* `technical_analysis` vs. `field_experience`
>
> *I chose, because:* `field_experience`. The post contains detailed hardware dimensions and wear analysis (`>3/4"` belay loop clearances), but under our hardest boundary rule, explicit first-person handling and crag trial ("Have been using one recently", "racking it on your harness") makes it `field_experience`.

**3.**

> *The post:* "So I'm more positive about clipping directly to the belay loop. Even with a Rhino locker on my GriGri, I occasionally get it cross loaded. After a few times, I figured out how to attach it smoothly. When feeding for a clip, I've used a technique with the GriGri where I hover my thumb over the brake lever, without hooking my index finger under the lip. This works better with the Pinch, as it's more stable..."
>
> *Could have been:* `technical_analysis` vs. `field_experience`
>
> *I chose, because:* `field_experience`. While it explains anti-cross-loading mechanics, the judgment is grounded in tactile first-person belaying habits and thumb positioning tested directly by the author.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:**

**Anything I changed from the defaults, and why:**

**Split sizes:**

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to analyze 30–40 posts from the Mountain Project thread to identify concrete, observable textual distinctions (moving beyond subjective "good vs bad" impressions) and draft candidate taxonomies with a decision rule for the hardest boundary.
- *What came back:* The AI suggested distinctions such as verifiable specs/weights, first-person physical trial, mechanical causal explanations, and comparative teardowns. It proposed a three-label structure (`technical_analysis`, `field_experience`, `chatter`) with a decision rule prioritizing hands-on field trials over armchair spec breakdowns.
- *What I changed:* I adopted the three proposed labels but edited their definitions directly in `label_definitions.txt` to keep them concise. I also customized `criteria.md` by writing my own rationale for class balance and seed variance rather than keeping generic starter templates.

**Moment 2**

- *What I asked for:* After labeling the first 20 posts manually ("cold") to anchor ground truth, I instructed AI to use those 20 examples to pre-label the remaining 185 rows of `labels.csv`.
- *What came back:* The AI produced label assignments for all 185 unlabelled rows, marked them as `pre-labelled, checked` in the `note` column, and ran an automated verification script mirroring the starter repo's `check_dataset` function to confirm zero warnings/errors (ensuring no label exceeded 70% share and all classes had $\ge 20$ rows).
- *What I changed:* I audited the resulting label distribution and checked borderline edge cases—specifically verifying that emotional rants containing load-bearing weight numbers (e.g. Row 23) stayed in `technical_analysis` and hands-on crag testing mentioning hardware measurements (e.g. Row 63) remained in `field_experience` as mandated by our decision rule.

**Pre-labelling disclosure:**
I hand-labelled the first 20 posts (rows 0 to 19) cold without any AI assistance to establish ground truth intuitions and stress-test the taxonomy. The remaining 185 posts (rows 20 to 204) were pre-labelled with AI assistance. Every pre-labelled row is designated as `pre-labelled, checked` in the `note` column, and the assignments were audited to ensure consistency.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure             | Baseline | Trained | Difference |
| ------------------- | -------- | ------- | ---------- |
| Overall accuracy    |          |         |            |
| Macro F1            |          |         |            |
| F1 — `label_one` |          |         |            |
| F1 — `label_two` |          |         |            |

**What I predicted before I looked:**

<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
| ---------------- | - | - | - |
| ****             |  |  |  |
| ****             |  |  |  |
| ****             |  |  |  |

**My biggest off-diagonal number, and what it means:**

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
| - | --------- | ------ | ------- | ------------- |
| 1 |           |        |         |               |
| 2 |           |        |         |               |
| 3 |           |        |         |               |
| 4 |           |        |         |               |
| 5 |           |        |         |               |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**

> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
