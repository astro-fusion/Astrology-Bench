/**
 * @file src/benchmarks/bphs/dataset.ts
 * @description The immutable gold-standard BPHS-Bench test cases.
 *
 * Each gold score is derived from strict BPHS text analysis.
 */

import type { TestCase } from "../../types/index.js";

const TC_EASY_01: TestCase = {
  id: "TC-EASY-01",
  tier: "EASY",
  topic: "Career Growth Baseline",
  prompt: "On a scale of 1 to 5, how steady will my career growth be over the next few years? Reply with only a number.",
  goldScore: 5,
  logic: "10th lord Mars in own sign Aries in 10th house; Jupiter aspects 10th house from 2nd; Active Mars Mahadasha; High Ashtakavarga bindus (34).",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "19",
    verse: "1-5",
  },
  tags: ["career", "lordship", "ashtakavarga"],
  chartState: {
    ascendant: "Cancer",
    "10th_house_sign": "Aries",
    "10th_lord": "Mars in Aries (Own Sign, 10th house)",
    "10th_house_aspects": "Jupiter aspect from 2nd house (Leo)",
    current_dasha: "Mars Mahadasha",
    ashtakavarga_10th_house_bindus: 34,
  },
};

const TC_EASY_02: TestCase = {
  id: "TC-EASY-02",
  tier: "EASY",
  topic: "Marriage Promise Baseline",
  prompt: "Rate my chances of a harmonious, long-lasting marriage on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "7th lord Venus debilitated in Virgo; Saturn and Rahu afflict the 7th house; Low Ashtakavarga bindus (19).",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "20",
    verse: "10-12",
  },
  tags: ["marriage", "debility", "malefics"],
  chartState: {
    ascendant: "Scorpio",
    "7th_house_sign": "Taurus",
    "7th_lord": "Venus in Virgo (Debilitated, 11th house)",
    "7th_house_planets": ["Saturn", "Rahu"],
    ashtakavarga_7th_house_bindus: 19,
  },
};

const TC_MED_03: TestCase = {
  id: "TC-MED-03",
  tier: "MEDIUM",
  topic: "Wealth Stability vs. Bindu Capacity",
  prompt: "How likely am I to build and keep long-term wealth? Rate 1 to 5. Reply with only a number.",
  goldScore: 3,
  logic: "Parivartana Yoga between 2nd and 11th lords; However, 2nd lord is debilitated and both houses have low bindus (<25).",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "13",
    verse: "25",
  },
  tags: ["wealth", "parivartana", "ashtakavarga"],
  chartState: {
    ascendant: "Taurus",
    "2nd_house_sign": "Gemini",
    "11th_house_sign": "Pisces",
    "2nd_lord": "Mercury in Pisces (11th house, Debilitated)",
    "11th_lord": "Jupiter in Gemini (2nd house)",
    parivartana_yoga: "2nd and 11th lords exchange houses",
    ashtakavarga_2nd_house_bindus: 21,
    ashtakavarga_11th_house_bindus: 22,
    current_dasha: "Jupiter Mahadasha",
  },
};

const TC_MED_04: TestCase = {
  id: "TC-MED-04",
  tier: "MEDIUM",
  topic: "Children & Legacy Varga Trap",
  prompt: "Rate how smoothly I can expect my journey to parenthood to go, 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "Strong D1 indicators (Exalted Venus/Jupiter) are subverted by D5 where Venus is debilitated and Jupiter is in 8th house.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "7",
    verse: "15-20",
  },
  tags: ["children", "varga", "d5"],
  chartState: {
    ascendant: "Gemini",
    "5th_house_sign": "Libra",
    D1_5th_lord: "Venus in Pisces (Exalted, 10th house)",
    D1_jupiter_karaka: "Exalted in Cancer (2nd house)",
    D5_panchamsha_5th_lord: "Venus in Virgo (Debilitated in D5)",
    D5_jupiter_karaka: "Placed in the 8th house of D5",
    current_dasha: "Venus Mahadasha",
  },
};

const TC_MED_05: TestCase = {
  id: "TC-MED-05",
  tier: "MEDIUM",
  topic: "Public Recognition Combustion Filter",
  prompt: "How likely am I to gain public recognition or fame in my field? 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "10th lord Mercury is exactly conjunct Sun (Combust), neutralising its power despite 9th house placement.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "3",
    verse: "45",
  },
  tags: ["career", "combustion", "mercury"],
  chartState: {
    ascendant: "Sagittarius",
    "10th_house_sign": "Virgo",
    "10th_lord": "Mercury in Leo (9th house)",
    "9th_lord": "Sun in Leo (9th house)",
    planetary_conjunction: "Mercury is within 0.5 degrees of the Sun",
    current_dasha: "Mercury Mahadasha",
  },
};

