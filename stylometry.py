"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

**The convention in this file, which matters more than any single number.**
Each of the three measures returns a RAW value in its own units, and for all
three the HIGH end of the raw value means "more human" — that includes
`type_token_ratio`, where higher means more varied vocabulary. `style_signal`
is the only function that changes direction: it inverts all three onto 0–1 and
weights them, returning the same orientation as `detector.model_signal`
(0.0 = human, 1.0 = AI). Keeping the raw measures raw means every direction
decision sits in one readable block instead of being scattered — and a sign
error in one of three metrics is otherwise exactly the kind of bug that stays
invisible all the way up to the label.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import math
import re
import statistics

import config


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── Scaling helper shared by the three measures ──────────────────────────────

def _ai_score(raw: float, human_anchor: float, ai_anchor: float) -> float:
    """
    Map one raw measure onto 0–1 AI-likeness using two anchors.

        (raw - human_anchor) / (ai_anchor - human_anchor)

    clamped to [0, 1]. The anchors are raw values, so they keep the units of
    whatever they're measuring — a CV, a ratio, a rate per 100 words — which is
    what lets three measures on three different scales be added together.

    **The direction comes from the anchor order, not from the caller.** Pass the
    human anchor first and a raw value at that end scores 0.0 (human), a raw
    value at the AI anchor scores 1.0, and anything past either end clamps. A
    measure whose raw values climb toward "human" — all three here — inverts for
    free, and no call site needs a hand-written `1 - x` that a future reader has
    to double-check. Changing your mind about a measure's direction is then a
    config edit, not a code edit.

    Degenerate input returns 0.5 (a coin flip): a non-finite raw value means
    there was nothing to measure, and equal anchors mean a config mistake. Both
    are crash guards rather than measurements, and deliberately not the
    short-text abstention policy — that's a Unit 8 improvement, see
    `_segment_lengths`.
    """
    if not math.isfinite(raw):
        return 0.5
    span = ai_anchor - human_anchor
    if span == 0:
        return 0.5
    return round(min(max((raw - human_anchor) / span, 0.0), 1.0), 4)


def _segment_lengths(text: str) -> list[int]:
    """
    Lengths in words of the text's big units, falling back to clauses.

    The given splitter only cuts where `.!?` is followed by whitespace, so a
    one-sentence submission — or a text with sentences jammed together,
    `"...end.Next sentence..."` — leaves nothing to take a spread of. Falling
    back to clause lengths (split on `, . ! ? ; :`) means a short or badly
    delimited text still gets a real measurement rather than a crash or a free
    pass.

    Returns word counts, one per unit. A list shorter than two entries means the
    text is one unbroken run and no spread can be computed at all.
    """
    lengths = [n for n in (len(words(s)) for s in sentences(text)) if n > 0]
    if len(lengths) >= 2:
        return lengths

    clause_lengths = [
        n for n in (len(words(c)) for c in re.split(r"[,.!?;:]+", text)) if n > 0
    ]
    # UNIT 8: if there is still only one unit, a single unbroken run reaches
    # style_signal as a spread of zero, which reads as maximally metronomic.
    # That harsh default is what an abstention rule ("too little shape to
    # measure — abstain") would replace.
    return clause_lengths if len(clause_lengths) >= 2 else lengths


