# Astro-Bench prompt pack, chunk 03 of 10 (items 21-30 of 100, input mode chart)

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

## Item 21 of 100: `L1-combustion-krishnamurti-mean-ws-000009`

Birth: 1923-09-27T09:40:00Z, latitude 13.0827, longitude 80.2707 (east positive) (Chennai)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 291.28 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 160.56
  Moon: 6.46
  Mars: 144.08
  Mercury: 164.29 R
  Jupiter: 205.03
  Venus: 165.10
  Saturn: 177.94
  Rahu: 137.38
  Ketu: 317.38

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 22 of 100: `L1-combustion-lahiri-mean-ws-000014`

Birth: 1925-12-11T04:54:00Z, latitude 48.8566, longitude 2.3522 (east positive) (Paris)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 204.42 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 235.82
  Moon: 176.71
  Mars: 205.72
  Mercury: 236.96 R
  Jupiter: 271.40
  Venus: 282.37
  Saturn: 207.85
  Rahu: 94.58
  Ketu: 274.58

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 23 of 100: `L1-combustion-lahiri-mean-ws-000016`

Birth: 1981-09-10T08:17:00Z, latitude -1.2921, longitude 36.8219 (east positive) (Nairobi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 219.30 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 143.93
  Moon: 276.57
  Mars: 101.63
  Mercury: 167.17
  Jupiter: 169.95
  Venus: 183.35
  Saturn: 166.11
  Rahu: 95.55
  Ketu: 275.55

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 24 of 100: `L1-combustion-lahiri-mean-ws-000033`

Birth: 1925-11-01T22:49:00Z, latitude -34.6037, longitude -58.3816 (east positive) (Buenos Aires)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 22.48 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 196.18
  Moon: 31.27
  Mars: 179.48
  Mercury: 211.59
  Jupiter: 264.16
  Venus: 241.62
  Saturn: 203.24
  Rahu: 96.67
  Ketu: 276.67

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 25 of 100: `L1-combustion-lahiri-mean-ws-000034`

Birth: 1956-11-30T19:06:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 146.89 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 225.31
  Moon: 207.19
  Mars: 334.00
  Mercury: 235.23
  Jupiter: 155.31
  Venus: 193.21
  Saturn: 222.47
  Rahu: 215.11
  Ketu: 35.11

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 26 of 100: `L1-combustion-lahiri-true-ws-000000`

Birth: 2020-05-08T10:39:00Z, latitude 27.7172, longitude 85.3240 (east positive) (Kathmandu)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 175.15 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 24.16
  Moon: 217.94
  Mars: 302.62
  Mercury: 28.41
  Jupiter: 273.04
  Venus: 57.26
  Saturn: 277.81
  Rahu: 65.6
  Ketu: 245.6

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 27 of 100: `L1-combustion-lahiri-true-ws-000008`

Birth: 1999-01-27T14:57:00Z, latitude 28.6139, longitude 77.2090 (east positive) (New Delhi)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 136.74 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 283.38
  Moon: 50.72
  Mars: 186.61
  Mercury: 278.18
  Jupiter: 332.73
  Venus: 304.84
  Saturn: 3.69
  Rahu: 118.4
  Ketu: 298.4

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 28 of 100: `L1-combustion-raman-mean-ws-000005`

Birth: 1989-12-17T16:22:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 351.58 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 243.44
  Moon: 127.22
  Mars: 217.36
  Mercury: 262.32
  Jupiter: 74.87 R
  Venus: 281.59
  Saturn: 261.65
  Rahu: 296.95
  Ketu: 116.95

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 29 of 100: `L1-combustion-raman-true-ws-000002`

Birth: 1913-12-25T11:46:00Z, latitude 13.0827, longitude 80.2707 (east positive) (Chennai)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 65.05 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 251.90
  Moon: 224.79
  Mars: 87.79 R
  Mercury: 234.94
  Jupiter: 272.46
  Venus: 240.32
  Saturn: 52.02 R
  Rahu: 327.0
  Ketu: 147.0

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 30 of 100: `L1-combustion-raman-true-ws-000005`

Birth: 1993-05-30T07:21:00Z, latitude 27.7172, longitude 85.3240 (east positive) (Kathmandu)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 151.81 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 46.58
  Moon: 157.11
  Mars: 114.23
  Mercury: 62.53
  Jupiter: 162.44 R
  Venus: 1.31
  Saturn: 307.91
  Rahu: 229.9
  Ketu: 49.9

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
