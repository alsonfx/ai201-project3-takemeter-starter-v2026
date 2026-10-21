# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area                  | A question it could answer                                            |
| --------------------- | --------------------------------------------------------------------- |
| Overall accuracy      | How often does it need to be right to be worth using?                 |
| Per-label performance | Is one label allowed to be much worse than the others?                |
| Balance               | How lopsided can your label counts get before it's a problem?         |
| Consistency           | If someone else labelled the same posts, how often should you agree?  |
| Confidence            | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy on held-out test data

The model achieves an overall accuracy of at least 0.65 across all three seeds on the held-out test split.

**Why this target:**
With three balanced classes, random chance guessing is roughly 0.33. An accuracy of 0.65 requires the model to correctly classify nearly two out of every three posts from an unstructured climbing gear forum.

---

## 2. Macro F1 across all labels (Balance)

The model achieves a Macro F1 score of at least 0.60 across all three seeds on the held-out test split.

**Why this target:**
Macro F1 computes the unweighted arithmetic mean of F1 scores across all three classes, directly testing whether performance is balanced rather than driven entirely by the largest category. If the classifier collapsed and simply guessed the high-volume `chatter` class, overall accuracy might look passable while Macro F1 would crash. A target of 0.60 ensures all three categories have solid recall and precision.

---

## 3. Per-label F1 for `chatter`

The F1 score for `chatter` is at least 0.70 across all three seeds on the held-out test split.

**Why this target:**
`chatter` is likely our largest category and exhibits distinct stylistic and syntactic cues, such as short character length, casual forum slang, jokes, and purchase/link inquiries. Because of it's probable large training presence and it should comfortably achieve a higher threshold of 0.70 across all seeds.

---

## 4. Per-label F1 for `field_experience`

The F1 score for `field_experience` is at least 0.52 across all three seeds on the held-out test split.

**Why this target:**
`field_experience` is likely our smallest class, meaning an F1 computed on it may be significantly between random seeds—misclassifying just one or two posts swings the score by a large amount. A target of 0.52 accounts for this high variance while still holding the model substantially above chance of .33.

---

## 5. Per-label F1 for `technical_analysis`

The F1 score for `technical_analysis` is at least 0.60 across all three seeds on the held-out test split.

**Why this target:**
`technical_analysis` should be concrete markers like numbers, weights in grams, safety certifications (e.g. `EN 12841-C`), and competitor hardware comparisons. However, they share climbing domain terminology with `field_experience` when discussing rope drag and belay loops. A target of 0.60 requires the model to learn the core mechanical arguments without failing if a couple of borderline boundary cases are missed.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
