"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

What lives here:

    combine_signals  ← IMPLEMENTED (Milestone 4): calibrate, pool, damp, squash
    score_breakdown  ← the same rule with every intermediate exposed, for the log
    guess_from_score ← the binary call, at the crossover plus a leniency bias
    confidence       ← how sure we are that the guess is right, 0.0 to 1.0
    score_to_label   ← TODO (Milestone 5): still a stub

`combine_signals` is where your false-positive decision from Milestone 1 actually gets
made — the bar it puts at 0.55 IS that decision, written as a number. Everything above
it, the labels and the appeal path, is downstream of a number this function produced.
The one thing deliberately NOT built here yet is `score_to_label`, so `label` stays
"placeholder" in the API and Milestone 5's criteria are expected to fail.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import math

import config


# ─── Calibration: getting two rulers to agree ─────────────────────────────────
# config.py holds the measured reference points and the reasoning behind them. This is
# the arithmetic that uses them. Read the "Scoring: calibration" block there first.


def _evidence(raw: float, human_ref: float, ai_ref: float) -> float | None:
    """
    One signal, expressed in evidence units instead of its own arbitrary scale.

        evidence = (raw - human_ref) / (ai_ref - human_ref)

    0.0 = what typical human prose scores on this signal. 1.0 = what typical AI prose
    scores. 0.5 = exactly halfway between them, which is what makes 0.5 finally mean
    the same thing in both signals: a real coin flip.

    Values outside 0-1 are KEPT rather than clamped. A text that is more human than the
    typical human is genuine information, and flattening it against a ceiling would
    throw away exactly the separation the calibration exists to reveal.

    Returns None when the references are unusable — unset, equal, or the wrong way
    round — so callers fall back to raw scores instead of dividing by zero or, worse,
    running the whole scale backwards in silence.
    """
    gap = ai_ref - human_ref
    if gap <= 0:
        return None
    return (raw - human_ref) / gap


def calibration_available() -> bool:
    """Do both signals have reference points far enough apart to calibrate against?"""
    return (
        config.CAL_AI_MODEL - config.CAL_HUMAN_MODEL > 0
        and config.CAL_AI_STYLE - config.CAL_HUMAN_STYLE > 0
    )


def signal_evidence(name: str, value: float) -> float:
    """
    Calibrated evidence for one named signal, "model" or "style".

    Falls back to the raw value when calibration is unavailable, which keeps this
    function total: callers never handle None, and never get a verdict quietly built on
    a division that made no sense.
    """
    human_ref, ai_ref = {
        "model": (config.CAL_HUMAN_MODEL, config.CAL_AI_MODEL),
        "style": (config.CAL_HUMAN_STYLE, config.CAL_AI_STYLE),
    }[name]
    evidence = _evidence(value, human_ref, ai_ref)
    return value if evidence is None else evidence


def combine_signals(
    model_score: float,
    style_score: float,
    style_available: bool = True,
) -> float:
    """
    Two 0-1 signals in, one 0-1 score out. ← Milestone 4's combining rule.

    All three numbers point the same way: higher means more likely AI.

    The rule, in words:

      1. CALIBRATE each signal into evidence units against its own human and AI
         reference points — because 0.5 means "perplexity 45, which plain human prose
         reaches" in the model signal and "already suspicious" in the style signal, and
         a rule that averages the two is averaging different questions.
      2. AVERAGE the two evidences by weight. Weights now act on comparable units, so
         0.5/0.5 means equal trust rather than equal-looking decimals.
      3. DAMP the average back toward the coin-flip point in proportion to how far
         apart the signals sit. Two perfectly opposed signals land on exactly 0.500:
         two methods disagreeing IS uncertainty, and it needs no special-case branch.
      4. SQUASH once, at the end, onto 0-1.

    `style_available=False` drops style rather than scoring it. Absent evidence is not
    evidence of anything — see STYLE_MIN_TOKENS in config.py for why a signal that could
    not read the text gets dropped rather than read as a low score.

    ⚠️ Your README's **Signals and Scoring** section names this function as where the
    rule lives, so a change to the arithmetic here is a change to that prose too. The
    grader checks the claim against the code.
    """
    return score_breakdown(model_score, style_score, style_available)["combined_score"]


