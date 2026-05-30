/**
 * @file src/benchmarks/saravali/dataset.ts
 * @description Test cases derived from Kalyana Varma's Saravali.
 */

import type { TestCase } from "../../types/index.js";

const TC_SAR_01: TestCase = {
  id: "TC-SAR-01",
  tier: "MEDIUM",
  topic: "Akhanda Samrajya Yoga",
  prompt: "Evaluate the potential for large-scale financial success and influence based on this chart. Rate 1 to 5.",
  goldScore: 5,
  logic: "2nd, 9th, and 11th lords are in Kendra from the Moon; Jupiter is the 11th lord in the 2nd (Gemini); powerful wealth yoga.",
  reference: {
    book: "Saravali",
    chapter: "35",
    verse: "10-15",
  },
  tags: ["wealth", "yoga", "raja_yoga"],
  chartState: {
    ascendant: "Taurus",
    moon_sign: "Aquarius",
    "2nd_lord": "Mercury in Scorpio",
    "9th_lord": "Saturn in Taurus",
    "11th_lord": "Jupiter in Gemini",
    yoga: "Akhanda Samrajya Yoga components active",
  },
};

const TC_SAR_02: TestCase = {
  id: "TC-SAR-02",
  tier: "EASY",
  topic: "Professional Authority (Sun Digbala)",
  prompt: "How much authority and fame will I achieve in my profession? Rate 1 to 5.",
  goldScore: 5,
  logic: "Sun in the 10th house (Digbala) and exalted in Aries for Cancer Lagna gives peak professional authority.",
  reference: {
    book: "Saravali",
    chapter: "30",
    verse: "5",
  },
  tags: ["career", "digbala", "sun"],
  chartState: {
    ascendant: "Cancer",
    sun_position: "Aries in 10th house (Exalted, Digbala)",
    aspects_on_sun: "None",
  },
};

const TC_SAR_03: TestCase = {
  id: "TC-SAR-03",
  tier: "MEDIUM",
  topic: "Financial Hardship (Kemadruma Yoga)",
  prompt: "Rate the stability of my mental peace and financial status. Rate 1 to 5.",
  goldScore: 1,
  logic: "No planets in 2nd/12th from Moon; no planets in Kendras to cancel Kemadruma; leads to poverty/distress.",
  reference: {
    book: "Saravali",
    chapter: "33",
    verse: "20-25",
  },
  tags: ["wealth", "yoga", "affliction"],
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
