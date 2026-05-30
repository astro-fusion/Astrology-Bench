/**
 * @file src/benchmarks/phaladeepika/dataset.ts
 * @description 10-case Phaladeepika dataset focusing on Mantreswara's specific mechanics.
 */

import type { TestCase } from "../../types/index.js";

const PHD_01: TestCase = {
  id: "PHD-01",
  source: "Phaladeepika",
  tier: "EASY",
  topic: "Domestic Peace (Exalted + Retrograde)",
  prompt: "Based purely on Phaladeepika, rate my lifelong domestic peace, happiness, and property luck on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Chapter 4, Verse 7: An exalted planet that is retrograde acts like a debilitated planet. Jupiter is Exalted but Retrograde in 4H.",
  reference: { book: "Phaladeepika", chapter: "4", verse: "7" },
  tags: ["4th_house", "retrograde", "dignity_inversion"],
  chartState: {
    ascendant: "Aries",
    "4th_house_sign": "Cancer",
    "4th_lord": "Moon",
    jupiter_placement: "Cancer (4th house)",
    jupiter_dignity: "Exalted",
    jupiter_motion: "Retrograde (Vakri)",
  },
};

const PHD_02: TestCase = {
  id: "PHD-02",
  source: "Phaladeepika",
  tier: "EASY",
  topic: "Luxury & Property (Debilitated + Retrograde)",
  prompt: "Rate my lifelong capacity for domestic happiness, luxury, and property acquisition from 1 to 5. Reply with only a number.",
  goldScore: 5,
  logic: "Chapter 4, Verse 7: A debilitated planet that is retrograde acts like an exalted planet. Venus is Debilitated but Retrograde in 4H.",
  reference: { book: "Phaladeepika", chapter: "4", verse: "7" },
  tags: ["4th_house", "retrograde", "dignity_inversion"],
  chartState: {
    ascendant: "Gemini",
    "4th_house_sign": "Virgo",
    venus_placement: "Virgo (4th house)",
    venus_dignity: "Debilitated",
    venus_motion: "Retrograde (Vakri)",
  },
};

const PHD_03: TestCase = {
  id: "PHD-03",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Fortune & Spiritual Growth",
  prompt: "Rate my luck, spiritual growth, and fortune on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Mercury is Debilitated + Retrograde = Exalted Strength. But for Cancer Asc, Mercury is the 3rd and 12th lord (malefic). Exalted 12th lord in 9th house destroys fortune.",
  reference: { book: "Phaladeepika", chapter: "4", verse: "7" },
  tags: ["9th_house", "retrograde", "functional_malefic"],
  chartState: {
    ascendant: "Cancer",
    "9th_house_sign": "Pisces",
    mercury_placement: "Pisces (9th house)",
    mercury_dignity: "Debilitated",
    mercury_motion: "Retrograde (Vakri)",
    mercury_lordship: "3rd and 12th houses",
  },
};

const PHD_04: TestCase = {
  id: "PHD-04",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Luck & Education (Combustion Override)",
  prompt: "Rate my inherent luck, higher education prospects, and father's fortune on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Chapter 4, Verse 4: Combustion destroys all strength, regardless of retrograde or exalted status. Jupiter is combust within 0.5 degrees.",
  reference: { book: "Phaladeepika", chapter: "4", verse: "4" },
  tags: ["9th_house", "combustion", "jupiter"],
  chartState: {
    ascendant: "Sagittarius",
    "9th_house_sign": "Leo",
    jupiter_placement: "Leo (9th house)",
    jupiter_motion: "Retrograde (Vakri)",
    combustion_status: "Combust (within 0.5 degrees of the Sun)",
  },
};

const PHD_05: TestCase = {
  id: "PHD-05",
  source: "Phaladeepika",
  tier: "MEDIUM",
  topic: "Sade Sati Career Stability",
  prompt: "I am entering the first phase of my Saturn return (Sade Sati). Rate my career stability and emotional peace for the next two and a half years on a scale of 1 to 5. Reply with only a number.",
  goldScore: 4,
  logic: "Chapter 26: High Ashtakavarga bindus (7) in the transit house cancel the maleficence of Sade Sati, yielding productive results.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "10" },
  tags: ["transit", "sade_sati", "ashtakavarga"],
  chartState: {
    natal_moon_sign: "Aries",
    transiting_saturn_sign: "Pisces (12th from Moon)",
    saturn_ashtakavarga_in_pisces: 7,
  },
};

