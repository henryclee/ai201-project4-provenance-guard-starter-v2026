"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400


# ─── Scoring: calibration (Milestone 4) ──────────────────────────────────────
# Both signals answer the same question — how likely is this AI? — but they do NOT
# answer it on the same scale, and combining them before fixing that is the mistake
# this whole section exists to prevent.
#
# Measured over milestone4_text.txt (two human pieces, two AI pieces):
#
#     model signal    human 0.34, 0.50     AI 0.70, 0.83
#     style signal    human 0.04, 0.24     AI 0.50, 0.52
#
# So `0.5` carries no shared meaning. On the model signal 0.5 is perplexity 45,
# which ordinary human writing reaches — the Human sample scored 0.336 and the
# Formal sample 0.499, one thousandth of a point from being called AI. On the style
# signal 0.5 is already a suspicious reading, yet blatant AI boilerplate only just
# clears it at 0.519. One shared bar at 0.5 would have the model accusing plain
# human prose while style could barely convict the obvious machine text in front of it.
#
# The fix: calibrate each signal against two reference points of its own and convert
# it to EVIDENCE UNITS before anything is combined or compared to a threshold.
#
#     evidence = (signal - HUMAN_REF) / (AI_REF - HUMAN_REF)
#
#     0.0  = what typical human prose scores on that signal
#     1.0  = what typical AI prose scores
#     0.5  = midway between the two: a genuine coin flip, in BOTH signals
#     <0, >1 = more human / more AI than typical, resolution kept (not clamped)
#
# ⚠️ PLACEHOLDER — and this is the weakest link in the service. Every reference
# below is the centre of TWO texts. Two is not a corpus. Before unit 8, replace all
# four with the centre of 10 pieces of your own writing against 10 generated ones
# and re-check everything downstream. The gap also encodes a blind spot worth naming:
# the AI references come from obvious boilerplate, so formulaic HUMAN prose (student
# essays, corporate memos, form letters) is the human writing that sits closest to
# the line we accuse on.
CAL_HUMAN_MODEL = 0.42  # PLACEHOLDER — centre of human model scores (n=2)
CAL_AI_MODEL = 0.77  # PLACEHOLDER — centre of AI model scores (n=2)
CAL_HUMAN_STYLE = 0.14  # PLACEHOLDER — centre of human style scores (n=2)
CAL_AI_STYLE = 0.51  # PLACEHOLDER — centre of AI style scores (n=2)

# How much each calibrated signal counts. Because weights now sit on evidence units
# rather than on two differently-scaled 0-1 outputs, 0.5/0.5 is a claim about which
# method we trust, not an artefact of how the two happen to be numbered.
#
# Measured effect on milestone4_text.txt: mean human-vs-AI separation is 0.675 with
# calibrated evidence, 0.408 with uncalibrated log-odds, and 0.360 with the plain
# weighted average this starter ships with. Equal weights are still a guess.
WEIGHT_MODEL_SIGNAL = 0.5
WEIGHT_STYLE_SIGNAL = 0.5


