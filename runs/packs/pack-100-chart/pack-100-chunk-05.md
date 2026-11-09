# Astro-Bench prompt pack, chunk 05 of 10 (items 41-50 of 100, input mode chart)

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

## Item 41 of 100: `L1-dignity-krishnamurti-true-ws-000004`

Birth: 2025-12-02T15:50:00Z, latitude 41.8781, longitude -87.6298 (east positive) (Chicago)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 264.55 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 226.60
  Moon: 13.72
  Mars: 236.40
  Mercury: 207.29
  Jupiter: 90.30 R
  Venus: 218.16
  Saturn: 331.05
  Rahu: 320.0
  Ketu: 140.0

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), what is the dignity of Sun? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 42 of 100: `L1-dignity-krishnamurti-true-ws-000005`

Birth: 1938-08-01T15:00:00Z, latitude 19.4326, longitude -99.1332 (east positive) (Mexico City)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 143.34 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 105.78
  Moon: 178.58
  Mars: 103.33
  Mercury: 132.98
  Jupiter: 306.82 R
  Venus: 148.10
  Saturn: 355.14 R
  Rahu: 210.8
  Ketu: 30.8

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), what is the dignity of Moon? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 43 of 100: `L1-dignity-krishnamurti-true-ws-000009`

Birth: 2018-10-01T11:38:00Z, latitude -12.0464, longitude -77.0428 (east positive) (Lima)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 176.95 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 164.22
  Moon: 62.30
  Mars: 282.12
  Mercury: 172.22
  Jupiter: 208.15
  Venus: 196.47
  Saturn: 249.03
  Rahu: 99.5
  Ketu: 279.5

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), what is the dignity of Mars? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 44 of 100: `L1-dignity-lahiri-mean-ws-000008`

Birth: 2028-02-18T03:46:00Z, latitude -34.6037, longitude -58.3816 (east positive) (Buenos Aires)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 229.45 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 304.75
  Moon: 224.46
  Mars: 311.65
  Mercury: 280.46
  Jupiter: 151.19 R
  Venus: 348.19
  Saturn: 359.49
  Rahu: 276.71
  Ketu: 96.71

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), what is the dignity of Mars? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 45 of 100: `L1-dignity-lahiri-mean-ws-000022`

Birth: 2027-05-29T02:45:00Z, latitude 35.6762, longitude 139.6503 (east positive) (Tokyo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 136.94 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 43.30
  Moon: 319.26
  Mars: 131.64
  Mercury: 66.13
  Jupiter: 115.80
  Venus: 23.08
  Saturn: 359.51
  Rahu: 290.76
  Ketu: 110.76

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), what is the dignity of Mercury? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 46 of 100: `L1-dignity-lahiri-mean-ws-000023`

Birth: 2030-06-28T15:39:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 289.62 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 72.71
  Moon: 48.05
  Mars: 63.69
  Mercury: 78.01
  Jupiter: 203.88 R
  Venus: 43.04
  Saturn: 39.09
  Rahu: 231.06
  Ketu: 51.06

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), what is the dignity of Jupiter? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 47 of 100: `L1-dignity-lahiri-mean-ws-000038`

Birth: 1945-06-11T01:26:00Z, latitude 59.9139, longitude 10.7522 (east positive) (Oslo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 42.05 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 56.67
  Moon: 68.33
  Mars: 6.59
  Mercury: 50.59
  Jupiter: 145.53
  Venus: 11.76
  Saturn: 77.98
  Rahu: 77.18
  Ketu: 257.18

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), what is the dignity of Moon? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 48 of 100: `L1-dignity-raman-true-ws-000005`

Birth: 1920-08-30T00:49:00Z, latitude 27.7172, longitude 85.3240 (east positive) (Kathmandu)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 145.83 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 135.03
  Moon: 320.80
  Mars: 215.03
  Mercury: 125.32
  Jupiter: 129.30
  Venus: 150.72
  Saturn: 142.58
  Rahu: 197.1
  Ketu: 17.1

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), what is the dignity of Moon? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 49 of 100: `L1-lordship-krishnamurti-mean-pl-000001`

Birth: 1909-08-08T18:53:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, Placidus houses):
  Lagna (ascendant): 70.72 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 113.05
  Moon: 26.65
  Mars: 342.89
  Mercury: 117.64
  Jupiter: 143.89
  Venus: 140.27
  Saturn: 0.72 R
  Rahu: 50.96
  Ketu: 230.96
  House cusps: 1: 70.72, 2: 111.51, 3: 154.00, 4: 186.78, 5: 211.02, 6: 231.07, 7: 250.72, 8: 291.51, 9: 334.00, 10: 6.78, 11: 31.02, 12: 51.07

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, Placidus houses), in which house does the lord of the 9th house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 50 of 100: `L1-lordship-krishnamurti-mean-ws-000005`

Birth: 1917-06-08T05:59:00Z, latitude 48.8566, longitude 2.3522 (east positive) (Paris)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 82.66 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 54.24
  Moon: 270.30
  Mars: 32.64
  Mercury: 31.47
  Jupiter: 32.61
  Venus: 65.69
  Saturn: 95.52
  Rahu: 259.38
  Ketu: 79.38

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses), in which house does the lord of the 4th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
