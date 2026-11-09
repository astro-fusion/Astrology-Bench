# Astro-Bench prompt pack, chunk 08 of 10 (items 71-80 of 100, input mode chart)

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

## Item 71 of 100: `L1-nakshatra-raman-mean-ws-000007`

Birth: 1904-05-16T21:04:00Z, latitude -6.2088, longitude 106.8456 (east positive) (Jakarta)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 6.72 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 34.46
  Moon: 52.16
  Mars: 38.03
  Mercury: 29.20 R
  Jupiter: 357.00
  Venus: 20.27
  Saturn: 299.75
  Rahu: 153.52
  Ketu: 333.52

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 72 of 100: `L1-nakshatra-raman-mean-ws-000008`

Birth: 1966-12-26T16:20:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 216.99 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 252.50
  Moon: 59.30
  Mars: 169.64
  Mercury: 239.86
  Jupiter: 100.57 R
  Venus: 264.08
  Saturn: 331.76
  Rahu: 21.66
  Ketu: 201.66

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 73 of 100: `L1-nakshatra-raman-true-ws-000006`

Birth: 1979-02-20T15:48:00Z, latitude -33.9249, longitude 18.4241 (east positive) (Cape Town)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 96.67 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 309.29
  Moon: 226.85
  Mars: 302.20
  Mercury: 318.61
  Jupiter: 98.62 R
  Venus: 265.09
  Saturn: 139.15 R
  Rahu: 145.5
  Ketu: 325.5

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), in which nakshatra and pada is the Moon? Give "answer" as {"nakshatra": "<name>", "pada": <1-4>}. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 74 of 100: `L1-rule-mangal_8th_aspect_ketu-lahiri-mean-ws-000004`

Birth: 1947-05-12T10:46:00Z, latitude 48.8566, longitude 2.3522 (east positive) (Paris)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 115.75 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 27.75
  Moon: 287.86
  Mars: 0.31
  Mercury: 23.59
  Jupiter: 209.82 R
  Venus: 357.68
  Saturn: 100.15
  Rahu: 40.07
  Ketu: 220.07

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Mangal-8th-Aspect-Ketu" hold in this chart? The rule as stated: Mars casting its special 8th aspect on Ketu triggers seismic stress. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 75 of 100: `L1-rule-mangal_ketu_primary-lahiri-mean-ws-000003`

Birth: 1955-05-22T12:59:00Z, latitude 35.6762, longitude 139.6503 (east positive) (Tokyo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 261.88 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 37.43
  Moon: 46.93
  Mars: 64.47
  Mercury: 59.73
  Jupiter: 92.86
  Venus: 10.35
  Saturn: 203.65 R
  Rahu: 244.69
  Ketu: 64.69

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Mangal-Ketu-Primary" hold in this chart? The rule as stated: A Mars-Ketu conjunction within 15 degrees releases sudden martial energy (earthquakes). Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 76 of 100: `L1-rule-mangal_shani_malefic-lahiri-mean-ws-000000`

Birth: 1902-07-10T16:50:00Z, latitude 13.0827, longitude 80.2707 (east positive) (Chennai)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 325.95 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 84.97
  Moon: 153.47
  Mars: 60.69
  Mercury: 65.94
  Jupiter: 292.94 R
  Venus: 49.68
  Saturn: 272.53 R
  Rahu: 187.91
  Ketu: 7.91

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Mangal-Shani-Malefic" hold in this chart? The rule as stated: A Mars-Saturn conjunction within 15 degrees is associated with earthquakes. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 77 of 100: `L1-rule-shani_10th_aspect_mars-lahiri-true-ws-000000`

Birth: 1907-08-05T02:48:00Z, latitude -33.8688, longitude 151.2093 (east positive) (Sydney)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 230.63 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 108.97
  Moon: 63.68
  Mars: 254.53 R
  Mercury: 93.85
  Jupiter: 94.44
  Venus: 97.83
  Saturn: 334.33 R
  Rahu: 90.8
  Ketu: 270.8

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), does "Shani-10th-Aspect-Mars" hold in this chart? The rule as stated: Saturn casting its special 10th aspect on Mars triggers seismic stress. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 78 of 100: `L1-rule-venus_own_sign-lahiri-mean-ws-000001`

Birth: 1938-09-22T19:19:00Z, latitude 40.7128, longitude -74.0060 (east positive) (New York)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 261.43 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 156.11
  Moon: 142.20
  Mars: 136.48
  Mercury: 142.05
  Jupiter: 300.52 R
  Venus: 201.75
  Saturn: 352.81 R
  Rahu: 207.19
  Ketu: 27.19

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Venus-Own-Sign" hold in this chart? The rule as stated: Venus in its own signs (Taurus, Libra) supports value and luxury assets. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 79 of 100: `L1-rule-venus_own_sign-lahiri-true-ws-000001`

Birth: 2021-09-13T00:38:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 16.63 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 146.30
  Moon: 225.34
  Mars: 154.56
  Mercury: 172.93
  Jupiter: 300.14 R
  Venus: 188.34
  Saturn: 283.36 R
  Rahu: 40.6
  Ketu: 220.6

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), does "Venus-Own-Sign" hold in this chart? The rule as stated: Venus in its own signs (Taurus, Libra) supports value and luxury assets. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 80 of 100: `L1-varga-krishnamurti-mean-ws-000002`

Birth: 2021-04-19T15:33:00Z, latitude 6.9271, longitude 79.8612 (east positive) (Colombo)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 225.85 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 5.74
  Moon: 88.32
  Mars: 63.62
  Mercury: 6.39
  Jupiter: 302.55
  Venus: 11.99
  Saturn: 288.55
  Rahu: 49.05
  Ketu: 229.05

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Jupiter occupy in the D9 Navamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
