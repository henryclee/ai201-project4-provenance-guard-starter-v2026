#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.


class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return (
            creator
            if isinstance(creator, str) and creator.strip()
            else get_remote_address()
        )

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify(
            {
                "error": "rate_limited",
                "message": "Too many submissions. Try again shortly.",
                "limit": str(exc.description),
            }
        ), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────


@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify(
        {
            "ok": True,
            "you_sent": payload.get("message"),
            "service": "provenance-guard",
        }
    )


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify(
        {
            "ok": True,
            "detector_model": config.DETECTOR_MODEL,
            "detector_loaded": loaded,
            "rate_limiting": config.RATE_LIMITING_ENABLED,
            "log_entries": len(audit.read_entries()),
        }
    )


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────


def _reject(creator_id: str, reason: str, message: str, **extra):
    """
    Refuse a request — and make sure the refusal exists afterwards.

    The logging lives here rather than at each call site so that no branch can forget it.
    A rejection that leaves no trace is indistinguishable from a quiet afternoon, and
    unit 8's entire argument about spotting abuse depends on those two being tellable
    apart. `status: "rejected"` also keeps a refusal from being mistaken downstream for
    a decision about a writer, which it is not: nothing was measured.
    """
    audit.log_rejection(creator_id=creator_id, reason=reason, **extra)
    return jsonify({"error": reason, "message": message, "status": "rejected"}), 400


