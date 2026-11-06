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
agreement = 1 − min(|E_model − E_style| / DISPERSION_FULL, 1)   # 2.0 this unit; was 1.0
effective = 0.5 + (pooled − 0.5)·agreement
score     = 1 / (1 + e^(−4·(effective − 0.5)))
guess     = AI if score > 0.55 else human         # internal binary call; ties go human
label     = AI above 0.65, human below 0.35, unsure between   # AI/HUMAN_THRESHOLD
```

**Two bars, and they do different jobs.** The internal `guess` clears a 0.55 bar, but what a
writer sees is the `label`, which needs 0.65 to accuse. That is why a response can carry
`guess: "unsure"` at score 0.62 — the ternary `guess` in the API response comes from
`score_to_label`, not from `guess_from_score`. Everywhere in the test sections below,
"flagged" means the accusation actually reached the writer: `score > 0.65` / `guess: "ai"`.

**What happens when they disagree:** the verdict collapses toward the middle instead of
averaging into a confident-looking number. Two signals `DISPERSION_FULL` units apart land on
exactly **0.500**, and 0.500 is not accused. Two methods telling opposite stories *is* the
finding, so it is reported as uncertainty rather than smoothed away — and the certainty that
comes with it is low (0.06 for a 0.90/0.10 pair, which now sits at score 0.534: dampening
drags a score toward the bar, so disagreement buys *less* confidence, never more). Damping
the evidence rather than clamping probabilities is also why an unusual text can still land at
0.05 or 0.89 instead of saturating at both ends and losing the ordering that matters.

⚠️ How wide that collapse should be is this unit's open question, and **The Improvement** at
the end of this README is the answer I measured: `DISPERSION_FULL` 1.0 → 2.0. One unit of
disagreement used to erase the verdict entirely; it now erases half. The trade is spelled out
there, with both sides run against the same attack set.

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
| `DISPERSION_FULL` | **2.0** *(was 1.0 — changed this unit, see The Improvement)* | disagreement, in evidence units, that cancels the verdict completely |
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

## Stretch Feature: A GET /content/<id> endpoint that returns one item's current status.

**Where it lives**
app.py::get_content_status

**Sample Run**

Correctly sees an item under review

```bash
$ curl -X GET "http://127.0.0.1:5000/content/989e0484-8408-421d-9ca9-0789bb2ad129"
```

```json
{
  "content_id": "989e0484-8408-421d-9ca9-0789bb2ad129",
  "status": "under_review"
}
```

Correctly sees an item that's been decided

```bash
$ curl -X GET "http://127.0.0.1:5000/content/e6470306-eb7c-469f-8d1d-846f8069676e"
```

```json
{
  "content_id": "e6470306-eb7c-469f-8d1d-846f8069676e",
  "status": "decided"
}
```

Correctly flags an invalid content_id

```bash
$ curl -X GET "http://127.0.0.1:5000/content/noid"
```

```json
{
  "content_id": "noid",
  "status": "not_found"
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

**Moment 2**

- *What I asked for:*
Help writing the improvement for criterion 3 (label coverage). Just adjusting the threshold to make the labels show up seemed
too simplistic, but reviewing all of the numbers from the scenario to find the appropriate lever felt better to give to AI.
- *What came back:*
A thorough evaluation of the scenario metrics, and a suggestion of what to change.
- *What I changed:*
DISPERSION_FULL, as suggested.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
10 per minute is very generous for a real writer -- one very 6 seconds is likely faster than most humans would ever 
submit. But a bot could easily attack by doing it more frequently. Likewise, 200 / day is a reasonable limit for a given 
user in a given day, that the system should be able to handle, but hopefully would be able to prevent bot abuse.

**What a caller counts as:** 
<!-- per address, or per creator_id? They fail differently — one script can look like a thousand callers, and one household
can look like one. -->

A `creator_id`, falling back to the caller's IP address when the body carries no usable one
(`app.py::rate_limit_key`, lines 74-95).

Per-creator rather than per-address because a script that rotates source addresses still has
to keep identities that survive an appeal, and because on a shared network one household
would otherwise look like one abuser. The address fallback is what keeps an anonymous script
countable at all. The honest cost of this design: the limit reads its own key out of the
request body, so a caller can dial their own speed by inventing `creator_id`s, and two
people who share an id share one budget. It stops a lazy script, not a determined one —
real deployment would tie the key to an authenticated account.

One harness interaction worth knowing: `run_eval.py`'s appeal-path and empty-text scenarios
each post five bodies under a single shared `creator_id`, so a full three-trial eval against
a limited server can brush the 10/minute budget on those two ids. The eval is therefore run
against a server started with `AI201_RATE_LIMITS=0` (the flag is read at import, so it goes
on the `app.py` process, not the client); the attack set and the flood are run with limiting
ON, which is where the 429 evidence has to come from.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 200
  [10/15] 200
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
============================================================
```

**Status of the switch this unit:** `config.RATE_LIMITING_ENABLED` had been pinned to a
hard `False` by the unit 7 Milestone 4 commit — `GET /health` was reporting
`"rate_limiting": false`, and the `flood_same_creator` rows of the attack set were being
judged against a limiter that was not running. Restored this unit (default ON, with the
starter's `AI201_RATE_LIMITS` escape hatch kept so the eval can opt out) and re-captured
the flood on both sides of this unit's comparison:

```
$ python run_attacks.py --flood 15     # DISPERSION_FULL = 1.0  (before_v2 baseline)
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

$ python run_attacks.py --flood 15     # DISPERSION_FULL = 2.0  (after the improvement)
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

Identical, and that is the point: this unit's change moves the combining rule only, so it
cannot move the limit, and the flood evidence is valid on both sides of the comparison.
`GET /health` now reports `"rate_limiting": true`, and the rejections land in
`logs/audit.jsonl` as `reason: "rate_limited"` with the limit quoted (`evidence` below).

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

  [ 1/56] EV01   evasion           200   human    broke
  [ 2/56] EV02   evasion           200   human    broke
  [ 3/56] EV03   evasion           200   human    broke
  [ 4/56] EV04   evasion           200   ai       held
  [ 5/56] EV05   evasion           200   human    broke
  [ 6/56] EV06   evasion           200   human    broke
  [ 7/56] EV07   evasion           200   human    broke
  [ 8/56] EV08   evasion           200   human    broke
  [ 9/56] EV09   evasion           200   human    broke
  [10/56] EV10   evasion           200   human    broke
  [11/56] FP01   false_positive    200   ai       broke
  [12/56] FP02   false_positive    200   ai       broke
  [13/56] FP03   false_positive    200   ai       broke
  [14/56] FP04   false_positive    200   ai       broke
  [15/56] FP05   false_positive    200   ai       broke
  [16/56] FP06   false_positive    200   ai       broke
  [17/56] FP07   false_positive    200   ai       broke
  [18/56] FP08   false_positive    200   human    held
  [19/56] PI01   prompt_injection  200   human    held
  [20/56] PI02   prompt_injection  200   human    held
  [21/56] PI03   prompt_injection  200   human    held
  [22/56] PI04   prompt_injection  200   human    held
  [23/56] PI05   prompt_injection  200   human    held
  [24/56] PI06   prompt_injection  200   human    held
  [25/56] MF01   malformed         400   —        held
  [26/56] MF02   malformed         400   —        held
  [27/56] MF03   malformed         200   human    broke
  [28/56] MF04   malformed         200   human    broke
  [29/56] MF05   malformed         200   ai       broke
  [30/56] MF06   malformed         200   ai       broke
  [31/56] MF07   malformed         200   ai       broke
  [32/56] MF08   malformed         200   ai       broke
  [33/56] RQ01   malformed         400   —        held
  [34/56] RQ02   malformed         200   human    broke
  [35/56] RQ03   malformed         400   —        held
  [36/56] RQ04   malformed         400   —        held
  [37/56] RQ05   malformed         400   —        held
  [38/56] RQ06   malformed         200   human    broke
  [39/56] RQ07   malformed         400   —        held
  [40/56] RQ08   malformed         400   —        held
  [41/56] RQ09   malformed         400   —        held
  [42/56] RQ10   malformed         400   —        held
  [43/56] RQ11   malformed         400   —        held
  [44/56] RQ12   malformed         400   —        held
  [45/56] FL01_01 flood_same_creator 200   human    held
  [46/56] FL01_02 flood_same_creator 200   human    held
  [47/56] FL01_03 flood_same_creator 200   human    held
  [48/56] FL01_04 flood_same_creator 200   human    held
  [49/56] FL01_05 flood_same_creator 200   human    held
  [50/56] FL01_06 flood_same_creator 200   human    held
  [51/56] FL01_07 flood_same_creator 200   human    held
  [52/56] FL01_08 flood_same_creator 200   human    held
  [53/56] FL01_09 flood_same_creator 200   human    held
  [54/56] FL01_10 flood_same_creator 200   human    held
  [55/56] FL01_11 flood_same_creator 429   —        held
  [56/56] FL01_12 flood_same_creator 429   —        held

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T00:27:14+00:00", "content_id": "8401563f-b8f2-4278-be3b-03ddd908246e", "creator_id": "attacker_FP01", "guess": "ai", "model_score": 0.6175, "style_score": 0.3721, "combined_score": 0.5888036976209314, "label": "placeholder", "status": "decided", "confidence": 0.1451410813149621, "word_count": 103, "style_tokens": 103, "style_available": true, "evidence_model": 0.5643, "evidence_style": 0.6273, "disagreement": 0.063, "agreement": 0.937}
{"timestamp": "2026-11-05T00:27:14+00:00", "content_id": "d3edf278-af1f-43bc-98b5-223b53a44fcc", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.423, "combined_score": 0.7512783969917364, "label": "placeholder", "status": "decided", "confidence": 0.6572956976346511, "word_count": 68, "style_tokens": 68, "style_available": true, "evidence_model": 1.1797, "evidence_style": 0.7649, "disagreement": 0.4148, "agreement": 0.5852}
{"timestamp": "2026-11-05T00:27:14+00:00", "content_id": "96ad3b28-b4e1-4b74-84cf-ed5deae29b84", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.3522, "combined_score": 0.6118805447453076, "label": "placeholder", "status": "decided", "confidence": 0.22948986743590977, "word_count": 64, "style_tokens": 64, "style_available": true, "evidence_model": 1.3183, "evidence_style": 0.5735, "disagreement": 0.7448, "agreement": 0.2552}
{"timestamp": "2026-11-05T00:27:14+00:00", "content_id": "07c2393c-fd79-41c0-820e-18270005f962", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.3423, "combined_score": 0.4365889322948916, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 8, "style_tokens": 8, "style_available": true, "evidence_model": -0.2791, "evidence_style": 0.5468, "disagreement": 0.8259, "agreement": 0.1741}
{"timestamp": "2026-11-05T00:27:15+00:00", "content_id": "6dc95295-7eb1-4231-ac03-c33f634db522", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": null, "combined_score": 0.0011125360328603227, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 3, "style_tokens": 3, "style_available": false, "evidence_model": -1.2, "evidence_style": null, "disagreement": 0.0, "agreement": 1.0}
{"timestamp": "2026-11-05T00:27:15+00:00", "content_id": "848701ff-722f-418e-bfc3-5e0ed4417589", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": null, "combined_score": 0.9900594521301628, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 1, "style_tokens": 1, "style_available": false, "evidence_model": 1.6503, "evidence_style": null, "disagreement": 0.0, "agreement": 1.0}
{"timestamp": "2026-11-05T00:27:15+00:00", "content_id": "ab71c9b9-fc13-4868-aca6-b5595cbdf8eb", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": null, "combined_score": 0.9723168322080543, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 17, "style_tokens": 0, "style_available": false, "evidence_model": 1.3897, "evidence_style": null, "disagreement": 0.0, "agreement": 1.0}
{"timestamp": "2026-11-05T00:27:15+00:00", "content_id": "4167788b-dcb8-4c6a-99b3-e40c61866547", "creator_id": "unknown", "guess": "human", "model_score": 0.2395, "style_score": 0.65, "combined_score": 0.5, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 11, "style_tokens": 11, "style_available": true, "evidence_model": -0.5157, "evidence_style": 1.3784, "disagreement": 1.8941, "agreement": 0.0}
{"timestamp": "2026-11-05T00:27:15+00:00", "content_id": "4a3cdf6f-40e6-4f01-a1b8-bfab8fe93569", "creator_id": "unknown", "guess": "human", "model_score": 0.0492, "style_score": null, "combined_score": 0.0019505055258997512, "label": "placeholder", "status": "decided", "confidence": 0.0, "word_count": 3, "style_tokens": 3, "style_available": false, "evidence_model": -1.0594, "evidence_style": null, "disagreement": 0.0, "agreement": 1.0}
{"timestamp": "2026-11-05T00:27:15+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

```json
{"timestamp": "2026-11-05T00:27:14+00:00", "content_id": "83c891fc-3624-44a3-91c8-d3061b36ab79", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.4796, "combined_score": 0.8408730176382264, "label": "placeholder", "status": "decided", "confidence": 0.829683814940543, "word_count": 83, "style_tokens": 83, "style_available": true, "evidence_model": 1.1003, "evidence_style": 0.9178, "disagreement": 0.1824, "agreement": 0.8176}
```

If we are flagging a non-native English speaker writing carefully as AI with high confidence, that reflects a problem with the model.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. human-written samples | <=1/10 | 0/10 | 0/10 | 0/10 | MET |
| 2. ai and human samples | >=0.4 | 0.051 | 0.051 | 0.051 | MISSED |
| 3. label coverage | 3/3 | 2/3 | 2/3 | 2/3 | MISSED |
| 5. appeal path | 5/5 | 5/5  | 5/5  | 5/5  | MET |
| 5. empty text | 5/5 | 5/5 | 5/5 | 5/5 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

### human-written samples
app.py::submit

**Trial 1**


```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8017247568826692,
    "model_score": 0.3379,
    "style_score": 0.2395,
    "label": "This appears to have been written by a human.",
    "sent": "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.95,
    "model_score": 0.3232,
    "style_score": 0.0,
    "label": "This appears to have been written by a human.",
    "sent": "Your Christmas gift to me sits unopened on my desk, next to the one I "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.95,
    "model_score": 0.3325,
    "style_score": 0.075,
    "label": "This appears to have been written by a human.",
    "sent": "A close friend died in 1999. After her funeral, grief's full weight in"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4329570033775598,
    "model_score": 0.635,
    "style_score": 0.166,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Finally, a succinct summary of my life, courtesy of the Scholarships E"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.95,
    "model_score": 0.2383,
    "style_score": 0.022,
    "label": "This appears to have been written by a human.",
    "sent": "Dear Journal, It is five minutes until midnight on Friday. We are havi"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.9458482141987881,
    "model_score": 0.4038,
    "style_score": 0.1583,
    "label": "This appears to have been written by a human.",
    "sent": "My high school had 4 guidance counselors. 3 were competent at their jo"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.9004153436069616,
    "model_score": 0.463,
    "style_score": 0.0365,
    "label": "This appears to have been written by a human.",
    "sent": "In looking at mine, I become aware that it is so recent in the stretch"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.843392977829802,
    "model_score": 0.5037,
    "style_score": 0.0778,
    "label": "This appears to have been written by a human.",
    "sent": "It turned out to be true. The face of the water, in time, became a won"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.02811610805277382,
    "model_score": 0.7531,
    "style_score": 0.2495,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Dear Dr. Huntington, My name is Georgina Geo, and I am writing to inqu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3917218235523799,
    "model_score": 0.6071,
    "style_score": 0.2562,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "As you probably know, the paper we use for our schoolwork and notes to"
  }
]
```

### ai and human samples
app.py::submit

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8017247568826692,
    "model_score": 0.3379,
    "style_score": 0.2395,
    "label": "This appears to have been written by a human.",
    "sent": "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.9458482141987881,
    "model_score": 0.4038,
    "style_score": 0.1583,
    "label": "This appears to have been written by a human.",
    "sent": "My high school had 4 guidance counselors. 3 were competent at their jo"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.843392977829802,
    "model_score": 0.5037,
    "style_score": 0.0778,
    "label": "This appears to have been written by a human.",
    "sent": "It turned out to be true. The face of the water, in time, became a won"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.02811610805277382,
    "model_score": 0.7531,
    "style_score": 0.2495,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Dear Dr. Huntington, My name is Georgina Geo, and I am writing to inqu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3917218235523799,
    "model_score": 0.6071,
    "style_score": 0.2562,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "As you probably know, the paper we use for our schoolwork and notes to"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4228566651258606,
    "model_score": 0.6091,
    "style_score": 0.2406,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "When I was twelve I broke my wrist trying to prove I could jump a fenc"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8695214550887325,
    "model_score": 0.4965,
    "style_score": 0.1159,
    "label": "This appears to have been written by a human.",
    "sent": "Genuinely cannot believe my school decided the best time to renovate t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5408869651227974,
    "model_score": 0.4068,
    "style_score": 0.3369,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "In The Yellow Wallpaper, Gilman never lets the narrator name her own c"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.31800431029693943,
    "model_score": 0.6658,
    "style_score": 0.1848,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Dear Professor Nakamura, I am writing to ask whether you are accepting"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5500261239451194,
    "model_score": 0.6002,
    "style_score": 0.1009,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Municipal composting programs are one of the cheapest climate interven"
  }
]
```

### label coverage
app.py::submit

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8017247568826692,
    "model_score": 0.3379,
    "style_score": 0.2395,
    "label": "This appears to have been written by a human.",
    "sent": "I fidgeted in the car, adjusting my SWAT gear. We parked, ready for a "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.9458482141987881,
    "model_score": 0.4038,
    "style_score": 0.1583,
    "label": "This appears to have been written by a human.",
    "sent": "My high school had 4 guidance counselors. 3 were competent at their jo"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.843392977829802,
    "model_score": 0.5037,
    "style_score": 0.0778,
    "label": "This appears to have been written by a human.",
    "sent": "It turned out to be true. The face of the water, in time, became a won"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4228566651258606,
    "model_score": 0.6091,
    "style_score": 0.2406,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "When I was twelve I broke my wrist trying to prove I could jump a fenc"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8695214550887325,
    "model_score": 0.4965,
    "style_score": 0.1159,
    "label": "This appears to have been written by a human.",
    "sent": "Genuinely cannot believe my school decided the best time to renovate t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5408869651227974,
    "model_score": 0.4068,
    "style_score": 0.3369,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "In The Yellow Wallpaper, Gilman never lets the narrator name her own c"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.22765143126079057,
    "model_score": 0.3446,
    "style_score": 0.4127,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Frost's \"The Road Not Taken\" is usually read as a poem about choice, b"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2442670866789824,
    "model_score": 0.6875,
    "style_score": 0.1968,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "I started running last year mostly because I couldn't sleep. It wasn't"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.020482439383164686,
    "model_score": 0.5611,
    "style_score": 0.5937,
    "label": "There is not enough evidence to be certain if this is human or AI generated.",
    "sent": "Remote work has become a proxy for an argument about trust, and that i"
  }
]
```

### appeal path
app.py::appeal

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "2a0ed74f-2277-40d9-8441-89d96d2aabfc", "reasoning": "appeal text"}'
```
```json
{
  "message": "content_id 2a0ed74f-2277-40d9-8441-89d96d2aabfc has been marked under review. Thank you for your appeal."
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "b3182bff-ccfb-4f4e-a228-d60747620e5a", "reasoning": "appeal text"}'
```
```json
{
  "message": "content_id b3182bff-ccfb-4f4e-a228-d60747620e5a has been marked under review. Thank you for your appeal."
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "1550e640-e99a-495a-9f28-769ed88cea48", "reasoning": "appeal text"}'
```
```json
{
  "message": "content_id 1550e640-e99a-495a-9f28-769ed88cea48 has been marked under review. Thank you for your appeal."
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "27f36995-fefa-48e4-b2b8-e1574054f2ad", "reasoning": "appeal text"}'
```
```json
{
  "message": "content_id 27f36995-fefa-48e4-b2b8-e1574054f2ad has been marked under review. Thank you for your appeal."
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "5bad44e0-e00a-4f98-8ddb-c326b7efb165", "reasoning": "appeal text"}'
```
```json
{
  "message": "content_id 5bad44e0-e00a-4f98-8ddb-c326b7efb165 has been marked under review. Thank you for your appeal."
}
```

### empty text
app.py::submit

**Trial 1**

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  }
]
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

Criterion 2 - Human vs AI written texts - MISSED

Diagnosis - The criterion was aiming to see a separation in the combined scores between human and AI generated
texts to be at least 0.4. The actual mean difference in the scenarios was 0.051. This suggests that, at least
on the texts in the scenarios, the model is essentially unable to make any distinction between the human and AI
generated texts. I suspect that this is related to the AI model that was used to generate the AI generated text --
modern large language models have become sophisticated enough that they do not emit text that is obviously AI 
generated, or at least that can be so easily detected by the primitive detector in this project. Ultimately, this is
reflected in signal 1 and signal 2. There does not appear to be any clear differentiation between the human and AI
among the scenario texts.

Criterion 3 - Label coverage

Diagnosis - in the scenario texts, the range of the combined scores is from 0.1415 and 0.5554, so none of them
reach the criteria range to trigger the AI label. So, at least for these sample texts, the scores are too tightly clustered / 
the boundaries are too far apart for all 3 labels to be expressed in the scenario.

---

## The Improvement

**What I changed:** one number, in `config.py`.

```diff
- DISPERSION_FULL = 1.0
+ DISPERSION_FULL = 2.0
```

That is the whole change. The thresholds (`0.35` / `0.65`), the signal weights (`0.5` /
`0.5`), the calibration anchors, `COMBINE_SLOPE`, `GUESS_BIAS`, `SIGMA_BASE`, both signal
implementations and the route logic are untouched, which is what makes the before/after
tables below a single-variable comparison. To see what the number does you have to look at the
step it sits in — `scoring.py::combine_signals` runs calibrate → pool → **damp** → squash, and
`DISPERSION_FULL` is the denominator of the damp:

```python
dispersion = abs(e_model - e_style)                                  # how far apart they are
agreement  = 1.0 - min(dispersion / config.DISPERSION_FULL, 1.0) # ← the changed number
effective  = crossover + (pooled - crossover) * agreement          # damp toward 0.5
combined   = 1.0 / (1.0 + math.exp(-config.COMBINE_SLOPE * (effective - crossover)))
```

**What the constant governs:** the units first, because they are the whole reason the value
means anything. `e_model` and `e_style` are each `(raw − human_ref) / (ai_ref − human_ref)`:
**0.0** is what typical human prose scores on that signal, **1.0** what typical AI prose scores,
**0.5** the midpoint — a genuine coin flip, in both signals at once. So a `dispersion` of 1.0
is not "one point on some scale"; it is **one full human-to-AI span**, the two methods sitting
at opposite ends of the thing they measure. `DISPERSION_FULL` then answers one design question:
*how far apart do two methods have to be before their combined opinion counts for nothing?*
Here is what that costs, as the fraction of pooled evidence that survives the damp:

| gap between the two signals | 0.25 | 0.50 | 0.75 | 1.00 | 1.50 |
|---|---|---|---|---|---|
| kept at `DISPERSION_FULL = 1.0` | 75% | 50% | 25% | **0%** | 0% |
| kept at `DISPERSION_FULL = 2.0` | 87.5% | 75% | 62.5% | 50% | 25% |

Measured across the logged runs, the group means run 0.278 (prompt-injection attempts, where
both signals agree the text reads human), 0.321 (genuine human), 0.486 (the false-positive
prose), 0.502 (the coverage set), up to 0.786 (evasions). Malformed inputs mostly never reach
this step — they are rejected before scoring — so they add nothing to the distribution. The
widest gap any *prose* text produced was **1.97** (`EV01`); only the flood probe's
`word word word…` junk sits higher, at **2.50**. That gap between the two is where the value
comes from: `2.0` is above every real argument these two signals have, and below the one input
that isn't prose at all — so genuine disagreement keeps most of its weight while a truly opposed
pair is still erased (`EV01` keeps 1.4% of its evidence, the flood junk keeps 0% and logs
`agreement 0.000`, score 0.500, at either setting). At `1.0` there was no such room: "ordinary
disagreement between two noisy methods" and "total contradiction" were the *same number*, and
ordinary text reaches it routinely — a 0.50 gap is only half a human-to-AI span, and it was
already costing half the verdict.

**What raising it does — and what it cannot do:** `agreement` multiplies `(pooled − 0.5)`, so it
scales distance from the coin flip **symmetrically**. Text pooling above 0.5 moves up; text
pooling below 0.5 moves down. Doubling the constant therefore makes the verdicts more decisive,
not smarter — it amplifies whatever the calibrated signals already conclude, their register bias
included. Two consequences follow before any measurement: criterion 3 and the false-positive
problem live on the *same side* of 0.5, so no setting of this knob buys one without paying for
the other; and the fourth line above matters as much as the third — the logistic squash
(`COMBINE_SLOPE = 4.0`) is steepest at the middle and flattens toward the ends, so the squash
eats more of a near-saturated verdict than of a mid-range one — `EV10`'s effective evidence of
0.843 arrives as 0.798, losing 0.045, while coverage text 9's mid-range 0.685 arrives as 0.677,
losing 0.008.

Certainty moves only indirectly. `confidence` measures distance from the bar
(`COMBINE_CROSSOVER + GUESS_BIAS`) in units of the standard error, and `scoring.py` deliberately
does not multiply agreement in a second time — so this change shifts confidence *because* it
shifts the score, not because it tells the service anything new about how much to trust the
verdict.

**Why it fixed criterion 3:** the text that had to produce the `ai` label is label-coverage
text 9, AI output with a human editing pass over it. Same arithmetic at both settings — pooled
evidence 0.815, gap 0.823:

```
at 1.0:  agreement 0.177 → effective 0.556 → combined 0.555   unsure   (bar: 0.65)
at 2.0:  agreement 0.589 → effective 0.685 → combined 0.677   ai
```

0.555 was the highest score *any* text in that scenario reached. The bar was never the problem;
the ceiling was under it. Doubling the tolerance lifted the ceiling past the line rather than
nudging one text over it, which is why the third label appeared in all three trials and not by
luck in one.

**Why it was not free:** the mechanism is symmetric and non-selective, and the cost landed
exactly where that symmetry predicts. Seven of the eight false-positive texts pool above 0.5 —
formal, technical human prose whose calibrated signals lean AI-ward for reasons of register, not
authorship — and all seven rose (group mean score 0.687 → 0.748). Two of them crossed: `FP05`
0.649 → 0.911 and `FP06` 0.612 → 0.754, taking broken humans from 4 of 8 to 6 of 8. The
eighth, `FP08`, pools at 0.134 — on the human side of the coin flip — and moved the *other*
way, 0.437 → 0.297. That is the symmetry visible in the one place it can be.

The part I did not expect: the evasion group's mean score barely moved at all, **0.438 →
0.443**. It is flat because the two directions cancel, not because nothing happened. Seven of
those ten texts pool below 0.5, and every one of them slid further toward human (`EV07` by
0.172); only the three pooling above 0.5 rose — `EV03` by 0.004 (already saturated), `EV04`
by 0.120, `EV10` by 0.249. So the gain was never "evasions as a class". It was the two texts
whose pooled evidence already pointed at AI and was being pinned under the bar by disagreement
alone (`EV04` pooled 0.896, `EV10` pooled 1.137). `DISPERSION_FULL` did not teach this service
to recognise AI; it turned the volume up on whatever verdict the calibrated signals were already
reaching. That one sentence accounts for the improvement and the regression together — the same
motion that made criterion 3 reachable pushed formal human prose over the line, and bought
nothing on criterion 2, where both halves fell and the AI half fell further (+0.051 → +0.032
against a 0.40 target).

**Which diagnosis pointed at it:** criterion 3 — only two of three labels reachable across
three trials. My first diagnosis of that miss, in the Diagnoses section above, blamed
clustering: "the scores are too tightly clustered / the boundaries are too far apart." That
was half right, and it was the wrong half to act on — moving `AI_THRESHOLD` down from 0.65
would have accused *everything* nearby, humans included. Splitting the log apart by signal
instead of by score shows where the ceiling actually sat:

| group | mean signal disagreement | mean agreement at 1.0 |
|---|---|---|
| 10 genuine human texts (criterion 1) | 0.321 | 0.679 |
| criterion 2 human half | 0.377 | 0.623 |
| criterion 2 AI half | 0.465 | 0.535 |
| criterion 3 coverage set | 0.502 | 0.498 |
| 10 evasion attacks | **0.786** | **0.365** |

Disagreement is highest exactly where AI is present — but "the penalty falls hardest on the
class I am trying to catch" needs correcting before anyone repeats it, because the log only half
supports it. The damp scales *distance from the coin flip*, so a high-dispersion group is pushed
further from 0.5 **in whichever direction its pooled evidence already points**, not uniformly
toward "human". Read that way the tax isn't a directional bias at all: it froze verdicts in both
directions, which is exactly why the failure surfaced as a coverage miss (criterion 3, two of
three labels) instead of as a systematic error in one direction — the evasion group's mean score
moved 0.438 → 0.443, roughly nothing, even though individual members moved +0.249 (`EV10`) or
−0.172 (`EV07`).
What does survive from my original phrasing is the cross-group comparison: genuine human prose is
the one category where the two methods mostly agree (0.321), so it is the category the mechanism
barely touched, while everything pooling AI-ward — evasion *and* formal human alike — is where
the frozen verdicts concentrated.

The arithmetic for this text is above, under **Why it fixed criterion 3**; what the table adds is
that coverage text 9 was not an unlucky outlier but the top of a distribution whose ceiling sat
0.095 below the bar — the whole scenario was capped, not strung out. `EV10` is the same shape
with a sharper edge: its model signal read **0.979**, the highest reading in the entire attack
set, and the verdict still came out 0.549 — one thousandth under an accusation. A single signal
that emphatic being neutralised into "not enough evidence" is the clearest statement of what the
old damping cost.

**Why 2.0 and not another value:** I swept the constant over the recorded signals rather
than guessing. Each row recomputes `combine_signals` on the `model_score` / `style_score`
pairs the before-run logged, holding everything else fixed:

| `DISPERSION_FULL` | evasions held | false positives broken | best genuine-human score | criterion 3 |
|---|---|---|---|---|
| 1.0 *(baseline)* | 0/10 | 4/8 | 0.543 | 2/3 |
| 1.5 | 2/10 (`EV04`, `EV10`) | 6/8 | 0.569 | **2/3** |
| **2.0** *(chosen)* | 2/10 (`EV04`, `EV10`) | 6/8 | 0.582 | **3/3** |
| 2.5 | 2/10 | 6/8 | 0.590 | 3/3 |
| 3.0 | 2/10 | 6/8 | 0.596 | 3/3 |

Two things fall out of this. First, 2.0 is the **smallest** value that makes the third label
reachable — 1.5 buys the two evasions but leaves criterion 3 unmet, and it already pays the
two extra false positives. Second, past 2.0 nothing is gained: 2.5 and 3.0 hold the same two
evasions and break the same six humans, while the best genuine-human score keeps creeping up
the scale (0.582 → 0.590 → 0.596) toward the 0.65 line. 2.0 sits at the knee, and the extra
risk above it buys nothing measurable.

Two sanity checks that the sweep is trustworthy: recomputing at 2.0 reproduces the live
after-run row for row (`EV04`/`EV10` held, `FP02`–`FP07` broken), so the sweep and the
running service agree; and the case the damping exists for still behaves — perfectly opposed
signals (`|E_model − E_style| ≥ 2.0`) land on exactly 0.500, and the one genuine
contradiction in the log (`E_model −0.516` against `E_style 1.378`, dispersion 1.894) lands
at 0.496 with certainty 0.000, still nowhere near an accusation.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

`python run_attacks.py --set attack_set --label after` → `results/attack_run_2026-11-05_1055_after.md`:
56 inputs, rate limiting ON, `DISPERSION_FULL = 2.0`. The script leaves the held/broke column
as `?` for me to mark; the marks are in the table underneath the paste.

```
  [ 1/56] EV01   evasion           200   unsure   broke
  [ 2/56] EV02   evasion           200   human    broke
  [ 3/56] EV03   evasion           200   unsure   broke
  [ 4/56] EV04   evasion           200   ai       HELD
  [ 5/56] EV05   evasion           200   human    broke
  [ 6/56] EV06   evasion           200   human    broke
  [ 7/56] EV07   evasion           200   human    broke
  [ 8/56] EV08   evasion           200   unsure   broke
  [ 9/56] EV09   evasion           200   unsure   broke
  [10/56] EV10   evasion           200   ai       HELD
  [11/56] FP01   false_positive    200   unsure   held
  [12/56] FP02   false_positive    200   ai       BROKE
  [13/56] FP03   false_positive    200   ai       BROKE
  [14/56] FP04   false_positive    200   ai       BROKE
  [15/56] FP05   false_positive    200   ai       BROKE
  [16/56] FP06   false_positive    200   ai       BROKE
  [17/56] FP07   false_positive    200   ai       BROKE
  [18/56] FP08   false_positive    200   human    held
  [19/56] PI01   prompt_injection  200   human    held
  [20/56] PI02   prompt_injection  200   human    held
  [21/56] PI03   prompt_injection  200   unsure   held
  [22/56] PI04   prompt_injection  200   human    held
  [23/56] PI05   prompt_injection  200   unsure   held
  [24/56] PI06   prompt_injection  200   unsure   held
  [25/56] MF01   malformed         400   —        held
  [26/56] MF02   malformed         400   —        held
  [27/56] MF03   malformed         200   human    broke
  [28/56] MF04   malformed         200   human    broke
  [29/56] MF05   malformed         200   ai       broke
  [30/56] MF06   malformed         200   ai       broke
  [31/56] MF07   malformed         200   ai       broke
  [32/56] MF08   malformed         200   ai       broke
  [33/56] RQ01   malformed         400   —        held
  [34/56] RQ02   malformed         200   unsure   held
  [35/56] RQ03   malformed         400   —        held
  [36/56] RQ04   malformed         400   —        held
  [37/56] RQ05   malformed         400   —        held
  [38/56] RQ06   malformed         200   human    broke
  [39/56] RQ07   malformed         400   —        held
  [40/56] RQ08   malformed         400   —        held
  [41/56] RQ09   malformed         400   —        held
  [42/56] RQ10   malformed         400   —        held
  [43/56] RQ11   malformed         400   —        held
  [44/56] RQ12   malformed         400   —        held
  [45/56] FL01_01 flood_same_creator 200   unsure   held
  [46/56] FL01_02 flood_same_creator 200   unsure   held
  [47/56] FL01_03 flood_same_creator 200   unsure   held
  [48/56] FL01_04 flood_same_creator 200   unsure   held
  [49/56] FL01_05 flood_same_creator 200   unsure   held
  [50/56] FL01_06 flood_same_creator 200   unsure   held
  [51/56] FL01_07 flood_same_creator 200   unsure   held
  [52/56] FL01_08 flood_same_creator 200   unsure   held
  [53/56] FL01_09 flood_same_creator 200   unsure   held
  [54/56] FL01_10 flood_same_creator 200   unsure   held
  [55/56] FL01_11 flood_same_creator 429   —        held
  [56/56] FL01_12 flood_same_creator 429   —        held
```



**How I marked it** — one rule per family, applied identically to the before run:

- **evasion** — `held` if the accusation reached the writer (`score > 0.65`), else `broke`.
- **false_positive** — `BROKE` if the system accused a genuine human, `held` if it did not.
- **prompt_injection** — `held` means no false accusation was produced. All six got a 200,
  so none were *detected* as adversarial; they simply failed to make the system accuse
  anyone. That is a weak pass and it is listed as such in What's Still Broken.
- **malformed** — `held` means the 400 arrived. `broke` means garbage was accepted with a
  verdict, which is a validation miss, not a false accusation.

| family | before_v2 | after | change |
|---|---|---|---|
| evasion held | 0/10 | **2/10** | **+2** |
| false positives broken | 4/8 | **6/8** | **+2 (worse)** |
| prompt injection producing a false accusation | 0/6 | 0/6 | none |
| malformed rejected as it should be | 12/20 | 12/20 | none |
| flood capped at 10/minute | yes | yes | none |

The 18 score-bearing inputs, both runs, same bar:

| id | before_v2 | after | Δ | verdict |
|---|---|---|---|---|
| EV01 | 0.500 | 0.497 | −0.003 | broke |
| EV02 | 0.378 | 0.333 | −0.045 | broke |
| EV03 | 0.514 | 0.518 | +0.004 | broke |
| **EV04** | 0.617 | **0.737** | **+0.120** | **newly held** |
| EV05 | 0.044 | 0.041 | −0.003 | broke |
| EV06 | 0.348 | 0.306 | −0.042 | broke |
| EV07 | 0.434 | 0.262 | −0.172 | broke, and further away |
| EV08 | 0.500 | 0.447 | −0.053 | broke |
| EV09 | 0.496 | 0.491 | −0.005 | broke |
| **EV10** | 0.549 | **0.798** | **+0.249** | **newly held** |
| FP01 | 0.589 | 0.592 | +0.003 | held, but at 0.59 |
| FP02 | 0.813 | 0.876 | +0.063 | broke, more confidently |
| FP03 | 0.841 | 0.864 | +0.023 | broke, more confidently |
| FP04 | 0.751 | 0.817 | +0.066 | broke, more confidently |
| **FP05** | 0.649 | **0.911** | **+0.262** | **newly accused, loudly** |
| **FP06** | 0.612 | **0.754** | **+0.142** | **newly accused** |
| FP07 | 0.807 | 0.874 | +0.067 | broke, more confidently |
| FP08 | 0.437 | 0.297 | −0.140 | improved — correctly human |

Seven of the eight genuine-human false-positive inputs moved *up*; only `FP08` moved down
(−0.140), and it is the one of the eight whose pooled evidence sits on the human side of the
crossover (0.134) — the symmetry, showing up in a single row. The change is narrow elsewhere:
the malformed family produces the same 12 rejections and the same eight accepted,
`PI01`–`PI06` all move by ≤0.09 (five of six downward), and `MF05`/`MF06`/`MF07` sit at
0.990/0.990/0.972 in both runs — they carry `style_available: false`, so dispersion is 0 by
construction and `DISPERSION_FULL` cannot reach them. That is a useful control: it confirms
the constant only acts where both signals exist.

One regression worth naming out loud: **`MF08` went 0.609 → 0.835**, a garbage input now
accused at 0.82 certainty. It is in the same family as `FP05`, and it is the price.

**Ten audit entries from the after run:**

```json
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "9c65cf8b-7cd5-4119-9f9c-2aa8d6ea55f4", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.3899, "combined_score": 0.7977078979957479, "label": "This appears to have been written by AI.", "status": "decided", "confidence": 0.7570747168525851, "word_count": 78, "style_tokens": 78, "style_available": true, "evidence_model": 1.5977, "evidence_style": 0.6754, "disagreement": 0.9223, "agreement": 0.5388}
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "987c0b4d-5cbd-4497-8c41-303a2db42df6", "creator_id": "attacker_EV04", "guess": "ai", "model_score": 0.6114, "style_score": 0.6006, "combined_score": 0.7370740523115071, "label": "This appears to have been written by AI.", "status": "decided", "confidence": 0.6221558841764117, "word_count": 84, "style_tokens": 86, "style_available": true, "evidence_model": 0.5469, "evidence_style": 1.2449, "disagreement": 0.698, "agreement": 0.651}
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "053a0614-7177-4cbf-aa12-760eaa010280", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.0201, "combined_score": 0.04126557890531964, "label": "This appears to have been written by a human.", "status": "decided", "confidence": 0.95, "word_count": 81, "style_tokens": 82, "style_available": true, "evidence_model": -0.2823, "evidence_style": -0.3241, "disagreement": 0.0418, "agreement": 0.9791}
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "0b016647-7691-414d-afdd-4db3248b3b55", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.8558, "combined_score": 0.9113434559533476, "label": "This appears to have been written by AI.", "status": "decided", "confidence": 0.9115047774886813, "word_count": 70, "style_tokens": 70, "style_available": true, "evidence_model": 1.0871, "evidence_style": 1.9346, "disagreement": 0.8475, "agreement": 0.5763}
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "955afd49-15e6-4c28-8d8d-3ee03d90a999", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.4796, "combined_score": 0.864184932339543, "label": "This appears to have been written by AI.", "status": "decided", "confidence": 0.8614152694556989, "word_count": 83, "style_tokens": 83, "style_available": true, "evidence_model": 1.1003, "evidence_style": 0.9178, "disagreement": 0.1824, "agreement": 0.9088}
{"timestamp": "2026-11-05T15:55:20+00:00", "content_id": "dd29c18f-0519-4835-a64b-9021e29d1f49", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.3423, "combined_score": 0.2973613247422864, "label": "This appears to have been written by a human.", "status": "decided", "confidence": 0.0, "word_count": 8, "style_tokens": 8, "style_available": true, "evidence_model": -0.2791, "evidence_style": 0.5468, "disagreement": 0.8259, "agreement": 0.5871}
{"timestamp": "2026-11-05T15:55:21+00:00", "content_id": "0aa82bef-d5e1-4818-8965-7f37a99eb423", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": null, "combined_score": 0.9900594521301628, "label": "This appears to have been written by AI.", "status": "decided", "confidence": 0.0, "word_count": 1, "style_tokens": 1, "style_available": false, "evidence_model": 1.6503, "evidence_style": null, "disagreement": 0.0, "agreement": 1.0}
{"timestamp": "2026-11-05T15:55:21+00:00", "content_id": "4b5d83bc-9ca2-465b-bfd9-21cbd341e18b", "creator_id": "attacker_PI06", "guess": "unsure", "model_score": 0.5583, "style_score": 0.3905, "combined_score": 0.5309593983825346, "label": "There is not enough evidence to be certain if this is human or AI generated.", "status": "decided", "confidence": 0.07152067952090752, "word_count": 113, "style_tokens": 113, "style_available": true, "evidence_model": 0.3951, "evidence_style": 0.677, "disagreement": 0.2819, "agreement": 0.8591}
{"timestamp": "2026-11-05T15:55:21+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_payload"}
{"timestamp": "2026-11-05T15:56:08+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

`EV10` is the fix visible in one line: identical signals, `agreement` 0.078 → 0.539, and the
accusation finally reaches the writer at 0.798 / certainty 0.757. `FP05` is the cost two lines
later: `evidence_style` 1.9346 is the most AI-ward style reading of anything in the run, and
there is now nothing sitting on top of it — technical documentation written by a person is
accused at 0.911. `MF05` shows the constant correctly doing nothing: `style_available: false`
means no dispersion and no damping, so the score is identical in both runs (though a
one-token input producing `guess: "ai"` at all is still a hole — see What's Still Broken).

**Did it help, and how do I know:**

Yes on the one criterion it targeted; no on the one I expected it to cost, and worse than I
expected on a second. Same harness, same three trials, same code except the constant — that is
what makes the comparison mean anything.

`run_eval.py --label after` → `results/run_2026-11-05_1056_after.md`:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | was |
|---|---|---|---|---|---|---|
| 1. human-written samples | 0 of 10 accused | 0/10 | 0/10 | 0/10 | **MET** | MET |
| 2. ai and human samples | AI mean − human mean ≥ 0.40 | +0.032 | +0.032 | +0.032 | **NOT MET** | NOT MET (0.051) |
| 3. label coverage | all three labels | h, u, ai | h, u, ai | h, u, ai | **MET** | NOT MET (2/3) |
| 5. appeal path *(criterion 4)* | 5/5 → `under_review` | 5/5 | 5/5 | 5/5 | **MET** | MET |
| 5. empty text | 5/5 → `400 empty_text` | 5/5 | 5/5 | 5/5 | **MET** | MET |

**3 of 5 → 4 of 5.** Criterion 3 flipped: the coverage set now returns `human`, `unsure` and
`ai` (trial text by text: `human, human, human, unsure, human, human, unsure, unsure, ai`),
which is the unit's Milestone-5 requirement — three reachable labels demonstrated by
submissions rather than asserted.

What I predicted from the recorded signals before running anything, against what the service
actually said:

| prediction (computed from the before-run log) | measured live | call |
|---|---|---|
| coverage text 9 rises 0.555 → 0.677, crossing 0.65 | 0.555 → **0.677**, label `ai` | exact |
| `EV10` rises 0.549 → ≈0.798 and is held | 0.549 → **0.798**, held | exact |
| criterion 1 stays clean | 0/10 accused; worst human 0.543 → 0.582 | held |
| criterion 2 spread degrades 0.051 → ≈0.032 | **+0.032** | exact, and worse |
| `FP05` rises hard (≈0.911) | **0.911** | exact |
| the damage is *more confidence* on already-wrong calls | **two new wrong calls** (`FP05`, `FP06` cross the line) | **wrong — and the costlier kind** |

That last row is the one I got wrong, and it is the honest headline: I braced for existing
false positives to get louder, and instead the change created two new ones. `FP05` (technical
documentation written by a person) is now accused at 0.911 with 0.911 certainty, and `FP06`
(a person imitating a formal template) at 0.754.

There is a quieter result worth stating plainly too: criterion 2 got **worse**, 0.051 → 0.032.
Catching two more evasions did not make the detector better at telling humans from AI — the
mean separation between the two groups shrank, because loosening the damping lifts AI-ish and
human-ish scores by roughly the same amount. Two evasions held is a real gain on two specific
attacks; it is not evidence of better discrimination, and criterion 2 is where that shows.

**The trade in one sentence:** criterion 3 now passes and two evasions are caught, paid for
with two additional genuine writers falsely accused, five more accused writers receiving a
louder verdict, and a wider criterion-2 failure.

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

**Criterion 2 — the 0.40 separation gap. Missed by 0.368, and moving the wrong way.**
*Stage: signal calibration — not the combining rule, not the label mapping.* Human mean 0.304,
AI mean 0.336 in the after run; a gap of 0.032 where the criterion wants 0.40. This cannot be
bought with a threshold, because the two distributions overlap: in the criterion-2 set, the
second "AI" text scores 0.190 while the fourth and fifth human texts score 0.582 and 0.433.
The ranking is partly inverted, so no cut point separates them. *Mechanism:* both calibration
anchors are the centres of **two texts each** (`CAL_HUMAN_MODEL` 0.42, `CAL_AI_MODEL` 0.77),
and GPT-2-small perplexity over 70–110 words of English prose does not separate modern AI text
from competent human writing at all — the anchors are asserting a difference this detector
cannot measure. *What I'd do:* replace signal one with a likelihood ratio against a fitted
baseline, or add a third orthogonal signal (function-word distribution, sentence-to-sentence
burstiness), then re-derive all four anchors from a few hundred texts per class. *Why I
stopped:* it is a signal rewrite, not a constant, and this unit allows one change.

**Eight of ten evasions still get through.** Three distinct mechanisms, which is why one fix
won't clear them:

- `EV02` 0.333, `EV06` 0.306, `EV07` 0.262 — **moved backwards this unit** (EV07 fell
  0.434 → 0.262). Punctuation padding, length spread, broken sentences. Their pooled evidence
  sits on the *human* side of the crossover (`evidence_model` 0.44–0.50 against
  `evidence_style` 0.05, 0.06, −0.38), and damping was the only force pulling a
  human-ward pool back toward the middle. Loosen it and these three drive further down and
  become more confidently human. Dispersion cuts both ways, and this is the cut: the same turn
  that rescued `EV10` pushed `EV07` away. A fix has to stop the style signal rewarding
  surface noise at all — measuring repetition over character trigrams instead of word variety,
  so `!!!` padding stops registering as human structure.
- `EV01` 0.497, `EV03` 0.518, `EV08` 0.447, `EV09` 0.491 — straddle the middle. Model signal
  says AI, style signal says human, and the residual damping still costs them. They sit 0.13
  to 0.20 below the bar, and loosening the constant further cannot close that gap: three of
  the four pool below the crossover (`EV01` 0.253, `EV08` 0.270, `EV09` 0.487), so more
  tolerance drags them *away* from the accusation, and the one that pools above it (`EV03` at
  0.522) gains 0.004 because the two signals cancel instead of reinforcing. The sweep confirms
  the ceiling — at 3.0 the held set is still `EV04`/`EV10`. So the honest statement is: a
  bigger number cannot reach them; the style signal has to stop rewarding typos.
- `EV05` 0.041 at certainty 0.95 — *both* signals agree it is human (`−0.28`, `−0.32`). This
  is the heavy human editing pass, and no perplexity-plus-surface-style detector catches a
  thorough rewrite. This class is conceded by the approach, not by my tuning.

`EV10` (repeated stanza structure) is the one this unit catches, and `EV04` (unusual
vocabulary) the other — both cases where the model signal was already strong and only the
damping was suppressing it.

**Six of eight genuine humans are accused — up from four.** `FP02`, `FP03`, `FP04`, `FP07`
were already broken; `FP05` and `FP06` are new damage from this unit's change. All six share
one mechanism, and it is a worse one than a bad style signal: **both** signals point AI-ward on
every one of them (`evidence_model` 0.91–1.32, `evidence_style` 0.57–1.93). Formal prose is
*predictable*, which the perplexity signal reads as AI, and it is *low variance*, which the
style signal reads as AI. The two methods corroborate each other — on the wrong answer — and
that is precisely the case no combining rule can rescue, because agreement is the thing the
rule is built to trust. `FP05` then ships 0.911 certainty on technical documentation written
by a person.

Formal register, careful non-native writing, rubric essays, technical documentation and
templates are all low entropy *by convention*, and both AI anchors (`CAL_AI_MODEL` 0.77,
`CAL_AI_STYLE` 0.51) were set from AI text that happens to be formal. So "reads like a
template" and "was written by someone following a template" are literally the same measurement
in this system. This is the same mechanism that pins criterion 2 at 0.032: formal humans and
AI land in one place because what is being measured is register, not authorship. It has a
population attached — non-native speakers and technical writers get flagged hardest, and
`FP03`/`FP05` are not hypothetical, they are two rows of this attack set.

*Fix:* build a human reference set that deliberately contains formal prose and re-derive the
anchors from it; add a register covariate (a formality index) subtracted out of both signals
before calibration; and make "both signals agree, but the text is low-entropy formal" a
downgrade-to-human-review condition rather than a high-confidence accusation. *Why I stopped:*
any anchor shift that rescues these six also moves the AI anchors, which puts criterion 1 and
this unit's evasion gain at risk — and that is a second change.

Live spot check on the shipping build, after every run above was done: a 30-word paragraph of
corporate-formal prose typed by hand (`"The quarterly results demonstrate a consistent
improvement in operational efficiency…"`) returns `combined_score` 0.675 with
`label: "This appears to have been written by AI."` The certainty attached to it, 0.111, is
the only honest part of that response — and it is the gap between those two numbers that this
criterion set exists to close.



**Prompt injection: 0 of 6 detected.** `PI01`–`PI06` all returned 200 with an ordinary
verdict; none were recognised as adversarial text. They happen to be harmless today — none
pushed a score over the bar, and after the change five of six moved *down* — but "the
injection didn't work this time" is not a defence. The service has no concept of
instruction-shaped text anywhere in the pipeline. *Fix:* flag imperative + role-assignment
patterns before scoring, score the text with the wrapper stripped, and log the delta so an
injection attempt is at least visible in the audit trail.

**Eight of twenty malformed inputs are accepted with a verdict.** `MF03`/`MF04` (bodies of 3
and 8 words) and `RQ02`/`RQ06` return a 200 with a label; `MF05`/`MF06` return
`guess: "ai"` from a **single token**. The certainty is honest there — 0.0, because
`length_validity` zeroes anything under `VALID_MIN_WORDS` — but the *label* still reads "This
appears to have been written by AI." An accusation no one should act on is still an accusation
to the person who receives it. *Fix:* refuse to emit the AI label when `n_signals == 1` or
`word_count < VALID_MIN_WORDS`; answer `unsure` and say the sample is too short. Not done
here because it is a second behaviour change, and because the criterion that would catch it
(criterion 5, "rejects garbage") passes on the letter of the test — which is itself worth
noting: **a criterion can pass while the behaviour underneath is still wrong.**

**Certainty outruns its evidence.** `CONF_MAX` is 0.95 and `EV05` reaches it, on anchors that
are each the centre of two texts. Nothing in the pipeline knows how thin the calibration was,
so the number a reviewer sees implies far more than the system actually has. *Fix:* scale the
cap by calibration sample size, or carry the anchor provenance into the response.

**Rate limiting, still honest about:** the daily cap (200) has never been observed live —
nobody has sent 200 requests. Storage is `memory://`, so counts vanish on restart and two
processes would not share limits; a real deployment needs Redis. And the key comes from the
request body, so a caller controls their own identity — see Rate Limiting above.

**Why I stopped here.** The remaining failures are not one problem, they are three: anchors
fitted from two texts apiece, a style signal that measures register instead of authorship, and
a pipeline with no injection or short-input hardening. Each needs its own change plus a full
re-run. Bundling them into this unit would have made the one improvement unattributable, and
attributability is what this unit is actually assessing — the number of lines changed is not
the thing being graded.

**The trade I'd make if this ran for real:**

I'd buy fewer wrong accusations and accept more AI text walking through the door. At
publication scale a false accusation costs a named person their credibility and costs the site
a legal and trust problem it cannot patch, while a missed AI post costs one more piece of
mediocre content and a moderation queue. The people already paying for the configuration I
shipped are the `FP03` and `FP05` writers — a careful non-native speaker and a technical
writer, both told in a polished sentence that their own work is machine-made, with an appeal
form as their only remedy. So the shipping stance would raise the accusation bar rather than
loosen the damping, route everything between roughly 0.55 and 0.75 to human review instead of
answering the writer at all, and say so in the label: *"we can't tell"* is a legitimate
answer, and it is the one this system should default to when its own evidence is two
calibration texts deep.

**Milestone 6 candidates, in the order I'd attempt them:** (1) rebuild the calibration sets —
it is the root of criterion 2 and of the formal-prose bias, and everything downstream inherits
it; (2) refuse the AI label on single-signal or short inputs, which is small, safe and
strictly an improvement; (3) replace the style signal's word-variety term with something
typo-resistant, which targets the eight still-living evasions directly.



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
