# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->
1. The writer submits a post to app.py::submit
2. The payload is validated, and the text and creator_id are extracted
3. The text is sent to detector.model_signal and a score for the text is retrieved (first signal)
4. The text is sent to stylometry.style_signal, and a score for the text is retrieved (second signal)
5. The scores are combined into a single score
6. The signal scores and the combined scores are logged, along with content_id for possible appeal
7. The score is converted into a label, which is then returned to the user

---

## Endpoint Shapes

### POST /submit
     Expects JSON:
          {"text": "...", "creator_id": "..."}

     Should return JSON with a shape of:
          {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
          "model_score": 0.0, "style_score": 0.0}

### POST /appeal

     Expects JSON:
          {"content_id": "...", "reasoning": "..."}

     Should return JSON with:
          {"message": "..."} or 404 if content_id doesn't exist

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
This is the signal that "reads the text for meaning". It runs a language model
on your own machine and asks one question: how predictable is this text?

The idea is the one every AI-detection product is built on. A language model
writes by repeatedly picking a likely next word, so text a model produced tends
to be text a model finds easy to predict. Human writing wanders more — odd word
choices, abrupt turns, the specific rather than the typical.

The measure is called perplexity. Low perplexity means "I could have
guessed this"; high perplexity means "that surprised me". This module turns
that into a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:**
Human writing with dense, ornate prose, or using rare words, is less likely to to be flagged 
as AI because those are the words that the model is least likely to predict.

**What it can't see:**
Predictability is not the same thing as authorship. What this signal actually flags as AI 
is common words in short, ordinary sentences — and plenty of real people write that way.

Someone writing in a second language, sticking to vocabulary they're sure of.
A younger writer. Anyone writing plainly on purpose. Measured against gpt2,
writing like that scores about as machine-like as machine writing does.

### Signal two — the style signal

**What it measures:**
style_signal measures how human the style of the writing is, as defined by three metrics. The
metrics used are sentence length spread, type token ratio, and punctuation density/variety. The
premise is that AI written prose is more likely to have even, mid-length sentences, with a narrower
band of vocabulary, and presumably follow punctuation rules precisely.

**Why that might differ between human and AI writing:**
Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is lumpier — a three-word 
sentence next to a forty-word one.

**What it can't see:**
Anything that changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

The two signals answer the same question, but they do not answer it on the same scale, so
the rule calibrates before it averages. Each signal is first converted into **evidence
units** against two reference points of its own — the score typical human prose gets on
that signal, and the score typical AI prose gets:

```
evidence = (signal − human_reference) / (AI_reference − human_reference)
```

`0` means "reads like our human samples", `1` means "reads like our AI samples", and
`0.5` is a genuine coin flip. That last one is the whole reason for the step. On the raw
model signal, `0.5` is perplexity 45 — comfortably ordinary human writing; my Formal
sample scored 0.4994 there. On the raw style signal, `0.5` is already a suspicious
reading, yet blatant AI boilerplate only just reaches it at 0.5194. A shared bar at 0.5
would have the model one thousandth of a point away from accusing plain human prose
while style could barely convict the obvious machine text in front of it.

The two evidences are then averaged with equal weight, **damped** toward the coin-flip
point in proportion to how far apart they sit, and squashed onto 0–1 once, at the end:

```
pooled    = 0.5·E_model + 0.5·E_style
agreement = 1 − min(|E_model − E_style| / 1.0, 1)
effective = 0.5 + (pooled − 0.5)·agreement
score     = 1 / (1 + e^(−4·(effective − 0.5)))
guess     = AI if score > 0.55 else human        # ties go human
```

**What happens when they disagree:** the verdict collapses toward the middle instead of
averaging into a confident-looking number. Two signals a full unit apart land on exactly
**0.500**, and 0.500 is not accused. Two methods telling opposite stories *is* the
finding, so it is reported as uncertainty rather than smoothed away — and the certainty
that comes with it is low (0.19 for a 0.90/0.10 pair). Damping the evidence rather than
clamping probabilities is also why an unusual text can still land at 0.05 or 0.89 instead
of saturating at both ends and losing the ordering that matters.

**Which way I chose to be wrong:** toward the human. The bar is `0.55`, not `0.50`, so an
accusation has to clear a gap and ties go human: a wrong accusation costs a writer far
more than a missed detection costs the site. The visible price is that light editing gets
through — a subtler rewrite landing near 0.50 is not accused at all.

**The numbers:**