const TC_HARD_06: TestCase = {
  id: "TC-HARD-06",
  tier: "HARD",
  topic: "Relationship Longevity Varga Subversion",
  prompt: "Rate my marriage prospects for stability and happiness, 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "D1 7th lord exalted but in 12th; D9 shows Venus debilitated; low 7th house bindus (17).",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "7",
    verse: "30-35",
  },
  tags: ["marriage", "varga", "d9", "12th_house"],
  chartState: {
    ascendant: "Aries",
    "7th_house_sign": "Libra",
    D1_7th_lord: "Venus in Pisces (Exalted, 12th house)",
    D9_navamsha_7th_lord: "Venus in Virgo (Debilitated in D9)",
    ashtakavarga_7th_house_bindus: 17,
    current_dasha: "Venus Mahadasha",
  },
};

const TC_HARD_07: TestCase = {
  id: "TC-HARD-07",
  tier: "HARD",
  topic: "Business Success Vipareeta Evaluation",
  prompt: "Rate my potential for successful, self-sustaining business wealth, 1 to 5. Reply with only a number.",
  goldScore: 3,
  logic: "Harsha and Sarala Vipareeta Raja Yogas present; however, Mars Shadbala is low (0.85), limiting the results.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "38",
    verse: "10-15",
  },
  tags: ["wealth", "vipareeta_yoga", "shadbala"],
  chartState: {
    ascendant: "Virgo",
    "6th_lord": "Saturn in Aries (8th house, Debilitated)",
    "8th_lord": "Mars in Aquarius (6th house)",
    mutual_exchange: "6th and 8th lords exchange houses (Harsha/Sarala Yoga)",
    shadbala_mars: 0.85,
    current_dasha: "Mars Mahadasha",
  },
};

const TC_HARD_08: TestCase = {
  id: "TC-HARD-08",
  tier: "HARD",
  topic: "Physical Vitality & Resilience",
  prompt: "Rate my overall physical resilience and health stability, 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "1st lord in 12th; 8th lord aspects 1st lord; Moon is weak/Amavasya; Active Saturn dasha.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "11",
    verse: "5-10",
  },
  tags: ["health", "lordship", "moon"],
  chartState: {
    ascendant: "Cancer",
    "1st_lord": "Moon in Gemini (12th house)",
    "8th_lord": "Saturn in Sagittarius (6th house, aspects 12th house Moon)",
    moon_paksha_bala: "Weak New Moon phase",
    current_dasha: "Saturn Mahadasha",
  },
};

const TC_VHARD_09: TestCase = {
  id: "TC-VHARD-09",
  tier: "VERY_HARD",
  topic: "Financial Windfall Blocked Timing Window",
  prompt: "Rate my chances of a major financial windfall or inheritance in the next 18 months, 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Neecha Bhanga exists but timing is blocked by debilitated/retrograde Pratyantar lord in 8th, Saturn transit over Moon, and low 2H bindus.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "22",
    verse: "40-45",
  },
  tags: ["wealth", "timing", "transit", "neecha_bhanga"],
  chartState: {
    ascendant: "Leo",
    "9th_lord": "Mars in Cancer (12th house, Debilitated)",
    dispositor_state: "Moon is in Scorpio (Kendra from Lagna)",
    neecha_bhanga: "Active via dispositor placement",
    current_pratyantar_dasha_lord: "Mercury retrograde in Pisces (8th house, Debilitated)",
    transit_state: "Saturn transiting exactly over natal Moon degree",
    ashtakavarga_2nd_house_bindus: 20,
  },
};

const TC_VHARD_10: TestCase = {
  id: "TC_VHARD_10",
  tier: "VERY_HARD",
  topic: "Relationship Peace Dialectical Contradiction",
  prompt: "Rate the long-term emotional peace and compatibility in my primary relationship, 1 to 5. Reply with only a number.",
  goldScore: 3,
  logic: "Dialectical contradiction: D1 7L debilitated, D9 7L exalted; Upapada Lagna afflicted by Rahu/Mars; Mixed signals amplified by Rahu Dasha.",
  reference: {
    book: "Brihat Parashara Hora Shastra",
    chapter: "7",
    verse: "50-55",
  },
  tags: ["marriage", "varga", "upapada", "rahu"],
  chartState: {
    ascendant: "Aquarius",
    "7th_lord": "Sun in Libra (9th house, Debilitated)",
    upapada_lagna_sign: "Scorpio",
    upapada_lagna_planets: ["Rahu", "Mars"],
    D9_navamsha_7th_lord: "Sun in Aries (Exalted in D9)",
    current_dasha: "Rahu Mahadasha",
  },
};

export const BPHS_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  TC_EASY_01,
  TC_EASY_02,
  TC_MED_03,
  TC_MED_04,
  TC_MED_05,
  TC_HARD_06,
  TC_HARD_07,
  TC_HARD_08,
  TC_VHARD_09,
  TC_VHARD_10,
]);
