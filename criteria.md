# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.
Of the 10 human-written samples in scenarios.py, at most 1 is labeled high-confidence AI.

**Why this target:**
A high confidence false positive is very costly, and must be rare.

---

## 2.
The mean scores of 5 AI written pieces, and 5 human written pieces should vary by at
least .4

**Why this target:**
Signal one (detector.py) and signal two (stylometry.py) are combined in 
scoring.py::combine_signals as a weighted average. If the two group means are only 
~.2 apart, the unsure band (0.4–0.6) swallows most of both groups and the 
false-positive rate climbs. A .4 spread keeps the unsure band from being the default 
outcome.

---

## 3.
Given 3 human texts, 3 AI written texts, and 3 human-edited AI texts, all 3 of the 
labels are returned at least once.

**Why this target:**
The human-edited AI texts should sit at the boundary of being detected as AI written 
or human written, so should rightly be classified as uncertain.

---

## 4.
For 5 of 5 valid appeals, the appeal always changes the status.

**Why this target:**
The appeal is the writer's only remedy for the false-positive mistake criterion 1 caps. 
If the endpoint ever silently drops an appeal, an accused human has no recourse, and 
the audit log becomes a record of the system lying. 5/5 means the safety net actually works.

---

## 5.
For 5 of 5 attempts, empty text returns a 400, not a 500.

**Why this target:**
An empty string is the cheapest way to make stylometry.py divide by zero (zero sentences, 
zero tokens) — a 500 means the input guard sits inside a signal rather than in front of 
the pipeline, and the same unguarded path will misbehave on short or malformed text in 
production. A 400 proves the guard is at the boundary.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
