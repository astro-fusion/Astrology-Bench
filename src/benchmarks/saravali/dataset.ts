/**
 * @file src/benchmarks/saravali/dataset.ts
 * @description Test cases derived from Kalyana Varma's Saravali.
 *
 * Saravali is renowned for its detailed exposition on planetary combinations,
 * Raja Yogas, and Nabhasa Yogas. These test cases focus on the specific
 * interpretive nuances provided in the text.
 */

import type { TestCase } from "../../types/index.js";

/**
 * TC-SAR-01 | Akhanda Samrajya Yoga
 *
 * Saravali Rule:
 *  - If the 2nd, 9th, and 11th lords are in Kendra from the Moon, and Jupiter
 *    is the 2nd, 5th, or 11th lord, it forms a powerful wealth yoga.
 *  - Lagna is Taurus, Jupiter is the 11th lord in the 2nd (Gemini).
 *  - Moon is in Aquarius (10th house).
 *  - 9th lord (Saturn) is in Taurus (Lagna, Kendra from Moon).
 *  - 2nd lord (Mercury) is in Scorpio (7th house, Kendra from Moon).
 * Verdict: Powerful Akhanda Samrajya Yoga. Gold Score = 5.
 */
const TC_SAR_01: TestCase = {
  id: "TC-SAR-01",
  tier: "MEDIUM",
  topic: "Akhanda Samrajya Yoga",
  prompt: "Evaluate the potential for large-scale financial success and influence based on this chart. Rate 1 to 5.",
  goldScore: 5,
  chartState: {
    ascendant: "Taurus",
    moon_sign: "Aquarius",
    "2nd_lord": "Mercury in Scorpio",
    "9th_lord": "Saturn in Taurus",
    "11th_lord": "Jupiter in Gemini",
    yoga: "Akhanda Samrajya Yoga components active",
  },
};

/**
 * TC-SAR-02 | Sun in 10th House (Digbala)
 *
 * Saravali Rule:
 *  - Sun in the 10th house gives great fame, authority, and success in ventures.
 *  - Sun is in Aries (Exalted) in the 10th house for Cancer Lagna.
 *  - No malefic aspects on the Sun.
 * Verdict: Excellent professional authority. Gold Score = 5.
 */
const TC_SAR_02: TestCase = {
  id: "TC-SAR-02",
  tier: "EASY",
  topic: "Professional Authority (Sun Digbala)",
  prompt: "How much authority and fame will I achieve in my profession? Rate 1 to 5.",
  goldScore: 5,
  chartState: {
    ascendant: "Cancer",
    sun_position: "Aries in 10th house (Exalted, Digbala)",
    aspects_on_sun: "None",
  },
};

/**
 * TC-SAR-03 | Kemadruma Yoga (Affliction)
 *
 * Saravali Rule:
 *  - If there are no planets (excluding Sun) in the 2nd and 12th from the Moon,
 *    Kemadruma Yoga is formed, leading to poverty and mental distress.
 *  - Moon in Leo, 4th house.
 *  - 3rd house (Cancer) is empty.
 *  - 5th house (Virgo) is empty.
 *  - No planets in Kendras from Lagna or Moon to cancel it.
 * Verdict: Severe financial and mental hardship. Gold Score = 1.
 */
const TC_SAR_03: TestCase = {
  id: "TC-SAR-03",
  tier: "MEDIUM",
  topic: "Financial Hardship (Kemadruma Yoga)",
  prompt: "Rate the stability of my mental peace and financial status. Rate 1 to 5.",
  goldScore: 1,
  chartState: {
    ascendant: "Taurus",
    moon_sign: "Leo",
    planets_in_2nd_from_moon: "None",
    planets_in_12th_from_moon: "None",
    planets_in_kendras: "None",
  },
};

export const SARAVALI_BENCH_DATASET: ReadonlyArray<TestCase> = Object.freeze([
  TC_SAR_01,
  TC_SAR_02,
  TC_SAR_03,
]);