@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← Milestones 3 and 4 are built. Milestone 5 (the label) is not.

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Returns JSON:
        {"content_id": "...", "guess": "ai"|"human", "confidence": 0.0-1.0,
         "label": "placeholder", "model_score": 0.0, "style_score": 0.0|null,
         "combined_score": 0.0, "word_count": 0, "style_tokens": 0,
         "style_available": true, "status": "decided"}

    `label` is still "placeholder" deliberately — the label PROSE is Milestone 5's work,
    so anything that checks label text fails here while the numbers, the guess and the
    certainty are all real.

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score` straight off
    this response into their reports. `style_score` comes back `null` when the style
    signal could not measure the text at all — see `style_available`. An unmeasured
    signal written as 0.0 would be a small lie that flatters the writer, and one written
    as 1.0 would convict someone on a number that was never taken.

    The failure contract, decided now because unit 8's attack set otherwise decides it
    for you:

        400  missing / non-string / whitespace-only text, or fewer than
             MIN_SUBMIT_WORDS words AND MIN_SUBMIT_CHARS characters — nothing to measure
        503  the model isn't loaded — the text is not in question, retry later
        200  a verdict, with certainty possibly 0.0 for text too short to mean much

    Every branch leaves a log line. A rejection that leaves no trace looks exactly like a
    quiet afternoon, and an attack you cannot see is an attack you cannot stop.
    """
    # `silent=True` so a body that isn't JSON at all lands in our validation instead
    # of Flask raising before this function runs. Note it is `or None`, not `or {}`:
    # a bare JSON string or list is valid JSON and must be distinguishable from an
    # empty object, because "you sent me the wrong shape" and "you sent me nothing"
    # are different messages to a caller trying to integrate against this.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return _reject(
            "unknown",
            "invalid_payload",
            'Expected a JSON object like {"text": "...", "creator_id": "..."}.',
        )

    creator_id = payload.get("creator_id")
    if not isinstance(creator_id, str) or not creator_id.strip():
        creator_id = "unknown"

    text = payload.get("text")
    if text is None:
        return _reject(creator_id, "missing_text", "No 'text' field in the request.")
    if not isinstance(text, str):
        return _reject(
            creator_id,
            "invalid_text",
            "'text' must be a string of written prose.",
            received=type(text).__name__,
        )
    if not text.strip():
        return _reject(creator_id, "empty_text", "'text' is empty or whitespace only.")

    # Two different counts, because they answer two different questions.
    #
    #   word_count  — whitespace words, the plain "is there enough text here" measure
    #                 that gates the request and judges whether there is enough of a
    #                 sample to be certain about anything.
    #   style_tokens — what THIS codebase's tokenizer can actually see. That is what the
    #                 style signal measured, so it is what decides whether style is
    #                 available at all.
    #
    # They disagree whenever text is dense or oddly spaced, which is why the request gate
    # requires BOTH floors to fail before refusing anything.
    word_count = len(text.split())
    char_count = len(text.strip())
    if word_count < config.MIN_SUBMIT_WORDS and char_count < config.MIN_SUBMIT_CHARS:
        return _reject(
            creator_id,
            "text_too_short",
            (
                f"Need at least {config.MIN_SUBMIT_WORDS} words "
                f"(or {config.MIN_SUBMIT_CHARS} characters) to score; "
                f"got {word_count} words / {char_count} characters."
            ),
            word_count=word_count,
            char_count=char_count,
        )

    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable as exc:
        # The model is missing or failed to download. Nothing about THIS text is in
        # question, so it must not arrive as a 500 that reads like the caller's input
        # was at fault, and it must not be logged as a decision about a writer.
        audit.log_rejection(
            creator_id=creator_id,
            reason="detector_unavailable",
            detail=str(exc),
            word_count=word_count,
        )
        return jsonify(
            {
                "error": "detector_unavailable",
                "message": (
                    "The text model isn't loaded, so nothing can be scored right now. "
                    "Check /health and try again once detector_report is true."
                ),
                "status": "unavailable",
            }
        ), 503

    # Absent evidence, not weak evidence. Below STYLE_MIN_TOKENS the style metrics are
    # measuring whichever few words happened to be there rather than how the text was
    # written, so they are dropped from the combination and the verdict rests on the
    # model alone, at reduced certainty. See STYLE_MIN_TOKENS in config.py.
    style_tokens = len(stylometry.words(text))
    style_available = style_tokens >= config.STYLE_MIN_TOKENS
    style_score = None
    if style_available:
        try:
            style_score = stylometry.style_signal(text)
        except Exception as exc:  # a broken signal must never take the route down
            style_available = False
            audit.log_rejection(
                creator_id=creator_id,
                reason="style_signal_failed",
                detail=str(exc),
                word_count=word_count,
            )

    # Minted only once there IS a decision to identify. A refused request has no
    # content, so giving it a content_id would put an identifier in the log for nothing,
    # and /appeal later would have something to point at that was never judged.
    content_id = str(uuid.uuid4())

    breakdown = scoring.score_breakdown(
        model_score, style_score or 0.0, style_available
    )
    combined_score = breakdown["combined_score"]
    confidence = scoring.confidence(
        model_score,
        style_score or 0.0,
        combined_score,
        word_count,
        style_available,
    )

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=breakdown["guess"],
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label="placeholder",
        status="decided",
        confidence=confidence,
        word_count=word_count,
        style_tokens=style_tokens,
        style_available=style_available,
        # The intermediates, so a verdict can be reconstructed months later without
        # re-running a model that may by then have been replaced.
        evidence_model=round(breakdown["evidence_model"], 4),
        evidence_style=(
            None
            if breakdown["evidence_style"] is None
            else round(breakdown["evidence_style"], 4)
        ),
        disagreement=round(breakdown["disagreement"], 4),
        agreement=round(breakdown["agreement"], 4),
    )

    response = {
        "content_id": content_id,
        "guess": breakdown["guess"],
        "confidence": confidence,
        "label": "placeholder",
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
        "word_count": word_count,
        "style_tokens": style_tokens,
        "style_available": style_available,
        "status": "decided",
    }

    return jsonify(response), 200


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = request.get_json(silent=True) or {}

    content_id = payload.get("content_id", "")
    reasoning = payload.get("reasoning", "")

    if content_id == "" or reasoning == "":
        return _reject(
            "unknown",
            "invalid_appeal",
            'Expected a JSON object like {"content_id": "...", "reasoning": "..."}.',
        ), 400

    entries = audit.entries_for(content_id)  # check it exists, or return 400
    creator_id = entries[0]["creator_id"] if entries else "unknown"

    if not entries:
        return jsonify({"error": "content_id not found"}), 400

    audit.log_appeal(content_id=content_id, creator_id=creator_id, reasoning=reasoning)

    return jsonify(
        {
            "message": f"content_id {content_id} has been marked under review. Thank you for your appeal.",
        }
    ), 200


# ── Already works ─────────────────────────────────────────────────────────────


@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(
        f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}"
    )
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f"  curl -X POST http://{config.HOST}:{config.PORT}/ping \\")
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"message": "hello"}\'')
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
