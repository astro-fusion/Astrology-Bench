# Astro-Bench prompt pack, chunk 10 of 10 (items 91-100 of 100, input mode chart)

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
