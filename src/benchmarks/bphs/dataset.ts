/**
 * @file src/benchmarks/bphs/dataset.ts
 * @description 10-case BPHS dataset focusing on foundational Parashari principles.
 */

import type { TestCase } from "../../types/index.js";

const BPHS_01: TestCase = {
  id: "BPHS-01",
  source: "BPHS",
  tier: "EASY",
  topic: "Career",
  prompt: "Rate my long-term career success 1-5.",
  goldScore: 5,
  logic: "10th lord exalted in 10th house; Jupiter aspects the 10th house from a Kendra.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "19", verse: "1-5" },
  tags: ["career", "lordship", "aspect"],
  chartState: {
    ascendant: "Cancer",
    "10th_house_sign": "Aries",
    "10th_lord": "Mars in Aries (Own Sign, 10th house)",
    "10th_house_aspects": "Jupiter aspect from 4th house (Libra)",
  },
};

const BPHS_02: TestCase = {
  id: "BPHS-02",
  source: "BPHS",
  tier: "EASY",
  topic: "Marriage",
  prompt: "Rate my marriage stability 1-5.",
  goldScore: 4,
  logic: "7th lord in a friendly sign; Venus is strong and unafflicted.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "20", verse: "1-4" },
  tags: ["marriage", "lordship"],
  chartState: {
    ascendant: "Leo",
    "7th_house_sign": "Aquarius",
    "7th_lord": "Saturn in Libra (Exalted, 3rd house)",
    venus_state: "Venus in Taurus (Own Sign, 10th house)",
  },
};

const BPHS_03: TestCase = {
  id: "BPHS-03",
  source: "BPHS",
  tier: "MEDIUM",
  topic: "Wealth",
  prompt: "Rate my wealth accumulation potential 1-5.",
  goldScore: 3,
  logic: "Dhana yoga present (2nd lord in 11th); However, Ashtakavarga bindus in 2nd house are below 28 threshold.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "13", verse: "25" },
  tags: ["wealth", "ashtakavarga"],
  chartState: {
    ascendant: "Taurus",
    "2nd_lord": "Mercury in Pisces (11th house)",
    "11th_lord": "Jupiter in Gemini (2nd house)",
    ashtakavarga_2nd_house_bindus: 22,
  },
};

const BPHS_04: TestCase = {
  id: "BPHS-04",
  source: "BPHS",
  tier: "MEDIUM",
  topic: "Children",
  prompt: "Rate ease of having children 1-5.",
  goldScore: 2,
  logic: "5th lord is combust by Sun; Jupiter (karaka) is debilitated in D1.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "16", verse: "1-10" },
  tags: ["children", "combustion", "karaka"],
  chartState: {
    ascendant: "Virgo",
    "5th_lord": "Saturn in Leo (12th house, Combust)",
    jupiter_state: "Jupiter in Capricorn (Debilitated, 5th house)",
  },
};

const BPHS_05: TestCase = {
  id: "BPHS-05",
  source: "BPHS",
  tier: "MEDIUM",
  topic: "Fame",
  prompt: "Rate my public recognition potential 1-5.",
  goldScore: 4,
  logic: "Gaja Kesari Yoga (Jupiter and Moon in mutual Kendras); Favorable Mahadasha active.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "35", verse: "1-3" },
  tags: ["fame", "yoga", "gaja_kesari"],
  chartState: {
    ascendant: "Aries",
    moon_position: "Cancer (4th house)",
    jupiter_position: "Capricorn (10th house)",
    current_dasha: "Jupiter Mahadasha",
  },
};

const BPHS_06: TestCase = {
  id: "BPHS-06",
  source: "BPHS",
  tier: "HARD",
  topic: "Career Volatility",
  prompt: "Rate my career resilience through crises 1-5.",
  goldScore: 1,
  logic: "D1 shows exalted Sun (10th lord); However, D10 (Dashamsha) shows 10th lord debilitated in the 8th house.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "7", verse: "10" },
  tags: ["career", "varga", "d10"],
  chartState: {
    ascendant: "Scorpio",
    D1_10th_lord: "Sun in Aries (Exalted, 6th house)",
    D10_10th_lord: "Sun in Libra (Debilitated, 8th house in D10)",
  },
};

const BPHS_07: TestCase = {
  id: "BPHS-07",
  source: "BPHS",
  tier: "HARD",
  topic: "Marriage Breakdown",
  prompt: "Rate true structural strength of my relationships 1-5.",
  goldScore: 2,
  logic: "D1 Venus exalted; However, D9 (Navamsha) shows Venus debilitated in the 6th house.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "7", verse: "12" },
  tags: ["marriage", "varga", "d9"],
  chartState: {
    ascendant: "Aries",
    D1_venus: "Exalted in Pisces (12th house)",
    D9_venus: "Debilitated in Virgo (6th house in D9)",
  },
};

const BPHS_08: TestCase = {
  id: "BPHS-08",
  source: "BPHS",
  tier: "HARD",
  topic: "Sudden Windfall",
  prompt: "Rate potential for unexpected financial reversal 1-5.",
  goldScore: 5,
  logic: "Vipareeta Raja Yoga: 6th, 8th, and 12th lords all posited in the 8th house.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "38", verse: "1-10" },
  tags: ["wealth", "vipareeta_yoga"],
  chartState: {
    ascendant: "Libra",
    "6th_lord": "Jupiter in Taurus (8th house)",
    "8th_lord": "Venus in Taurus (8th house)",
    "12th_lord": "Mercury in Taurus (8th house)",
  },
};

const BPHS_09: TestCase = {
  id: "BPHS-09",
  source: "BPHS",
  tier: "VERY_HARD",
  topic: "Perception vs Reality",
  prompt: "Rate how the world perceives my wealth 1-5.",
  goldScore: 5,
  logic: "Arudha Lagna (AL) is packed with exalted planets, creating a facade of immense wealth.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "29", verse: "1-10" },
  tags: ["wealth", "arudha_lagna"],
  chartState: {
    ascendant: "Leo",
    arudha_lagna: "Sagittarius",
    planets_in_al: ["Exalted Jupiter", "Exalted Sun"],
  },
};

const BPHS_10: TestCase = {
  id: "BPHS-10",
  source: "BPHS",
  tier: "VERY_HARD",
  topic: "Hidden Karma",
  prompt: "Rate my internal peace despite outward success 1-5.",
  goldScore: 1,
  logic: "Dasha lord is placed in 'Ghora' (Terrible) Shashtiamsa (D60), indicating severe internal distress.",
  reference: { book: "Brihat Parashara Hora Shastra", chapter: "7", verse: "38" },
  tags: ["karma", "shashtiamsa", "d60"],
  chartState: {
    ascendant: "Aquarius",
    current_dasha: "Rahu Mahadasha",
    dasha_lord_shashtiamsa: "Ghora (D60)",
  },
};

export const BPHS_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  BPHS_01, BPHS_02, BPHS_03, BPHS_04, BPHS_05,
  BPHS_06, BPHS_07, BPHS_08, BPHS_09, BPHS_10,
]);
