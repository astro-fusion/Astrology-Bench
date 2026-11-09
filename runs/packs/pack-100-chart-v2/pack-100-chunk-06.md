# Astro-Bench prompt pack, chunk 06 of 10 (items 51-60 of 100, input mode chart)

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

## Item 51 of 100: `L1-lordship-krishnamurti-true-pl-000003`

Birth: 1989-10-16T04:19:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, Placidus houses):
  Lagna (ascendant): 229.03 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 179.16
  Moon: 18.14
  Mars: 173.72
  Mercury: 162.80
  Jupiter: 76.98
  Venus: 224.75
  Saturn: 254.66
  Rahu: 300.4
  Ketu: 120.4
  House cusps: 1: 229.03, 2: 259.97, 3: 293.79, 4: 328.10, 5: 359.07, 6: 25.51, 7: 49.03, 8: 79.97, 9: 113.79, 10: 148.10, 11: 179.07, 12: 205.51

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, Placidus houses), in which house does the lord of the 1st house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 52 of 100: `L1-lordship-lahiri-mean-pl-000000`

Birth: 1952-07-07T04:26:00Z, latitude 1.3521, longitude 103.8198 (east positive) (Singapore)
Sidereal chart (Lahiri ayanamsa, mean node, Placidus houses):
  Lagna (ascendant): 162.63 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 81.79
  Moon: 257.02
  Mars: 192.37
  Mercury: 106.72
  Jupiter: 21.66
  Venus: 85.17
  Saturn: 165.58
  Rahu: 300.30
  Ketu: 120.30
  House cusps: 1: 162.63, 2: 194.34, 3: 223.86, 4: 251.76, 5: 280.07, 6: 310.46, 7: 342.63, 8: 14.34, 9: 43.86, 10: 71.76, 11: 100.07, 12: 130.46

Using the sidereal chart above (Lahiri ayanamsa, mean node, Placidus houses), in which house does the lord of the 8th house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 53 of 100: `L1-lordship-lahiri-mean-ws-000011`

Birth: 1940-02-14T19:02:00Z, latitude 59.9139, longitude 10.7522 (east positive) (Oslo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 150.69 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 301.93
  Moon: 12.21
  Mars: 5.43
  Mercury: 312.81
  Jupiter: 345.65
  Venus: 340.04
  Saturn: 3.49
  Rahu: 180.16
  Ketu: 0.16

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which house does the lord of the 9th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 54 of 100: `L1-lordship-lahiri-mean-ws-000032`

Birth: 1934-03-09T16:27:00Z, latitude 41.8781, longitude -87.6298 (east positive) (Chicago)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 56.17 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 325.48
  Moon: 247.70
  Mars: 333.40
  Mercury: 318.15 R
  Jupiter: 178.84 R
  Venus: 287.63
  Saturn: 299.33
  Rahu: 295.05
  Ketu: 115.05

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which house does the lord of the 7th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 55 of 100: `L1-lordship-lahiri-mean-ws-000034`

Birth: 1914-07-15T10:28:00Z, latitude 28.6139, longitude 77.2090 (east positive) (New Delhi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 223.54 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 89.41
  Moon: 0.74
  Mars: 138.72
  Mercury: 91.54 R
  Jupiter: 297.85 R
  Venus: 127.15
  Saturn: 63.08
  Rahu: 315.39
  Ketu: 135.39

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which house does the lord of the 5th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 56 of 100: `L1-lordship-lahiri-mean-ws-000038`

Birth: 1998-10-13T23:23:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 269.24 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 176.58
  Moon: 104.72
  Mars: 130.10
  Mercury: 189.08
  Jupiter: 325.86 R
  Venus: 172.40
  Saturn: 7.10 R
  Rahu: 124.74
  Ketu: 304.74

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), in which house does the lord of the 9th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 57 of 100: `L1-lordship-lahiri-true-pl-000005`

Birth: 1914-07-29T19:25:00Z, latitude 27.7172, longitude 85.3240 (east positive) (Kathmandu)
Sidereal chart (Lahiri ayanamsa, true node, Placidus houses):
  Lagna (ascendant): 44.27 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 103.13
  Moon: 190.69
  Mars: 147.48
  Mercury: 86.47
  Jupiter: 296.23 R
  Venus: 143.78
  Saturn: 64.76
  Rahu: 313.5
  Ketu: 133.5
  House cusps: 1: 44.27, 2: 69.12, 3: 92.46, 4: 118.11, 5: 149.29, 6: 186.54, 7: 224.27, 8: 249.12, 9: 272.46, 10: 298.11, 11: 329.29, 12: 6.54

Using the sidereal chart above (Lahiri ayanamsa, true node, Placidus houses), in which house does the lord of the 2nd house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 58 of 100: `L1-lordship-lahiri-true-ws-000002`

Birth: 1975-04-24T19:07:00Z, latitude 27.7172, longitude 85.3240 (east positive) (Kathmandu)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 277.54 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 10.46
  Moon: 176.41
  Mars: 316.38
  Mercury: 17.28
  Jupiter: 345.33
  Venus: 49.22
  Saturn: 79.96
  Rahu: 217.6
  Ketu: 37.6

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), in which house does the lord of the 5th house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 59 of 100: `L1-lordship-raman-mean-pl-000005`

Birth: 1972-03-04T11:44:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Raman ayanamsa, mean node, Placidus houses):
  Lagna (ascendant): 132.17 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 321.98
  Moon: 190.32
  Mars: 23.08
  Mercury: 335.84
  Jupiter: 252.41
  Venus: 4.96
  Saturn: 38.56
  Rahu: 281.25
  Ketu: 101.25
  House cusps: 1: 132.17, 2: 159.23, 3: 189.51, 4: 221.31, 5: 252.78, 6: 283.17, 7: 312.17, 8: 339.23, 9: 9.51, 10: 41.31, 11: 72.78, 12: 103.17

Using the sidereal chart above (Raman ayanamsa, mean node, Placidus houses), in which house does the lord of the 6th house sit? The lord is the Parashari ruler of the sign on that house's cusp (cusps listed above); Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 60 of 100: `L1-lordship-raman-mean-ws-000003`

Birth: 1934-06-05T22:14:00Z, latitude 51.5074, longitude -0.1278 (east positive) (London)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 262.56 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 53.03
  Moon: 340.57
  Mars: 40.81
  Mercury: 75.48
  Jupiter: 171.81 R
  Venus: 12.49
  Saturn: 306.68
  Rahu: 291.82
  Ketu: 111.82

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), in which house does the lord of the 1st house sit? The lord is the Parashari ruler of the sign of that house; Rahu and Ketu rule no sign. Give "answer" as the house number 1-12 as a string. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
