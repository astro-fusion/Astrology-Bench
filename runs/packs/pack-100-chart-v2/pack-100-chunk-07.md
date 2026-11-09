# Astro-Bench prompt pack, chunk 07 of 10 (items 61-70 of 100, input mode chart)

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

## Item 61 of 100: `L1-lordship-raman-mean-ws-000009`

Birth: 1942-09-13T06:51:00Z, latitude 35.6762, longitude 139.6503 (east positive) (Tokyo)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 286.27 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 148.25
  Moon: 180.70
  Mars: 155.72
  Mercury: 174.70
  Jupiter: 88.28
  Venus: 131.70
  Saturn: 50.79
  Rahu: 131.72
  Ketu: 311.72

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), in which house does the lord of the 7th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 62 of 100: `L1-lordship-raman-true-pl-000002`

Birth: 1925-08-04T10:42:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)
Sidereal chart (Raman ayanamsa, true node, Placidus houses):
  Lagna (ascendant): 347.48 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 110.14
  Moon: 289.39
  Mars: 123.29
  Mercury: 136.00
  Jupiter: 263.26 R
  Venus: 137.39
  Saturn: 196.71
  Rahu: 103.3
  Ketu: 283.3
  House cusps: 1: 347.48, 2: 13.53, 3: 44.51, 4: 79.34, 5: 113.51, 6: 143.14, 7: 167.48, 8: 193.53, 9: 224.51, 10: 259.34, 11: 293.51, 12: 323.14

Using the sidereal chart above (Raman ayanamsa, true node, Placidus houses), in which house does the lord of the 1st house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 63 of 100: `L1-lordship-raman-true-pl-000003`

Birth: 2018-01-09T00:51:00Z, latitude 30.0444, longitude 31.2357 (east positive) (Cairo)
Sidereal chart (Raman ayanamsa, true node, Placidus houses):
  Lagna (ascendant): 210.95 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 266.04
  Moon: 177.23
  Mars: 206.51
  Mercury: 244.49
  Jupiter: 205.58
  Venus: 265.97
  Saturn: 249.66
  Rahu: 112.6
  Ketu: 292.6
  House cusps: 1: 210.95, 2: 240.82, 3: 273.58, 4: 307.77, 5: 339.86, 6: 7.43, 7: 30.95, 8: 60.82, 9: 93.58, 10: 127.77, 11: 159.86, 12: 187.43

Using the sidereal chart above (Raman ayanamsa, true node, Placidus houses), in which house does the lord of the 12th house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 64 of 100: `L1-lordship-raman-true-ws-000006`

Birth: 1945-12-14T11:27:00Z, latitude -33.9249, longitude 18.4241 (east positive) (Cape Town)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 340.83 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 240.48
  Moon: 356.82
  Mars: 100.95 R
  Mercury: 225.89 R
  Jupiter: 180.76
  Venus: 228.72
  Saturn: 91.97 R
  Rahu: 68.3
  Ketu: 248.3

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), in which house does the lord of the 10th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 65 of 100: `L1-nakshatra-krishnamurti-mean-ws-000007`

Birth: 1919-07-22T11:43:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 331.34 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 95.96
  Moon: 32.82
  Mars: 76.59
  Mercury: 122.34
  Jupiter: 94.94
  Venus: 140.11
  Saturn: 124.79
  Rahu: 218.35
  Ketu: 38.35

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 66 of 100: `L1-nakshatra-krishnamurti-true-ws-000008`

Birth: 2004-12-01T13:41:00Z, latitude 28.6139, longitude 77.2090 (east positive) (New Delhi)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 72.41 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 225.88
  Moon: 97.58
  Mars: 199.79
  Mercury: 242.82 R
  Jupiter: 169.50
  Venus: 197.32
  Saturn: 93.02 R
  Rahu: 7.6
  Ketu: 187.6

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 67 of 100: `L1-nakshatra-lahiri-mean-ws-000000`

Birth: 1985-09-13T22:19:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 346.39 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 147.40
  Moon: 135.54
  Mars: 128.80
  Mercury: 139.47
  Jupiter: 284.08 R
  Venus: 116.42
  Saturn: 209.77
  Rahu: 17.94
  Ketu: 197.94

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 68 of 100: `L1-nakshatra-lahiri-mean-ws-000010`

Birth: 1951-01-24T22:33:00Z, latitude 40.7128, longitude -74.0060 (east positive) (New York)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 107.78 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 280.96
  Moon: 121.05
  Mars: 308.71
  Mercury: 256.50
  Jupiter: 316.40
  Venus: 298.20
  Saturn: 159.04 R
  Rahu: 328.34
  Ketu: 148.34

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 69 of 100: `L1-nakshatra-lahiri-mean-ws-000028`

Birth: 1993-12-09T13:56:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 85.92 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 233.74
  Moon: 182.52
  Mars: 238.40
  Mercury: 220.04
  Jupiter: 192.13
  Venus: 224.50
  Saturn: 301.37
  Rahu: 218.51
  Ketu: 38.51

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 70 of 100: `L1-nakshatra-lahiri-true-ws-000001`

Birth: 1963-10-24T09:10:00Z, latitude -33.8688, longitude 151.2093 (east positive) (Sydney)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 19.08 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 186.89
  Moon: 261.63
  Mars: 215.69
  Mercury: 179.15
  Jupiter: 349.02 R
  Venus: 201.48
  Saturn: 293.11
  Rahu: 80.8
  Ketu: 260.8

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