# Pooling. The weighted mean of the two evidences is damped toward the coin-flip
# point in proportion to how far apart the signals sit — disagreement of
# DISPERSION_FULL units pins the verdict at exactly 0.500, because two methods
# disagreeing IS uncertainty and needs no special-case branch. Damping the
# EVIDENCE rather than clamping probabilities is what keeps the clearly-human and
# clearly-AI ends distinguishable instead of saturating both at 0.0 and 1.0.
#
# ⚠️ UNIT 8, MILESTONE 5 — THE ONE CHANGED NUMBER IN THIS UNIT: 1.0 -> 2.0.
#
# Mean signal disagreement, measured over the scenario texts and logged decisions in
# logs/audit.jsonl (values are |evidence_model - evidence_style|, in evidence units):
#
#     10 genuine human texts        0.321   (mean agreement 0.679)
#     criterion 2 human half        0.377   (mean agreement 0.623)
#     criterion 2 AI half           0.465   (mean agreement 0.535)
#     criterion 3 coverage set      0.502   (mean agreement 0.498)
#     10 evasion attacks            0.786   (mean agreement 0.365)  <-- most disagreed
#
# Disagreement is therefore HIGHEST exactly where AI is present, and at 1.0 a routine
# 0.5-0.8 unit gap deleted 50-80% of the pooled evidence. Mind the direction, because the
# damping is SYMMETRIC: it pulls toward the coin flip, so it drags a verdict DOWN only when
# the pooled evidence sits ABOVE 0.5 — which is true of the texts this unit needed to catch
# (EV04 pooled 0.896, EV10 1.137, coverage text 9 0.815) and of the formal-human false
# positives. The seven evasion texts pooling BELOW 0.5 went the other way, further into
# "human", which is why the evasion group's mean score barely moved (0.438 -> 0.443) even
# though individual members moved by as much as 0.249. Full breakdown in README, section
# "The Improvement". Two logged examples:
#
#     EV10  e_model 1.598, e_style 0.675, dispersion 0.922 -> agreement 0.078. The
#           model signal read 0.979, its highest reading in the whole set, and the
#           combined score came out 0.549: one thousandth under the accusation bar.
#     label-coverage text 9 (human-edited AI): e_model 0.403, e_style 1.226,
#           dispersion 0.823 -> agreement 0.177 -> combined 0.555, the best score any
#           scenario text ever produced, still 0.095 short of AI_THRESHOLD. Which is
#           why criterion 3 could only ever reach 2 of 3 labels: the ceiling sat below
#           the line, so no submission in the scenario could have crossed it.
#
# At 2.0, ordinary disagreement (0.5-0.8 units) costs 25-40% of the evidence instead of 50-80%.
# Where the value came from: the widest gap any PROSE text in the log produces is 1.97 (EV01);
# the only input above it is the flood probe's "word word word..." junk at 2.50. So 2.0 sits
# above every real argument the two signals ever have and below the one input that is not prose
# at all — real disagreement keeps most of its weight, and a genuinely opposed pair is still
# erased. Checking that the case this damping exists for still behaves:
#
#     flood junk  e_model -1.118, e_style 1.378, dispersion 2.496 -> agreement 0.000, score
#                 0.500, certainty 0.000 at BOTH settings (2.496 >= DISPERSION_FULL either way)
#     prose       e_model -0.516, e_style 1.378, dispersion 1.894 -> 0.500 at 1.0, 0.496 at
#                 2.0, certainty 0.000 either way
#
# 0.496 rather than exactly 0.500 is the honest cost of the change: 0.004 off a coin flip, with
# the certainty still pinned at zero. Stating it because "still behaves" is not the same as
# "behaves identically", and the difference is the kind of thing a later unit trips over.
COMBINE_CROSSOVER = 0.5  # evidence separating a human-ward verdict from AI-ward
COMBINE_SLOPE = 4.0  # how hard the pooled evidence is squashed onto 0-1
DISPERSION_FULL = 2.0  # disagreement (in evidence units) that zeroes the verdict
#                                       ^ was 1.0 — see the measurement block above

# The verdict bar sits at the crossover PLUS a leniency bias, so calling something AI
# means clearing 0.55 rather than 0.50. That 0.05 is the Milestone 1 false-positive
# decision written down as a visible number: a wrong accusation costs a writer far
# more than a missed detection costs the site. Ties go human.
GUESS_BIAS = 0.05

# ─── Certainty (Milestone 4) ─────────────────────────────────────────────────
# Certainty answers a different question from the score. The score says WHICH WAY;
# certainty says how sure we are that the LABEL is right — 0.0 = no idea, 1.0 = sure.
# Direction stays in the score and the guess, so the two numbers cannot contradict.
#
#     z = |score - GUESS_BAR| / (SIGMA_BASE / sqrt(n_signals used))
#     certainty = erf(z / sqrt(2)) * length_validity, capped at CONF_MAX
#
# The sqrt(n) is the standard-error argument: one usable signal is noisier than two
# independent ones, so a verdict resting on the model alone is automatically less
# certain without a special case anywhere in the code.
#
# ⚠️ SIGMA_BASE is the single most influential number in this service. It is the
# standard deviation of combined scores WITHIN one class — how much honest overlap
# there is between human and AI writing — and it sets how confident the system is
# ever allowed to sound. Sensitivity, over the four milestone4 texts (Human, Formal,
# edited AI, AI):
#
#     SIGMA_BASE 0.20  ->  certainties 0.95 / 0.95 / 0.66 / 0.50
#     SIGMA_BASE 0.30  ->  certainties 0.95 / 0.82 / 0.40 / 0.60   (shipped)
#     SIGMA_BASE 0.50  ->  certainties 0.84 / 0.57 / 0.44 / 0.27
#
# Nothing in that table is defensible until it is measured on a real corpus, which is
# why it ships as a PLACEHOLDER rather than dressed up as a tuned value.
SIGMA_BASE = 0.30  # PLACEHOLDER — within-class sd of combined scores
CONF_MAX = 0.95  # never claim certainty 1.0; also keeps log-odds finite

