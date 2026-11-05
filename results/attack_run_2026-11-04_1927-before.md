# Attack run

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 19:27
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `2e423a05-0e16-48df-8873-ef471cdec0d0` | human | 0.186 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `7d8b4d77-20ba-4098-9d76-c9820c91854e` | human | 0.583 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `efb0f7ec-ffcd-42a6-adce-77cafdcc3f26` | human | 0.135 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `b5982954-50db-4c9e-84e1-4bc4e873858d` | ai | 0.249 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `8501fa41-2646-4c8b-a36a-16577b80147d` | human | 0.950 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `abad1a28-6ead-43d7-90e8-09c66eeeb8fb` | human | 0.659 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `5c37ca71-4fef-42b9-b9e1-f5a62c9ebf68` | human | 0.415 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `1ffd75d1-fa48-49d7-a30b-f067c2c28ac6` | human | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d057106b-e87f-4404-8439-191dc1e75d8c` | human | 0.203 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b0fc3295-77fc-40f2-8d5d-998d5f8046ea` | human | 0.003 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8401563f-b8f2-4278-be3b-03ddd908246e` | ai | 0.145 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `67dcbad3-ab42-4414-85fe-6240270f08dc` | ai | 0.786 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `83c891fc-3624-44a3-91c8-d3061b36ab79` | ai | 0.830 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d3edf278-af1f-43bc-98b5-223b53a44fcc` | ai | 0.657 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `5891f88c-13a6-4a7a-bbc6-cb1fc6a4f547` | ai | 0.361 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `96ad3b28-b4e1-4b74-84cf-ed5deae29b84` | ai | 0.229 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `518c5dfa-7cda-4d9f-b028-d3bbef57168a` | ai | 0.755 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `07c2393c-fd79-41c0-820e-18270005f962` | human | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4a1cf0ce-b2e7-49b7-aa1c-1a8be583edfb` | human | 0.562 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `74385f6f-1b0f-4f71-90e9-c5c17503cecc` | human | 0.514 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `40c1e9b6-694a-4b01-bdbb-739bac266f23` | human | 0.250 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `681cd784-91cc-4863-bfe0-f28b40909ffd` | human | 0.552 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `7b31409a-6c91-42ae-aec8-6f0f45b31664` | human | 0.080 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `17336008-8035-4eda-a56d-06dd397b711e` | human | 0.090 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `6dc95295-7eb1-4231-ac03-c33f634db522` | human | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `d467e4e0-802b-4bfe-acb3-e4df26cb6f3e` | human | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `848701ff-722f-418e-bfc3-5e0ed4417589` | ai | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `cf6036ff-5033-4c82-8424-13c42057039a` | ai | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `ab71c9b9-fc13-4868-aca6-b5595cbdf8eb` | ai | 0.000 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `28c15540-ed8f-474f-b9a7-131d94d3cc39` | ai | 0.218 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `4167788b-dcb8-4c6a-99b3-e40c61866547` | human | 0.000 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `4a3cdf6f-40e6-4f01-a1b8-bfab8fe93569` | human | 0.000 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f189e0db-b021-49f2-958d-8507db381829` | human | 0.000 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `de52ed23-8430-4394-9aa3-8e37f16f9ab0` | human | 0.000 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dbcb62cf-e4c6-445d-8491-789bba7296f9` | human | 0.000 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6d9cc497-f613-43ac-830d-6d62c1de7803` | human | 0.000 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e6a520b2-1ed3-451b-9215-7d26ec3f02af` | human | 0.000 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `13f78700-378a-48ab-a492-84ebf96604e6` | human | 0.000 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4c15ca5b-e6d4-4c84-8c9d-b48f172bb15d` | human | 0.000 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `20c55c93-3d31-49fe-b76a-4492c1fb61c1` | human | 0.000 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ebb1a6e7-553d-43d0-b3ff-6d822b19c7db` | human | 0.000 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9e1ae35f-61e4-488c-9eaf-f70a1d0c739b` | human | 0.000 |  |
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
  "content_id": "2e423a05-0e16-48df-8873-ef471cdec0d0",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.18633628423320822,
  "model_score": 0.1635,
  "style_score": 0.5985,
  "label": "placeholder",
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
  "content_id": "7d8b4d77-20ba-4098-9d76-c9820c91854e",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.5825291397594665,
  "model_score": 0.5943,
  "style_score": 0.1602,
  "label": "placeholder",
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
  "content_id": "efb0f7ec-ffcd-42a6-adce-77cafdcc3f26",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.1347473737778723,
  "model_score": 0.6662,
  "style_score": 0.266,
  "label": "placeholder",
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
  "content_id": "b5982954-50db-4c9e-84e1-4bc4e873858d",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.24902114698305855,
  "model_score": 0.6114,
  "style_score": 0.6006,
  "label": "placeholder",
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
  "content_id": "8501fa41-2646-4c8b-a36a-16577b80147d",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.95,
  "model_score": 0.3212,
  "style_score": 0.0201,
  "label": "placeholder",
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
  "content_id": "abad1a28-6ead-43d7-90e8-09c66eeeb8fb",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.6593673127441511,
  "model_score": 0.5727,
  "style_score": 0.162,
  "label": "placeholder",
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
  "content_id": "5c37ca71-4fef-42b9-b9e1-f5a62c9ebf68",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.41523348405187244,
  "model_score": 0.5862,
  "style_score": 0.0,
  "label": "placeholder",
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
  "content_id": "1ffd75d1-fa48-49d7-a30b-f067c2c28ac6",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.2452,
  "style_score": 0.5249,
  "label": "placeholder",
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
  "content_id": "d057106b-e87f-4404-8439-191dc1e75d8c",
  "creator_id": "attacker_EV09",
  "guess": "human",
  "confidence": 0.2026822099817128,
  "model_score": 0.7042,
  "style_score": 0.2001,
  "label": "placeholder",
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
  "content_id": "b0fc3295-77fc-40f2-8d5d-998d5f8046ea",
  "creator_id": "attacker_EV10",
  "guess": "human",
  "confidence": 0.0026539449181178123,
  "model_score": 0.9792,
  "style_score": 0.3899,
  "label": "placeholder",
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
  "content_id": "8401563f-b8f2-4278-be3b-03ddd908246e",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.1451410813149621,
  "model_score": 0.6175,
  "style_score": 0.3721,
  "label": "placeholder",
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
  "content_id": "67dcbad3-ab42-4414-85fe-6240270f08dc",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7855077897505828,
  "model_score": 0.7387,
  "style_score": 0.623,
  "label": "placeholder",
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
  "content_id": "83c891fc-3624-44a3-91c8-d3061b36ab79",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.829683814940543,
  "model_score": 0.8051,
  "style_score": 0.4796,
  "label": "placeholder",
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
  "content_id": "d3edf278-af1f-43bc-98b5-223b53a44fcc",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6572956976346511,
  "model_score": 0.8329,
  "style_score": 0.423,
  "label": "placeholder",
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
  "content_id": "5891f88c-13a6-4a7a-bbc6-cb1fc6a4f547",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.3609512297621331,
  "model_score": 0.8005,
  "style_score": 0.8558,
  "label": "placeholder",
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
  "content_id": "96ad3b28-b4e1-4b74-84cf-ed5deae29b84",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.22948986743590977,
  "model_score": 0.8814,
  "style_score": 0.3522,
  "label": "placeholder",
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
  "content_id": "518c5dfa-7cda-4d9f-b028-d3bbef57168a",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7548537743970766,
  "model_score": 0.8816,
  "style_score": 0.4744,
  "label": "placeholder",
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
  "content_id": "07c2393c-fd79-41c0-820e-18270005f962",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.3223,
  "style_score": 0.3423,
  "label": "placeholder",
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
  "content_id": "4a1cf0ce-b2e7-49b7-aa1c-1a8be583edfb",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.5619956546160001,
  "model_score": 0.4625,
  "style_score": 0.2,
  "label": "placeholder",
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
  "content_id": "74385f6f-1b0f-4f71-90e9-c5c17503cecc",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5139718429458559,
  "model_score": 0.2044,
  "style_score": 0.1028,
  "label": "placeholder",
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
  "content_id": "40c1e9b6-694a-4b01-bdbb-739bac266f23",
  "creator_id": "attacker_PI03",
  "guess": "human",
  "confidence": 0.2502410027038921,
  "model_score": 0.5943,
  "style_score": 0.304,
  "label": "placeholder",
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
  "content_id": "681cd784-91cc-4863-bfe0-f28b40909ffd",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.5518258543194977,
  "model_score": 0.4998,
  "style_score": 0.234,
  "label": "placeholder",
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
  "content_id": "7b31409a-6c91-42ae-aec8-6f0f45b31664",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.08007897516399883,
  "model_score": 0.6401,
  "style_score": 0.0956,
  "label": "placeholder",
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
  "content_id": "17336008-8035-4eda-a56d-06dd397b711e",
  "creator_id": "attacker_PI06",
  "guess": "human",
  "confidence": 0.09048924178302728,
  "model_score": 0.5583,
  "style_score": 0.3905,
  "label": "placeholder",
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
  "content_id": "6dc95295-7eb1-4231-ac03-c33f634db522",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "d467e4e0-802b-4bfe-acb3-e4df26cb6f3e",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0112,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "848701ff-722f-418e-bfc3-5e0ed4417589",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9976,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "cf6036ff-5033-4c82-8424-13c42057039a",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9969,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "ab71c9b9-fc13-4868-aca6-b5595cbdf8eb",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.0,
  "model_score": 0.9064,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "28c15540-ed8f-474f-b9a7-131d94d3cc39",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.2181780507676133,
  "model_score": 0.9876,
  "style_score": 0.4284,
  "label": "placeholder",
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
  "content_id": "4167788b-dcb8-4c6a-99b3-e40c61866547",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.2395,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "4a3cdf6f-40e6-4f01-a1b8-bfab8fe93569",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0492,
  "style_score": null,
  "label": "placeholder",
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
  "content_id": "f189e0db-b021-49f2-958d-8507db381829",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "de52ed23-8430-4394-9aa3-8e37f16f9ab0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "dbcb62cf-e4c6-445d-8491-789bba7296f9",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "6d9cc497-f613-43ac-830d-6d62c1de7803",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "e6a520b2-1ed3-451b-9215-7d26ec3f02af",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "13f78700-378a-48ab-a492-84ebf96604e6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "4c15ca5b-e6d4-4c84-8c9d-b48f172bb15d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "20c55c93-3d31-49fe-b76a-4492c1fb61c1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "ebb1a6e7-553d-43d0-b3ff-6d822b19c7db",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
  "content_id": "9e1ae35f-61e4-488c-9eaf-f70a1d0c739b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "placeholder",
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
