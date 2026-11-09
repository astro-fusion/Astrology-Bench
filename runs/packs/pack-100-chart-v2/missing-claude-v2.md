# Astro-Bench prompt pack pack-100.manifest.json, selected items (items 1-8 of 8, input mode chart)

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

## Item 1 of 8: `L0-positions-raman-true-ws-000006`

Birth: 1962-01-25T22:36:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)

From the birth data above alone, compute the sidereal position of each graha and the Lagna using Raman ayanamsa, true node, whole-sign houses. Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, 2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": "<sign>"}. Ketu is exactly opposite Rahu. No citation is required for this task; set citations to [] unless you want to name the source of your method.

## Item 2 of 8: `L1-combustion-lahiri-mean-ws-000033`

Birth: 1910-12-27T15:08:00Z, latitude 51.5074, longitude -0.1278 (east positive) (London)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 62.81 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 252.40
  Moon: 208.29
  Mars: 222.36
  Mercury: 271.89
  Jupiter: 196.22
  Venus: 259.88
  Saturn: 7.11 R
  Rahu: 24.06
  Ketu: 204.06

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), which planets are combust? Use the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 (12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; Rahu and Ketu are never combust. Give "answer" as a list of planet names, [] if none. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 3 of 8: `L1-dignity-krishnamurti-true-ws-000004`

Birth: 1955-07-06T04:38:00Z, latitude -6.2088, longitude 106.8456 (east positive) (Jakarta)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 167.97 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 80.21
  Moon: 270.93
  Mars: 93.52
  Mercury: 59.75
  Jupiter: 101.60
  Venus: 64.64
  Saturn: 201.50 R
  Rahu: 243.3
  Ketu: 63.3

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), what is the dignity of Moon? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 4 of 8: `L1-dignity-krishnamurti-true-ws-000005`

Birth: 1924-01-31T17:34:00Z, latitude -1.2921, longitude 36.8219 (east positive) (Nairobi)
Sidereal chart (Krishnamurti (KP) ayanamsa, true node, whole-sign houses):
  Lagna (ascendant): 135.45 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 287.89
  Moon: 230.86
  Mars: 224.96
  Mercury: 263.05
  Jupiter: 231.20
  Venus: 322.20
  Saturn: 189.54
  Rahu: 129.6
  Ketu: 309.6

Using the sidereal chart above (Krishnamurti (KP) ayanamsa, true node, whole-sign houses), what is the dignity of Saturn? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 5 of 8: `L1-dignity-lahiri-mean-ws-000038`

Birth: 1937-11-19T08:35:00Z, latitude -45.0312, longitude 168.6626 (east positive) (Queenstown)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 41.65 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 213.61
  Moon: 48.02
  Mars: 282.63
  Mercury: 225.49
  Jupiter: 270.88
  Venus: 195.18
  Saturn: 335.50 R
  Rahu: 223.48
  Ketu: 43.48

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), what is the dignity of Venus? Choose one of: moolatrikona, exalted, debilitated, own, friend, enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by the BPHS degree ranges; when several apply, report the first in the order moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) relation of the planet to the lord of the sign it occupies. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 6 of 8: `L1-lordship-raman-mean-ws-000009`

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

## Item 7 of 8: `L1-varga-lahiri-mean-ws-000004`

Birth: 1977-11-27T06:56:00Z, latitude 19.4326, longitude -99.1332 (east positive) (Mexico City)
Sidereal chart (Lahiri ayanamsa, mean node, whole-sign houses):
  Lagna (ascendant): 138.50 deg
  Body: sidereal longitude deg (R = retrograde)
  Sun: 221.37
  Moon: 58.34
  Mars: 106.51
  Mercury: 241.56
  Jupiter: 70.74 R
  Venus: 207.92
  Saturn: 126.81
  Rahu: 168.84
  Ketu: 348.84

Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Mercury occupy in the D9 Navamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.

## Item 8 of 8: `L1-varga-lahiri-true-ws-000007`

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
  Rahu: 255.2
  Ketu: 75.2

Using the sidereal chart above (Lahiri ayanamsa, true node, whole-sign houses) and the Parashari (BPHS) varga rules, which sign does Rahu occupy in the D10 Dasamsa chart? Give "answer" as the sign name. Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that supports your answer. If you cannot cite one, set citations to [] and say so.
