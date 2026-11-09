# Astro-Bench prompt pack, chunk 02 of 10 (items 11-20 of 100, input mode chart)

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

## Item 11 of 100: `L1-aspect-krishnamurti-mean-ws-000009`

Birth: 1972-08-20T20:30:00Z, latitude -1.2921, longitude 36.8219 (east positive) (Nairobi)
Sidereal chart (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 22.29 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 124.51
  Moon: 256.87
  Mars: 130.31
  Mercury: 107.61
  Jupiter: 245.14 R
  Venus: 78.88
  Saturn: 55.60
  Rahu: 270.92
  Ketu: 90.92

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 12th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 12 of 100: `L1-aspect-lahiri-mean-ws-000029`

Birth: 1997-11-04T03:12:00Z, latitude 59.9139, longitude 10.7522 (east positive) (Oslo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 163.75 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 197.91
  Moon: 241.12
  Mars: 242.36
  Mercury: 210.77
  Jupiter: 289.45
  Venus: 244.93
  Saturn: 351.22 R
  Rahu: 142.96
  Ketu: 322.96

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 9th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 13 of 100: `L1-aspect-lahiri-mean-ws-000031`

Birth: 2012-08-07T12:09:00Z, latitude 48.8566, longitude 2.3522 (east positive) (Paris)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 192.94 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 111.35
  Moon: 356.23
  Mars: 175.90
  Mercury: 97.42 R
  Jupiter: 47.31
  Venus: 65.90
  Saturn: 180.22
  Rahu: 217.32
  Ketu: 37.32

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 8th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 14 of 100: `L1-aspect-lahiri-mean-ws-000037`

Birth: 1940-12-27T06:53:00Z, latitude 13.0827, longitude 80.2707 (east positive) (Chennai)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 348.00 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 252.36
  Moon: 231.50
  Mars: 211.24
  Mercury: 243.68
  Jupiter: 12.67 R
  Venus: 225.01
  Saturn: 15.02 R
  Rahu: 163.39
  Ketu: 343.39

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 5th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 15 of 100: `L1-aspect-lahiri-true-ws-000003`

Birth: 2029-09-12T22:44:00Z, latitude 25.3176, longitude 82.9739 (east positive) (Varanasi)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 125.38 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 146.17
  Moon: 208.50
  Mars: 208.66
  Mercury: 152.04 R
  Jupiter: 183.48
  Venus: 188.58
  Saturn: 30.70 R
  Rahu: 246.8
  Ketu: 66.8

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 9th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 16 of 100: `L1-aspect-lahiri-true-ws-000009`

Birth: 1996-11-16T00:31:00Z, latitude -42.8821, longitude 147.3272 (east positive) (Hobart)
Sidereal chart (Lahiri ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 290.24 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 210.12
  Moon: 273.38
  Mars: 135.18
  Mercury: 218.25
  Jupiter: 261.58
  Venus: 177.52
  Saturn: 337.07 R
  Rahu: 163.1
  Ketu: 343.1

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 3rd house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 17 of 100: `L1-aspect-raman-mean-ws-000001`

Birth: 1981-03-11T12:19:00Z, latitude 59.9139, longitude 10.7522 (east positive) (Oslo)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 105.17 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 328.70
  Moon: 38.22
  Mars: 333.49
  Mercury: 301.59
  Jupiter: 165.20 R
  Venus: 321.91
  Saturn: 165.49 R
  Rahu: 106.69
  Ketu: 286.69

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 2nd house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 18 of 100: `L1-aspect-raman-mean-ws-000003`

Birth: 1993-07-18T11:39:00Z, latitude 6.9271, longitude 79.8612 (east positive) (Colombo)
Sidereal chart (Raman ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 254.94 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 93.53
  Moon: 80.55
  Mars: 142.53
  Mercury: 88.12 R
  Jupiter: 165.57
  Venus: 51.35
  Saturn: 306.87 R
  Rahu: 227.59
  Ketu: 47.59

Using the sidereal chart above (Raman ayanamsa, mean node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 8th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 19 of 100: `L1-aspect-raman-true-ws-000003`

Birth: 1936-03-06T01:05:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 37.80 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 323.78
  Moon: 119.79
  Mars: 348.32
  Mercury: 298.38
  Jupiter: 240.99
  Venus: 294.26
  Saturn: 321.60
  Rahu: 259.3
  Ketu: 79.3

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 7th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 20 of 100: `L1-aspect-raman-true-ws-000007`

Birth: 1924-01-24T20:09:00Z, latitude -33.9249, longitude 18.4241 (east positive) (Cape Town)
Sidereal chart (Raman ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 148.76 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 282.24
  Moon: 136.05
  Mars: 221.89
  Mercury: 261.47
  Jupiter: 231.36
  Venus: 315.12
  Saturn: 190.73
  Rahu: 131.0
  Ketu: 311.0

Using the sidereal chart above (Raman ayanamsa, true node, whole-sign houses), which planets cast a graha drishti (Parashari sign aspect) on the 8th house? Every planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the 5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the house itself is conjunct, not aspecting. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
