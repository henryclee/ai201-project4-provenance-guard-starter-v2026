# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 10:55
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `ef10614c-f74f-463b-9722-d0fa24df55d2` | unsure | 0.199 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `2db4fb37-5915-4c08-82e6-09a93e53b654` | human | 0.695 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `317d460a-3779-49f3-99aa-bc8a65cba981` | unsure | 0.120 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `987c0b4d-5cbd-4497-8c41-303a2db42df6` | ai | 0.622 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `053a0614-7177-4cbf-aa12-760eaa010280` | human | 0.950 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a2f35b4a-3e37-4d69-991f-9a70b3333c15` | human | 0.750 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `94fc26c3-9c13-460a-a9fc-f28e37f6aa3e` | human | 0.826 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `2c926a97-42a7-4907-ac6c-90422a6efba6` | unsure | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `83392632-5298-4858-85ce-d1a868f732bc` | unsure | 0.218 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `9c65cf8b-7cd5-4119-9f9c-2aa8d6ea55f4` | ai | 0.757 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0f605b34-a1a4-43e7-b3c3-3c3a00720767` | unsure | 0.156 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `89f12dd3-f780-4e52-91e5-4e4406a78d8a` | ai | 0.875 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `955afd49-15e6-4c28-8d8d-3ee03d90a999` | ai | 0.861 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `626b6ff4-107d-4f59-9a8d-2deed93d4a23` | ai | 0.792 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `0b016647-7691-414d-afdd-4db3248b3b55` | ai | 0.912 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `05e968d8-3d6d-4ba8-96da-c4f962b053a3` | ai | 0.663 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `002699fc-7bad-4c5b-b20e-06d5b40f98c5` | ai | 0.852 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `dd29c18f-0519-4835-a64b-9021e29d1f49` | human | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `b2c9cdd7-d540-4814-96ea-907e12615592` | human | 0.565 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `78628fb4-3fd2-4027-b885-8e993057e467` | human | 0.537 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `bcdcc9f7-97a0-458b-8994-2df908605aaa` | unsure | 0.253 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9b54708b-0831-46e8-b92c-cbca767e6534` | human | 0.555 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1bed9f4c-c0bc-41d0-9433-1b052fb409a4` | unsure | 0.130 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4b5d83bc-9ca2-465b-bfd9-21cbd341e18b` | unsure | 0.072 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `f685648b-b68c-4b0d-82a2-38cbe166a9b4` | human | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `44a4f5d9-a55c-44c8-be77-094309e039bb` | human | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `0aa82bef-d5e1-4818-8965-7f37a99eb423` | ai | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `7ff805da-7e10-4e39-80e9-ec2d8765bd29` | ai | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `835947eb-a910-425b-8cdd-e7d493947310` | ai | 0.000 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `d49c85ae-eec6-4b71-8e6a-92c3fb9c9397` | ai | 0.821 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `e42a06d2-ab18-4d84-843f-7d665c09ff03` | unsure | 0.000 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c139b8e9-04a5-47af-9496-37854e2002f9` | human | 0.000 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cc4d414d-4cd4-43fb-a94b-549a753cd1f8` | unsure | 0.000 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0519ebd9-5e31-4dbd-96f1-b6788b90a635` | unsure | 0.000 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aad5455d-5394-40d2-b5fe-b3dea7cb6459` | unsure | 0.000 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ae87b11e-dc40-4ad3-89d9-b800a81c50ab` | unsure | 0.000 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3df09878-e8ab-4c94-bc8c-722e244051d9` | unsure | 0.000 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e28e144-f0a6-493c-bbdc-d08c25c67af7` | unsure | 0.000 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `31a1dde0-4250-46c6-a448-93b8d994d59c` | unsure | 0.000 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `60966e64-1755-40da-b97f-c9e4a4a9b614` | unsure | 0.000 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8ba04ddb-076e-4edb-9ad1-b16e91d9e4f0` | unsure | 0.000 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dc2a0797-0b91-4615-a1c8-a2408657f537` | unsure | 0.000 |  |
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
  "content_id": "ef10614c-f74f-463b-9722-d0fa24df55d2",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.19893208231418857,
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
  "content_id": "2db4fb37-5915-4c08-82e6-09a93e53b654",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.6945482518295679,
  "model_score": 0.5943,
  "style_score": 0.1602,
  "label": "This appears to have been written by a human.",
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
  "content_id": "317d460a-3779-49f3-99aa-bc8a65cba981",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.11995080055775693,
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
  "content_id": "987c0b4d-5cbd-4497-8c41-303a2db42df6",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6221558841764117,
  "model_score": 0.6114,
  "style_score": 0.6006,
  "label": "This appears to have been written by AI.",
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
  "content_id": "053a0614-7177-4cbf-aa12-760eaa010280",
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
  "content_id": "a2f35b4a-3e37-4d69-991f-9a70b3333c15",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.7497873008752113,
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
  "content_id": "94fc26c3-9c13-460a-a9fc-f28e37f6aa3e",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.8255760002610252,
  "model_score": 0.5862,
  "style_score": 0.0,
  "label": "This appears to have been written by a human.",
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
  "content_id": "2c926a97-42a7-4907-ac6c-90422a6efba6",
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
  "content_id": "83392632-5298-4858-85ce-d1a868f732bc",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.21775069493447302,
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
  "content_id": "9c65cf8b-7cd5-4119-9f9c-2aa8d6ea55f4",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7570747168525851,
  "model_score": 0.9792,
  "style_score": 0.3899,
  "label": "This appears to have been written by AI.",
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
  "content_id": "0f605b34-a1a4-43e7-b3c3-3c3a00720767",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.15592642944677282,
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
  "content_id": "89f12dd3-f780-4e52-91e5-4e4406a78d8a",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8752450894027877,
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
  "content_id": "955afd49-15e6-4c28-8d8d-3ee03d90a999",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8614152694556989,
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
  "content_id": "626b6ff4-107d-4f59-9a8d-2deed93d4a23",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7921351775209188,
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
  "content_id": "0b016647-7691-414d-afdd-4db3248b3b55",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.9115047774886813,
  "model_score": 0.8005,
  "style_score": 0.8558,
  "label": "This appears to have been written by AI.",
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
  "content_id": "05e968d8-3d6d-4ba8-96da-c4f962b053a3",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6634966461326074,
  "model_score": 0.8814,
  "style_score": 0.3522,
  "label": "This appears to have been written by AI.",
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
  "content_id": "002699fc-7bad-4c5b-b20e-06d5b40f98c5",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.8516184135363957,
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
  "content_id": "dd29c18f-0519-4835-a64b-9021e29d1f49",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.3223,
  "style_score": 0.3423,
  "label": "This appears to have been written by a human.",
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
  "content_id": "b2c9cdd7-d540-4814-96ea-907e12615592",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.5647957372504155,
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
  "content_id": "78628fb4-3fd2-4027-b885-8e993057e467",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5365794567997446,
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
  "content_id": "bcdcc9f7-97a0-458b-8994-2df908605aaa",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.2527066657547947,
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
  "content_id": "9b54708b-0831-46e8-b92c-cbca767e6534",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.5545529896566704,
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
  "content_id": "1bed9f4c-c0bc-41d0-9433-1b052fb409a4",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.13034359514701382,
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
  "content_id": "4b5d83bc-9ca2-465b-bfd9-21cbd341e18b",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.07152067952090752,
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
  "content_id": "f685648b-b68c-4b0d-82a2-38cbe166a9b4",
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
  "content_id": "44a4f5d9-a55c-44c8-be77-094309e039bb",
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
  "content_id": "0aa82bef-d5e1-4818-8965-7f37a99eb423",
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
  "content_id": "7ff805da-7e10-4e39-80e9-ec2d8765bd29",
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
  "content_id": "835947eb-a910-425b-8cdd-e7d493947310",
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
  "content_id": "d49c85ae-eec6-4b71-8e6a-92c3fb9c9397",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8210411768689612,
  "model_score": 0.9876,
  "style_score": 0.4284,
  "label": "This appears to have been written by AI.",
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
  "content_id": "e42a06d2-ab18-4d84-843f-7d665c09ff03",
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
  "content_id": "c139b8e9-04a5-47af-9496-37854e2002f9",
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
  "content_id": "cc4d414d-4cd4-43fb-a94b-549a753cd1f8",
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
  "content_id": "0519ebd9-5e31-4dbd-96f1-b6788b90a635",
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
  "content_id": "aad5455d-5394-40d2-b5fe-b3dea7cb6459",
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
  "content_id": "ae87b11e-dc40-4ad3-89d9-b800a81c50ab",
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
  "content_id": "3df09878-e8ab-4c94-bc8c-722e244051d9",
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
  "content_id": "4e28e144-f0a6-493c-bbdc-d08c25c67af7",
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
  "content_id": "31a1dde0-4250-46c6-a448-93b8d994d59c",
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
  "content_id": "60966e64-1755-40da-b97f-c9e4a4a9b614",
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
  "content_id": "8ba04ddb-076e-4edb-9ad1-b16e91d9e4f0",
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
  "content_id": "dc2a0797-0b91-4615-a1c8-a2408657f537",
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
