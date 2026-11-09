# Astro-Bench prompt pack, chunk 04 of 10 (items 31-40 of 100, input mode chart)

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

## Item 31 of 100: `L1-dasha-krishnamurti-true-ws-000002`

Birth: 1949-10-05T12:16:00Z, latitude -12.0464, longitude -77.0428 (east positive) (Lima)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 193.01 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 168.86
  Moon: 331.41
  Mars: 114.36
  Mercury: 165.34 R
  Jupiter: 269.73
  Venus: 211.27
  Saturn: 140.58
  Rahu: 353.6
  Ketu: 173.6

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's mahadasha is running at 1976-07-27T10:08:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 32 of 100: `L1-dasha-krishnamurti-true-ws-000008`

Birth: 1949-05-10T00:09:00Z, latitude 1.3521, longitude 103.8198 (east positive) (Singapore)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 42.90 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 25.96
  Moon: 171.08
  Mars: 14.34
  Mercury: 47.33
  Jupiter: 278.94
  Venus: 32.01
  Saturn: 126.33
  Rahu: 2.5
  Ketu: 182.5

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's antardasha is running at 2011-04-08T19:54:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 33 of 100: `L1-dasha-krishnamurti-true-ws-000009`

Birth: 1948-06-17T22:59:00Z, latitude 19.0760, longitude 72.8777 (east positive) (Mumbai)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 40.28 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 63.58
  Moon: 200.84
  Mars: 140.92
  Mercury: 72.76 R
  Jupiter: 240.69 R
  Venus: 73.84 R
  Saturn: 115.87
  Rahu: 20.4
  Ketu: 200.4

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's mahadasha is running at 1957-11-07T05:32:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 34 of 100: `L1-dasha-lahiri-mean-ws-000007`

Birth: 2016-10-06T01:27:00Z, latitude -12.0464, longitude -77.0428 (east positive) (Lima)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 24.40 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 169.14
  Moon: 224.32
  Mars: 251.71
  Mercury: 153.86
  Jupiter: 161.64
  Venus: 201.07
  Saturn: 227.91
  Rahu: 136.74
  Ketu: 316.74

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's mahadasha is running at 2032-04-25T01:39:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 35 of 100: `L1-dasha-lahiri-mean-ws-000011`

Birth: 1948-08-18T13:45:00Z, latitude 28.6139, longitude 77.2090 (east positive) (New Delhi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 309.31 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 122.36
  Moon: 289.69
  Mars: 176.52
  Mercury: 129.18
  Jupiter: 235.97
  Venus: 77.59
  Saturn: 122.92
  Rahu: 15.47
  Ketu: 195.47

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's antardasha is running at 1994-01-12T21:28:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 36 of 100: `L1-dasha-lahiri-mean-ws-000013`

Birth: 1948-12-23T17:33:00Z, latitude 28.6139, longitude 77.2090 (east positive) (New Delhi)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 141.57 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 248.68
  Moon: 165.38
  Mars: 267.47
  Mercury: 254.88
  Jupiter: 255.32
  Venus: 221.11
  Saturn: 133.02 R
  Rahu: 8.73
  Ketu: 188.73

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's antardasha is running at 2008-07-26T17:12:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 37 of 100: `L1-dasha-lahiri-mean-ws-000019`

Birth: 2018-07-16T10:05:00Z, latitude 19.0760, longitude 72.8777 (east positive) (Mumbai)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 218.74 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 89.73
  Moon: 135.98
  Mars: 282.79 R
  Mercury: 115.65
  Jupiter: 199.28
  Venus: 132.91
  Saturn: 250.39 R
  Rahu: 102.38
  Ketu: 282.38

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's antardasha is running at 2059-05-28T02:47:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 38 of 100: `L1-dasha-lahiri-mean-ws-000035`

Birth: 1911-02-09T04:31:00Z, latitude -33.8688, longitude 151.2093 (east positive) (Sydney)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 49.97 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 296.71
  Moon: 60.24
  Mars: 253.37
  Mercury: 272.24
  Jupiter: 201.31
  Venus: 314.49
  Saturn: 8.39
  Rahu: 21.75
  Ketu: 201.75

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's mahadasha is running at 1990-06-20T03:39:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 39 of 100: `L1-dasha-raman-true-ws-000007`

Birth: 1926-11-02T10:53:00Z, latitude -1.2921, longitude 36.8219 (east positive) (Nairobi)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 307.79 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 197.88
  Moon: 162.37
  Mars: 20.51 R
  Mercury: 220.92
  Jupiter: 296.54
  Venus: 193.11
  Saturn: 215.01
  Rahu: 77.8
  Ketu: 257.8

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses) and Vimshottari dasha from the Moon's nakshatra at birth (dasha year = 365.25 days), which planet's antardasha is running at 1953-09-10T08:07:00Z? Give "answer" as the planet name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 40 of 100: `L1-dignity-krishnamurti-mean-ws-000007`

Birth: 1953-01-31T22:13:00Z, latitude -34.6037, longitude -58.3816 (east positive) (Buenos Aires)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 95.57 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 288.66
  Moon: 129.66
  Mars: 331.48
  Mercury: 287.20
  Jupiter: 19.06
  Venus: 335.56
  Saturn: 184.17
  Rahu: 289.33
  Ketu: 109.33

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses), what is the dignity of Moon? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