| Constant | Value | What it does |
|---|---|---|
| `CAL_HUMAN_MODEL` / `CAL_AI_MODEL` | 0.42 / 0.77 | model-signal reference points — ⚠️ centres of **two** texts each: a placeholder, not a corpus |
| `CAL_HUMAN_STYLE` / `CAL_AI_STYLE` | 0.14 / 0.51 | style-signal reference points — same caveat |
| `WEIGHT_MODEL_SIGNAL` / `WEIGHT_STYLE_SIGNAL` | 0.5 / 0.5 | equal trust, applied to comparable units rather than to two different scales |
| `COMBINE_CROSSOVER` | 0.5 | the coin flip — calibration is what makes it meaningful |
| `COMBINE_SLOPE` | 4.0 | how hard pooled evidence is squashed onto 0–1 |
| `DISPERSION_FULL` | 1.0 | disagreement, in evidence units, that cancels the verdict completely |
| `GUESS_BIAS` | +0.05 | the accusation bar sits at **0.55**; ties go human |
| `SIGMA_BASE` | 0.30 | within-class noise — sets how confident this system is ever allowed to sound. ⚠️ Judgement call, and the single most influential number here |
| `CONF_MAX` | 0.95 | never claim certainty 1.0 |
| `VALID_MIN_WORDS` / `VALID_FULL_WORDS` | 20 / 60 | certainty ramps with sample size; 20 words earns nothing |
| `STYLE_MIN_TOKENS` | 8 | below this the style signal is **absent**, not weak |

Scope: the tokenizer, both signals and both anchor sets are English-only, so non-English
submissions are out of scope for this unit — see *Known limitation* below the measurements.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

`score_breakdown()` in the same file is the same rule with every intermediate exposed —
evidence per signal, disagreement, agreement, the verdict — and that dict is what
`/submit` writes to the audit log, so a decision can be reconstructed months later
instead of re-guessed. `combine_signals()` is a one-line call into it, which keeps there
being exactly one implementation of the rule.

### Confidence

The score says which way; confidence says how sure we are that the guess is right — 0.0 
is no idea, 1.0 is sure — and it carries no direction of its own, so 0.9 on a human verdict 
is the same size of claim as 0.9 on an AI verdict.

```
z         = |score − 0.55| / (SIGMA_BASE / √n_signals)      # n_signals = 1 or 2
certainty = erf(z / √2) × length_validity,  capped at 0.95
length_validity = 0 at ≤20 words, ramping to 1 at ≥60 words
```

Three ideas are doing the work:

- **Distance in units of our own noise, not raw points.** 0.56 next to a bar of 0.55 is a
  coin flip that happened to land and gets near-zero certainty; 0.05 is a verdict.
- **The standard error.** Dividing by `√n_signals` means a ruling resting on one signal is
  automatically less certain than one corroborated by two — no special case in the code.
- **Sample size.** A two-sentence submission cannot buy certainty at any score, which is
  what `length_validity` is for; it can take the number to zero and does.

Corroboration is deliberately **not** multiplied in a second time. Disagreement has
already collapsed the score toward 0.500 in the combining step, which shrinks the distance
from the bar and therefore the certainty; charging the same disagreement twice would make
the number impossible to reason about. The cap at 0.95 exists because an automated
accusation claiming certainty 1.0 is a statement no evidence this thin supports — and it
keeps any log-odds taken downstream finite.

**A case where my two signals split, and what my rule does with it:**

My Human2 test uses purposefully simple language, one that a younger writer, or someone for
whom english is a second language might use.

"Last month, my family and I stayed at The Seaside Hotel for three nights. The location 
was perfect, because it was only a two-minute walk from the beach and very close to the 
shops and restaurants in the town."

The model score is 0.8681 (very suggestive of AI). The style score is 0.2814 (more suggestive
of human).

The combining rule results in a combined score of 0.5337, which is above the coin flip, but
below the bar (0.55), so the guess is human. The leniency is the only reason the guess is human.