# ── The three measures — raw values, high end = more human ───────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. Raw, not scored.

    Returns:
        The coefficient of variation of sentence lengths — standard deviation
        over mean. Dimensionless, and dividing by the mean is what makes a 60-word
        text and a 300-word text comparable at all.

        Scale: about 0.05 (every sentence the same length) up to about 0.8 (a
        three-word sentence next to a forty-word one).

        Direction: **higher means more varied, therefore more HUMAN.**
        `style_signal` inverts this one.

    A one-sentence text has no spread and `statistics.stdev` raises below two
    values, so the units come from `_segment_lengths`, which falls back to
    clauses. If there is genuinely only one unit, this returns 0.0 — steady,
    and read as AI-ward downstream.
    """
    lengths = _segment_lengths(text)
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean <= 0:
        return 0.0
    return statistics.stdev(lengths) / mean



def type_token_ratio(text: str) -> float:
    """
    Unique words over total words — the raw ratio, exactly as this stub asks.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary,
        therefore more HUMAN.** `style_signal` inverts it:
        `adj_ttr = 1 - ttr`, expressed through the anchors in config.py.

        Empty text returns 0.0 — no vocabulary at all.

    Worth knowing before anyone leans on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths are not
    comparable on it, and where test inputs vary in length the length difference
    alone can look like a signal. That is why `style_signal` scores the
    length-robust version in `_lexicon_measure` rather than this global ratio,
    and why `python stylometry.py` prints both side by side.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def _windowed_ttr(text: str, window: int) -> float:
    """
    Moving-average type-token ratio: the mean TTR over consecutive windows of
    `window` words.

    Holding the window fixed is what makes the measure length-robust — every
    window is judged on the same number of words, so a 60-word text and a
    300-word text are measured with the same yardstick. Text shorter than one
    window falls back to its own global TTR.

    Small windows notice repetition sooner but jitter more on short texts; that
    trade-off is the config lever, not a constant to get right now.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if window <= 0 or len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    spans = [
        len(set(tokens[i:i + window])) / window
        for i in range(len(tokens) - window + 1)
    ]
    return sum(spans) / len(spans)


def _lexicon_measure(text: str) -> float:
    """
    The vocabulary measure `style_signal` actually scores, raw and human-ward
    like its siblings (high = varied = human).

    Windowed when config.STYLE_LEXICON_WINDOW > 0, which is the default; set it
    to 0 to score the global type-token ratio instead and compare the two on the
    same texts. Same units as `type_token_ratio`, so `LEXICON_HUMAN` and
    `LEXICON_AI` are anchors for either.
    """
    window = config.STYLE_LEXICON_WINDOW
    if window <= 0:
        return type_token_ratio(text)
    return _windowed_ttr(text, window)



def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. Raw, not scored.

    Returns:
        A rate: comma-class marks per 100 words, so roughly 0 to 12 for real
        prose. **Higher means more punctuated; on the assumption recorded in
        config.py that means more HUMAN**, and `style_signal` inverts it.

    Which marks count is a real choice and it lives in config.STYLE_PUNCT_CHARS:
    `, ; : ( ) — – “ ” …`. Three things went into that set.

      - Comma-class marks carry the weight because a set of only `; : —` sits at
        zero for most ordinary prose, which pins the metric at one end for every
        text — a measure that doesn't discriminate is worse than no measure, and
        exactly the failure Milestone 4 asks you to catch.
      - Em dashes, parentheses and quotes are in because they vary more between
        writers than full stops do.
      - Full stops and question marks are out. They mostly count sentences, which
        sentence_length_spread already measures; double-counting them would let
        one property vote twice.
      - Apostrophes are out. `don't` and `it's` would score contractions as
        punctuation and hand informal writing a free human reading.

    Empty text returns 0.0.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    marks = sum(text.count(char) for char in config.STYLE_PUNCT_CHARS)
    return 100.0 * marks / len(tokens)



# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

        raw measures (high end = human)  ->  invert + anchor-scale to 0–1  ->  weighted mean

    Same direction as `detector.model_signal`, so `scoring.combine_signals` can
    treat the two signals the same way — one signal running backwards makes
    everything above it wrong in a way that is very hard to see.

    Every direction decision lives in the `adj_*` block below, on three
    consecutive lines that can be read against each other. The raw measures keep
    their own units and their own human-ward tilt; nothing outside this function
    has to know which of them needed flipping.

    The anchors and weights are uncalibrated placeholders — there is no baseline
    corpus yet. `grep -n PLACEHOLDER config.py` lists every number to revisit, and
    the comment above them records the rule used to place them (human median for
    the human anchor, human 5th percentile for the AI anchor) along with the two
    things that follow from it: this function clamps to exact 0.0 and 1.0, and the
    lexicon metric is the weakest of the three.

    Known limitation, stated plainly: the given `words()` tokenizer matches
    `[a-z0-9']+` only. Accented Latin text fragments ("café" becomes "caf"), and a
    text in a non-Latin script yields no tokens at all, so its vocabulary and
    punctuation measures fall to zero and this function returns 1.0 — a hard AI
    verdict produced by the tokenizer, not by the writing. Anything beyond English
    needs the tokenizer widened, which is a separate decision, not a tweak here.
    """
    # ── raw, all climbing toward "human" ───────────────────────────────────
    raw_spread = sentence_length_spread(text)   # CV of sentence/clause lengths
    raw_ttr = _lexicon_measure(text)            # windowed unique-over-total words
    raw_punct = punctuation_density(text)       # comma-class marks per 100 words

    # ── align direction: human-ward raw -> AI-ward 0–1 ─────────────────────
    # All three raw measures climb toward human, so all three invert. The
    # inversion comes from the anchor order — human anchor first — which is why
    # no line here needs a hand-written `1 - x`. For the literal form on the
    # lexicon, set LEXICON_HUMAN = 1.0 and LEXICON_AI = 0.0 in config.py, and
    # this line becomes adj_ttr = 1 - raw_ttr; see the note there about why the
    # tighter default anchors are preferred.
    adj_spread = _ai_score(raw_spread, config.SPREAD_HUMAN, config.SPREAD_AI)
    adj_ttr = _ai_score(raw_ttr, config.LEXICON_HUMAN, config.LEXICON_AI)
    adj_punct = _ai_score(raw_punct, config.PUNCT_HUMAN, config.PUNCT_AI)

    # ── weight ───────────────────────────────────────────────────────────────
    # Divided by the sum of the weights so they read as relative influence:
    # zeroing one retires that metric without shifting the other two's scales.
    weights = (
        config.STYLE_WEIGHT_SPREAD,
        config.STYLE_WEIGHT_LEXICON,
        config.STYLE_WEIGHT_PUNCT,
    )
    total = sum(weights)
    if total <= 0:
        return 0.5    # every weight zeroed — a config mistake, not a measurement

    score = sum(w * v for w, v in zip(weights, (adj_spread, adj_ttr, adj_punct))) / total
    return round(min(max(score, 0.0), 1.0), 4)