# How much text a measurement needs before it is worth anything at all.
VALID_MIN_WORDS = 20  # at/below this, certainty is 0.0 — sample too small
VALID_FULL_WORDS = 60  # at/above this, length costs nothing

# Below this the request is refused rather than scored. Three words is not a stylistic
# sample, and it is the floor the model itself imposes: perplexity needs a trigram to
# measure anything, and `detector.perplexity` raises below that. Refusing with a clear
# 400 is what stops "hello" becoming a 500 in someone's integration, and it is logged as
# a rejection rather than a decision so a pattern of probing the endpoint with junk stays
# visible in the log.
MIN_SUBMIT_WORDS = 3

# ⚠️ Why there is a CHARACTER floor next to the word floor. `len(text.split())` is a
# fragile counter: one run-on line, a hyphenated stretch, or a paste that arrived with
# its newlines stripped counts as a single word while still being plenty of text for the
# model to score. So the gate is "too short by BOTH measures" — few words AND few
# characters. Either floor on its own would refuse something scorable.
MIN_SUBMIT_CHARS = 12

# A signal that cannot measure the text is ABSENT — not weak evidence, not evidence
# of anything. Below a handful of tokens the spread metrics describe whichever words
# happened to be there rather than how anything was written, and each one drifts toward
# whichever end of its range a stub input lands on. Below this floor style is dropped
# from the combination: the verdict rests on the model alone, and `confidence` pays for
# it through n_signals. `style_score` comes back null rather than 0.0 when it is dropped,
# because an unmeasured signal written as a number would be a small lie that flatters
# whoever that number points at. See `scoring.combine_signals`.
STYLE_MIN_TOKENS = 8


# ─── Style signal (Milestone 4) ──────────────────────────────────────────────
# stylometry.py measures three raw properties of the text. Each one returns a
# RAW value whose high end means "more human":
#
#   sentence_length_spread   CV of sentence lengths,  ~0.05 .. ~0.8
#   type_token_ratio         unique words / total,      0 .. 1
#   punctuation_density      marks per 100 words,       ~0 .. ~12
#
# `style_signal` is the only place direction gets decided. It inverts all three
# (human-ward raw -> AI-ward) using the anchors below, puts them on a shared
# 0–1 scale, and weights them. Output convention matches detector.model_signal:
#
#   0.0 = looks human .......................... 1.0 = looks AI
#
# ⚠️ EVERY anchor below is a PLACEHOLDER. There is no calibration corpus yet —
# these are informed guesses about direction and rough magnitude, not measured
# values. When baseline texts exist, replace the six anchors and nothing else in
# the design has to change:
#
#     grep -n PLACEHOLDER config.py
#
# The weights are relative influence, normalised by their sum inside
# style_signal, so setting one to 0.0 retires that metric without shifting
# anyone else's scale.

STYLE_WEIGHT_SPREAD = (
    0.45  # sentence-length regularity — the strongest idea of the three
)
STYLE_WEIGHT_LEXICON = 0.35  # vocabulary variety, length-corrected
STYLE_WEIGHT_PUNCT = 0.20  # punctuation rate — cheapest to spoof, so lightest weight

