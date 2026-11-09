# Astro-Bench prompt pack, chunk 01 of 10 (items 1-10 of 100, input mode chart)

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