def score_breakdown(
    model_score: float,
    style_score: float,
    style_available: bool = True,
) -> dict:
    """
    Every intermediate from the combining rule, for the audit log and for tests.

    A lone number in a log records the verdict; it does not record the REASON, and the
    reason is the thing you need at 2am when a writer appeals and asks why their essay
    was flagged. This returns the calibrated evidences, how far apart they sat, what the
    verdict came to, and which way the guess fell — so a decision can be reconstructed
    later instead of re-guessed.

    `combine_signals` is a one-line call into here, which means there is exactly one
    implementation of the rule and no chance of the logged numbers and the returned
    number drifting apart.
    """
    crossover = config.COMBINE_CROSSOVER
    e_model = signal_evidence("model", model_score)

    if style_available:
        e_style = signal_evidence("style", style_score)
        w_total = config.WEIGHT_MODEL_SIGNAL + config.WEIGHT_STYLE_SIGNAL
        pooled = (
            config.WEIGHT_MODEL_SIGNAL * e_model + config.WEIGHT_STYLE_SIGNAL * e_style
        ) / w_total
        # Distance apart, in evidence units. Two independent methods that land a full
        # unit apart have told you opposite things about the same text.
        dispersion = abs(e_model - e_style)
        n_signals = 2
    else:
        # Nothing to disagree WITH is not agreement, so dispersion stays 0 and the
        # damping does nothing; the penalty for a lone signal is paid in `confidence`,
        # where n_signals widens the noise.
        e_style = None
        pooled = e_model
        dispersion = 0.0
        n_signals = 1

    agreement = 1.0 - min(dispersion / config.DISPERSION_FULL, 1.0)
    effective = crossover + (pooled - crossover) * agreement
    combined = 1.0 / (1.0 + math.exp(-config.COMBINE_SLOPE * (effective - crossover)))

    return {
        "evidence_model": e_model,
        "evidence_style": e_style,
        "evidence_pooled": pooled,
        "disagreement": dispersion,
        "agreement": agreement,
        "evidence_effective": effective,
        "n_signals": n_signals,
        "style_available": style_available,
        "combined_score": combined,
        "guess": guess_from_score(combined),
    }


def guess_from_score(score: float) -> str:
    """
    The binary call: the crossover PLUS the leniency bias, so 0.55 not 0.50.

    An accusation has to clear a gap rather than just tip the scales, because a wrong
    accusation costs a writer more than a missed detection costs the site. Anything at
    or below the bar is human, so ties go human and the bias is one-directional by
    design — it only ever protects the person being judged.

    This stays binary on purpose. "Unsure" is a LABEL, and the label is `score_to_label`'s
    call (Milestone 5), made from the band and the certainty. The guess is where the
    false-positive decision lives, and that decision is `GUESS_BIAS`.
    """
    if score > config.COMBINE_CROSSOVER + config.GUESS_BIAS:
        return "ai"
    return "human"


def length_validity(word_count) -> float:
    """
    How much a submission's length earns its certainty: 0.0 to 1.0.

    Twenty words is not a sample of anybody's writing. At or below VALID_MIN_WORDS
    nothing concluded from the text deserves to be called certain at all, and the ramp
    up to VALID_FULL_WORDS means the penalty fades as the evidence gets more substantial
    rather than switching off at an arbitrary line.

    Multiplying rather than adding is the point: 40% of the words does not buy 40% of a
    verdict on top of whatever else you were sure about, it scales whatever you had.
    """
    if word_count is None:
        return 1.0
    if word_count <= config.VALID_MIN_WORDS:
        return 0.0
    if word_count >= config.VALID_FULL_WORDS:
        return 1.0
    span = config.VALID_FULL_WORDS - config.VALID_MIN_WORDS
    return (word_count - config.VALID_MIN_WORDS) / span if span > 0 else 1.0


def confidence(
    model_score: float,
    style_score: float,
    combined_score: float,
    word_count=None,
    style_available: bool = True,
) -> float:
    """
    How sure we are that the label is right: 0.0 = no idea, 1.0 = sure. ← Milestone 4

    NOT a direction. The direction is `guess` and the score; this says how much weight
    that call carries, and it behaves the same whichever way the call went. A 0.9 on a
    human verdict means the same size of claim as a 0.9 on an AI verdict.

    Three things go into it:

      - **Distance from the verdict bar, in units of our own noise.** A 0.56 next to a
        bar of 0.55 is a coin flip that happened to land; a 0.05 is a verdict. The unit
        is SIGMA_BASE / sqrt(n_signals) — the standard error — so a ruling resting on
        one signal is automatically less certain than one corroborated by two, with no
        special case in the code. erf(z/sqrt(2)) turns that distance into the
        probability a Gaussian stays within z standard deviations of its mean: how far
        this text sits from the overlap you would expect between the two populations.

      - **How much text there was.** `length_validity` can take certainty to zero, and
        does for anything under VALID_MIN_WORDS.

      - **Whether style could read the text at all**, which arrives as n_signals=1 and
        shows up as the wider noise above.

    Corroboration is NOT multiplied in a second time. Disagreement has already collapsed
    the score toward 0.500 inside `combine_signals`, which shrinks the distance from the
    bar and so shrinks the certainty. Multiplying by agreement as well would charge the
    same disagreement twice and leave the number impossible to reason about.

    Capped at CONF_MAX, because an automated accusation claiming certainty 1.0 is a
    statement no evidence this thin supports — and the cap keeps any log-odds taken
    downstream finite.

    `combined_score` should be the value `combine_signals` returned for these same two
    signals: it is the score being certified, not something to re-derive here.
    """
    breakdown = score_breakdown(model_score, style_score, style_available)
    bar = config.COMBINE_CROSSOVER + config.GUESS_BIAS

    noise = config.SIGMA_BASE / math.sqrt(breakdown["n_signals"])
    if noise <= 0:
        return 0.0

    z = abs(combined_score - bar) / noise
    certainty = math.erf(z / math.sqrt(2.0))
    certainty *= length_validity(word_count)
    return max(0.0, min(config.CONF_MAX, certainty))


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    # TODO: replace this — thresholds are in config.py
    if score >= config.AI_THRESHOLD:
        return "ai", "This appears to have been written by AI."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "This appears to have been written by a human."
    return (
        "unsure",
        "There is not enough evidence to be certain if this is human or AI generated.",
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
