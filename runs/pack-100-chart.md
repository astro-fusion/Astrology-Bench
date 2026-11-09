# Astro-Bench prompt pack

100 items; input mode chart; bench 0.1.0; items sha256 `34c4f0711a46`.

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

## Item 1 of 100: `L0-positions-krishnamurti-mean-ws-000005`

Birth: 1950-02-07T04:40:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Krishnamurti (KP) ayanamsa, mean node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 2 of 100: `L0-positions-krishnamurti-true-ws-000006`

Birth: 1952-10-31T06:18:00Z, latitude 30.0444, longitude 31.2357 (east positive) (Cairo)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Krishnamurti (KP) ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 3 of 100: `L0-positions-lahiri-mean-ws-000004`

Birth: 2012-01-11T07:12:00Z, latitude 41.8781, longitude -87.6298 (east positive) (Chicago)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Lahiri ayanamsa, mean node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 4 of 100: `L0-positions-lahiri-mean-ws-000025`

Birth: 1956-04-27T12:31:00Z, latitude -6.2088, longitude 106.8456 (east positive) (Jakarta)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Lahiri ayanamsa, mean node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 5 of 100: `L0-positions-lahiri-true-ws-000007`

Birth: 2017-07-16T00:46:00Z, latitude 51.5074, longitude -0.1278 (east positive) (London)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Lahiri ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 6 of 100: `L0-positions-lahiri-true-ws-000008`

Birth: 2020-03-31T17:55:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Lahiri ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 7 of 100: `L0-positions-lahiri-true-ws-000009`

Birth: 1933-04-23T20:49:00Z, latitude 6.9271, longitude 79.8612 (east positive) (Colombo)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Lahiri ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 8 of 100: `L0-positions-raman-mean-ws-000004`

Birth: 1998-07-04T13:54:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Raman ayanamsa, mean node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 9 of 100: `L0-positions-raman-true-ws-000002`

Birth: 1920-03-04T17:36:00Z, latitude 30.0444, longitude 31.2357 (east positive) (Cairo)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Raman ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 10 of 100: `L0-positions-raman-true-ws-000006`

Birth: 1949-12-10T18:18:00Z, latitude -33.8688, longitude 151.2093 (east positive) (Sydney)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Raman ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

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
  Saturn: 50.78
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

## Item 91 of 100: `L1-yoga-gaja_kesari_classical-lahiri-mean-ws-000008`

Birth: 1986-09-05T19:53:00Z, latitude -23.5505, longitude -46.6333 (east positive) (Sao Paulo)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 305.64 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 139.28
  Moon: 158.20
  Mars: 261.68
  Mercury: 139.37
  Jupiter: 324.86 R
  Venus: 184.93
  Saturn: 220.10
  Rahu: 359.03
  Ketu: 179.03

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Gaja Kesari Yoga (BPHS definition)" hold in this chart? The rule as stated: Jupiter in a kendra from the Lagna or the Moon, joined or aspected by a benefic, and not debilitated, combust or in an enemy's sign, gives a splendid, wealthy and lasting reputation. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 92 of 100: `L1-yoga-gaja_kesari_moon_kendra-lahiri-mean-ws-000005`

Birth: 1956-08-01T18:00:00Z, latitude -34.6037, longitude -58.3816 (east positive) (Buenos Aires)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 246.14 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 106.17
  Moon: 40.66
  Mars: 329.86
  Mercury: 119.56
  Jupiter: 131.61
  Venus: 65.15
  Saturn: 212.91
  Rahu: 221.52
  Ketu: 41.52

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Gaja Kesari Yoga (Moon kendra form)" hold in this chart? The rule as stated: Jupiter in a kendra (1, 4, 7, 10) counted by sign from the Moon gives fame, wealth and lasting reputation. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 93 of 100: `L1-yoga-gaja_kesari_moon_kendra-lahiri-mean-ws-000009`

Birth: 1994-11-18T02:41:00Z, latitude 51.5074, longitude -0.1278 (east positive) (London)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 161.18 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 211.74
  Moon: 29.82
  Mars: 118.25
  Mercury: 197.28
  Jupiter: 211.51
  Venus: 189.34 R
  Saturn: 311.96
  Rahu: 200.30
  Ketu: 20.30

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Gaja Kesari Yoga (Moon kendra form)" hold in this chart? The rule as stated: Jupiter in a kendra (1, 4, 7, 10) counted by sign from the Moon gives fame, wealth and lasting reputation. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 94 of 100: `L1-yoga-gaja_kesari_moon_kendra-lahiri-mean-ws-000011`

Birth: 2005-10-24T11:18:00Z, latitude 19.4326, longitude -99.1332 (east positive) (Mexico City)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 168.64 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 187.21
  Moon: 90.82
  Mars: 25.80 R
  Mercury: 208.67
  Jupiter: 185.70
  Venus: 233.89
  Saturn: 106.61
  Rahu: 348.69
  Ketu: 168.69

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), does "Gaja Kesari Yoga (Moon kendra form)" hold in this chart? The rule as stated: Jupiter in a kendra (1, 4, 7, 10) counted by sign from the Moon gives fame, wealth and lasting reputation. Answer true or false. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 95 of 100: `L2-citation-1dc8378a5033`

Which classical text, chapter and verse defines the following yoga rule ("chandra mangala")? Rule: The Moon and Mars together make the native valorous and brave in war, an artisan and metallurgist (the conjunction effect; the later wealth-giving Chandra-Mangala yoga is not stated). Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)

## Item 96 of 100: `L2-citation-3f08c3d42198`

Which classical text, chapter and verse defines the following yoga rule ("budha aditya")? Rule: The Sun and Mercury in one sign make the native skilled, intelligent, famous and comfortable (the conjunction effect; the name Budha-Aditya is not used). Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)

## Item 97 of 100: `L2-citation-623850b3e0ab`

Which classical text, chapter and verse defines the following varga rule ("drekkana d3")? Rule: The three drekkanas of a sign are its 1st, 5th and 9th signs. Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)

## Item 98 of 100: `L2-citation-7caed961b97a`

Which classical text, chapter and verse defines the following aspect rule ("graha drishti")? Rule: All planets aspect the 7th fully; Saturn, Jupiter and Mars additionally aspect fully the 3rd and 10th, the 5th and 9th, and the 4th and 8th respectively. Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)

## Item 99 of 100: `L2-citation-a9cbd6036e8e`

Which classical text, chapter and verse defines the following yoga rule ("amala")? Rule: A benefic exclusively in the 10th from the ascendant or the Moon forms Amala yoga. Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)

## Item 100 of 100: `L2-citation-adc1fb52b58d`

Which classical text, chapter and verse defines the following aspect rule ("rasi drishti")? Rule: Signs aspect the signs in their front, excepting the sign next to them (movable signs aspect fixed signs except the adjacent one, and so on). Use the chapter and verse numbering of a standard edition and name it in "edition". Give "answer" as {"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": "<edition>"} and repeat it in citations. If you do not know, set "answer" to null and citations to []. (Convention, if it matters: Lahiri ayanamsa, mean node, whole-sign houses.)
