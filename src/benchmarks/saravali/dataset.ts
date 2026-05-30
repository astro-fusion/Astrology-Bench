/**
 * @file src/benchmarks/saravali/dataset.ts
 * @description 10-case Saravali dataset focusing on conjunctions and nuanced Yogas.
 */

import type { TestCase } from "../../types/index.js";

const SAR_01: TestCase = {
  id: "SAR-01",
  source: "Saravali",
  tier: "EASY",
  topic: "Reputation",
  prompt: "Rate my social standing potential 1-5.",
  goldScore: 5,
  logic: "Sun and Jupiter conjunction in a Kendra house gives great reputation and honors.",
  reference: { book: "Saravali", chapter: "22", verse: "10" },
  tags: ["reputation", "conjunction", "yoga"],
  chartState: {
    ascendant: "Aries",
    conjunction: "Sun and Jupiter in 4th house (Cancer)",
  },
};

const SAR_02: TestCase = {
  id: "SAR-02",
  source: "Saravali",
  tier: "EASY",
  topic: "Family Harmony",
  prompt: "Rate peace within my family 1-5.",
  goldScore: 4,
  logic: "4th lord is strong and Moon is unafflicted by malefics.",
  reference: { book: "Saravali", chapter: "24", verse: "5" },
  tags: ["family", "moon", "lordship"],
  chartState: {
    ascendant: "Taurus",
    "4th_lord": "Sun in Leo (Own Sign, 4th house)",
    moon_state: "Moon in Taurus (Exalted, 1st house)",
  },
};

const SAR_03: TestCase = {
  id: "SAR-03",
  source: "Saravali",
  tier: "MEDIUM",
  topic: "Career Partnership",
  prompt: "Rate success of business partnerships 1-5.",
  goldScore: 3,
  logic: "7th lord is strong; However, Mars aspect on the 7th house creates friction and aggressive competition.",
  reference: { book: "Saravali", chapter: "35", verse: "20" },
  tags: ["career", "partnership", "aspect"],
  chartState: {
    ascendant: "Libra",
    "7th_lord": "Mars in Scorpio (Own Sign, 2nd house)",
    "7th_house_aspects": "Mars aspect from 2nd house",
  },
};

const SAR_04: TestCase = {
  id: "SAR-04",
  source: "Saravali",
  tier: "MEDIUM",
  topic: "Spiritual Growth",
  prompt: "Rate my progress on spiritual path 1-5.",
  goldScore: 5,
  logic: "Ketu in the 9th house (Dharma) with a powerful aspect from Jupiter.",
  reference: { book: "Saravali", chapter: "31", verse: "15" },
  tags: ["spirituality", "ketu", "jupiter"],
  chartState: {
    ascendant: "Leo",
    planets_in_9th: ["Ketu"],
    "9th_house_aspects": "Jupiter aspect from 1st house (Leo)",
  },
};

const SAR_05: TestCase = {
  id: "SAR-05",
  source: "Saravali",
  tier: "MEDIUM",
  topic: "Creative Success",
  prompt: "Rate recognition for my artistic work 1-5.",
  goldScore: 4,
  logic: "Venus in the 5th house (Creativity) with Mercury's aspect, indicating refined artistic skill.",
  reference: { book: "Saravali", chapter: "15", verse: "12" },
  tags: ["creativity", "venus", "mercury"],
  chartState: {
    ascendant: "Aquarius",
    planets_in_5th: ["Venus in Gemini"],
    "5th_house_aspects": "Mercury aspect from 11th house (Sagittarius)",
  },
};

const SAR_06: TestCase = {
  id: "SAR-06",
  source: "Saravali",
  tier: "HARD",
  topic: "Hidden Enemies",
  prompt: "Rate risk of betrayal from close associates 1-5.",
  goldScore: 2,
  logic: "11th lord (gains/associates) is placed in the 6th house (enemies) with Rahu's aspect.",
  reference: { book: "Saravali", chapter: "18", verse: "40" },
  tags: ["enemies", "betrayal", "lordship"],
  chartState: {
    ascendant: "Gemini",
    "11th_lord": "Mars in Scorpio (6th house)",
    "6th_house_aspects": "Rahu aspect from 10th house (Pisces)",
  },
};

const SAR_07: TestCase = {
  id: "SAR-07",
  source: "Saravali",
  tier: "HARD",
  topic: "Inheritance",
  prompt: "Rate likelihood of receiving family wealth 1-5.",
  goldScore: 3,
  logic: "2nd and 4th lords are connected; However, the 8th lord aspects the 2nd house, causing delays/disputes.",
  reference: { book: "Saravali", chapter: "13", verse: "30" },
  tags: ["wealth", "inheritance", "aspect"],
  chartState: {
    ascendant: "Virgo",
    "2nd_lord": "Venus in Sagittarius (4th house)",
    "4th_lord": "Jupiter in Libra (2nd house)",
    "2nd_house_aspects": "Mars (8th lord) aspect from 7th house (Pisces)",
  },
};

const SAR_08: TestCase = {
  id: "SAR-08",
  source: "Saravali",
  tier: "HARD",
  topic: "Health Crisis Timing",
  prompt: "Rate risk of major health issue in next 2 years 1-5.",
  goldScore: 1,
  logic: "8th lord Mahadasha active; Saturn is transiting over the natal Moon (Sadesati influence).",
  reference: { book: "Saravali", chapter: "33", verse: "12" },
  tags: ["health", "timing", "transit"],
  chartState: {
    ascendant: "Cancer",
    current_dasha: "Saturn Mahadasha (8th lord)",
    transit_state: "Saturn transiting over natal Moon in Aquarius",
  },
};

const SAR_09: TestCase = {
  id: "SAR-09",
  source: "Saravali",
  tier: "VERY_HARD",
  topic: "Karmic Debt",
  prompt: "Rate if past-life karma is blocking current goals 1-5.",
  goldScore: 2,
  logic: "Saturn and Ketu conjunction in a Dusthana (6/8/12) with weak Shadbala, indicating heavy karmic baggage.",
  reference: { book: "Saravali", chapter: "18", verse: "55" },
  tags: ["karma", "conjunction", "shadbala"],
  chartState: {
    ascendant: "Scorpio",
    conjunction: "Saturn and Ketu in 12th house (Libra)",
    saturn_shadbala: 0.75,
  },
};

const SAR_10: TestCase = {
  id: "SAR-10",
  source: "Saravali",
  tier: "VERY_HARD",
  topic: "Multi-Generational Impact",
  prompt: "Rate how my actions will affect my descendants 1-5.",
  goldScore: 4,
  logic: "5th and 9th lords are strong; Jupiter is in its own Navamsha, indicating high-quality lineage impact.",
  reference: { book: "Saravali", chapter: "7", verse: "45" },
  tags: ["legacy", "varga", "lordship"],
  chartState: {
    ascendant: "Sagittarius",
    "5th_lord": "Mars in Aries (Own Sign, 5th house)",
    "9th_lord": "Sun in Leo (Own Sign, 9th house)",
    jupiter_navamsha: "Jupiter in Pisces in D9",
  },
};

export const SARAVALI_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  SAR_01, SAR_02, SAR_03, SAR_04, SAR_05,
  SAR_06, SAR_07, SAR_08, SAR_09, SAR_10,
]);
