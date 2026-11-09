# Astro-Bench prompt pack, chunk 09 of 10 (items 81-90 of 100, input mode chart)

## Disclosure header

Fill this in once per run and copy it, filled, to the top of every reply file. One run is one harness, one model and one effort setting.

```
harness:
model (exactly as the UI shows):
provider model id (if known):
effort or thinking setting (or "not shown"):
tools allowed (yes/no):
operator:
date:
```

## How to reply

Reply to every item below. For each item write a line `### <item_id>` (the id exactly as given) and, on the next lines, one JSON object in the format of the system prompt: {"answer": ..., "citations": [...], "confidence": 0.0-1.0, "note": "optional"}. Nothing else is graded. Example:

### L1-dasha-lahiri-mean-ws-000000
{"answer": "Venus", "citations": [], "confidence": 0.6}

## System prompt

You are being evaluated on Astro-Bench, a benchmark of classical Vedic astrology (Jyotish).
Each question gives a birth moment and place and, for most questions, a computed sidereal
chart table, then asks one question under a stated convention (ayanamsa, node model,
house system). Answer under that convention only.

Reply with exactly one JSON object and nothing else of substance:

```json
{"answer": <see below>, "citations": [{"text": "BPHS", "chapter": "36", "verse": "3", "edition": "santhanam1984"}], "confidence": 0.0, "note": "optional"}
```

- `answer` has the shape the question asks for: `true`/`false` for yes/no questions; a
  string for a single choice (use the English names: Sun, Moon, Mars, Mercury, Jupiter,
  Venus, Saturn, Rahu, Ketu; Aries ... Pisces; Ashwini ... Revati); a JSON list for a set
  (use `[]` for the empty set); an object when the question gives an object format.
- `citations` lists the classical text, chapter and verse that support your answer
  (BPHS, Brihat Jataka, Phaladeepika, Saravali, Jaimini Sutras, Brihat Samhita, ...).
  Cite only what you are confident exists. If you cannot cite a source, set
  `"citations": []` and say so in `note`. A fabricated or wrong citation scores lower
  than no citation.
- `confidence` is your probability (0 to 1) that `answer` is correct.

## Items

## Item 81 of 100: `L1-varga-krishnamurti-true-ws-000008`

Birth: 1909-01-01T22:34:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 88.56 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 258.43
  Moon: 22.89
  Mars: 212.07
  Mercury: 263.60
  Jupiter: 142.03 R
  Venus: 230.05
  Saturn: 341.50
  Rahu: 63.4
  Ketu: 243.4

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Saturn occupy in the D10 Dasamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 82 of 100: `L1-varga-lahiri-mean-ws-000004`

Birth: 1993-01-27T14:41:00Z, latitude 30.0444, longitude 31.2357 (east positive) (Cairo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 94.92 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 283.92
  Moon: 336.84
  Mars: 77.19 R
  Mercury: 286.67
  Jupiter: 170.93
  Venus: 330.75
  Saturn: 295.60
  Rahu: 235.25
  Ketu: 55.25

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Moon occupy in the D10 Dasamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 83 of 100: `L1-varga-lahiri-mean-ws-000030`

Birth: 1966-06-30T13:43:00Z, latitude -33.9249, longitude 18.4241 (east positive) (Cape Town)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 226.32 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 74.93
  Moon: 228.23
  Mars: 59.43
  Mercury: 100.64
  Jupiter: 78.57
  Venus: 41.44
  Saturn: 336.20
  Rahu: 29.70
  Ketu: 209.70

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Rahu occupy in the D7 Saptamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 84 of 100: `L1-varga-lahiri-mean-ws-000032`

Birth: 1975-11-01T07:56:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 4.59 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 194.75
  Moon: 163.94
  Mars: 68.95
  Mercury: 178.64
  Jupiter: 353.72 R
  Venus: 148.31
  Saturn: 99.28
  Rahu: 208.96
  Ketu: 28.96

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Venus occupy in the D7 Saptamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 85 of 100: `L1-varga-lahiri-true-ws-000005`

Birth: 1948-07-02T19:31:00Z, latitude 59.9139, longitude 10.7522 (east positive) (Oslo)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 243.13 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 77.64
  Moon: 24.47
  Mars: 148.72
  Mercury: 65.46 R
  Jupiter: 238.77 R
  Venus: 64.97 R
  Saturn: 117.27
  Rahu: 19.3
  Ketu: 199.3

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Sun occupy in the D7 Saptamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 86 of 100: `L1-varga-lahiri-true-ws-000007`

Birth: 1973-05-14T02:42:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 106.23 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 29.68
  Moon: 174.96
  Mars: 310.69
  Mercury: 22.29
  Jupiter: 288.19
  Venus: 38.66
  Saturn: 56.52
  Rahu: 255.1
  Ketu: 75.1

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Rahu occupy in the D10 Dasamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 87 of 100: `L1-varga-raman-mean-ws-000004`

Birth: 1986-07-26T10:08:00Z, latitude 30.0444, longitude 31.2357 (east positive) (Cairo)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 189.83 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 100.91
  Moon: 345.38
  Mars: 261.12 R
  Mercury: 96.13 R
  Jupiter: 330.33 R
  Venus: 144.30
  Saturn: 220.95 R
  Rahu: 2.67
  Ketu: 182.67

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Jupiter occupy in the D7 Saptamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 88 of 100: `L1-varga-raman-true-ws-000002`

Birth: 1996-07-02T15:01:00Z, latitude -12.0464, longitude -77.0428 (east positive) (Lima)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 132.88 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 78.63
  Moon: 279.50
  Mars: 51.77
  Mercury: 68.27
  Jupiter: 260.64 R
  Venus: 49.41
  Saturn: 344.81
  Rahu: 170.3
  Ketu: 350.3

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Rahu occupy in the D9 Navamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 89 of 100: `L1-yoga-budha_aditya-lahiri-mean-ws-000008`

Birth: 1955-01-21T05:45:00Z, latitude 1.3521, longitude 103.8198 (east positive) (Singapore)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 19.49 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 277.18
  Moon: 245.04
  Mars: 341.10
  Mercury: 293.48
  Jupiter: 90.95 R
  Venus: 230.42
  Saturn: 206.66
  Rahu: 251.12
  Ketu: 71.12

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Budha-Aditya Yoga" hold in this chart? The rule as stated: The Sun and Mercury in the same sign give intelligence and skill. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 90 of 100: `L1-yoga-budha_aditya-lahiri-mean-ws-000013`

Birth: 2029-09-12T21:48:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 184.84 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 146.14
  Moon: 207.93
  Mars: 208.63
  Mercury: 152.08 R
  Jupiter: 183.47
  Venus: 188.54
  Saturn: 30.70 R
  Rahu: 246.36
  Ketu: 66.36

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Budha-Aditya Yoga" hold in this chart? The rule as stated: The Sun and Mercury in the same sign give intelligence and skill. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