if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )
    if not sys.argv[1:]:
        print("(no text given — scoring a sample)\n")

    raw_spread = sentence_length_spread(text)
    raw_ttr = type_token_ratio(text)
    raw_lex = _lexicon_measure(text)
    raw_punct = punctuation_density(text)

    window = config.STYLE_LEXICON_WINDOW
    lex_label = f"lexicon, MTTR/{window}w" if window > 0 else "lexicon, global TTR"

    print(
        f"{len(sentences(text))} sentences, "
        f"{len(words(text))} words, "
        f"{len(_segment_lengths(text))} units for spread\n"
    )
    print(f"{'raw measure':<24}{'raw':>9}{'  adjusted (1.0 = AI)':>22}")
    print(f"{'sentence_length_spread':<24}{raw_spread:>9.3f}"
          f"{_ai_score(raw_spread, config.SPREAD_HUMAN, config.SPREAD_AI):>22.4f}")
    print(f"{'type_token_ratio':<24}{raw_ttr:>9.3f}"
          f"{_ai_score(raw_ttr, config.LEXICON_HUMAN, config.LEXICON_AI):>22.4f}")
    print(f"{lex_label:<24}{raw_lex:>9.3f}"
          f"{_ai_score(raw_lex, config.LEXICON_HUMAN, config.LEXICON_AI):>22.4f}")
    print(f"{'punctuation_density':<24}{raw_punct:>9.3f}"
          f"{_ai_score(raw_punct, config.PUNCT_HUMAN, config.PUNCT_AI):>22.4f}")
    print(f"{'style_signal':<24}{'':>9}{style_signal(text):>22.4f}")
    print(
        "\nRaw values are human-ward (high = human); adjusted and style_signal "
        "are AI-ward (high = AI).\n"
        "Anchors are uncalibrated placeholders — grep -n PLACEHOLDER config.py"
    )