# The anchor rule, because three numbers with no rule behind them are three
# guesses: put the HUMAN anchor at the median of real human prose and the AI
# anchor at or below its 5th percentile, so a metric only reaches 1.0 on text more
# uniform than almost anything human writing manages. That leniency is deliberate —
# a false accusation is the expensive error here, a missed AI text the cheap one.
# Measured on 36 paragraphs of this repo's own prose (three sentences or longer):
#
#     spread CV      p05 0.195   median 0.546   p95 1.196
#     MTTR/25w       p05 0.820   median 0.901   p95 0.967
#     marks per 100  p05 3.12    median 6.15    p95 13.79
#
# Two consequences of that rule, recorded because they are design facts and not
# details:
#
#   1. Every metric clamps, so `style_signal` can return exact 0.0 and exact 1.0 —
#      infinite log-odds. Floor them with an epsilon if `combine_signals` goes
#      log-odds in Milestone 5.
#   2. The lexicon metric is the weakest of the three. Roughly 5% of genuine human
#      paragraphs already fall below 0.820 MTTR, while fluent AI prose typically
#      sits near 0.90 — word-level vocabulary variety is not what gives generated
#      text away; phrase-level recycling is. If a calibration corpus confirms that,
#      swap the measure for n-gram repetition and cut STYLE_WEIGHT_LEXICON; the
#      weight is a lever, which is the point of putting it here.

# Metric 1 — coefficient of variation of sentence lengths (stdev / mean).
# Human prose is lumpy, generated prose marches in step. High raw = human, so
# style_signal inverts it.
SPREAD_HUMAN = 0.55  # PLACEHOLDER — median CV of human prose, measured above
SPREAD_AI = 0.18  # PLACEHOLDER — just under the human floor (p05 0.195)

# Metric 2 — vocabulary variety. High raw value = more varied = human, so this is
# the measure that needs the inversion (`adj_ttr = 1 - ttr`), applied through the
# anchors rather than as a hand-written `1 - x` at the call site. The anchors are
# what make it a *generalised* `1 - x`: set LEXICON_HUMAN = 1.0 and LEXICON_AI =
# 0.0 and the line becomes literally that. Tighter anchors ship by default because
# real TTRs crowd the top of the range (0.82-0.97 measured); under literal `1 - x`
# the metric sits near zero all day and its weight below is mostly fiction.
LEXICON_HUMAN = 0.90  # PLACEHOLDER — median windowed TTR of human prose
LEXICON_AI = 0.72  # PLACEHOLDER — near the human floor (0.70 seen, p05 0.820)
STYLE_LEXICON_WINDOW = 25  # moving-average TTR window in words; 0 = global TTR

# Metric 3 — comma-class punctuation per 100 words.
# Comma-class marks carry the weight because a set of only `; : —` sits at zero for
# most ordinary prose, which pins the metric at one end for every text. Apostrophes
# are excluded on purpose: `don't` and `it's` would score contractions as
# punctuation and hand informal writing a free human reading.
PUNCT_HUMAN = 6.5  # PLACEHOLDER — median marks per 100w of human prose
PUNCT_AI = 2.5  # PLACEHOLDER — just under the human floor (p05 3.12)
STYLE_PUNCT_CHARS = ",;:()\u2014\u2013\u201c\u201d\u2026"  # , ; : ( ) — – “ ” …


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Where one label becomes another. Scores run 0.0 (confidently human) to 1.0
# (confidently AI).
#
#   score < HUMAN_THRESHOLD          -> high-confidence human
#   between the two                  -> unsure
#   score > AI_THRESHOLD             -> high-confidence AI

HUMAN_THRESHOLD = 0.35
AI_THRESHOLD = 0.65

# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

# UNIT 8, MILESTONE 1 — ON. This was switched back to a hard `False` in the unit 7
# Milestone 4 commit (the flood evidence in results/flood_2026-11-04_1910.md was
# captured while it was True), which is why GET /health reported limiting off.
# Restored here so the attack set's flood_same_creator family can be judged honestly.
# Escape hatch kept from the starter: start the SERVICE with `AI201_RATE_LIMITS=0`
# (`AI201_RATE_LIMITS=0 python app.py`) to run the three-trial evaluation without the
# per-creator budget interfering, since the appeal-path and empty-text scenarios each submit
# five bodies under one shared creator_id. The flag is read once at import, so it must be
# set on the server process — setting it on the run_eval.py client changes nothing.
RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "1") == "1"

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