const PHD_06: TestCase = {
  id: "PHD-06",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Financial Expansion (Vedha Blocked)",
  prompt: "My astrologer said Jupiter is transiting my 11th house of gains. Rate my actual financial expansion and luck during this specific month on a scale of 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "Chapter 26: The 8th house is the Vedha (obstruction) point for the 11th house. Transiting Sun in 8th blocks Jupiter's 11th house gains.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "15" },
  tags: ["transit", "vedha", "jupiter"],
  chartState: {
    natal_moon_sign: "Gemini",
    transiting_jupiter: "Aries (11th from Moon)",
    transiting_sun: "Capricorn (8th from Moon)",
  },
};

const PHD_07: TestCase = {
  id: "PHD-07",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Victory & Expansion (Vama Vedha)",
  prompt: "Rate my courage, victory over competitors, and general success during this current planetary window on a scale of 1 to 5. Reply with only a number.",
  goldScore: 2,
  logic: "Chapter 26: The 12th house is the Vedha point for the 3rd house. Mars in 12th blocks Saturn's 3rd house transit benefits.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "18" },
  tags: ["transit", "vedha", "saturn"],
  chartState: {
    natal_moon_sign: "Leo",
    transiting_saturn: "Libra (3rd from Moon)",
    transiting_mars: "Cancer (12th from Moon)",
  },
};

const PHD_08: TestCase = {
  id: "PHD-08",
  source: "Phaladeepika",
  tier: "HARD",
  topic: "Romantic & Financial Luck (Kakshya)",
  prompt: "Rate my romantic luck, financial gains, and happiness for this specific week on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Chapter 26: Transit through a Kakshya with 0 bindus from its lord (Saturn) yields no results despite good house placement.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "25" },
  tags: ["transit", "kakshya", "ashtakavarga"],
  chartState: {
    natal_moon_sign: "Virgo",
    transiting_venus: "Cancer (11th from Moon)",
    current_kakshya_lord: "Saturn",
    saturn_bindu_contribution_to_venus_in_cancer: 0,
  },
};

const PHD_09: TestCase = {
  id: "PHD-09",
  source: "Phaladeepika",
  tier: "VERY_HARD",
  topic: "Jupiter 9H Transit (Loha Moorti)",
  prompt: "Rate my overall fortune, wealth, and spiritual grace for the upcoming year while Jupiter transits my 9th house on a scale of 1 to 5. Reply with only a number.",
  goldScore: 1,
  logic: "Chapter 26: Moorti Nirnaya. Jupiter in 9th from Moon is usually great, but if Moon is in 8th from natal at entry, it is Loha Moorti (Iron), turning it malefic.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "30" },
  tags: ["transit", "moorti_nirnaya", "jupiter"],
  chartState: {
    natal_moon_sign: "Taurus",
    transiting_jupiter: "Capricorn (9th from Moon)",
    transiting_moon_at_exact_time_of_jupiter_entry: "Sagittarius (8th from Natal Moon)",
  },
};

const PHD_10: TestCase = {
  id: "PHD-10",
  source: "Phaladeepika",
  tier: "VERY_HARD",
  topic: "Ashtama Shani (Swarna Moorti)",
  prompt: "Rate my overall health, stability, and protection against enemies for the next year while Saturn transits my 8th house. Reply with only a number.",
  goldScore: 4,
  logic: "Chapter 26: Moorti Nirnaya. Saturn in 8th (Ashtama Shani) is usually bad, but Moon in 1st at entry grants Swarna Moorti (Gold), erasing maleficence.",
  reference: { book: "Phaladeepika", chapter: "26", verse: "35" },
  tags: ["transit", "moorti_nirnaya", "saturn"],
  chartState: {
    natal_moon_sign: "Libra",
    transiting_saturn: "Taurus (8th from Moon)",
    transiting_moon_at_exact_time_of_saturn_entry: "Libra (1st from Natal Moon)",
  },
};

export const PHALADEEPIKA_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  PHD_01, PHD_02, PHD_03, PHD_04, PHD_05,
  PHD_06, PHD_07, PHD_08, PHD_09, PHD_10,
]);
