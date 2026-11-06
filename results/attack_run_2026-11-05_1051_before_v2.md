# Attack run — before_v2

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 10:51
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `0dc759ad-19bd-4a44-a60c-8e6204f84a29` | unsure | 0.186 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `fe9228c8-947c-4f2c-861d-8ef9b980f33c` | unsure | 0.583 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `fa73e6d8-b4c0-4323-8bc8-d7181c7b6d1a` | unsure | 0.135 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `1d3d8a9e-0e96-4aac-b374-8a8ffbe15968` | unsure | 0.249 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `fdb009f5-39c5-4e45-a79e-aaeb59158c1d` | human | 0.950 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `9fe0197b-8b3d-4cf4-846a-c71ba1e0d70b` | human | 0.659 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d8390999-3be1-46bc-bf1d-ab8d0636d43a` | unsure | 0.415 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `37f22d32-c458-4072-bf0e-04b2e81b0528` | unsure | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `4d6fda01-0dda-45fd-a7e7-faf2fbb05e76` | unsure | 0.203 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c244c530-7039-434b-b510-24272369b5dc` | unsure | 0.003 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `247703f7-9603-46e6-8123-2a037ce8b4c6` | unsure | 0.145 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `71907935-a857-467a-8223-242771df67e3` | ai | 0.786 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `dd72053a-c43d-446f-941c-a32f22fe05ff` | ai | 0.830 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `f7c69dba-4bb2-4c6c-919f-37b1dd937289` | ai | 0.657 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d9bb7f9e-2371-482f-9863-0ffed58e9986` | unsure | 0.361 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `49c0650d-5bf8-41c6-ab24-1ec0b06e863f` | unsure | 0.229 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `bede700f-128a-4a89-9dcb-85e373181595` | ai | 0.755 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `48c8effb-2ed7-4361-beb4-2659eb858b37` | unsure | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `26826e44-81fa-46f6-a03c-ee81c72a6336` | human | 0.562 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `aa5398e5-7f4b-48fb-8ab6-0d38e5ec1a86` | human | 0.514 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8ba707a5-f172-4ad8-a891-884ae1a3f04f` | unsure | 0.250 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `a20f8f86-aa6e-493f-acc3-7a8808d1d111` | human | 0.552 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `6063fd65-b2be-453c-90bc-8ed9a539040f` | unsure | 0.080 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `d28c46b0-7c82-4d69-9fef-2c5892311d78` | unsure | 0.090 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `f8106fa4-2cfe-4496-8036-2318f6b0c12b` | human | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `805ef11a-028b-440f-b28e-141548e714f5` | human | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `58da4a49-6efd-4468-80d7-a786b3f23165` | ai | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `8e763fd5-58b5-41cd-8f30-a03fa8e2acdd` | ai | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `4c37833c-ecd1-45c2-a75d-16f54c64405f` | ai | 0.000 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `b5e55787-5ed3-4f64-8017-256891f6bf2a` | unsure | 0.218 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `3c76fac4-fe52-49cc-8bfb-45f592f3625c` | unsure | 0.000 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `ae17064f-d387-4661-93c4-74d1072f8a8f` | human | 0.000 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `664994e6-1396-4513-9ae9-c3c8d00b28e2` | unsure | 0.000 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ddf9b484-cea6-476d-b78b-1d6ba6c92eae` | unsure | 0.000 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aba91214-2cfd-4c85-92d7-41e11ea65ce3` | unsure | 0.000 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `03c48985-4ccd-4f29-9850-ae05e1fe270e` | unsure | 0.000 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3dc1931d-b9df-4006-a9c8-5a21f0cbd187` | unsure | 0.000 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `61cfc9a8-a569-4937-a844-742aa0d40bcf` | unsure | 0.000 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ff9f6432-cf7d-4546-b1ff-b7927aec120a` | unsure | 0.000 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e52dd8ef-b943-4536-91f6-681d82e986ad` | unsure | 0.000 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e89156c7-120a-4f33-b1c6-bcc586f5221a` | unsure | 0.000 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5947888d-4759-45f8-99bf-b969b7716ebb` | unsure | 0.000 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "0dc759ad-19bd-4a44-a60c-8e6204f84a29",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.18633628423320822,
  "model_score": 0.1635,
  "style_score": 0.5985,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "fe9228c8-947c-4f2c-861d-8ef9b980f33c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5825291397594665,
  "model_score": 0.5943,
  "style_score": 0.1602,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "fa73e6d8-b4c0-4323-8bc8-d7181c7b6d1a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.1347473737778723,
  "model_score": 0.6662,
  "style_score": 0.266,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "1d3d8a9e-0e96-4aac-b374-8a8ffbe15968",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.24902114698305855,
  "model_score": 0.6114,
  "style_score": 0.6006,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "fdb009f5-39c5-4e45-a79e-aaeb59158c1d",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.95,
  "model_score": 0.3212,
  "style_score": 0.0201,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "9fe0197b-8b3d-4cf4-846a-c71ba1e0d70b",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.6593673127441511,
  "model_score": 0.5727,
  "style_score": 0.162,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "d8390999-3be1-46bc-bf1d-ab8d0636d43a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.41523348405187244,
  "model_score": 0.5862,
  "style_score": 0.0,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "37f22d32-c458-4072-bf0e-04b2e81b0528",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.2452,
  "style_score": 0.5249,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "4d6fda01-0dda-45fd-a7e7-faf2fbb05e76",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.2026822099817128,
  "model_score": 0.7042,
  "style_score": 0.2001,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c244c530-7039-434b-b510-24272369b5dc",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.0026539449181178123,
  "model_score": 0.9792,
  "style_score": 0.3899,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "247703f7-9603-46e6-8123-2a037ce8b4c6",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1451410813149621,
  "model_score": 0.6175,
  "style_score": 0.3721,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "71907935-a857-467a-8223-242771df67e3",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7855077897505828,
  "model_score": 0.7387,
  "style_score": 0.623,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "dd72053a-c43d-446f-941c-a32f22fe05ff",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.829683814940543,
  "model_score": 0.8051,
  "style_score": 0.4796,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "f7c69dba-4bb2-4c6c-919f-37b1dd937289",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6572956976346511,
  "model_score": 0.8329,
  "style_score": 0.423,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "d9bb7f9e-2371-482f-9863-0ffed58e9986",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.3609512297621331,
  "model_score": 0.8005,
  "style_score": 0.8558,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "49c0650d-5bf8-41c6-ab24-1ec0b06e863f",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.22948986743590977,
  "model_score": 0.8814,
  "style_score": 0.3522,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "bede700f-128a-4a89-9dcb-85e373181595",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7548537743970766,
  "model_score": 0.8816,
  "style_score": 0.4744,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "48c8effb-2ed7-4361-beb4-2659eb858b37",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.3223,
  "style_score": 0.3423,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "26826e44-81fa-46f6-a03c-ee81c72a6336",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.5619956546160001,
  "model_score": 0.4625,
  "style_score": 0.2,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "aa5398e5-7f4b-48fb-8ab6-0d38e5ec1a86",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5139718429458559,
  "model_score": 0.2044,
  "style_score": 0.1028,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "8ba707a5-f172-4ad8-a891-884ae1a3f04f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.2502410027038921,
  "model_score": 0.5943,
  "style_score": 0.304,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "a20f8f86-aa6e-493f-acc3-7a8808d1d111",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.5518258543194977,
  "model_score": 0.4998,
  "style_score": 0.234,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "6063fd65-b2be-453c-90bc-8ed9a539040f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.08007897516399883,
  "model_score": 0.6401,
  "style_score": 0.0956,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "d28c46b0-7c82-4d69-9fef-2c5892311d78",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.09048924178302728,
  "model_score": 0.5583,
  "style_score": 0.3905,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "f8106fa4-2cfe-4496-8036-2318f6b0c12b",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": null,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "805ef11a-028b-440f-b28e-141548e714f5",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0112,
  "style_score": null,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "58da4a49-6efd-4468-80d7-a786b3f23165",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9976,
  "style_score": null,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "8e763fd5-58b5-41cd-8f30-a03fa8e2acdd",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9969,
  "style_score": null,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "4c37833c-ecd1-45c2-a75d-16f54c64405f",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9064,
  "style_score": null,
  "label": "This appears to have been written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "b5e55787-5ed3-4f64-8017-256891f6bf2a",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.2181780507676133,
  "model_score": 0.9876,
  "style_score": 0.4284,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "3c76fac4-fe52-49cc-8bfb-45f592f3625c",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.2395,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "ae17064f-d387-4661-93c4-74d1072f8a8f",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0492,
  "style_score": null,
  "label": "This appears to have been written by a human.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "664994e6-1396-4513-9ae9-c3c8d00b28e2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "ddf9b484-cea6-476d-b78b-1d6ba6c92eae",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "aba91214-2cfd-4c85-92d7-41e11ea65ce3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "03c48985-4ccd-4f29-9850-ae05e1fe270e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "3dc1931d-b9df-4006-a9c8-5a21f0cbd187",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "61cfc9a8-a569-4937-a844-742aa0d40bcf",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "ff9f6432-cf7d-4546-b1ff-b7927aec120a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "e52dd8ef-b943-4536-91f6-681d82e986ad",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "e89156c7-120a-4f33-b1c6-bcc586f5221a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "5947888d-4759-45f8-99bf-b969b7716ebb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "There is not enough evidence to be certain if this is human or AI generated.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