Confidence comes back at 0.029, so the guess is with very low certainty, which is probably the best
case scenario for conflicting signals like this.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | "This appears to have been written by a human." |
| unsure | 0.35 - 0.65 | "There is not enough evidence to be certain if this is human or AI generated." |
| high-confidence AI | 0.65 - 1.00 | "This appears to have been written by AI." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It is not making a decision either way. It basically is a way for the app to say "I don't know."


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**Milestone 3 sample run**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "This text is a sterling example short prose that is unequivocally written by a human. It must be clear that no machine, even in an insane bout of high temperature rambling, could have come up with it. It should have sentences of varying length, unexpected word choices, and some literary surprise. Short sentences. Sentences of medium length. And sentences that are so long that a reader might become fatigued reading it, perhaps wondering in desperation whether hopefully, eventually, the sentence might end.", "creator_id": "a_human"}'
```

```json
{
  "confidence": 0.0,
  "content_id": "5d9d046c-9155-4574-a481-cf17f587abc9",
  "guess": "human",
  "label": "placeholder",
  "model_score": 0.3488,
  "style_score": 0.0
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs.  Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "ai"}'
```

```json
{
  "confidence": 0.0,
  "content_id": "48dceef0-ccee-4f0b-a28a-7bbe76565a34",
  "guess": "AI",
  "label": "placeholder",
  "model_score": 0.8326,
  "style_score": 0.0
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework carefully consider several key factors. Firstly, it is critical that the system be able to handle a wide variety of different inputs.  Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "human+ai"}'
```

```json
{
  "confidence": 0.0,
  "content_id": "2d871414-9281-45db-a2b8-52eaf09c2e9f",
  "guess": "AI",
  "label": "placeholder",
  "model_score": 0.7016,
  "style_score": 0.0
}
```

```bash
$ curl -X GET http://127.0.0.1:5000/log
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.0,
      "content_id": "31364310-87d5-4ff4-878d-3b353d2463ec",
      "creator_id": "a_human",
      "guess": "human",
      "label": "placeholder",
      "model_score": 0.3488,
      "status": "placeholder",
      "style_score": 0.0,
      "timestamp": "2026-10-29T20:46:45+00:00"
    },
    {
      "combined_score": 0.0,
      "content_id": "c9b6fccf-14b7-4d43-85ca-7dfed9549860",
      "creator_id": "ai",
      "guess": "AI",
      "label": "placeholder",
      "model_score": 0.8326,
      "status": "placeholder",
      "style_score": 0.0,
      "timestamp": "2026-10-29T20:46:55+00:00"
    },
    {
      "combined_score": 0.0,
      "content_id": "86c68209-3385-4aaa-bd60-203d58901eaa",
      "creator_id": "human+ai",
      "guess": "AI",
      "label": "placeholder",
      "model_score": 0.7016,
      "status": "placeholder",
      "style_score": 0.0,
      "timestamp": "2026-10-29T20:47:02+00:00"
    }
  ]
}
```

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Where Congress has spoken, Congress has spoken; only its judgments matter. And courts alone determine when that has happened: Using all their normal interpretive tools, they decide whether Congress has addressed a given issue. But when courts have decided that Congress has not done so, a choice arises. Absent a legislative directive, either the administering agency or a court must take the lead. And the matter is more fit for the agency.", "creator_id": "Formal human"}'
```

```json
{
  "combined_score": 0.2687272959587301,
  "confidence": 0.815137858037386,
  "content_id": "989e0484-8408-421d-9ca9-0789bb2ad129",
  "guess": "human",
  "label": "placeholder",
  "model_score": 0.4994,
  "status": "decided",
  "style_available": true,
  "style_score": 0.2351,
  "style_tokens": 72,
  "word_count": 72
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "989e0484-8408-421d-9ca9-0789bb2ad129", "reasoning": "Please help"}'
```

```json
{
  "message": "content_id 989e0484-8408-421d-9ca9-0789bb2ad129 has been marked under review. Thank you for your appeal."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "content_id": "c2c9a811-7b54-469d-b1c8-2bcd11e082e1",
      "creator_id": "human2",
      "event": "appeal",
      "reasoning": "I am human!",
      "status": "under_review",
      "timestamp": "2026-10-30T21:48:49+00:00"
    },
    {
      "agreement": 0.9698,
      "combined_score": 0.2687272959587301,
      "confidence": 0.815137858037386,
      "content_id": "989e0484-8408-421d-9ca9-0789bb2ad129",
      "creator_id": "Formal human",
      "disagreement": 0.0302,
      "evidence_model": 0.2269,
      "evidence_style": 0.257,
      "guess": "human",
      "label": "placeholder",
      "model_score": 0.4994,
      "status": "decided",
      "style_available": true,
      "style_score": 0.2351,
      "style_tokens": 72,
      "timestamp": "2026-10-30T21:53:18+00:00",
      "word_count": 72
    },
    {
      "content_id": "989e0484-8408-421d-9ca9-0789bb2ad129",
      "creator_id": "Formal human",
      "event": "appeal",
      "reasoning": "Please help",
      "status": "under_review",
      "timestamp": "2026-10-30T21:55:30+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
Help writing the logic for stylometry functions, as using a naive approach for sentence length variance,
token variability, and punctuation density seemed like it would be terrible for this purpose.
- *What came back:*
A rather comprehensive set of functions calibrated on self generated text segments to have reasonable parameters.
- *What I changed:*
I reviewed the code, made some manual changes, and used it.

**Moment 2**

- *What I asked for:*
Help writing the logic for combining scores and confidence, as just taking an average seemed like it would be too simplistic.
- *What came back:*
A rather sophisticated approach to combining scores, and generating a confidence level.
- *What I changed:*
I reviewed the suggested changes, and reviewed the artifacts that the AI generated, and used it.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
