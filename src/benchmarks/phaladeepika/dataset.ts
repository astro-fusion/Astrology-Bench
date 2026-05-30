/**
 * @file src/benchmarks/phaladeepika/dataset.ts
 * @description 10-case Phaladeepika dataset focusing on Ashtakavarga and Predictive nuances.
 */

import type { TestCase } from "../../types/index.js";

const PHD_01: TestCase = {
  id: "PHD-01",
  source: "Phaladeepika",
  tier: "EASY",
  topic: "Career",
  prompt: "Rate my professional growth stability 1-5.",
  goldScore: 5,
  logic: "10th house Ashtakavarga bindus > 30; Benefic Jupiter transit over the 10th house.",
  reference: { book: "Phaladeepika", chapter: "28", verse: "10" },
  tags: ["career", "ashtakavarga", "transit"],
  chartState: {
    ascendant: "Leo",
    ashtakavarga_10th_house_bindus: 32,
    transit_state: "Jupiter transiting 10th house (Taurus)",
  },
};

const PHD_02: TestCase = {
  id: "PHD-02",
  source: "Phaladeepika",
  tier: "EASY",
  topic: "Health",
  prompt: "Rate my physical resilience 1-5.",
  goldScore: 4,
  logic: "1st lord is strong in a Kendra; Moon Shadbala is high (>1.5).",
  reference: { book: "Phaladeepika", chapter: "4", verse: "1-5" },
  tags: ["health", "shadbala", "lordship"],
  chartState: {
    ascendant: "Cancer",
    "1st_lord": "Moon in Taurus (Exalted, 11th house)",
    moon_shadbala: 1.6,
  },
};

const PHD_03: TestCase = {
  id: "PHD-03",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Marriage Timing",
  prompt: "Rate likelihood of marriage in next 3 years 1-5.",
  goldScore: 3,
  logic: "7th lord transit is favorable (transiting 7th house); However, 7th house Ashtakavarga is low (22 bindus).",
  reference: { book: "Phaladeepika", chapter: "28", verse: "15" },
  tags: ["marriage", "timing", "ashtakavarga"],
  chartState: {
    ascendant: "Scorpio",
    "7th_lord": "Venus transiting 7th house (Taurus)",
    ashtakavarga_7th_house_bindus: 22,
  },
};

const PHD_04: TestCase = {
  id: "PHD-04",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Wealth Flow",
  prompt: "Rate my year-over-year financial growth 1-5.",
  goldScore: 2,
  logic: "11th lord is strong in D1; However, Saturn is transiting over the 2nd house (Dhana Bhava), causing blockages.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "5" },
  tags: ["wealth", "transit", "saturn"],
  chartState: {
    ascendant: "Aquarius",
    "11th_lord": "Jupiter in Pisces (Own Sign, 2nd house)",
    transit_state: "Saturn transiting 2nd house (Pisces)",
  },
};

const PHD_05: TestCase = {
  id: "PHD-05",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Travel/Relocation",
  prompt: "Rate success of moving abroad for work 1-5.",
  goldScore: 4,
  logic: "12th lord (foreign) placed in the 9th house (long journeys) with Jupiter's aspect.",
  reference: { book: "Phaladeepika", chapter: "12", verse: "20" },
  tags: ["travel", "foreign", "lordship"],
  chartState: {
    ascendant: "Gemini",
    "12th_lord": "Venus in Aquarius (9th house)",
    "9th_house_aspects": "Jupiter aspect from 1st house (Gemini)",
  },
};

const PHD_06: TestCase = {
  id: "PHD-06",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Career Shift",
  prompt: "Rate success of changing industries now 1-5.",
  goldScore: 1,
  logic: "Dasha lord has very low bindus in its own Ashtakavarga; Malefic Rahu transiting over the 10th lord.",
  reference: { book: "Phaladeepika", chapter: "28", verse: "30" },
  tags: ["career", "ashtakavarga", "transit"],
  chartState: {
    ascendant: "Aries",
    current_dasha: "Mars Mahadasha",
    mars_bindus_in_own_av: 2,
    transit_state: "Rahu transiting over natal Saturn (10th lord)",
  },
};

const PHD_07: TestCase = {
  id: "PHD-07",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Relationship Peace",
  prompt: "Rate emotional harmony in current relationship 1-5.",
  goldScore: 3,
  logic: "Venus is strong in D1 (Own sign); However, it is combust by Sun and the 7th house has very low bindus (18).",
  reference: { book: "Phaladeepika", chapter: "20", verse: "15" },
  tags: ["marriage", "combustion", "ashtakavarga"],
  chartState: {
    ascendant: "Taurus",
    venus_state: "Venus in Taurus (Own Sign, 1st house, Combust)",
    ashtakavarga_7th_house_bindus: 18,
  },
};

const PHD_08: TestCase = {
  id: "PHD-08",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Sudden Loss",
  prompt: "Rate risk of unexpected financial loss this year 1-5.",
  goldScore: 2,
  logic: "8th lord (loss) is transiting the 2nd house; 2nd and 11th houses have low Ashtakavarga bindus (<20).",
  reference: { book: "Phaladeepika", chapter: "26", verse: "12" },
  tags: ["wealth", "loss", "transit"],
  chartState: {
    ascendant: "Virgo",
    "8th_lord": "Mars transiting 2nd house (Libra)",
    ashtakavarga_2nd_house_bindus: 19,
    ashtakavarga_11th_house_bindus: 17,
  },
};

const PHD_09: TestCase = {
  id: "PHD-09",
  source: "Phaladeepika",
  tier: "VERY_HARD",
  topic: "Transit Override",
  prompt: "Rate if a major opportunity will materialize in 6 months 1-5.",
  goldScore: 1,
  logic: "Current Dasha is favorable; However, the transiting planet has <20 bindus in the transit house (Phaladeepika Ch.28 override).",
  reference: { book: "Phaladeepika", chapter: "28", verse: "42" },
  tags: ["timing", "ashtakavarga", "transit"],
  chartState: {
    ascendant: "Capricorn",
    current_dasha: "Jupiter Mahadasha (Exalted in D1)",
    transit_ashtakavarga_bindus: 18,
  },
};

const PHD_10: TestCase = {
  id: "PHD-10",
  source: "Phaladeepika",
  tier: "VERY_HARD",
  topic: "Multi-Transit Synthesis",
  prompt: "Rate overall life momentum for next 18 months 1-5.",
  goldScore: 4,
  logic: "Simultaneous favorable transits of Jupiter and Saturn into houses with high Ashtakavarga bindus (>30).",
  reference: { book: "Phaladeepika", chapter: "28", verse: "50" },
  tags: ["transit", "ashtakavarga", "timing"],
  chartState: {
    ascendant: "Pisces",
    ashtakavarga_jupiter_transit_house: 34,
    ashtakavarga_saturn_transit_house: 31,
  },
};

export const PHALADEEPIKA_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  PHD_01, PHD_02, PHD_03, PHD_04, PHD_05,
  PHD_06, PHD_07, PHD_08, PHD_09, PHD_10,
]);
